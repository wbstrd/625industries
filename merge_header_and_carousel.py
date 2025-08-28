#!/usr/bin/env python3

def merge_improvements():
    """Add header and carousel improvements to the correctly mapped index"""
    
    # Read the correct mapping file
    with open('index_with_correct_mapping.html', 'r') as f:
        content = f.read()
    
    # Fix BASE_PATH to be local
    content = content.replace('const BASE_PATH = "./images/";', 'const BASE_PATH = "images/";')
    
    # Add header CSS and carousel improvements before </style>
    header_and_carousel_css = """
        /* Header Styles */
        .site-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            padding: 40px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            pointer-events: none;
        }

        .header-left {
            pointer-events: auto;
        }

        .header-logo {
            font-family: 'Bitcount Mono Light', monospace;
            font-size: 2rem;
            color: white;
            font-weight: normal;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }

        .header-tagline {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-size: 0.75rem;
            color: #ccc;
            font-weight: 200;
            line-height: 1.4;
            max-width: 300px;
        }

        .header-right {
            pointer-events: auto;
            position: relative;
        }

        .contact-trigger {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-size: 0.75rem;
            color: white;
            font-weight: 300;
            cursor: pointer;
            transition: color 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .contact-trigger:hover {
            color: #ddd;
        }

        .contact-form {
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 20px;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 30px;
            width: 320px;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.3s ease;
        }

        .contact-trigger:hover + .contact-form,
        .contact-form:hover {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }

        .contact-form h3 {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-size: 0.9rem;
            color: white;
            margin-bottom: 20px;
            font-weight: 200;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .contact-form input,
        .contact-form textarea {
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            padding: 12px;
            color: white;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-size: 0.75rem;
            font-weight: 200;
            margin-bottom: 15px;
            transition: border-color 0.3s ease;
        }

        .contact-form input:focus,
        .contact-form textarea:focus {
            outline: none;
            border-color: rgba(255, 255, 255, 0.3);
        }

        .contact-form input::placeholder,
        .contact-form textarea::placeholder {
            color: #666;
        }

        .contact-form textarea {
            resize: vertical;
            height: 80px;
        }

        .contact-form button {
            background: white;
            color: black;
            border: none;
            padding: 12px 24px;
            border-radius: 4px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-size: 0.75rem;
            font-weight: 200;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .contact-form button:hover {
            background: #f0f0f0;
            transform: translateY(-1px);
        }

        /* Enhanced Modal Carousel */
        #modal-carousel {
            width: 100%;
            height: 70vh;
            overflow-x: auto;
            overflow-y: hidden;
            white-space: nowrap;
            scroll-behavior: auto;
            scrollbar-width: none;
            -ms-overflow-style: none;
            display: flex;
            align-items: center;
            gap: 0;
            padding: 0;
            background: transparent;
        }
        
        #modal-carousel::-webkit-scrollbar {
            display: none;
        }
        
        #modal-carousel img {
            height: 60vh !important;
            width: auto !important;
            max-width: none !important;
            object-fit: contain !important;
            flex-shrink: 0 !important;
            border-radius: 4px;
            border: none;
            transition: transform 0.3s ease;
        }
        
        #modal-carousel img:hover {
            transform: scale(1.02);
        }

        #modal-description {
            margin: 15px 0 0 0;
            line-height: 1.5;
            color: #aaa;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-size: 0.9rem;
            font-weight: 200;
            max-width: 500px;
        }"""
    
    content = content.replace('</style>', header_and_carousel_css + '\n    </style>')
    
    # Add header HTML after <body>
    header_html = '''
    <!-- Site Header -->
    <header class="site-header">
        <div class="header-left">
            <div class="header-logo">625</div>
            <div class="header-tagline">A universally taught creative agency with deep roots in NYC, Miami, LA, and Paris.</div>
        </div>
        <div class="header-right">
            <div class="contact-trigger">Contact</div>
            <div class="contact-form">
                <h3>Get in Touch</h3>
                <input type="text" placeholder="Name" required>
                <input type="email" placeholder="Email" required>
                <input type="text" placeholder="Subject">
                <textarea placeholder="Message" required></textarea>
                <button type="submit">Send Message</button>
            </div>
        </div>
    </header>

    '''
    
    content = content.replace('<body>', '<body>' + header_html)
    
    # Write the merged file
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print("✅ Merged correct mapping with header and carousel improvements!")

if __name__ == "__main__":
    merge_improvements()
