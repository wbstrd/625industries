#!/usr/bin/env python3
"""
Image Mapping Script for 625 Industries
Maps project-organized folders to numbered image system
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
import shutil

# Paths
PROJECT_FOLDERS_PATH = "/Volumes/T7/wetransfer_arizona-february-2023-undefeated_2025-05-29_0306"
NUMBERED_IMAGES_PATH = "/Volumes/T7/625industriesGIT/625industries/images"
PROJECTS_JSON_PATH = "/Volumes/T7/625industriesGIT/625industries/Archives/projects.json"
OUTPUT_MAPPING_PATH = "/Volumes/T7/625industriesGIT/625industries/image_mapping.json"

def load_projects():
    """Load projects from JSON file"""
    with open(PROJECTS_JSON_PATH, 'r') as f:
        return json.load(f)

def get_project_folders():
    """Get list of project folders and their contents"""
    folders = {}
    project_path = Path(PROJECT_FOLDERS_PATH)
    
    for folder in project_path.iterdir():
        if folder.is_dir() and folder.name != "converted":
            images = []
            for file in folder.iterdir():
                if file.suffix.lower() in ['.jpg', '.jpeg', '.heic', '.png']:
                    images.append(file.name)
            
            if images:  # Only include folders with images
                folders[folder.name] = {
                    'path': str(folder),
                    'images': images,
                    'count': len(images)
                }
    
    return folders

def parse_folder_date(folder_name):
    """Extract date from folder name"""
    # Common date patterns
    patterns = [
        r'(\w+)\s+(\d{4})',  # "February 2024"
        r'(\d{4})\s+(\w+)',  # "2024 February"
        r'(\w+)\s+(\d{4})\s+(\w+)',  # "July 2022 Baseball"
    ]
    
    months = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    
    folder_lower = folder_name.lower()
    
    for pattern in patterns:
        match = re.search(pattern, folder_lower)
        if match:
            groups = match.groups()
            if len(groups) >= 2:
                # Try to identify month and year
                month_str = groups[0] if groups[0].lower() in months else groups[1] if len(groups) > 1 and groups[1].lower() in months else None
                year_str = None
                
                for group in groups:
                    if group.isdigit() and len(group) == 4:
                        year_str = group
                        break
                
                if month_str and year_str and month_str.lower() in months:
                    return f"{year_str}-{months[month_str.lower()]:02d}"
    
    return None

def match_folders_to_projects(projects, folders):
    """Match project folders to JSON projects based on names and dates"""
    matches = {}
    unmatched_folders = []
    unmatched_projects = []
    
    # Create a mapping of projects by date and keywords
    projects_by_date = {}
    for i, project in enumerate(projects):
        date_key = project['date'][:7]  # YYYY-MM format
        if date_key not in projects_by_date:
            projects_by_date[date_key] = []
        projects_by_date[date_key].append((i, project))
    
    # Try to match folders to projects
    for folder_name, folder_info in folders.items():
        best_match = None
        best_score = 0
        
        # Extract date from folder
        folder_date = parse_folder_date(folder_name)
        
        # Look for matches
        candidates = []
        if folder_date and folder_date in projects_by_date:
            candidates = projects_by_date[folder_date]
        else:
            # If no date match, check all projects
            candidates = [(i, p) for i, p in enumerate(projects)]
        
        for project_idx, project in candidates:
            score = 0
            
            # Date matching
            if folder_date and project['date'][:7] == folder_date:
                score += 50
            
            # Client/event keyword matching
            folder_lower = folder_name.lower()
            client_lower = project['client'].lower()
            event_lower = project['event'].lower()
            city_lower = project['city'].lower()
            
            # Check for client matches
            if client_lower in folder_lower or any(word in folder_lower for word in client_lower.split()):
                score += 30
            
            # Check for event matches
            event_words = event_lower.split()
            folder_words = folder_lower.split()
            common_words = set(event_words) & set(folder_words)
            if common_words:
                score += len(common_words) * 10
            
            # Check for city matches
            if city_lower in folder_lower:
                score += 20
            
            # Special case matching
            special_matches = {
                'superbowl': ['super bowl', 'super', 'bowl'],
                'nike': ['nike', 'nikebyyou'],
                'rolling loud': ['rolling', 'loud'],
                'levi': ['levi', "levi's"],
                'allstar': ['all-star', 'all star'],
                'baseball': ['mlb', 'baseball'],
                'basketball': ['nba', 'basketball'],
                'undefeated': ['undftd', 'undefeated'],
                'modelo': ['modelo'],
                'billie': ['billie', 'eilish']
            }
            
            for key, variations in special_matches.items():
                if any(var in folder_lower for var in variations) and any(var in event_lower or var in client_lower for var in variations):
                    score += 25
            
            if score > best_score:
                best_score = score
                best_match = (project_idx, project, score)
        
        if best_match and best_match[2] > 20:  # Minimum score threshold
            matches[folder_name] = {
                'project_index': best_match[0],
                'project': best_match[1],
                'score': best_match[2],
                'folder_info': folder_info
            }
        else:
            unmatched_folders.append(folder_name)
    
    # Find unmatched projects
    matched_project_indices = {match['project_index'] for match in matches.values()}
    for i, project in enumerate(projects):
        if i not in matched_project_indices:
            unmatched_projects.append((i, project))
    
    return matches, unmatched_folders, unmatched_projects

def create_image_mapping(matches, total_images=240):
    """Create mapping of image numbers to project folders"""
    mapping = {}
    current_image = 1
    
    # Sort matches by date for logical ordering
    sorted_matches = sorted(matches.items(), key=lambda x: x[1]['project']['date'])
    
    for folder_name, match_info in sorted_matches:
        project_index = match_info['project_index']
        folder_info = match_info['folder_info']
        image_count = min(folder_info['count'], 5)  # Max 5 images per project as in original
        
        project_images = []
        for i in range(image_count):
            if current_image <= total_images:
                project_images.append(current_image)
                current_image += 1
        
        mapping[folder_name] = {
            'project_index': project_index,
            'project': match_info['project'],
            'images': project_images,
            'folder_path': folder_info['path'],
            'source_images': folder_info['images'][:image_count]
        }
    
    return mapping

def main():
    """Main function to create the mapping"""
    print("Loading projects...")
    projects = load_projects()
    print(f"Found {len(projects)} projects")
    
    print("Scanning project folders...")
    folders = get_project_folders()
    print(f"Found {len(folders)} folders with images")
    
    print("\nProject folders found:")
    for name, info in folders.items():
        print(f"  {name}: {info['count']} images")
    
    print("\nMatching folders to projects...")
    matches, unmatched_folders, unmatched_projects = match_folders_to_projects(projects, folders)
    
    print(f"\nMatching results:")
    print(f"  Matched: {len(matches)} folders")
    print(f"  Unmatched folders: {len(unmatched_folders)}")
    print(f"  Unmatched projects: {len(unmatched_projects)}")
    
    print("\nMatched folders:")
    for folder_name, match_info in matches.items():
        project = match_info['project']
        score = match_info['score']
        print(f"  {folder_name} -> {project['date']} {project['client']} {project['event']} (score: {score})")
    
    if unmatched_folders:
        print("\nUnmatched folders:")
        for folder in unmatched_folders:
            print(f"  {folder}")
    
    if unmatched_projects:
        print("\nUnmatched projects:")
        for i, project in unmatched_projects:
            print(f"  {project['date']} {project['client']} {project['event']} {project['city']}")
    
    # Create image mapping
    print("\nCreating image mapping...")
    image_mapping = create_image_mapping(matches)
    
    # Save mapping to file
    with open(OUTPUT_MAPPING_PATH, 'w') as f:
        json.dump(image_mapping, f, indent=2)
    
    print(f"\nImage mapping saved to: {OUTPUT_MAPPING_PATH}")
    print(f"Total mapped projects: {len(image_mapping)}")
    
    # Show image assignments
    print("\nImage assignments:")
    for folder_name, mapping_info in image_mapping.items():
        images = mapping_info['images']
        project = mapping_info['project']
        print(f"  {folder_name}: images {images[0]}-{images[-1] if len(images) > 1 else images[0]} -> {project['date']} {project['event']}")

if __name__ == "__main__":
    main()
