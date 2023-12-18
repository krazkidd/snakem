<script setup lang="ts">
  import { ref, shallowRef, watchEffect } from 'vue';

  import { Game, Scene } from 'phaser';

  const props = defineProps<{
    startGame: boolean,
    startingScene: Scene,
  }>();

  const parent = ref(null);
  const game = shallowRef<Game>();

  watchEffect(() => {
    if (parent.value && props.startGame) {
      game.value?.destroy(true);

      game.value = new Game({
        type: Phaser.AUTO,
        //disableContextMenu: true,
        disablePreFX: true,
        disablePostFX: true,
        failIfMajorPerformanceCaveat: true,
        //loaderAsync: true,
        //callbacks: {
        //  preBoot: (game) => { },
        //  postBoot: (game) => { }
        //},
        audio: {
          disableWebAudio: true
        },
        scale: {
          autoCenter: Phaser.Scale.CENTER_BOTH,
          mode: Phaser.Scale.FIT,
          parent: parent.value,
          expandParent: false,
          width: 800,
          height: 800
        },
        scene: props.startingScene,
        fps: {
          limit: 20,
          smoothStep: false,
        }
      });
    } else {
      game.value?.destroy(true);
    }
  });
</script>

<template>
  <div ref="parent" />
</template>
