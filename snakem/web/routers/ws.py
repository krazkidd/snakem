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

from starlette.websockets import WebSocket # aka fastapi.{WebSocket, WebSocketDisconnect}
from fastapi import APIRouter

from ...config import server as config
from ...net import server

_server = None # type: server.Server
_server_task = None # type: asyncio.Task

router = APIRouter(
    prefix="/ws",
    tags=["websockets"],
    #dependencies=[Depends(...)],
    responses={404: {"description": "Not found"}},
)

@router.websocket("")
async def ws_root(ws: WebSocket):
    global _server, _server_task
    if not _server:
        _server = server.Server(config.MOTD, config.WIN_WIDTH, config.WIN_HEIGHT, config.STEP_TIME_MS)
        _server_task = asyncio.create_task(_server.start())

    await ws.accept()

    await _server.connect_client(ws)
