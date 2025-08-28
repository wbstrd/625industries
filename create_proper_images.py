#!/usr/bin/env python3
"""
Create Proper High-Quality Images
Use T7/625 source images and create multiple resolutions WITHOUT ugly white borders
"""

import json
import shutil
import os
from pathlib import Path
from PIL import Image

# Paths
BACKUP_625_PATH = "/Volumes/T7/625"
WETRANSFER_PATH = "/Volumes/T7/wetransfer_arizona-february-2023-undefeated_2025-05-29_0306"

def create_quality_resize(input_path, output_path, target_size, maintain_aspect=True):
    """Create high-quality resize WITHOUT white borders"""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            if maintain_aspect:
                # Resize maintaining aspect ratio, crop to fit if needed
                img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
                
                # If image is smaller than target, don't upscale - just save as is
                if img.width <= target_size and img.height <= target_size:
                    img.save(output_path, 'JPEG', quality=95, optimize=True)
                else:
                    # Create center crop to exact square
                    if img.width != img.height:
                        size = min(img.width, img.height)
                        left = (img.width - size) // 2
                        top = (img.height - size) // 2
                        img = img.crop((left, top, left + size, top + size))
                    
                    # Resize to target
                    img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
                    img.save(output_path, 'JPEG', quality=95, optimize=True)
            else:
                # Direct resize
                img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
                img.save(output_path, 'JPEG', quality=95, optimize=True)
            
            return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def create_resolutions():
    """Create multiple high-quality resolutions from 625 source images"""
    
    print("🎨 CREATING HIGH-QUALITY IMAGE RESOLUTIONS")
    print("=" * 60)
    
    # High-quality resolution settings
    resolutions = {
        'low_res': (200, '-low'),      # Increased from 150
        'small_res': (400, '-small'),  # Increased from 300
        'medium_res': (800, '-med'),   # Increased from 600
        'high_res_1200': (1200, '-high'),  # Same
        'high_res': (2000, '')         # Same but with better quality
    }
    
    total_processed = 0
    
    # Process images 1-240 (more than we need, but covers all possibilities)
    for img_num in range(1, 241):
        source_path = Path(BACKUP_625_PATH) / f"img{img_num:03d}.jpg"
        
        if source_path.exists():
            print(f"📸 Processing img{img_num:03d} - Creating {len(resolutions)} resolutions")
            
            # Create all resolution versions
            for res_folder, (size, suffix) in resolutions.items():
                target_filename = f"img{img_num:03d}{suffix}.jpg"
                target_path = Path(f"images/{res_folder}/{target_filename}")
                
                # Ensure directory exists
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Create high-quality resize
                if create_quality_resize(source_path, target_path, size):
                    total_processed += 1
                else:
                    print(f"   ⚠️  Failed to process {res_folder}")
        else:
            # Stop when we run out of source images
            break
    
    print(f"\n✅ HIGH-QUALITY PROCESSING COMPLETE!")
    print(f"📊 Total image files created: {total_processed}")
    print(f"🎯 All images now have:")
    print(f"   • High quality (95% JPEG quality)")
    print(f"   • NO white borders")
    print(f"   • Proper aspect ratios")
    print(f"   • Multiple resolutions for web optimization")

if __name__ == "__main__":
    create_resolutions()
