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

from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from ..config import server as config
from ..net import net
from ..game import game

from .enums import GameState, MsgType

app = FastAPI()

@app.get("/api/health")
async def api_health():
    return {"status": "alive"}

@app.websocket("/ws")
#@app.websocket("/ws/")
#@app.websocket("/ws/{client_id}")
async def websocket_endpoint(ws: WebSocket, client_id: int | None = None):
    #TODO if client_id != None, then we should not accept() and hand them off to the server

    await ws.accept()

    try:
        while 1:
            await asyncio.sleep(1)
            await net.send_motd(ws, config.MOTD)
            # await manager.send_personal_message(f"You wrote: {data}", ws)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        # manager.disconnect(ws)
        # await manager.broadcast(f"Client #{client_id} left the chat")
        pass

class Server:
    def __init__(self, width: int, height: int, step_time_ms: int) -> None:
        self._width: int = width
        self._height: int = height
        self._step_time_ms: int = step_time_ms

        # self.active_players maps websockets to tuples of (r, s) where:
        #   r = ready status (MsgType.{NOT_,}READY)
        #   s = snake id when a game is running
        self._players: dict[WebSocket, tuple[MsgType, int | None]] = dict()

        self._game_state: GameState = GameState.LOBBY
        self._game: game.Game

    async def start(self) -> Any: # Awaitable
        logging.info('Server started.')

        last_step_time = time.monotonic_ns()

        try:
            while 1:
                #TODO handle disconnects by handling WebSocketDisconnect exception
                # try:
                #     while 1:
                #         data = await websocket.receive_text()
                #         # await manager.send_personal_message(f"You wrote: {data}", websocket)
                #         # await manager.broadcast(f"Client #{client_id} says: {data}")
                # except WebSocketDisconnect:
                #     websocket.disconnect(websocket)
                #     await websocket.broadcast(f"Client #{client_id} left the chat")

                done, _ = await asyncio.wait([net.receive_message(ws) for ws in self._players.keys], return_when=asyncio.FIRST_COMPLETED)

                #TODO do i need to cancel pending tasks?
                #TODO do i need to cancel done tasks if i don't consume them?

                for awaitable in done:
                    ws, msg_type, json = await awaitable

                    if self._game_state == GameState.GAME:
                        await self._handle_game_message(ws, msg_type, json)
                    else:
                        await self._handle_lobby_message(ws, msg_type, json)

                if self._game_state == GameState.GAME:
                    now = time.monotonic_ns()

                    if (now - last_step_time) // 1_000_000 >= self._step_time_ms:
                        last_step_time = now

                        self._game.tick()

                        # update all players with all snakes
                        await asyncio.wait([net.send_snake_update(ws, self._game.tick_num, snake_id, snake) for ws in self._players for snake_id, snake in self._game.snakes.items()])

                        # end game when all snakes are dead
                        #TODO the game should end when at most *one* snake is alive
                        for snake in self._game.snakes.values():
                            if snake.is_alive:
                                break
                        else:
                            await asyncio.wait([net.send_lobby_join_request(ws) for ws in self._players])

                            self._start_lobby_mode()
        except Exception:
            logging.exception('Unknown exception.')

    async def _handle_lobby_message(self, ws: WebSocket, msg_type: MsgType, json: dict) -> None:
        if ws in self._players:
            _, snake_id = self._players[ws]

            if msg_type == MsgType.LOBBY_JOIN:
                await net.send_lobby_join_request(ws)  # LOBBY_JOIN is used for join confirmation
                self._players[ws] = (MsgType.NOT_READY, snake_id)  # reset READY status
            elif msg_type == MsgType.LOBBY_QUIT:
                del self._players[ws]
            elif msg_type == MsgType.READY:
                self._players[ws] = (MsgType.READY, snake_id)

                for player_tuple in self._players.values():
                    if player_tuple[0] != MsgType.READY:
                        break
                else:
                    await self._start_game_mode(self._width, self._height)
            elif msg_type == MsgType.NOT_READY:
                self._players[ws] = (MsgType.NOT_READY, snake_id)
        else:
            if msg_type == MsgType.LOBBY_JOIN:
                if len(self._players) < 4:
                    await net.send_lobby_join_request(ws)  # LOBBY_JOIN is used for join confirmation
                    self._players[ws] = (MsgType.NOT_READY, None)
                else:
                    await net.send_quit_message(ws)  # LOBBY_QUIT is used for join rejection

    async def _handle_game_message(self, ws: WebSocket, msg_type: MsgType, json: dict) -> None:
        if ws in self._players:
            do_update_clients = False

            if msg_type == MsgType.INPUT:
                self._game.snakes[self._players[ws][1]].change_heading(net.unpack_input_message(json)) # type: ignore
                do_update_clients = True

            if do_update_clients:
                for sock in self._players:
                    await net.send_pellet_update(sock, self._game.tick_num, 0, self._game.pellet)

                    for snake_id, snake in self._game.snakes.items():
                        await net.send_snake_update(sock, self._game.tick_num, snake_id, snake)

    def _start_lobby_mode(self) -> None:
        self._game_state = GameState.LOBBY

    async def _start_game_mode(self, width: int, height: int) -> None:
        self._game_state = GameState.GAME

        self._game = game.Game(width, height)

        for ws, player_tuple in self._players.items():
            self._players[addr] = (player_tuple[0], self._game.spawn_new_snake())

        self._game.spawn_new_pellet()

        for ws in self._players:
            await net.send_pellet_update(ws, self._game.tick_num, 0, self._game.pellet)

            for snake_id, snake in self._game.snakes.items():
                await net.send_snake_update(ws, self._game.tick_num, snake_id, snake)

        for addr in self._players:
            await net.send_start_message(ws, self._game.width, self._game.height)

if __name__ == '__main__':
    #TODO add timestamp (with format)
    #logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    #TODO Server(config.WIN_WIDTH, config.WIN_HEIGHT, config.STEP_TIME_MS).start()
