import json
from collections import defaultdict

# Read the archive projects
with open('Archives/projects.json', 'r') as f:
    archive_projects = json.load(f)

# Group by year and convert format
projects_by_year = defaultdict(list)

for project in archive_projects:
    year = project['date'][:4]  # Extract year from date
    month = project['date'][5:7]
    day = project['date'][8:10]
    
    # Convert to HTML format
    html_project = {
        "title": project['event'].upper(),
        "date": f"{year}.{month}.{day}",
        "location": project['city'].upper(),
        "description": f"{project['client']} {project['event']} event in {project['city']}.",
        "images": []
    }
    
    projects_by_year[year].append(html_project)

# Generate the JavaScript object
print("const projects = {")
for year in sorted(projects_by_year.keys()):
    print(f'  "{year}": [')
    for project in projects_by_year[year]:
        print(f'    {{')
        print(f'      "title": "{project["title"]}",')
        print(f'      "date": "{project["date"]}",')
        print(f'      "location": "{project["location"]}",')
        print(f'      "description": "{project["description"]}",')
        print(f'      "images": []')
        print(f'    }},')
    print(f'  ],')
print("};")

print(f"\nTotal projects: {len(archive_projects)}")
print(f"Years: {sorted(projects_by_year.keys())}")
