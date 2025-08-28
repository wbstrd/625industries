#!/usr/bin/env python3

import json

def fix_project_mapping():
    # Read the correct project mapping
    with open('simple_project_mapping.json', 'r') as f:
        project_data = json.load(f)
    
    # Read the current HTML
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Create a flat list of all projects for easier access
    all_projects = []
    for year, projects in project_data.items():
        for project in projects:
            all_projects.append(project)
    
    # Replace the project click handler with real data
    new_handler = '''
        // Add click handlers to project items with real data
        function addProjectClickHandlers() {
            const projectsByYear = ''' + json.dumps(project_data, indent=8) + ''';
            
            const projectItems = document.querySelectorAll('.project-item');
            let projectIndex = 0;
            
            // Flatten projects to match the DOM order
            const allProjects = [];
            Object.keys(projectsByYear).sort().forEach(year => {
                projectsByYear[year].forEach(project => {
                    allProjects.push(project);
                });
            });
            
            projectItems.forEach((item, index) => {
                if (index < allProjects.length) {
                    const project = allProjects[index];
                    item.addEventListener('click', function() {
                        showProjectModal(project);
                    });
                }
            });
        }'''
    
    # Replace the existing addProjectClickHandlers function
    import re
    pattern = r'function addProjectClickHandlers\(\)\s*\{[^}]*\}[^}]*\}'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_handler.strip(), content, flags=re.DOTALL)
    
    # Write back to file
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print("Fixed project mapping with real data!")

if __name__ == "__main__":
    fix_project_mapping()
