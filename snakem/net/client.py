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

import sys
import logging
import socket
import select
import time

from ..config import client as config
from ..game import game, display
from ..enums import GameState, MsgType, Dir

from . import net

class Client:
    def __init__(self):
        self._poll = select.poll()

        self._socket: socket.socket

        # the lobby server address
        self._server_addr: tuple[str, int] = (config.SERVER_HOST, config.SERVER_PORT)

        self._motd: str | None = None
        self._game_state: GameState = GameState.LOBBY
        self._game: game.Game

    def start(self) -> None:
        self._socket = net.init_client_socket()

        self._poll.register(self._socket, select.POLLIN)
        self._poll.register(sys.stdin, select.POLLIN)

        logging.info('Contacting %s on port %s.', config.SERVER_HOST, config.SERVER_PORT)

        net.send_hello_message(self._socket, self._server_addr)
        net.send_lobby_join_request(self._socket, self._server_addr)

        #TODO don't pass self._start_with_curses method as a delegate (use an interface)
        display.init_client_window(self._start_with_curses)

    def _start_with_curses(self) -> None:
        display.show_message(f'Contacting server at {config.SERVER_HOST}:{config.SERVER_PORT} . . .')

        last_step_time = time.monotonic_ns()

        try:
            while 1:
                if self._game_state == GameState.GAME:
                    inputs = self._poll.poll(net.TIMEOUT)
                else:
                    # we block on this call so we're not wasting cycles outside of an active game
                    inputs = self._poll.poll()

                for fd, event in inputs:
                    if fd == sys.stdin.fileno():
                        self._handle_input(display.get_key())
                    elif fd == self._socket.fileno():
                        address, msg_type, msg_body = net.receive_message(self._socket)

                        if self._game_state == GameState.GAME:
                            self._handle_game_message(address, msg_type, msg_body)
                        else:
                            self._handle_lobby_message(address, msg_type, msg_body)

                if self._game_state == GameState.GAME:
                    now = time.monotonic_ns()

                    #TODO get STEP_TIME_MS from server during game setup
                    if (now - last_step_time) // 1_000_000 >= config.STEP_TIME_MS:
                        last_step_time = now

                        display.show_game(self._game)
        finally:
            if self._server_addr:
                net.send_quit_message(self._socket, self._server_addr)
            self._socket.close()

    def _handle_lobby_message(self, address: tuple[str, int], msg_type: MsgType, msg_body: bytes) -> None:
        if msg_type == MsgType.LOBBY_JOIN:
            self._start_lobby_mode()
        elif msg_type == MsgType.LOBBY_QUIT:
            display.show_debug('Lobby rejected your join request.')
            self._start_lobby_mode()
        elif msg_type == MsgType.START:
            width, height = net.unpack_start_message(msg_body)

            self._start_game_mode(width, height)
        elif msg_type == MsgType.MOTD:
            self._motd = bytes.decode(msg_body)

            self._start_lobby_mode()

    def _handle_game_message(self, address: tuple[str, int], msg_type: MsgType, msg_body: bytes) -> None:
        if msg_type == MsgType.SNAKE_UPDATE:
            tick, snake_id, heading, is_alive, body = net.unpack_snake_update(msg_body)

            self._game.update_snake(tick, snake_id, heading, is_alive, body)
        elif msg_type == MsgType.PELLET_UPDATE:
            tick, pellet_id, pos_x, pos_y = net.unpack_pellet_update(msg_body)

            self._game.update_pellet(tick, pellet_id, pos_x, pos_y)
        elif msg_type == MsgType.LOBBY_JOIN:
            self._start_lobby_mode()

    def _handle_input(self, input_char: int) -> None:
        if self._game_state == GameState.LOBBY:
            if input_char in config.KEYS_LOBBY_QUIT:
                sys.exit()
            elif input_char in config.KEYS_LOBBY_REFRESH:
                net.send_hello_message(self._socket, self._server_addr)
                net.send_lobby_join_request(self._socket, self._server_addr)
            elif input_char in config.KEYS_LOBBY_READY:
                net.send_ready_message(self._socket, self._server_addr)
        elif self._game_state == GameState.GAME:
            if input_char in config.KEYS_GAME_QUIT:
                #TODO make it harder to quit running game
                net.send_quit_message(self._socket, self._server_addr)
                self._start_lobby_mode()
            elif input_char in config.KEYS_MV_LEFT:
                net.send_input_message(self._socket, self._server_addr, Dir.LEFT)
            elif input_char in config.KEYS_MV_DOWN:
                net.send_input_message(self._socket, self._server_addr, Dir.DOWN)
            elif input_char in config.KEYS_MV_UP:
                net.send_input_message(self._socket, self._server_addr, Dir.UP)
            elif input_char in config.KEYS_MV_RIGHT:
                net.send_input_message(self._socket, self._server_addr, Dir.RIGHT)

    def _start_lobby_mode(self) -> None:
        self._game_state = GameState.LOBBY

        display.show_lobby(self._motd)

    def _start_game_mode(self, width: int, height: int) -> None:
        self._game_state = GameState.GAME

        self._game = game.Game(width, height)

        display.show_game(self._game)

if __name__ == '__main__':
    #TODO add timestamp (with format)
    #logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    Client().start()
