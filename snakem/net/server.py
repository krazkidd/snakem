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

import os
import sys

from ..config import server as cfg

from ..game import game
from . import net
from ..test import debug
from ..enums import GameState, MsgType

class MainServer:
    def __init__(self):
        self.__lobbies = []

    def start(self):
        debug.init_debug('MainServer', cfg.PRINT_DEBUG, cfg.PRINT_ERROR, cfg.PRINT_NETMSG)

        # start lobbies as separate processes
        for i in range(1, cfg.NUM_LOBBIES + 1):
            lobby = LobbyServer(i)
            pid = os.fork()
            if pid == 0:
                lobby.start()
                sys.exit(0)
            self.__lobbies.append(lobby)

        net.init_server_socket(cfg.BIND_ADDR)

        print(f'Main server has started on port {cfg.BIND_ADDR[1]}. Waiting for clients...')

        try:
            while True:
                net.wait_for_input(self)
        except Exception as ex:
            debug.print_err(str(ex))
        finally:
            net.close_socket()

    def handle_net_message(self, address, msg_type, msg_body):
        if msg_type == MsgType.HELLO:
            net.send_motd(address, cfg.MOTD)
        elif msg_type == MsgType.LOBBY_REQ:
            net.send_lobby_list(address, self.__lobbies)

class LobbyServer(MainServer):
    def __init__(self, lobbyNum):
        MainServer.__init__(self)

        # unique server ID #
        self.lobby_num = lobbyNum
        self.connect_port = net.init_server_socket((cfg.BIND_ADDR[0], 0)) # port = 0 will use random port

        self.server_state = None

        # activePlayers maps net addresses to tuples of (r, s) where:
        #   r = ready status (MsgType.{NOT_,}READY)
        #   s = snake id when a game is running
        self.active_players = dict()

        self.game = None

    def start(self):
        debug.init_debug('LobbyServer', cfg.PRINT_DEBUG, cfg.PRINT_ERROR, cfg.PRINT_NETMSG)

        print(f'Lobby server {self.lobby_num} has started on port {self.connect_port}. Waiting for clients...')

        self._start_lobby_mode()

        tick_time = 0.0

        try:
            while True:
                net.wait_for_input(self, self.server_state != GameState.GAME)

                if self.server_state == GameState.GAME:
                    tick_time += net.TIMEOUT
                    if tick_time >= cfg.STEP_TIME:
                        tick_time -= cfg.STEP_TIME
                        self.game.tick()

                        for addr in self.active_players:
                            for snake_id, snake in self.game.snakes.items():
                                debug.print_debug('(' + str(snake.body[0][0]) + ', ' + str(snake.body[0][1]) + ')')
                                net.send_snake_update(addr, self.game.tick_num, snake_id, snake)

                        # end game when all snakes are dead
                        #TODO the game should end when at most *one* snake is alive
                        for snake in self.game.snakes.values():
                            if snake.is_alive:
                                break
                            #TODO does this have the correct indentation?
                            else:
                                self._end_game_mode()
                                self._start_lobby_mode()
        except Exception as ex:
            debug.print_err(f'{self.lobby_num}: {ex}')
        finally:
            net.close_socket()

    def handle_net_message(self, address, msg_type, msg_body):
        if address in self.active_players:
            if self.server_state == GameState.GAME:
                self._handle_net_message_during_game(address, msg_type, msg_body)
            elif self.server_state == GameState.LOBBY:
                status, snake_id = self.active_players[address]

                if msg_type == MsgType.LOBBY_JOIN:
                    net.send_lobby_join_request(address)  # LOBBY_JOIN is used for join confirmation
                    self.active_players[address] = (MsgType.NOT_READY, snake_id)  # reset READY status
                elif msg_type == MsgType.LOBBY_QUIT:
                    del self.active_players[address]
                elif msg_type == MsgType.READY:
                    self.active_players[address] = (MsgType.READY, snake_id)

                    for addr, player_tuple in self.active_players.items():
                        if player_tuple[0] != MsgType.READY:
                            break
                    else:
                        self._start_game_mode()
                elif msg_type == MsgType.NOT_READY:
                    self.active_players[address] = (MsgType.NOT_READY, snake_id)
        else:  # address not in self.activePlayers
            if self.server_state == GameState.LOBBY:
                if msg_type == MsgType.LOBBY_JOIN:
                    if len(self.active_players) < 4:
                        net.send_lobby_join_request(address)  # LOBBY_JOIN is used for join confirmation
                        self.active_players[address] = (MsgType.NOT_READY, None)
                    else:
                        net.send_quit_message(address)  # LOBBY_QUIT is used for join rejection

    def _handle_net_message_during_game(self, address, msg_type, msg_body):
        do_update_clients = False

        if msg_type == MsgType.INPUT:
            self.game.snakes[self.active_players[address][1]].change_heading(net.unpack_input_message(msg_body))
            do_update_clients = True

        if do_update_clients:
            for addr in self.active_players:
                for snake_id, snake in self.game.snakes.items():
                    net.send_snake_update(addr, self.game.tick_num, snake_id, snake)

    def _start_lobby_mode(self):
        self.server_state = GameState.LOBBY

    def _start_game_mode(self):
        self.server_state = GameState.GAME

        self.game = game.Game(cfg.WIN_WIDTH, cfg.WIN_HEIGHT)

        for addr, player_tuple in self.active_players.items():
            self.active_players[addr] = (player_tuple[0], self.game.spawn_new_snake())

        self.game.spawn_new_pellet()

        for addr in self.active_players:
            for snake_id, snake in self.game.snakes.items():
                net.send_snake_update(addr, self.game.tick_num, snake_id, snake)

        for addr in self.active_players:
            net.send_start_message(addr)

    def _end_game_mode(self):
        for addr in self.active_players:
            net.send_end_message(addr)

        self.game = None
