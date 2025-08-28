#!/usr/bin/env python3
"""
Restore Real Photos from 625 Backup Folder
Copy the original numbered photos to replace grey placeholders
"""

import shutil
import os
from pathlib import Path
from PIL import Image

BACKUP_625_PATH = "/Volumes/T7/625"

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

def restore_photos():
    """Restore real photos from 625 backup folder"""
    
    print("🔄 RESTORING REAL PHOTOS FROM 625 BACKUP FOLDER")
    print("=" * 60)
    
    resolutions = {
        'low_res': (150, '-low'),
        'small_res': (300, '-small'), 
        'medium_res': (600, '-med'),
        'high_res_1200': (1200, '-high'),
        'high_res': (2000, '')
    }
    
    # We know we need photos for positions 1-96 based on our simple mapping
    total_restored = 0
    
    for img_num in range(1, 97):  # images 1-96
        backup_path = Path(BACKUP_625_PATH) / f"img{img_num:03d}.jpg"
        
        if backup_path.exists():
            print(f"📸 Restoring img{img_num:03d} from backup")
            
            # Create all resolution versions
            for res_folder, (size, suffix) in resolutions.items():
                target_filename = f"img{img_num:03d}{suffix}.jpg"
                target_path = Path(f"images/{res_folder}/{target_filename}")
                
                # Resize and save
                if resize_image(backup_path, target_path, size):
                    total_restored += 1
                else:
                    print(f"   ⚠️  Failed to resize img{img_num:03d} for {res_folder}")
        else:
            print(f"   ❌ No backup found for img{img_num:03d}")
    
    print(f"\n✅ RESTORATION COMPLETE!")
    print(f"📊 Total image files restored: {total_restored}")
    print(f"🎯 Real photos from 625 backup now replace grey placeholders")

if __name__ == "__main__":
    restore_photos()
