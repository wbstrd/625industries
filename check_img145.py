#!/usr/bin/env python3
"""
Check img145 specifically and verify Super Bowl project membership
"""

import cv2
import numpy as np
from PIL import Image
import os

def analyze_img145():
    """Analyze img145 for rotation and project membership"""
    
    filename = "img145-med.jpg"
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
    except Exception as e:
        print(f"❌ Error reading image: {e}")
        return
    
    # Face detection in all orientations
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
            faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(20, 20))
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
                    apply_rotation_to_image(145, rotation_needed)
                    
            else:
                print(f"\n✅ RECOMMENDATION: Image orientation looks correct")
        else:
            print(f"\n🤷 No faces detected in any orientation")
            
    except Exception as e:
        print(f"❌ Error in face analysis: {e}")

def apply_rotation_to_image(img_num, rotation):
    """Apply rotation to specific image across all resolutions"""
    
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

def check_superbowl_project():
    """Check current Super Bowl project mapping"""
    print(f"\n📋 Current Super Bowl project in index_with_carousel.html:")
    
    try:
        with open("index_with_carousel.html", "r") as f:
            content = f.read()
            
        # Find Super Bowl project
        if "SUPER BOWL LVIII NIKEBYYOU" in content:
            # Extract the images array
            start = content.find('"SUPER BOWL LVIII NIKEBYYOU"')
            if start != -1:
                # Find the images array for this project
                images_start = content.find('"images":', start)
                if images_start != -1:
                    bracket_start = content.find('[', images_start)
                    bracket_end = content.find(']', bracket_start)
                    if bracket_start != -1 and bracket_end != -1:
                        images_str = content[bracket_start+1:bracket_end]
                        # Extract numbers
                        import re
                        numbers = re.findall(r'\d+', images_str)
                        current_images = [int(n) for n in numbers]
                        
                        print(f"  📸 Current images: {current_images}")
                        print(f"  📊 Total count: {len(current_images)}")
                        
                        if 145 in current_images:
                            print(f"  ✅ img145 is already in Super Bowl project")
                        else:
                            print(f"  ❌ img145 is NOT in Super Bowl project")
                            print(f"  💡 Should it be added?")
                            
                            add_to_superbowl = input(f"\n❓ Add img145 to Super Bowl project? (y/n): ").lower()
                            if add_to_superbowl == 'y':
                                add_img145_to_superbowl(current_images)
                        
        else:
            print(f"  ❌ Super Bowl project not found in HTML file")
            
    except Exception as e:
        print(f"❌ Error checking Super Bowl project: {e}")

def add_img145_to_superbowl(current_images):
    """Add img145 to Super Bowl project"""
    new_images = sorted(current_images + [145])
    
    print(f"🔄 Adding img145 to Super Bowl project...")
    print(f"  📸 New images list: {new_images}")
    
    try:
        with open("index_with_carousel.html", "r") as f:
            content = f.read()
        
        # Find and replace the Super Bowl images array
        old_array = str(current_images).replace(' ', '')
        new_array = str(new_images).replace(' ', '')
        
        # More precise replacement
        old_pattern = f'"images": [\n        {", ".join(map(str, current_images))}\n      ]'
        new_pattern = f'"images": [\n        {", ".join(map(str, new_images))}\n      ]'
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
        else:
            # Fallback: replace the array format
            old_fallback = f'[{", ".join(map(str, current_images))}]'
            new_fallback = f'[{", ".join(map(str, new_images))}]'
            content = content.replace(old_fallback, new_fallback)
        
        with open("index_with_carousel.html", "w") as f:
            f.write(content)
            
        print(f"  ✅ Successfully added img145 to Super Bowl project")
        
    except Exception as e:
        print(f"  ❌ Error updating HTML file: {e}")

def main():
    print("🔍 Checking img145...")
    
    # First analyze the image
    analyze_img145()
    
    # Then check Super Bowl project membership
    check_superbowl_project()

if __name__ == "__main__":
    main()
