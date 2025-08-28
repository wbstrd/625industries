#!/usr/bin/env python3
"""
Simple carousel enhancement - just make it look better with infinite scroll on mousepad drag
"""

def enhance_carousel():
    with open('index.html', 'r') as f:
        html_content = f.read()
    
    # Fix the BASE_PATH to use GitHub URLs
    html_content = html_content.replace(
        'const BASE_PATH = "./images/";',
        'const BASE_PATH = "https://raw.githubusercontent.com/wbstrd/625industries/main/images/";'
    )
    
    # Fix the showProjectModal function - it was broken
    modal_function_start = html_content.find('function showProjectModal(project) {')
    if modal_function_start != -1:
        # Find the end of the function
        brace_count = 0
        pos = html_content.find('{', modal_function_start) + 1
        brace_count = 1
        
        while brace_count > 0 and pos < len(html_content):
            if html_content[pos] == '{':
                brace_count += 1
            elif html_content[pos] == '}':
                brace_count -= 1
            pos += 1
        
        modal_function_end = pos
        
        new_modal_function = '''function showProjectModal(project) {
            document.getElementById("modal-title").textContent = project.title;
            document.getElementById("modal-date").textContent = `${project.date} – ${project.location}`;
            document.getElementById("modal-description").textContent = project.description;
            
            // Create carousel with all project images
            const carousel = document.getElementById("modal-carousel");
            carousel.innerHTML = '';
            
            // Create infinite scroll by duplicating images 3 times
            const allImages = [...project.images, ...project.images, ...project.images];
            
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
            
            // Set up infinite scroll
            setupInfiniteScroll(carousel, project.images.length);
        }'''
        
        html_content = html_content[:modal_function_start] + new_modal_function + html_content[modal_function_end:]
    
    # Enhance the carousel CSS
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
            scroll-behavior: smooth;
            -webkit-overflow-scrolling: touch;
        }

        #modal-carousel::-webkit-scrollbar {
            display: none;
        }

        .carousel-item {
            display: inline-block !important;
            width: auto !important;
            height: 500px !important;
            margin-right: 25px !important;
            vertical-align: top !important;
            flex-shrink: 0 !important;
            transition: transform 0.3s ease !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4) !important;
        }

        .carousel-item:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6) !important;
        }

        .carousel-item img {
            width: auto !important;
            height: 100% !important;
            object-fit: cover !important;
            display: block !important;
            border-radius: 12px !important;
        }'''
        
        html_content = html_content[:carousel_css_start] + new_carousel_css + html_content[carousel_css_end:]
    
    # Enhance the mouse wheel scrolling
    wheel_listener_start = html_content.find('// Add mouse wheel support for horizontal scrolling in modal')
    if wheel_listener_start != -1:
        wheel_listener_end = html_content.find('}, { passive: false });', wheel_listener_start) + len('}, { passive: false });')
        
        new_wheel_listener = '''// Enhanced mouse wheel support for smooth horizontal scrolling
        window.addEventListener("wheel", (e) => {
            const modal = document.getElementById("project-modal");
            const carousel = document.getElementById("modal-carousel");
            
            if (modal.style.display === "block" && carousel) {
                e.preventDefault();
                
                // Smooth horizontal scroll with momentum
                const scrollSpeed = Math.abs(e.deltaY) > Math.abs(e.deltaX) ? e.deltaY : e.deltaX;
                const scrollAmount = scrollSpeed * 3; // Increased speed
                
                // Apply smooth scroll
                carousel.scrollBy({
                    left: scrollAmount,
                    behavior: 'smooth'
                });
            }
        }, { passive: false });'''
        
        html_content = html_content[:wheel_listener_start] + new_wheel_listener + html_content[wheel_listener_end:]
    
    # Enhance setupInfiniteScroll function
    setup_func_start = html_content.find('function setupInfiniteScroll(carousel, originalLength) {')
    if setup_func_start != -1:
        # Find the end of the function
        brace_count = 0
        pos = html_content.find('{', setup_func_start) + 1
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
            const itemWidth = 400; // Approximate item width + margin
            const totalWidth = itemWidth * originalLength;
            
            // Set initial scroll position to the middle set
            setTimeout(() => {
                carousel.scrollLeft = totalWidth;
            }, 100);
            
            carousel.addEventListener('scroll', () => {
                if (isScrolling) return;
                
                const scrollLeft = carousel.scrollLeft;
                
                // If scrolled to the end of the third set, jump to the middle set
                if (scrollLeft >= totalWidth * 2.8) {
                    isScrolling = true;
                    carousel.scrollLeft = totalWidth;
                    setTimeout(() => { isScrolling = false; }, 100);
                }
                // If scrolled to the beginning of the first set, jump to the middle set
                else if (scrollLeft <= totalWidth * 0.2) {
                    isScrolling = true;
                    carousel.scrollLeft = totalWidth;
                    setTimeout(() => { isScrolling = false; }, 100);
                }
            });
            
            // Enhanced touch/trackpad support
            let startX = 0;
            let scrollLeftStart = 0;
            
            carousel.addEventListener('touchstart', (e) => {
                startX = e.touches[0].pageX;
                scrollLeftStart = carousel.scrollLeft;
            });
            
            carousel.addEventListener('touchmove', (e) => {
                e.preventDefault();
                const x = e.touches[0].pageX;
                const walk = (startX - x) * 2; // Scroll speed
                carousel.scrollLeft = scrollLeftStart + walk;
            });
        }'''
        
        html_content = html_content[:setup_func_start] + new_setup_function + html_content[setup_func_end:]
    
    with open('index.html', 'w') as f:
        f.write(html_content)
    
    print("🎨 CAROUSEL ENHANCED!")
    print("✅ Fixed broken modal function")
    print("✅ Updated to GitHub image URLs")
    print("✅ Bigger, better-looking photos (500px height)")
    print("✅ Smooth infinite horizontal scroll")
    print("✅ Enhanced mousepad/trackpad scrolling")
    print("✅ Beautiful hover effects and shadows")
    print("✅ Smooth transitions and animations")

if __name__ == "__main__":
    enhance_carousel()

