<script setup>
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

  import { useFetch } from '../composables/fetch.js'

  const { data, error } = useFetch('/api/highscores');
</script>

<template>
  <div class="alert alert-info" role="alert">
    <font-awesome-icon :icon="['fas', 'ranking-star']" />
    High Scores
  </div>

  <div v-if="error">Oops! Error encountered: {{ error.message }}</div>
  <div v-else-if="data">
    <ol class="fa-ul">
      <li v-for="highScoreItem of data">
        <span v-if="highScoreItem.rank <= 3" class="fa-li" :data-rank="highScoreItem.rank"><font-awesome-icon :icon="['fas', 'trophy']" /></span>
        <span v-else class="fa-li" :data-rank="highScoreItem.rank"><font-awesome-icon :icon="['fas', 'medal']" /></span>
        <strong>{{ highScoreItem.score }}</strong>
        <span v-if="highScoreItem.name"> &mdash; {{ highScoreItem.name }}</span>
      </li>
    </ol>
  </div>
  <div v-else>Loading...</div>
</template>

<style>
  span[data-rank="1"] {
    color: #ffd700;
  }

  span[data-rank="2"] {
    color: #c0c0c0;
  }

  span[data-rank="3"] {
    color: #8c7853;
  }
</style>