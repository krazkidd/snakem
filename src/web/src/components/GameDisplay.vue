<script setup lang="ts">
    import { shallowRef } from 'vue';

    import { Game } from 'phaser';

    import Demo from '../scenes/Demo';

    let game = shallowRef<Game | null>(null);

    function handleClick() {
        if (!game.value) {
            game.value = new Game({
                type: Phaser.AUTO,
                //disableContextMenu: true,
                disablePreFX: true,
                disablePostFX: true,
                failIfMajorPerformanceCaveat: true,
                //loaderAsync: true,
                //callbacks: {
                //    preBoot: (game) => { },
                //    postBoot: (game) => { }
                //},
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
                scale: {
                    autoCenter: Phaser.Scale.CENTER_BOTH,
                    mode: Phaser.Scale.FIT,
                    parent: 'phaser-game',
                    //expandParent: true,
                    width: 800,
                    height: 800
                },
                scene: Demo
            });
        }
    };
</script>

<template>
    <div id="phaser-game">
        <button v-if="!game" type="button" class="btn btn-primary position-absolute top-50 start-50 translate-middle" :onclick="handleClick">Click to Start</button>
    </div>
</template>
