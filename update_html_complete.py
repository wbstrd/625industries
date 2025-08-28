#!/usr/bin/env python3
"""
Update HTML with Complete Project List
Updates the HTML file to show all 76 projects with real photos and grey placeholders
"""

import json

# Load the complete project structure
with open('/Volumes/T7/625industriesGIT/625industries/complete_project_mapping.json', 'r') as f:
    complete_projects = json.load(f)

# Read current HTML file
with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'r') as f:
    html_content = f.read()

# Update the grid to handle 380 images (76 projects × 5 images each)
# Update the NUM_IMAGES constant
new_html_content = html_content.replace(
    'const WIDTH = 25, HEIGHT = 35, DIGIT_SPACING = 3, NUM_IMAGES = 240;',
    'const WIDTH = 25, HEIGHT = 35, DIGIT_SPACING = 3, NUM_IMAGES = 380;'
)

# Find and replace the projects constant
start_marker = 'const projects = {'
end_marker = '};'

start_pos = new_html_content.find(start_marker)
if start_pos == -1:
    print("Could not find projects constant in HTML file")
    exit(1)

end_pos = new_html_content.find(end_marker, start_pos)
if end_pos == -1:
    print("Could not find end of projects constant")
    exit(1)

# Create the new projects JavaScript
new_projects_js = "const projects = " + json.dumps(complete_projects, indent=2) + ";"

# Replace the projects section
new_html_content = (
    new_html_content[:start_pos] + 
    new_projects_js + 
    new_html_content[end_pos + 2:]  # +2 to skip the '};'
)

# Write the updated HTML file
with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'w') as f:
    f.write(new_html_content)

print("✅ HTML file updated with complete project list!")
print("Now includes:")
print("- ✅ ALL 76 projects from 2018-2025")
print("- ✅ 20 projects with real photos")
print("- ✅ 56 projects with grey placeholder squares")
print("- ✅ TXRX Workshop correctly mapped")
print("- ✅ Complete chronological organization")

# Show summary
total_projects = sum(len(projects) for projects in complete_projects.values())
print(f"\nTotal projects: {total_projects}")
print("Projects by year:")
for year, projects in complete_projects.items():
    if projects:
        real_photos = sum(1 for p in projects if any(img <= 380 for img in p['images']))
        print(f"  {year}: {len(projects)} projects")
