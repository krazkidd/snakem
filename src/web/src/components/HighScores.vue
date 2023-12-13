<script lang="ts" setup>
  import { useFetch } from '@vueuse/core';

  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

  import { type HighScoreItem } from '../types/api';

  const { execute, data, error } = useFetch('http://' + (SERVER_HOST ? SERVER_HOST + ':' + SERVER_PORT : '') + import.meta.env.BASE_URL + 'api/highscores').json();

  function handleRefreshClick() {
    execute();
  }
</script>

<template>
  <div class="d-flex justify-content-between mb-0 p-1">
    <div class="align-self-center text-info fs-5 mb-0">
      <font-awesome-icon :icon="['fas', 'ranking-star']" />
      High Scores
    </div>

    <button type="button" class="btn btn-outline-info btn-sm" @click="handleRefreshClick">
      <font-awesome-icon :icon="['fas', 'rotate']" />
    </button>
  </div>

  <div v-if="data" class="p-1">
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