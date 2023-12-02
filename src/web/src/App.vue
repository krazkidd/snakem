<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import { RouterLink, RouterView } from 'vue-router';

import { useWebSocket } from '@vueuse/core';

import PhaserGame from './components/PhaserGame.vue';

import { MsgType } from './game/enums';
import { sendMessage } from './game/net';
import type { Message } from './game/net';
import Snakem from './game/scenes/Snakem';

const ws = useWebSocket<Message>('ws://' + (SERVER_HOST ? SERVER_HOST + ':' + SERVER_PORT : '') + '/ws');

const gameStarted = ref(false);

watchEffect(() => {
  if (ws.data.value) {
    //TODO handle message

    if (import.meta.env.DEV) {
      console.log(ws.data.value);
    }
  }
});

watchEffect(() => {
  if (gameStarted.value) {
    //TODO these should wait for user input
    sendMessage<Message>(ws, MsgType.LOBBY_JOIN);
    sendMessage<Message>(ws, MsgType.READY);
  }
});
</script>

<template>
  <main role="main" class="h-100">
    <div class="row h-100">
      <div class="col-12 col-sm-8 col-md-6 col-xl-4 h-100">
        <PhaserGame :startGame="gameStarted" :startingScene="Snakem" />
      </div>

      <div class="col">
        <nav class="navbar navbar-expand-md navbar-dark bg-dark px-2">
          <RouterLink class="navbar-brand" to="/">Snake-M</RouterLink>

          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>

          <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="navbar-nav mr-auto">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/" activeClass="active">Home</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/about" activeClass="active">About</RouterLink>
              </li>
            </ul>
          </div>
        </nav>

        <div class="m-2">
          <button type="button"
            :class="{ 'btn-success': !gameStarted, 'btn-outline-danger': gameStarted }"
            class="btn"
            @click="gameStarted = !gameStarted"
          >
            {{ gameStarted ? 'Stop Game' : 'Start Game' }}
          </button>
        </div>

        <RouterView />

        <BToaster />
      </div>
    </div>
  </main>
</template>
