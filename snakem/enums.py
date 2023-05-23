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

from enum import Enum
from enum import IntEnum

class Dir(Enum):
    """An enum of the cardinal directions."""

    #TODO use auto()?

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class GameState(Enum):
    #TODO use auto()?

    LOBBY = 0
    GAME = 1

class MsgFmt:
    # net message header
    # B: message type
    # H: length of message (including header)
    HDR = '!BH'

    # start message
    # i: window width
    # i: window height
    START = '!ii'

    # snake update message (header)
    # I: tick num (game time elapsed)
    # i: snake ID
    # B: heading
    # ?: is alive
    # I: body length
    SNAKE_UPDATE_HDR = '!IiB?I'

    # snake update message (snake body)
    # i: x position
    # i: y position
    SNAKE_UPDATE_BDY = '!ii'

    # pellet update message
    # I: tick num (game time elapsed)
    # i: pellet ID
    # i: x position
    # i: y position
    PELLET_UPDATE = '!Iiii'

    # client/player input
    # B: new heading
    PLAYER_INPUT = '!B'

class MsgType(Enum):
    """Enum for Snake network messages"""

    #TODO use auto()?

    MOTD = 0
    LOBBY_JOIN = 1
    LOBBY_QUIT = 2
    READY = 3
    NOT_READY = 4
    START = 5
    SNAKE_UPDATE = 6
    PELLET_UPDATE = 7
    CHAT = 8
    SETUP = 9
    INPUT = 10
