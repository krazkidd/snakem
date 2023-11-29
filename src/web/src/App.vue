<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink, RouterView } from 'vue-router';

import PhaserGame from './components/PhaserGame.vue';

const gameStarted = ref(false);
</script>

<template>
  <main role="main" class="h-100">
    <div class="row h-100">
      <div class="col-12 col-sm-4 col-md-6 col-lg-8 h-100">
        <PhaserGame :startGame="gameStarted" />
      </div>

      <div class="col">
        <nav class="navbar navbar-expand-md navbar-dark bg-dark px-2">
          <RouterLink class="navbar-brand" to="/">Snake-M</RouterLink>

          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>

          <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="navbar-nav mr-auto">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/" activeClass="active">Home</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/about" activeClass="active">About</RouterLink>
              </li>
            </ul>
          </div>
        </nav>

        <div class="m-2">
          <button type="button"
            :class="{ 'btn-success': !gameStarted, 'btn-outline-danger': gameStarted }"
            class="btn"
            @click="gameStarted = !gameStarted"
          >
            {{ gameStarted ? 'Stop Game' : 'Start Game' }}
          </button>
        </div>

        <RouterView />
      </div>
    </div>
  </main>
</template>
