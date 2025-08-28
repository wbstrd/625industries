#!/usr/bin/env python3
"""
More sensitive face detection for img135
"""

import cv2
import numpy as np
from PIL import Image
import os

def sensitive_face_detection(img_num):
    """More sensitive face detection with multiple cascades"""
    
    filename = f"img{img_num:03d}-med.jpg"
    path = os.path.join("images/medium_res", filename)
    
    if not os.path.exists(path):
        print(f"❌ {filename} not found")
        return
    
    print(f"🔍 Sensitive face analysis for {filename}...")
    
    try:
        image = cv2.imread(path)
        if image is None:
            print("❌ Could not load image")
            return
        
        # Try multiple face detection methods
        cascades = [
            ('Default frontal face', cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'),
            ('Alt frontal face', cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'),
            ('Alt2 frontal face', cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'),
            ('Profile face', cv2.data.haarcascades + 'haarcascade_profileface.xml')
        ]
        
        orientations = {
            "Original (0°)": image,
            "Rotated 90° CW": cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE),
            "Rotated 180°": cv2.rotate(image, cv2.ROTATE_180),
            "Rotated 270° CW": cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        }
        
        best_results = {}
        
        for orientation_name, rotated_img in orientations.items():
            print(f"\n📐 Testing {orientation_name}:")
            gray = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2GRAY)
            
            total_faces = 0
            best_method = ""
            
            for cascade_name, cascade_path in cascades:
                try:
                    if os.path.exists(cascade_path):
                        cascade = cv2.CascadeClassifier(cascade_path)
                        
                        # Try different scale factors for sensitivity
                        for scale_factor in [1.1, 1.2, 1.3]:
                            faces = cascade.detectMultiScale(
                                gray, 
                                scaleFactor=scale_factor,
                                minNeighbors=3,
                                minSize=(15, 15),  # Smaller minimum size
                                maxSize=(300, 300)
                            )
                            
                            if len(faces) > 0:
                                print(f"  ✅ {cascade_name} (scale {scale_factor}): {len(faces)} faces")
                                total_faces = max(total_faces, len(faces))
                                if len(faces) > 0:
                                    best_method = f"{cascade_name} (scale {scale_factor})"
                                break
                        
                        if total_faces == 0:
                            print(f"  ❌ {cascade_name}: no faces")
                    
                except Exception as e:
                    print(f"  ⚠️  {cascade_name}: error - {e}")
            
            best_results[orientation_name] = {
                'faces': total_faces,
                'method': best_method
            }
            
            if total_faces > 0:
                print(f"  🎯 Best for this orientation: {best_method}")
        
        # Find overall best orientation
        best_orientation = max(best_results, key=lambda k: best_results[k]['faces'])
        max_faces = best_results[best_orientation]['faces']
        
        print(f"\n📊 SUMMARY:")
        for orientation, result in best_results.items():
            if result['faces'] > 0:
                print(f"  {orientation}: {result['faces']} faces ({result['method']})")
            else:
                print(f"  {orientation}: no faces detected")
        
        if max_faces > 0:
            print(f"\n🏆 BEST ORIENTATION: {best_orientation}")
            print(f"   Method: {best_results[best_orientation]['method']}")
            
            if best_orientation != "Original (0°)":
                rotation_map = {
                    "Rotated 90° CW": "90°",
                    "Rotated 180°": "180°", 
                    "Rotated 270° CW": "270°"
                }
                suggested_rotation = rotation_map.get(best_orientation, "unknown")
                print(f"🔄 RECOMMENDATION: Rotate by {suggested_rotation}")
                
                apply = input(f"\n❓ Apply {suggested_rotation} rotation to all resolutions? (y/n): ").lower()
                if apply == 'y':
                    apply_rotation(135, suggested_rotation)
            else:
                print(f"✅ Current orientation is best")
        else:
            print(f"\n🤷 Still no faces detected with sensitive analysis")
            print(f"   This might be a product/object photo without people")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def apply_rotation(img_num, rotation):
    """Apply rotation to all resolutions"""
    folders = [
        ("images/high_res", ""),
        ("images/high_res_1200", "-high"),
        ("images/medium_res", "-med"),
        ("images/small_res", "-small"),
        ("images/low_res", "-low")
    ]
    
    print(f"\n🔄 Applying {rotation} rotation to img{img_num:03d}...")
    
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
                    print(f"  ✅ {folder_path}/{target_file}")
                    
            except Exception as e:
                print(f"  ❌ Failed {target_file}: {e}")

def main():
    sensitive_face_detection(135)

if __name__ == "__main__":
    main()
