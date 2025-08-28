#!/usr/bin/env python3

def add_complete_functionality():
    with open('index.html', 'r') as f:
        content = f.read()
    
    # Add project modal HTML before closing body tag
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

    <!-- Projects List Container -->
    <div id="projects-container">
        <div id="projects-list">
            <!-- Projects will be populated by JavaScript -->
        </div>
    </div>
'''
    
    # Insert before closing body tag
    content = content.replace('</body>', modal_html + '\n</body>')
    
    # Add project list styles before </style>
    project_styles = '''
        /* Projects List Styles */
        #projects-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: black;
            color: white;
            font-family: 'Bitcount', monospace;
            z-index: 1500;
            display: none;
            overflow-y: auto;
            padding: 60px 40px 40px 40px;
        }

        #projects-list {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }

        .project-item {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }

        .project-item:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }

        .project-title {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            color: white;
        }

        .project-details {
            font-size: 12px;
            color: #ccc;
            line-height: 1.4;
        }

        .project-detail {
            margin-bottom: 4px;
        }

        .has-photos {
            border-left: 3px solid #4CAF50;
        }

        .no-photos {
            border-left: 3px solid #666;
            opacity: 0.7;
        }
'''
    
    content = content.replace('</style>', project_styles + '\n        </style>')
    
    # Add JavaScript for project functionality before </script>
    project_js = '''
        // Project data and functionality
        const projects = [
            {"index": 1, "client": "Nike", "date": "February 2023", "event": "Arizona", "city": "Phoenix", "photos": [1, 2, 3, 4, 5]},
            {"index": 2, "client": "Adidas", "date": "March 2023", "event": "LA Event", "city": "Los Angeles", "photos": [6, 7, 8, 9, 10]},
            {"index": 3, "client": "Puma", "date": "April 2023", "event": "NYC Launch", "city": "New York", "photos": [11, 12, 13, 14, 15]}
        ];

        function showProjects() {
            document.getElementById('projects-container').style.display = 'block';
            document.getElementById('clock625-container').style.display = 'none';
            populateProjectsList();
        }

        function hideProjects() {
            document.getElementById('projects-container').style.display = 'none';
            document.getElementById('clock625-container').style.display = 'block';
        }

        function populateProjectsList() {
            const projectsList = document.getElementById('projects-list');
            projectsList.innerHTML = '';
            
            projects.forEach(project => {
                const projectItem = document.createElement('div');
                projectItem.className = `project-item ${project.photos && project.photos.length > 0 ? 'has-photos' : 'no-photos'}`;
                
                projectItem.innerHTML = `
                    <div class="project-title">${project.client} - ${project.event}</div>
                    <div class="project-details">
                        <div class="project-detail">Date: ${project.date}</div>
                        <div class="project-detail">City: ${project.city}</div>
                        <div class="project-detail">Photos: ${project.photos ? project.photos.length : 0}</div>
                    </div>
                `;
                
                if (project.photos && project.photos.length > 0) {
                    projectItem.addEventListener('click', () => openProjectModal(project));
                }
                
                projectsList.appendChild(projectItem);
            });
        }

        function openProjectModal(project) {
            const modal = document.getElementById('project-modal');
            document.getElementById('modal-project-title').textContent = `${project.client} - ${project.event}`;
            document.getElementById('modal-project-client').textContent = `Client: ${project.client}`;
            document.getElementById('modal-project-date').textContent = `Date: ${project.date}`;
            document.getElementById('modal-project-event').textContent = `Event: ${project.event}`;
            document.getElementById('modal-project-city').textContent = `City: ${project.city}`;
            
            // Create image array for carousel
            const images = project.photos.map(photoNum => 
                `${BASE_PATH}high_res_1200/img${String(photoNum).padStart(3, '0')}-high.jpg`
            );
            
            createCarousel(images, modal);
            modal.style.display = 'block';
        }

        function createCarousel(images, modalElement) {
            const container = modalElement.querySelector('.carousel-container');
            if (!container) return;
            
            container.innerHTML = '';
            
            if (images.length === 0) {
                container.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #666;">No images available</div>';
                return;
            }
            
            // Create carousel track
            const track = document.createElement('div');
            track.className = 'carousel-track';
            
            // Create slides
            images.forEach((imgSrc, index) => {
                const slide = document.createElement('div');
                slide.className = 'carousel-slide';
                
                const img = document.createElement('img');
                img.src = imgSrc;
                img.alt = `Project image ${index + 1}`;
                
                slide.appendChild(img);
                track.appendChild(slide);
            });
            
            container.appendChild(track);
            
            // Add navigation if more than one image
            if (images.length > 1) {
                const prevBtn = document.createElement('button');
                prevBtn.className = 'carousel-nav carousel-prev';
                prevBtn.innerHTML = '&#8249;';
                
                const nextBtn = document.createElement('button');
                nextBtn.className = 'carousel-nav carousel-next';
                nextBtn.innerHTML = '&#8250;';
                
                container.appendChild(prevBtn);
                container.appendChild(nextBtn);
                
                // Simple carousel functionality
                let currentSlide = 0;
                
                function updateSlide() {
                    track.style.transform = `translateX(-${currentSlide * 100}%)`;
                }
                
                nextBtn.addEventListener('click', () => {
                    currentSlide = (currentSlide + 1) % images.length;
                    updateSlide();
                });
                
                prevBtn.addEventListener('click', () => {
                    currentSlide = (currentSlide - 1 + images.length) % images.length;
                    updateSlide();
                });
                
                // Auto-play
                let autoPlay = setInterval(() => {
                    currentSlide = (currentSlide + 1) % images.length;
                    updateSlide();
                }, 4000);
                
                container.addEventListener('mouseenter', () => clearInterval(autoPlay));
                container.addEventListener('mouseleave', () => {
                    autoPlay = setInterval(() => {
                        currentSlide = (currentSlide + 1) % images.length;
                        updateSlide();
                    }, 4000);
                });
            }
        }

        // Toggle button functionality
        document.addEventListener('DOMContentLoaded', function() {
            const toggleButton = document.getElementById('toggle-button');
            let showingProjects = false;
            
            toggleButton.addEventListener('click', function() {
                showingProjects = !showingProjects;
                if (showingProjects) {
                    showProjects();
                } else {
                    hideProjects();
                }
            });
            
            // Modal close functionality
            const modal = document.getElementById('project-modal');
            const closeBtn = modal.querySelector('.close-button');
            
            closeBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
            
            window.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });
        });
'''
    
    # Insert before the last closing script tag
    content = content.replace('    </script>', project_js + '\n    </script>')
    
    # Write the updated content
    with open('index.html', 'w') as f:
        f.write(content)
    
    print("Complete project functionality added successfully!")

if __name__ == "__main__":
    add_complete_functionality()
