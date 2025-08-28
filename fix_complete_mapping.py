#!/usr/bin/env python3
"""
Fix Complete Mapping - Preserve existing photos and add grey placeholders only for missing ones
"""

import json
import shutil
from pathlib import Path
from PIL import Image

# Load projects and current mapping
with open('/Volumes/T7/625industriesGIT/625industries/Archives/projects.json', 'r') as f:
    all_projects = json.load(f)

with open('/Volumes/T7/625industriesGIT/625industries/image_mapping_corrected.json', 'r') as f:
    current_mapping = json.load(f)

def copy_existing_photos_to_new_positions():
    """Copy our existing good photos to their correct positions in the complete system"""
    
    # Map project indices to their new positions
    project_position_map = {}
    for i, project in enumerate(all_projects):
        # Each project gets 5 images starting at position (i * 5) + 1
        start_pos = (i * 5) + 1
        project_position_map[i] = list(range(start_pos, start_pos + 5))
    
    # Copy existing photos to new positions
    for folder_name, mapping_info in current_mapping.items():
        project_index = mapping_info['project_index']
        old_images = mapping_info['images']
        new_positions = project_position_map[project_index]
        
        print(f"Moving {folder_name}: {old_images} -> {new_positions}")
        
        # Copy each image from old position to new position
        for old_img, new_img in zip(old_images, new_positions):
            resolutions = ['low_res', 'small_res', 'medium_res', 'high_res_1200', 'high_res']
            suffixes = ['-low', '-small', '-med', '-high', '']
            
            for res_folder, suffix in zip(resolutions, suffixes):
                old_path = Path(f'images/{res_folder}/img{old_img:03d}{suffix}.jpg')
                new_path = Path(f'images/{res_folder}/img{new_img:03d}{suffix}.jpg')
                
                if old_path.exists():
                    shutil.copy2(old_path, new_path)
                    print(f"  Copied {old_path} -> {new_path}")

def create_grey_placeholder(image_num):
    """Create grey placeholder for missing project"""
    grey_color = (128, 128, 128)
    
    resolutions = {
        'low_res': (400, 400, '-low'),
        'small_res': (600, 600, '-small'),
        'medium_res': (800, 800, '-med'), 
        'high_res_1200': (1200, 1200, '-high'),
        'high_res': (2000, 2000, '')
    }
    
    for res_folder, (width, height, suffix) in resolutions.items():
        grey_image = Image.new('RGB', (width, height), grey_color)
        output_dir = Path('images') / res_folder
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"img{image_num:03d}{suffix}.jpg"
        grey_image.save(output_file, 'JPEG', quality=95)

def create_complete_project_structure():
    """Create complete project structure for HTML"""
    complete_projects = {
        "2018": [], "2019": [], "2020": [], "COVID": [], 
        "2022": [], "2023": [], "2024": [], "2025": []
    }
    
    mapped_indices = [info['project_index'] for info in current_mapping.values()]
    
    for i, project in enumerate(all_projects):
        date = project['date']
        year = date[:4]
        
        if year in ['2020', '2021']:
            category = "COVID"
        else:
            category = year
            
        # Each project gets 5 images
        start_pos = (i * 5) + 1
        project_images = list(range(start_pos, start_pos + 5))
        
        # Create grey placeholders for missing projects
        if i not in mapped_indices:
            for img_num in project_images:
                # Only create if doesn't exist
                low_res_path = Path(f'images/low_res/img{img_num:03d}-low.jpg')
                if not low_res_path.exists():
                    create_grey_placeholder(img_num)
            print(f"Grey placeholders: {project['date']} {project['event']} -> images {project_images[0]}-{project_images[-1]}")
        else:
            print(f"Has photos: {project['date']} {project['event']} -> images {project_images[0]}-{project_images[-1]}")
        
        project_entry = {
            "title": project['event'].upper(),
            "date": date.replace('-', '.'),
            "location": project['city'].upper(),
            "description": f"{project['client']} {project['event']} event in {project['city']}.",
            "images": project_images
        }
        
        if category in complete_projects:
            complete_projects[category].append(project_entry)
    
    # Sort by date
    for year in complete_projects:
        complete_projects[year].sort(key=lambda x: x['date'])
    
    return complete_projects

print("Step 1: Copying existing photos to correct positions...")
copy_existing_photos_to_new_positions()

print("\nStep 2: Creating complete project structure...")
complete_projects = create_complete_project_structure()

print("\nStep 3: Saving complete mapping...")
with open('/Volumes/T7/625industriesGIT/625industries/complete_project_mapping.json', 'w') as f:
    json.dump(complete_projects, f, indent=2)

print("\n✅ Fixed complete mapping created!")
print(f"Total projects: {len(all_projects)}")

# Show summary
mapped_indices = [info['project_index'] for info in current_mapping.values()]
print(f"Projects with real photos: {len(mapped_indices)}")
print(f"Projects with grey placeholders: {len(all_projects) - len(mapped_indices)}")

for year, projects in complete_projects.items():
    if projects:
        print(f"{year}: {len(projects)} projects")
