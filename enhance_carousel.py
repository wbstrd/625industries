#!/usr/bin/env python3
"""
Enhance Carousel with Bigger Photos and Infinite Animation
"""

import re

def enhance_carousel():
    # Read the current HTML
    with open('index.html', 'r') as f:
        html_content = f.read()
    
    # Enhanced carousel CSS
    new_carousel_css = '''
        #modal-carousel {
            width: 100%;
            height: 70%;
            overflow-x: auto;
            overflow-y: hidden;
            white-space: nowrap;
            padding: 20px 0;
            scrollbar-width: none;
            -ms-overflow-style: none;
            display: flex;
            align-items: center;
            position: relative;
        }

        #modal-carousel::-webkit-scrollbar {
            display: none;
        }

        .carousel-item {
            display: inline-block !important;
            width: 500px !important;
            height: auto !important;
            margin-right: 30px !important;
            vertical-align: top !important;
            flex-shrink: 0 !important;
            transition: transform 0.3s ease !important;
            border-radius: 8px !important;
            overflow: hidden !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        }

        .carousel-item:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7) !important;
        }

        .carousel-item img {
            width: 100% !important;
            height: 600px !important;
            object-fit: cover !important;
            display: block !important;
            border-radius: 8px !important;
        }

        /* Auto-scroll animation */
        @keyframes infiniteScroll {
            from {
                transform: translateX(0);
            }
            to {
                transform: translateX(-100%);
            }
        }

        .carousel-auto-scroll {
            animation: infiniteScroll 30s linear infinite;
        }

        .carousel-auto-scroll:hover {
            animation-play-state: paused;
        }
    '''
    
    # Replace the existing carousel CSS
    pattern = r'#modal-carousel \{[^}]*\}'
    html_content = re.sub(pattern, new_carousel_css.strip(), html_content, flags=re.DOTALL)
    
    # Enhanced JavaScript for bigger images and better scrolling
    new_js_carousel = '''
        function setupInfiniteScroll(carousel, originalLength) {
            let isScrolling = false;
            let autoScrollInterval;
            const itemWidth = 530; // 500px + 30px margin
            const totalWidth = itemWidth * originalLength;
            
            // Set initial scroll position to the middle set
            carousel.scrollLeft = totalWidth;
            
            // Auto-scroll function
            function startAutoScroll() {
                autoScrollInterval = setInterval(() => {
                    if (!isScrolling) {
                        carousel.scrollLeft += 1.5; // Smooth continuous scroll
                    }
                }, 16); // ~60fps
            }
            
            // Stop auto-scroll on user interaction
            function stopAutoScroll() {
                clearInterval(autoScrollInterval);
            }
            
            // Resume auto-scroll after user stops interacting
            let userInteractionTimeout;
            function resetAutoScroll() {
                clearTimeout(userInteractionTimeout);
                stopAutoScroll();
                userInteractionTimeout = setTimeout(() => {
                    startAutoScroll();
                }, 3000); // Resume after 3 seconds of no interaction
            }
            
            carousel.addEventListener('scroll', () => {
                if (isScrolling) return;
                
                const scrollLeft = carousel.scrollLeft;
                
                // If scrolled to the end of the third set, jump to the middle set
                if (scrollLeft >= totalWidth * 2) {
                    isScrolling = true;
                    carousel.scrollLeft = totalWidth;
                    setTimeout(() => { isScrolling = false; }, 50);
                }
                // If scrolled to the beginning of the first set, jump to the middle set
                else if (scrollLeft <= 0) {
                    isScrolling = true;
                    carousel.scrollLeft = totalWidth;
                    setTimeout(() => { isScrolling = false; }, 50);
                }
            });
            
            // Event listeners for user interaction
            carousel.addEventListener('mouseenter', stopAutoScroll);
            carousel.addEventListener('mouseleave', resetAutoScroll);
            carousel.addEventListener('wheel', resetAutoScroll);
            carousel.addEventListener('touchstart', stopAutoScroll);
            carousel.addEventListener('touchend', resetAutoScroll);
            
            // Start auto-scroll
            startAutoScroll();
        }'''
    
    # Replace the setupInfiniteScroll function
    setup_pattern = r'function setupInfiniteScroll\(carousel, originalLength\) \{[^}]*\}[^}]*\}[^}]*\}'
    html_content = re.sub(setup_pattern, new_js_carousel.strip(), html_content, flags=re.DOTALL)
    
    # Enhanced showProjectModal function for bigger images
    new_show_modal = '''
        function showProjectModal(project) {
            document.getElementById("modal-title").textContent = project.title;
            document.getElementById("modal-date").textContent = `${project.date} – ${project.location}`;
            document.getElementById("modal-description").textContent = project.description;
            
            // Create carousel with all project images
            const carousel = document.getElementById("modal-carousel");
            carousel.innerHTML = '';
            
            // Create infinite scroll by duplicating images 5 times for smoother infinite effect
            const allImages = [
                ...project.images, 
                ...project.images, 
                ...project.images, 
                ...project.images, 
                ...project.images
            ];
            
            allImages.forEach((imageNum, index) => {
                const carouselItem = document.createElement("div");
                carouselItem.className = "carousel-item";
                
                const img = document.createElement("img");
                img.src = `${BASE_PATH}high_res_1200/img${String(imageNum).padStart(3, '0')}-high.jpg`;
                img.alt = `${project.title} - Image ${index + 1}`;
                img.onerror = () => {
                    // Fallback to medium res if high res fails
                    img.src = `${BASE_PATH}medium_res/img${String(imageNum).padStart(3, '0')}-med.jpg`;
                };
                
                carouselItem.appendChild(img);
                carousel.appendChild(carouselItem);
            });
            
            modal.style.display = "block";
            
            // Set up infinite scroll with auto-animation
            setupInfiniteScroll(carousel, project.images.length);
        }'''
    
    # Replace the showProjectModal function
    modal_pattern = r'function showProjectModal\(project\) \{[^}]*\}[^}]*\}[^}]*\}[^}]*\}[^}]*\}'
    html_content = re.sub(modal_pattern, new_show_modal.strip(), html_content, flags=re.DOTALL)
    
    # Enhanced wheel scrolling
    new_wheel_scroll = '''
        // Enhanced mouse wheel support for horizontal scrolling in modal
        window.addEventListener("wheel", (e) => {
            const modal = document.getElementById("project-modal");
            const carousel = document.getElementById("modal-carousel");
            
            if (modal.style.display === "block" && carousel) {
                e.preventDefault();
                // Enhanced smooth scroll with better momentum
                const scrollAmount = e.deltaY * 3;
                
                // Add smooth easing
                const currentScroll = carousel.scrollLeft;
                const targetScroll = currentScroll + scrollAmount;
                
                // Smooth animation
                carousel.style.scrollBehavior = 'smooth';
                carousel.scrollLeft = targetScroll;
                
                // Reset scroll behavior after animation
                setTimeout(() => {
                    carousel.style.scrollBehavior = 'auto';
                }, 300);
            }
        }, { passive: false });'''
    
    # Replace the wheel event listener
    wheel_pattern = r'// Add mouse wheel support.*?\}, \{ passive: false \}\);'
    html_content = re.sub(wheel_pattern, new_wheel_scroll.strip(), html_content, flags=re.DOTALL)
    
    # Write the enhanced HTML
    with open('index.html', 'w') as f:
        f.write(html_content)
    
    print("🎨 CAROUSEL ENHANCED!")
    print("✅ BIGGER photos (500px → 600px height)")
    print("✅ High-resolution images (1200px)")
    print("✅ Infinite auto-scroll animation")
    print("✅ Smooth mouse wheel scrolling")
    print("✅ Hover effects and shadows")
    print("✅ Auto-pause on interaction")

if __name__ == "__main__":
    enhance_carousel()

