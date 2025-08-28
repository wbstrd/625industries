#!/usr/bin/env python3
"""
Check a specific image for rotation needs
"""

import cv2
import numpy as np
from PIL import Image
import os

def analyze_specific_image(img_num):
    """Analyze a specific image number"""
    
    # Check medium res version
    filename = f"img{img_num:03d}-med.jpg"
    path = os.path.join("images/medium_res", filename)
    
    if not os.path.exists(path):
        print(f"❌ {filename} not found")
        return
    
    print(f"🔍 Analyzing {filename}...")
    
    # Check basic info
    try:
        with Image.open(path) as img:
            w, h = img.size
            ratio = w / h
            print(f"📐 Dimensions: {w}×{h} (ratio: {ratio:.2f})")
            
            if ratio > 1.5:
                print("  📏 Landscape orientation")
            elif ratio < 0.67:
                print("  📏 Portrait orientation")
            else:
                print("  📏 Square-ish orientation")
    except Exception as e:
        print(f"❌ Error reading image: {e}")
        return
    
    # Face detection test in all orientations
    try:
        image = cv2.imread(path)
        if image is None:
            print("❌ Could not load image for face analysis")
            return
        
        # Resize for faster processing
        height, width = image.shape[:2]
        if width > 600:
            scale = 600 / width
            image = cv2.resize(image, (int(width * scale), int(height * scale)))
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        orientations = {
            "Original (0°)": image,
            "Rotated 90° CW": cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE),
            "Rotated 180°": cv2.rotate(image, cv2.ROTATE_180),
            "Rotated 270° CW": cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        }
        
        print(f"\n👥 Face detection results:")
        face_results = {}
        
        for name, rotated_img in orientations.items():
            gray = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20, 20))
            face_count = len(faces)
            face_results[name] = face_count
            
            if face_count > 0:
                print(f"  ✅ {name}: {face_count} faces detected")
            else:
                print(f"  ❌ {name}: no faces")
        
        # Determine best orientation
        best_orientation = max(face_results, key=face_results.get)
        max_faces = face_results[best_orientation]
        
        if max_faces > 0:
            if best_orientation != "Original (0°)":
                rotation_needed = best_orientation.split("Rotated ")[1].split(" ")[0]
                print(f"\n🔄 RECOMMENDATION: Rotate by {rotation_needed} for better face detection")
                
                # Ask user if they want to apply the rotation
                apply = input(f"\n❓ Apply {rotation_needed} rotation to all resolutions? (y/n): ").lower()
                if apply == 'y':
                    apply_rotation_to_image(img_num, rotation_needed)
                    
            else:
                print(f"\n✅ RECOMMENDATION: Image orientation looks correct")
        else:
            print(f"\n🤷 No faces detected in any orientation - image might not contain people")
            print(f"   Manual review recommended")
            
    except Exception as e:
        print(f"❌ Error in face analysis: {e}")

def apply_rotation_to_image(img_num, rotation):
    """Apply rotation to specific image across all resolutions"""
    
    # Define resolution folders and their suffixes
    folders = [
        ("images/high_res", ""),
        ("images/high_res_1200", "-high"),
        ("images/medium_res", "-med"),
        ("images/small_res", "-small"),
        ("images/low_res", "-low")
    ]
    
    print(f"\n🔄 Applying {rotation} rotation to img{img_num:03d} across all resolutions...")
    
    for folder_path, suffix in folders:
        if suffix:
            target_file = f"img{img_num:03d}{suffix}.jpg"
        else:
            target_file = f"img{img_num:03d}.jpg"
        
        full_path = os.path.join(folder_path, target_file)
        
        if os.path.exists(full_path):
            try:
                with Image.open(full_path) as img:
                    if rotation == "90°":
                        rotated = img.rotate(-90, expand=True)
                    elif rotation == "180°":
                        rotated = img.rotate(180, expand=True)
                    elif rotation == "270°":
                        rotated = img.rotate(90, expand=True)
                    
                    rotated.save(full_path, quality=95)
                    print(f"  ✅ Rotated {folder_path}/{target_file}")
                    
            except Exception as e:
                print(f"  ❌ Failed {target_file}: {e}")
        else:
            print(f"  ⚠️  Not found: {target_file}")
    
    print(f"✅ Rotation complete for img{img_num:03d}")

def main():
    analyze_specific_image(135)

if __name__ == "__main__":
    main()
