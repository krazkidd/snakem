<script setup lang="ts">
  import GameDisplay from '../components/GameDisplay.vue';
  import MessageOfTheDay from '../components/MessageOfTheDay.vue'
  import HighScores from '../components/HighScores.vue'
</script>

<template>
  <div class="row">
    <div class="col-12 col-sm-4 col-md-6 col-lg-8">
      <GameDisplay class="w-100 h-100" />
    </div>

    <div class="col">
      <MessageOfTheDay />

      <HighScores />
    </div>
  </div>
</template>

<style>
.row {
  min-height: 100vh;
}
</style>
