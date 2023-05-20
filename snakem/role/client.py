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

import curses.ascii

from ..config import client as cfg

from ..game import display, game
from ..net import net
from ..test import debug
from ..enums import GameState, MsgType, Dir

_motd = None
_lobby_list = None

# the lobby server address
_lobby_addr = None

_client_state = None

_game_instance = None

def start():
    debug.init_debug('Client', cfg.PRINT_DEBUG, cfg.PRINT_ERROR, cfg.PRINT_NETMSG)

    net.init_client_socket()
    display.init_client_window(_start_with_curses)

def _start_with_curses():
    _start_motd_mode()

    tick_time = 0.0

    try:
        while True:
            net.wait_for_input(_handle_net_message, _handle_input, _client_state != GameState.GAME)

            if _client_state == GameState.GAME:
                tick_time += net.TIMEOUT
                # TODO get STEP_TIME from server during game setup
                if tick_time >= cfg.STEP_TIME:
                    tick_time -= cfg.STEP_TIME
                    display.show_game(_game_instance)
    finally:
        if _lobby_addr:
            net.send_quit_message(_lobby_addr)
        net.close_socket()

def _handle_net_message(address, msg_type, msg_body):
    global _motd, _lobby_list

    display.show_debug(debug.get_net_msg(address, 'from', msg_type, msg_body, net.get_addl_info_for_debug(msg_type, msg_body)))

    if address == _lobby_addr:
        if _client_state == GameState.MOTD:
            if msg_type == MsgType.LOBBY_JOIN:
                _start_lobby_mode()
            elif msg_type == MsgType.LOBBY_QUIT:
                display.show_debug('Lobby rejected your join request.')
                _start_motd_mode()
        elif _client_state == GameState.LOBBY:
            if msg_type == MsgType.START:
                _start_game_mode()
        elif _client_state == GameState.GAME:
            _handle_net_message_during_game(msg_type, msg_body)
    #TODO if cfg.SERVER_ADDR[0] is a hostname, convert it to IP address. Because this might not match
    elif address == cfg.SERVER_ADDR:
        if _client_state == GameState.MOTD:
            if msg_type == MsgType.MOTD:
                _motd = msg_body
                display.show_motd(address, _motd, _lobby_list)
            elif msg_type == MsgType.LOBBY_REP:
                _lobby_list = net.unpack_lobby_list(msg_body)
                display.show_motd(address, _motd, _lobby_list)

def _handle_net_message_during_game(msg_type, msg_body):
    if msg_type == MsgType.SNAKE_UPDATE:
        tick, snake_id, heading, is_alive, body = net.unpack_snake_update(msg_body)

        _game_instance.update_snake(tick, snake_id, heading, is_alive, body)
    elif msg_type == MsgType.END:
        _end_game_mode()
        _start_lobby_mode()

def _handle_input():
    global _lobby_addr

    input_char = display.get_key()

    if _client_state == GameState.MOTD:
        if input_char in cfg.KEYS_LOBBY_QUIT:
            sys.exit()
        elif curses.ascii.isdigit(input_char):
            selection = int(curses.ascii.unctrl(input_char))
            if 1 <= selection <= len(_lobby_list):
                _lobby_addr = (cfg.SERVER_ADDR[0], _lobby_list[selection - 1][1])
                net.send_lobby_join_request(_lobby_addr)
        elif input_char in cfg.KEYS_LOBBY_REFRESH:
            net.send_hello_message(cfg.SERVER_ADDR)
            net.send_lobby_list_request(cfg.SERVER_ADDR)
    elif _client_state == GameState.LOBBY:
        if input_char in cfg.KEYS_LOBBY_QUIT:
            net.send_quit_message(_lobby_addr)
            _start_motd_mode()
        elif input_char in cfg.KEYS_LOBBY_READY:
            net.send_ready_message(_lobby_addr)
    elif _client_state == GameState.GAME:
        if input_char in cfg.KEYS_GAME_QUIT:
            #TODO make it harder to quit running game
            net.send_quit_message(_lobby_addr)
            _start_motd_mode()
        elif input_char in cfg.KEYS_MV_LEFT:
            net.send_input_message(_lobby_addr, Dir.Left)
        elif input_char in cfg.KEYS_MV_DOWN:
            net.send_input_message(_lobby_addr, Dir.Down)
        elif input_char in cfg.KEYS_MV_UP:
            net.send_input_message(_lobby_addr, Dir.Up)
        elif input_char in cfg.KEYS_MV_RIGHT:
            net.send_input_message(_lobby_addr, Dir.Right)
    elif _client_state == GameState.GAME_OVER:
        if input_char in cfg.KEYS_LOBBY_QUIT:
            _start_lobby_mode()

def _start_motd_mode():
    global _client_state, _lobby_addr
    _client_state  = GameState.MOTD
    _lobby_addr = None

    net.send_hello_message(cfg.SERVER_ADDR)
    net.send_lobby_list_request(cfg.SERVER_ADDR)

    display.show_message(f'Contacting server at {cfg.SERVER_ADDR[0]}:{cfg.SERVER_ADDR[1]} . . .')

def _start_lobby_mode():
    global _client_state
    _client_state = GameState.LOBBY

    display.show_lobby()

def _start_game_mode():
    global _client_state, _game_instance
    _client_state = GameState.GAME

    #TODO get win width/height from server (and/or change display code to handle large maps)
    #gameInstance = game.Game(WIN_WIDTH, WIN_HEIGHT)
    height, width = display.get_window_size()
    _game_instance = game.Game(width, height)

    display.show_game(_game_instance)

def _end_game_mode():
    global _game_instance

    _game_instance = None
