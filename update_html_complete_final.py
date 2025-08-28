#!/usr/bin/env python3
"""
Update HTML with Complete Project Structure
All 76 projects listed, real photos where available, placeholder numbers for others
"""

import json

# Load the complete project structure
with open('/Volumes/T7/625industriesGIT/625industries/complete_project_structure.json', 'r') as f:
    complete_projects = json.load(f)

# Read current HTML file
with open('/Volumes/T7/625industriesGIT/625industries/index.html', 'r') as f:
    html_content = f.read()

# Update NUM_IMAGES to a reasonable number (covers our real photos + some buffer)
new_html_content = html_content.replace(
    'const WIDTH = 25, HEIGHT = 35, DIGIT_SPACING = 3, NUM_IMAGES = 240;',
    'const WIDTH = 25, HEIGHT = 35, DIGIT_SPACING = 3, NUM_IMAGES = 150;'
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

print("✅ HTML UPDATED WITH COMPLETE PROJECT STRUCTURE!")
print("="*60)

total_projects = sum(len(projects) for projects in complete_projects.values())
print(f"📋 ALL {total_projects} PROJECTS NOW LISTED IN INDEX")

print(f"\\n🎯 WHAT YOU'LL SEE:")
print(f"   • 625 display: Uses real photos (positions 1-96)")
print(f"   • Project index: Shows ALL 76 projects")
print(f"   • Clickable projects: 20 projects with real photos")
print(f"   • Listed projects: 56 projects without photos (still appear in index)")

print(f"\\n📊 PROJECT BREAKDOWN:")
for year, projects in complete_projects.items():
    if projects:
        with_photos = sum(1 for p in projects if any(img < 100 for img in p['images']))
        without_photos = len(projects) - with_photos
        print(f"   {year}: {len(projects)} total ({with_photos} with photos)")

print(f"\\n🚀 READY TO VIEW!")
print(f"   Refresh your browser to see all projects listed!")
