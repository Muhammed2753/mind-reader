// Performance Optimization Script
(function() {
    'use strict';
    
    // Debounce function to limit rapid function calls
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Optimize animations for low-end devices
    function optimizeForDevice() {
        const isLowEnd = navigator.hardwareConcurrency < 4 || 
                        navigator.deviceMemory < 4 ||
                        /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        
        if (isLowEnd) {
            document.body.classList.add('low-performance');
            // Disable complex animations
            document.querySelectorAll('.football').forEach(el => el.remove());
            // Reduce transition durations
            const style = document.createElement('style');
            style.textContent = `
                * { transition-duration: 0.1s !important; }
                .card { animation: none !important; }
            `;
            document.head.appendChild(style);
        }
    }
    
    // Lazy load images
    function lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Optimize button clicks
    function optimizeButtons() {
        const buttons = document.querySelectorAll('button, .btn');
        buttons.forEach(button => {
            button.addEventListener('click', debounce((e) => {
                // Add loading state
                button.style.opacity = '0.7';
                button.disabled = true;
                
                // Re-enable after delay
                setTimeout(() => {
                    button.style.opacity = '1';
                    button.disabled = false;
                }, 1000);
            }, 300));
        });
    }
    
    // Memory cleanup
    function cleanupMemory() {
        // Remove unused event listeners
        const oldElements = document.querySelectorAll('[data-cleanup]');
        oldElements.forEach(el => {
            el.removeEventListener('click', el._clickHandler);
            el.remove();
        });
        
        // Force garbage collection if available
        if (window.gc) {
            window.gc();
        }
    }
    
    // Initialize optimizations
    document.addEventListener('DOMContentLoaded', () => {
        optimizeForDevice();
        lazyLoadImages();
        optimizeButtons();
        
        // Cleanup every 30 seconds
        setInterval(cleanupMemory, 30000);
        
        // Reduce animation frame rate on mobile
        if (window.innerWidth < 768) {
            const style = document.createElement('style');
            style.textContent = `
                * { 
                    animation-duration: 0.2s !important;
                    transition-duration: 0.2s !important;
                }
            `;
            document.head.appendChild(style);
        }
    });
    
    // Handle page visibility changes
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            // Pause animations when tab is not visible
            document.querySelectorAll('*').forEach(el => {
                if (el.style.animationPlayState !== undefined) {
                    el.style.animationPlayState = 'paused';
                }
            });
        } else {
            // Resume animations
            document.querySelectorAll('*').forEach(el => {
                if (el.style.animationPlayState !== undefined) {
                    el.style.animationPlayState = 'running';
                }
            });
        }
    });
    
})();