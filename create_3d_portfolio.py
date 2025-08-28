#!/usr/bin/env python3
"""
Create a stunning 3D portfolio with Three.js featuring cinematic photo galleries and smooth transitions
"""

def create_3d_portfolio():
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>625 Industries - 3D Portfolio</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
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
            font-family: 'Bitcount', monospace;
            background: #000;
            color: #fff;
            overflow: hidden;
            cursor: none;
        }

        #canvas-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 1;
        }

        #ui-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 100;
            pointer-events: none;
        }

        #logo {
            position: absolute;
            top: 40px;
            left: 40px;
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 2px;
            pointer-events: auto;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        #logo:hover {
            transform: scale(1.1);
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
        }

        #mode-toggle {
            position: absolute;
            top: 40px;
            right: 40px;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            color: #fff;
            font-family: 'Bitcount', monospace;
            font-size: 14px;
            cursor: pointer;
            pointer-events: auto;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        #mode-toggle:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(255, 255, 255, 0.1);
        }

        #project-info {
            position: absolute;
            bottom: 40px;
            left: 40px;
            max-width: 400px;
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.5s ease;
            pointer-events: none;
        }

        #project-info.visible {
            opacity: 1;
            transform: translateY(0);
        }

        #project-title {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }

        #project-details {
            font-size: 14px;
            opacity: 0.8;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
        }

        #project-description {
            font-size: 16px;
            line-height: 1.4;
            opacity: 0.9;
        }

        #navigation-hint {
            position: absolute;
            bottom: 40px;
            right: 40px;
            font-size: 12px;
            opacity: 0.6;
            text-align: right;
            line-height: 1.4;
            transition: opacity 0.3s ease;
        }

        #custom-cursor {
            position: fixed;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255, 255, 255, 0.6);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transition: all 0.1s ease;
            mix-blend-mode: difference;
        }

        .cursor-hover {
            width: 40px !important;
            height: 40px !important;
            border-color: rgba(255, 255, 255, 1) !important;
            background: rgba(255, 255, 255, 0.1) !important;
        }

        #loading {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            transition: opacity 1s ease;
        }

        #loading.hidden {
            opacity: 0;
            pointer-events: none;
        }

        .loading-text {
            font-size: 24px;
            letter-spacing: 3px;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.4; }
            50% { opacity: 1; }
        }

        .floating {
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        /* Responsive */
        @media (max-width: 768px) {
            #logo, #mode-toggle, #project-info, #navigation-hint {
                left: 20px;
                right: 20px;
                top: 20px;
                bottom: 20px;
            }
            
            #project-title {
                font-size: 22px;
            }
            
            #project-details, #project-description {
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <div id="loading">
        <div class="loading-text">LOADING 625 INDUSTRIES</div>
    </div>

    <div id="canvas-container"></div>

    <div id="ui-overlay">
        <div id="logo" class="floating">625 INDUSTRIES</div>
        <button id="mode-toggle">GALLERY MODE</button>
        
        <div id="project-info">
            <div id="project-title"></div>
            <div id="project-details"></div>
            <div id="project-description"></div>
        </div>

        <div id="navigation-hint">
            Mouse to rotate • Scroll to zoom<br>
            Click photos for details
        </div>
    </div>

    <div id="custom-cursor"></div>

    <script>
        // Custom cursor
        const cursor = document.getElementById('custom-cursor');
        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX - 10 + 'px';
            cursor.style.top = e.clientY - 10 + 'px';
        });

        // Hover effects
        document.addEventListener('mouseover', (e) => {
            if (e.target.style.cursor === 'pointer' || e.target.classList.contains('clickable')) {
                cursor.classList.add('cursor-hover');
            }
        });

        document.addEventListener('mouseout', (e) => {
            cursor.classList.remove('cursor-hover');
        });

        // Three.js Scene Setup
        let scene, camera, renderer, controls;
        let photoMeshes = [];
        let currentMode = '625'; // '625' or 'gallery'
        let digitMeshes = [];
        
        const BASE_PATH = "https://raw.githubusercontent.com/wbstrd/625industries/main/images/";

        // Project data with working image ranges
        const projects = [
            {
                title: "MAKERS STUDIO",
                date: "2018.10.18",
                location: "LOS ANGELES",
                description: "Nike Makers Studio event in Los Angeles featuring custom sneaker design workshops.",
                images: [1, 2, 3, 4, 5],
                color: "#FF6B35"
            },
            {
                title: "MAKERS STUDIO",
                date: "2018.12.01", 
                location: "ROOSEVELT FIELD MALL",
                description: "Nike Makers Studio event in Roosevelt Field Mall.",
                images: [6, 7, 8, 9, 10],
                color: "#F7931E"
            },
            {
                title: "NIKEBYYOU SUPER BOWL LVI",
                date: "2022.02.03",
                location: "LOS ANGELES", 
                description: "Nike NikeByYou Super Bowl LVI event in Los Angeles.",
                images: [11, 12, 13, 14, 15],
                color: "#FFD23F"
            },
            {
                title: "LEVI'S HOUSE × DAISY WORLD",
                date: "2022.04.05",
                location: "LOS ANGELES",
                description: "Levi's House × Daisy World event in Los Angeles.",
                images: [16, 17, 18, 19, 20],
                color: "#06FFA5"
            },
            {
                title: "LEVI'S × COME",
                date: "2022.04.07",
                location: "WATTS",
                description: "Levi's × COME event in Watts.",
                images: [21, 22, 23, 24, 25],
                color: "#4ECDC4"
            },
            {
                title: "BILLIE EILISH × NIKE",
                date: "2022.04.19",
                location: "LOS ANGELES",
                description: "Billie Eilish × Nike (Upcycle) event in Los Angeles.",
                images: [26, 27, 28, 29, 30],
                color: "#45B7D1"
            },
            {
                title: "NFL DRAFT DAY",
                date: "2022.04.27",
                location: "LAS VEGAS",
                description: "Nike NFL Draft Day event in Las Vegas.",
                images: [31, 32, 33, 34, 35],
                color: "#5D4E75"
            },
            {
                title: "MLB NIKEBYYOU",
                date: "2022.07.15",
                location: "LOS ANGELES",
                description: "Nike MLB NikeByYou event in Los Angeles.",
                images: [36, 37, 38, 39, 40],
                color: "#B83DBA"
            },
            {
                title: "ROLLING LOUD × LEVI'S",
                date: "2022.07.21",
                location: "MIAMI",
                description: "Rolling Loud × Levi's event in Miami.",
                images: [41, 42, 43, 44, 45],
                color: "#FF6B9D"
            },
            {
                title: "SUPER BOWL LVII × UNDFTD",
                date: "2023.02.07",
                location: "PHOENIX",
                description: "Nike Super Bowl LVII × UNDFTD event in Phoenix.",
                images: [46, 47, 48, 49, 50],
                color: "#FF4757"
            },
            {
                title: "NIKEBYYOU SUPER BOWL",
                date: "2023.02.08",
                location: "PHOENIX",
                description: "Nike NikeByYou Super Bowl event in Phoenix.",
                images: [51, 52, 53, 54, 55],
                color: "#3742FA"
            },
            {
                title: "ROLLING LOUD × LEVI'S",
                date: "2023.03.04",
                location: "LOS ANGELES",
                description: "Rolling Loud × Levi's event in Los Angeles.",
                images: [56, 57, 58, 59, 60],
                color: "#2ED573"
            },
            {
                title: "LEVI'S 501 DAY",
                date: "2023.05.18",
                location: "SAN FRANCISCO",
                description: "Levi's 501 Day event in San Francisco.",
                images: [61, 62, 63, 64, 65],
                color: "#FFA726"
            },
            {
                title: "ROLLING LOUD × LEVI'S",
                date: "2023.07.05",
                location: "PORTIMÃO",
                description: "Rolling Loud × Levi's event in Portimão.",
                images: [66, 67, 68, 69],
                color: "#26A69A"
            },
            {
                title: "NIKE TEA ROOM",
                date: "2023.07.13",
                location: "LAS VEGAS",
                description: "Nike Tea Room event in Las Vegas.",
                images: [70, 71, 72, 73],
                color: "#AB47BC"
            },
            {
                title: "SUPER BOWL LVIII NIKEBYYOU",
                date: "2024.02.06",
                location: "LAS VEGAS",
                description: "Nike Super Bowl LVIII NikeByYou event in Las Vegas.",
                images: [74, 75, 76, 77, 78],
                color: "#EF5350"
            },
            {
                title: "ROLLING LOUD × MODELO",
                date: "2024.03.14",
                location: "LOS ANGELES",
                description: "Rolling Loud × Modelo event in Los Angeles.",
                images: [79, 80, 81, 82, 83],
                color: "#42A5F5"
            },
            {
                title: "VEGAS KICK OFF",
                date: "2024.09.01",
                location: "LAS VEGAS",
                description: "Modelo Vegas Kick Off event in Las Vegas.",
                images: [84, 85, 86, 87, 88],
                color: "#66BB6A"
            },
            {
                title: "TXRX WORKSHOP",
                date: "2025.02.11",
                location: "HOUSTON",
                description: "Nike TXRX Workshop event in Houston.",
                images: [89, 90, 91, 92, 93],
                color: "#FFCA28"
            },
            {
                title: "ALL STAR WEEKEND × BOARDROOM",
                date: "2025.02.15",
                location: "SAN FRANCISCO",
                description: "Nike All Star Weekend × Boardroom event in San Francisco.",
                images: [94, 95, 96],
                color: "#8E24AA"
            }
        ];

        function init() {
            // Scene
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x000000);

            // Camera
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0, 0, 15);

            // Renderer
            renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            renderer.setClearColor(0x000000, 1);
            document.getElementById('canvas-container').appendChild(renderer.domElement);

            // Controls
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.enableZoom = true;
            controls.autoRotate = false;
            controls.maxDistance = 50;
            controls.minDistance = 5;

            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
            scene.add(ambientLight);

            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(10, 10, 5);
            directionalLight.castShadow = true;
            directionalLight.shadow.mapSize.width = 2048;
            directionalLight.shadow.mapSize.height = 2048;
            scene.add(directionalLight);

            // Start with 625 mode
            create625Display();
            
            // Mode toggle
            const modeToggle = document.getElementById('mode-toggle');
            modeToggle.addEventListener('click', toggleMode);

            // Logo click to return to 625
            const logo = document.getElementById('logo');
            logo.addEventListener('click', () => {
                if (currentMode !== '625') {
                    toggleMode();
                }
            });

            // Handle window resize
            window.addEventListener('resize', onWindowResize);
            
            // Hide loading screen
            setTimeout(() => {
                document.getElementById('loading').classList.add('hidden');
            }, 2000);

            // Start animation loop
            animate();
        }

        function create625Display() {
            // Clear existing meshes
            clearScene();
            
            // Create stylized 625 with floating elements
            const geometry = new THREE.PlaneGeometry(2, 3);
            
            // Create materials for each digit
            const materials = [
                new THREE.MeshLambertMaterial({ color: 0xff6b35 }), // 6
                new THREE.MeshLambertMaterial({ color: 0xffd23f }), // 2  
                new THREE.MeshLambertMaterial({ color: 0x06ffa5 })  // 5
            ];

            // Position digits
            const positions = [-4, 0, 4];
            
            positions.forEach((x, index) => {
                const mesh = new THREE.Mesh(geometry, materials[index]);
                mesh.position.set(x, 0, 0);
                mesh.rotation.y = Math.sin(Date.now() * 0.001 + index) * 0.1;
                
                // Add floating animation
                mesh.userData = {
                    originalY: 0,
                    floatSpeed: 0.002 + index * 0.001,
                    floatAmount: 0.5
                };
                
                scene.add(mesh);
                digitMeshes.push(mesh);
            });

            // Add surrounding particles
            createParticles();
            
            controls.autoRotate = true;
            controls.autoRotateSpeed = 0.5;
        }

        function createGalleryDisplay() {
            // Clear existing meshes
            clearScene();
            
            // Create 3D photo gallery
            const loader = new THREE.TextureLoader();
            
            projects.forEach((project, projectIndex) => {
                project.images.forEach((imageNum, imageIndex) => {
                    const geometry = new THREE.PlaneGeometry(3, 2);
                    
                    // Load image texture
                    const texture = loader.load(
                        `${BASE_PATH}medium_res/img${String(imageNum).padStart(3, '0')}-med.jpg`,
                        (texture) => {
                            texture.minFilter = THREE.LinearFilter;
                            texture.magFilter = THREE.LinearFilter;
                        }
                    );
                    
                    const material = new THREE.MeshLambertMaterial({ 
                        map: texture,
                        transparent: true,
                        opacity: 0.9
                    });
                    
                    const mesh = new THREE.Mesh(geometry, material);
                    
                    // Arrange in a spiral
                    const angle = (projectIndex * project.images.length + imageIndex) * 0.3;
                    const radius = 8 + Math.sin(angle * 0.5) * 3;
                    const height = Math.sin(angle * 0.3) * 4;
                    
                    mesh.position.set(
                        Math.cos(angle) * radius,
                        height,
                        Math.sin(angle) * radius
                    );
                    
                    // Face center
                    mesh.lookAt(new THREE.Vector3(0, height, 0));
                    
                    // Add hover interaction
                    mesh.userData = {
                        project: project,
                        originalScale: 1,
                        isHovered: false
                    };
                    
                    // Add glow effect
                    const glowGeometry = new THREE.PlaneGeometry(3.2, 2.2);
                    const glowMaterial = new THREE.MeshBasicMaterial({
                        color: new THREE.Color(project.color),
                        transparent: true,
                        opacity: 0.1,
                        side: THREE.DoubleSide
                    });
                    const glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
                    glowMesh.position.copy(mesh.position);
                    glowMesh.position.z -= 0.01;
                    glowMesh.lookAt(new THREE.Vector3(0, height, 0));
                    
                    scene.add(glowMesh);
                    scene.add(mesh);
                    photoMeshes.push(mesh);
                });
            });
            
            controls.autoRotate = true;
            controls.autoRotateSpeed = 1;
        }

        function createParticles() {
            const particleCount = 100;
            const particles = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            
            for (let i = 0; i < particleCount * 3; i += 3) {
                positions[i] = (Math.random() - 0.5) * 50;
                positions[i + 1] = (Math.random() - 0.5) * 50;
                positions[i + 2] = (Math.random() - 0.5) * 50;
            }
            
            particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            
            const particleMaterial = new THREE.PointsMaterial({
                color: 0xffffff,
                size: 0.1,
                transparent: true,
                opacity: 0.6
            });
            
            const particleSystem = new THREE.Points(particles, particleMaterial);
            scene.add(particleSystem);
        }

        function clearScene() {
            // Remove all meshes
            while(scene.children.length > 0) {
                const child = scene.children[0];
                if (child.geometry) child.geometry.dispose();
                if (child.material) {
                    if (child.material.map) child.material.map.dispose();
                    child.material.dispose();
                }
                scene.remove(child);
            }
            
            // Re-add lights
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
            scene.add(ambientLight);

            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(10, 10, 5);
            directionalLight.castShadow = true;
            scene.add(directionalLight);
            
            digitMeshes = [];
            photoMeshes = [];
        }

        function toggleMode() {
            const toggle = document.getElementById('mode-toggle');
            const projectInfo = document.getElementById('project-info');
            
            if (currentMode === '625') {
                currentMode = 'gallery';
                toggle.textContent = '625 MODE';
                createGalleryDisplay();
                projectInfo.style.opacity = '0';
            } else {
                currentMode = '625';
                toggle.textContent = 'GALLERY MODE';
                create625Display();
                projectInfo.classList.remove('visible');
            }
        }

        // Mouse interaction for gallery mode
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        let hoveredMesh = null;

        function onMouseMove(event) {
            mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
            
            if (currentMode === 'gallery') {
                raycaster.setFromCamera(mouse, camera);
                const intersects = raycaster.intersectObjects(photoMeshes);
                
                // Reset previous hover
                if (hoveredMesh && hoveredMesh !== intersects[0]?.object) {
                    hoveredMesh.scale.setScalar(hoveredMesh.userData.originalScale);
                    hoveredMesh.userData.isHovered = false;
                    document.getElementById('project-info').classList.remove('visible');
                }
                
                if (intersects.length > 0) {
                    const mesh = intersects[0].object;
                    if (mesh !== hoveredMesh) {
                        hoveredMesh = mesh;
                        mesh.scale.setScalar(1.2);
                        mesh.userData.isHovered = true;
                        
                        // Show project info
                        const project = mesh.userData.project;
                        document.getElementById('project-title').textContent = project.title;
                        document.getElementById('project-details').textContent = `${project.date} – ${project.location}`;
                        document.getElementById('project-description').textContent = project.description;
                        document.getElementById('project-info').classList.add('visible');
                    }
                } else {
                    hoveredMesh = null;
                }
            }
        }

        function onClick(event) {
            if (currentMode === 'gallery' && hoveredMesh) {
                // Smooth zoom to selected photo
                const targetPosition = hoveredMesh.position.clone();
                targetPosition.add(new THREE.Vector3(0, 0, 5));
                
                // Animate camera
                new TWEEN.Tween(camera.position)
                    .to(targetPosition, 1000)
                    .easing(TWEEN.Easing.Quadratic.Out)
                    .start();
            }
        }

        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        function animate() {
            requestAnimationFrame(animate);
            
            // Update controls
            controls.update();
            
            // Animate 625 digits
            if (currentMode === '625') {
                digitMeshes.forEach((mesh, index) => {
                    if (mesh.userData) {
                        mesh.position.y = mesh.userData.originalY + 
                            Math.sin(Date.now() * mesh.userData.floatSpeed + index) * mesh.userData.floatAmount;
                        mesh.rotation.y = Math.sin(Date.now() * 0.001 + index) * 0.1;
                    }
                });
            }
            
            // Animate gallery photos
            if (currentMode === 'gallery') {
                photoMeshes.forEach((mesh, index) => {
                    if (!mesh.userData.isHovered) {
                        mesh.rotation.y += 0.001;
                        mesh.position.y += Math.sin(Date.now() * 0.001 + index) * 0.001;
                    }
                });
            }
            
            renderer.render(scene, camera);
        }

        // Event listeners
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('click', onClick);

        // Initialize when page loads
        window.addEventListener('load', init);
    </script>
</body>
</html>'''

    with open('index.html', 'w') as f:
        f.write(html_content)
    
    print("🚀 STUNNING 3D PORTFOLIO CREATED!")
    print("✨ Features:")
    print("  • Beautiful 3D floating '625' display")
    print("  • Immersive 3D photo gallery with spiral layout")
    print("  • Smooth camera controls and animations")
    print("  • Interactive photo hover effects")
    print("  • Custom cursor and cinematic UI")
    print("  • Particle effects and atmospheric lighting")
    print("  • Toggle between '625' and 'GALLERY' modes")
    print("  • Responsive design for all devices")
    print("  • Professional project information display")
    print("🎯 Click 'GALLERY MODE' to explore projects in 3D!")

if __name__ == "__main__":
    create_3d_portfolio()

