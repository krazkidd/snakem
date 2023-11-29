<script setup lang="ts">
  import { shallowRef, watchPostEffect } from 'vue';

  import { Game } from 'phaser';

  import { createGame } from '../game/game';

  const props = withDefaults(defineProps<{
    startGame?: boolean
  }>(), {
    startGame: false
  });

  let game = shallowRef<Game>();

  watchPostEffect(() => {
    if (props.startGame) {
      if (game.value) {
        game.value.destroy(true);
      }

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
