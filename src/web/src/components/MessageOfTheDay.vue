<script lang="ts" setup>
  import { useFetch } from '@vueuse/core';

  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

  const { data, error } = useFetch('http://' + (SERVER_HOST ? SERVER_HOST + ':' + SERVER_PORT : '') + '/api/motd').json();
</script>

<template>
  <div class="text-info fs-5 mb-0 p-1">
    <font-awesome-icon :icon="['fas', 'newspaper']" />
    Message of the Day
  </div>

  <div v-if="data" class="fs-5 font-weight-bold p-1">
    {{ data }}
  </div>
  <div v-else-if="error">Oops! Error encountered: {{ error }}</div>
  <div v-else>Loading...</div>
</template>

<style>
</style>