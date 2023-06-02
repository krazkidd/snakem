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

import json
import logging

from collections import deque

from starlette.websockets import WebSocket # aka fastapi.WebSocket
from websockets.client import WebSocketClientProtocol

from ..game.enums import Dir
from ..game.pellet import Pellet
from ..game.snake import Snake

from .enums import MsgType

# how long to wait for a network message or other input event
TIMEOUT: float = 0.005

async def send_message(ws: WebSocketClientProtocol | WebSocket, msg_type: MsgType, json_dict: dict | None = None) -> None:
    if json_dict is None:
        json_dict = { '_msg_type': msg_type.value }
    else:
        json_dict['_msg_type'] = msg_type.value

    logging.debug('NETMSG (to %s): <%s>', 'TODO', msg_type.name)

    if isinstance(ws, WebSocketClientProtocol):
        await ws.send(json.dumps(json_dict))
    else:
        await ws.send_json(json_dict)

async def receive_message(ws: WebSocketClientProtocol | WebSocket) -> tuple[MsgType, dict]:
    json_dict: dict

    if isinstance(ws, WebSocketClientProtocol):
        json_dict = json.loads(await ws.recv())
    else:
        json_dict = await ws.receive_json()

    msg_type = MsgType(json_dict['_msg_type'])

    #TODO print address as first argument
    logging.debug('NETMSG (from %s): <%s>', 'TODO', msg_type.name)

    return msg_type, json_dict

async def send_motd(ws: WebSocketClientProtocol | WebSocket, motd: str) -> None:
    await send_message(ws, MsgType.MOTD, {
        'motd': motd
    })

async def send_quit_message(ws: WebSocketClientProtocol | WebSocket) -> None:
    await send_message(ws, MsgType.LOBBY_QUIT)

async def send_pellet_update(ws: WebSocketClientProtocol | WebSocket, tick: int, pellet_id: int, pellet: Pellet) -> None:
    await send_message(ws, MsgType.PELLET_UPDATE, {
        'tick': tick,
        'pellet_id': pellet_id,
        'pos_x': pellet.pos[0],
        'pos_y': pellet.pos[1]
    })

def unpack_pellet_update(json_dict: dict) -> tuple[int, int, int, int]:
    return json_dict['tick'], json_dict['pellet_id'], json_dict['pos_x'], json_dict['pos_y']

async def send_snake_update(ws: WebSocketClientProtocol | WebSocket, tick: int, snake_id: int, snake: Snake) -> None:
    await send_message(ws, MsgType.SNAKE_UPDATE, {
        'tick': tick,
        'snake_id': snake_id,
        'heading': snake.heading.value,
        'is_alive': snake.is_alive,
        #TODO might have to use arrays (rather than tuples) for body piece positions
        'body': snake.body
    })

def unpack_snake_update(json_dict: dict) -> tuple[int, int, Dir, bool, deque[tuple[int, int]]]:
    #TODO get the body
    body: deque[tuple[int, int]] = deque()
    for pos_x, pos_y in body:
        body.append((pos_x, pos_y))

    return json_dict['tick'], json_dict['snake_id'], Dir(json_dict['heading']), json_dict['is_alive'] == 'true', body

async def send_lobby_join_request(ws: WebSocketClientProtocol | WebSocket) -> None:
    await send_message(ws, MsgType.LOBBY_JOIN)

async def send_ready_message(ws: WebSocketClientProtocol | WebSocket) -> None:
    await send_message(ws, MsgType.READY)

async def send_start_message(ws: WebSocketClientProtocol | WebSocket, width: int, height: int, step_time_ms: int) -> None:
    await send_message(ws, MsgType.START, {
        'width': width,
        'height': height,
        'step_time_ms': step_time_ms
    })

def unpack_start_message(json_dict: dict) -> tuple[int, int, int]:
    return json_dict['width'], json_dict['height'], json_dict['step_time_ms']

async def send_input_message(ws: WebSocketClientProtocol | WebSocket, tick: int, heading: Dir) -> None:
    await send_message(ws, MsgType.INPUT, {
        'tick': tick,
        'heading': heading.value
    })

def unpack_input_message(json_dict: dict) -> tuple[int, Dir]:
    return json_dict['tick'], Dir(json_dict['heading'])
