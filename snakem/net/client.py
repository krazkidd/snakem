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

from ..config import client as config
from ..game import game, display
from ..test import debug
from ..enums import GameState, MsgType, Dir

from . import net

class Client:
    def __init__(self):
        self._motd = None

        # the lobby server address
        self._lobby_addr = (config.SERVER_HOST, config.SERVER_PORT)

        self._client_state  = GameState.LOBBY

        self._game_instance = None

    def start(self):
        debug.init_debug('Client', config.PRINT_DEBUG, config.PRINT_ERROR, config.PRINT_NETMSG)

        net.init_client_socket()
        #TODO don't pass self._start_with_curses method as a delegate (use an interface)
        display.init_client_window(self._start_with_curses)

    def _start_with_curses(self):
        display.show_message(f'Contacting server at {config.SERVER_HOST}:{config.SERVER_PORT} . . .')

        tick_time = 0.0

        try:
            while True:
                net.wait_for_input(self, self._client_state != GameState.GAME)

                if self._client_state == GameState.GAME:
                    tick_time += net.TIMEOUT
                    #TODO get STEP_TIME from server during game setup
                    if tick_time >= config.STEP_TIME:
                        tick_time -= config.STEP_TIME
                        display.show_game(self._game_instance)
        finally:
            if self._lobby_addr:
                net.send_quit_message(self._lobby_addr)
            net.close_socket()

    def handle_net_message(self, address, msg_type, msg_body):
        display.show_debug(debug.get_net_msg(address, 'from', msg_type, msg_body, net.get_addl_info_for_debug(msg_type, msg_body)))

        if address == self._lobby_addr:
            if self._client_state == GameState.LOBBY:
                if msg_type == MsgType.LOBBY_JOIN:
                    self._start_lobby_mode()
                elif msg_type == MsgType.LOBBY_QUIT:
                    display.show_debug('Lobby rejected your join request.')
                    self._start_lobby_mode()
                elif msg_type == MsgType.START:
                    self._start_game_mode()
                elif msg_type == MsgType.MOTD:
                    self._motd = bytes.decode(msg_body)

                    self._start_lobby_mode()
            elif self._client_state == GameState.GAME:
                self._handle_net_message_during_game(msg_type, msg_body)

    def _handle_net_message_during_game(self, msg_type, msg_body):
        if msg_type == MsgType.SNAKE_UPDATE:
            tick, snake_id, heading, is_alive, body = net.unpack_snake_update(msg_body)

            self._game_instance.update_snake(tick, snake_id, heading, is_alive, body)
        elif msg_type == MsgType.LOBBY_JOIN:
            self._start_lobby_mode()

    def handle_input(self):
        input_char = display.get_key()

        if self._client_state == GameState.LOBBY:
            if input_char in config.KEYS_LOBBY_QUIT:
                sys.exit()
            elif input_char in config.KEYS_LOBBY_REFRESH:
                net.send_hello_message(self._lobby_addr)
                net.send_lobby_join_request(self._lobby_addr)
            elif input_char in config.KEYS_LOBBY_READY:
                net.send_ready_message(self._lobby_addr)
        elif self._client_state == GameState.GAME:
            if input_char in config.KEYS_GAME_QUIT:
                #TODO make it harder to quit running game
                net.send_quit_message(self._lobby_addr)
                self._start_lobby_mode()
            elif input_char in config.KEYS_MV_LEFT:
                net.send_input_message(self._lobby_addr, Dir.Left)
            elif input_char in config.KEYS_MV_DOWN:
                net.send_input_message(self._lobby_addr, Dir.Down)
            elif input_char in config.KEYS_MV_UP:
                net.send_input_message(self._lobby_addr, Dir.Up)
            elif input_char in config.KEYS_MV_RIGHT:
                net.send_input_message(self._lobby_addr, Dir.Right)

    def _start_lobby_mode(self):
        self._client_state = GameState.LOBBY

        self._game_instance = None

        display.show_lobby(self._motd)

    def _start_game_mode(self):
        self._client_state = GameState.GAME

        #TODO get win width/height from server (and/or change display code to handle large maps)
        #gameInstance = game.Game(WIN_WIDTH, WIN_HEIGHT)
        height, width = display.get_window_size()
        self._game_instance = game.Game(width, height)

        display.show_game(self._game_instance)

if __name__ == '__main__':
    Client().start()
