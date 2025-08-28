#!/usr/bin/env python3
"""
Check image rotations project by project to avoid overwhelming the system
"""

import cv2
import numpy as np
from PIL import Image
import os
import json
import time

# Project data from your index_with_carousel.html
projects = {
    "2018": [
        {"title": "AIR MAX DAY", "date": "03.26.2018", "location": "WILLIAMSBURG, BROOKLYN", "images": [1, 2, 3, 4, 5]},
        {"title": "NIKE AIR MAX 90 CUSTOM", "date": "07.15.2018", "location": "MIAMI BEACH", "images": [6, 7, 8]},
        {"title": "LEVI'S × NIKE JORDAN 4 CUSTOM", "date": "09.12.2018", "location": "BROOKLYN", "images": [9, 10]},
        {"title": "ROLLING LOUD FESTIVAL", "date": "12.14.2018", "location": "LOS ANGELES", "images": [11, 12, 13, 14, 15]},
        {"title": "CUSTOM SNEAKER WORKSHOP", "date": "11.20.2018", "location": "PARIS", "images": [16, 17, 18, 19, 20]}
    ],
    "2019": [
        {"title": "COACHELLA FESTIVAL ACTIVATION", "date": "04.14.2019", "location": "INDIO, CALIFORNIA", "images": [21, 22, 23, 24, 25]},
        {"title": "NIKE AIR FORCE 1 CUSTOM", "date": "06.10.2019", "location": "NEW YORK CITY", "images": [26, 27, 28]},
        {"title": "LEVI'S DENIM CUSTOMIZATION", "date": "08.22.2019", "location": "SAN FRANCISCO", "images": [29, 30, 31]},
        {"title": "BURNING MAN FESTIVAL", "date": "08.30.2019", "location": "BLACK ROCK CITY, NEVADA", "images": [32, 33, 34]}
    ],
    "2020": [
        {"title": "VIRTUAL SNEAKER DESIGN", "date": "03.15.2020", "location": "REMOTE", "images": [35, 36, 37, 38, 39]},
        {"title": "NIKE DUNK CUSTOM", "date": "07.04.2020", "location": "MIAMI", "images": [40, 41, 42, 43]},
        {"title": "LEVI'S × JORDAN COLLABORATION", "date": "10.12.2020", "location": "LOS ANGELES", "images": [44, 45, 46, 47, 48, 49, 50]}
    ],
    "2021": [
        {"title": "TRAVIS SCOTT × NIKE COLLABORATION", "date": "05.15.2021", "location": "HOUSTON", "images": [51, 52, 53, 54, 55]},
        {"title": "LEVI'S 501 FESTIVAL", "date": "08.20.2021", "location": "SAN FRANCISCO", "images": [56, 57, 58, 59]},
        {"title": "NIKE AIR MAX COLLECTION", "date": "11.11.2021", "location": "NEW YORK CITY", "images": [60, 61, 62, 63, 64, 65]}
    ],
    "2024": [
        {"title": "SUPER BOWL LVIII NIKEBYYOU", "date": "2024.02.06", "location": "LAS VEGAS", "images": [66, 67, 68, 69, 70, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140]},
        {"title": "ROLLING LOUD × MODELO", "date": "2024.03.22", "location": "LOS ANGELES", "images": [71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86]},
        {"title": "LEVI'S × JORDAN 4 TRAVIS SCOTT", "date": "2024.04.15", "location": "CHICAGO", "images": [87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127]}
    ]
}

def sensitive_face_detection_single(img_num):
    """Sensitive face detection for a single image"""
    filename = f"img{img_num:03d}-med.jpg"
    path = os.path.join("images/medium_res", filename)
    
    if not os.path.exists(path):
        return None, f"File not found: {filename}"
    
    try:
        image = cv2.imread(path)
        if image is None:
            return None, f"Could not load {filename}"
        
        # Quick face detection with default cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        orientations = {
            0: image,
            90: cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE),
            180: cv2.rotate(image, cv2.ROTATE_180),
            270: cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        }
        
        best_rotation = 0
        max_faces = 0
        
        for rotation, rotated_img in orientations.items():
            gray = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(20, 20))
            face_count = len(faces)
            
            if face_count > max_faces:
                max_faces = face_count
                best_rotation = rotation
        
        if max_faces > 0 and best_rotation != 0:
            return best_rotation, f"Found {max_faces} faces at {best_rotation}°"
        else:
            return 0, f"No rotation needed (faces: {max_faces})"
            
    except Exception as e:
        return None, f"Error analyzing {filename}: {e}"

def apply_rotation_to_image(img_num, rotation):
    """Apply rotation to specific image across all resolutions"""
    folders = [
        ("images/high_res", ""),
        ("images/high_res_1200", "-high"),
        ("images/medium_res", "-med"),
        ("images/small_res", "-small"),
        ("images/low_res", "-low")
    ]
    
    success_count = 0
    
    for folder_path, suffix in folders:
        if suffix:
            target_file = f"img{img_num:03d}{suffix}.jpg"
        else:
            target_file = f"img{img_num:03d}.jpg"
        
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
                    success_count += 1
                    
            except Exception as e:
                print(f"    ❌ Failed {target_file}: {e}")
        
    return success_count

def process_project(year, project, project_num, total_projects):
    """Process a single project"""
    print(f"\n{'='*60}")
    print(f"📁 PROJECT {project_num}/{total_projects}: {project['title']}")
    print(f"📅 {project['date']} - {project['location']}")
    print(f"🖼️  Images: {len(project['images'])} photos")
    print(f"{'='*60}")
    
    rotation_suggestions = []
    
    for i, img_num in enumerate(project['images']):
        print(f"  ({i+1}/{len(project['images'])}) Checking img{img_num:03d}...", end="")
        
        rotation, reason = sensitive_face_detection_single(img_num)
        
        if rotation is None:
            print(f" ❌ {reason}")
        elif rotation != 0:
            print(f" 🔄 NEEDS {rotation}° rotation - {reason}")
            rotation_suggestions.append({
                'img_num': img_num,
                'rotation': rotation,
                'reason': reason
            })
        else:
            print(f" ✅ OK - {reason}")
        
        # Small delay to not overwhelm system
        time.sleep(0.1)
    
    # Apply rotations for this project if any found
    if rotation_suggestions:
        print(f"\n📋 Found {len(rotation_suggestions)} images needing rotation in this project:")
        for suggestion in rotation_suggestions:
            print(f"  img{suggestion['img_num']:03d}: {suggestion['rotation']}° - {suggestion['reason']}")
        
        apply_project = input(f"\n❓ Apply rotations for this project? (y/n/skip_all): ").lower()
        
        if apply_project == 'y':
            for suggestion in rotation_suggestions:
                print(f"  🔄 Rotating img{suggestion['img_num']:03d} by {suggestion['rotation']}°...")
                success = apply_rotation_to_image(suggestion['img_num'], suggestion['rotation'])
                if success == 5:
                    print(f"    ✅ Applied to all {success} resolutions")
                else:
                    print(f"    ⚠️  Applied to {success}/5 resolutions")
        elif apply_project == 'skip_all':
            return False  # Signal to stop processing
    else:
        print(f"\n✅ No rotations needed for this project")
    
    return True  # Continue processing

def main():
    print("🔄 Project-by-Project Rotation Checker")
    print("Analyzing images project by project to avoid system overload")
    
    # Count total projects
    total_projects = sum(len(projects[year]) for year in projects)
    project_counter = 0
    
    for year in sorted(projects.keys()):
        print(f"\n🗓️  YEAR: {year}")
        
        for project in projects[year]:
            project_counter += 1
            
            # Process this project
            continue_processing = process_project(year, project, project_counter, total_projects)
            
            if not continue_processing:
                print(f"\n⏹️  Stopping at user request")
                return
            
            # Pause between projects
            if project_counter < total_projects:
                time.sleep(1)
                input(f"\n⏳ Press Enter to continue to next project...")
    
    print(f"\n🎉 Completed analysis of all {total_projects} projects!")

if __name__ == "__main__":
    main()
