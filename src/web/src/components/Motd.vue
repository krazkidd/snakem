<script setup>
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

  import { useFetch } from '../composables/fetch.js'

  const { data, error } = useFetch(__SERVER_URL__ + '/api/motd');
</script>

<template>
  <div class="alert alert-info" role="alert">
    <font-awesome-icon :icon="['fas', 'newspaper']" />
    Message of the Day
  </div>

  <div v-if="error">Oops! Error encountered: {{ error.message }}</div>
  <div v-else-if="data">
    {{ data }}
  </div>
  <div v-else>Loading...</div>
</template>

<style>
</style>