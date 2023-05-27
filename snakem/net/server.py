# -*- coding: utf-8 -*-

# *************************************************************************
#
#  This file is part of Snake-M.
#
#  Copyright © 2014 Mark Ross <krazkidd@gmail.com>
#
#  Snake-M is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Snake-M is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Snake-M.  If not, see <http://www.gnu.org/licenses/>.
#
# *************************************************************************

import logging
import socket
import select
import time

from ..config import server as config
from ..game import game
from ..enums import GameState, MsgType

from . import net

class Server:
    def __init__(self):
        self._health_check_socket: socket.socket
        self._socket: socket.socket

        self._poll = select.poll()

        # self.active_players maps net addresses to tuples of (r, s) where:
        #   r = ready status (MsgType.{NOT_,}READY)
        #   s = snake id when a game is running
        self._players: dict[tuple[str, int], tuple[MsgType, int | None]] = dict()

        self._game_state: GameState = GameState.LOBBY
        self._game: game.Game

    def start(self) -> None:
        self._health_check_socket = net.init_health_check_socket((config.BIND_ADDR, config.BIND_PORT_HEALTH_CHECK))
        self._socket = net.init_server_socket((config.BIND_ADDR, config.BIND_PORT))

        self._poll.register(self._health_check_socket, select.POLLIN)
        self._poll.register(self._socket, select.POLLIN)

        logging.info('Health check listening on port %s.', config.BIND_PORT_HEALTH_CHECK)
        logging.info('Server listening on port %s.', config.BIND_PORT)

        last_step_time = time.monotonic_ns()

        try:
            while 1:
                if self._game_state == GameState.GAME:
                    inputs = self._poll.poll(net.TIMEOUT)
                else:
                    # we block on this call so we're not wasting cycles outside of an active game
                    inputs = self._poll.poll()

                for fd, event in inputs:
                    if fd == self._health_check_socket.fileno():
                        conn, addr = self._health_check_socket.accept()
                        conn.shutdown(socket.SHUT_RDWR)
                        conn.close()
                    elif fd == self._socket.fileno():
                        address, msg_type, msg_body = net.receive_message(self._socket)

                        if self._game_state == GameState.GAME:
                            self._handle_game_message(address, msg_type, msg_body)
                        else:
                            self._handle_lobby_message(address, msg_type, msg_body)

                if self._game_state == GameState.GAME:
                    now = time.monotonic_ns()

                    if (now - last_step_time) // 1_000_000 >= config.STEP_TIME_MS:
                        last_step_time = now

                        self._game.tick()

                        for addr in self._players:
                            for snake_id, snake in self._game.snakes.items():
                                logging.debug('(%s, %s)', snake.body[0][0], snake.body[0][1])
                                net.send_snake_update(self._socket, addr, self._game.tick_num, snake_id, snake)

                        # end game when all snakes are dead
                        #TODO the game should end when at most *one* snake is alive
                        for snake in self._game.snakes.values():
                            if snake.is_alive:
                                break
                        else:
                            for addr in self._players:
                                net.send_lobby_join_request(self._socket, addr)

                            self._start_lobby_mode()
        except Exception:
            logging.exception('Unknown exception.')
        finally:
            self._health_check_socket.close()
            self._socket.close()

    def _handle_lobby_message(self, address: tuple[str, int], msg_type: MsgType, msg_body: bytes) -> None:
        if address in self._players:
            status, snake_id = self._players[address]

            if msg_type == MsgType.LOBBY_JOIN:
                net.send_lobby_join_request(self._socket, address)  # LOBBY_JOIN is used for join confirmation
                self._players[address] = (MsgType.NOT_READY, snake_id)  # reset READY status
            elif msg_type == MsgType.LOBBY_QUIT:
                del self._players[address]
            elif msg_type == MsgType.READY:
                self._players[address] = (MsgType.READY, snake_id)

                for addr, player_tuple in self._players.items():
                    if player_tuple[0] != MsgType.READY:
                        break
                else:
                    self._start_game_mode(config.WIN_WIDTH, config.WIN_HEIGHT)
            elif msg_type == MsgType.NOT_READY:
                self._players[address] = (MsgType.NOT_READY, snake_id)
        else:
            if msg_type == MsgType.LOBBY_JOIN:
                if len(self._players) < 4:
                    net.send_lobby_join_request(self._socket, address)  # LOBBY_JOIN is used for join confirmation
                    self._players[address] = (MsgType.NOT_READY, None)
                else:
                    net.send_quit_message(self._socket, address)  # LOBBY_QUIT is used for join rejection

    def _handle_game_message(self, address: tuple[str, int], msg_type: MsgType, msg_body: bytes) -> None:
        if address in self._players:
            do_update_clients = False

            if msg_type == MsgType.INPUT:
                self._game.snakes[self._players[address][1]].change_heading(net.unpack_input_message(msg_body)) # type: ignore
                do_update_clients = True

            if do_update_clients:
                for addr in self._players:
                    net.send_pellet_update(self._socket, addr, self._game.tick_num, 0, self._game.pellet)

                    for snake_id, snake in self._game.snakes.items():
                        net.send_snake_update(self._socket, addr, self._game.tick_num, snake_id, snake)

    def _start_lobby_mode(self) -> None:
        self._game_state = GameState.LOBBY

    def _start_game_mode(self, width: int, height: int) -> None:
        self._game_state = GameState.GAME

        self._game = game.Game(width, height)

        for addr, player_tuple in self._players.items():
            self._players[addr] = (player_tuple[0], self._game.spawn_new_snake())

        self._game.spawn_new_pellet()

        for addr in self._players:
            net.send_pellet_update(self._socket, addr, self._game.tick_num, 0, self._game.pellet)

            for snake_id, snake in self._game.snakes.items():
                net.send_snake_update(self._socket, addr, self._game.tick_num, snake_id, snake)

        for addr in self._players:
            net.send_start_message(self._socket, addr, self._game.width, self._game.height)

if __name__ == '__main__':
    #TODO add timestamp (with format)
    #logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    Server().start()
