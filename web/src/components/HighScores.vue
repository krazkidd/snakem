<script setup>
  import { useFetch } from '../composables/fetch.js'

  const { data, error } = useFetch('/api/highscores');
</script>

<template>
  <div v-if="error">Oops! Error encountered: {{ error.message }}</div>
  <div v-else-if="data">
    <div>High Scores</div>

    <ol>
      <li v-for="score of data">
        <strong>{{ score }}</strong>
      </li>
    </ol>
  </div>
  <div v-else>Loading...</div>
</template>

<style>
</style>