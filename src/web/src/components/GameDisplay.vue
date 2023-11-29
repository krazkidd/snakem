<script setup lang="ts">
    import { onMounted } from 'vue';

    import { Game } from 'phaser';

    import Demo from '../scenes/Demo';

    let game;

    onMounted(() => {
        game = new Game({
            width: "100%",
            height: "100%",
            type: Phaser.AUTO,
            parent: 'game',
            audio: {
                disableWebAudio: true
            },
            physics: {
                default: 'arcade',
                arcade: {
                    fps: 60,
                    gravity: {y : 0},
                }
            },
            scene: Demo
        });
    });
</script>

<template>
    <div id="game">
    </div>
</template>
