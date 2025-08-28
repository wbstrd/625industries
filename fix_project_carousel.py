#!/usr/bin/env python3

def fix_project_carousel():
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Enhanced carousel CSS for bigger photos and smooth scroll
    enhanced_carousel_css = """
        /* Enhanced Project Modal Carousel */
        #modal-carousel {
            width: 100%;
            height: 600px;
            overflow-x: auto;
            overflow-y: hidden;
            display: flex;
            scroll-behavior: smooth;
            scrollbar-width: none;
            -ms-overflow-style: none;
            position: relative;
            border-radius: 12px;
            background: #111;
        }
        
        #modal-carousel::-webkit-scrollbar {
            display: none;
        }
        
        .carousel-item {
            min-width: 90%;
            height: 100%;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            margin-right: 20px;
        }
        
        .carousel-item img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            transition: transform 0.3s ease;
        }
        
        .carousel-item img:hover {
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
            font-size: 28px;
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
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.4);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .carousel-indicator.active {
            background: rgba(255, 255, 255, 0.9);
            transform: scale(1.3);
        }"""
    
    # Replace existing modal-carousel styles or add them
    if '#modal-carousel {' in content:
        import re
        pattern = r'#modal-carousel\s*\{[^}]*\}'
        content = re.sub(pattern, enhanced_carousel_css.split('#modal-carousel {')[1].split('}')[0], content)
    else:
        content = content.replace('</style>', enhanced_carousel_css + '\n        </style>')
    
    # Enhanced JavaScript for project clicks and infinite carousel
    enhanced_js = """
        // Enhanced project modal functionality
        function populateProjectList() {
            const projectsContainer = document.getElementById('projects-container');
            if (!projectsContainer) return;
            
            projectsContainer.innerHTML = '';
            
            // Group projects by year
            const projectsByYear = {};
            Object.values(imageToProjectMap).forEach(project => {
                const year = project.date ? project.date.split(' ').pop() : 'Unknown';
                if (!projectsByYear[year]) {
                    projectsByYear[year] = [];
                }
                projectsByYear[year].push(project);
            });
            
            // Sort years in descending order
            const sortedYears = Object.keys(projectsByYear).sort((a, b) => {
                if (a === 'Unknown') return 1;
                if (b === 'Unknown') return -1;
                return parseInt(b) - parseInt(a);
            });
            
            sortedYears.forEach(year => {
                const yearSection = document.createElement('div');
                yearSection.className = 'year-section';
                
                const yearTitle = document.createElement('div');
                yearTitle.className = 'year-title';
                yearTitle.textContent = year;
                yearSection.appendChild(yearTitle);
                
                projectsByYear[year].forEach(project => {
                    const projectItem = document.createElement('div');
                    projectItem.className = 'project-item';
                    projectItem.textContent = `${project.title} - ${project.location}`;
                    
                    // Add click handler to open modal
                    projectItem.addEventListener('click', () => {
                        openProjectModal(project);
                    });
                    
                    yearSection.appendChild(projectItem);
                });
                
                projectsContainer.appendChild(yearSection);
            });
        }
        
        function openProjectModal(project) {
            const modal = document.getElementById('project-modal');
            const modalTitle = document.getElementById('modal-title');
            const modalDate = document.getElementById('modal-date');
            const carousel = document.getElementById('modal-carousel');
            
            if (!modal || !carousel) return;
            
            // Set project info
            modalTitle.textContent = project.title;
            modalDate.textContent = `${project.date} - ${project.location}`;
            
            // Get project images
            const projectImages = [];
            if (project.images && project.images.length > 0) {
                project.images.forEach(imageNum => {
                    projectImages.push(`${BASE_PATH}high_res_1200/img${String(imageNum).padStart(3, '0')}-high.jpg`);
                });
            }
            
            createInfiniteCarousel(carousel, projectImages);
            modal.style.display = 'block';
            
            // Prevent body scroll
            document.body.style.overflow = 'hidden';
        }
        
        function createInfiniteCarousel(container, images) {
            if (!container || !images || images.length === 0) return;
            
            container.innerHTML = '';
            container.style.position = 'relative';
            
            // Create infinite scroll by tripling the images
            const infiniteImages = [...images, ...images, ...images];
            
            infiniteImages.forEach((imgSrc, index) => {
                const item = document.createElement('div');
                item.className = 'carousel-item';
                
                const img = document.createElement('img');
                img.src = imgSrc;
                img.alt = `Project image ${(index % images.length) + 1}`;
                img.loading = 'lazy';
                
                item.appendChild(img);
                container.appendChild(item);
            });
            
            // Only add controls if more than one image
            if (images.length > 1) {
                // Add navigation buttons
                const prevBtn = document.createElement('button');
                prevBtn.className = 'carousel-nav carousel-prev';
                prevBtn.innerHTML = '&#8249;';
                
                const nextBtn = document.createElement('button');
                nextBtn.className = 'carousel-nav carousel-next';
                nextBtn.innerHTML = '&#8250;';
                
                container.appendChild(prevBtn);
                container.appendChild(nextBtn);
                
                // Add indicators
                const indicators = document.createElement('div');
                indicators.className = 'carousel-indicators';
                images.forEach((_, index) => {
                    const indicator = document.createElement('div');
                    indicator.className = `carousel-indicator ${index === 0 ? 'active' : ''}`;
                    indicators.appendChild(indicator);
                });
                container.appendChild(indicators);
                
                // Carousel state
                let currentIndex = 0;
                const itemWidth = container.querySelector('.carousel-item').offsetWidth + 20; // including margin
                
                // Start at the middle set for infinite scroll
                container.scrollLeft = itemWidth * images.length;
                
                function updateCarousel(animate = true) {
                    const targetScroll = (currentIndex + images.length) * itemWidth;
                    
                    if (animate) {
                        container.scrollTo({
                            left: targetScroll,
                            behavior: 'smooth'
                        });
                    } else {
                        container.scrollLeft = targetScroll;
                    }
                    
                    // Update indicators
                    indicators.querySelectorAll('.carousel-indicator').forEach((indicator, index) => {
                        indicator.classList.toggle('active', index === currentIndex);
                    });
                }
                
                function nextSlide() {
                    currentIndex = (currentIndex + 1) % images.length;
                    updateCarousel();
                    
                    // Handle infinite scroll wrap
                    setTimeout(() => {
                        if (container.scrollLeft >= itemWidth * (images.length * 2)) {
                            container.scrollLeft = itemWidth * images.length;
                        }
                    }, 500);
                }
                
                function prevSlide() {
                    currentIndex = (currentIndex - 1 + images.length) % images.length;
                    updateCarousel();
                    
                    // Handle infinite scroll wrap
                    setTimeout(() => {
                        if (container.scrollLeft <= 0) {
                            container.scrollLeft = itemWidth * images.length;
                        }
                    }, 500);
                }
                
                // Event listeners
                nextBtn.addEventListener('click', nextSlide);
                prevBtn.addEventListener('click', prevSlide);
                
                // Indicator clicks
                indicators.querySelectorAll('.carousel-indicator').forEach((indicator, index) => {
                    indicator.addEventListener('click', () => {
                        currentIndex = index;
                        updateCarousel();
                    });
                });
                
                // Auto-play
                let autoPlay = setInterval(nextSlide, 4000);
                
                container.addEventListener('mouseenter', () => clearInterval(autoPlay));
                container.addEventListener('mouseleave', () => {
                    autoPlay = setInterval(nextSlide, 4000);
                });
                
                // Mouse wheel support
                container.addEventListener('wheel', (e) => {
                    e.preventDefault();
                    if (e.deltaY > 0) {
                        nextSlide();
                    } else {
                        prevSlide();
                    }
                });
                
                // Touch support
                let startX = 0;
                container.addEventListener('touchstart', (e) => {
                    startX = e.touches[0].clientX;
                    clearInterval(autoPlay);
                });
                
                container.addEventListener('touchend', (e) => {
                    const endX = e.changedTouches[0].clientX;
                    const diff = startX - endX;
                    
                    if (Math.abs(diff) > 50) {
                        if (diff > 0) {
                            nextSlide();
                        } else {
                            prevSlide();
                        }
                    }
                    
                    autoPlay = setInterval(nextSlide, 4000);
                });
            }
        }
        
        // Close modal function
        function closeProjectModal() {
            const modal = document.getElementById('project-modal');
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        }"""
    
    # Add the enhanced JavaScript before the Initialize comment
    content = content.replace('        // Initialize', enhanced_js + '\n\n        // Initialize')
    
    # Make sure close button works
    close_button_js = """
        // Modal close functionality
        document.addEventListener('DOMContentLoaded', function() {
            const closeButton = document.querySelector('.close-button');
            if (closeButton) {
                closeButton.addEventListener('click', closeProjectModal);
            }
            
            // Close on background click
            const modal = document.getElementById('project-modal');
            if (modal) {
                modal.addEventListener('click', function(e) {
                    if (e.target === modal) {
                        closeProjectModal();
                    }
                });
            }
            
            // Close on Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeProjectModal();
                }
            });
        });"""
    
    content = content.replace('        // Initialize', close_button_js + '\n\n        // Initialize')
    
    # Write the updated content
    with open('index_with_carousel_enhanced.html', 'w') as f:
        f.write(content)
    
    print("Enhanced carousel with project clicks created as index_with_carousel_enhanced.html!")

if __name__ == "__main__":
    fix_project_carousel()
