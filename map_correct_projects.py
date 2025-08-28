#!/usr/bin/env python3
"""
Map Correct Projects to Images
Create proper mapping between WeTransfer project folders and image numbers
"""

import json
import shutil
import os
from pathlib import Path
from PIL import Image

# Paths
WETRANSFER_PATH = "/Volumes/T7/wetransfer_arizona-february-2023-undefeated_2025-05-29_0306"
BACKUP_625_PATH = "/Volumes/T7/625"

def create_quality_resize(input_path, output_path, target_size):
    """Create high-quality resize"""
    try:
        with Image.open(input_path) as img:
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize maintaining aspect ratio
            img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
            img.save(output_path, 'JPEG', quality=95, optimize=True)
            return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def get_project_photos(folder_name):
    """Get JPG/JPEG photos from a project folder"""
    folder_path = Path(WETRANSFER_PATH) / folder_name
    if not folder_path.exists():
        print(f"Folder not found: {folder_path}")
        return []
    
    # Get JPG/JPEG files only (skip HEIC for now)
    photo_extensions = {'.jpg', '.jpeg'}
    photos = []
    
    for file_path in folder_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in photo_extensions:
            photos.append(file_path)
    
    # Sort by name
    photos.sort(key=lambda x: x.name.lower())
    return photos

def create_project_mapping():
    """Map WeTransfer projects to correct image numbers"""
    
    # Correct mapping based on WeTransfer folders
    project_mapping = {
        # 2018 Projects
        "December 2018 - Maker's Studio Nike": {
            "title": "MAKERS STUDIO",
            "date": "2018.12.01",
            "location": "LOS ANGELES",
            "description": "Nike Makers Studio creative workshop in Los Angeles.",
            "images": [1, 2, 3, 4, 5]
        },
        "October 2018 Nike Maker's Space": {
            "title": "MAKERS STUDIO",
            "date": "2018.10.01",
            "location": "LOS ANGELES", 
            "description": "Nike Makers Studio October session in Los Angeles.",
            "images": [6, 7, 8, 9, 10]
        },
        
        # 2022 Projects
        "LA 2022 Levi's House": {
            "title": "LEVI'S HOUSE",
            "date": "2022.02.01",
            "location": "LOS ANGELES",
            "description": "Levi's House activation in Los Angeles.",
            "images": [11, 12, 13, 14, 15]
        },
        "LA Billie Eillish Nike Activation": {
            "title": "BILLIE EILISH × NIKE",
            "date": "2022.04.01",
            "location": "LOS ANGELES",
            "description": "Billie Eilish Nike upcycle activation in Los Angeles.",
            "images": [16, 17, 18, 19, 20]
        },
        "Levi's x Come Watts LA": {
            "title": "LEVI'S × COME WATTS",
            "date": "2022.06.01",
            "location": "LOS ANGELES",
            "description": "Levi's x Come collaboration in Watts, Los Angeles.",
            "images": [21, 22, 23, 24, 25]
        },
        "NFL Draft Vegas 2022": {
            "title": "NFL DRAFT VEGAS",
            "date": "2022.04.28",
            "location": "LAS VEGAS",
            "description": "NFL Draft experience in Las Vegas.",
            "images": [26, 27, 28, 29, 30]
        },
        "July 2022 Baseball Allstar NikeByYou": {
            "title": "MLB NIKEBYYOU",
            "date": "2022.07.19",
            "location": "LOS ANGELES",
            "description": "MLB All-Star NikeByYou customization experience.",
            "images": [31, 32, 33, 34, 35]
        },
        
        # 2023 Projects
        "Arizona February 2023 Undefeated": {
            "title": "SUPER BOWL LVII × UNDFTD",
            "date": "2023.02.12",
            "location": "PHOENIX",
            "description": "Super Bowl LVII Undefeated activation in Phoenix.",
            "images": [36, 37, 38, 39, 40]
        },
        "Phoenix Superbowl NikeByYou February 2023": {
            "title": "NIKEBYYOU – SUPER BOWL",
            "date": "2023.02.12",
            "location": "PHOENIX",
            "description": "Super Bowl LVII NikeByYou experience in Phoenix.",
            "images": [41, 42, 43, 44, 45]
        },
        "Rolling Loud 2023 March Levi's": {
            "title": "ROLLING LOUD × LEVI'S",
            "date": "2023.03.03",
            "location": "MIAMI",
            "description": "Rolling Loud Miami Levi's activation.",
            "images": [46, 47, 48, 49, 50]
        },
        "Photos 501 Day Levi's SF": {
            "title": "LEVI'S 501 DAY",
            "date": "2023.05.20",
            "location": "SAN FRANCISCO",
            "description": "Levi's 501 Day celebration in San Francisco.",
            "images": [51, 52, 53, 54, 55]
        },
        "July 2023 Rolling Loud Levi's": {
            "title": "ROLLING LOUD × LEVI'S",
            "date": "2023.07.21",
            "location": "MIAMI",
            "description": "Rolling Loud July Levi's collaboration.",
            "images": [56, 57, 58, 59, 60]
        },
        "Tea Room July 2023 Nike": {
            "title": "NIKE TEA ROOM",
            "date": "2023.07.15",
            "location": "LOS ANGELES",
            "description": "Nike Tea Room experience in Los Angeles.",
            "images": [61, 62, 63, 64, 65]
        },
        
        # 2024 Projects
        "February 2024 Superbowl Vegas": {
            "title": "SUPER BOWL LVIII NIKEBYYOU",
            "date": "2024.02.11",
            "location": "LAS VEGAS",
            "description": "Super Bowl LVIII NikeByYou activation in Las Vegas.",
            "images": [66, 67, 68, 69, 70]
        },
        "Modelo Rolling Loud LA March": {
            "title": "ROLLING LOUD × MODELO",
            "date": "2024.03.22",
            "location": "LOS ANGELES",
            "description": "Modelo Rolling Loud LA activation.",
            "images": [71, 72, 73, 74, 75]
        },
        "Vegas Modelo Kick Off - 2024": {
            "title": "VEGAS KICK OFF",
            "date": "2024.09.14",
            "location": "LAS VEGAS",
            "description": "Vegas Modelo Kick Off event.",
            "images": [76, 77, 78, 79, 80]
        },
        
        # 2025 Projects
        "Photos for TXRX Nike": {
            "title": "TXRX WORKSHOP",
            "date": "2025.02.11",
            "location": "HOUSTON",
            "description": "Nike TXRX Workshop event in Houston.",
            "images": [81, 82, 83, 84, 85]
        },
        "Photos for Boardroom Brunch": {
            "title": "ALL STAR WEEKEND × BOARDROOM",
            "date": "2025.02.15",
            "location": "SAN FRANCISCO",
            "description": "NBA All-Star Weekend Boardroom event in San Francisco.",
            "images": [86, 87, 88, 89, 90]
        },
        "LA 2017 All Star": {
            "title": "LA ALL STAR",
            "date": "2017.02.18",
            "location": "LOS ANGELES",
            "description": "NBA All-Star Weekend activation in Los Angeles.",
            "images": [91, 92, 93, 94, 95]
        }
    }
    
    return project_mapping

def copy_project_photos():
    """Copy actual project photos to correct numbered positions"""
    
    print("🔄 MAPPING CORRECT PROJECT PHOTOS")
    print("=" * 60)
    
    project_mapping = create_project_mapping()
    
    resolutions = {
        'low_res': (200, '-low'),
        'small_res': (400, '-small'),
        'medium_res': (800, '-med'),
        'high_res_1200': (1200, '-high'),
        'high_res': (2000, '')
    }
    
    total_copied = 0
    
    for folder_name, project_info in project_mapping.items():
        print(f"\\n📁 Processing: {folder_name}")
        
        # Get photos from WeTransfer folder
        project_photos = get_project_photos(folder_name)
        target_images = project_info['images']
        
        if not project_photos:
            print(f"   ⚠️  No JPG photos found, trying 625 backup...")
            # Fallback to 625 backup for this project
            for i, img_num in enumerate(target_images):
                backup_path = Path(BACKUP_625_PATH) / f"img{img_num:03d}.jpg"
                if backup_path.exists():
                    print(f"   🔄 Using backup img{img_num:03d}")
                    for res_folder, (size, suffix) in resolutions.items():
                        target_filename = f"img{img_num:03d}{suffix}.jpg"
                        target_path = Path(f"images/{res_folder}/{target_filename}")
                        create_quality_resize(backup_path, target_path, size)
                        total_copied += 1
            continue
        
        print(f"   📸 Found {len(project_photos)} photos")
        print(f"   🎯 Target positions: {target_images}")
        
        # Copy photos to target positions
        for i, target_img_num in enumerate(target_images):
            if i < len(project_photos):
                source_photo = project_photos[i]
                print(f"   📋 img{target_img_num:03d} ← {source_photo.name}")
                
                # Create all resolution versions
                for res_folder, (size, suffix) in resolutions.items():
                    target_filename = f"img{target_img_num:03d}{suffix}.jpg"
                    target_path = Path(f"images/{res_folder}/{target_filename}")
                    
                    if create_quality_resize(source_photo, target_path, size):
                        total_copied += 1
            else:
                # Use backup if we don't have enough project photos
                backup_path = Path(BACKUP_625_PATH) / f"img{target_img_num:03d}.jpg"
                if backup_path.exists():
                    print(f"   🔄 Using backup for img{target_img_num:03d}")
                    for res_folder, (size, suffix) in resolutions.items():
                        target_filename = f"img{target_img_num:03d}{suffix}.jpg"
                        target_path = Path(f"images/{res_folder}/{target_filename}")
                        create_quality_resize(backup_path, target_path, size)
                        total_copied += 1
    
    print(f"\\n✅ PROJECT PHOTO MAPPING COMPLETE!")
    print(f"📊 Total image files processed: {total_copied}")
    return project_mapping

def update_html_with_correct_mapping():
    """Update HTML with correctly mapped projects"""
    
    project_mapping = create_project_mapping()
    
    # Organize by year
    projects_by_year = {
        "2017": [],
        "2018": [],
        "2022": [],
        "2023": [],
        "2024": [],
        "2025": []
    }
    
    for folder_name, project_info in project_mapping.items():
        year = project_info['date'][:4]
        if year in projects_by_year:
            projects_by_year[year].append(project_info)
    
    # Sort by date within each year
    for year in projects_by_year:
        projects_by_year[year].sort(key=lambda x: x['date'])
    
    # Read current HTML
    with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'r') as f:
        html_content = f.read()
    
    # Find and replace the projects constant
    start_marker = 'const projects = {'
    end_marker = '};'
    
    start_pos = html_content.find(start_marker)
    end_pos = html_content.find(end_marker, start_pos)
    
    if start_pos == -1 or end_pos == -1:
        print("Could not find projects constant in HTML file")
        return False
    
    # Create the new projects JavaScript
    new_projects_js = "const projects = " + json.dumps(projects_by_year, indent=2) + ";"
    
    # Replace the projects section
    new_html_content = (
        html_content[:start_pos] + 
        new_projects_js + 
        html_content[end_pos + 2:]
    )
    
    # Write the updated HTML file
    with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'w') as f:
        f.write(new_html_content)
    
    return True

if __name__ == "__main__":
    # First copy the correct photos
    copy_project_photos()
    
    # Then update the HTML
    if update_html_with_correct_mapping():
        print("\\n🎯 HTML UPDATED WITH CORRECT PROJECT MAPPING!")
        print("✅ Projects now show their actual photos!")
    else:
        print("\\n❌ Failed to update HTML")
