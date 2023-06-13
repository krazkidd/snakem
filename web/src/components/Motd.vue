<script setup>
  import { ref, onMounted } from 'vue'

  const motd = ref(null);
  const loading = ref(true);
  const error = ref(null);

  function fetchData() {
    loading.value = true;

    return fetch('/api/motd', {
      method: 'GET',
      headers: {
        'content-type': 'application/json'
      }
    })
    .then(res => {
      if (!res.ok) {
        const error = new Error(res.statusText);
        error.json = res.json();

        throw error;
      }

      return res.json();
    })
    .then(json => {
      motd.value = json;
    })
    .catch(err => {
      error.value = err;

      if (err.json) {
        return err.json.then(json => {
          error.value.message = json;
        });
      }
    })
    .then(() => {
      loading.value = false;
    });
  }

  onMounted(() => {
    fetchData();
  });
</script>

<template>
  <h2 class="text-center">{{ motd }}</h2>

  <p v-if="loading">
   Loading...
  </p>
  <p v-if="error">
  </p>
</template>

<style>
</style>