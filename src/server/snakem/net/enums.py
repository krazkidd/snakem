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

class GameState(Enum):
    #TODO use auto()?

    LOBBY = 0
    GAME = 1

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
