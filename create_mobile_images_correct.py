#!/usr/bin/env python3

import os
from PIL import Image

def create_mobile_optimized_images():
    """Create ultra-small mobile images for all 380 images"""
    
    # Source and target directories
    source_dir = "/Volumes/T7/625industriesGIT/625industries/images/low_res"
    target_dir = "/Volumes/T7/625industriesGIT/625industries/images/mobile_res"
    
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Mobile optimization settings - even smaller for mobile
    MOBILE_MAX_SIZE = (120, 120)  # Even smaller for ultra-fast loading
    MOBILE_QUALITY = 50  # Lower quality for smaller file size
    
    print("Creating mobile-optimized images for all photos...")
    processed = 0
    errors = 0
    
    # Get all image files from source directory
    image_files = [f for f in sorted(os.listdir(source_dir)) if f.lower().endswith(('.jpg', '.jpeg'))]
    print(f"Found {len(image_files)} images to process")
    
    # Process each image
    for filename in image_files:
        source_path = os.path.join(source_dir, filename)
        
        # Create mobile filename (replace -low with -mobile)
        mobile_filename = filename.replace('-low', '-mobile')
        target_path = os.path.join(target_dir, mobile_filename)
        
        try:
            # Open and resize image
            with Image.open(source_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Resize maintaining aspect ratio
                img.thumbnail(MOBILE_MAX_SIZE, Image.Resampling.LANCZOS)
                
                # Save with optimized settings
                img.save(target_path, 
                        'JPEG', 
                        quality=MOBILE_QUALITY, 
                        optimize=True,
                        progressive=True)
                
                processed += 1
                if processed % 50 == 0:
                    print(f"✓ Processed {processed}/{len(image_files)} images...")
                    
        except Exception as e:
            print(f"✗ Error processing {filename}: {e}")
            errors += 1
    
    print(f"\n✅ Successfully created {processed} mobile images")
    if errors > 0:
        print(f"❌ {errors} errors occurred")
    
    # Show size comparison
    original_size = sum(os.path.getsize(os.path.join(source_dir, f)) 
                       for f in image_files)
    mobile_size = sum(os.path.getsize(os.path.join(target_dir, f)) 
                     for f in os.listdir(target_dir) if f.endswith('.jpg'))
    
    print(f"📊 Size comparison:")
    print(f"   Low-res total: {original_size / (1024*1024):.1f} MB")
    print(f"   Mobile-res total: {mobile_size / (1024*1024):.1f} MB")
    print(f"   Space saved: {((original_size - mobile_size) / original_size) * 100:.1f}%")

if __name__ == "__main__":
    create_mobile_optimized_images()
