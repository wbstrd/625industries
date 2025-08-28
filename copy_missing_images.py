#!/usr/bin/env python3
"""
Copy Missing Images Script
Copies the NFL Draft and Boardroom Brunch images that weren't processed initially
"""

import json
from pathlib import Path
from PIL import Image
import pillow_heif

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

# Load the corrected mapping
with open('/Volumes/T7/625industriesGIT/625industries/image_mapping_corrected.json', 'r') as f:
    corrected_mapping = json.load(f)

# Load original mapping to see what was already processed
with open('/Volumes/T7/625industriesGIT/625industries/image_mapping.json', 'r') as f:
    original_mapping = json.load(f)

IMAGES_PATH = "/Volumes/T7/625industriesGIT/625industries/images"

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

# Find folders that need new images
folders_to_process = []
for folder_name, mapping_info in corrected_mapping.items():
    if folder_name not in original_mapping:
        folders_to_process.append(folder_name)

print(f"Processing {len(folders_to_process)} additional folders...")

for folder_name in folders_to_process:
    mapping_info = corrected_mapping[folder_name]
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

print("\n✅ Missing images processing complete!")
