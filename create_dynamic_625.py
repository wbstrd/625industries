#!/usr/bin/env python3
import json
import random
from pathlib import Path

def create_dynamic_625_layout():
    """
    Create a dynamic, visually striking 625 clock layout using many more photos
    in creative patterns that look amazing and crazy.
    """
    
    # Total images available
    total_images = 236
    
    # Create a more dynamic layout with multiple layers and patterns
    layout = {
        "description": "Dynamic 625 Clock with multiple photo layers and creative patterns",
        "total_images": total_images,
        "layout_type": "dynamic_mosaic",
        "patterns": {
            "background_layer": {
                "description": "Background mosaic of photos forming the overall 625 shape",
                "image_count": 180,
                "pattern": "organic_mosaic"
            },
            "digit_outlines": {
                "description": "Sharp outlines of 6, 2, 5 using high-contrast photos",
                "image_count": 36,
                "pattern": "digit_contours"
            },
            "accent_highlights": {
                "description": "Bright accent photos for visual pop",
                "image_count": 20,
                "pattern": "strategic_highlights"
            }
        },
        "digit_mappings": {
            "6": {
                "background_tiles": list(range(1, 61)),  # 60 background tiles
                "outline_tiles": list(range(61, 73)),    # 12 outline tiles
                "accent_tiles": list(range(73, 78))      # 5 accent tiles
            },
            "2": {
                "background_tiles": list(range(78, 138)), # 60 background tiles
                "outline_tiles": list(range(138, 150)),   # 12 outline tiles
                "accent_tiles": list(range(150, 155))     # 5 accent tiles
            },
            "5": {
                "background_tiles": list(range(155, 215)), # 60 background tiles
                "outline_tiles": list(range(215, 227)),    # 12 outline tiles
                "accent_tiles": list(range(227, 232))      # 5 accent tiles
            }
        },
        "visual_effects": {
            "gradient_layers": True,
            "dynamic_spacing": True,
            "photo_clusters": True,
            "color_themes": ["warm", "cool", "neutral"],
            "size_variations": [0.8, 1.0, 1.2, 1.5],
            "rotation_angles": [-15, -5, 0, 5, 15],
            "opacity_levels": [0.7, 0.85, 1.0]
        },
        "layout_grid": {
            "width": 120,
            "height": 60,
            "cell_size": "variable",
            "spacing": "organic"
        },
        "photo_clusters": {
            "cluster_1": {
                "center": [20, 15],
                "radius": 8,
                "photos": list(range(1, 25)),
                "effect": "zoom_focus"
            },
            "cluster_2": {
                "center": [60, 15],
                "radius": 8,
                "photos": list(range(25, 49)),
                "effect": "color_burst"
            },
            "cluster_3": {
                "center": [100, 15],
                "radius": 8,
                "photos": list(range(49, 73)),
                "effect": "motion_blur"
            },
            "cluster_4": {
                "center": [20, 45],
                "radius": 8,
                "photos": list(range(73, 97)),
                "effect": "depth_layers"
            },
            "cluster_5": {
                "center": [60, 45],
                "radius": 8,
                "photos": list(range(97, 121)),
                "effect": "light_leak"
            },
            "cluster_6": {
                "center": [100, 45],
                "radius": 8,
                "photos": list(range(121, 145)),
                "effect": "grain_texture"
            }
        },
        "digit_contours": {
            "6": {
                "outline_points": [
                    [15, 10], [15, 50], [25, 50], [25, 30], [35, 30], [35, 50], [45, 50], [45, 10], [35, 10], [35, 20], [25, 20], [25, 10]
                ],
                "fill_pattern": "radial_gradient",
                "photos_used": list(range(145, 157))
            },
            "2": {
                "outline_points": [
                    [55, 10], [75, 10], [75, 20], [65, 20], [65, 30], [75, 30], [75, 40], [65, 40], [65, 50], [75, 50], [75, 60], [55, 60], [55, 50], [65, 50], [65, 40], [55, 40], [55, 30], [65, 30], [65, 20], [55, 20]
                ],
                "fill_pattern": "linear_gradient",
                "photos_used": list(range(157, 169))
            },
            "5": {
                "outline_points": [
                    [95, 10], [115, 10], [115, 20], [105, 20], [105, 30], [115, 30], [115, 40], [105, 40], [105, 50], [115, 50], [115, 60], [95, 60], [95, 50], [105, 50], [105, 40], [95, 40], [95, 30], [105, 30], [105, 20], [95, 20]
                ],
                "fill_pattern": "diagonal_stripes",
                "photos_used": list(range(169, 181))
            }
        },
        "dynamic_elements": {
            "floating_photos": list(range(181, 201)),
            "particle_effects": list(range(201, 221)),
            "light_rays": list(range(221, 236))
        }
    }
    
    return layout

def create_creative_patterns():
    """
    Generate creative patterns for the 625 clock
    """
    patterns = {
        "spiral_pattern": {
            "description": "Photos arranged in spiral patterns within each digit",
            "algorithm": "fibonacci_spiral",
            "photos_per_digit": 40
        },
        "wave_pattern": {
            "description": "Photos flowing in wave-like patterns",
            "algorithm": "sine_wave",
            "photos_per_digit": 35
        },
        "explosion_pattern": {
            "description": "Photos radiating outward from digit centers",
            "algorithm": "radial_explosion",
            "photos_per_digit": 45
        },
        "mosaic_pattern": {
            "description": "Complex mosaic with varying tile sizes",
            "algorithm": "voronoi_mosaic",
            "photos_per_digit": 50
        }
    }
    return patterns

def generate_photo_assignments():
    """
    Generate specific photo assignments for the dynamic layout
    """
    assignments = {
        "digit_6": {
            "core_photos": list(range(1, 41)),
            "accent_photos": list(range(41, 51)),
            "border_photos": list(range(51, 61)),
            "highlight_photos": list(range(61, 71))
        },
        "digit_2": {
            "core_photos": list(range(71, 111)),
            "accent_photos": list(range(111, 121)),
            "border_photos": list(range(121, 131)),
            "highlight_photos": list(range(131, 141))
        },
        "digit_5": {
            "core_photos": list(range(141, 181)),
            "accent_photos": list(range(181, 191)),
            "border_photos": list(range(191, 201)),
            "highlight_photos": list(range(201, 211))
        },
        "background_elements": list(range(211, 236))
    }
    return assignments

if __name__ == "__main__":
    # Generate the dynamic layout
    layout = create_dynamic_625_layout()
    patterns = create_creative_patterns()
    assignments = generate_photo_assignments()
    
    # Combine everything into a comprehensive configuration
    config = {
        "layout": layout,
        "patterns": patterns,
        "assignments": assignments,
        "metadata": {
            "created_by": "Dynamic 625 Generator",
            "version": "2.0",
            "description": "Crazy, visually striking 625 clock with multiple photo layers"
        }
    }
    
    # Save to JSON file
    with open('dynamic_625_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Generated dynamic 625 configuration!")
    print(f"📊 Total photos used: {layout['total_images']}")
    print(f"🎨 Layout type: {layout['layout_type']}")
    print(f"📁 Saved to: dynamic_625_config.json")
    
    # Print some stats
    print("\n📈 Layout Statistics:")
    print(f"   • Background layer: {layout['patterns']['background_layer']['image_count']} photos")
    print(f"   • Digit outlines: {layout['patterns']['digit_outlines']['image_count']} photos")
    print(f"   • Accent highlights: {layout['patterns']['accent_highlights']['image_count']} photos")
    print(f"   • Photo clusters: {len(layout['photo_clusters'])} clusters")
    print(f"   • Dynamic elements: {len(layout['dynamic_elements'])} types")
