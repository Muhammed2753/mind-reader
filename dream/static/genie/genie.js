// genie.js — Football Oracle Animation Engine
// Reactions: meditating → yes / no / sometimes / unknown → back to meditating
// Plus: Blink, Float, Sound, Victory

class FootballOracle {
    constructor() {
        this.face = document.getElementById('genie-face');
        if (!this.face) {
            console.warn("❌ Genie face not found.");
            return;
        }

        this.questionNumber = parseInt(this.face.dataset.questionNumber) || 1;
        this.poseMap = {
            'meditating': 'genie_meditating.png',
            'yes': 'genie_yes.png',
            'no': 'genie_no.png',
            'sometimes': 'genie_sometimes.png',
            'unknown': 'genie_unknown.png',
            'victory': 'genie_victory.png'
        };

        this.init();
    }

    init() {
        // Start in meditating pose
        this.setPose('meditating');

        // Start animations
        this.startBlinking();
        this.startFloating();

        // Handle answer buttons
        this.bindAnswerButtons();

        // Click to react
        this.face.addEventListener('click', () => this.setPose('meditating'));
    }

    setPose(poseName) {
        const filename = this.poseMap[poseName];
        if (!filename) return;

        const url = `/static/genie/${filename}`;
        this.face.src = url;

        // Handle victory separately (no reset)
        if (poseName === 'victory') {
            this.playSound('fanfare');
        } else {
            // Reset to meditating after 1.5s
            if (poseName !== 'meditating') {
                setTimeout(() => this.setPose('meditating'), 1500);
            }
        }
    }

    bindAnswerButtons() {
        const buttons = document.querySelectorAll('.answer-buttons button');
        buttons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const answer = e.target.value;
                this.playSound('chime');
                if (answer === 'yes') this.setPose('yes');
                else if (answer === 'no') this.setPose('no');
                else if (answer === 'sometimes') this.setPose('sometimes');
                else if (answer === "i don't know") this.setPose('unknown');
            });
        });
    }

    startBlinking() {
        setInterval(() => {
            this.face.style.opacity = '0.8';
            setTimeout(() => {
                this.face.style.opacity = '1';
            }, 150);
        }, Math.random() * 5000 + 3000);
    }

    startFloating() {
        setInterval(() => {
            const y = Math.sin(Date.now() / 600) * 5;
            this.face.style.transform = `translateY(${y}px)`;
        }, 50);
    }

    playSound(type) {
        let audio = document.getElementById('genie-audio');
        if (!audio) {
            audio = document.createElement('audio');
            audio.id = 'genie-audio';
            audio.style.display = 'none';
            document.body.appendChild(audio);
        }

        if (type === 'chime') {
            audio.src = 'data:audio/mpeg;base64,SUQzBAAAAAABEVRYWFgAAAAtAAADY29tbWVudABCaWdTb3VuZEJhbmsuY29tIC8gTGFTb25vdGhlcXVlLm9yZwBURU5DAAAAHQAAA1N3aXRjaCBQbHVzIMKpIE5DSCBTb2Z0d2FyZQBUSVQyAAAABgAAAzIyMzUAVFNTRQAAAA8AAANMYXZmNTcuODMuMTAwAAAAAAAAAAAAAAD/80DEAAAAA0gAAAAATEFNRTMuMTAwVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQsRbAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQMSkAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV';
        } else if (type === 'fanfare') {
            audio.src = 'data:audio/mpeg;base64,SUQzBAAAAAABEVRYWFgAAAAtAAADY29tbWVudABCaWdTb3VuZEJhbmsuY29tIC8gTGFTb25vdGhlcXVlLm9yZwBURU5DAAAAHQAAA1N3aXRjaCBQbHVzIMKpIE5DSCBTb2Z0d2FyZQBUSVQyAAAABgAAAzIyMzUAVFNTRQAAAA8AAANMYXZmNTcuODMuMTAwAAAAAAAAAAAAAAD/80DEAAAAA0gAAAAATEFNRTMuMTAwVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQsRbAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQMSkAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV';
        }

        audio.play().catch(e => console.warn("🔇 Sound blocked:", e));
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.footballOracle = new FootballOracle();
});

// Victory function for answer.html
window.celebrateVictory = () => {
    if (window.footballOracle) {
        window.footballOracle.setPose('victory');
    }
};