#!/usr/bin/env python3
"""
Correct photo mapping - map actual wetransfer photos to their proper projects
"""

import os
import shutil
from PIL import Image
from pillow_heif import register_heif_opener

# Enable HEIC support
register_heif_opener()

def create_quality_resize(source_path, target_path, target_size):
    """Create a high-quality resized version of an image"""
    try:
        with Image.open(source_path) as img:
            # Convert HEIC to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate aspect ratio preserving resize
            img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
            
            # Save with high quality
            img.save(target_path, 'JPEG', quality=95, optimize=True)
            return True
    except Exception as e:
        print(f"    ❌ Error processing {source_path}: {e}")
        return False

def get_wetransfer_folders():
    """Get all wetransfer project folders with their photos"""
    wetransfer_base = "/Volumes/T7"
    projects = {}
    
    print("🔍 Scanning wetransfer folders...")
    
    # Find all wetransfer folders
    for root, dirs, files in os.walk(wetransfer_base):
        if "wetransfer" in root.lower():
            for dir_name in dirs:
                if dir_name.startswith('.'):
                    continue
                    
                full_path = os.path.join(root, dir_name)
                
                # Count and collect image files
                image_files = []
                try:
                    for f in os.listdir(full_path):
                        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic')):
                            image_files.append(f)
                except:
                    continue
                
                if len(image_files) > 0:
                    projects[dir_name] = {
                        'path': full_path,
                        'files': sorted(image_files),
                        'count': len(image_files)
                    }
                    print(f"  📁 {dir_name}: {len(image_files)} images")
    
    return projects

def get_current_projects_from_html():
    """Extract current project structure from HTML"""
    print("\n📊 Reading current project structure...")
    
    with open("index_with_carousel.html", "r") as f:
        content = f.read()
    
    # Find projects constant
    projects_start = content.find('const projects = {')
    if projects_start == -1:
        print("❌ Could not find projects constant")
        return {}
    
    # Find closing brace
    brace_count = 0
    projects_end = projects_start
    for i, char in enumerate(content[projects_start:], projects_start):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                projects_end = i + 1
                break
    
    projects_str = content[projects_start:projects_end]
    
    # Parse manually to extract project info
    projects = {}
    lines = projects_str.split('\n')
    current_year = None
    current_project = None
    in_images = False
    
    for line in lines:
        line = line.strip()
        
        # Year detection
        if '"' in line and ':' in line and len(line.split('"')[1]) == 4:
            try:
                year = line.split('"')[1]
                if year.isdigit():
                    current_year = year
                    projects[current_year] = []
                    continue
            except:
                pass
        
        # Project title
        if '"title":' in line:
            title = line.split('"')[3]
            current_project = {'title': title}
            continue
        
        # Date
        if '"date":' in line and current_project:
            date = line.split('"')[3]
            current_project['date'] = date
            continue
        
        # Location 
        if '"location":' in line and current_project:
            location = line.split('"')[3]
            current_project['location'] = location
            continue
        
        # Description
        if '"description":' in line and current_project:
            description = line.split('"')[3]
            current_project['description'] = description
            continue
        
        # Images array
        if '"images":' in line:
            in_images = True
            current_project['original_images'] = []
            continue
        
        if in_images:
            if ']' in line:
                in_images = False
                if current_project and current_year:
                    projects[current_year].append(current_project)
                    current_project = None
                continue
            
            # Extract numbers from line
            import re
            numbers = re.findall(r'\b(\d+)\b', line)
            if numbers and current_project:
                current_project['original_images'].extend([int(n) for n in numbers])
    
    return projects

def create_folder_to_project_mapping():
    """Create mapping between wetransfer folders and projects"""
    return {
        'December 2018 - Maker\'s Studio Nike': 'MAKERS STUDIO',
        'October 2018 Nike Maker\'s Space': 'MAKERS STUDIO',
        'LA 2022 Levi\'s House': 'LEVI\'S HOUSE × DAISY WORLD',
        'LA Billie Eillish Nike Activation': 'BILLIE EILISH × NIKE (UPCYCLE)',
        'Levi\'s x Come Watts LA': 'LEVI\'S × COME',
        'NFL Draft Vegas 2022': 'NFL DRAFT DAY',
        'July 2022 Baseball Allstar NikeByYou': 'MLB NIKEBYYOU',
        'Arizona February 2023 Undefeated': 'SUPER BOWL LVII × UNDFTD',
        'Phoenix Superbowl NikeByYou February 2023': 'NIKEBYYOU – SUPER BOWL',
        'Rolling Loud 2023 March Levi\'s': 'ROLLING LOUD × LEVI\'S',
        'Photos 501 Day Levi\'s SF': 'LEVI\'S 501 DAY',
        'July 2023 Rolling Loud Levi\'s': 'ROLLING LOUD × LEVI\'S',
        'Tea Room July 2023 Nike': 'NIKE TEA ROOM',
        'February 2024 Superbowl Vegas': 'SUPER BOWL LVIII NIKEBYYOU',
        'Modelo Rolling Loud LA March': 'ROLLING LOUD × MODELO',
        'Vegas Modelo Kick Off - 2024': 'VEGAS KICK OFF',
        'Photos for TXRX Nike': 'TXRX WORKSHOP',
        'Photos for Boardroom Brunch': 'ALL STAR WEEKEND × BOARDROOM',
        'LA 2017 All Star': 'LA ALL STAR'
    }

def copy_project_photos(wetransfer_folders, html_projects, folder_mapping):
    """Copy photos from wetransfer folders to match HTML project structure"""
    
    print(f"\n🔄 Copying photos to match project structure...")
    
    # Resolution configurations
    resolutions = {
        'low_res': (200, '-low'),
        'small_res': (400, '-small'), 
        'medium_res': (800, '-med'),
        'high_res_1200': (1200, '-high'),
        'high_res': (2400, '')
    }
    
    updated_projects = {}
    
    for year, year_projects in html_projects.items():
        updated_projects[year] = []
        
        print(f"\n📅 Processing {year}...")
        
        for project in year_projects:
            project_title = project['title']
            original_images = project['original_images']
            
            print(f"  📂 {project_title} (currently {len(original_images)} images)")
            
            # Find matching wetransfer folder
            matching_folder = None
            for folder_name, folder_title in folder_mapping.items():
                if folder_title == project_title:
                    matching_folder = folder_name
                    break
            
            if not matching_folder or matching_folder not in wetransfer_folders:
                print(f"    ⚠️  No wetransfer folder found, keeping original")
                updated_projects[year].append(project)
                continue
            
            # Get photos from wetransfer folder
            folder_data = wetransfer_folders[matching_folder]
            actual_photo_count = folder_data['count']
            
            print(f"    📁 Found {actual_photo_count} photos in {matching_folder}")
            
            # Copy photos to the original image positions
            images_to_use = original_images[:actual_photo_count]  # Use original positions
            
            for i, source_file in enumerate(folder_data['files']):
                if i >= len(images_to_use):
                    break
                    
                img_num = images_to_use[i]
                source_path = os.path.join(folder_data['path'], source_file)
                
                print(f"    📋 img{img_num:03d} ← {source_file}")
                
                # Create all resolution versions
                for res_folder, (size, suffix) in resolutions.items():
                    target_dir = f"images/{res_folder}"
                    os.makedirs(target_dir, exist_ok=True)
                    
                    target_file = f"img{img_num:03d}{suffix}.jpg"
                    target_path = os.path.join(target_dir, target_file)
                    
                    create_quality_resize(source_path, target_path, size)
            
            # Update project with actual photo count
            updated_project = project.copy()
            updated_project['images'] = images_to_use
            updated_projects[year].append(updated_project)
    
    return updated_projects

def generate_updated_js(updated_projects):
    """Generate updated JavaScript projects constant"""
    
    js_output = "const projects = {\n"
    
    for year in sorted(updated_projects.keys()):
        js_output += f'  "{year}": [\n'
        
        for project in updated_projects[year]:
            js_output += f'    {{\n'
            js_output += f'      "title": "{project["title"]}",\n'
            js_output += f'      "date": "{project["date"]}",\n'
            js_output += f'      "location": "{project["location"]}",\n'
            js_output += f'      "description": "{project["description"]}",\n'
            js_output += f'      "images": [\n'
            
            # Format images
            images = project["images"]
            for i in range(0, len(images), 10):
                chunk = images[i:i+10]
                js_output += f'        {", ".join(map(str, chunk))}'
                if i + 10 < len(images):
                    js_output += ','
                js_output += '\n'
            
            js_output += f'      ]\n'
            js_output += f'    }}'
            
            if project != updated_projects[year][-1]:
                js_output += ','
            js_output += '\n'
        
        js_output += '  ]'
        if year != sorted(updated_projects.keys())[-1]:
            js_output += ','
        js_output += '\n'
    
    js_output += "};"
    
    return js_output

def main():
    print("🎯 CORRECT PHOTO MAPPING")
    print("=" * 50)
    
    # Get wetransfer folders
    wetransfer_folders = get_wetransfer_folders()
    
    # Get current HTML projects
    html_projects = get_current_projects_from_html()
    
    # Create mapping
    folder_mapping = create_folder_to_project_mapping()
    
    # Copy photos correctly
    updated_projects = copy_project_photos(wetransfer_folders, html_projects, folder_mapping)
    
    # Generate updated JavaScript
    updated_js = generate_updated_js(updated_projects)
    
    # Save
    with open("correctly_mapped_projects.js", "w") as f:
        f.write(updated_js)
    
    print(f"\n✅ Generated correctly_mapped_projects.js")
    print(f"📝 Next: Update HTML with this mapping")

if __name__ == "__main__":
    main()
