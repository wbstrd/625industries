#!/usr/bin/env python3

def make_carousel_like_image():
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Enhanced carousel CSS to match the screenshot exactly
    enhanced_carousel_css = """
        #modal-carousel {
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
        }
        
        #modal-carousel::-webkit-scrollbar {
            display: none;
        }
        
        #modal-carousel img {
            height: 80vh;
            width: auto;
            object-fit: contain;
            border-radius: 8px;
            flex-shrink: 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
            transition: transform 0.3s ease;
        }
        
        #modal-carousel img:hover {
            transform: scale(1.02);
        }
        
        .modal-content {
            width: 100%;
            height: 100%;
            position: relative;
            color: white;
            font-family: 'Inter', sans-serif;
            overflow: hidden;
            background: black;
        }
        
        .modal-header {
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
            margin: 0;
            color: #ccc;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .modal-body {
            width: 100%;
            height: 100%;
            padding: 0;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }"""
    
    # Replace existing modal styles
    import re
    
    # Replace modal-carousel styles
    pattern = r'#modal-carousel\s*\{[^}]*\}'
    if re.search(pattern, content):
        content = re.sub(pattern, enhanced_carousel_css.split('#modal-carousel {')[1].split('}')[0], content)
    
    # Replace modal-content styles
    pattern = r'\.modal-content\s*\{[^}]*\}'
    if re.search(pattern, content):
        new_modal_content = enhanced_carousel_css.split('.modal-content {')[1].split('.modal-header {')[0] + '}'
        content = re.sub(pattern, new_modal_content.strip(), content)
    
    # Replace modal-header styles
    pattern = r'\.modal-header\s*\{[^}]*\}'
    if re.search(pattern, content):
        new_modal_header = '.modal-header {' + enhanced_carousel_css.split('.modal-header {')[1].split('.modal-header h2 {')[0] + '}'
        content = re.sub(pattern, new_modal_header.strip(), content)
    
    # Replace modal-header h2 styles
    pattern = r'\.modal-header h2\s*\{[^}]*\}'
    if re.search(pattern, content):
        new_h2 = '.modal-header h2 {' + enhanced_carousel_css.split('.modal-header h2 {')[1].split('.modal-header p {')[0] + '}'
        content = re.sub(pattern, new_h2.strip(), content)
    
    # Replace modal-header p styles
    pattern = r'\.modal-header p\s*\{[^}]*\}'
    if re.search(pattern, content):
        new_p = '.modal-header p {' + enhanced_carousel_css.split('.modal-header p {')[1].split('.modal-body {')[0] + '}'
        content = re.sub(pattern, new_p.strip(), content)
    
    # Replace modal-body styles
    pattern = r'\.modal-body\s*\{[^}]*\}'
    if re.search(pattern, content):
        new_body = '.modal-body {' + enhanced_carousel_css.split('.modal-body {')[1]
        content = re.sub(pattern, new_body.strip(), content)
    
    # Write the updated content
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print("Enhanced carousel to match the exact look from your image!")

if __name__ == "__main__":
    make_carousel_like_image()
