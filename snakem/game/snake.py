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

from collections import deque

from ..enums import Dir

class Snake:

    """This is the human player's avatar in the game.

    For every tick of the game world, the Snake moves. And for every
    pellet it eats, its length grows.

    """

    def __init__(self, head_pos: tuple[int, int], heading: Dir, length: int = 4) -> None:
        self.body: deque[tuple[int, int]] = deque()

        x_pos, y_pos = head_pos
        for i in range(length):
            if heading == Dir.RIGHT:
                self.body.append((x_pos - i, y_pos))
            elif heading == Dir.LEFT:
                self.body.append((x_pos + i, y_pos))
            elif heading == Dir.UP:
                self.body.append((x_pos, y_pos + i))
            elif heading == Dir.DOWN:
                self.body.append((x_pos, y_pos - i))

        self.heading: Dir = heading
        self.is_alive: bool = True

        self.__next_heading: Dir | None = None
        self.__heading_changed: bool = False
        self.__should_grow: bool = False

    def grow(self) -> None:

        """Grow the Snake one segment longer.

        This is called whenever a snake eats a pellet.

        """

        # this just sets a flag so that on the next move(),
        # the last body segment won't be popped off
        self.__should_grow = True

    def move(self) -> None:

        """Move (update) the snake's body.

        This should be called once for every game tick.

        """

        if self.is_alive:
            x_pos, y_pos = self.body[0]

            # check the heading of the snake and move the
            # head's position accordingly
            if self.heading == Dir.RIGHT:
                self.body.appendleft((x_pos + 1, y_pos))
            elif self.heading == Dir.LEFT:
                self.body.appendleft((x_pos - 1, y_pos))
            elif self.heading == Dir.UP:
                self.body.appendleft((x_pos, y_pos - 1))
            elif self.heading == Dir.DOWN:
                self.body.appendleft((x_pos, y_pos + 1))

            # pop the last body segment unless the snake is supposed to grow
            if self.__should_grow:
                self.__should_grow = False
            else:
                self.body.pop()

            if self.__next_heading:
                self.heading = self.__next_heading
                self.__next_heading = None

            self.__heading_changed = False

    def change_heading(self, new_heading: Dir) -> bool:

        """Tell the Snake the new direction to move in.

        The Snake cannot go backwards, so the only real change that
        can happen is to turn left or right.

        Returns False if there was no heading change; True if there was
        a change.

        """

        # if heading was already changed, queue the change for
        # the next move()
        if self.__heading_changed:
            self.__next_heading = new_heading
            return False

        # skip if move is parallel
        if (self.heading in (Dir.UP, Dir.DOWN) and new_heading in (Dir.UP, Dir.DOWN)) \
           or (self.heading in (Dir.LEFT, Dir.RIGHT) and new_heading in (Dir.LEFT, Dir.RIGHT)):
            return False

        self.heading = new_heading
        self.__heading_changed = True

        return True
