<script setup>
  import { useFetch } from '../composables/fetch.js'

  const { data, error } = useFetch('/api/motd');
</script>

<template>
  <div v-if="error">Oops! Error encountered: {{ error.message }}</div>
  <div v-else-if="data">
    <h2 class="text-center">{{ data }}</h2>
  </div>
  <div v-else>Loading...</div>
</template>

<style>
</style>