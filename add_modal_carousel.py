#!/usr/bin/env python3

def add_modal_carousel():
    with open('index.html', 'r') as f:
        content = f.read()
    
    # Add modal HTML before closing body tag if it doesn't exist
    if 'project-modal' not in content:
        modal_html = '''
    <!-- Project Modal -->
    <div id="project-modal" class="modal">
        <div class="modal-content">
            <span class="close-button">&times;</span>
            <div class="modal-header">
                <h2 id="modal-project-title">Project Title</h2>
                <div class="modal-project-info">
                    <p id="modal-project-client">Client</p>
                    <p id="modal-project-date">Date</p>
                    <p id="modal-project-event">Event</p>
                    <p id="modal-project-city">City</p>
                </div>
            </div>
            <div class="carousel-container">
                <!-- Carousel content will be populated by JavaScript -->
            </div>
        </div>
    </div>
'''
        content = content.replace('</body>', modal_html + '\n</body>')
    
    # Add modal styles before </style> if they don't exist
    if '.modal {' not in content:
        modal_styles = '''
        /* Project Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 2000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(10px);
        }

        .modal-content {
            width: 100%;
            height: 100%;
            position: relative;
            color: white;
            font-family: 'Bitcount', monospace;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 60px 40px 40px 40px;
        }

        .close-button {
            color: white;
            font-size: 48px;
            font-weight: 300;
            position: absolute;
            right: 40px;
            top: 40px;
            cursor: pointer;
            z-index: 2001;
            transition: all 0.3s ease;
            line-height: 1;
        }

        .close-button:hover {
            color: #ccc;
            transform: scale(1.1);
        }

        .modal-header {
            position: absolute;
            top: 60px;
            left: 40px;
            z-index: 2001;
        }

        .modal-header h2 {
            font-size: 24px;
            margin-bottom: 10px;
            font-weight: normal;
        }

        .modal-project-info {
            font-size: 14px;
            color: #ccc;
            line-height: 1.6;
        }
'''
        content = content.replace('</style>', modal_styles + '\n        </style>')
    
    # Add showProjectModal function before the last closing script tag if it doesn't exist
    if 'function showProjectModal' not in content:
        modal_js = '''
        function showProjectModal(project) {
            const modal = document.getElementById('project-modal');
            if (!modal) return;
            
            // Set project info
            document.getElementById('modal-project-title').textContent = `${project.client} - ${project.event}`;
            document.getElementById('modal-project-client').textContent = `Client: ${project.client}`;
            document.getElementById('modal-project-date').textContent = `Date: ${project.date}`;
            document.getElementById('modal-project-event').textContent = `Event: ${project.event}`;
            document.getElementById('modal-project-city').textContent = `City: ${project.city}`;
            
            // Create image array for carousel from project photos
            const images = [];
            if (project.photos && project.photos.length > 0) {
                project.photos.forEach(photoNum => {
                    images.push(`${BASE_PATH}high_res_1200/img${String(photoNum).padStart(3, '0')}-high.jpg`);
                });
            }
            
            createCarousel(images, modal);
            modal.style.display = 'block';
            
            // Prevent body scroll
            document.body.style.overflow = 'hidden';
        }

        function closeProjectModal() {
            const modal = document.getElementById('project-modal');
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        }

        // Modal event listeners
        document.addEventListener('DOMContentLoaded', function() {
            const modal = document.getElementById('project-modal');
            const closeBtn = document.querySelector('.close-button');
            
            if (closeBtn) {
                closeBtn.addEventListener('click', closeProjectModal);
            }
            
            if (modal) {
                modal.addEventListener('click', function(e) {
                    if (e.target === modal) {
                        closeProjectModal();
                    }
                });
            }
            
            // Escape key to close modal
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && modal && modal.style.display === 'block') {
                    closeProjectModal();
                }
            });
        });
'''
        content = content.replace('        // Initialize', modal_js + '\n\n        // Initialize')
    
    # Write the updated content
    with open('index.html', 'w') as f:
        f.write(content)
    
    print("Modal carousel system added successfully!")

if __name__ == "__main__":
    add_modal_carousel()
