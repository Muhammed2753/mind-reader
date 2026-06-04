class GenieAnimator {
    constructor() {
        this.genie = document.getElementById('genie-face');
        this.currentState = 'idle';
        this.animationQueue = [];
        this.isAnimating = false;
        
        // Performance optimization
        this.rafId = null;
        this.lastFrameTime = 0;
        
        this.init();
    }
    
    init() {
        if (!this.genie) return;
        
        // Add click interaction
        this.genie.addEventListener('click', () => this.playRandomAnimation());
        
        // Auto-animate based on question number
        this.autoAnimate();
        
        // Optimize animations for performance
        this.optimizePerformance();
    }
    
    setState(state, duration = 2000) {
        if (this.isAnimating) {
            this.animationQueue.push({ state, duration });
            return;
        }
        
        this.isAnimating = true;
        this.currentState = state;
        
        // Remove all animation classes
        this.genie.classList.remove('genie-thinking', 'genie-excited', 'genie-confused');
        
        // Add new state class
        if (state !== 'idle') {
            this.genie.classList.add(`genie-${state}`);
        }
        
        // Auto-return to idle
        setTimeout(() => {
            this.genie.classList.remove(`genie-${state}`);
            this.isAnimating = false;
            this.processQueue();
        }, duration);
    }
    
    processQueue() {
        if (this.animationQueue.length > 0) {
            const next = this.animationQueue.shift();
            this.setState(next.state, next.duration);
        }
    }
    
    playRandomAnimation() {
        const animations = ['thinking', 'excited', 'confused'];
        const randomAnim = animations[Math.floor(Math.random() * animations.length)];
        this.setState(randomAnim, 1500);
    }
    
    autoAnimate() {
        // Animate based on question progress
        const questionNumber = parseInt(document.querySelector('[data-question-number]')?.dataset.questionNumber || 0);
        
        if (questionNumber > 0) {
            setTimeout(() => {
                if (questionNumber <= 3) {
                    this.setState('thinking', 3000);
                } else if (questionNumber <= 8) {
                    this.setState('excited', 2000);
                } else {
                    this.setState('confused', 2500);
                }
            }, 500);
        }
    }
    
    optimizePerformance() {
        // Use Intersection Observer to pause animations when not visible
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.genie.style.animationPlayState = 'running';
                    } else {
                        this.genie.style.animationPlayState = 'paused';
                    }
                });
            });
            
            observer.observe(this.genie);
        }
        
        // Reduce animations on low-end devices
        if (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
            document.body.classList.add('low-performance');
        }
    }
    
    celebrate() {
        // Create celebration particles
        this.createParticles();
        this.setState('excited', 3000);
    }
    
    createParticles() {
        const celebration = document.createElement('div');
        celebration.className = 'celebration';
        document.body.appendChild(celebration);
        
        // Create 20 particles
        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 0.5 + 's';
                celebration.appendChild(particle);
            }, i * 50);
        }
        
        // Clean up after animation
        setTimeout(() => {
            document.body.removeChild(celebration);
        }, 3000);
    }
}

// Performance Monitor
class PerformanceMonitor {
    constructor() {
        this.fps = 0;
        this.lastTime = performance.now();
        this.frameCount = 0;
        this.isMonitoring = false;
        
        this.startMonitoring();
    }
    
    startMonitoring() {
        if (this.isMonitoring) return;
        this.isMonitoring = true;
        this.measureFPS();
    }
    
    measureFPS() {
        const now = performance.now();
        this.frameCount++;
        
        if (now - this.lastTime >= 1000) {
            this.fps = Math.round((this.frameCount * 1000) / (now - this.lastTime));
            this.frameCount = 0;
            this.lastTime = now;
            
            // Adjust quality based on FPS
            this.adjustQuality();
        }
        
        if (this.isMonitoring) {
            requestAnimationFrame(() => this.measureFPS());
        }
    }
    
    adjustQuality() {
        const body = document.body;
        
        if (this.fps < 30) {
            body.classList.add('low-performance');
            // Disable complex animations
            document.querySelectorAll('.football').forEach(el => el.style.display = 'none');
        } else if (this.fps > 50) {
            body.classList.remove('low-performance');
        }
    }
}

// Smooth Loading System
class LoadingManager {
    constructor() {
        this.loadingElements = new Set();
        this.init();
    }
    
    init() {
        // Add loading states to buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('button[type="submit"], .btn')) {
                this.showLoading(e.target);
            }
        });
    }
    
    showLoading(element) {
        element.classList.add('loading');
        element.disabled = true;
        this.loadingElements.add(element);
        
        // Auto-remove after 5 seconds (fallback)
        setTimeout(() => {
            this.hideLoading(element);
        }, 5000);
    }
    
    hideLoading(element) {
        element.classList.remove('loading');
        element.disabled = false;
        this.loadingElements.delete(element);
    }
    
    hideAllLoading() {
        this.loadingElements.forEach(element => {
            this.hideLoading(element);
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize systems
    window.genieAnimator = new GenieAnimator();
    window.performanceMonitor = new PerformanceMonitor();
    window.loadingManager = new LoadingManager();
    
    // Hide loading on page load
    setTimeout(() => {
        window.loadingManager.hideAllLoading();
    }, 100);
    
    // Add smooth transitions to all interactive elements
    document.querySelectorAll('button, .btn, .quick-link').forEach(el => {
        el.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    });
});

// Export for global access
window.GenieAnimator = GenieAnimator;
window.PerformanceMonitor = PerformanceMonitor;
window.LoadingManager = LoadingManager;