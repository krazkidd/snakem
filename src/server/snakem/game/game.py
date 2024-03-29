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

from .pellet import Pellet
from .snake import Snake
from .enums import Dir

class Game:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height

        self.snakes: dict[int, Snake] = dict()
        self.pellet: Pellet

        self.tick_num: int = 0

        self.spawn_new_pellet()

    def tick(self) -> None:
        # move all snakes before checking collisions
        for snake in self.snakes.values():
            snake.move()

        for snake in self.snakes.values():
            # check with other snakes
            for other_snake in self.snakes.values():
                if snake is not other_snake and snake.body[0] in other_snake.body:
                    snake.is_alive = False

            x_pos, y_pos = snake.body[0]
            # check boundaries
            if x_pos in (0, self.width - 1) or y_pos in (0, self.height - 1):
                snake.is_alive = False
            # check pellet
            elif snake.body[0] == self.pellet.pos: # type: ignore
                snake.grow()
                self.spawn_new_pellet()

        self.tick_num += 1

    def spawn_new_snake(self, snake_id: int | None = None) -> int | None:
        # NOTE: Only 4 snakes are supported.

        if snake_id is None:
            snake_id = len(self.snakes)

            if snake_id >= 4:
                return None

        start_pos = [
            (self.width // 4, self.height // 4),
            (self.width - self.width // 4, self.height // 4),
            (self.width - self.width // 4, self.height - self.height // 4),
            (self.width // 4, self.height - self.height // 4)
        ]

        self.snakes[snake_id] = Snake(start_pos[snake_id], Dir(snake_id % 4))

        return snake_id

    def spawn_new_pellet(self) -> None:
        self.pellet = Pellet(1, 1, self.width - 1 - 1, self.height - 1 - 1)

        # make sure pellet doesn't appear on top of a snake...
        is_good_pos = False
        while not is_good_pos:
            for snake in self.snakes.values():
                if self.pellet.pos in snake.body:
                    self.pellet.randomize_position()
                    break
            else:
                is_good_pos = True

    def update_snake(self, snake_id: int, heading: Dir, is_alive: bool, body: list[tuple[int, int]]) -> None:
        if snake_id not in self.snakes:
            # just add the snake, I guess?
            self.spawn_new_snake(snake_id)

        snake = self.snakes[snake_id]
        snake.heading = heading
        snake.is_alive = is_alive
        snake.body = body

    def update_pellet(self, pellet_id: int, pos_x: int, pos_y: int) -> None:
        if not self.pellet:
            self.pellet = Pellet(1, 1, self.width - 1 - 1, self.height - 1 - 1)

        self.pellet.pos = (pos_x, pos_y)
