#!/usr/bin/env python3
"""
Create Complete Project Mapping
Maps ALL 76 projects and creates grey placeholders for missing photos
"""

import json
from pathlib import Path
from PIL import Image

# Load all projects
with open('/Volumes/T7/625industriesGIT/625industries/Archives/projects.json', 'r') as f:
    all_projects = json.load(f)

# Load current mapping to see what we have
with open('/Volumes/T7/625industriesGIT/625industries/image_mapping_corrected.json', 'r') as f:
    current_mapping = json.load(f)

# Get list of mapped project indices
mapped_indices = [info['project_index'] for info in current_mapping.values()]

def create_grey_placeholder(image_num):
    """Create grey placeholder images for missing projects"""
    # Create a grey square
    grey_color = (128, 128, 128)  # Medium grey
    
    resolutions = {
        'low_res': (400, 400, '-low'),
        'small_res': (600, 600, '-small'), 
        'medium_res': (800, 800, '-med'),
        'high_res_1200': (1200, 1200, '-high'),
        'high_res': (2000, 2000, '')
    }
    
    for res_folder, (width, height, suffix) in resolutions.items():
        # Create grey image
        grey_image = Image.new('RGB', (width, height), grey_color)
        
        # Create output path
        output_dir = Path('images') / res_folder
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"img{image_num:03d}{suffix}.jpg"
        
        # Save image
        grey_image.save(output_file, 'JPEG', quality=95)
    
    print(f"Created grey placeholder for image {image_num}")

# Create complete project structure
complete_projects = {
    "2018": [],
    "2019": [], 
    "2020": [],
    "COVID": [],
    "2022": [],
    "2023": [],
    "2024": [],
    "2025": []
}

current_image_num = 1

print("Creating complete project mapping with grey placeholders...")

for i, project in enumerate(all_projects):
    # Determine year/category
    date = project['date']
    year = date[:4]
    
    # Handle special COVID category
    if year in ['2020', '2021']:
        category = "COVID"
    else:
        category = year
    
    # Determine how many images this project should have (5 per project)
    images_per_project = 5
    project_images = list(range(current_image_num, current_image_num + images_per_project))
    
    # Check if we have real photos for this project
    has_real_photos = i in mapped_indices
    
    if not has_real_photos:
        # Create grey placeholders for missing projects
        for img_num in project_images:
            create_grey_placeholder(img_num)
        print(f"  Missing: {project['date']} {project['client']} {project['event']} -> images {project_images[0]}-{project_images[-1]} (grey placeholders)")
    else:
        print(f"  Has photos: {project['date']} {project['client']} {project['event']} -> images {project_images[0]}-{project_images[-1]}")
    
    # Create project entry
    project_entry = {
        "title": project['event'].upper(),
        "date": date.replace('-', '.'),
        "location": project['city'].upper(),
        "description": f"{project['client']} {project['event']} event in {project['city']}.",
        "images": project_images
    }
    
    if category in complete_projects:
        complete_projects[category].append(project_entry)
    
    current_image_num += images_per_project

# Sort projects by date within each year
for year in complete_projects:
    complete_projects[year].sort(key=lambda x: x['date'])

# Save the complete mapping
with open('/Volumes/T7/625industriesGIT/625industries/complete_project_mapping.json', 'w') as f:
    json.dump(complete_projects, f, indent=2)

print(f"\n✅ Complete mapping created!")
print(f"Total projects: {len(all_projects)}")
print(f"Projects with real photos: {len(mapped_indices)}")
print(f"Projects with grey placeholders: {len(all_projects) - len(mapped_indices)}")

# Show summary by year
print("\nProjects by year:")
for year, projects in complete_projects.items():
    if projects:
        print(f"{year}: {len(projects)} projects")
        
print(f"\nNext step: Update HTML file with complete mapping")
