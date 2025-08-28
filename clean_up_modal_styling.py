#!/usr/bin/env python3

def clean_up_modal_styling():
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    import re
    
    # Clean modal carousel CSS - remove gaps and weird background
    clean_carousel_css = """        #modal-carousel {
            width: 100%;
            height: calc(100vh - 200px);
            overflow-x: auto;
            overflow-y: hidden;
            display: flex;
            scroll-behavior: smooth;
            scrollbar-width: none;
            -ms-overflow-style: none;
            position: relative;
            background: transparent;
            padding: 0;
            align-items: center;
            gap: 15px;
        }
        
        #modal-carousel::-webkit-scrollbar {
            display: none;
        }
        
        #modal-carousel img {
            height: 80vh;
            width: auto;
            max-width: none;
            object-fit: contain;
            border-radius: 0;
            flex-shrink: 0;
            display: inline-block;
            box-shadow: none;
            transition: transform 0.3s ease;
        }
        
        #modal-carousel img:hover {
            transform: scale(1.02);
        }"""
    
    # Clean modal header CSS - white text, better positioning
    clean_header_css = """        .modal-header {
            position: absolute;
            top: 40px;
            left: 40px;
            z-index: 2001;
            font-family: 'Bitcount Mono Light', monospace;
        }
        
        .modal-header h2 {
            margin: 0 0 5px 0;
            font-size: 2rem;
            font-weight: 300;
            color: white;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .modal-header p {
            margin: 0 0 10px 0;
            color: #ccc;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        #modal-description {
            margin: 10px 0 0 0;
            color: #aaa;
            font-size: 0.85rem;
            line-height: 1.4;
            max-width: 400px;
        }"""
    
    # Clean modal content CSS - pure black background
    clean_content_css = """        .modal-content {
            width: 100%;
            height: 100%;
            position: relative;
            color: white;
            font-family: 'Inter', sans-serif;
            overflow: hidden;
            background: black;
        }
        
        .modal-body {
            width: 100%;
            height: 100%;
            padding: 0;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: center;
            background: black;
        }"""
    
    # Replace modal-carousel styles
    pattern = r'#modal-carousel\s*\{[^}]*\}'
    content = re.sub(pattern, clean_carousel_css.strip(), content)
    
    # Replace modal-header styles
    pattern = r'\.modal-header\s*\{[^}]*\}'
    content = re.sub(pattern, clean_header_css.split('.modal-header {')[1].split('.modal-header h2 {')[0].strip(), content)
    
    # Replace modal-header h2 styles
    pattern = r'\.modal-header h2\s*\{[^}]*\}'
    content = re.sub(pattern, clean_header_css.split('.modal-header h2 {')[1].split('.modal-header p {')[0].strip(), content)
    
    # Replace modal-header p styles
    pattern = r'\.modal-header p\s*\{[^}]*\}'
    content = re.sub(pattern, clean_header_css.split('.modal-header p {')[1].split('#modal-description {')[0].strip(), content)
    
    # Add modal-description styles if not exists
    if '#modal-description {' not in content:
        desc_css = '\n        #modal-description {' + clean_header_css.split('#modal-description {')[1]
        content = content.replace('</style>', desc_css + '\n        </style>')
    
    # Replace modal-content styles
    pattern = r'\.modal-content\s*\{[^}]*\}'
    content = re.sub(pattern, clean_content_css.split('.modal-content {')[1].split('.modal-body {')[0].strip(), content)
    
    # Replace modal-body styles
    pattern = r'\.modal-body\s*\{[^}]*\}'
    content = re.sub(pattern, clean_content_css.split('.modal-body {')[1].strip(), content)
    
    # Write the updated content
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print("Cleaned up modal styling - removed weird background, closer images, white text!")

if __name__ == "__main__":
    clean_up_modal_styling()
