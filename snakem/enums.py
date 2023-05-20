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

class Dir:
    """An enum of the cardinal directions."""
    Up, Down, Left, Right = range(4)

class GameState:
    MOTD, LOBBY, GAME_SETUP, GAME, GAME_OVER = range(5)

class MsgFmt:
    # net message header
    # B: message type
    # H: length of message (including header)
    HDR = '!BH'

    # number of lobbies
    LBY_CNT = '!B'

    # info for single lobby
    # B: lobby number
    # H: port number
    LBY = '!BH'

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

    # client/player input
    # B: new heading
    PLAYER_INPUT = '!B'

class MsgType:
    """Enum for Snake network messages"""

    NONE, HELLO, MOTD, LOBBY_REQ, LOBBY_REP, LOBBY_JOIN, LOBBY_QUIT, \
       READY, NOT_READY, START, END, SNAKE_UPDATE, CHAT, SETUP, INPUT = range(15)

    @staticmethod
    def get_name(msg_type):
        if msg_type == MsgType.NONE:
            return "NONE"
        elif msg_type == MsgType.HELLO:
            return "HELLO"
        elif msg_type == MsgType.MOTD:
            return "MOTD"
        elif msg_type == MsgType.LOBBY_REQ:
            return "LOBBY_REQ"
        elif msg_type == MsgType.LOBBY_REP:
            return "LOBBY_REP"
        elif msg_type == MsgType.LOBBY_JOIN:
            return "LOBBY_JOIN"
        elif msg_type == MsgType.LOBBY_QUIT:
            return "LOBBY_QUIT"
        elif msg_type == MsgType.READY:
            return "READY"
        elif msg_type == MsgType.NOT_READY:
            return "NOT_READY"
        elif msg_type == MsgType.START:
            return "START"
        elif msg_type == MsgType.END:
            return "END"
        elif msg_type == MsgType.SNAKE_UPDATE:
            return "SNAKE_UPDATE"
        elif msg_type == MsgType.CHAT:
            return "CHAT"
        elif msg_type == MsgType.SETUP:
            return "SETUP"
        elif msg_type == MsgType.INPUT:
            return "INPUT"
