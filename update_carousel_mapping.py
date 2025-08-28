#!/usr/bin/env python3

import json

def update_carousel_mapping():
    """Update the index_with_carousel.html with the correct project mapping"""
    
    # The correct mapping from the HEIC script
    projects_by_year = {
        "2017": [
            {
                "title": "LA ALL STAR",
                "date": "2017.02.18",
                "location": "LOS ANGELES",
                "description": "NBA All-Star Weekend activation in Los Angeles.",
                "images": [91, 92, 93, 94, 95]
            }
        ],
        "2018": [
            {
                "title": "MAKERS STUDIO",
                "date": "2018.12.01",
                "location": "LOS ANGELES",
                "description": "Nike Makers Studio creative workshop in Los Angeles.",
                "images": [1, 2, 3, 4, 5]
            },
            {
                "title": "MAKERS STUDIO",
                "date": "2018.10.01",
                "location": "LOS ANGELES", 
                "description": "Nike Makers Studio October session in Los Angeles.",
                "images": [6, 7, 8, 9, 10]
            }
        ],
        "2022": [
            {
                "title": "LEVI'S HOUSE × DAISY WORLD",
                "date": "2022.02.01",
                "location": "LOS ANGELES",
                "description": "Levi's House × Daisy World activation in Los Angeles.",
                "images": [11, 12, 13, 14, 15]
            },
            {
                "title": "BILLIE EILISH × NIKE (UPCYCLE)",
                "date": "2022.04.01",
                "location": "LOS ANGELES",
                "description": "Billie Eilish Nike upcycle activation in Los Angeles.",
                "images": [16, 17, 18, 19, 20]
            },
            {
                "title": "NFL DRAFT DAY",
                "date": "2022.04.28",
                "location": "LAS VEGAS",
                "description": "NFL Draft Day experience in Las Vegas.",
                "images": [26, 27, 28, 29, 30]
            },
            {
                "title": "LEVI'S × COME",
                "date": "2022.06.01",
                "location": "LOS ANGELES",
                "description": "Levi's × Come collaboration in Watts, Los Angeles.",
                "images": [21, 22, 23, 24, 25]
            },
            {
                "title": "MLB NIKEBYYOU",
                "date": "2022.07.19",
                "location": "LOS ANGELES",
                "description": "MLB All-Star NikeByYou customization experience.",
                "images": [31, 32, 33, 34, 35]
            }
        ],
        "2023": [
            {
                "title": "SUPER BOWL LVII × UNDFTD",
                "date": "2023.02.12",
                "location": "PHOENIX",
                "description": "Super Bowl LVII Undefeated activation in Phoenix.",
                "images": [36, 37, 38, 39, 40]
            },
            {
                "title": "NIKEBYYOU – SUPER BOWL",
                "date": "2023.02.12",
                "location": "PHOENIX",
                "description": "Super Bowl LVII NikeByYou experience in Phoenix.",
                "images": [41, 42, 43, 44, 45]
            },
            {
                "title": "ROLLING LOUD × LEVI'S",
                "date": "2023.03.03",
                "location": "MIAMI",
                "description": "Rolling Loud Miami Levi's activation.",
                "images": [46, 47, 48, 49, 50]
            },
            {
                "title": "LEVI'S 501 DAY",
                "date": "2023.05.20",
                "location": "SAN FRANCISCO",
                "description": "Levi's 501 Day celebration in San Francisco.",
                "images": [51, 52, 53, 54, 55]
            },
            {
                "title": "NIKE TEA ROOM",
                "date": "2023.07.15",
                "location": "LOS ANGELES",
                "description": "Nike Tea Room experience in Los Angeles.",
                "images": [61, 62, 63, 64, 65]
            },
            {
                "title": "ROLLING LOUD × LEVI'S",
                "date": "2023.07.21",
                "location": "MIAMI",
                "description": "Rolling Loud July Levi's collaboration.",
                "images": [56, 57, 58, 59, 60]
            }
        ],
        "2024": [
            {
                "title": "SUPER BOWL LVIII NIKEBYYOU",
                "date": "2024.02.11",
                "location": "LAS VEGAS",
                "description": "Super Bowl LVIII NikeByYou activation in Las Vegas.",
                "images": [66, 67, 68, 69, 70]
            },
            {
                "title": "ROLLING LOUD × MODELO",
                "date": "2024.03.22",
                "location": "LOS ANGELES",
                "description": "Modelo Rolling Loud LA activation.",
                "images": [71, 72, 73, 74, 75]
            },
            {
                "title": "VEGAS KICK OFF",
                "date": "2024.09.14",
                "location": "LAS VEGAS",
                "description": "Vegas Modelo Kick Off event.",
                "images": [76, 77, 78, 79, 80]
            }
        ],
        "2025": [
            {
                "title": "TXRX WORKSHOP",
                "date": "2025.02.11",
                "location": "HOUSTON",
                "description": "Nike TXRX Workshop event in Houston.",
                "images": [81, 82, 83, 84, 85]
            },
            {
                "title": "ALL STAR WEEKEND × BOARDROOM",
                "date": "2025.02.15",
                "location": "SAN FRANCISCO",
                "description": "NBA All-Star Weekend Boardroom event in San Francisco.",
                "images": [86, 87, 88, 89, 90]
            }
        ]
    }
    
    # Read current HTML
    with open('index_with_carousel.html', 'r') as f:
        html_content = f.read()
    
    # Find and replace the projects constant
    import re
    
    # Create the new projects JavaScript
    new_projects_js = "const projects = " + json.dumps(projects_by_year, indent=2) + ";"
    
    # Replace the projects constant
    pattern = r'const projects = \{[^}]*\};'
    if re.search(pattern, html_content, re.DOTALL):
        html_content = re.sub(pattern, new_projects_js, html_content, flags=re.DOTALL)
    else:
        print("Could not find projects constant")
        return False
    
    # Write the updated HTML file
    with open('index_with_carousel.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Updated index_with_carousel.html with correct project mapping!")
    return True

if __name__ == "__main__":
    update_carousel_mapping()
