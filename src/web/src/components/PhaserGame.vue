<script setup lang="ts">
  import { shallowRef, watchEffect, watchPostEffect } from 'vue';
  import { useWebSocket } from '@vueuse/core';

  import { Game } from 'phaser';

  import { createGame } from '../game/game';

  const props = withDefaults(defineProps<{
    startGame?: boolean
  }>(), {
    startGame: false
  });

  const emit = defineEmits<{
    (e: "wsMessage", message: string): void;
  }>();

  let game = shallowRef<Game>();
  let ws = useWebSocket('ws://' + (SERVER_HOST ? SERVER_HOST + ':' + SERVER_PORT : '') + '/ws');

  watchEffect(() => {
    if (ws.data.value) {
      emit('wsMessage', ws.data.value);
    }
  });

  watchPostEffect(() => {
    if (props.startGame) {
      game.value?.destroy(true);

      game.value = createGame();
    } else if (game.value) {
      game.value.destroy(true);
    }
  });
</script>

<template>
  <div id="phaser-game">

  </div>
</template>
