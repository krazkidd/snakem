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

router = APIRouter(
    prefix="/api",
    tags=["api"],
    #dependencies=[Depends(...)],
    responses={404: {"description": "Not found"}},
)

@router.get("/health")
async def api_health():
    #TODO return a health status object and document the type in the decorator (for reusability)
    return {"status": "alive"}
