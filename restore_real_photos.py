#!/usr/bin/env python3
"""
Restore Real Photos from WeTransfer Project Folders
Replace the grey placeholders with actual project photos
"""

import json
import shutil
import os
from pathlib import Path
from PIL import Image

# Path to WeTransfer folder with project-sorted photos
WETRANSFER_PATH = "/Volumes/T7/wetransfer_arizona-february-2023-undefeated_2025-05-29_0306"
BACKUP_625_PATH = "/Volumes/T7/625"

# Load our corrected mapping to know which photos go where
with open('/Volumes/T7/625industriesGIT/625industries/image_mapping_corrected.json', 'r') as f:
    mapping = json.load(f)

def resize_image(input_path, output_path, target_size):
    """Resize image to target size"""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize maintaining aspect ratio
            img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
            
            # Create a square image with white background
            square_img = Image.new('RGB', (target_size, target_size), 'white')
            
            # Center the image
            x = (target_size - img.width) // 2
            y = (target_size - img.height) // 2
            square_img.paste(img, (x, y))
            
            # Save
            square_img.save(output_path, 'JPEG', quality=85)
            return True
    except Exception as e:
        print(f"Error resizing {input_path}: {e}")
        return False

def get_project_photos(folder_name):
    """Get photo files from a project folder"""
    folder_path = Path(WETRANSFER_PATH) / folder_name
    if not folder_path.exists():
        print(f"Folder not found: {folder_path}")
        return []
    
    # Get all image files
    photo_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.tiff', '.tif'}
    photos = []
    
    for file_path in folder_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in photo_extensions:
            photos.append(file_path)
    
    # Sort by name
    photos.sort(key=lambda x: x.name.lower())
    return photos

def restore_photos():
    """Restore real photos to replace grey placeholders"""
    
    print("🔄 RESTORING REAL PHOTOS FROM PROJECT FOLDERS")
    print("=" * 60)
    
    resolutions = {
        'low_res': (150, '-low'),
        'small_res': (300, '-small'), 
        'medium_res': (600, '-med'),
        'high_res_1200': (1200, '-high'),
        'high_res': (2000, '')
    }
    
    total_restored = 0
    
    for folder_name, mapping_info in mapping.items():
        print(f"\n📁 Processing: {folder_name}")
        
        # Get photos from project folder
        project_photos = get_project_photos(folder_name)
        target_images = mapping_info['images']
        
        if not project_photos:
            print(f"   ⚠️  No photos found in folder")
            continue
            
        print(f"   📸 Found {len(project_photos)} photos")
        print(f"   🎯 Target positions: {target_images}")
        
        # Copy photos to target positions
        for i, target_img_num in enumerate(target_images):
            if i < len(project_photos):
                source_photo = project_photos[i]
                print(f"   📋 img{target_img_num:03d} ← {source_photo.name}")
                
                # Create all resolution versions
                for res_folder, (size, suffix) in resolutions.items():
                    target_filename = f"img{target_img_num:03d}{suffix}.jpg"
                    target_path = Path(f"images/{res_folder}/{target_filename}")
                    
                    # Resize and save
                    if resize_image(source_photo, target_path, size):
                        total_restored += 1
                    else:
                        # Fallback: try copying from 625 folder if available
                        backup_path = Path(BACKUP_625_PATH) / f"img{target_img_num:03d}.jpg"
                        if backup_path.exists():
                            print(f"   🔄 Using backup from 625 folder")
                            resize_image(backup_path, target_path, size)
            else:
                print(f"   ⚠️  Not enough photos for img{target_images[i]:03d}")
    
    print(f"\n✅ RESTORATION COMPLETE!")
    print(f"📊 Total image files restored: {total_restored}")
    print(f"🎯 Real photos now replace grey placeholders")

if __name__ == "__main__":
    restore_photos()
