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
import logging
import time
import curses
import os
import sys

from collections.abc import Awaitable
from websockets.client import connect, WebSocketClientProtocol

# must come after Awaitable
import aioconsole

from ..config import client as config
from ..net import net
from ..game import game, display
from ..game.enums import Dir

from .enums import GameState, MsgType
from .server import app

class Client:
    def __init__(self, ws: WebSocketClientProtocol, scr: curses.window, step_time_ms: int, keys: dict) -> None:
        self._socket: WebSocketClientProtocol = ws

        self._stdscr: curses.window = scr

        self._step_time_ms: int = step_time_ms
        self._keys: dict = keys

        self._motd: str | None = None
        self._game_state: GameState = GameState.LOBBY
        self._game: game.Game

    async def start(self) -> Awaitable:
        display.show_message(self._stdscr, 'Contacting server...')

        # contact the server immediately
        # async with asyncio.TaskGroup() as tg:
        #     task1 = tg.create_task(net.send_hello_message(self._socket))
        #     task2 = tg.create_task(net.send_lobby_join_request(self._socket))
        await net.send_hello_message(self._socket)
        await net.send_lobby_join_request(self._socket)

        last_step_time = time.monotonic_ns()

        try:
            while 1:
                done, pending = await asyncio.wait([
                    asyncio.create_task(aioconsole.ainput(), name='stdin'),
                    asyncio.create_task(net.receive_message(self._socket), name='ws')
                ], return_when=asyncio.FIRST_COMPLETED)

                #TODO handle *all* net messages first before checking input?

                input_char = display.get_key(self._stdscr)
                if input_char != curses.ERR:
                    await self._handle_input(input_char)
                else:
                    #TODO is this right?
                    ws, msg_type, json = await net.receive_message(self._socket)

                    if self._game_state == GameState.GAME:
                        self._handle_game_message(msg_type, json)
                    else:
                        self._handle_lobby_message(msg_type, json)

                if self._game_state == GameState.GAME:
                    now = time.monotonic_ns()

                    #TODO get STEP_TIME_MS from server during game setup
                    if (now - last_step_time) // 1_000_000 >= self._step_time_ms:
                        last_step_time = now

                        display.show_game(self._stdscr, self._game)
        finally:
            await net.send_quit_message(self._socket)
            self._socket.close()

    async def _poll_for_input(self) -> int:
        return self._stdscr.getch();

    def _handle_lobby_message(self, msg_type: MsgType, json: dict) -> None:
        if msg_type == MsgType.LOBBY_JOIN:
            self._start_lobby_mode()
        elif msg_type == MsgType.LOBBY_QUIT:
            display.show_debug(self._stdscr, 'Lobby rejected your join request.')
            self._start_lobby_mode()
        elif msg_type == MsgType.START:
            width, height = net.unpack_start_message(json)

            self._start_game_mode(width, height)
        elif msg_type == MsgType.MOTD:
            self._motd = json['motd']

            self._start_lobby_mode()

    def _handle_game_message(self, msg_type: MsgType, msg_body: dict) -> None:
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
                sys.exit()
            elif input_char in self._keys['LOBBY_REFRESH']:
                await asyncio.wait([
                    net.send_hello_message(self._socket),
                    net.send_lobby_join_request(self._socket)
                ])
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

    def _start_lobby_mode(self) -> None:
        self._game_state = GameState.LOBBY

        display.show_lobby(self._stdscr, self._motd)

    def _start_game_mode(self, width: int, height: int) -> None:
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
            #TODO provide client_id to reconnect (save to file?)
            async with connect(f'ws://{config.SERVER_HOST}:{config.SERVER_PORT}/ws') as ws:
                await Client(ws, scr, config.STEP_TIME_MS, config.KEYS).start()

        asyncio.run(main())

    # cbreak on, echo off, keypad on, colors on
    curses.wrapper(start_with_curses)
