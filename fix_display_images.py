#!/usr/bin/env python3
"""
Fix Display Images - Move real photos to positions 1-93 so they show in the 625 display
"""

import json
import shutil
from pathlib import Path

# Load the current mapping
with open('/Volumes/T7/625industriesGIT/625industries/image_mapping_corrected.json', 'r') as f:
    current_mapping = json.load(f)

def move_photos_to_display_range():
    """Move real photos from high positions back to 1-93 range for the 625 display"""
    
    # Collect all our real photo positions 
    real_photo_positions = []
    for folder_name, mapping_info in current_mapping.items():
        old_images = mapping_info['images']
        real_photo_positions.extend(old_images)
    
    print(f"Found {len(real_photo_positions)} real photos to move to display range")
    
    # The 625 display uses approximately positions 1-93
    # Let's move our real photos to fill those positions
    display_positions = list(range(1, 94))  # positions 1-93
    
    # Map old positions to new display positions
    position_mapping = {}
    for i, old_pos in enumerate(real_photo_positions[:93]):  # Take first 93 real photos
        new_pos = display_positions[i]
        position_mapping[old_pos] = new_pos
    
    print("Moving photos to display positions:")
    
    # Move the actual image files
    for old_pos, new_pos in position_mapping.items():
        print(f"  Moving img{old_pos:03d} -> img{new_pos:03d}")
        
        resolutions = ['low_res', 'small_res', 'medium_res', 'high_res_1200', 'high_res']
        suffixes = ['-low', '-small', '-med', '-high', '']
        
        for res_folder, suffix in zip(resolutions, suffixes):
            old_path = Path(f'images/{res_folder}/img{old_pos:03d}{suffix}.jpg')
            new_path = Path(f'images/{res_folder}/img{new_pos:03d}{suffix}.jpg')
            
            if old_path.exists():
                # Copy to new position
                shutil.copy2(old_path, new_path)
    
    return position_mapping

def update_project_mapping_for_display(position_mapping):
    """Update the project structure to reflect new positions for the 625 display"""
    
    # Load all projects
    with open('/Volumes/T7/625industriesGIT/625industries/Archives/projects.json', 'r') as f:
        all_projects = json.load(f)
    
    # Create a simplified structure that prioritizes real photos for the display
    display_projects = {
        "2018": [],
        "2019": [], 
        "2020": [],
        "COVID": [],
        "2022": [],
        "2023": [],
        "2024": [],
        "2025": []
    }
    
    # First, map our real photos to display positions
    current_display_pos = 1
    for folder_name, mapping_info in current_mapping.items():
        project_index = mapping_info['project_index']
        project = all_projects[project_index]
        old_images = mapping_info['images']
        
        # Assign new display positions
        num_images = len(old_images)
        new_images = list(range(current_display_pos, current_display_pos + num_images))
        current_display_pos += num_images
        
        # Determine year/category
        date = project['date']
        year = date[:4]
        if year in ['2020', '2021']:
            category = "COVID"
        else:
            category = year
        
        project_entry = {
            "title": project['event'].upper(),
            "date": date.replace('-', '.'),
            "location": project['city'].upper(),
            "description": f"{project['client']} {project['event']} event in {project['city']}.",
            "images": new_images
        }
        
        if category in display_projects:
            display_projects[category].append(project_entry)
    
    # Sort by date
    for year in display_projects:
        display_projects[year].sort(key=lambda x: x['date'])
    
    return display_projects

print("Step 1: Moving real photos to display range (1-93)...")
position_mapping = move_photos_to_display_range()

print("\\nStep 2: Creating display-optimized project structure...")
display_projects = update_project_mapping_for_display(position_mapping)

print("\\nStep 3: Saving display mapping...")
with open('/Volumes/T7/625industriesGIT/625industries/display_project_mapping.json', 'w') as f:
    json.dump(display_projects, f, indent=2)

print("\\n✅ Display images fixed!")
print("Real photos are now in positions 1-93 and will show up in the 625 display")
print(f"Total projects with photos: {sum(len(projects) for projects in display_projects.values())}")

for year, projects in display_projects.items():
    if projects:
        print(f"{year}: {len(projects)} projects")
