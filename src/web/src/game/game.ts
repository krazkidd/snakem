import { Game } from 'phaser';

import Demo from './scenes/Demo';

export function createGame(): Game {
  return new Game({
    type: Phaser.AUTO,
    //disableContextMenu: true,
    disablePreFX: true,
    disablePostFX: true,
    failIfMajorPerformanceCaveat: true,
    //loaderAsync: true,
    //callbacks: {
    //  preBoot: (game) => { },
    //  postBoot: (game) => { }
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
      expandParent: false,
      width: 800,
      height: 800
    },
    scene: Demo
  });
}
