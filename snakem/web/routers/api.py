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

import math
import random

from fastapi import APIRouter
from pydantic import BaseModel

from ...config import server as config

router = APIRouter(
    prefix="/api",
    tags=["api"],
    #dependencies=[Depends(...)],
    responses={404: {"description": "Not found"}},
)

class HealthCheck(BaseModel):
    alive: bool
    ready: bool

class HighScoreItem(BaseModel):
    rank: int
    score: int
    name: str | None

@router.get("/health")
async def get_health() -> HealthCheck:
    return HealthCheck(alive=True, ready=True)

@router.get("/motd")
async def get_motd() -> str:
    return config.MOTD

@router.get("/highscores")
async def get_highscores() -> list[HighScoreItem]:
    scores: list[HighScoreItem] = [ HighScoreItem(rank=1,score=random.randint(300, 400), name=None) ]

    for i in range(1, 10):
        scores.append(HighScoreItem(rank=i + 1, score=math.ceil(scores[i - 1].score * random.randint(80, 100) / 100), name=None))

    return scores
