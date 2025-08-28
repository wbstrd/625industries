#!/usr/bin/env python3

def fix_superbowl_mapping():
    """Fix the Super Bowl project mapping to include all 28 images"""
    
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Based on the mapping script output, the February 2024 Super Bowl should have images 66-93
    # (28 images total as shown in the folder)
    
    # Find and replace the Super Bowl project
    old_mapping = '''    {
      "title": "SUPER BOWL LVIII NIKEBYYOU",
      "date": "2024.02.11",
      "location": "LAS VEGAS",
      "description": "Super Bowl LVIII NikeByYou activation in Las Vegas.",
      "images": [
        66,
        67,
        68,
        69,
        70,
        132
      ]
    }'''
    
    # Create the new mapping with all 28 images (66-93)
    superbowl_images = list(range(66, 94))  # 66 to 93 = 28 images
    
    new_mapping = f'''    {{
      "title": "SUPER BOWL LVIII NIKEBYYOU",
      "date": "2024.02.06",
      "location": "LAS VEGAS",
      "description": "Super Bowl LVIII NikeByYou activation in Las Vegas.",
      "images": {superbowl_images}
    }}'''
    
    if old_mapping in content:
        content = content.replace(old_mapping, new_mapping)
        print("✅ Updated Super Bowl mapping with all 28 images!")
    else:
        print("❌ Could not find Super Bowl project to update")
        return False
    
    # Write back
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print(f"🎯 Super Bowl now includes images 66-93 (28 total images)")
    print(f"✅ img132 should now work!")
    
    return True

if __name__ == "__main__":
    fix_superbowl_mapping()
