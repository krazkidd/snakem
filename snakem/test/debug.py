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

import datetime
import sys

from ..enums import MsgType

_name = 'None'

DO_PRINT_DEBUG = False
DO_PRINT_ERROR = False
DO_PRINT_NET_MSG = False

def init_debug(name, debug, error, net_msg):
    global _name, DO_PRINT_DEBUG, DO_PRINT_ERROR, DO_PRINT_NET_MSG

    _name = str(name)
    DO_PRINT_DEBUG = debug
    DO_PRINT_ERROR = error
    DO_PRINT_NET_MSG = net_msg

def print_debug(msg):
    if DO_PRINT_DEBUG:
        print(f'DEBUG ({datetime.datetime.now().strftime("%H:%M:%S")}) {_name}: {msg}')

def print_err(msg):
    if DO_PRINT_ERROR:
        print(f'ERROR ({datetime.datetime.now().strftime("%H:%M:%S")}) {_name} (line {sys.exc_info()[-1].tb_lineno}): {msg}')

def get_net_msg(address, to_or_from_str, msg_type, msg_body=None, addl_info=None):
    if msg_body:
        body_length = str(len(msg_body))
    else:
        body_length = '0'

    #TODO find out if addl_info, as a reference, is being changed after function returns
    if addl_info and  len(addl_info) > 0:
        addl_info = ' ' + addl_info
    else:
        addl_info = ''

    return f'NETMSG ({to_or_from_str} {address[0]}) {_name}: <{MsgType.get_name(msg_type)}, length {body_length}> {addl_info}'

def print_net_msg_sent(address, msg_type, msg_body=None, addl_info=None):
    if DO_PRINT_NET_MSG:
        print(get_net_msg(address, 'to', msg_type, msg_body, addl_info))

def print_net_msg_received(address, msg_type, msg_body=None, addl_info=None):
    if DO_PRINT_NET_MSG:
        print(get_net_msg(address, 'from', msg_type, msg_body, addl_info))
