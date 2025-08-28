#!/usr/bin/env python3

import json

def surgical_add_projects():
    """Surgically add individual project entries without touching anything else"""
    
    # Read the complete projects list
    with open('Archives/projects.json', 'r') as f:
        all_projects = json.load(f)
    
    # Read current HTML
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Get current project titles to see what's missing
    current_titles = set()
    
    # Extract titles from the existing content using simple string matching
    lines = content.split('\n')
    for line in lines:
        if '"title":' in line:
            # Extract title value
            start = line.find('"title": "') + len('"title": "')
            end = line.find('"', start)
            if start > len('"title": "') - 1 and end > start:
                current_titles.add(line[start:end])
    
    print(f"Found {len(current_titles)} existing projects")
    
    # Create missing projects grouped by year
    missing_by_year = {}
    for project in all_projects:
        year = project['date'][:4]
        title = project['event'].upper()
        
        if title not in current_titles:
            if year not in missing_by_year:
                missing_by_year[year] = []
            
            missing_by_year[year].append({
                "title": title,
                "date": project['date'].replace('-', '.'),
                "location": project['city'].upper(),
                "description": f"{project['client']} {project['event']} in {project['city']}."
            })
    
    # Now add them by finding year sections and inserting
    for year, projects_to_add in missing_by_year.items():
        year_pattern = f'"{year}": ['
        year_pos = content.find(year_pattern)
        
        if year_pos != -1:
            # Find where this year's array ends
            bracket_count = 0
            pos = year_pos + len(year_pattern) - 1  # Start at the opening bracket
            
            while pos < len(content):
                if content[pos] == '[':
                    bracket_count += 1
                elif content[pos] == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        # Found the closing bracket for this year
                        # Check if there are existing projects (look for comma before closing)
                        section = content[year_pos:pos]
                        has_existing = '"title":' in section
                        
                        if has_existing:
                            # Add comma and new projects
                            insert_text = ','
                        else:
                            # Empty array, just add projects
                            insert_text = ''
                        
                        for i, proj in enumerate(projects_to_add):
                            if i > 0 or has_existing:
                                insert_text += ','
                            insert_text += f'\n    {{\n      "title": "{proj["title"]}",\n      "date": "{proj["date"]}",\n      "location": "{proj["location"]}",\n      "description": "{proj["description"]}"\n    }}'
                        
                        if not has_existing and projects_to_add:
                            insert_text += '\n  '
                        
                        content = content[:pos] + insert_text + content[pos:]
                        break
                pos += 1
        else:
            # Year doesn't exist, need to add it
            # Find where to insert new year (before the closing brace of projects object)
            projects_end = content.rfind('}', content.find('const projects = '))
            if projects_end != -1:
                # Add new year before closing brace
                new_year_text = f',\n  "{year}": [\n'
                for i, proj in enumerate(projects_to_add):
                    if i > 0:
                        new_year_text += ','
                    new_year_text += f'\n    {{\n      "title": "{proj["title"]}",\n      "date": "{proj["date"]}",\n      "location": "{proj["location"]}",\n      "description": "{proj["description"]}"\n    }}'
                new_year_text += '\n  ]'
                
                content = content[:projects_end] + new_year_text + content[projects_end:]
    
    # Write back
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    total_added = sum(len(projects) for projects in missing_by_year.values())
    print(f"✅ Surgically added {total_added} missing projects!")
    print(f"📝 Added to years: {list(missing_by_year.keys())}")
    
    return True

if __name__ == "__main__":
    surgical_add_projects()
