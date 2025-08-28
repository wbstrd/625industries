#!/usr/bin/env python3

import json
import re

def careful_add_projects():
    """Very carefully add missing projects without touching anything else"""
    
    # Read the complete projects list
    with open('Archives/projects.json', 'r') as f:
        all_projects = json.load(f)
    
    # Read current HTML
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Find the exact projects constant
    projects_start = content.find('const projects = {')
    if projects_start == -1:
        print("Could not find projects constant")
        return False
    
    # Find the end of the projects object
    brace_count = 0
    pos = projects_start + len('const projects = ')
    while pos < len(content):
        if content[pos] == '{':
            brace_count += 1
        elif content[pos] == '}':
            brace_count -= 1
            if brace_count == 0:
                projects_end = pos + 1
                if pos + 1 < len(content) and content[pos + 1] == ';':
                    projects_end += 1
                break
        pos += 1
    
    # Extract current projects string
    current_projects_str = content[projects_start:projects_end]
    
    # Parse just the projects object part
    projects_obj_str = current_projects_str[len('const projects = '):-1]  # Remove const and semicolon
    current_projects = json.loads(projects_obj_str)
    
    # Get current project titles
    current_titles = set()
    for year_projects in current_projects.values():
        for project in year_projects:
            current_titles.add(project['title'].upper())
    
    # Add missing projects
    for project in all_projects:
        year = project['date'][:4]
        title = project['event'].upper()
        
        # Skip if already exists
        if title in current_titles:
            continue
        
        # Create text-only project
        new_project = {
            "title": title,
            "date": project['date'].replace('-', '.'),
            "location": project['city'].upper(),
            "description": f"{project['client']} {project['event']} in {project['city']}."
        }
        
        # Add to appropriate year
        if year not in current_projects:
            current_projects[year] = []
        current_projects[year].append(new_project)
    
    # Sort projects within each year by date
    for year in current_projects:
        current_projects[year].sort(key=lambda x: x['date'])
    
    # Create new projects constant
    new_projects_const = f"const projects = {json.dumps(current_projects, indent=2)};"
    
    # Replace ONLY the projects constant in the original content
    new_content = content[:projects_start] + new_projects_const + content[projects_end:]
    
    # Write back
    with open('index_with_carousel.html', 'w') as f:
        f.write(new_content)
    
    total = sum(len(year_projects) for year_projects in current_projects.values())
    with_photos = sum(len([p for p in year_projects if 'images' in p]) for year_projects in current_projects.values())
    
    print(f"✅ Carefully added missing projects!")
    print(f"📸 {with_photos} projects with photos")
    print(f"📝 {total - with_photos} text-only projects")
    print(f"🎯 Total: {total} projects")
    
    return True

if __name__ == "__main__":
    careful_add_projects()
