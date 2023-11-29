import { Scene } from 'phaser';

export default class Demo extends Scene
{
    constructor ()
    {
        super('demo');
    }

    preload ()
    {
        this.load.image('logo', '/favicon/favicon-32x32.png');
    }

    create ()
    {
        const logo = this.add.image(400, 70, 'logo');

        this.tweens.add({
            targets: logo,
            y: 350,
            duration: 1500,
            ease: 'Sine.inOut',
            yoyo: true,
            repeat: -1
        })
    }
}