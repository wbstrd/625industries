#!/usr/bin/env python3
"""
Smart image rotation detection using OpenCV
Uses multiple techniques: face detection, text detection, and edge analysis
"""

import cv2
import numpy as np
import os
from PIL import Image
import shutil
from pathlib import Path

def detect_faces(image):
    """Detect faces and return their orientation info"""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return len(faces), faces

def detect_text_orientation(image):
    """Detect text regions and analyze their orientation"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use EAST text detector if available, otherwise use simple edge detection
    # For now, we'll use edge-based text detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Find horizontal and vertical lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    
    horizontal_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel)
    vertical_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, vertical_kernel)
    
    h_score = np.sum(horizontal_lines) / 255
    v_score = np.sum(vertical_lines) / 255
    
    return h_score, v_score

def analyze_dominant_edges(image):
    """Analyze edge directions to guess orientation"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Use Hough line detection
    lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
    
    if lines is None:
        return 0, 0
    
    horizontal_count = 0
    vertical_count = 0
    
    for rho, theta in lines[:, 0]:
        angle = theta * 180 / np.pi
        
        # Check if line is roughly horizontal (0° or 180°)
        if (angle < 10) or (angle > 170):
            horizontal_count += 1
        # Check if line is roughly vertical (90°)
        elif 80 < angle < 100:
            vertical_count += 1
    
    return horizontal_count, vertical_count

def detect_horizon(image):
    """Try to detect horizon lines (for landscape photos)"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Look for long horizontal lines in the middle third of the image
    h, w = gray.shape
    middle_section = edges[h//3:2*h//3, :]
    
    lines = cv2.HoughLinesP(middle_section, 1, np.pi/180, threshold=50, minLineLength=w//4, maxLineGap=20)
    
    if lines is None:
        return 0
    
    horizontal_lines = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = abs(np.arctan2(y2-y1, x2-x1) * 180 / np.pi)
        if angle < 10 or angle > 170:  # Nearly horizontal
            horizontal_lines += 1
    
    return horizontal_lines

def suggest_rotation(image_path):
    """Analyze image and suggest rotation"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            return None, "Could not load image"
        
        h, w = image.shape[:2]
        
        # Collect evidence
        evidence = {}
        
        # 1. Face detection (strongest signal)
        face_count, faces = detect_faces(image)
        evidence['faces'] = face_count
        
        # Test rotations if faces found
        best_faces = face_count
        best_rotation = 0
        
        for rotation in [90, 180, 270]:
            if rotation == 90:
                rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            elif rotation == 180:
                rotated = cv2.rotate(image, cv2.ROTATE_180)
            elif rotation == 270:
                rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            
            rot_face_count, _ = detect_faces(rotated)
            if rot_face_count > best_faces:
                best_faces = rot_face_count
                best_rotation = rotation
        
        # 2. Text orientation
        h_score, v_score = detect_text_orientation(image)
        evidence['text_h'] = h_score
        evidence['text_v'] = v_score
        
        # 3. Edge analysis
        h_edges, v_edges = analyze_dominant_edges(image)
        evidence['edges_h'] = h_edges
        evidence['edges_v'] = v_edges
        
        # 4. Horizon detection
        horizon_lines = detect_horizon(image)
        evidence['horizon'] = horizon_lines
        
        # Decision logic
        confidence = 0
        suggested_rotation = 0
        reasons = []
        
        # Face detection is strongest signal
        if best_rotation != 0:
            suggested_rotation = best_rotation
            confidence += 0.8
            reasons.append(f"faces detected better at {best_rotation}°")
        
        # Text should be more horizontal than vertical usually
        if h_score > v_score * 2:
            confidence += 0.3
            reasons.append("text appears horizontal")
        elif v_score > h_score * 2:
            # Might need 90° rotation
            if suggested_rotation == 0:
                suggested_rotation = 90
            confidence += 0.3
            reasons.append("text appears vertical")
        
        # Edge analysis
        if h_edges > v_edges * 1.5:
            confidence += 0.2
            reasons.append("more horizontal edges")
        elif v_edges > h_edges * 1.5:
            if suggested_rotation == 0:
                suggested_rotation = 90
            confidence += 0.2
            reasons.append("more vertical edges")
        
        # Horizon detection
        if horizon_lines > 0:
            confidence += 0.3
            reasons.append("horizon detected")
        
        # Aspect ratio check
        if w > h * 1.5:  # Very wide
            if suggested_rotation in [90, 270]:
                confidence += 0.2
                reasons.append("aspect ratio suggests landscape")
        elif h > w * 1.5:  # Very tall
            if suggested_rotation == 0:
                confidence += 0.2
                reasons.append("aspect ratio suggests portrait")
        
        return {
            'rotation': suggested_rotation,
            'confidence': min(confidence, 1.0),
            'reasons': reasons,
            'evidence': evidence
        }, None
        
    except Exception as e:
        return None, str(e)

def process_image_folder(folder_path, min_confidence=0.5):
    """Process all images in a folder"""
    print(f"\n📁 Analyzing folder: {folder_path}")
    
    if not os.path.exists(folder_path):
        print(f"  ❌ Folder doesn't exist")
        return []
    
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    suggestions = []
    
    for filename in sorted(image_files):
        image_path = os.path.join(folder_path, filename)
        print(f"  🔍 Analyzing {filename}...")
        
        result, error = suggest_rotation(image_path)
        
        if error:
            print(f"    ❌ Error: {error}")
            continue
        
        if result['rotation'] != 0 and result['confidence'] >= min_confidence:
            print(f"    🔄 Suggest {result['rotation']}° rotation (confidence: {result['confidence']:.2f})")
            print(f"    📝 Reasons: {', '.join(result['reasons'])}")
            suggestions.append({
                'file': filename,
                'path': image_path,
                'rotation': result['rotation'],
                'confidence': result['confidence'],
                'reasons': result['reasons']
            })
        else:
            print(f"    ✅ Looks correct (confidence: {result['confidence']:.2f})")
    
    return suggestions

def apply_rotations(suggestions, dry_run=True):
    """Apply the suggested rotations"""
    if dry_run:
        print(f"\n🧪 DRY RUN - Would rotate {len(suggestions)} images:")
        for suggestion in suggestions:
            print(f"  {suggestion['file']}: {suggestion['rotation']}° (confidence: {suggestion['confidence']:.2f})")
        return
    
    print(f"\n🔄 Applying rotations to {len(suggestions)} images...")
    
    for suggestion in suggestions:
        try:
            # Use PIL for rotation
            with Image.open(suggestion['path']) as img:
                if suggestion['rotation'] == 90:
                    rotated = img.rotate(-90, expand=True)
                elif suggestion['rotation'] == 180:
                    rotated = img.rotate(180, expand=True)
                elif suggestion['rotation'] == 270:
                    rotated = img.rotate(90, expand=True)
                
                rotated.save(suggestion['path'], quality=95)
                print(f"  ✅ Rotated {suggestion['file']} by {suggestion['rotation']}°")
                
        except Exception as e:
            print(f"  ❌ Failed to rotate {suggestion['file']}: {e}")

def main():
    print("🤖 Smart Image Rotation Detector")
    print("Using OpenCV for face detection, text analysis, and edge detection...")
    
    # Start with medium resolution for speed
    test_folder = "images/medium_res"
    
    print(f"\n📊 Analyzing {test_folder} folder first...")
    suggestions = process_image_folder(test_folder, min_confidence=0.6)
    
    if not suggestions:
        print("\n✅ No rotation suggestions found!")
        return
    
    print(f"\n📋 Found {len(suggestions)} images that might need rotation:")
    apply_rotations(suggestions, dry_run=True)
    
    response = input(f"\n❓ Apply these rotations? (y/n): ").lower()
    if response == 'y':
        apply_rotations(suggestions, dry_run=False)
        
        # Ask if user wants to apply to all resolution folders
        apply_all = input("\n❓ Apply same rotations to all resolution folders? (y/n): ").lower()
        if apply_all == 'y':
            folders = ["images/high_res", "images/high_res_1200", "images/small_res", "images/low_res"]
            
            for folder in folders:
                print(f"\n🔄 Processing {folder}...")
                for suggestion in suggestions:
                    # Find corresponding file in this folder
                    base_name = suggestion['file'].replace('-med', '')
                    
                    if 'high_res_1200' in folder:
                        target_file = base_name.replace('.jpg', '-high.jpg')
                    elif 'small_res' in folder:
                        target_file = base_name.replace('.jpg', '-small.jpg')
                    elif 'low_res' in folder:
                        target_file = base_name.replace('.jpg', '-low.jpg')
                    else:  # high_res
                        target_file = base_name
                    
                    target_path = os.path.join(folder, target_file)
                    
                    if os.path.exists(target_path):
                        try:
                            with Image.open(target_path) as img:
                                if suggestion['rotation'] == 90:
                                    rotated = img.rotate(-90, expand=True)
                                elif suggestion['rotation'] == 180:
                                    rotated = img.rotate(180, expand=True)
                                elif suggestion['rotation'] == 270:
                                    rotated = img.rotate(90, expand=True)
                                
                                rotated.save(target_path, quality=95)
                                print(f"  ✅ Rotated {target_file}")
                        except Exception as e:
                            print(f"  ❌ Failed to rotate {target_file}: {e}")
    
    print("\n🎉 Smart rotation detection complete!")

if __name__ == "__main__":
    main()
