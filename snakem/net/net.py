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
import logging

from collections import deque

from struct import pack
from struct import unpack
from struct import calcsize

from ..enums import MsgType, MsgFmt, Dir
from ..game.pellet import Pellet
from ..game.snake import Snake

MAX_MSG_SIZE: int = 1024

# how long to wait for a network message or other input event
TIMEOUT: float = 0.005

EMPTY_BYTES: bytes = b''

def init_health_check_socket(addr: tuple[str, int]) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)

    sock.listen(1024)

    return sock

def init_server_socket(addr: tuple[str, int]) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(addr)

    return sock

def init_client_socket() -> socket.socket:
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def _send_message(sock: socket.socket, address: tuple[str, int], msg_type: MsgType, msg_body: bytes | None = None) -> None:
    if msg_body:
        msg_len = len(msg_body)

        buf = pack(MsgFmt.HDR, msg_type.value, calcsize(MsgFmt.HDR) + msg_len)
        buf += msg_body
    else:
        msg_len = 0

        buf = pack(MsgFmt.HDR, msg_type.value, calcsize(MsgFmt.HDR))

    logging.debug('NETMSG (to %s): <%s, length %s>', address[0], msg_type.name, msg_len)

    sock.sendto(buf, address)

def receive_message(sock: socket.socket) -> tuple[tuple[str, int], MsgType, bytes]:
    msg, address = sock.recvfrom(MAX_MSG_SIZE)
    msg_type_, msg_len = unpack(MsgFmt.HDR, msg[:calcsize(MsgFmt.HDR)])

    msg_type = MsgType(msg_type_)

    #TODO verify msg size!
    if len(msg) > calcsize(MsgFmt.HDR):
        msg_body = msg[calcsize(MsgFmt.HDR):]
    else:
        msg_body = EMPTY_BYTES

    logging.debug('NETMSG (from %s): <%s, length %s>', address[0], msg_type.name, msg_len)

    return address, msg_type, msg_body

def send_hello_message(sock: socket.socket, address: tuple[str, int]) -> None:
    _send_message(sock, address, MsgType.MOTD)

def send_motd(sock: socket.socket, address: tuple[str, int], motd: str) -> None:
    _send_message(sock, address, MsgType.MOTD, str.encode(motd))

def send_quit_message(sock: socket.socket, address: tuple[str, int]) -> None:
    _send_message(sock, address, MsgType.LOBBY_QUIT)

def send_pellet_update(sock: socket.socket, address: tuple[str, int], tick: int, pellet_id: int, pellet: Pellet) -> None:
    _send_message(sock, address, MsgType.PELLET_UPDATE, pack(MsgFmt.PELLET_UPDATE, tick, pellet_id, pellet.pos[0], pellet.pos[1]))

def unpack_pellet_update(msg_body: bytes) -> tuple[int, int, int, int]:
    tick, pellet_id, pos_x, pos_y = unpack(MsgFmt.PELLET_UPDATE, msg_body[:calcsize(MsgFmt.PELLET_UPDATE)])

    return tick, pellet_id, pos_x, pos_y

def send_snake_update(sock: socket.socket, address: tuple[str, int], tick: int, snake_id: int, snake: Snake) -> None:
    #TODO don't exceed MAX_MSG_SIZE (without breaking the game--allow splitting an update or increase MAX_MSG_SIZE)
    buf = pack(MsgFmt.SNAKE_UPDATE_HDR, tick, snake_id, snake.heading.value, snake.is_alive, len(snake.body))
    for pos in snake.body:
        buf += pack(MsgFmt.SNAKE_UPDATE_BDY, pos[0], pos[1])

    _send_message(sock, address, MsgType.SNAKE_UPDATE, buf)

def unpack_snake_update(msg_body: bytes) -> tuple[int, int, Dir, bool, deque[tuple[int, int]]]:
    tick, snake_id, heading, is_alive, length = unpack(MsgFmt.SNAKE_UPDATE_HDR, msg_body[:calcsize(MsgFmt.SNAKE_UPDATE_HDR)]) # type: ignore
    body_buf = msg_body[calcsize(MsgFmt.SNAKE_UPDATE_HDR):]

    body: deque[tuple[int, int]] = deque()
    size = calcsize(MsgFmt.SNAKE_UPDATE_BDY)
    for i in range(length):
        body.append(unpack(MsgFmt.SNAKE_UPDATE_BDY, body_buf[i * size:(i + 1) * size])) # type: ignore

    return tick, snake_id, Dir(heading), is_alive, body

def send_lobby_join_request(sock: socket.socket, address: tuple[str, int]) -> None:
    _send_message(sock, address, MsgType.LOBBY_JOIN)

def send_ready_message(sock: socket.socket, address: tuple[str, int]) -> None:
    _send_message(sock, address, MsgType.READY)

def send_start_message(sock: socket.socket, address: tuple[str, int], width: int, height: int) -> None:
    _send_message(sock, address, MsgType.START, pack(MsgFmt.START, width, height))

def unpack_start_message(msg_body: bytes) -> tuple[int, int]:
    width, height = unpack(MsgFmt.START, msg_body[:calcsize(MsgFmt.START)]) # type: ignore

    return width, height

def send_input_message(sock: socket.socket, address: tuple[str, int], heading: Dir) -> None:
    _send_message(sock, address, MsgType.INPUT, pack(MsgFmt.PLAYER_INPUT, heading.value))

def unpack_input_message(msg_body: bytes) -> Dir:
    return Dir(unpack(MsgFmt.PLAYER_INPUT, msg_body)[0])
