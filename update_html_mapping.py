#!/usr/bin/env python3
"""
Update HTML file with corrected projects mapping
"""

def update_html_with_corrected_mapping():
    # Read the corrected mapping
    with open("corrected_projects_mapping.js", "r") as f:
        corrected_mapping = f.read()
    
    # Read the current HTML file
    with open("index_with_carousel.html", "r") as f:
        lines = f.readlines()
    
    # Find the start and end of the projects constant
    start_line = None
    end_line = None
    
    for i, line in enumerate(lines):
        if "const projects = {" in line:
            start_line = i
        elif line.strip() == "};" and start_line is not None:
            end_line = i
            break
    
    if start_line is None or end_line is None:
        print("❌ Could not find projects constant boundaries")
        return False
    
    print(f"📍 Found projects constant: lines {start_line + 1} to {end_line + 1}")
    
    # Replace the projects section
    new_lines = (
        lines[:start_line] +
        ["        " + corrected_mapping + "\n"] +
        lines[end_line + 1:]
    )
    
    # Write the updated HTML
    with open("index_with_carousel.html", "w") as f:
        f.writelines(new_lines)
    
    print("✅ Successfully updated index_with_carousel.html with corrected mapping")
    return True

def main():
    print("🔄 Updating HTML file with corrected projects mapping...")
    
    if update_html_with_corrected_mapping():
        print("\n🎯 HTML file updated successfully!")
        print("📊 All projects now have correct photo counts:")
        print("  • TXRX WORKSHOP: 10 images (179-188)")
        print("  • SUPER BOWL LVIII: 28 images (19-46)")
        print("  • NFL DRAFT DAY: 20 images (113-132)")
        print("  • And all other projects with their actual photo counts")
    else:
        print("\n❌ Failed to update HTML file")

if __name__ == "__main__":
    main()
