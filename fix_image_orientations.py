#!/usr/bin/env python3
"""
Auto-fix image orientations based on EXIF data
This script will detect and correct rotated images in all resolution folders
"""

import os
from PIL import Image, ImageOps
import shutil
from pathlib import Path

def fix_image_orientation(image_path):
    """Fix image orientation based on EXIF data"""
    try:
        with Image.open(image_path) as img:
            # Get original orientation
            original_orientation = getattr(img, '_getexif', lambda: None)()
            if original_orientation:
                orientation = original_orientation.get(274)  # 274 is the EXIF orientation tag
                if orientation:
                    print(f"  Original orientation: {orientation}")
            
            # Use ImageOps.exif_transpose to automatically fix orientation
            fixed_img = ImageOps.exif_transpose(img)
            
            # Check if image was actually rotated
            if fixed_img.size != img.size:
                print(f"  ✅ Fixed orientation: {img.size} -> {fixed_img.size}")
                # Save the corrected image
                fixed_img.save(image_path, quality=95, optimize=True)
                return True
            else:
                print(f"  ✓ Already correct orientation")
                return False
                
    except Exception as e:
        print(f"  ❌ Error processing {image_path}: {e}")
        return False

def process_folder(folder_path):
    """Process all images in a folder"""
    print(f"\n📁 Processing folder: {folder_path}")
    
    if not os.path.exists(folder_path):
        print(f"  ❌ Folder doesn't exist: {folder_path}")
        return
    
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print(f"  No images found in {folder_path}")
        return
    
    fixed_count = 0
    total_count = len(image_files)
    
    for filename in sorted(image_files):
        image_path = os.path.join(folder_path, filename)
        print(f"  🔍 Checking {filename}...")
        
        if fix_image_orientation(image_path):
            fixed_count += 1
    
    print(f"  📊 Fixed {fixed_count}/{total_count} images in this folder")
    return fixed_count

def main():
    print("🔄 Auto-fixing image orientations...")
    
    # Define all image folders
    image_folders = [
        "images/high_res",
        "images/high_res_1200", 
        "images/medium_res",
        "images/small_res",
        "images/low_res"
    ]
    
    total_fixed = 0
    
    for folder in image_folders:
        folder_path = os.path.join(os.getcwd(), folder)
        fixed_count = process_folder(folder_path)
        if fixed_count:
            total_fixed += fixed_count
    
    print(f"\n🎉 COMPLETED! Fixed orientation for {total_fixed} images total")
    
    if total_fixed > 0:
        print("\n💡 Note: The fixes have been applied to all resolution versions.")
        print("   You may want to commit these changes to git.")

if __name__ == "__main__":
    main()
