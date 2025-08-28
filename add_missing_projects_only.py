#!/usr/bin/env python3

import json
import re

def add_missing_projects_only():
    """Add ONLY the missing projects to the existing list without changing anything else"""
    
    # Read the complete projects list
    with open('Archives/projects.json', 'r') as f:
        all_projects = json.load(f)
    
    # Read current HTML
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Extract current projects data
    pattern = r'const projects = (\{.*?\});'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print("Could not find projects constant")
        return False
    
    current_projects_str = match.group(1)
    
    # Parse current projects
    import ast
    try:
        current_projects = ast.literal_eval(current_projects_str)
    except:
        # Try with json if ast fails
        current_projects = json.loads(current_projects_str)
    
    # Get all current project titles to see what's missing
    current_titles = set()
    for year_projects in current_projects.values():
        for project in year_projects:
            current_titles.add(project['title'].upper())
    
    # Add missing projects by year
    for project in all_projects:
        year = project['date'][:4]
        title = project['event'].upper()
        
        # Skip if we already have this project
        if title in current_titles:
            continue
        
        # Create new project entry (text only, no images)
        new_project = {
            "title": title,
            "date": project['date'].replace('-', '.'),
            "location": project['city'].upper(),
            "description": f"{project['client']} {project['event']} in {project['city']}."
        }
        
        # Add to the appropriate year
        if year not in current_projects:
            current_projects[year] = []
        
        current_projects[year].append(new_project)
    
    # Sort projects within each year by date
    for year in current_projects:
        current_projects[year].sort(key=lambda x: x['date'])
    
    # Create the new projects JavaScript
    new_projects_js = "const projects = " + json.dumps(current_projects, indent=2, ensure_ascii=False) + ";"
    
    # Replace ONLY the projects constant
    content = re.sub(pattern, new_projects_js, content, flags=re.DOTALL)
    
    # Write the updated HTML file
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    total_projects = sum(len(year_projects) for year_projects in current_projects.values())
    projects_with_photos = sum(len([p for p in year_projects if 'images' in p]) for year_projects in current_projects.values())
    
    print(f"✅ Added missing projects to the index!")
    print(f"📸 {projects_with_photos} projects have photos")
    print(f"📝 {total_projects - projects_with_photos} projects are text-only")
    print(f"🎯 Total projects: {total_projects}")
    
    return True

if __name__ == "__main__":
    add_missing_projects_only()