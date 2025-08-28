#!/usr/bin/env python3
"""
Create complete portfolio with all 76 projects from projects.json
Show photos only for the 19 projects we have mapped, others just as text
"""
import json

def create_complete_portfolio():
    # Read the projects.json file
    with open('Archives/projects.json', 'r') as f:
        all_projects = json.load(f)
    
    # The 19 projects we have photos for (with their correct mappings)
    projects_with_photos = {
        "LA ALL STAR": [91, 92, 93, 94, 95],
        "MAKERS STUDIO": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Two instances
        "LEVI'S HOUSE × DAISY WORLD": [11, 12, 13, 14, 15],
        "BILLIE EILISH × NIKE (UPCYCLE)": [16, 17, 18, 19, 20],
        "LEVI'S × COME": [21, 22, 23, 24, 25],
        "NFL DRAFT DAY": [26, 27, 28, 29, 30],
        "MLB NIKEBYYOU": [31, 32, 33, 34, 35],
        "SUPER BOWL LVII × UNDFTD": [36, 37, 38, 39, 40],
        "NIKEBYYOU – SUPER BOWL": [41, 42, 43, 44, 45],
        "ROLLING LOUD × LEVI'S": [46, 47, 48, 49, 50, 56, 57, 58, 59, 60],  # Multiple instances
        "LEVI'S 501 DAY": [51, 52, 53, 54, 55],
        "NIKE TEA ROOM": [61, 62, 63, 64, 65],
        "SUPER BOWL LVIII NIKEBYYOU": [66, 67, 68, 69, 70],
        "ROLLING LOUD × MODELO": [71, 72, 73, 74, 75],
        "VEGAS KICK OFF": [76, 77, 78, 79, 80],
        "TXRX WORKSHOP": [81, 82, 83, 84, 85],
        "ALL STAR WEEKEND × BOARDROOM": [86, 87, 88, 89, 90]
    }
    
    # Build the complete projects structure
    projects_by_year = {}
    image_counter = 1
    
    for project in all_projects:
        year = project['date'][:4]
        if year not in projects_by_year:
            projects_by_year[year] = []
        
        # Check if this project has photos
        project_key = None
        project_images = []
        
        # Try to match project to our photo mappings
        event_upper = project['event'].upper()
        if "MAKERS STUDIO" in event_upper:
            if project['city'] == "Los Angeles" and project['date'] == "2018-12-01":
                project_images = [1, 2, 3, 4, 5]
            elif project['city'] == "Los Angeles" and project['date'] == "2018-10-18":
                project_images = [6, 7, 8, 9, 10]
        elif "BILLIE EILISH" in event_upper and "NIKE" in event_upper:
            project_images = [16, 17, 18, 19, 20]
        elif "NFL DRAFT" in event_upper:
            project_images = [26, 27, 28, 29, 30]
        elif "LEVI'S HOUSE" in event_upper and "DAISY" in event_upper:
            project_images = [11, 12, 13, 14, 15]
        elif "LEVI'S" in event_upper and "COME" in event_upper:
            project_images = [21, 22, 23, 24, 25]
        elif "MLB" in event_upper and "NIKE" in event_upper:
            project_images = [31, 32, 33, 34, 35]
        elif "SUPER BOWL LVII" in event_upper and "UNDFTD" in event_upper:
            project_images = [36, 37, 38, 39, 40]
        elif "SUPER BOWL" in event_upper and "NIKE" in event_upper and "2023" in project['date']:
            project_images = [41, 42, 43, 44, 45]
        elif "ROLLING LOUD" in event_upper and "LEVI'S" in event_upper:
            if "2023-03-04" in project['date']:
                project_images = [46, 47, 48, 49, 50]
            elif "2023-07-21" in project['date']:
                project_images = [56, 57, 58, 59, 60]
        elif "LEVI'S 501" in event_upper:
            project_images = [51, 52, 53, 54, 55]
        elif "NIKE TEA ROOM" in event_upper:
            project_images = [61, 62, 63, 64, 65]
        elif "SUPER BOWL LVIII" in event_upper:
            project_images = [66, 67, 68, 69, 70]
        elif "ROLLING LOUD" in event_upper and "MODELO" in event_upper and "2024-03-14" in project['date']:
            project_images = [71, 72, 73, 74, 75]
        elif "VEGAS KICK OFF" in event_upper:
            project_images = [76, 77, 78, 79, 80]
        elif "TXRX" in event_upper:
            project_images = [81, 82, 83, 84, 85]
        elif "ALL STAR WEEKEND" in event_upper and "BOARDROOM" in event_upper:
            project_images = [86, 87, 88, 89, 90]
        elif "ALL-STAR WEEKEND" in event_upper and "2017" in project['date']:
            # This should be LA ALL STAR 2017
            project_images = [91, 92, 93, 94, 95]
        
        # Create project entry
        project_entry = {
            "title": project['event'].upper(),
            "date": project['date'].replace('-', '.'),
            "location": project['city'].upper(),
            "description": f"{project['client']} {project['event']} event in {project['city']}.",
            "images": project_images if project_images else []
        }
        
        projects_by_year[year].append(project_entry)
    
    # Generate the HTML
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>625 Industries</title>
    <style>
        @font-face {
            font-family: 'Bitcount';
            src: url('https://raw.githubusercontent.com/wbstrd/625industries/main/Fonts/BitcountGridSingle-LightCircle.otf') format('opentype');
            font-weight: normal;
            font-style: normal;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: black;
            color: white;
            font-family: 'Bitcount', monospace;
            overflow: hidden;
            width: 100%;
            height: 100%;
            background: black;
            font-family: 'Inter', sans-serif;
        }

        #clock625-container {
            width: 100%;
            height: 100%;
            overflow: hidden;
            cursor: grab;
            position: relative;
        }

        #toggle-container {
            position: absolute;
            top: 40px;
            right: 40px;
            z-index: 1000;
        }

        #toggle-button {
            width: 60px;
            height: 30px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            cursor: pointer;
            position: relative;
            transition: all 0.3s ease;
        }

        #toggle-button:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        #toggle-circle {
            width: 22px;
            height: 22px;
            background: white;
            border-radius: 50%;
            position: absolute;
            top: 2px;
            left: 2px;
            transition: all 0.3s ease;
        }

        #toggle-button.active #toggle-circle {
            left: 32px;
        }

        #projects-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: black;
            overflow-y: auto;
            padding: 40px;
            display: none;
            z-index: 999;
        }

        #projects-container.visible {
            display: block;
        }

        .year-section {
            margin-bottom: 40px;
        }

        .year-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #fff;
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
            padding-bottom: 10px;
        }

        .project-item {
            padding: 8px 0;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
            padding-left: 15px;
            opacity: 0;
            animation: slideInLeft 0.6s ease forwards;
        }

        .project-item:hover {
            background: rgba(255, 255, 255, 0.1);
            border-left-color: #fff;
            padding-left: 20px;
        }

        .project-item.has-photos {
            color: #00ff88;
            font-weight: bold;
        }

        .project-item.no-photos {
            color: rgba(255, 255, 255, 0.6);
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        /* Clock Display */
        #clock625 {
            display: grid;
            grid-template-columns: repeat(81, 16px);
            grid-template-rows: repeat(35, 16px);
            gap: 1px;
            justify-content: center;
            align-content: center;
            height: 100vh;
            transform: scale(0.8);
        }

        #clock625.hidden {
            display: none;
        }

        .pixel {
            width: 16px;
            height: 16px;
            background-size: cover;
            background-position: center;
            transition: transform 0.1s ease;
        }

        /* Modal Styles */
        #project-modal {
            display: none;
            position: fixed;
            z-index: 10000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(10px);
            animation: fadeIn 0.3s ease-in-out;
        }

        .modal-content {
            background-color: transparent;
            margin: 2% auto;
            padding: 20px;
            width: 95%;
            height: 90%;
            border-radius: 15px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        #modal-carousel {
            width: 100%;
            height: 70%;
            overflow-x: auto;
            overflow-y: hidden;
            white-space: nowrap;
            padding: 20px 0;
            scrollbar-width: none;
            -ms-overflow-style: none;
            display: flex;
            align-items: center;
            position: relative;
            will-change: scroll-position;
        }

        #modal-carousel::-webkit-scrollbar {
            display: none;
        }

        .carousel-item {
            display: inline-block !important;
            width: auto !important;
            height: 480px !important;
            margin-right: 25px !important;
            vertical-align: top !important;
            flex-shrink: 0 !important;
            transition: transform 0.2s ease !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3) !important;
            will-change: transform !important;
        }

        .carousel-item:hover {
            transform: scale(1.03) !important;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4) !important;
        }

        .carousel-item img {
            width: auto !important;
            height: 100% !important;
            object-fit: cover !important;
            display: block !important;
            border-radius: 12px !important;
            will-change: auto !important;
        }

        .close-button {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            position: absolute;
            top: 10px;
            right: 25px;
            z-index: 1001;
        }

        .close-button:hover,
        .close-button:focus {
            color: white;
            text-decoration: none;
            cursor: pointer;
        }

        .modal-header {
            text-align: center;
            margin-bottom: 20px;
        }

        #modal-title {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        #modal-date {
            font-size: 16px;
            color: #ccc;
            margin-bottom: 20px;
        }

        #modal-description {
            font-size: 14px;
            color: #999;
            text-align: center;
            max-width: 600px;
            margin: 0 auto 30px;
            line-height: 1.4;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        #clock625-container img {
            transition: all 0.2s ease !important;
            cursor: pointer !important;
        }
        
        #clock625-container img:hover {
            transform: scale(1.05) !important;
            filter: brightness(1.1) !important;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.3) !important;
        }
    </style>
</head>
<body>
    <div id="clock625-container">
        <div id="toggle-container">
            <div id="toggle-button">
                <div id="toggle-circle"></div>
            </div>
        </div>
        <div id="clock625"></div>
        
        <!-- Projects List -->
        <div id="projects-container">'''
    
    # Add all projects organized by year
    for year in sorted(projects_by_year.keys()):
        html_content += f'''
            <div class="year-section">
                <div class="year-title">{year}</div>'''
        
        for project in projects_by_year[year]:
            has_photos = len(project['images']) > 0
            photo_class = 'has-photos' if has_photos else 'no-photos'
            html_content += f'''
                <div class="project-item {photo_class}" data-project='{json.dumps(project)}'>
                    {project['date']} – {project['title']} – {project['location']}
                </div>'''
        
        html_content += '''
            </div>'''
    
    html_content += '''
        </div>
    </div>

    <!-- Modal for project details -->
    <div id="project-modal">
        <div class="modal-content">
            <span class="close-button">&times;</span>
            <div class="modal-header">
                <h2 id="modal-title"></h2>
                <p id="modal-date"></p>
            </div>
            <div class="modal-body">
                <div id="modal-carousel"></div>
                <div id="modal-description"></div>
            </div>
        </div>
    </div>

    <script>
        const WIDTH = 25, HEIGHT = 35, DIGIT_SPACING = 3, NUM_IMAGES = 150;
        const BASE_PATH = "https://raw.githubusercontent.com/wbstrd/625industries/main/images/";

        const poolPaths = {
            low: "low_res",
            small: "small_res",
            medium: "medium_res",
            high1200: "high_res_1200",
            high: "high_res"
        };

        // Create image to project mapping from projects with photos
        const imageToProjectMap = {};'''
    
    # Add the image mapping for projects with photos
    for year in sorted(projects_by_year.keys()):
        for project in projects_by_year[year]:
            if project['images']:
                html_content += f'''
        // {project['title']}
        {json.dumps(project['images'])}.forEach(imageNum => {{
            imageToProjectMap[imageNum] = {json.dumps(project)};
        }});'''
    
    html_content += '''

        function getPhotos(res, suffix = "") {
            return Array.from({ length: NUM_IMAGES }, (_, i) =>
                `${BASE_PATH}${poolPaths[res]}/img${String(i + 1).padStart(3, '0')}${suffix}.jpg`
            );
        }

        function horizontalPill(width = 21, height = 4) {
            const map = Array.from({ length: height }, () => Array(width).fill(1));
            for (let r = 0; r < height; r++)
                for (let c = 0; c < width; c++) {
                    const d = Math.min(c, width - 1 - c);
                    if ((r === 0 || r === height - 1) && d < 2) map[r][c] = 0;
                }
            return map;
        }

        function verticalPill(height = 13, width = 4) {
            const map = Array.from({ length: height }, () => Array(width).fill(1));
            for (let r = 0; r < height; r++)
                for (let c = 0; c < width; c++) {
                    const d = Math.min(r, height - 1 - r);
                    if ((c === 0 || c === width - 1) && d < 2) map[r][c] = 0;
                }
            return map;
        }

        function blankDigit() {
            return Array.from({ length: HEIGHT }, () => Array(WIDTH).fill(0));
        }

        function place(map, target, row, col) {
            map.forEach((r, y) => {
                r.forEach((val, x) => {
                    const gridY = row + y;
                    const gridX = col + x;
                    if (val && target[gridY] && target[gridY][gridX] !== undefined) {
                        target[gridY][gridX] = 1;
                        for (let dy = -3; dy <= 3; dy++) {
                            for (let dx = -3; dx <= 3; dx++) {
                                const by = gridY + dy;
                                const bx = gridX + dx;
                                if (
                                    (dy !== 0 || dx !== 0) &&
                                    target[by] &&
                                    target[by][bx] !== undefined &&
                                    target[by][bx] !== 1
                                ) {
                                    target[by][bx] = 0;
                                }
                            }
                        }
                    }
                });
            });
        }

        function buildDigit(segments) {
            const digit = blankDigit();
            const h = horizontalPill();
            const v = verticalPill();
            if (segments.includes(0)) place(h, digit, 0, 2);
            if (segments.includes(6)) place(h, digit, 15, 2);
            if (segments.includes(3)) place(h, digit, 30, 2);
            if (segments.includes(1)) place(v, digit, 2, WIDTH - 6);
            if (segments.includes(2)) place(v, digit, 17, WIDTH - 6);
            if (segments.includes(5)) place(v, digit, 2, 2);
            if (segments.includes(4)) place(v, digit, 17, 2);
            return digit;
        }

        const segmentMap = {
            6: [0, 5, 4, 3, 2, 6],
            2: [0, 1, 6, 4, 3],
            5: [0, 5, 6, 2, 3]
        };

        const digit6 = buildDigit(segmentMap[6]);
        const digit2 = buildDigit(segmentMap[2]);
        const digit5 = buildDigit(segmentMap[5]);
        const spacer = Array(HEIGHT).fill(0).map(() => Array(DIGIT_SPACING).fill(0));
        const combined = [];

        for (let r = 0; r < HEIGHT; r++) {
            combined.push([...digit6[r], ...spacer[r], ...digit2[r], ...spacer[r], ...digit5[r]]);
        }

        const litCount = combined.flat().filter(v => v).length;

        function fillPool(arr) {
            let pool = [];
            while (pool.length < litCount) {
                pool = pool.concat(arr);
            }
            return pool.slice(0, litCount);
        }

        const pools = {
            low: fillPool(getPhotos("low", "-low")),
            small: fillPool(getPhotos("small", "-small")),
            medium: fillPool(getPhotos("medium", "-med")),
            high1200: fillPool(getPhotos("high1200", "-high")),
            high: fillPool(getPhotos("high", "-high"))
        };

        const holder = document.getElementById("clock625");
        const imgRefs = [];
        let currentRes = "low";

        // Build the display
        let index = 0;
        combined.forEach((row, y) => {
            row.forEach((cell, x) => {
                const div = document.createElement("div");
                div.className = "pixel";
                div.dataset.x = x;
                div.dataset.y = y;
                if (cell === 1) {
                    const img = document.createElement("img");
                    const src = pools.low[index];
                    img.src = src;
                    img.dataset.src = src;
                    img.dataset.low = pools.low[index];
                    img.dataset.small = pools.small[index];
                    img.dataset.medium = pools.medium[index];
                    img.dataset.high1200 = pools.high1200[index];
                    img.dataset.high = pools.high[index];
                    
                    const imageNumber = index + 1;
                    const project = imageToProjectMap[imageNumber];
                    if (project) {
                        img.dataset.projectTitle = project.title;
                        img.dataset.projectDate = project.date;
                        img.dataset.projectLocation = project.location;
                        img.dataset.projectDescription = project.description;
                    }
                    
                    div.appendChild(img);
                    imgRefs.push({ div, img, key: src, imageNumber });
                    index++;
                }
                holder.appendChild(div);
            });
        });

        // Modal functionality
        const modal = document.getElementById("project-modal");
        const closeButton = document.querySelector(".close-button");

        function setupInfiniteScroll(carousel, originalLength) {
            let isScrolling = false;
            const itemWidth = 400;
            const totalWidth = itemWidth * originalLength;
            
            setTimeout(() => {
                carousel.scrollLeft = totalWidth;
            }, 100);
            
            carousel.addEventListener('scroll', () => {
                if (isScrolling) return;
                
                const scrollLeft = carousel.scrollLeft;
                
                if (scrollLeft >= totalWidth * 2.8) {
                    isScrolling = true;
                    carousel.scrollLeft = totalWidth;
                    setTimeout(() => { isScrolling = false; }, 100);
                }
                else if (scrollLeft <= totalWidth * 0.2) {
                    isScrolling = true;
                    carousel.scrollLeft = totalWidth;
                    setTimeout(() => { isScrolling = false; }, 100);
                }
            });
            
            let startX = 0;
            let scrollLeftStart = 0;
            
            carousel.addEventListener('touchstart', (e) => {
                startX = e.touches[0].pageX;
                scrollLeftStart = carousel.scrollLeft;
            });
            
            carousel.addEventListener('touchmove', (e) => {
                e.preventDefault();
                const x = e.touches[0].pageX;
                const walk = (startX - x) * 2;
                carousel.scrollLeft = scrollLeftStart + walk;
            });
        }

        function showProjectModal(project) {
            document.getElementById("modal-title").textContent = project.title;
            document.getElementById("modal-date").textContent = `${project.date} – ${project.location}`;
            document.getElementById("modal-description").textContent = project.description;
            
            const carousel = document.getElementById("modal-carousel");
            carousel.innerHTML = '';
            
            if (project.images && project.images.length > 0) {
                const allImages = [...project.images, ...project.images, ...project.images];
                
                allImages.forEach((imageNum, index) => {
                    const carouselItem = document.createElement("div");
                    carouselItem.className = "carousel-item";
                    
                    const img = document.createElement("img");
                    img.src = `${BASE_PATH}high_res_1200/img${String(imageNum).padStart(3, '0')}-high.jpg`;
                    img.alt = `${project.title} - Image ${index + 1}`;
                    img.onerror = () => {
                        img.src = `${BASE_PATH}medium_res/img${String(imageNum).padStart(3, '0')}-med.jpg`;
                    };
                    
                    carouselItem.appendChild(img);
                    carousel.appendChild(carouselItem);
                });
                
                setupInfiniteScroll(carousel, project.images.length);
            } else {
                carousel.innerHTML = '<div style="color: #666; font-size: 18px; text-align: center; padding: 100px;">No photos available for this project</div>';
            }
            
            modal.style.display = "block";
        }

        closeButton.addEventListener("click", () => {
            modal.style.display = "none";
        });

        window.addEventListener("click", (e) => {
            if (e.target === modal) {
                modal.style.display = "none";
            }
        });

        // Image click handler
        holder.addEventListener("click", (e) => {
            const img = e.target;
            if (img.tagName !== "IMG") return;
            
            const imageNumber = imgRefs.find(ref => ref.img === img)?.imageNumber;
            if (!imageNumber) return;
            
            const project = imageToProjectMap[imageNumber];
            if (project) {
                showProjectModal(project);
            }
        });
          
        // Optimized mouse wheel support for smooth scrolling
        let scrollTimeout;
        window.addEventListener("wheel", (e) => {
            const modal = document.getElementById("project-modal");
            const carousel = document.getElementById("modal-carousel");
            
            if (modal.style.display === "block" && carousel) {
                e.preventDefault();
                
                clearTimeout(scrollTimeout);
                
                const scrollSpeed = Math.abs(e.deltaY) > Math.abs(e.deltaX) ? e.deltaY : e.deltaX;
                const scrollAmount = scrollSpeed * 2;
                
                carousel.scrollLeft += scrollAmount;
                
                scrollTimeout = setTimeout(() => {
                    carousel.style.scrollBehavior = 'smooth';
                    setTimeout(() => {
                        carousel.style.scrollBehavior = 'auto';
                    }, 100);
                }, 50);
            }
        }, { passive: false });

        // Populate project list with click handlers
        function populateProjectList() {
            const projectItems = document.querySelectorAll('.project-item');
            projectItems.forEach((item, index) => {
                item.style.animationDelay = `${index * 0.05}s`;
                
                item.addEventListener("click", () => {
                    const projectData = JSON.parse(item.dataset.project);
                    showProjectModal(projectData);
                });
            });
        }

        // Toggle functionality
        function toggleProjects() {
            const toggleButton = document.getElementById("toggle-button");
            const projectsContainer = document.getElementById("projects-container");
            const clock625 = document.getElementById("clock625");

            if (!projectsContainer.classList.contains("visible")) {
                toggleButton.classList.add("active");
                projectsContainer.classList.add("visible");
                clock625.classList.add("hidden");
            } else {
                toggleButton.classList.remove("active");
                projectsContainer.classList.remove("visible");
                clock625.classList.remove("hidden");
            }
        }

        document.getElementById("toggle-button").addEventListener("click", toggleProjects);

        // Zoom and resolution management
        let scale = 1;

        window.addEventListener("wheel", (e) => {
            const modal = document.getElementById("project-modal");
            if (modal.style.display === "block") return;

            const container = document.getElementById("clock625-container");
            const rect = container.getBoundingClientRect();
            
            if (e.target.closest("#toggle-container") || e.target.closest("#project-list")) return;

            e.preventDefault();
            
            const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
            scale *= zoomFactor;
            scale = Math.max(0.5, Math.min(scale, 15));

            holder.style.transform = `scale(${scale})`;

            let newRes = "low";
            if (scale >= 2) newRes = "small";
            if (scale >= 4) newRes = "medium";
            if (scale >= 8) newRes = "high1200";
            if (scale >= 11) newRes = "high";

            if (newRes !== currentRes) {
                currentRes = newRes;
                imgRefs.forEach(({ img }) => {
                    img.src = img.dataset[currentRes];
                });
            }

            const explodeFactor = Math.max(0, Math.min(1, (scale - 6) / 4));
            imgRefs.forEach(({ div }) => {
                const x = div.dataset.x - 40;
                const y = div.dataset.y - 17;
                const dx = x * explodeFactor * 12;
                const dy = y * explodeFactor * 4;
                div.style.transform = `translate(${dx}px, ${dy}px)`;
            });
        }, { passive: false });

        const container = document.getElementById("clock625-container");
        let isDragging = false;
        let startX, startY, scrollLeft, scrollTop;

        container.addEventListener("mousedown", (e) => {
            if (e.target.closest("#toggle-container")) return;
            isDragging = true;
            container.style.cursor = "grabbing";
            startX = e.pageX - container.offsetLeft;
            startY = e.pageY - container.offsetTop;
            scrollLeft = container.scrollLeft;
            scrollTop = container.scrollTop;
        });

        container.addEventListener("mouseleave", () => {
            isDragging = false;
            container.style.cursor = "grab";
        });

        container.addEventListener("mouseup", () => {
            isDragging = false;
            container.style.cursor = "grab";
        });

        container.addEventListener("mousemove", (e) => {
            if (!isDragging) return;
            e.preventDefault();
            const x = e.pageX - container.offsetLeft;
            const y = e.pageY - container.offsetTop;
            const walkX = (x - startX) * 2;
            const walkY = (y - startY) * 2;
            container.scrollLeft = scrollLeft - walkX;
            container.scrollTop = scrollTop - walkY;
        });

        // Initialize project list
        populateProjectList();
    </script>
</body>
</html>'''

    with open('index.html', 'w') as f:
        f.write(html_content)
    
    print("🚀 COMPLETE PORTFOLIO CREATED!")
    print(f"✅ All {len(all_projects)} projects from projects.json included")
    print("🎯 Project display:")
    
    # Count projects with and without photos
    projects_with_photos_count = 0
    projects_without_photos_count = 0
    
    for year in projects_by_year:
        for project in projects_by_year[year]:
            if project['images']:
                projects_with_photos_count += 1
            else:
                projects_without_photos_count += 1
    
    print(f"  • {projects_with_photos_count} projects WITH photos (green, clickable)")
    print(f"  • {projects_without_photos_count} projects WITHOUT photos (grey, listed only)")
    print()
    print("🎨 Visual indicators:")
    print("  • GREEN text = Has photos, opens carousel")
    print("  • GREY text = No photos, just listed")
    print("  • Working carousel for projects with photos")
    print("  • All projects organized by year")

if __name__ == "__main__":
    create_complete_portfolio()

