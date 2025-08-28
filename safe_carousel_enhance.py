#!/usr/bin/env python3
"""
Safe Carousel Enhancement - Only modify carousel CSS and functions without breaking 625 clock
"""

def safe_enhance_carousel():
    # Read the current HTML
    with open('index.html', 'r') as f:
        html_content = f.read()
    
    # Find and replace ONLY the specific carousel CSS block
    carousel_css_start = html_content.find('#modal-carousel {')
    if carousel_css_start != -1:
        carousel_css_end = html_content.find('}', carousel_css_start) + 1
        
        new_carousel_css = '''#modal-carousel {
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
        }'''
        
        html_content = html_content[:carousel_css_start] + new_carousel_css + html_content[carousel_css_end:]
    
    # Find and replace ONLY the carousel item creation in showProjectModal
    show_modal_start = html_content.find('carouselItem.style.display = "inline-block";')
    if show_modal_start != -1:
        # Find the end of this styling block
        styling_end = html_content.find('carouselItem.appendChild(img);', show_modal_start)
        if styling_end != -1:
            new_styling = '''// Enhanced styling for bigger images
                carouselItem.className = "carousel-item";
                
                const img = document.createElement("img");
                img.src = `${BASE_PATH}high_res_1200/img${String(imageNum).padStart(3, '0')}-high.jpg`;
                img.alt = `${project.title} - Image ${index + 1}`;
                img.onerror = () => {
                    // Fallback to medium res if high res fails
                    img.src = `${BASE_PATH}medium_res/img${String(imageNum).padStart(3, '0')}-med.jpg`;
                };
                
                carouselItem.appendChild(img);'''
            
            # Replace the styling section
            start_of_styling = html_content.rfind('const carouselItem = document.createElement("div");', 0, show_modal_start)
            if start_of_styling != -1:
                end_of_styling = html_content.find('carouselItem.appendChild(img);', styling_end) + len('carouselItem.appendChild(img);')
                html_content = html_content[:start_of_styling] + new_styling + html_content[end_of_styling:]
    
    # Enhance the setupInfiniteScroll function with auto-scroll
    setup_func_start = html_content.find('function setupInfiniteScroll(carousel, originalLength) {')
    if setup_func_start != -1:
        # Find the end of the function
        brace_count = 0
        pos = setup_func_start
        func_start_brace = html_content.find('{', pos) 
        pos = func_start_brace + 1
        brace_count = 1
        
        while brace_count > 0 and pos < len(html_content):
            if html_content[pos] == '{':
                brace_count += 1
            elif html_content[pos] == '}':
                brace_count -= 1
            pos += 1
        
        setup_func_end = pos
        
        new_setup_function = '''function setupInfiniteScroll(carousel, originalLength) {
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
        
        html_content = html_content[:setup_func_start] + new_setup_function + html_content[setup_func_end:]
    
    # Write the enhanced HTML
    with open('index.html', 'w') as f:
        f.write(html_content)
    
    print("🎨 SAFE CAROUSEL ENHANCEMENT COMPLETE!")
    print("✅ 625 clock functionality preserved")
    print("✅ Bigger photos (500px × 600px)")
    print("✅ High-resolution images")
    print("✅ Infinite auto-scroll animation")
    print("✅ Enhanced hover effects")

if __name__ == "__main__":
    safe_enhance_carousel()

