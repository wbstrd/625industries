#!/usr/bin/env python3
"""
Quick image rotation checker - much faster approach
Just checks a few sample images and looks for obvious issues
"""

import cv2
import numpy as np
import os
from PIL import Image

def quick_face_check(image_path):
    """Quick face detection check"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            return 0, 0
        
        # Resize to speed up processing
        height, width = image.shape[:2]
        if width > 800:
            scale = 800 / width
            new_width = 800
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height))
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
        
        return len(faces), faces
    except:
        return 0, 0

def check_aspect_ratio(image_path):
    """Check if aspect ratio suggests wrong orientation"""
    try:
        with Image.open(image_path) as img:
            w, h = img.size
            ratio = w / h
            
            # Very wide images might be rotated portraits
            if ratio > 2.0:
                return "possibly_rotated_portrait"
            # Very tall images might be rotated landscapes  
            elif ratio < 0.5:
                return "possibly_rotated_landscape"
            else:
                return "normal"
    except:
        return "error"

def quick_sample_check():
    """Check just a few sample images to see if there are obvious issues"""
    print("🔍 Quick sample check...")
    
    folder = "images/medium_res"
    if not os.path.exists(folder):
        print("❌ Medium res folder not found")
        return
    
    files = [f for f in os.listdir(folder) if f.lower().endswith('.jpg')][:20]  # Just first 20
    
    issues = []
    
    for filename in files:
        print(f"  Checking {filename}...")
        path = os.path.join(folder, filename)
        
        # Quick aspect ratio check
        aspect_issue = check_aspect_ratio(path)
        if aspect_issue != "normal":
            issues.append(f"{filename}: {aspect_issue}")
        
        # Quick face check for people photos
        face_count, _ = quick_face_check(path)
        if face_count > 0:
            print(f"    Found {face_count} faces")
    
    if issues:
        print(f"\n⚠️  Potential orientation issues found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print(f"\n✅ No obvious orientation issues in sample")

def manual_review_mode():
    """Create a simple manual review"""
    print("\n🎯 Manual review mode - let's check specific images you're concerned about")
    
    folder = "images/medium_res"
    
    while True:
        img_num = input("\nEnter image number to check (or 'quit'): ").strip()
        
        if img_num.lower() == 'quit':
            break
            
        try:
            img_num = int(img_num)
            filename = f"img{img_num:03d}-med.jpg"
            path = os.path.join(folder, filename)
            
            if not os.path.exists(path):
                print(f"❌ {filename} not found")
                continue
            
            # Show image info
            with Image.open(path) as img:
                w, h = img.size
                ratio = w / h
                print(f"📐 {filename}: {w}×{h} (ratio: {ratio:.2f})")
                
                if ratio > 2:
                    print("  ⚠️  Very wide - might be rotated portrait")
                elif ratio < 0.5:
                    print("  ⚠️  Very tall - might be rotated landscape")
                else:
                    print("  ✅ Normal aspect ratio")
            
            # Face check
            faces, _ = quick_face_check(path)
            if faces > 0:
                print(f"  👥 Found {faces} faces")
            
            # Ask user
            action = input("  Rotate? (90/180/270/n): ").strip()
            
            if action in ['90', '180', '270']:
                rotation = int(action)
                print(f"  🔄 Rotating {filename} by {rotation}°...")
                
                # Apply to all resolutions
                base_num = f"{img_num:03d}"
                files_to_rotate = [
                    (f"images/high_res/img{base_num}.jpg", ""),
                    (f"images/high_res_1200/img{base_num}-high.jpg", ""),
                    (f"images/medium_res/img{base_num}-med.jpg", ""),
                    (f"images/small_res/img{base_num}-small.jpg", ""),
                    (f"images/low_res/img{base_num}-low.jpg", "")
                ]
                
                for file_path, suffix in files_to_rotate:
                    if os.path.exists(file_path):
                        try:
                            with Image.open(file_path) as img:
                                if rotation == 90:
                                    rotated = img.rotate(-90, expand=True)
                                elif rotation == 180:
                                    rotated = img.rotate(180, expand=True)
                                elif rotation == 270:
                                    rotated = img.rotate(90, expand=True)
                                
                                rotated.save(file_path, quality=95)
                                print(f"    ✅ Rotated {os.path.basename(file_path)}")
                        except Exception as e:
                            print(f"    ❌ Failed: {e}")
                
        except ValueError:
            print("❌ Please enter a valid number")

def main():
    print("⚡ Quick Image Rotation Checker")
    
    # First do a quick sample check
    quick_sample_check()
    
    # Then offer manual review
    review = input("\n❓ Want to manually review specific images? (y/n): ").lower()
    if review == 'y':
        manual_review_mode()
    
    print("\n🎉 Done!")

if __name__ == "__main__":
    main()
