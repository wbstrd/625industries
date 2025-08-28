#!/usr/bin/env python3
"""
Restore Complete Project Structure
Shows all 76 projects in the index, with real photos where available
"""

import json

# Load all projects from the canonical source
with open('/Volumes/T7/625industriesGIT/625industries/Archives/projects.json', 'r') as f:
    all_projects = json.load(f)

# Load our photo mappings to see which projects have real photos
with open('/Volumes/T7/625industriesGIT/625industries/image_mapping_corrected.json', 'r') as f:
    photo_mappings = json.load(f)

# Create a lookup of which projects have photos
projects_with_photos = {}
for folder_name, mapping_info in photo_mappings.items():
    project_index = mapping_info['project_index']
    projects_with_photos[project_index] = mapping_info['images']

print(f"Found {len(projects_with_photos)} projects with real photos")

# Create the complete project structure
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

# Current image number for projects without photos
placeholder_image_start = 100  # Start placeholders after our real photos

# Process all projects
for i, project in enumerate(all_projects):
    date = project['date']
    year = date[:4]
    
    # Determine category
    if year in ['2020', '2021']:
        category = "COVID"
    else:
        category = year
    
    # Check if this project has real photos
    if i in projects_with_photos:
        # Use real photos
        images = projects_with_photos[i]
        print(f"✅ {project['event']} - Using real photos: {images}")
    else:
        # Use placeholder numbers (these won't have actual image files)
        images = [placeholder_image_start, placeholder_image_start + 1, placeholder_image_start + 2]
        placeholder_image_start += 5  # Space them out
        print(f"📝 {project['event']} - Listed without photos")
    
    project_entry = {
        "title": project['event'].upper(),
        "date": date.replace('-', '.'),
        "location": project['city'].upper(),
        "description": f"{project['client']} {project['event']} event in {project['city']}.",
        "images": images
    }
    
    if category in complete_projects:
        complete_projects[category].append(project_entry)

# Sort by date within each year
for year in complete_projects:
    complete_projects[year].sort(key=lambda x: x['date'])

# Save the complete structure
with open('/Volumes/T7/625industriesGIT/625industries/complete_project_structure.json', 'w') as f:
    json.dump(complete_projects, f, indent=2)

print("\\n" + "="*60)
print("✅ COMPLETE PROJECT STRUCTURE CREATED")
print("="*60)

total_projects = sum(len(projects) for projects in complete_projects.values())
projects_with_real_photos = len(projects_with_photos)
projects_listed_only = total_projects - projects_with_real_photos

print(f"📊 SUMMARY:")
print(f"   Total projects listed: {total_projects}")
print(f"   Projects with real photos: {projects_with_real_photos}")
print(f"   Projects listed without photos: {projects_listed_only}")

print(f"\\n📅 BREAKDOWN BY YEAR:")
for year, projects in complete_projects.items():
    if projects:
        with_photos = sum(1 for p in projects if any(img < 100 for img in p['images']))
        without_photos = len(projects) - with_photos
        print(f"   {year}: {len(projects)} projects ({with_photos} with photos, {without_photos} listed only)")

print(f"\\n💡 RESULT:")
print(f"   - All 76 projects will appear in the project index")
print(f"   - Projects with photos will show real images when clicked")
print(f"   - Projects without photos will be listed but won't show images")
print(f"   - The '625' display will use the first ~93 real photos")
