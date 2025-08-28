#!/usr/bin/env python3

def add_missing_modal_functionality():
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # Add the missing JavaScript functionality right before the Initialize comment
    modal_js = """
        // Project modal functionality
        function showProjectModal(project) {
            const modal = document.getElementById('project-modal');
            const modalTitle = document.getElementById('modal-title');
            const modalDate = document.getElementById('modal-date');
            const carousel = document.getElementById('modal-carousel');
            
            if (!modal || !carousel) return;
            
            // Set project info
            modalTitle.textContent = project.title;
            modalDate.textContent = `${project.date} - ${project.location}`;
            
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
        }
        
        function closeProjectModal() {
            const modal = document.getElementById('project-modal');
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        }
        
        // Add click handlers to project items
        function addProjectClickHandlers() {
            const projectItems = document.querySelectorAll('.project-item');
            projectItems.forEach(item => {
                item.addEventListener('click', function() {
                    // Extract project info from the text
                    const text = this.textContent;
                    // Create a mock project object - you may need to adjust this based on actual data
                    const project = {
                        title: text.split(' - ')[0] || text,
                        date: '2023',
                        location: text.split(' - ')[1] || 'Location',
                        images: [1, 2, 3, 4, 5] // Default images - adjust as needed
                    };
                    showProjectModal(project);
                });
            });
        }
        
        // Modal close handlers
        document.addEventListener('DOMContentLoaded', function() {
            const closeButton = document.querySelector('.close-button');
            const modal = document.getElementById('project-modal');
            
            if (closeButton) {
                closeButton.addEventListener('click', closeProjectModal);
            }
            
            if (modal) {
                modal.addEventListener('click', function(e) {
                    if (e.target === modal) {
                        closeProjectModal();
                    }
                });
            }
            
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeProjectModal();
                }
            });
            
            // Add click handlers after projects are populated
            setTimeout(addProjectClickHandlers, 500);
        });"""
    
    # Insert before the Initialize comment
    content = content.replace('        // Initialize', modal_js + '\n\n        // Initialize')
    
    # Write the updated content
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print("Added missing modal functionality - now projects should open modals when clicked!")

if __name__ == "__main__":
    add_missing_modal_functionality()
