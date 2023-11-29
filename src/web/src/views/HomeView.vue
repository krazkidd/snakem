<script setup lang="ts">
  import { ref } from 'vue';

  import PhaserGame from '../components/PhaserGame.vue';
  import MessageOfTheDay from '../components/MessageOfTheDay.vue';
  import HighScores from '../components/HighScores.vue';

  const gameStarted = ref(false);
</script>

<template>
  <div class="row h-100">
    <div class="col-12 col-sm-4 col-md-6 col-lg-8 h-100">
      <PhaserGame :startGame="gameStarted" />
    </div>

    <div class="col p-2">
      <div class="mb-2">
        <button type="button"
          :class="{ 'btn-success': !gameStarted, 'btn-outline-danger': gameStarted }"
          class="btn"
          @click="gameStarted = !gameStarted"
        >
          {{ gameStarted ? 'Stop Game' : 'Start Game' }}
        </button>
      </div>

      <MessageOfTheDay />

      <HighScores />
    </div>
  </div>
</template>
