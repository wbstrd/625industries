#!/usr/bin/env python3

def restore_clock_functions():
    """Add back the missing clock JavaScript functions"""
    
    with open('index_with_carousel.html', 'r') as f:
        content = f.read()
    
    # The clock functions that are missing
    clock_functions = '''
        // Clock digit patterns
        const digits = {
            0: [
                '  ███  ',
                ' █   █ ',
                ' █   █ ',
                ' █   █ ',
                ' █   █ ',
                ' █   █ ',
                '  ███  '
            ],
            1: [
                '   █   ',
                '  ██   ',
                '   █   ',
                '   █   ',
                '   █   ',
                '   █   ',
                ' █████ '
            ],
            2: [
                ' █████ ',
                '     █ ',
                '     █ ',
                ' █████ ',
                ' █     ',
                ' █     ',
                ' █████ '
            ],
            3: [
                ' █████ ',
                '     █ ',
                '     █ ',
                ' █████ ',
                '     █ ',
                '     █ ',
                ' █████ '
            ],
            4: [
                ' █   █ ',
                ' █   █ ',
                ' █   █ ',
                ' █████ ',
                '     █ ',
                '     █ ',
                '     █ '
            ],
            5: [
                ' █████ ',
                ' █     ',
                ' █     ',
                ' █████ ',
                '     █ ',
                '     █ ',
                ' █████ '
            ],
            6: [
                ' █████ ',
                ' █     ',
                ' █     ',
                ' █████ ',
                ' █   █ ',
                ' █   █ ',
                ' █████ '
            ],
            7: [
                ' █████ ',
                '     █ ',
                '     █ ',
                '     █ ',
                '     █ ',
                '     █ ',
                '     █ '
            ],
            8: [
                ' █████ ',
                ' █   █ ',
                ' █   █ ',
                ' █████ ',
                ' █   █ ',
                ' █   █ ',
                ' █████ '
            ],
            9: [
                ' █████ ',
                ' █   █ ',
                ' █   █ ',
                ' █████ ',
                '     █ ',
                '     █ ',
                ' █████ '
            ],
            ':': [
                '       ',
                '   █   ',
                '       ',
                '       ',
                '       ',
                '   █   ',
                '       '
            ]
        };

        let tiles = [], imgRefs = [], currentTime = '', isToggled = false;
        let scale = 1, holder;

        function updateClock() {
            const now = new Date();
            const time = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
            
            if (time !== currentTime) {
                currentTime = time;
                renderTime(currentTime);
            }
        }

        function renderTime(time) {
            const timeStr = time.replace(/:/g, ':');
            let grid = Array(HEIGHT).fill().map(() => Array(WIDTH * timeStr.length + (timeStr.length - 1) * DIGIT_SPACING).fill(false));
            
            let xOffset = 0;
            for (let i = 0; i < timeStr.length; i++) {
                const char = timeStr[i];
                const pattern = digits[char];
                if (pattern) {
                    for (let row = 0; row < pattern.length; row++) {
                        for (let col = 0; col < pattern[row].length; col++) {
                            if (pattern[row][col] === '█') {
                                grid[row][xOffset + col] = true;
                            }
                        }
                    }
                }
                xOffset += WIDTH + DIGIT_SPACING;
            }
            
            const clock = document.getElementById('clock625');
            if (!clock) return;
            
            clock.innerHTML = '';
            clock.style.gridTemplateColumns = `repeat(${grid[0].length}, 16px)`;
            clock.style.gridTemplateRows = `repeat(${HEIGHT}, 16px)`;
            
            tiles = [];
            
            for (let row = 0; row < HEIGHT; row++) {
                for (let col = 0; col < grid[row].length; col++) {
                    const tile = document.createElement('div');
                    tile.className = 'tile';
                    if (grid[row][col]) {
                        const img = document.createElement('img');
                        const imageIndex = Math.floor(Math.random() * NUM_IMAGES) + 1;
                        const paddedIndex = String(imageIndex).padStart(3, '0');
                        img.dataset.src = `img${paddedIndex}.jpg`;
                        img.src = `${BASE_PATH}${poolPaths.low}/img${paddedIndex}-low.jpg`;
                        img.loading = 'lazy';
                        tile.appendChild(img);
                    }
                    clock.appendChild(tile);
                    tiles.push(tile);
                }
            }
            
            updateImageRefs();
        }

        function updateImageRefs() {
            imgRefs = [];
            const allImages = document.querySelectorAll('#clock625 img');
            allImages.forEach(img => {
                const div = img.parentElement;
                imgRefs.push({ div, img, key: img.dataset.src });
            });
            
            if (!holder) {
                holder = document.getElementById('clock625');
            }
        }

        function updateZoom() {
            const clock = document.getElementById('clock625');
            if (!clock) return;
            
            if (scale >= 5) {
                clock.classList.add('zoomed');
                imgRefs.forEach(({ img, key }) => {
                    img.src = `${BASE_PATH}${poolPaths.high}/img${key.replace('.jpg', '-high.jpg')}`;
                });
            } else if (scale >= 3) {
                clock.classList.remove('zoomed');
                imgRefs.forEach(({ img, key }) => {
                    img.src = `${BASE_PATH}${poolPaths.high1200}/img${key.replace('.jpg', '-high.jpg')}`;
                });
            } else if (scale >= 1.8) {
                clock.classList.remove('zoomed');
                imgRefs.forEach(({ img, key }) => {
                    img.src = `${BASE_PATH}${poolPaths.medium}/img${key.replace('.jpg', '-med.jpg')}`;
                });
            } else if (scale >= 1.2) {
                clock.classList.remove('zoomed');
                imgRefs.forEach(({ img, key }) => {
                    img.src = `${BASE_PATH}${poolPaths.small}/img${key.replace('.jpg', '-small.jpg')}`;
                });
            } else {
                clock.classList.remove('zoomed');
                imgRefs.forEach(({ img, key }) => {
                    img.src = `${BASE_PATH}${poolPaths.low}/img${key.replace('.jpg', '-low.jpg')}`;
                });
            }
            
            if (holder) {
                holder.style.transform = `scale(${scale})`;
            }
        }

        // Zoom with scroll
        document.addEventListener("wheel", e => {
            e.preventDefault();
            scale *= e.deltaY > 0 ? 0.9 : 1.1;
            scale = Math.max(0.5, Math.min(scale, 20));
            updateZoom();
        });

        // Toggle functionality
        document.getElementById("toggle-button").addEventListener("click", () => {
            isToggled = !isToggled;
            const projectList = document.getElementById("project-list");
            const clock = document.getElementById("clock625");
            const toggleCircle = document.getElementById("toggle-circle");
            
            if (isToggled) {
                projectList.style.display = "block";
                clock.style.display = "none";
                toggleCircle.style.left = "32px";
            } else {
                projectList.style.display = "none";
                clock.style.display = "grid";
                toggleCircle.style.left = "4px";
            }
        });

        // Start the clock
        setInterval(updateClock, 1000);
        updateClock();'''
    
    # Find where to insert the clock functions (before the wind blow effect)
    insertion_point = content.find('        // Combined hover interactions with wind blow effect')
    
    if insertion_point == -1:
        print("Could not find insertion point")
        return False
    
    # Insert the clock functions
    content = content[:insertion_point] + clock_functions + '\n\n' + content[insertion_point:]
    
    # Write the updated file
    with open('index_with_carousel.html', 'w') as f:
        f.write(content)
    
    print("✅ Clock functions restored!")
    return True

if __name__ == "__main__":
    restore_clock_functions()
