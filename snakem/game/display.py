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
import os
import logging

_stdscr = None

_app_callback = None

_last_debug_message = ''

def init_client_window(app_callback):
    global _app_callback
    _app_callback = app_callback

    # set shorter delay for ESC key recognition
    if 'ESCDELAY' not in os.environ:
        os.environ.setdefault('ESCDELAY', '75')

    # cbreak on, echo off, keypad on, colors on
    curses.wrapper(_wrapper_callback)

def _wrapper_callback(scr):
    global _stdscr
    _stdscr = scr

    if curses.curs_set(0) == curses.ERR:
        show_debug('Can\'t hide cursor')

    _app_callback()

def show_message(msg):
    erase()
    height, width = get_window_size()
    _stdscr.addstr(height // 2, max(0, width // 2 - len(msg) // 2), msg)
    _stdscr.refresh()

def show_lobby(motd):
    if motd:
        show_message(motd)
    else:
        show_message('Waiting for game to start . . .')

def show_game(game):
    height, width = get_window_size()

    _stdscr.erase()

    _stdscr.hline(0, 0, curses.ACS_HLINE, min(width, game.width) - 1)
    _stdscr.vline(0, 0, curses.ACS_VLINE, min(height, game.height) - 1)

    if game.height <= height:
        _stdscr.hline(game.height, 0, curses.ACS_HLINE, min(width, game.width) - 1)

    if game.width <= width:
        _stdscr.vline(0, game.width - 1, curses.ACS_VLINE, min(height, game.height) - 1)

    debug_str = ''
    for snake in game.snakes.values():
        if len(debug_str) > 0:
            debug_str += ', '

        for x_pos, y_pos in snake.body:
            if 0 <= x_pos <= width - 1 and 0 <= y_pos <= height - 1:
                if (x_pos, y_pos) == snake.body[0]:
                    _stdscr.addch(y_pos, x_pos, ord('X'))
                else:
                    _stdscr.addch(y_pos, x_pos, ord('O'))

        debug_str += 'snake: ' + str(len(snake.body))

    if game.pellet is not None:
        if 0 <= game.pellet.pos[0] <= width - 1 and 0 <= game.pellet.pos[1] <= height - 1:
            _stdscr.addch(game.pellet.pos[1], game.pellet.pos[0], ord('+'))

    #TODO name the snakes and show score at the top?
    #show_debug_in_game(debugStr)
    show_debug_in_game()

    _stdscr.refresh()

def show_debug(msg=None):
    global _last_debug_message

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        height, width = get_window_size()
        if msg and len(msg) > 0:
            msg += ' '
            msg = msg[:width - 1]
            _last_debug_message = msg
        else:
            msg = _last_debug_message
        _stdscr.addstr(height - 1, 0, msg)
        _stdscr.hline(height - 1, len(msg), ord('-'), width - len(msg))

def show_debug_in_game(msg=None):
    global _last_debug_message

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        height, width = get_window_size()
        if msg and len(msg) > 0:
            msg = ' ' + msg + ' '
            # truncate very long messages
            msg = msg[:width - 1 - 2] # - 2 because we start at cell 2
            _last_debug_message = msg
        else:
            msg = _last_debug_message
        _stdscr.addstr(height - 1, 2, msg)

def get_window_size():
    height, width = _stdscr.getmaxyx()
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        height -= 1
    return height, width

def get_key():
    return _stdscr.getch()

def erase():
    _stdscr.erase()
    show_debug()
    _stdscr.refresh()
