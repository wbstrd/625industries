#!/usr/bin/env python3
"""
Fix Project Mappings Script
Manually corrects the mismatched projects and adds missing ones
"""

import json
from pathlib import Path

# Load current mapping
with open('/Volumes/T7/625industriesGIT/625industries/image_mapping.json', 'r') as f:
    current_mapping = json.load(f)

# Load projects for reference
with open('/Volumes/T7/625industriesGIT/625industries/Archives/projects.json', 'r') as f:
    all_projects = json.load(f)

# Create corrected mapping with manual fixes
corrected_mapping = {}
current_image_num = 1

# Define the correct mappings manually
correct_mappings = [
    # 2018
    {
        "folder": "October 2018 Nike Maker's Space", 
        "project_index": 2,  # 2018-10-18 Makers Studio
        "images": list(range(1, 6))
    },
    {
        "folder": "December 2018 - Maker's Studio Nike",
        "project_index": 4,  # 2018-12-01 Makers Studio  
        "images": list(range(6, 11))
    },
    
    # 2022
    {
        "folder": "Super Bowl The Grove NikeByYou",
        "project_index": 23,  # 2022-02-03 NikeByYou – Super Bowl LVI
        "images": list(range(11, 16))
    },
    {
        "folder": "LA 2022 Levi's House",
        "project_index": 26,  # 2022-04-05 Levi's House × Daisy World
        "images": list(range(16, 21))
    },
    {
        "folder": "Levi's x Come Watts LA",
        "project_index": 27,  # 2022-04-07 Levi's × COME
        "images": list(range(21, 26))
    },
    {
        "folder": "LA Billie Eillish Nike Activation",
        "project_index": 29,  # 2022-04-19 Billie Eilish × Nike (Upcycle)
        "images": list(range(26, 31))
    },
    {
        "folder": "NFL Draft Vegas 2022", 
        "project_index": 30,  # 2022-04-27 NFL Draft Day
        "images": list(range(31, 36))
    },
    {
        "folder": "July 2022 Baseball Allstar NikeByYou",
        "project_index": 33,  # 2022-07-15 MLB NikeByYou
        "images": list(range(36, 41))
    },
    {
        "folder": "Rolling Loud Miami 2024",  # This is actually 2022 based on mapping
        "project_index": 34,  # 2022-07-21 Rolling Loud × Levi's
        "images": list(range(41, 46))
    },
    
    # 2023
    {
        "folder": "Arizona February 2023 Undefeated",
        "project_index": 39,  # 2023-02-07 Nike Super Bowl LVII × UNDFTD
        "images": list(range(46, 51))
    },
    {
        "folder": "Phoenix Superbowl NikeByYou February 2023",
        "project_index": 40,  # 2023-02-08 Nike NikeByYou – Super Bowl
        "images": list(range(51, 56))
    },
    {
        "folder": "Rolling Loud 2023 March Levi's",
        "project_index": 41,  # 2023-03-04 Rolling Loud × Levi's
        "images": list(range(56, 61))
    },
    {
        "folder": "Photos 501 Day Levi's SF",
        "project_index": 43,  # 2023-05-18 Levi's 501 Day
        "images": list(range(61, 66))
    },
    {
        "folder": "July 2023 Rolling Loud Levi's",
        "project_index": 44,  # 2023-07-05 Rolling Loud × Levi's
        "images": list(range(66, 70))  # Only 4 images
    },
    {
        "folder": "Tea Room July 2023 Nike",
        "project_index": 46,  # 2023-07-13 Nike Tea Room
        "images": list(range(70, 74))  # Only 4 images
    },
    
    # 2024
    {
        "folder": "February 2024 Superbowl Vegas",
        "project_index": 55,  # 2024-02-06 Nike Super Bowl LVIII NikeByYou
        "images": list(range(74, 79))
    },
    {
        "folder": "Modelo Rolling Loud LA March",
        "project_index": 56,  # 2024-03-14 Rolling Loud × Modelo
        "images": list(range(79, 84))
    },
    {
        "folder": "Vegas Modelo Kick Off - 2024",
        "project_index": 65,  # 2024-09-01 Modelo Vegas Kick Off
        "images": list(range(84, 89))
    },
    
    # 2025 - CORRECTED MAPPINGS
    {
        "folder": "Photos for TXRX Nike",  # FIXED: This should be TXRX Workshop, not Tea Room
        "project_index": 74,  # 2025-02-11 Nike TXRX Workshop
        "images": list(range(89, 94))
    },
    {
        "folder": "Photos for Boardroom Brunch",  # FIXED: This should be All Star Weekend
        "project_index": 75,  # 2025-02-15 Nike All Star Weekend × Boardroom  
        "images": list(range(94, 97))  # Only 3 images
    }
]

# Create the corrected mapping
project_folders_path = "/Volumes/T7/wetransfer_arizona-february-2023-undefeated_2025-05-29_0306"

for mapping in correct_mappings:
    folder_name = mapping["folder"]
    project_index = mapping["project_index"]
    images = mapping["images"]
    
    # Get project info
    project = all_projects[project_index]
    
    # Get folder info from current mapping or scan directly
    if folder_name in current_mapping:
        folder_info = current_mapping[folder_name]
        folder_path = folder_info["folder_path"]
        source_images = folder_info["source_images"]
    else:
        # Scan the folder directly for missing mappings
        folder_path = f"{project_folders_path}/{folder_name}"
        folder_dir = Path(folder_path)
        if folder_dir.exists():
            source_images = []
            for file in folder_dir.iterdir():
                if file.suffix.lower() in ['.jpg', '.jpeg', '.heic', '.png']:
                    source_images.append(file.name)
            source_images = source_images[:len(images)]  # Limit to available images
        else:
            print(f"Warning: Folder not found: {folder_path}")
            continue
    
    corrected_mapping[folder_name] = {
        "project_index": project_index,
        "project": project,
        "images": images,
        "folder_path": folder_path,
        "source_images": source_images[:len(images)]  # Make sure we don't exceed available images
    }

# Save corrected mapping
with open('/Volumes/T7/625industriesGIT/625industries/image_mapping_corrected.json', 'w') as f:
    json.dump(corrected_mapping, f, indent=2)

print("Corrected mapping created!")
print(f"Total projects in corrected mapping: {len(corrected_mapping)}")

# Show corrections made
print("\nCorrections made:")
print("- TXRX folder now maps to 2025-02-11 TXRX Workshop (was Nike Tea Room)")
print("- Boardroom Brunch folder now maps to 2025-02-15 All Star Weekend × Boardroom")
print("- NFL Draft Vegas 2022 folder now included")

# Show final mapping summary
print("\nFinal project mapping:")
for folder_name, mapping_info in corrected_mapping.items():
    project = mapping_info['project']
    images = mapping_info['images']
    print(f"  {folder_name}: images {images[0]}-{images[-1]} -> {project['date']} {project['event']}")

