<script lang="ts" setup>
  import { useFetch } from '@vueuse/core';

  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

  import { type HighScoreItem } from '../types/api';

  const { data, error } = useFetch(__SERVER_URL__ + '/api/highscores').json();
</script>

<template>
  <div class="alert alert-info" role="alert">
    <font-awesome-icon :icon="['fas', 'ranking-star']" />
    High Scores
  </div>

  <div v-if="data">
    <ol class="fa-ul">
      <li v-for="highScoreItem of (data as HighScoreItem[])" :key="highScoreItem.rank">
        <span v-if="highScoreItem.rank <= 3" class="fa-li" :data-rank="highScoreItem.rank"><font-awesome-icon :icon="['fas', 'trophy']" /></span>
        <span v-else class="fa-li" :data-rank="highScoreItem.rank"><font-awesome-icon :icon="['fas', 'medal']" /></span>
        <strong>{{ highScoreItem.score }}</strong>
        <span v-if="highScoreItem.name"> &mdash; {{ highScoreItem.name }}</span>
      </li>
    </ol>
  </div>
  <div v-else-if="error">Oops! Error encountered: {{ error }}</div>
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