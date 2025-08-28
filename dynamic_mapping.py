#!/usr/bin/env python3
"""
Dynamic mapping that assigns correct number of images per project
"""

import os
import json
from collections import OrderedDict

def scan_wetransfer_folders():
    """Scan wetransfer folders and count actual photos"""
    wetransfer_base = "/Volumes/T7"
    projects = []
    
    print("🔍 Scanning wetransfer folders for accurate photo counts...")
    
    # Find all wetransfer folders
    for root, dirs, files in os.walk(wetransfer_base):
        if "wetransfer" in root.lower():
            for dir_name in dirs:
                # Skip system directories
                if dir_name.startswith('.'):
                    continue
                    
                full_path = os.path.join(root, dir_name)
                
                # Count image files
                image_files = []
                try:
                    for f in os.listdir(full_path):
                        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic')):
                            image_files.append(f)
                except:
                    continue
                
                if len(image_files) > 0:
                    projects.append({
                        'folder_name': dir_name,
                        'path': full_path,
                        'image_count': len(image_files),
                        'files': sorted(image_files)
                    })
                    print(f"  📁 {dir_name}: {len(image_files)} images")
    
    return sorted(projects, key=lambda x: x['folder_name'])

def create_dynamic_mapping():
    """Create mapping with correct image counts"""
    projects = scan_wetransfer_folders()
    
    # Project mapping to years and proper names
    project_mapping = {
        'December 2018 - Maker\'s Studio Nike': {'year': '2018', 'title': 'MAKERS STUDIO', 'date': '2018.12.01', 'location': 'LOS ANGELES'},
        'October 2018 Nike Maker\'s Space': {'year': '2018', 'title': 'MAKERS STUDIO', 'date': '2018.10.01', 'location': 'LOS ANGELES'},
        'LA 2022 Levi\'s House': {'year': '2022', 'title': 'LEVI\'S HOUSE × DAISY WORLD', 'date': '2022.02.01', 'location': 'LOS ANGELES'},
        'LA Billie Eillish Nike Activation': {'year': '2022', 'title': 'BILLIE EILISH × NIKE (UPCYCLE)', 'date': '2022.04.01', 'location': 'LOS ANGELES'},
        'Levi\'s x Come Watts LA': {'year': '2022', 'title': 'LEVI\'S × COME', 'date': '2022.06.01', 'location': 'LOS ANGELES'},
        'NFL Draft Vegas 2022': {'year': '2022', 'title': 'NFL DRAFT DAY', 'date': '2022.04.28', 'location': 'LAS VEGAS'},
        'July 2022 Baseball Allstar NikeByYou': {'year': '2022', 'title': 'MLB NIKEBYYOU', 'date': '2022.07.19', 'location': 'LOS ANGELES'},
        'Arizona February 2023 Undefeated': {'year': '2023', 'title': 'SUPER BOWL LVII × UNDFTD', 'date': '2023.02.12', 'location': 'PHOENIX'},
        'Phoenix Superbowl NikeByYou February 2023': {'year': '2023', 'title': 'NIKEBYYOU – SUPER BOWL', 'date': '2023.02.12', 'location': 'PHOENIX'},
        'Rolling Loud 2023 March Levi\'s': {'year': '2023', 'title': 'ROLLING LOUD × LEVI\'S', 'date': '2023.03.03', 'location': 'MIAMI'},
        'Photos 501 Day Levi\'s SF': {'year': '2023', 'title': 'LEVI\'S 501 DAY', 'date': '2023.05.20', 'location': 'SAN FRANCISCO'},
        'July 2023 Rolling Loud Levi\'s': {'year': '2023', 'title': 'ROLLING LOUD × LEVI\'S', 'date': '2023.07.15', 'location': 'MIAMI'},
        'Tea Room July 2023 Nike': {'year': '2023', 'title': 'NIKE TEA ROOM', 'date': '2023.07.21', 'location': 'LOS ANGELES'},
        'February 2024 Superbowl Vegas': {'year': '2024', 'title': 'SUPER BOWL LVIII NIKEBYYOU', 'date': '2024.02.06', 'location': 'LAS VEGAS'},
        'Modelo Rolling Loud LA March': {'year': '2024', 'title': 'ROLLING LOUD × MODELO', 'date': '2024.03.22', 'location': 'LOS ANGELES'},
        'Vegas Modelo Kick Off - 2024': {'year': '2024', 'title': 'VEGAS KICK OFF', 'date': '2024.09.14', 'location': 'LAS VEGAS'},
        'Photos for TXRX Nike': {'year': '2025', 'title': 'TXRX WORKSHOP', 'date': '2025.02.11', 'location': 'HOUSTON'},
        'Photos for Boardroom Brunch': {'year': '2025', 'title': 'ALL STAR WEEKEND × BOARDROOM', 'date': '2025.02.15', 'location': 'SAN FRANCISCO'},
        'LA 2017 All Star': {'year': '2017', 'title': 'LA ALL STAR', 'date': '2017.02.18', 'location': 'LOS ANGELES'}
    }
    
    # Create dynamic mapping with correct image counts
    print(f"\n📊 Creating dynamic mapping...")
    
    organized_projects = {}
    current_image_num = 1
    
    for project in projects:
        folder_name = project['folder_name']
        
        if folder_name in project_mapping:
            mapping = project_mapping[folder_name]
            year = mapping['year']
            
            if year not in organized_projects:
                organized_projects[year] = []
            
            # Create image range
            start_img = current_image_num
            end_img = current_image_num + project['image_count'] - 1
            image_range = list(range(start_img, end_img + 1))
            
            project_data = {
                'title': mapping['title'],
                'date': mapping['date'],
                'location': mapping['location'],
                'description': f"{mapping['title']} event.",
                'images': image_range,
                'folder_name': folder_name,
                'actual_count': project['image_count']
            }
            
            organized_projects[year].append(project_data)
            
            print(f"  📂 {mapping['title']}: {project['image_count']} images → img{start_img:03d}-img{end_img:03d}")
            
            current_image_num = end_img + 1
        else:
            print(f"  ⚠️  Unmapped folder: {folder_name}")
    
    return organized_projects

def generate_js_projects_constant(organized_projects):
    """Generate the JavaScript projects constant"""
    
    print(f"\n📝 Generating JavaScript projects constant...")
    
    js_output = "const projects = {\n"
    
    for year in sorted(organized_projects.keys()):
        js_output += f'  "{year}": [\n'
        
        for project in organized_projects[year]:
            js_output += f'    {{\n'
            js_output += f'      "title": "{project["title"]}",\n'
            js_output += f'      "date": "{project["date"]}",\n'
            js_output += f'      "location": "{project["location"]}",\n'
            js_output += f'      "description": "{project["description"]}",\n'
            js_output += f'      "images": [\n'
            
            # Format images nicely
            images = project["images"]
            for i in range(0, len(images), 10):
                chunk = images[i:i+10]
                js_output += f'        {", ".join(map(str, chunk))}'
                if i + 10 < len(images):
                    js_output += ','
                js_output += '\n'
            
            js_output += f'      ]\n'
            js_output += f'    }}'
            
            # Add comma if not last project in year
            if project != organized_projects[year][-1]:
                js_output += ','
            js_output += '\n'
        
        js_output += '  ]'
        
        # Add comma if not last year
        if year != sorted(organized_projects.keys())[-1]:
            js_output += ','
        js_output += '\n'
    
    js_output += "};"
    
    return js_output

def main():
    print("🎯 Dynamic Project Mapping with Correct Image Counts")
    print("=" * 60)
    
    # Create the mapping
    organized_projects = create_dynamic_mapping()
    
    # Generate JavaScript
    js_constant = generate_js_projects_constant(organized_projects)
    
    # Save to file
    with open("dynamic_projects_mapping.js", "w") as f:
        f.write(js_constant)
    
    print(f"\n✅ Generated dynamic_projects_mapping.js")
    print(f"📊 Summary:")
    
    total_images = 0
    for year, year_projects in organized_projects.items():
        year_count = sum(len(p['images']) for p in year_projects)
        total_images += year_count
        print(f"  📅 {year}: {len(year_projects)} projects, {year_count} images")
    
    print(f"\n🎯 Total: {total_images} images mapped")
    print(f"📝 Next step: Update index_with_carousel.html with this mapping")

if __name__ == "__main__":
    main()
