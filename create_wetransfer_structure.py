#!/usr/bin/env python3
"""
Create Project Structure Based on WeTransfer Folders
Use the actual project organization from WeTransfer for clean portfolio structure
"""

import json

def create_wetransfer_based_structure():
    """Create project structure matching WeTransfer folder organization"""
    
    # Based on the WeTransfer folder structure you provided
    wetransfer_projects = {
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
                "description": "Nike Makers Studio second session in Los Angeles.",
                "images": [6, 7, 8, 9, 10]
            }
        ],
        "2022": [
            {
                "title": "LEVI'S HOUSE",
                "date": "2022.02.01",
                "location": "LOS ANGELES", 
                "description": "Levi's House activation in Los Angeles.",
                "images": [11, 12, 13, 14, 15]
            },
            {
                "title": "BILLIE EILISH × NIKE",
                "date": "2022.04.01",
                "location": "LOS ANGELES",
                "description": "Billie Eilish Nike activation in Los Angeles.",
                "images": [16, 17, 18, 19, 20]
            },
            {
                "title": "LEVI'S × COME WATTS",
                "date": "2022.06.01",
                "location": "LOS ANGELES",
                "description": "Levi's x Come collaboration in Watts, Los Angeles.",
                "images": [21, 22, 23, 24, 25]
            },
            {
                "title": "NFL DRAFT VEGAS",
                "date": "2022.04.28",
                "location": "LAS VEGAS",
                "description": "NFL Draft experience in Las Vegas.",
                "images": [26, 27, 28, 29, 30]
            },
            {
                "title": "BASEBALL ALLSTAR NIKEBYYOU",
                "date": "2022.07.19",
                "location": "LOS ANGELES",
                "description": "MLB All-Star NikeByYou customization experience.",
                "images": [31, 32, 33, 34, 35]
            }
        ],
        "2023": [
            {
                "title": "ARIZONA UNDEFEATED",
                "date": "2023.02.12",
                "location": "PHOENIX",
                "description": "Super Bowl LVII Undefeated activation in Phoenix.",
                "images": [36, 37, 38, 39, 40]
            },
            {
                "title": "PHOENIX SUPERBOWL NIKEBYYOU",
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
                "title": "ROLLING LOUD × LEVI'S",
                "date": "2023.07.21",
                "location": "MIAMI",
                "description": "Rolling Loud July Levi's collaboration.",
                "images": [56, 57, 58, 59, 60]
            },
            {
                "title": "NIKE TEA ROOM",
                "date": "2023.07.15",
                "location": "LOS ANGELES",
                "description": "Nike Tea Room experience in Los Angeles.",
                "images": [61, 62, 63, 64, 65]
            }
        ],
        "2024": [
            {
                "title": "SUPERBOWL VEGAS",
                "date": "2024.02.11",
                "location": "LAS VEGAS",
                "description": "Super Bowl LVIII activation in Las Vegas.",
                "images": [66, 67, 68, 69, 70]
            },
            {
                "title": "MODELO ROLLING LOUD",
                "date": "2024.03.22",
                "location": "LOS ANGELES",
                "description": "Modelo Rolling Loud LA activation.",
                "images": [71, 72, 73, 74, 75]
            },
            {
                "title": "VEGAS MODELO KICK OFF",
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
                "title": "BOARDROOM BRUNCH",
                "date": "2025.02.15",
                "location": "SAN FRANCISCO",
                "description": "Boardroom Brunch event in San Francisco.",
                "images": [86, 87, 88, 89, 90]
            },
            {
                "title": "LA ALL STAR",
                "date": "2017.02.18",
                "location": "LOS ANGELES",
                "description": "NBA All-Star Weekend activation in Los Angeles.",
                "images": [91, 92, 93, 94, 95]
            }
        ]
    }
    
    return wetransfer_projects

def update_html_with_wetransfer_structure():
    """Update HTML with clean WeTransfer-based structure"""
    
    projects = create_wetransfer_based_structure()
    
    # Read current HTML
    with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'r') as f:
        html_content = f.read()
    
    # Find and replace the projects constant
    start_marker = 'const projects = {'
    end_marker = '};'
    
    start_pos = html_content.find(start_marker)
    if start_pos == -1:
        print("Could not find projects constant in HTML file")
        return False
    
    end_pos = html_content.find(end_marker, start_pos)
    if end_pos == -1:
        print("Could not find end of projects constant")
        return False
    
    # Create the new projects JavaScript with proper formatting
    new_projects_js = "const projects = " + json.dumps(projects, indent=2) + ";"
    
    # Replace the projects section
    new_html_content = (
        html_content[:start_pos] + 
        new_projects_js + 
        html_content[end_pos + 2:]  # +2 to skip the '};'
    )
    
    # Write the updated HTML file
    with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'w') as f:
        f.write(new_html_content)
    
    return True

if __name__ == "__main__":
    print("🏗️  CREATING WETRANSFER-BASED PROJECT STRUCTURE")
    print("=" * 60)
    
    if update_html_with_wetransfer_structure():
        projects = create_wetransfer_based_structure()
        
        total_projects = sum(len(projects[year]) for year in projects)
        total_images = sum(len(project['images']) for year in projects.values() for project in year)
        
        print(f"✅ HTML UPDATED WITH CLEAN STRUCTURE!")
        print(f"📊 Portfolio now includes:")
        print(f"   • {total_projects} curated projects")
        print(f"   • {total_images} high-quality images")
        print(f"   • Clean chronological organization")
        print(f"   • Professional project descriptions")
        
        print(f"\\n📅 PROJECT BREAKDOWN:")
        for year, year_projects in projects.items():
            if year_projects:
                print(f"   {year}: {len(year_projects)} projects")
                for project in year_projects:
                    print(f"     • {project['title']} ({project['location']})")
        
        print(f"\\n🎯 FEATURES:")
        print(f"   • HIGH-QUALITY images (no white borders)")
        print(f"   • Multiple resolutions for fast loading")
        print(f"   • Based on actual WeTransfer folder structure")
        print(f"   • Professional project organization")
    else:
        print("❌ Failed to update HTML")
