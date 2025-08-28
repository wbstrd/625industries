#!/usr/bin/env python3

import json
import re

def simple_add_projects():
    """Simply add missing projects to the existing working file"""
    
    # Read the complete projects list
    with open('Archives/projects.json', 'r') as f:
        all_projects = json.load(f)
    
    # Read current HTML
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Find current projects and add missing ones manually
    # We'll add them to the existing structure without parsing/replacing the whole thing
    
    missing_projects_by_year = {
        "2018": [
            '{"title": "AIR MAX DAY", "date": "2018.03.26", "location": "BROOKLYN", "description": "Nike Air Max Day in Brooklyn."}',
            '{"title": "KYRIE SNEAKER CUSTOMIZATION", "date": "2018.09.28", "location": "BROOKLYN", "description": "Nike Kyrie Sneaker Customization in Brooklyn."}',
            '{"title": "SOCIAL STUDIES", "date": "2018.11.16", "location": "NEW YORK", "description": "Nike Social Studies in New York."}',
            '{"title": "GIFTING SUITE", "date": "2018.12.06", "location": "MIAMI", "description": "Nike Gifting Suite in Miami."}'
        ],
        "2019": [
            '{"title": "ALL-STAR WEEKEND", "date": "2019.02.15", "location": "CHARLOTTE", "description": "Nike All-Star Weekend in Charlotte."}',
            '{"title": "AIR MAX WEEK", "date": "2019.03.22", "location": "NEW YORK", "description": "Nike Air Max Week in New York."}',
            '{"title": "CUSTOM POLO (SNKRS)", "date": "2019.07.31", "location": "NYC", "description": "Nike Custom Polo (SNKRS) in NYC."}',
            '{"title": "LEVI\'S × CENTURY 21", "date": "2019.10.03", "location": "NYC", "description": "Levi\'s × Century 21 in NYC."}',
            '{"title": "LEVI\'S HAUS", "date": "2019.12.04", "location": "MIAMI", "description": "Levi\'s Haus in Miami."}'
        ],
        "2020": [
            '{"title": "VERDY × LEVI\'S HAUS", "date": "2020.01.24", "location": "MIAMI", "description": "Verdy × Levi\'s Haus in Miami."}',
            '{"title": "SUPER BOWL LIV", "date": "2020.01.26", "location": "MIAMI", "description": "Nike Super Bowl LIV in Miami."}',
            '{"title": "LEVI\'S × BAPE", "date": "2020.03.05", "location": "MIAMI", "description": "Levi\'s × BAPE in Miami."}'
        ]
    }
    
    # Add more years with missing projects
    # For now, let's just add a few to test
    
    # Find where to insert new projects in each year
    for year, projects_list in missing_projects_by_year.items():
        year_pattern = f'"{year}": \\['
        year_match = re.search(year_pattern, content)
        
        if year_match:
            # Find the end of this year's array
            start_pos = year_match.end()
            bracket_count = 1
            pos = start_pos
            
            while bracket_count > 0 and pos < len(content):
                if content[pos] == '[':
                    bracket_count += 1
                elif content[pos] == ']':
                    bracket_count -= 1
                pos += 1
            
            # Insert new projects before the closing bracket
            insert_pos = pos - 1
            
            # Add comma if there are existing projects
            if content[start_pos:insert_pos].strip():
                insertion = ',\n    ' + ',\n    '.join(projects_list)
            else:
                insertion = '\n    ' + ',\n    '.join(projects_list) + '\n  '
            
            content = content[:insert_pos] + insertion + content[insert_pos:]
        else:
            # Year doesn't exist, add it
            # Find where to add new year (this is more complex, let's skip for now)
            pass
    
    # Write the updated file
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print("✅ Added missing projects to existing structure!")
    return True

if __name__ == "__main__":
    simple_add_projects()
