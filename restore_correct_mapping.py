#!/usr/bin/env python3
"""
Restore the EXACT correct mapping that was working perfectly before the carousel enhancement request
"""

def restore_correct_mapping():
    # Read current HTML
    with open('index.html', 'r') as f:
        html_content = f.read()
    
    # The EXACT correct mapping from the working commit
    correct_projects_data = '''const projects = {
  "2017": [
    {
      "title": "LA ALL STAR",
      "date": "2017.02.18",
      "location": "LOS ANGELES",
      "description": "NBA All-Star Weekend activation in Los Angeles.",
      "images": [
        91,
        92,
        93,
        94,
        95
      ]
    }
  ],
  "2018": [
    {
      "title": "MAKERS STUDIO",
      "date": "2018.10.01",
      "location": "LOS ANGELES",
      "description": "Nike Makers Studio October session in Los Angeles.",
      "images": [
        6,
        7,
        8,
        9,
        10
      ]
    },
    {
      "title": "MAKERS STUDIO",
      "date": "2018.12.01",
      "location": "LOS ANGELES",
      "description": "Nike Makers Studio creative workshop in Los Angeles.",
      "images": [
        1,
        2,
        3,
        4,
        5
      ]
    }
  ],
  "2022": [
    {
      "title": "LEVI'S HOUSE × DAISY WORLD",
      "date": "2022.02.01",
      "location": "LOS ANGELES",
      "description": "Levi's House × Daisy World activation in Los Angeles.",
      "images": [
        11,
        12,
        13,
        14,
        15
      ]
    },
    {
      "title": "BILLIE EILISH × NIKE (UPCYCLE)",
      "date": "2022.04.01",
      "location": "LOS ANGELES",
      "description": "Billie Eilish Nike upcycle activation in Los Angeles.",
      "images": [
        16,
        17,
        18,
        19,
        20
      ]
    },
    {
      "title": "NFL DRAFT DAY",
      "date": "2022.04.28",
      "location": "LAS VEGAS",
      "description": "NFL Draft Day experience in Las Vegas.",
      "images": [
        26,
        27,
        28,
        29,
        30
      ]
    },
    {
      "title": "LEVI'S × COME",
      "date": "2022.06.01",
      "location": "LOS ANGELES",
      "description": "Levi's × Come collaboration in Watts, Los Angeles.",
      "images": [
        21,
        22,
        23,
        24,
        25
      ]
    },
    {
      "title": "MLB NIKEBYYOU",
      "date": "2022.07.19",
      "location": "LOS ANGELES",
      "description": "MLB All-Star NikeByYou customization experience.",
      "images": [
        31,
        32,
        33,
        34,
        35
      ]
    }
  ],
  "2023": [
    {
      "title": "SUPER BOWL LVII × UNDFTD",
      "date": "2023.02.12",
      "location": "PHOENIX",
      "description": "Super Bowl LVII Undefeated activation in Phoenix.",
      "images": [
        36,
        37,
        38,
        39,
        40
      ]
    },
    {
      "title": "NIKEBYYOU – SUPER BOWL",
      "date": "2023.02.12",
      "location": "PHOENIX",
      "description": "Super Bowl LVII NikeByYou experience in Phoenix.",
      "images": [
        41,
        42,
        43,
        44,
        45
      ]
    },
    {
      "title": "ROLLING LOUD × LEVI'S",
      "date": "2023.03.03",
      "location": "MIAMI",
      "description": "Rolling Loud Miami Levi's activation.",
      "images": [
        46,
        47,
        48,
        49,
        50
      ]
    },
    {
      "title": "LEVI'S 501 DAY",
      "date": "2023.05.20",
      "location": "SAN FRANCISCO",
      "description": "Levi's 501 Day celebration in San Francisco.",
      "images": [
        51,
        52,
        53,
        54,
        55
      ]
    },
    {
      "title": "NIKE TEA ROOM",
      "date": "2023.07.15",
      "location": "LOS ANGELES",
      "description": "Nike Tea Room experience in Los Angeles.",
      "images": [
        61,
        62,
        63,
        64,
        65
      ]
    },
    {
      "title": "ROLLING LOUD × LEVI'S",
      "date": "2023.07.21",
      "location": "MIAMI",
      "description": "Rolling Loud July Levi's collaboration.",
      "images": [
        56,
        57,
        58,
        59,
        60
      ]
    }
  ],
  "2024": [
    {
      "title": "SUPER BOWL LVIII NIKEBYYOU",
      "date": "2024.02.11",
      "location": "LAS VEGAS",
      "description": "Super Bowl LVIII NikeByYou activation in Las Vegas.",
      "images": [
        66,
        67,
        68,
        69,
        70
      ]
    },
    {
      "title": "ROLLING LOUD × MODELO",
      "date": "2024.03.22",
      "location": "LOS ANGELES",
      "description": "Modelo Rolling Loud LA activation.",
      "images": [
        71,
        72,
        73,
        74,
        75
      ]
    },
    {
      "title": "VEGAS KICK OFF",
      "date": "2024.09.14",
      "location": "LAS VEGAS",
      "description": "Vegas Modelo Kick Off event.",
      "images": [
        76,
        77,
        78,
        79,
        80
      ]
    }
  ],
  "2025": [
    {
      "title": "TXRX WORKSHOP",
      "date": "2025.02.11",
      "location": "HOUSTON",
      "description": "Nike TXRX Workshop event in Houston.",
      "images": [
        81,
        82,
        83,
        84,
        85
      ]
    },
    {
      "title": "ALL STAR WEEKEND × BOARDROOM",
      "date": "2025.02.15",
      "location": "SAN FRANCISCO",
      "description": "NBA All-Star Weekend Boardroom event in San Francisco.",
      "images": [
        86,
        87,
        88,
        89,
        90
      ]
    }
  ]
};'''

    # Replace the projects data
    projects_start = html_content.find('const projects = {')
    if projects_start != -1:
        # Find the end of the projects object
        brace_count = 0
        pos = html_content.find('{', projects_start) + 1
        brace_count = 1
        
        while brace_count > 0 and pos < len(html_content):
            if html_content[pos] == '{':
                brace_count += 1
            elif html_content[pos] == '}':
                brace_count -= 1
            pos += 1
        
        projects_end = pos
        
        # Replace with correct mapping
        html_content = html_content[:projects_start] + correct_projects_data + html_content[projects_end:]
    
    with open('index.html', 'w') as f:
        f.write(html_content)
    
    print("✅ EXACT CORRECT MAPPING RESTORED!")
    print("🎯 Perfect project-to-image matching:")
    print("  • BILLIE EILISH × NIKE → images 16-20")
    print("  • ROLLING LOUD × MODELO → images 71-75") 
    print("  • TXRX WORKSHOP → images 81-85")
    print("  • NFL DRAFT DAY → images 26-30")
    print("  • LEVI'S HOUSE × DAISY WORLD → images 11-15")
    print("  • LA ALL STAR → images 91-95")
    print("  • And all other projects perfectly mapped!")
    print()
    print("🚀 Carousel stays perfect + correct photos!")

if __name__ == "__main__":
    restore_correct_mapping()

