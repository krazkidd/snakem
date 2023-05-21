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

import socket
import sys
import select
from struct import pack
from struct import unpack
from struct import calcsize

from ..test import debug
from ..enums import MsgType, MsgFmt

MAX_MSG_SIZE = 1024

# how long to wait for an input event
TIMEOUT = 0.005

_sock = None

def init_server_socket(addr):
    global _sock
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _sock.bind(addr)

    return _sock.getsockname()[1] # return port

def init_client_socket():
    global _sock
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def close_socket():
    if _sock:
        _sock.close()

def wait_for_input(handler, do_block=True):
    if do_block:
        # we block on this call so we're not wasting cycles outside of an active game
        readable, writable, exceptional = select.select([_sock, sys.stdin], [], [])
    else:
        readable, writable, exceptional = select.select([_sock, sys.stdin], [], [], TIMEOUT)

    if handler.handle_input is not None and sys.stdin in readable:
        handler.handle_input()
    elif handler.handle_net_message is not None and _sock in readable:
        address, msg_type, msg_body = receive_message()
        handler.handle_net_message(address, msg_type, msg_body)

def send_message(address, msg_type, msg_body=None):
    if msg_body:
        buf = pack(MsgFmt.HDR, msg_type, calcsize(MsgFmt.HDR) + len(msg_body))
        buf += msg_body
    else:
        buf = pack(MsgFmt.HDR, msg_type, calcsize(MsgFmt.HDR))

    debug.print_net_msg_sent(address, msg_type, msg_body, get_addl_info_for_debug(msg_type, msg_body))

    _sock.sendto(buf, address)

def receive_message():
    msg, address = _sock.recvfrom(MAX_MSG_SIZE)
    msg_type, msg_len = unpack(MsgFmt.HDR, msg[:calcsize(MsgFmt.HDR)])

    #TODO verify msg size!
    if len(msg) > calcsize(MsgFmt.HDR):
        msg_body = msg[calcsize(MsgFmt.HDR):]
    else:
        msg_body = None

    debug.print_net_msg_received(address, msg_type, msg_body, get_addl_info_for_debug(msg_type, msg_body))

    return address, msg_type, msg_body

def get_addl_info_for_debug(msg_type, msg_body):
    if msg_type == MsgType.SNAKE_UPDATE:
        tick, snake_id, heading, is_alive, body = unpack_snake_update(msg_body)
        x_pos, y_pos = body[0]
        return '(' + str(x_pos) + ', ' + str(y_pos) + ')'

    return None

def send_hello_message(address):
    send_message(address, MsgType.HELLO)

def send_motd(address, motd):
    send_message(address, MsgType.MOTD, motd)

def send_quit_message(address):
    send_message(address, MsgType.LOBBY_QUIT)

def send_lobby_list_request(address):
    send_message(address, MsgType.LOBBY_REQ)

def send_lobby_list(address, lobbies):
    buf = pack(MsgFmt.LBY_CNT, len(lobbies))
    for lobby in lobbies:
        buf += pack(MsgFmt.LBY, lobby.lobby_num, lobby.connect_port)

    send_message(address, MsgType.LOBBY_REP, buf)

def unpack_lobby_list(msg_body):
    lobby_count = unpack(MsgFmt.LBY_CNT, msg_body[:calcsize(MsgFmt.LBY_CNT)])[0]
    packed_lobbies = msg_body[calcsize(MsgFmt.LBY_CNT):]

    lobby_list = []
    size = calcsize(MsgFmt.LBY)
    for i in range(lobby_count):
        lobby_list.append(unpack(MsgFmt.LBY, packed_lobbies[i * size:(i + 1) * size]))

    return lobby_list

def send_snake_update(address, tick, snake_id, snake):
    #TODO don't exceed MAX_MSG_SIZE (without breaking the game--allow splitting an update or increase MAX_MSG_SIZE)
    buf = pack(MsgFmt.SNAKE_UPDATE_HDR, tick, snake_id, snake.heading, snake.isAlive, len(snake.body))
    for pos in snake.body:
        buf += pack(MsgFmt.SNAKE_UPDATE_BDY, pos[0], pos[1])

    send_message(address, MsgType.SNAKE_UPDATE, buf)

def unpack_snake_update(msg_body):
    tick, snake_id, heading, is_alive, length = unpack(MsgFmt.SNAKE_UPDATE_HDR, msg_body[:calcsize(MsgFmt.SNAKE_UPDATE_HDR)])
    body_buf = msg_body[calcsize(MsgFmt.SNAKE_UPDATE_HDR):]

    body = list()
    size = calcsize(MsgFmt.SNAKE_UPDATE_BDY)
    for i in range(length):
        body.append(unpack(MsgFmt.SNAKE_UPDATE_BDY, body_buf[i * size:(i + 1) * size]))

    return tick, snake_id, heading, is_alive, body

def send_lobby_join_request(address):
    send_message(address, MsgType.LOBBY_JOIN)

def send_ready_message(address):
    send_message(address, MsgType.READY)

def send_setup_message(address):
    send_message(address, MsgType.SETUP)

def send_start_message(address):
    send_message(address, MsgType.START)

def send_end_message(address):
    send_message(address, MsgType.END)

def send_input_message(address, heading):
    send_message(address, MsgType.INPUT, pack(MsgFmt.PLAYER_INPUT, heading))

def unpack_input_message(msg_body):
    return int(unpack(MsgFmt.PLAYER_INPUT, msg_body)[0])
