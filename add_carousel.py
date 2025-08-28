#!/usr/bin/env python3

def add_carousel():
    with open('index.html', 'r') as f:
        content = f.read()
    
    # Find the modal content and add enhanced carousel
    if '.carousel-container {' not in content:
        # Add carousel CSS before </style>
        carousel_css = """
        .carousel-container {
            position: relative;
            width: 100%;
            height: 500px;
            overflow: hidden;
            border-radius: 10px;
            background: #111;
        }
        
        .carousel-track {
            display: flex;
            height: 100%;
            transition: transform 0.5s ease;
        }
        
        .carousel-slide {
            min-width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .carousel-slide img {
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
            border-radius: 8px;
            transition: transform 0.3s ease;
        }
        
        .carousel-nav {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0, 0, 0, 0.5);
            color: white;
            border: none;
            padding: 15px 20px;
            cursor: pointer;
            font-size: 18px;
            border-radius: 5px;
            z-index: 10;
        }
        
        .carousel-prev { left: 20px; }
        .carousel-next { right: 20px; }
"""
        content = content.replace('</style>', carousel_css + '\n        </style>')
    
    # Save
    with open('index.html', 'w') as f:
        f.write(content)
    
    print("Carousel enhancement added!")

if __name__ == "__main__":
    add_carousel()
