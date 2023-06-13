<script setup>
  import Motd from './components/Motd.vue'
  import HighScores from './components/HighScores.vue'
</script>

<template>
  <main class="container">
    <div class="row">
      <div class="col-12 col-sm-4 col-md-6 col-lg-8">
        <Motd />
      </div>

      <div class="col">
        <HighScores />
      </div>
    </div>
  </main>

  <main>
  </main>
</template>

<style>
</style>
