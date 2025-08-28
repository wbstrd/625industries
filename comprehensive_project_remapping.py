#!/usr/bin/env python3
"""
Comprehensive project remapping - analyze wetransfer folders vs website projects
"""

import os
import json
import re
from collections import defaultdict

def find_wetransfer_projects():
    """Find all project folders in wetransfer directory"""
    wetransfer_base = "/Volumes/T7"
    projects = {}
    
    print("🔍 Scanning for project folders in T7...")
    
    # Find all wetransfer folders
    for root, dirs, files in os.walk(wetransfer_base):
        if "wetransfer" in root.lower():
            for dir_name in dirs:
                # Skip system directories
                if dir_name.startswith('.'):
                    continue
                    
                full_path = os.path.join(root, dir_name)
                
                # Count image files
                image_count = 0
                try:
                    for f in os.listdir(full_path):
                        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic')):
                            image_count += 1
                except:
                    continue
                
                if image_count > 0:
                    projects[dir_name] = {
                        'path': full_path,
                        'image_count': image_count
                    }
                    print(f"  📁 {dir_name}: {image_count} images")
    
    return projects

def get_current_website_projects():
    """Extract current project mappings from index_with_carousel.html"""
    print("\n📊 Analyzing current website projects...")
    
    with open("index_with_carousel.html", "r") as f:
        content = f.read()
    
    # Extract the projects constant
    projects_start = content.find('const projects = {')
    if projects_start == -1:
        print("❌ Could not find projects constant")
        return {}
    
    # Find the closing brace - need to count braces
    brace_count = 0
    projects_end = projects_start
    for i, char in enumerate(content[projects_start:], projects_start):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                projects_end = i + 1
                break
    
    projects_str = content[projects_start:projects_end]
    
    # Parse manually since it's JS format
    website_projects = {}
    lines = projects_str.split('\n')
    current_year = None
    current_project = None
    in_images = False
    
    for line in lines:
        line = line.strip()
        
        # Year detection
        year_match = re.search(r'"(\d{4})":', line)
        if year_match:
            current_year = year_match.group(1)
            website_projects[current_year] = []
            continue
        
        # Project title
        title_match = re.search(r'"title":\s*"([^"]+)"', line)
        if title_match and current_year:
            current_project = {
                'title': title_match.group(1),
                'year': current_year,
                'images': []
            }
            continue
        
        # Images array
        if '"images":' in line:
            in_images = True
            continue
        
        if in_images:
            if ']' in line:
                in_images = False
                if current_project:
                    website_projects[current_year].append(current_project)
                    current_project = None
                continue
            
            # Extract numbers from line
            numbers = re.findall(r'\b(\d+)\b', line)
            if numbers and current_project:
                current_project['images'].extend([int(n) for n in numbers])
    
    # Print summary
    total_images_used = 0
    for year, year_projects in website_projects.items():
        print(f"\n  📅 {year}:")
        for project in year_projects:
            image_count = len(project['images'])
            total_images_used += image_count
            print(f"    📂 {project['title']}: {image_count} images ({project['images'][0] if project['images'] else 'N/A'}-{project['images'][-1] if project['images'] else 'N/A'})")
    
    print(f"\n📊 Total images used on website: {total_images_used}")
    
    return website_projects

def find_missing_images():
    """Find which images (1-150+) are not assigned to any project"""
    print("\n🔍 Finding unassigned images...")
    
    website_projects = get_current_website_projects()
    
    # Collect all used image numbers
    used_images = set()
    for year, year_projects in website_projects.items():
        for project in year_projects:
            used_images.update(project['images'])
    
    # Find missing images (assuming we have images 1-150+)
    max_image = 240  # Based on NUM_IMAGES in HTML
    all_images = set(range(1, max_image + 1))
    missing_images = sorted(all_images - used_images)
    
    print(f"📊 Images 1-{max_image}: {len(all_images)} total")
    print(f"✅ Assigned: {len(used_images)} images")
    print(f"❌ Unassigned: {len(missing_images)} images")
    
    if len(missing_images) <= 20:
        print(f"🔍 Unassigned images: {missing_images}")
    else:
        print(f"🔍 First 20 unassigned: {missing_images[:20]}")
        print(f"🔍 Last 20 unassigned: {missing_images[-20:]}")
    
    return missing_images, used_images

def suggest_remapping():
    """Suggest remapping based on wetransfer folders vs website projects"""
    print("\n🎯 REMAPPING ANALYSIS")
    print("=" * 50)
    
    wetransfer_projects = find_wetransfer_projects()
    website_projects = get_current_website_projects()
    missing_images, used_images = find_missing_images()
    
    print(f"\n📋 COMPARISON:")
    print(f"  🗂️  Wetransfer folders: {len(wetransfer_projects)}")
    total_website_projects = sum(len(year_projects) for year_projects in website_projects.values())
    print(f"  🌐 Website projects: {total_website_projects}")
    
    # Analyze specific mismatches
    print(f"\n🔍 SPECIFIC ISSUES:")
    
    # TXRX example
    txrx_folder = None
    for name, data in wetransfer_projects.items():
        if 'txrx' in name.lower():
            txrx_folder = data
            break
    
    if txrx_folder:
        print(f"  📁 TXRX folder: {txrx_folder['image_count']} images")
        
        # Find TXRX project on website
        txrx_website = None
        for year, year_projects in website_projects.items():
            for project in year_projects:
                if 'txrx' in project['title'].lower():
                    txrx_website = project
                    break
        
        if txrx_website:
            print(f"  🌐 TXRX website: {len(txrx_website['images'])} images ({txrx_website['images']})")
            print(f"  ⚠️  MISMATCH: {txrx_folder['image_count']} vs {len(txrx_website['images'])}")
            
            # Suggest using missing images
            needed = txrx_folder['image_count'] - len(txrx_website['images'])
            if needed > 0:
                suggested = missing_images[:needed]
                print(f"  💡 Suggested additional images for TXRX: {suggested}")
    
    print(f"\n🚀 NEXT STEPS:")
    print(f"  1. Run the original map_heic_projects.py to get proper mapping")
    print(f"  2. Or manually assign missing images to projects")
    print(f"  3. Remove duplicate image 82 from TXRX (identical to 81)")
    
    return {
        'wetransfer_projects': wetransfer_projects,
        'website_projects': website_projects,
        'missing_images': missing_images,
        'used_images': used_images
    }

def main():
    print("🔄 Comprehensive Project Remapping Analysis")
    print("=" * 60)
    
    analysis = suggest_remapping()
    
    print(f"\n✅ Analysis complete!")
    print(f"   Check the output above for specific issues and suggestions.")

if __name__ == "__main__":
    main()
