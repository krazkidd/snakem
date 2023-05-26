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

import select
import socket
import logging

from ..config import server as config
from ..game import game
from ..enums import GameState, MsgType

from . import net

class Server:
    def __init__(self):
        self._socket: socket.socket

        self.server_state: GameState = GameState.LOBBY

        # self.active_players maps net addresses to tuples of (r, s) where:
        #   r = ready status (MsgType.{NOT_,}READY)
        #   s = snake id when a game is running
        self.active_players: dict[tuple[str, int], tuple[MsgType, int | None]] = dict()

        self.game: game.Game

    def start(self) -> None:
        self._socket = net.init_server_socket((config.BIND_ADDR, config.BIND_PORT))

        logging.info('Listening on port %s.', config.BIND_PORT)

        tick_time = 0.0

        try:
            while True:
                if self.server_state == GameState.GAME:
                    readable, _, _ = select.select([self._socket], [], [], net.TIMEOUT)
                else:
                    # we block on this call so we're not wasting cycles outside of an active game
                    readable, _, _ = select.select([self._socket], [], [])

                if self._socket in readable:
                    address, msg_type, msg_body = net.receive_message(self._socket)

                    if self.server_state == GameState.GAME:
                        self._handle_game_message(address, msg_type, msg_body)
                    else:
                        self._handle_lobby_message(address, msg_type, msg_body)

                if self.server_state == GameState.GAME:
                    tick_time += net.TIMEOUT
                    if tick_time >= config.STEP_TIME:
                        tick_time -= config.STEP_TIME
                        self.game.tick()

                        for addr in self.active_players:
                            for snake_id, snake in self.game.snakes.items():
                                logging.debug('(%s, %s)', snake.body[0][0], snake.body[0][1])
                                net.send_snake_update(self._socket, addr, self.game.tick_num, snake_id, snake)

                        # end game when all snakes are dead
                        #TODO the game should end when at most *one* snake is alive
                        for snake in self.game.snakes.values():
                            if snake.is_alive:
                                break
                        else:
                            for addr in self.active_players:
                                net.send_lobby_join_request(self._socket, addr)

                            self._start_lobby_mode()
        except Exception:
            logging.exception('Unknown exception.')
        finally:
            self._socket.close()

    def _handle_lobby_message(self, address: tuple[str, int], msg_type: MsgType, msg_body: bytes) -> None:
        if address in self.active_players:
            status, snake_id = self.active_players[address]

            if msg_type == MsgType.LOBBY_JOIN:
                net.send_lobby_join_request(self._socket, address)  # LOBBY_JOIN is used for join confirmation
                self.active_players[address] = (MsgType.NOT_READY, snake_id)  # reset READY status
            elif msg_type == MsgType.LOBBY_QUIT:
                del self.active_players[address]
            elif msg_type == MsgType.READY:
                self.active_players[address] = (MsgType.READY, snake_id)

                for addr, player_tuple in self.active_players.items():
                    if player_tuple[0] != MsgType.READY:
                        break
                else:
                    self._start_game_mode(config.WIN_WIDTH, config.WIN_HEIGHT)
            elif msg_type == MsgType.NOT_READY:
                self.active_players[address] = (MsgType.NOT_READY, snake_id)
        else:
            if msg_type == MsgType.LOBBY_JOIN:
                if len(self.active_players) < 4:
                    net.send_lobby_join_request(self._socket, address)  # LOBBY_JOIN is used for join confirmation
                    self.active_players[address] = (MsgType.NOT_READY, None)
                else:
                    net.send_quit_message(self._socket, address)  # LOBBY_QUIT is used for join rejection

    def _handle_game_message(self, address: tuple[str, int], msg_type: MsgType, msg_body: bytes) -> None:
        if address in self.active_players:
            do_update_clients = False

            if msg_type == MsgType.INPUT:
                self.game.snakes[self.active_players[address][1]].change_heading(net.unpack_input_message(msg_body)) # type: ignore
                do_update_clients = True

            if do_update_clients:
                for addr in self.active_players:
                    net.send_pellet_update(self._socket, addr, self.game.tick_num, 0, self.game.pellet)

                    for snake_id, snake in self.game.snakes.items():
                        net.send_snake_update(self._socket, addr, self.game.tick_num, snake_id, snake)

    def _start_lobby_mode(self) -> None:
        self.server_state = GameState.LOBBY

    def _start_game_mode(self, width: int, height: int) -> None:
        self.server_state = GameState.GAME

        self.game = game.Game(width, height)

        for addr, player_tuple in self.active_players.items():
            self.active_players[addr] = (player_tuple[0], self.game.spawn_new_snake())

        self.game.spawn_new_pellet()

        for addr in self.active_players:
            net.send_pellet_update(self._socket, addr, self.game.tick_num, 0, self.game.pellet)

            for snake_id, snake in self.game.snakes.items():
                net.send_snake_update(self._socket, addr, self.game.tick_num, snake_id, snake)

        for addr in self.active_players:
            net.send_start_message(self._socket, addr, self.game.width, self.game.height)

if __name__ == '__main__':
    #TODO add timestamp (with format)
    #logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    Server().start()
