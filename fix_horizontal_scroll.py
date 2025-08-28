#!/usr/bin/env python3

def fix_horizontal_scroll():
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Find and replace the modal-carousel CSS to make it truly horizontal
    import re
    
    # New horizontal carousel CSS
    horizontal_carousel_css = """        #modal-carousel {
            width: 100%;
            height: calc(100vh - 200px);
            overflow-x: auto;
            overflow-y: hidden;
            display: flex;
            scroll-behavior: smooth;
            scrollbar-width: none;
            -ms-overflow-style: none;
            position: relative;
            background: #111;
            padding: 20px;
            align-items: center;
            gap: 30px;
            white-space: nowrap;
        }
        
        #modal-carousel::-webkit-scrollbar {
            display: none;
        }
        
        #modal-carousel img {
            height: 80vh;
            width: auto;
            max-width: none;
            object-fit: contain;
            border-radius: 8px;
            flex-shrink: 0;
            display: inline-block;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
            transition: transform 0.3s ease;
        }
        
        #modal-carousel img:hover {
            transform: scale(1.02);
        }"""
    
    # Replace the existing modal-carousel CSS
    pattern = r'#modal-carousel\s*\{[^}]*\}'
    if re.search(pattern, content):
        content = re.sub(pattern, horizontal_carousel_css.strip(), content)
    else:
        # If not found, add before </style>
        content = content.replace('</style>', horizontal_carousel_css + '\n        </style>')
    
    # Write the updated content
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print("Fixed horizontal scroll - images should now scroll horizontally!")

if __name__ == "__main__":
    fix_horizontal_scroll()
