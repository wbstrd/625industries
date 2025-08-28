#!/usr/bin/env python3
"""
Add functionality so clicking on any image in the 625 display opens that project's modal
"""

def add_image_click_modal():
    with open('index.html', 'r') as f:
        html_content = f.read()
    
    # Find the existing image click handler and enhance it
    click_handler_start = html_content.find('holder.addEventListener("click", (e) => {')
    if click_handler_start != -1:
        # Find the end of the existing click handler
        brace_count = 0
        pos = html_content.find('{', click_handler_start) + 1
        brace_count = 1
        
        while brace_count > 0 and pos < len(html_content):
            if html_content[pos] == '{':
                brace_count += 1
            elif html_content[pos] == '}':
                brace_count -= 1
            pos += 1
        
        click_handler_end = pos
        
        new_click_handler = '''holder.addEventListener("click", (e) => {
            const img = e.target;
            if (img.tagName !== "IMG") return;
            
            // Get the image number from the image element
            const imageNumber = imgRefs.find(ref => ref.img === img)?.imageNumber;
            if (!imageNumber) return;
            
            // Find the project for this image
            const project = imageToProjectMap[imageNumber];
            if (project) {
                // Open the project modal with enhanced carousel
                showProjectModal(project);
            }
        });'''
        
        html_content = html_content[:click_handler_start] + new_click_handler + html_content[click_handler_end:]
    
    # Make sure the modal is accessible - remove any conflicting styles
    # Find and update modal styles to ensure it shows on top
    modal_style_start = html_content.find('#project-modal {')
    if modal_style_start != -1:
        modal_style_end = html_content.find('}', modal_style_start) + 1
        
        enhanced_modal_style = '''#project-modal {
            display: none;
            position: fixed;
            z-index: 10000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(10px);
            animation: fadeIn 0.3s ease-in-out;
        }'''
        
        html_content = html_content[:modal_style_start] + enhanced_modal_style + html_content[modal_style_end:]
    
    # Add a subtle click indicator to images
    img_hover_style = '''
        #clock625-container img {
            transition: all 0.2s ease !important;
            cursor: pointer !important;
        }
        
        #clock625-container img:hover {
            transform: scale(1.05) !important;
            filter: brightness(1.1) !important;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.3) !important;
        }
    '''
    
    # Add the hover styles before the closing </style> tag
    style_end = html_content.rfind('</style>')
    if style_end != -1:
        html_content = html_content[:style_end] + img_hover_style + html_content[style_end:]
    
    with open('index.html', 'w') as f:
        f.write(html_content)
    
    print("✅ IMAGE CLICK FUNCTIONALITY ADDED!")
    print("🎯 Now when you click any image in the 625 display:")
    print("  • Opens the project modal for that specific image")
    print("  • Shows the enhanced carousel with all project photos")
    print("  • Smooth hover effects on images")
    print("  • High z-index modal ensures it appears on top")
    print("  • Backdrop blur for cinematic effect")
    print()
    print("🚀 Click any photo in the 625 → instant project gallery!")

if __name__ == "__main__":
    add_image_click_modal()

