import { Scene } from 'phaser';

export default class Snakem extends Scene
{
    private snake?: Phaser.GameObjects.Image;
    private pellet?: Phaser.GameObjects.Image;

    private cursors?: Phaser.Types.Input.Keyboard.CursorKeys;

    constructor() {
        super('snakem');
    }

    preload() {
        // this.load.svg('snake', '/1f34e.svg');
        // this.load.svg('pellet', '/1f40d.svg');
        this.load.image('snake', '/1f34e.png');
        this.load.image('pellet', '/1f40d.png');
    }

    create() {
        this.snake = this.add.image(400, 70, 'snake').setOrigin(0, 0);

        this.pellet = this.add.image(400, 140, 'pellet').setOrigin(0, 0);

        //this.cursors = this.input.keyboard?.createCursorKeys();

        //TODO add score text
        //scoreText = this.add.text(16, 16, 'score: 0', { fontSize: '32px', fill: '#000' });
    }

    // update(time: number, delta: number): void {
    //     if (this.cursors?.left.isDown) {
    //         //this.snake.setVelocityX(-160);

    //         //this.snake.anims.play('left', true);
    //     } else if (this.cursors?.right.isDown) {
    //         //this.snake.setVelocityX(160);

    //         //this.snake.anims.play('right', true);
    //     } else {
    //         //this.snake.setVelocityX(0);

    //         //this.snake.anims.play('turn');
    //     }

    //     // if (this.cursors?.up.isDown && this.snake?.body.touching.down) {
    //     //     //this.snake.setVelocityY(-330);
    //     // }
    // }
}