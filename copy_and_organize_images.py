#!/usr/bin/env python3
"""
Copy and Organize Images Script for 625 Industries
Copies images from project folders to numbered system and updates HTML
"""

import os
import json
import shutil
from pathlib import Path
from PIL import Image
import pillow_heif

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

# Paths
MAPPING_FILE = "/Volumes/T7/625industriesGIT/625industries/image_mapping.json"
IMAGES_PATH = "/Volumes/T7/625industriesGIT/625industries/images"
HTML_FILE = "/Volumes/T7/625industriesGIT/625industries/index.html"

def load_mapping():
    """Load the image mapping from JSON file"""
    with open(MAPPING_FILE, 'r') as f:
        return json.load(f)

def convert_heic_to_jpg(heic_path, jpg_path):
    """Convert HEIC file to JPG"""
    try:
        # Open HEIC file
        image = Image.open(heic_path)
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'LA'):
            # Create a white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
            else:
                background.paste(image)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save as JPG
        image.save(jpg_path, 'JPEG', quality=95)
        return True
    except Exception as e:
        print(f"Error converting {heic_path}: {e}")
        return False

def create_resized_versions(source_path, base_name, image_num):
    """Create all the different resolution versions of an image"""
    resolutions = {
        'low_res': (400, 400, '-low'),
        'small_res': (600, 600, '-small'),
        'medium_res': (800, 800, '-med'),
        'high_res_1200': (1200, 1200, '-high'),
        'high_res': (2000, 2000, '')
    }
    
    try:
        # Open source image
        if source_path.suffix.lower() in ['.heic']:
            # For HEIC files, use pillow_heif
            image = Image.open(source_path)
        else:
            image = Image.open(source_path)
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[-1])
            else:
                background.paste(image)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Create each resolution
        for res_folder, (max_width, max_height, suffix) in resolutions.items():
            # Calculate new size maintaining aspect ratio
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Create output path
            output_dir = Path(IMAGES_PATH) / res_folder
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / f"{base_name}{suffix}.jpg"
            
            # Save image
            image.save(output_file, 'JPEG', quality=95)
            
            print(f"  Created: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error processing {source_path}: {e}")
        return False

def copy_and_organize_images(mapping):
    """Copy images from project folders to numbered system"""
    print("Copying and organizing images...")
    
    for folder_name, mapping_info in mapping.items():
        print(f"\nProcessing: {folder_name}")
        
        source_folder = Path(mapping_info['folder_path'])
        source_images = mapping_info['source_images']
        target_image_numbers = mapping_info['images']
        
        for i, (source_image, image_num) in enumerate(zip(source_images, target_image_numbers)):
            source_path = source_folder / source_image
            
            if not source_path.exists():
                print(f"  Warning: Source image not found: {source_path}")
                continue
            
            print(f"  Processing image {image_num}: {source_image}")
            
            # Create base name for numbered image
            base_name = f"img{image_num:03d}"
            
            # Create all resolution versions
            success = create_resized_versions(source_path, base_name, image_num)
            
            if success:
                print(f"  Successfully created all versions for image {image_num}")
            else:
                print(f"  Failed to process image {image_num}")

def update_html_project_mappings(mapping):
    """Update the HTML file with correct project mappings"""
    print("\nUpdating HTML file with new mappings...")
    
    # Create new project data structure
    new_projects = {
        "2018": [],
        "2019": [],
        "2020": [],
        "COVID": [],
        "2022": [],
        "2023": [],
        "2024": [],
        "2025": []
    }
    
    # Process each mapped project
    for folder_name, mapping_info in mapping.items():
        project = mapping_info['project']
        images = mapping_info['images']
        
        # Determine year/category
        date = project['date']
        year = date[:4]
        
        # Handle special COVID category
        if year in ['2020', '2021']:
            category = "COVID"
        else:
            category = year
        
        # Create project entry
        project_entry = {
            "title": project['event'].upper(),
            "date": date.replace('-', '.'),
            "location": project['city'].upper(),
            "description": f"{project['client']} {project['event']} event in {project['city']}.",
            "images": images
        }
        
        if category in new_projects:
            new_projects[category].append(project_entry)
    
    # Read current HTML file
    with open(HTML_FILE, 'r') as f:
        html_content = f.read()
    
    # Convert new_projects to JavaScript format
    js_projects = "const projects = " + json.dumps(new_projects, indent=2) + ";"
    
    # Replace the projects constant in HTML
    import re
    pattern = r'const projects = \{.*?\};'
    replacement = js_projects
    
    new_html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Write updated HTML file
    with open(HTML_FILE, 'w') as f:
        f.write(new_html_content)
    
    print("HTML file updated successfully!")

def main():
    """Main function"""
    print("Loading image mapping...")
    mapping = load_mapping()
    
    print(f"Found {len(mapping)} mapped projects")
    
    # Install required packages if not available
    try:
        import pillow_heif
    except ImportError:
        print("Installing pillow-heif for HEIC support...")
        os.system("pip3 install pillow-heif")
        import pillow_heif
        pillow_heif.register_heif_opener()
    
    # Copy and organize images
    copy_and_organize_images(mapping)
    
    # Update HTML file
    update_html_project_mappings(mapping)
    
    print("\n✅ Image organization complete!")
    print("Your website should now display the correct images for each project.")

if __name__ == "__main__":
    main()
