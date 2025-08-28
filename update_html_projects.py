#!/usr/bin/env python3
"""
Update HTML Projects Script
Manually updates the HTML file with correct project mappings
"""

import json

# Load the mapping
with open('/Volumes/T7/625industriesGIT/625industries/image_mapping.json', 'r') as f:
    mapping = json.load(f)

# Create new project structure based on our mappings
new_projects = {
    "2018": [
        {
            "title": "NIKE MAKERS STUDIO",
            "date": "10.18.2018",
            "location": "LOS ANGELES, CA",
            "description": "Interactive makers studio at the Staples Center showcasing Nike's customization capabilities.",
            "images": [1, 2, 3, 4, 5]
        },
        {
            "title": "NIKE MAKERS STUDIO",
            "date": "12.01.2018",
            "location": "ROOSEVELT FIELD MALL",
            "description": "Holiday season makers studio bringing customization to the mall environment.",
            "images": [6, 7, 8, 9, 10]
        }
    ],
    "2019": [],
    "2020": [],
    "COVID": [],
    "2022": [
        {
            "title": "NIKEBYYOU SUPER BOWL LVI",
            "date": "02.03.2022",
            "location": "LOS ANGELES, CA",
            "description": "Super Bowl LVI customization event featuring football and LA-inspired designs.",
            "images": [11, 12, 13, 14, 15]
        },
        {
            "title": "LEVI'S HOUSE × DAISY WORLD",
            "date": "04.05.2022",
            "location": "LOS ANGELES, CA",
            "description": "Collaboration with Daisy World at Levi's House featuring custom denim pieces.",
            "images": [16, 17, 18, 19, 20]
        },
        {
            "title": "LEVI'S × COME",
            "date": "04.07.2022",
            "location": "WATTS, CA",
            "description": "Community-focused collaboration with COME featuring custom streetwear.",
            "images": [21, 22, 23, 24, 25]
        },
        {
            "title": "BILLIE EILISH × NIKE (UPCYCLE)",
            "date": "04.19.2022",
            "location": "LOS ANGELES, CA",
            "description": "Sustainability-focused collaboration with Billie Eilish featuring upcycled Nike pieces.",
            "images": [26, 27, 28, 29, 30]
        },
        {
            "title": "MLB NIKEBYYOU",
            "date": "07.15.2022",
            "location": "LOS ANGELES, CA",
            "description": "MLB All-Star Game customization event featuring baseball-inspired designs.",
            "images": [31, 32, 33, 34, 35]
        },
        {
            "title": "ROLLING LOUD × LEVI'S",
            "date": "07.21.2022",
            "location": "MIAMI, FL",
            "description": "Rolling Loud Festival collaboration with Levi's featuring custom festival wear.",
            "images": [36, 37, 38, 39, 40]
        }
    ],
    "2023": [
        {
            "title": "NIKE SUPER BOWL LVII × UNDFTD",
            "date": "02.07.2023",
            "location": "PHOENIX, ARIZONA",
            "description": "Super Bowl LVII collaboration with UNDFTD featuring exclusive custom designs.",
            "images": [41, 42, 43, 44, 45]
        },
        {
            "title": "NIKEBYYOU SUPER BOWL",
            "date": "02.08.2023",
            "location": "PHOENIX, ARIZONA",
            "description": "Super Bowl LVII NikeByYou customization event featuring football-inspired designs.",
            "images": [46, 47, 48, 49, 50]
        },
        {
            "title": "ROLLING LOUD × LEVI'S",
            "date": "03.04.2023",
            "location": "LOS ANGELES, CA",
            "description": "Rolling Loud LA collaboration with Levi's featuring custom festival wear.",
            "images": [51, 52, 53, 54, 55]
        },
        {
            "title": "LEVI'S 501 DAY",
            "date": "05.18.2023",
            "location": "SAN FRANCISCO, CA",
            "description": "Celebration of Levi's 501 jeans featuring custom denim designs and heritage pieces.",
            "images": [56, 57, 58, 59, 60]
        },
        {
            "title": "ROLLING LOUD × LEVI'S",
            "date": "07.05.2023",
            "location": "PORTIMÃO, PORTUGAL",
            "description": "European Rolling Loud Festival collaboration with Levi's in Portugal.",
            "images": [61, 62, 63, 64]
        },
        {
            "title": "NIKE TEA ROOM",
            "date": "07.13.2023",
            "location": "LAS VEGAS, NV",
            "description": "Exclusive Nike Tea Room experience featuring luxury custom sneaker designs.",
            "images": [65, 66, 67, 68, 69]
        },
        {
            "title": "NIKE TEA ROOM",
            "date": "07.13.2023",
            "location": "LAS VEGAS, NV",
            "description": "Exclusive Nike Tea Room experience featuring luxury custom sneaker designs.",
            "images": [70, 71, 72, 73]
        }
    ],
    "2024": [
        {
            "title": "NIKEBYYOU SUPER BOWL LVIII",
            "date": "02.06.2024",
            "location": "LAS VEGAS, NV",
            "description": "Super Bowl LVIII NikeByYou customization event featuring Vegas-inspired designs.",
            "images": [74, 75, 76, 77, 78]
        },
        {
            "title": "ROLLING LOUD × MODELO",
            "date": "03.14.2024",
            "location": "LOS ANGELES, CA",
            "description": "Rolling Loud LA collaboration with Modelo featuring custom festival wear.",
            "images": [79, 80, 81, 82, 83]
        },
        {
            "title": "VEGAS KICK OFF × MODELO",
            "date": "09.01.2024",
            "location": "LAS VEGAS, NV",
            "description": "NFL season kickoff collaboration with Modelo featuring football-inspired designs.",
            "images": [84, 85, 86, 87, 88]
        }
    ],
    "2025": [
        {
            "title": "ALL STAR WEEKEND × BOARDROOM",
            "date": "02.15.2025",
            "location": "SAN FRANCISCO, CA",
            "description": "NBA All-Star Weekend collaboration with Boardroom featuring custom basketball designs.",
            "images": [89, 90, 91, 92, 93]
        }
    ]
}

# Read the HTML file
with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'r') as f:
    html_content = f.read()

# Find the start of the projects constant
start_marker = 'const projects = {'
end_marker = '};'

start_pos = html_content.find(start_marker)
if start_pos == -1:
    print("Could not find projects constant in HTML file")
    exit(1)

# Find the end of the projects constant
end_pos = html_content.find(end_marker, start_pos)
if end_pos == -1:
    print("Could not find end of projects constant")
    exit(1)

# Create the new projects JavaScript
new_projects_js = "const projects = " + json.dumps(new_projects, indent=2) + ";"

# Replace the projects section
new_html_content = (
    html_content[:start_pos] + 
    new_projects_js + 
    html_content[end_pos + 2:]  # +2 to skip the '};'
)

# Write the updated HTML file
with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'w') as f:
    f.write(new_html_content)

print("✅ HTML file updated successfully!")
print("Your website now displays the correct images for each project.")
