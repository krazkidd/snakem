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

import socket
import sys
from select import select
from struct import pack
from struct import unpack
from struct import calcsize

from SnakeConfig import *
from SnakeDebug import *
from SnakeEnums import *

MAX_MSG_SIZE = 1024

# net message header
# B: message type
# H: length of message (including header)
STRUCT_FMT_HDR = '!BH'

# number of lobbies
STRUCT_FMT_LOBBY_COUNT = '!B'

# info for single lobby
# B: lobby number
# H: port number
STRUCT_FMT_LOBBY = '!BH'

# game update message
# I: tick num of update (game time elapsed)
# B: new heading of player's snake
STRUCT_FMT_GAME_UPDATE = '!IB'

sock = None

def InitServerSocket(port=0):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', port))

    return sock.getsockname()[1] # return port

def InitClientSocket():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def CloseSocket():
    if sock:
        sock.close()

def UnpackMessage():
    msg, address = sock.recvfrom(MAX_MSG_SIZE)
    msgType, msgLen = unpack(STRUCT_FMT_HDR, msg[:calcsize(STRUCT_FMT_HDR)])
    #TODO verify msg size!
    if len(msg) > calcsize(STRUCT_FMT_HDR):
        return address, msgType, msg[calcsize(STRUCT_FMT_HDR):]
    else:
        return address, msgType, None

def SendMOTDTo(address):
    buf = pack(STRUCT_FMT_HDR, MessageType.MOTD, calcsize(STRUCT_FMT_HDR) + len(MOTD))
    buf += MOTD
    sock.sendto(buf, address)

def SendLobbyListTo(address, lobbies):
    buf = pack(STRUCT_FMT_HDR, MessageType.LOBBY_REP, calcsize(STRUCT_FMT_HDR) + calcsize(STRUCT_FMT_LOBBY_COUNT) + calcsize(STRUCT_FMT_LOBBY) * len(lobbies))
    buf += pack(STRUCT_FMT_LOBBY_COUNT, len(lobbies))
    for lobby in lobbies:
        buf += pack(STRUCT_FMT_LOBBY, lobby.lobbyNum, lobby.connectPort)

    sock.sendto(buf, address)

def UnpackLobbyList(msgBody):
    lobbyCount = unpack(STRUCT_FMT_LOBBY_COUNT, msgBody[:calcsize(STRUCT_FMT_LOBBY_COUNT)])[0]
    packedLobbies = msgBody[calcsize(STRUCT_FMT_LOBBY_COUNT):]

    lobbyList = []
    for i in range(lobbyCount):
        lobbyList.append(unpack(STRUCT_FMT_LOBBY, packedLobbies[i * calcsize(STRUCT_FMT_LOBBY):i * calcsize(STRUCT_FMT_LOBBY) + calcsize(STRUCT_FMT_LOBBY)]))

    return lobbyList

def SendSetupMessage(address):
    sock.sendto(pack(STRUCT_FMT_HDR, MessageType.SETUP, calcsize(STRUCT_FMT_HDR)), address)

def SendStartMessage(address):
    sock.sendto(pack(STRUCT_FMT_HDR, MessageType.START, calcsize(STRUCT_FMT_HDR)), address)

def SendHelloMessage():
    sock.sendto(pack(STRUCT_FMT_HDR, MessageType.HELLO, calcsize(STRUCT_FMT_HDR)), (HOST, SERVER_PORT))

def SendQuitMessageTo(address):
    if address:
        sock.sendto(pack(STRUCT_FMT_HDR, MessageType.LOBBY_QUIT, calcsize(STRUCT_FMT_HDR)), address)

def SendLobbyListRequest():
    sock.sendto(pack(STRUCT_FMT_HDR, MessageType.LOBBY_REQ, calcsize(STRUCT_FMT_HDR)), (HOST, SERVER_PORT))

def SendLobbyJoinRequestTo(address):
    sock.sendto(pack(STRUCT_FMT_HDR, MessageType.LOBBY_JOIN, calcsize(STRUCT_FMT_HDR)), address)

def SendReadyMessageTo(address):
    sock.sendto(pack(STRUCT_FMT_HDR, MessageType.READY, calcsize(STRUCT_FMT_HDR)), address)

def SendGameUpdateTo(address, packedUpdate):
    msg = pack(STRUCT_FMT_HDR, MessageType.UPDATE, calcsize(STRUCT_FMT_HDR) + calcsize(STRUCT_FMT_GAME_UPDATE))
    msg += packedUpdate
    sock.sendto(msg, address)

