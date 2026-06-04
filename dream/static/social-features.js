class SocialShare {
    constructor() {
        this.baseUrl = window.location.origin;
        this.init();
    }
    
    init() {
        this.createShareButtons();
        this.setupEventListeners();
    }
    
    createShareButtons() {
        // Add share buttons to success page
        const successElements = document.querySelectorAll('.show-success');
        successElements.forEach(element => {
            this.addShareButtonsToElement(element);
        });
    }
    
    addShareButtonsToElement(element) {
        const shareContainer = document.createElement('div');
        shareContainer.className = 'share-container';
        shareContainer.innerHTML = `
            <div class="share-buttons">
                <h4>🎉 Share Your Victory!</h4>
                <button class="share-btn twitter" data-platform="twitter">
                    🐦 Twitter
                </button>
                <button class="share-btn facebook" data-platform="facebook">
                    📘 Facebook
                </button>
                <button class="share-btn whatsapp" data-platform="whatsapp">
                    💬 WhatsApp
                </button>
                <button class="share-btn copy" data-platform="copy">
                    📋 Copy Link
                </button>
            </div>
        `;
        
        element.appendChild(shareContainer);
    }
    
    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('.share-btn')) {
                const platform = e.target.dataset.platform;
                this.share(platform);
            }
        });
    }
    
    share(platform) {
        const gameData = this.getGameData();
        const message = this.generateMessage(gameData);
        const url = `${this.baseUrl}`;
        
        switch (platform) {
            case 'twitter':
                this.shareToTwitter(message, url);
                break;
            case 'facebook':
                this.shareToFacebook(url);
                break;
            case 'whatsapp':
                this.shareToWhatsApp(message, url);
                break;
            case 'copy':
                this.copyToClipboard(message + ' ' + url);
                break;
        }
    }
    
    getGameData() {
        // Extract game data from page
        const playerName = document.querySelector('.player-name')?.textContent || 'Unknown Player';
        const questionsCount = document.querySelector('.questions-count')?.textContent || '?';
        const streak = document.querySelector('#streak')?.textContent || '0';
        
        return {
            playerName,
            questionsCount,
            streak
        };
    }
    
    generateMessage(data) {
        const messages = [
            `🧠 I just beat Muhfal! Guessed ${data.playerName} in ${data.questionsCount} questions! Current streak: ${data.streak} 🔥`,
            `⚽ Muhfal couldn't stump me! ${data.playerName} was too easy 😎 Streak: ${data.streak}`,
            `🎯 Another victory! Guessed ${data.playerName} in just ${data.questionsCount} questions on Muhfal!`
        ];
        
        return messages[Math.floor(Math.random() * messages.length)];
    }
    
    shareToTwitter(message, url) {
        const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(message)}&url=${encodeURIComponent(url)}`;
        window.open(twitterUrl, '_blank', 'width=600,height=400');
    }
    
    shareToFacebook(url) {
        const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
        window.open(facebookUrl, '_blank', 'width=600,height=400');
    }
    
    shareToWhatsApp(message, url) {
        const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(message + ' ' + url)}`;
        window.open(whatsappUrl, '_blank');
    }
    
    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showNotification('✅ Copied to clipboard!');
        }).catch(() => {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showNotification('✅ Copied to clipboard!');
        });
    }
    
    showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 1000;
            animation: slideIn 0.3s ease-out;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in forwards';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Multiplayer Challenge System
class MultiplayerChallenge {
    constructor() {
        this.challengeId = null;
        this.init();
    }
    
    init() {
        this.createChallengeButton();
    }
    
    createChallengeButton() {
        const challengeButton = document.createElement('button');
        challengeButton.className = 'btn btn-challenge';
        challengeButton.innerHTML = '⚔️ Challenge Friends';
        challengeButton.onclick = () => this.createChallenge();
        
        // Add to success pages
        document.querySelectorAll('.show-success').forEach(element => {
            element.appendChild(challengeButton);
        });
    }
    
    createChallenge() {
        const gameData = this.getGameData();
        this.challengeId = this.generateChallengeId();
        
        const challengeUrl = `${window.location.origin}/challenge/${this.challengeId}`;
        const message = `🏆 I just beat Muhfal in ${gameData.questionsCount} questions! Can you do better? ${challengeUrl}`;
        
        // Auto-copy challenge link
        navigator.clipboard.writeText(message).then(() => {
            this.showChallengeModal(challengeUrl, message);
        });
    }
    
    generateChallengeId() {
        return Math.random().toString(36).substr(2, 9);
    }
    
    getGameData() {
        return {
            questionsCount: document.querySelector('.questions-count')?.textContent || '?',
            playerName: document.querySelector('.player-name')?.textContent || 'Unknown',
            timestamp: Date.now()
        };
    }
    
    showChallengeModal(url, message) {
        const modal = document.createElement('div');
        modal.className = 'challenge-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>🏆 Challenge Created!</h3>
                <p>Share this link with your friends:</p>
                <div class="challenge-link">
                    <input type="text" value="${url}" readonly>
                    <button onclick="navigator.clipboard.writeText('${message}')">📋 Copy</button>
                </div>
                <div class="modal-buttons">
                    <button onclick="this.parentElement.parentElement.parentElement.remove()">Close</button>
                </div>
            </div>
        `;
        
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        `;
        
        document.body.appendChild(modal);
    }
}

// Initialize social features
document.addEventListener('DOMContentLoaded', () => {
    window.socialShare = new SocialShare();
    window.multiplayerChallenge = new MultiplayerChallenge();
});

// Add CSS for social buttons
const socialCSS = `
.share-container {
    margin: 20px 0;
    text-align: center;
}

.share-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-top: 15px;
}

.share-btn {
    padding: 10px 15px;
    border: none;
    border-radius: 25px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 100px;
}

.share-btn.twitter { background: #1DA1F2; color: white; }
.share-btn.facebook { background: #4267B2; color: white; }
.share-btn.whatsapp { background: #25D366; color: white; }
.share-btn.copy { background: #6c757d; color: white; }

.share-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.notification {
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
}

.btn-challenge {
    background: linear-gradient(135deg, #ff6b6b, #ee5a24);
    color: white;
    margin: 10px;
}

.challenge-modal .modal-content {
    background: white;
    padding: 30px;
    border-radius: 15px;
    max-width: 400px;
    width: 90%;
}

.challenge-link {
    display: flex;
    gap: 10px;
    margin: 15px 0;
}

.challenge-link input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

@media (max-width: 600px) {
    .share-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .share-btn {
        width: 200px;
    }
}
`;

// Inject CSS
const styleSheet = document.createElement('style');
styleSheet.textContent = socialCSS;
document.head.appendChild(styleSheet);