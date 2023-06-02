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

from starlette.websockets import WebSocket, WebSocketDisconnect # aka fastapi.WebSocket

from ..net import net
from ..game import game

from .enums import GameState, MsgType

class Server:
    def __init__(self, motd: str, width: int, height: int, step_time_ms: int) -> None:
        self._motd: str = motd
        self._width: int = width
        self._height: int = height
        self._step_time_ms: int = step_time_ms

        # self.active_players maps websockets to tuples of (r, s) where:
        #   r = ready status (MsgType.{NOT_,}READY)
        #   s = snake id when a game is running
        self._players: dict[WebSocket, tuple[MsgType, int | None]] = dict()

        self._game_state: GameState = GameState.LOBBY
        self._game: game.Game

    async def connect_client(self, ws: WebSocket) -> None:
        #TODO accessing self._players needs thread safety if we are going to multithread

        self._players[ws] = (MsgType.NOT_READY, None)

        try:
            await net.send_motd(ws, self._motd)

            async for json_dict in ws.iter_json():
                msg_type = MsgType(json_dict['_msg_type'])

                #TODO print address as first argument
                logging.debug('NETMSG (from %s): <%s>', 'TODO', msg_type.name)

                if self._game_state == GameState.GAME:
                    await self._handle_game_message(ws, msg_type, json_dict)
                else:
                    await self._handle_lobby_message(ws, msg_type, json_dict)
        except WebSocketDisconnect:
            pass
        finally:
            #TODO if the connection is still in an open state, send a quit message
            #await websocket.close(code=1000, reason=None)

            del self._players[ws]

    async def start(self) -> None:
        logging.info('Server started.')

        last_step_time = time.monotonic_ns()

        while 1:
            if self._game_state == GameState.GAME:
                now = time.monotonic_ns()

                if (now - last_step_time) // 1_000_000 >= self._step_time_ms:
                    self._game.tick()

                    #TODO uncomment
                    # # update all players with all snakes
                    # await asyncio.wait([net.send_snake_update(ws, self._game.tick_num, snake_id, snake) for ws in self._players for snake_id, snake in self._game.snakes.items()])

                    # end game when all snakes are dead
                    #TODO the game should end when at most *one* snake is alive
                    for snake in self._game.snakes.values():
                        if snake.is_alive:
                            break
                    else:
                        #TODO consider returning from this and letting the thread end

                        await self._start_lobby_mode()

                    last_step_time = now

                await asyncio.sleep(self._step_time_ms / 1000)
            else:
                await asyncio.sleep(1)

    async def _handle_lobby_message(self, ws: WebSocket, msg_type: MsgType, json_dict: dict) -> None:
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

    async def _handle_game_message(self, ws: WebSocket, msg_type: MsgType, json_dict: dict) -> None:
        if ws in self._players:
            do_update_clients = False

            if msg_type == MsgType.INPUT:
                self._game.snakes[self._players[ws][1]].change_heading(net.unpack_input_message(json_dict)[1])
                do_update_clients = True

            if do_update_clients:
                for sock in self._players:
                    await net.send_pellet_update(sock, self._game.tick_num, 0, self._game.pellet)

                    for snake_id, snake in self._game.snakes.items():
                        await net.send_snake_update(sock, self._game.tick_num, snake_id, snake)

    async def _start_lobby_mode(self) -> None:
        self._game_state = GameState.LOBBY

        await asyncio.wait([net.send_lobby_join_request(ws) for ws in self._players])

    async def _start_game_mode(self, width: int, height: int) -> None:
        self._game_state = GameState.GAME

        self._game = game.Game(width, height)

        for ws, player_tuple in self._players.items():
            self._players[ws] = (player_tuple[0], self._game.spawn_new_snake())

        #TODO send snake and pellet statuses with start message

        for ws in self._players:
            await net.send_pellet_update(ws, self._game.tick_num, 0, self._game.pellet)

            for snake_id, snake in self._game.snakes.items():
                await net.send_snake_update(ws, self._game.tick_num, snake_id, snake)

        for ws in self._players:
            await net.send_start_message(ws, self._game.width, self._game.height, self._step_time_ms)
