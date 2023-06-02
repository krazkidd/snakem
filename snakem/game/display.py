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

import curses
import logging

from .game import Game

_last_debug_message: str = ''

def show_message(scr: curses.window, msg: str) -> None:
    logging.info(msg)

    erase(scr)
    height, width = get_window_size(scr)
    scr.addstr(height // 2, max(0, width // 2 - len(msg) // 2), msg)
    scr.refresh()

def show_lobby(scr: curses.window, motd: str | None = None) -> None:
    if motd:
        show_message(scr, motd)
    else:
        show_message(scr, 'Waiting for game to start . . .')

def show_game(scr: curses.window, game: Game) -> None:
    height, width = get_window_size(scr)

    scr.erase()

    scr.hline(0, 0, curses.ACS_HLINE, min(width, game.width) - 1)
    scr.vline(0, 0, curses.ACS_VLINE, min(height, game.height) - 1)

    if game.height <= height:
        scr.hline(game.height, 0, curses.ACS_HLINE, min(width, game.width) - 1)

    if game.width <= width:
        scr.vline(0, game.width - 1, curses.ACS_VLINE, min(height, game.height) - 1)

    debug_str = ''
    for snake in game.snakes.values():
        if len(debug_str) > 0:
            debug_str += ', '

        for x_pos, y_pos in snake.body:
            if 0 <= x_pos <= width - 1 and 0 <= y_pos <= height - 1:
                if (x_pos, y_pos) == snake.body[0]:
                    scr.addch(y_pos, x_pos, ord('X'))
                else:
                    scr.addch(y_pos, x_pos, ord('O'))

        debug_str += 'snake: ' + str(len(snake.body))

    if game.pellet is not None:
        if 0 <= game.pellet.pos[0] <= width - 1 and 0 <= game.pellet.pos[1] <= height - 1:
            scr.addch(game.pellet.pos[1], game.pellet.pos[0], ord('+'))

    #TODO name the snakes and show score at the top?
    #show_debug_in_game(debugStr)
    show_debug_in_game(scr)

    scr.refresh()

def show_debug(scr: curses.window, msg: str | None = None) -> None:
    global _last_debug_message

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        height, width = scr.getmaxyx()
        if msg and len(msg) > 0:
            logging.debug(msg)

            msg += ' '
            msg = msg[:width - 1]
            _last_debug_message = msg
        else:
            msg = _last_debug_message
        scr.addstr(height - 1, 0, msg)
        scr.hline(height - 1, len(msg), ord('-'), width - len(msg))

def show_debug_in_game(scr: curses.window, msg: str | None = None) -> None:
    global _last_debug_message

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        height, width = scr.getmaxyx()
        if msg and len(msg) > 0:
            logging.debug(msg)

            msg = ' ' + msg + ' '
            # truncate very long messages
            msg = msg[:width - 1 - 2] # - 2 because we start at cell 2
            _last_debug_message = msg
        else:
            msg = _last_debug_message
        scr.addstr(height - 1, 2, msg)

def get_window_size(scr: curses.window) -> tuple[int, int]:
    height, width = scr.getmaxyx()
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        height -= 1
    return height, width

def get_key(scr: curses.window) -> int:
    return scr.getch()

def erase(scr: curses.window) -> None:
    scr.erase()
    show_debug(scr)
    scr.refresh()
