#!/usr/bin/env python3

def enhance_modal_carousel_only():
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # ONLY enhance the modal carousel CSS for bigger photos and smooth scroll
    enhanced_carousel_css = """
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
            padding: 20px;
        }
        
        #modal-carousel::-webkit-scrollbar {
            display: none;
        }
        
        #modal-carousel img {
            min-width: 80%;
            max-width: 80%;
            height: auto;
            max-height: 100%;
            object-fit: contain;
            border-radius: 8px;
            margin-right: 40px;
            flex-shrink: 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            transition: transform 0.3s ease;
        }
        
        #modal-carousel img:hover {
            transform: scale(1.02);
        }"""
    
    # Find and replace existing modal-carousel styles or add them
    if '#modal-carousel' in content:
        import re
        # Replace existing modal-carousel styles
        pattern = r'#modal-carousel\s*\{[^}]*\}'
        if re.search(pattern, content):
            content = re.sub(pattern, enhanced_carousel_css.strip(), content)
        else:
            # Add new styles before </style>
            content = content.replace('</style>', enhanced_carousel_css + '\n        </style>')
    else:
        # Add new styles before </style>
        content = content.replace('</style>', enhanced_carousel_css + '\n        </style>')
    
    # Write the updated content back to the same file
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print("Enhanced modal carousel only - bigger photos with smooth horizontal scroll!")

if __name__ == "__main__":
    enhance_modal_carousel_only()
