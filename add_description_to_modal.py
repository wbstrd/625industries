#!/usr/bin/env python3

def add_description_to_modal():
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Find and update the showProjectModal function to include description
    import re
    
    # Find the existing showProjectModal function and replace it
    old_function_pattern = r'function showProjectModal\(project\)\s*\{[^}]*\}[^}]*\}'
    
    new_function = """function showProjectModal(project) {
            const modal = document.getElementById('project-modal');
            const modalTitle = document.getElementById('modal-title');
            const modalDate = document.getElementById('modal-date');
            const modalDescription = document.getElementById('modal-description');
            const carousel = document.getElementById('modal-carousel');
            
            if (!modal || !carousel) return;
            
            // Set project info
            modalTitle.textContent = project.title;
            modalDate.textContent = `${project.date} - ${project.location}`;
            
            // Add description
            if (modalDescription) {
                modalDescription.textContent = project.description || 'Photography project showcasing creative visual storytelling and artistic composition.';
            }
            
            // Create image elements for carousel
            carousel.innerHTML = '';
            if (project.images && project.images.length > 0) {
                project.images.forEach(imageNum => {
                    const img = document.createElement('img');
                    img.src = `${BASE_PATH}high_res_1200/img${String(imageNum).padStart(3, '0')}-high.jpg`;
                    img.alt = `Project image ${imageNum}`;
                    img.loading = 'lazy';
                    carousel.appendChild(img);
                });
            }
            
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }"""
    
    # Replace the function
    if re.search(old_function_pattern, content, re.DOTALL):
        content = re.sub(old_function_pattern, new_function, content, flags=re.DOTALL)
    
    # Write the updated content
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print("Added description functionality to modal!")

if __name__ == "__main__":
    add_description_to_modal()
