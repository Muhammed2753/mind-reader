// Sound Effects Manager
class SoundManager {
    constructor() {
        this.enabled = localStorage.getItem('soundEnabled') !== 'false';
        this.sounds = {
            click: new Audio('/static/sounds/click.mp3'),
            success: new Audio('/static/sounds/success.mp3'),
            wrong: new Audio('/static/sounds/wrong.mp3'),
            thinking: new Audio('/static/sounds/thinking.mp3')
        };
        
        // Set volumes
        Object.values(this.sounds).forEach(sound => {
            sound.volume = 0.3;
        });
    }
    
    play(soundName) {
        if (this.enabled && this.sounds[soundName]) {
            this.sounds[soundName].currentTime = 0;
            this.sounds[soundName].play().catch(() => {});
        }
    }
    
    toggle() {
        this.enabled = !this.enabled;
        localStorage.setItem('soundEnabled', this.enabled);
        return this.enabled;
    }
}

const soundManager = new SoundManager();

// Add click sounds to all buttons
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button').forEach(btn => {
        btn.addEventListener('click', () => soundManager.play('click'));
    });
});
