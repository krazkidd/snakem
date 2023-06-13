<script setup>
  import { ref, onMounted } from 'vue'

  const data = ref(null);
  const loading = ref(true);
  const error = ref(null);

  function fetchData() {
    loading.value = true;

    return fetch('/api/highscores', {
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
      data.value = json;
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
  <div>High Scores</div>

  <ol v-if="!loading && data && data.length">
    <li v-for="score of data">
      <strong>{{ score }}</strong>
    </li>
  </ol>

  <p v-if="loading">
   Loading...
  </p>
  <p v-if="error">
  </p>
</template>

<style>
</style>