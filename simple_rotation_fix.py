#!/usr/bin/env python3
"""
Simple rotation fixer - analyze medium res only, apply to all
"""

import cv2
import os
from PIL import Image

def detect_faces_in_orientations(image_path):
    """Test all 4 orientations and see which has most faces"""
    try:
        # Load and resize for speed
        image = cv2.imread(image_path)
        if image is None:
            return 0, "Could not load"
        
        height, width = image.shape[:2]
        if width > 600:
            scale = 600 / width
            image = cv2.resize(image, (int(width * scale), int(height * scale)))
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        results = {}
        
        # Test original
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20, 20))
        results[0] = len(faces)
        
        # Test 90° rotation
        rotated_90 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        gray = cv2.cvtColor(rotated_90, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20, 20))
        results[90] = len(faces)
        
        # Test 180° rotation
        rotated_180 = cv2.rotate(image, cv2.ROTATE_180)
        gray = cv2.cvtColor(rotated_180, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20, 20))
        results[180] = len(faces)
        
        # Test 270° rotation
        rotated_270 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        gray = cv2.cvtColor(rotated_270, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20, 20))
        results[270] = len(faces)
        
        # Find best orientation
        best_angle = max(results, key=results.get)
        max_faces = results[best_angle]
        
        # Only suggest rotation if significantly better
        if max_faces > 0 and best_angle != 0:
            return best_angle, f"Found {max_faces} faces at {best_angle}°"
        else:
            return 0, f"No clear improvement (faces: {results})"
            
    except Exception as e:
        return 0, f"Error: {e}"

def check_aspect_ratio(image_path):
    """Quick aspect ratio check"""
    try:
        with Image.open(image_path) as img:
            w, h = img.size
            ratio = w / h
            
            # Very unusual ratios might indicate rotation issues
            if ratio > 3.0:
                return 90, f"Very wide ({ratio:.1f}:1) - likely rotated portrait"
            elif ratio < 0.33:
                return 90, f"Very tall (1:{1/ratio:.1f}) - likely rotated landscape"
            else:
                return 0, f"Normal ratio ({ratio:.1f}:1)"
    except Exception as e:
        return 0, f"Error: {e}"

def analyze_medium_res():
    """Analyze all images in medium res folder"""
    print("🔍 Analyzing medium_res folder...")
    
    folder = "images/medium_res"
    if not os.path.exists(folder):
        print("❌ medium_res folder not found")
        return []
    
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith('.jpg')])
    print(f"📊 Found {len(files)} images to analyze")
    
    rotation_suggestions = []
    
    for i, filename in enumerate(files):
        print(f"  ({i+1}/{len(files)}) Checking {filename}...")
        
        path = os.path.join(folder, filename)
        
        # First check aspect ratio (fast)
        aspect_rotation, aspect_reason = check_aspect_ratio(path)
        
        # If aspect ratio suggests rotation, check faces to confirm
        if aspect_rotation != 0:
            face_rotation, face_reason = detect_faces_in_orientations(path)
            
            if face_rotation != 0:
                rotation_suggestions.append({
                    'file': filename,
                    'rotation': face_rotation,
                    'reason': f"Aspect: {aspect_reason}, Faces: {face_reason}"
                })
                print(f"    🔄 SUGGEST {face_rotation}° rotation - {face_reason}")
            else:
                # No faces found, go with aspect ratio suggestion
                rotation_suggestions.append({
                    'file': filename,
                    'rotation': aspect_rotation,
                    'reason': aspect_reason
                })
                print(f"    🔄 SUGGEST {aspect_rotation}° rotation - {aspect_reason}")
        else:
            print(f"    ✅ Looks good - {aspect_reason}")
    
    return rotation_suggestions

def apply_rotations_all_res(suggestions):
    """Apply rotations to all resolution folders"""
    if not suggestions:
        print("✅ No rotations needed!")
        return
    
    print(f"\n📋 Rotation plan:")
    for suggestion in suggestions:
        print(f"  {suggestion['file']}: {suggestion['rotation']}° - {suggestion['reason']}")
    
    confirm = input(f"\n❓ Apply these {len(suggestions)} rotations to ALL resolution folders? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    # Define resolution folders and their suffixes
    folders = [
        ("images/high_res", ""),
        ("images/high_res_1200", "-high"),
        ("images/medium_res", "-med"),
        ("images/small_res", "-small"),
        ("images/low_res", "-low")
    ]
    
    print(f"\n🔄 Applying rotations to all resolutions...")
    
    for suggestion in suggestions:
        # Extract image number from filename (e.g., img001-med.jpg -> 001)
        img_num = suggestion['file'].replace('img', '').replace('-med.jpg', '')
        rotation = suggestion['rotation']
        
        print(f"\n  📸 Rotating img{img_num} by {rotation}°...")
        
        for folder_path, suffix in folders:
            if suffix:
                target_file = f"img{img_num}{suffix}.jpg"
            else:
                target_file = f"img{img_num}.jpg"
            
            full_path = os.path.join(folder_path, target_file)
            
            if os.path.exists(full_path):
                try:
                    with Image.open(full_path) as img:
                        if rotation == 90:
                            rotated = img.rotate(-90, expand=True)
                        elif rotation == 180:
                            rotated = img.rotate(180, expand=True)
                        elif rotation == 270:
                            rotated = img.rotate(90, expand=True)
                        
                        rotated.save(full_path, quality=95)
                        print(f"    ✅ {folder_path}/{target_file}")
                        
                except Exception as e:
                    print(f"    ❌ Failed {target_file}: {e}")
            else:
                print(f"    ⚠️  Not found: {target_file}")

def main():
    print("🔄 Simple Image Rotation Fixer")
    print("Analyzing medium_res only, then applying to all resolutions\n")
    
    # Analyze medium res folder
    suggestions = analyze_medium_res()
    
    # Apply to all resolutions
    apply_rotations_all_res(suggestions)
    
    print(f"\n🎉 Done! Processed {len(suggestions)} rotations")

if __name__ == "__main__":
    main()
