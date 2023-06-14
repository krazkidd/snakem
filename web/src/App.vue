<script setup>
  import Motd from './components/Motd.vue'
  import HighScores from './components/HighScores.vue'
</script>

<template>
  <nav class="navbar navbar-expand-md navbar-dark bg-dark">
    <a class="navbar-brand" href="#">Snake-M</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarCollapse">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
        </li>
      </ul>
    </div>
  </nav>

  <main role="main" class="container-fluid mt-2">
    <div class="row">
      <div class="col-12 col-sm-4 col-md-6 col-lg-8">

      </div>

      <div class="col">
        <Motd />

        <HighScores />
      </div>
    </div>
  </main>
</template>

<style>
</style>
