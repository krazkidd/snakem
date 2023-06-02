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

import asyncio
import json
import logging
import select
import time
import curses
import os
import sys

from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from websockets.client import connect, WebSocketClientProtocol

from ..config import client as config
from ..net import net
from ..game import game, display
from ..game.enums import Dir

from .enums import GameState, MsgType

class Client:
    def __init__(self, scr: curses.window, keys: dict) -> None:
        self._motd: str | None = None
        self._step_time_ms: int = 100

        self._stdscr: curses.window = scr
        self._keys: dict = keys

        self._socket: WebSocketClientProtocol

        self._game_state: GameState = GameState.LOBBY
        self._game: game.Game

    async def connect_client(self, ws: WebSocketClientProtocol) -> None:
        self._socket = ws

        try:
            while 1:
                json_dict = json.loads(await ws.recv())

                msg_type = MsgType(json_dict['_msg_type'])

                #TODO print address as first argument
                logging.debug('NETMSG (from %s): <%s>', 'TODO', msg_type.name)

                if self._game_state == GameState.GAME:
                    await self._handle_game_message(ws, msg_type, json_dict)
                else:
                    await self._handle_lobby_message(ws, msg_type, json_dict)

                await asyncio.sleep(0)
        except ConnectionClosedOK:
            pass
        except ConnectionClosedError:
            pass
        finally:
            del self._socket

    async def start(self) -> None:
        display.show_message(self._stdscr, 'Contacting server...')

        poll = select.poll()
        poll.register(sys.stdin, select.POLLIN)

        last_step_time = time.monotonic_ns()

        while 1:
            input_char = display.get_key(self._stdscr)

            while input_char != curses.ERR:
                await self._handle_input(input_char)

                input_char = display.get_key(self._stdscr)

            if self._game_state == GameState.GAME:
                now = time.monotonic_ns()

                if (now - last_step_time) // 1_000_000 >= self._step_time_ms:
                    self._game.tick()

                    display.show_game(self._stdscr, self._game)

                    last_step_time = now

                await asyncio.sleep(self._step_time_ms / 1000)
            else:
                await asyncio.sleep(0.3)

    async def _poll_for_input(self) -> int:
        return self._stdscr.getch()

    async def _handle_lobby_message(self, ws: WebSocketClientProtocol, msg_type: MsgType, json_dict: dict) -> None:
        if msg_type == MsgType.MOTD:
            self._start_lobby_mode(json_dict['motd'])
        elif msg_type == MsgType.LOBBY_JOIN:
            self._start_lobby_mode()
        elif msg_type == MsgType.LOBBY_QUIT:
            self._start_lobby_mode()
        elif msg_type == MsgType.START:
            width, height, step_time_ms = net.unpack_start_message(json_dict)
            self._start_game_mode(width, height, step_time_ms)

    async def _handle_game_message(self, ws: WebSocketClientProtocol, msg_type: MsgType, msg_body: dict) -> None:
        if msg_type == MsgType.SNAKE_UPDATE:
            #TODO use tick value to determine if it's safe to update game state
            #     or if it's out of date (compare to current game tick value)
            tick, snake_id, heading, is_alive, body = net.unpack_snake_update(msg_body)

            self._game.update_snake(snake_id, heading, is_alive, body)
        elif msg_type == MsgType.PELLET_UPDATE:
            #TODO use tick value to determine if it's safe to update game state
            #     or if it's out of date (compare to current game tick value)
            tick, pellet_id, pos_x, pos_y = net.unpack_pellet_update(msg_body)

            self._game.update_pellet(pellet_id, pos_x, pos_y)
        elif msg_type == MsgType.LOBBY_JOIN:
            self._start_lobby_mode()

    async def _handle_input(self, input_char: int) -> None:
        if self._game_state == GameState.LOBBY:
            if input_char in self._keys['LOBBY_QUIT']:
                #TODO if the connection is still in an open state, send a quit message
                #await self._socket.close(code=1000, reason=None)

                sys.exit()
            elif input_char in self._keys['LOBBY_REFRESH']:
                await net.send_lobby_join_request(self._socket)
            elif input_char in self._keys['LOBBY_READY']:
                await net.send_ready_message(self._socket)
        elif self._game_state == GameState.GAME:
            if input_char in self._keys['GAME_QUIT']:
                #TODO make it harder to quit running game
                await net.send_quit_message(self._socket)
                self._start_lobby_mode()
            elif input_char in self._keys['MV_LEFT']:
                await net.send_input_message(self._socket, self._game.tick_num, Dir.LEFT)
            elif input_char in self._keys['MV_DOWN']:
                await net.send_input_message(self._socket, self._game.tick_num, Dir.DOWN)
            elif input_char in self._keys['MV_UP']:
                await net.send_input_message(self._socket, self._game.tick_num, Dir.UP)
            elif input_char in self._keys['MV_RIGHT']:
                await net.send_input_message(self._socket, self._game.tick_num, Dir.RIGHT)

    def _start_lobby_mode(self, motd: str | None = None) -> None:
        if (motd):
            self._motd = motd

        self._game_state = GameState.LOBBY

        display.show_lobby(self._stdscr, self._motd)

    def _start_game_mode(self, width: int, height: int, step_time_ms: int) -> None:
        self._step_time_ms = step_time_ms

        self._game_state = GameState.GAME
        self._game = game.Game(width, height)

        display.show_game(self._stdscr, self._game)

if __name__ == '__main__':
    #TODO add timestamp (with format)
    #logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    # set shorter delay for ESC key recognition
    if 'ESCDELAY' not in os.environ:
        os.environ.setdefault('ESCDELAY', '75')

    def start_with_curses(scr: curses.window) -> None:
        # scr.getch() will return immediately (-1 if no input)
        # see: https://docs.python.org/3/library/curses.html#curses.window.getch
        scr.nodelay(True)

        async def main() -> None:
            client = Client(scr, config.KEYS)

            asyncio.create_task(client.start())

            async with connect(f'ws://{config.SERVER_HOST}:{config.SERVER_PORT}/ws') as ws:
                await client.connect_client(ws)

        asyncio.run(main())

    # cbreak on, echo off, keypad on, colors on
    curses.wrapper(start_with_curses)
