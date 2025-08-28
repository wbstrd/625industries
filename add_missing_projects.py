#!/usr/bin/env python3

import json

def add_missing_projects():
    """Add all missing projects from projects.json to the index list"""
    
    # Read the complete projects list
    with open('Archives/projects.json', 'r') as f:
        all_projects = json.load(f)
    
    # Read current HTML
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Current projects that have photos (from the mapping)
    projects_with_photos = {
        "LA ALL STAR",
        "MAKERS STUDIO", 
        "LEVI'S HOUSE × DAISY WORLD",
        "BILLIE EILISH × NIKE (UPCYCLE)",
        "NFL DRAFT DAY",
        "LEVI'S × COME",
        "MLB NIKEBYYOU",
        "SUPER BOWL LVII × UNDFTD",
        "NIKEBYYOU – SUPER BOWL",
        "ROLLING LOUD × LEVI'S",
        "LEVI'S 501 DAY",
        "NIKE TEA ROOM",
        "SUPER BOWL LVIII NIKEBYYOU",
        "ROLLING LOUD × MODELO",
        "VEGAS KICK OFF",
        "TXRX WORKSHOP",
        "ALL STAR WEEKEND × BOARDROOM"
    }
    
    # Organize all projects by year
    projects_by_year = {}
    
    for project in all_projects:
        year = project['date'][:4]
        if year not in projects_by_year:
            projects_by_year[year] = []
        
        # Convert to our format
        title = project['event'].upper()
        
        # Check if this project has photos
        has_photos = any(photo_title in title for photo_title in projects_with_photos)
        
        project_entry = {
            "title": title,
            "date": project['date'].replace('-', '.'),
            "location": project['city'].upper(),
            "description": f"{project['client']} {project['event']} in {project['city']}.",
        }
        
        # Only add images array if it has photos
        if has_photos:
            # Map to existing image ranges (this is simplified - you may need to adjust)
            if "TXRX" in title:
                project_entry["images"] = [81, 82, 83, 84, 85]
            elif "LA ALL STAR" in title:
                project_entry["images"] = [91, 92, 93, 94, 95]
            elif "MAKERS STUDIO" in title and "2018.12" in project_entry["date"]:
                project_entry["images"] = [1, 2, 3, 4, 5]
            elif "MAKERS STUDIO" in title and "2018.10" in project_entry["date"]:
                project_entry["images"] = [6, 7, 8, 9, 10]
            elif "LEVI'S HOUSE" in title:
                project_entry["images"] = [11, 12, 13, 14, 15]
            elif "BILLIE EILISH" in title:
                project_entry["images"] = [16, 17, 18, 19, 20]
            elif "LEVI'S × COME" in title:
                project_entry["images"] = [21, 22, 23, 24, 25]
            elif "NFL DRAFT" in title:
                project_entry["images"] = [26, 27, 28, 29, 30]
            elif "MLB" in title:
                project_entry["images"] = [31, 32, 33, 34, 35]
            elif "SUPER BOWL LVII × UNDFTD" in title:
                project_entry["images"] = [36, 37, 38, 39, 40]
            elif "NIKEBYYOU – SUPER BOWL" in title and "2023" in year:
                project_entry["images"] = [41, 42, 43, 44, 45]
            elif "ROLLING LOUD" in title and "2023.03" in project_entry["date"]:
                project_entry["images"] = [46, 47, 48, 49, 50]
            elif "501 DAY" in title:
                project_entry["images"] = [51, 52, 53, 54, 55]
            elif "ROLLING LOUD" in title and "2023.07" in project_entry["date"]:
                project_entry["images"] = [56, 57, 58, 59, 60]
            elif "TEA ROOM" in title:
                project_entry["images"] = [61, 62, 63, 64, 65]
            elif "SUPER BOWL LVIII" in title:
                project_entry["images"] = [66, 67, 68, 69, 70]
            elif "ROLLING LOUD × MODELO" in title and "2024" in year:
                project_entry["images"] = [71, 72, 73, 74, 75]
            elif "VEGAS KICK OFF" in title:
                project_entry["images"] = [76, 77, 78, 79, 80]
            elif "ALL STAR WEEKEND × BOARDROOM" in title:
                project_entry["images"] = [86, 87, 88, 89, 90]
        
        projects_by_year[year].append(project_entry)
    
    # Sort projects within each year by date
    for year in projects_by_year:
        projects_by_year[year].sort(key=lambda x: x['date'])
    
    # Create the new projects JavaScript
    new_projects_js = "const projects = " + json.dumps(projects_by_year, indent=2) + ";"
    
    # Replace the projects constant
    import re
    pattern = r'const projects = \{.*?\};'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_projects_js, content, flags=re.DOTALL)
    else:
        print("Could not find projects constant")
        return False
    
    # Write the updated HTML file
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print(f"✅ Added all {len(all_projects)} projects to the index!")
    print(f"📸 {len([p for year_projects in projects_by_year.values() for p in year_projects if 'images' in p])} projects have photos")
    print(f"📝 {len([p for year_projects in projects_by_year.values() for p in year_projects if 'images' not in p])} projects are text-only")
    
    return True

if __name__ == "__main__":
    add_missing_projects()
