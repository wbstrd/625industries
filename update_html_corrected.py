#!/usr/bin/env python3
"""
Update HTML with Corrected Projects Script
Updates the HTML file with the corrected project mappings including TXRX and NFL Draft
"""

import json

# Load the corrected mapping
with open('/Volumes/T7/625industriesGIT/625industries/image_mapping_corrected.json', 'r') as f:
    corrected_mapping = json.load(f)

# Create new project structure based on corrected mappings
new_projects = {
    "2018": [],
    "2019": [],
    "2020": [],
    "COVID": [],
    "2022": [],
    "2023": [],
    "2024": [],
    "2025": []
}

# Process each mapped project from corrected mapping
for folder_name, mapping_info in corrected_mapping.items():
    project = mapping_info['project']
    images = mapping_info['images']
    
    # Determine year/category
    date = project['date']
    year = date[:4]
    
    # Handle special COVID category
    if year in ['2020', '2021']:
        category = "COVID"
    else:
        category = year
    
    # Create project entry
    project_entry = {
        "title": project['event'].upper(),
        "date": date.replace('-', '.'),
        "location": project['city'].upper(),
        "description": f"{project['client']} {project['event']} event in {project['city']}.",
        "images": images
    }
    
    if category in new_projects:
        new_projects[category].append(project_entry)

# Sort projects by date within each year
for year in new_projects:
    new_projects[year].sort(key=lambda x: x['date'])

# Read current HTML file
with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'r') as f:
    html_content = f.read()

# Find the start of the projects constant
start_marker = 'const projects = {'
end_marker = '};'

start_pos = html_content.find(start_marker)
if start_pos == -1:
    print("Could not find projects constant in HTML file")
    exit(1)

# Find the end of the projects constant
end_pos = html_content.find(end_marker, start_pos)
if end_pos == -1:
    print("Could not find end of projects constant")
    exit(1)

# Create the new projects JavaScript
new_projects_js = "const projects = " + json.dumps(new_projects, indent=2) + ";"

# Replace the projects section
new_html_content = (
    html_content[:start_pos] + 
    new_projects_js + 
    html_content[end_pos + 2:]  # +2 to skip the '};'
)

# Write the updated HTML file
with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'w') as f:
    f.write(new_html_content)

print("✅ HTML file updated with corrected mappings!")
print("Now includes:")
print("- ✅ TXRX Workshop (2025-02-11) with proper images")
print("- ✅ NFL Draft Day (2022-04-27) with proper images") 
print("- ✅ All Star Weekend × Boardroom (2025-02-15) with proper images")
print("- ✅ All previously mapped projects with corrected assignments")

# Show final project count
total_projects = sum(len(projects) for projects in new_projects.values())
print(f"\nTotal projects mapped: {total_projects}")

# Show projects by year
for year, projects in new_projects.items():
    if projects:
        print(f"{year}: {len(projects)} projects")
        for project in projects:
            image_range = f"{project['images'][0]}-{project['images'][-1]}" if len(project['images']) > 1 else str(project['images'][0])
            print(f"  - {project['title']} (images {image_range})")
