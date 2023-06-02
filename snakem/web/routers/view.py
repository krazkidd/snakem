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

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from ...config import server

router = APIRouter(
    prefix="/view",
    tags=["view"],
    #dependencies=[Depends(...)],
    responses={404: {"description": "Not found"}},
)

@router.get("", response_class=HTMLResponse)
async def view_root():
    return f'<html><head><title></title></head><body>{server.MOTD}</body></html>'
