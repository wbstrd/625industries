#!/usr/bin/env python3

def enhance_carousel():
    with open('index.html', 'r') as f:
        content = f.read()
    
    # Enhanced carousel CSS - add before </style>
    enhanced_carousel_css = """
        /* Enhanced Carousel Styles */
        .carousel-container {
            position: relative;
            width: 100%;
            height: 600px;
            overflow: hidden;
            border-radius: 12px;
            background: #111;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }
        
        .carousel-track {
            display: flex;
            height: 100%;
            transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            will-change: transform;
        }
        
        .carousel-slide {
            min-width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .carousel-slide img {
            max-width: 95%;
            max-height: 95%;
            object-fit: contain;
            border-radius: 8px;
            transition: transform 0.4s ease;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        
        .carousel-slide img:hover {
            transform: scale(1.02);
        }
        
        .carousel-nav {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0, 0, 0, 0.7);
            color: white;
            border: none;
            padding: 20px 25px;
            cursor: pointer;
            font-size: 24px;
            border-radius: 8px;
            transition: all 0.3s ease;
            z-index: 10;
            backdrop-filter: blur(10px);
        }
        
        .carousel-nav:hover {
            background: rgba(0, 0, 0, 0.9);
            transform: translateY(-50%) scale(1.1);
        }
        
        .carousel-prev {
            left: 30px;
        }
        
        .carousel-next {
            right: 30px;
        }
        
        .carousel-indicators {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 12px;
            z-index: 10;
        }
        
        .carousel-indicator {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.4);
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .carousel-indicator:hover {
            background: rgba(255, 255, 255, 0.6);
            transform: scale(1.2);
        }
        
        .carousel-indicator.active {
            background: rgba(255, 255, 255, 0.9);
            border-color: rgba(255, 255, 255, 0.5);
            transform: scale(1.3);
        }
        
        .carousel-progress {
            position: absolute;
            bottom: 0;
            left: 0;
            height: 4px;
            background: rgba(255, 255, 255, 0.8);
            transition: width 0.3s ease;
            z-index: 10;
        }"""
    
    # Add enhanced styles before </style>
    if '.carousel-container {' not in content:
        content = content.replace('</style>', enhanced_carousel_css + '\n        </style>')
    else:
        # Replace existing carousel styles
        import re
        pattern = r'\.carousel-container\s*\{[^}]*\}.*?\.carousel-indicator\.active\s*\{[^}]*\}'
        content = re.sub(pattern, enhanced_carousel_css.strip(), content, flags=re.DOTALL)
    
    # Enhanced carousel JavaScript - find and replace the existing createCarousel function
    enhanced_js = """
            function createCarousel(images, modalElement) {
                const container = modalElement.querySelector('.carousel-container');
                if (!container) return;
                
                container.innerHTML = '';
                
                if (images.length === 0) {
                    container.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #666; font-size: 18px;">No images available</div>';
                    return;
                }
                
                // Create carousel structure
                const track = document.createElement('div');
                track.className = 'carousel-track';
                
                // Create slides with infinite scroll (duplicate first and last)
                const allImages = images.length > 1 ? [images[images.length - 1], ...images, images[0]] : images;
                allImages.forEach((imgSrc, index) => {
                    const slide = document.createElement('div');
                    slide.className = 'carousel-slide';
                    
                    const img = document.createElement('img');
                    img.src = imgSrc;
                    img.alt = `Project image ${index}`;
                    img.loading = 'lazy';
                    
                    slide.appendChild(img);
                    track.appendChild(slide);
                });
                
                container.appendChild(track);
                
                // Create progress bar
                const progressBar = document.createElement('div');
                progressBar.className = 'carousel-progress';
                container.appendChild(progressBar);
                
                // Only add navigation and indicators if more than one image
                if (images.length > 1) {
                    // Create navigation buttons
                    const prevBtn = document.createElement('button');
                    prevBtn.className = 'carousel-nav carousel-prev';
                    prevBtn.innerHTML = '&#8249;';
                    prevBtn.setAttribute('aria-label', 'Previous image');
                    
                    const nextBtn = document.createElement('button');
                    nextBtn.className = 'carousel-nav carousel-next';
                    nextBtn.innerHTML = '&#8250;';
                    nextBtn.setAttribute('aria-label', 'Next image');
                    
                    container.appendChild(prevBtn);
                    container.appendChild(nextBtn);
                    
                    // Create indicators
                    const indicators = document.createElement('div');
                    indicators.className = 'carousel-indicators';
                    images.forEach((_, index) => {
                        const indicator = document.createElement('div');
                        indicator.className = `carousel-indicator ${index === 0 ? 'active' : ''}`;
                        indicator.addEventListener('click', () => goToSlide(index));
                        indicators.appendChild(indicator);
                    });
                    container.appendChild(indicators);
                    
                    // Carousel state
                    let currentSlide = images.length > 1 ? 1 : 0; // Start at 1 for infinite scroll
                    let isTransitioning = false;
                    let autoPlayInterval;
                    let autoPlayProgress = 0;
                    const autoPlayDuration = 5000;
                    
                    function updateSlidePosition(animate = true) {
                        if (animate) {
                            track.style.transition = 'transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
                        } else {
                            track.style.transition = 'none';
                        }
                        track.style.transform = `translateX(-${currentSlide * 100}%)`;
                        
                        // Update indicators
                        const realIndex = images.length > 1 ? 
                            (currentSlide === 0 ? images.length - 1 : 
                             currentSlide === allImages.length - 1 ? 0 : currentSlide - 1) : 0;
                        indicators.querySelectorAll('.carousel-indicator').forEach((indicator, index) => {
                            indicator.classList.toggle('active', index === realIndex);
                        });
                    }
                    
                    function updateProgress() {
                        const progress = (autoPlayProgress / autoPlayDuration) * 100;
                        progressBar.style.width = `${progress}%`;
                    }
                    
                    function goToSlide(index) {
                        if (isTransitioning) return;
                        currentSlide = images.length > 1 ? index + 1 : index;
                        updateSlidePosition();
                        resetAutoPlay();
                    }
                    
                    function nextSlide() {
                        if (isTransitioning) return;
                        isTransitioning = true;
                        currentSlide++;
                        updateSlidePosition();
                        
                        setTimeout(() => {
                            if (images.length > 1 && currentSlide >= allImages.length - 1) {
                                currentSlide = 1;
                                updateSlidePosition(false);
                            }
                            isTransitioning = false;
                        }, 600);
                    }
                    
                    function prevSlide() {
                        if (isTransitioning) return;
                        isTransitioning = true;
                        currentSlide--;
                        updateSlidePosition();
                        
                        setTimeout(() => {
                            if (images.length > 1 && currentSlide <= 0) {
                                currentSlide = images.length;
                                updateSlidePosition(false);
                            }
                            isTransitioning = false;
                        }, 600);
                    }
                    
                    function startAutoPlay() {
                        autoPlayProgress = 0;
                        const progressInterval = setInterval(() => {
                            autoPlayProgress += 50;
                            updateProgress();
                            
                            if (autoPlayProgress >= autoPlayDuration) {
                                clearInterval(progressInterval);
                                nextSlide();
                                if (autoPlayInterval) startAutoPlay();
                            }
                        }, 50);
                        
                        autoPlayInterval = progressInterval;
                    }
                    
                    function stopAutoPlay() {
                        clearInterval(autoPlayInterval);
                        autoPlayInterval = null;
                        progressBar.style.width = '0%';
                    }
                    
                    function resetAutoPlay() {
                        stopAutoPlay();
                        startAutoPlay();
                    }
                    
                    // Event listeners
                    nextBtn.addEventListener('click', () => {
                        nextSlide();
                        resetAutoPlay();
                    });
                    
                    prevBtn.addEventListener('click', () => {
                        prevSlide();
                        resetAutoPlay();
                    });
                    
                    // Auto-play with pause on hover
                    container.addEventListener('mouseenter', stopAutoPlay);
                    container.addEventListener('mouseleave', startAutoPlay);
                    
                    // Mouse wheel support
                    container.addEventListener('wheel', (e) => {
                        e.preventDefault();
                        if (e.deltaY > 0) {
                            nextSlide();
                        } else {
                            prevSlide();
                        }
                        resetAutoPlay();
                    });
                    
                    // Touch/swipe support
                    let startX = 0;
                    let startY = 0;
                    let isDragging = false;
                    
                    container.addEventListener('touchstart', (e) => {
                        startX = e.touches[0].clientX;
                        startY = e.touches[0].clientY;
                        isDragging = true;
                        stopAutoPlay();
                    });
                    
                    container.addEventListener('touchmove', (e) => {
                        if (!isDragging) return;
                        e.preventDefault();
                    });
                    
                    container.addEventListener('touchend', (e) => {
                        if (!isDragging) return;
                        isDragging = false;
                        
                        const endX = e.changedTouches[0].clientX;
                        const endY = e.changedTouches[0].clientY;
                        const diffX = startX - endX;
                        const diffY = startY - endY;
                        
                        if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                            if (diffX > 0) {
                                nextSlide();
                            } else {
                                prevSlide();
                            }
                        }
                        
                        resetAutoPlay();
                        startX = 0;
                        startY = 0;
                    });
                    
                    // Keyboard support
                    document.addEventListener('keydown', (e) => {
                        if (modalElement.style.display === 'block') {
                            if (e.key === 'ArrowLeft') {
                                prevSlide();
                                resetAutoPlay();
                            } else if (e.key === 'ArrowRight') {
                                nextSlide();
                                resetAutoPlay();
                            }
                        }
                    });
                    
                    // Initialize
                    updateSlidePosition(false);
                    startAutoPlay();
                } else {
                    // Single image - just center it
                    updateSlidePosition(false);
                }
            }"""
    
    # Replace the existing createCarousel function
    import re
    pattern = r'function createCarousel\(images, modalElement\)\s*\{.*?\n\s*\}'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, enhanced_js.strip(), content, flags=re.DOTALL)
    else:
        print("Warning: Could not find createCarousel function to replace")
        # Add before the last closing script tag if function doesn't exist
        content = content.replace('        // Initialize', enhanced_js + '\n\n        // Initialize')
    
    # Write the updated content
    with open('index.html', 'w') as f:
        f.write(content)
    
    print("Enhanced carousel functionality added successfully!")

if __name__ == "__main__":
    enhance_carousel()
