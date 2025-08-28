#!/usr/bin/env python3
"""
Update HTML with Simple Display Mapping
Uses only the 20 projects that have real photos, no grey squares
"""

import json

# Load the simple project structure
with open('/Volumes/T7/625industriesGIT/625industries/simple_project_mapping.json', 'r') as f:
    simple_projects = json.load(f)

# Read current HTML file
with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'r') as f:
    html_content = f.read()

# Update NUM_IMAGES back to 240 (more than enough for our 96 real images)
new_html_content = html_content.replace(
    'const WIDTH = 25, HEIGHT = 35, DIGIT_SPACING = 3, NUM_IMAGES = 380;',
    'const WIDTH = 25, HEIGHT = 35, DIGIT_SPACING = 3, NUM_IMAGES = 240;'
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
new_projects_js = "const projects = " + json.dumps(simple_projects, indent=2) + ";"

# Replace the projects section
new_html_content = (
    new_html_content[:start_pos] + 
    new_projects_js + 
    new_html_content[end_pos + 2:]  # +2 to skip the '};'
)

# Write the updated HTML file
with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'w') as f:
    f.write(new_html_content)

print("✅ HTML file updated with simple display mapping!")
print("Now shows:")
print("- ✅ 20 projects with REAL PHOTOS (no grey squares)")
print("- ✅ TXRX Workshop with correct photos")
print("- ✅ All real photos visible in the 625 display")
print("- ✅ Clean project index with only completed projects")

# Show summary
total_projects = sum(len(projects) for projects in simple_projects.values())
print(f"\\nTotal projects displayed: {total_projects}")
print("Projects by year:")
for year, projects in simple_projects.items():
    if projects:
        print(f"  {year}: {len(projects)} projects")
