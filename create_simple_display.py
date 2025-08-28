#!/usr/bin/env python3
"""
Create Simple Display Mapping
Use the real photos we have in positions 1-96 for the 625 display
"""

import json

# Load the corrected mapping to see what we have
with open('/Volumes/T7/625industriesGIT/625industries/image_mapping_corrected.json', 'r') as f:
    current_mapping = json.load(f)

# Load all projects
with open('/Volumes/T7/625industriesGIT/625industries/Archives/projects.json', 'r') as f:
    all_projects = json.load(f)

# Create a simple project structure using our existing photos
simple_projects = {
    "2018": [],
    "2019": [],
    "2020": [],
    "COVID": [],
    "2022": [],
    "2023": [],
    "2024": [],
    "2025": []
}

# Map our existing projects that have photos
for folder_name, mapping_info in current_mapping.items():
    project_index = mapping_info['project_index'] 
    project = all_projects[project_index]
    images = mapping_info['images']
    
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
        "images": images
    }
    
    if category in simple_projects:
        simple_projects[category].append(project_entry)

# Sort by date
for year in simple_projects:
    simple_projects[year].sort(key=lambda x: x['date'])

# Save the simple mapping
with open('/Volumes/T7/625industriesGIT/625industries/simple_project_mapping.json', 'w') as f:
    json.dump(simple_projects, f, indent=2)

print("✅ Simple display mapping created!")
print("This uses only the projects that have real photos")

total_projects = sum(len(projects) for projects in simple_projects.values())
print(f"Total projects with photos: {total_projects}")

print("\\nProjects by year:")
for year, projects in simple_projects.items():
    if projects:
        print(f"  {year}: {len(projects)} projects")
        for project in projects:
            image_range = f"{project['images'][0]}-{project['images'][-1]}" if len(project['images']) > 1 else str(project['images'][0])
            print(f"    - {project['title']} (images {image_range})")
