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

import random

class Pellet:

    """This is what the Snake eats.

    Holds a randomized position."""

    def __init__(self, min_x: int, min_y: int, max_x: int, max_y: int):

        """On creation, randomly set a position using the
        given arguments as maximum values."""

        self.__min_x: int = min_x
        self.__min_y: int  = min_y
        self.__max_x: int  = max_x
        self.__max_y: int  = max_y

        self.pos: tuple[int, int] = (min_x, min_y)
        self.randomize_position()

    def randomize_position(self) -> None:
        self.pos = (random.randint(self.__min_x, self.__max_x), random.randint(self.__min_y, self.__max_y))
