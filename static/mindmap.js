// Mind Map Visualization for Search Results
document.addEventListener('DOMContentLoaded', function() {
    const svg = document.getElementById('mind-map');
    const group = document.getElementById('mind-map-group');
    const zoomInBtn = document.getElementById('zoom-in');
    const zoomOutBtn = document.getElementById('zoom-out');
    const resetBtn = document.getElementById('reset-view');

    let scale = 1;
    let translateX = 0;
    let translateY = 0;
    const centerX = 600;
    const centerY = 400;
    const radius = 250;

    // Render mind map
    function renderMindMap(searchResults) {
        // Clear previous content
        group.innerHTML = '';

        if (!searchResults || searchResults.length === 0) return;

        const numItems = searchResults.length;
        const angleStep = (2 * Math.PI) / numItems;

        // Create nodes
        const nodes = [];
        searchResults.forEach((item, index) => {
            const angle = index * angleStep;
            const x = centerX + radius * Math.cos(angle);
            const y = centerY + radius * Math.sin(angle);

            // Create node group
            const nodeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            nodeGroup.setAttribute('class', 'node');
            nodeGroup.setAttribute('transform', `translate(${x}, ${y})`);

            // Create circle
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('r', '60');
            circle.setAttribute('fill', getColorForCategory(item.masterCategory));
            circle.setAttribute('stroke', '#fff');
            circle.setAttribute('stroke-width', '2');

            // Create text
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('dy', '0.35em');
            text.setAttribute('fill', '#fff');
            text.setAttribute('font-size', '12px');
            text.setAttribute('font-weight', 'bold');
            text.textContent = item.productDisplayName.length > 15 ?
                item.productDisplayName.substring(0, 15) + '...' :
                item.productDisplayName;

            // Add tooltip
            const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
            title.textContent = `${item.productDisplayName}\nCategory: ${item.masterCategory} - ${item.subCategory}\nColor: ${item.baseColour}\nSeason: ${item.season}`;

            nodeGroup.appendChild(circle);
            nodeGroup.appendChild(text);
            nodeGroup.appendChild(title);

            // Add click event
            nodeGroup.addEventListener('click', () => showItemDetails(item));

            group.appendChild(nodeGroup);
            nodes.push({ x, y, item, group: nodeGroup });
        });

        // Create connections
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                if (nodes[i].item.masterCategory === nodes[j].item.masterCategory ||
                    nodes[i].item.baseColour === nodes[j].item.baseColour) {
                    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                    line.setAttribute('x1', nodes[i].x);
                    line.setAttribute('y1', nodes[i].y);
                    line.setAttribute('x2', nodes[j].x);
                    line.setAttribute('y2', nodes[j].y);
                    line.setAttribute('stroke', '#ccc');
                    line.setAttribute('stroke-width', '1');
                    line.setAttribute('opacity', '0.6');
                    group.insertBefore(line, group.firstChild);
                }
            }
        }

        updateTransform();
    }

    // Show item details in a modal
    function showItemDetails(item) {
        // Remove existing modal
        const existingModal = document.querySelector('.item-details-modal');
        if (existingModal) {
            existingModal.remove();
        }

        // Create modal
        const modal = document.createElement('div');
        modal.className = 'item-details-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close-button">&times;</span>
                <h2>${item.productDisplayName}</h2>
                ${item.image ? `<img src="${item.image}" alt="${item.productDisplayName}" class="item-image">` : ''}
                <div class="item-details">
                    <p><strong>Category:</strong> ${item.masterCategory} - ${item.subCategory}</p>
                    <p><strong>Color:</strong> ${item.baseColour}</p>
                    <p><strong>Season:</strong> ${item.season}</p>
                    ${item.productDescription ? `<p><strong>Description:</strong> ${item.productDescription}</p>` : ''}
                    ${item.price ? `<p><strong>Price:</strong> ${item.price}</p>` : ''}
                    ${item.brandName ? `<p><strong>Brand:</strong> ${item.brandName}</p>` : ''}
                    ${item.ageGroup ? `<p><strong>Age Group:</strong> ${item.ageGroup}</p>` : ''}
                    ${item.gender ? `<p><strong>Gender:</strong> ${item.gender}</p>` : ''}
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Close modal functionality
        const closeBtn = modal.querySelector('.close-button');
        closeBtn.onclick = () => modal.remove();

        modal.onclick = (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        };

        // Prevent event bubbling
        modal.querySelector('.modal-content').onclick = (e) => e.stopPropagation();
    }

    // Color mapping for categories
    function getColorForCategory(category) {
        const colors = {
            'Apparel': '#FF6B6B',
            'Accessories': '#4ECDC4',
            'Footwear': '#45B7D1',
            'Personal Care': '#FFA07A',
            'Free Items': '#98D8C8',
            'Sporting Goods': '#F7DC6F',
            'Home': '#BB8FCE'
        };
        return colors[category] || '#95A5A6';
    }

    // Update SVG transform
    function updateTransform() {
        group.setAttribute('transform', `translate(${translateX}, ${translateY}) scale(${scale})`);
    }

    // Zoom and pan functionality
    let isDragging = false;
    let lastMouseX, lastMouseY;

    svg.addEventListener('mousedown', (e) => {
        isDragging = true;
        lastMouseX = e.clientX;
        lastMouseY = e.clientY;
        svg.style.cursor = 'grabbing';
    });

    svg.addEventListener('mousemove', (e) => {
        if (isDragging) {
            const dx = e.clientX - lastMouseX;
            const dy = e.clientY - lastMouseY;
            translateX += dx;
            translateY += dy;
            updateTransform();
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
        }
    });

    svg.addEventListener('mouseup', () => {
        isDragging = false;
        svg.style.cursor = 'grab';
    });

    svg.addEventListener('mouseleave', () => {
        isDragging = false;
        svg.style.cursor = 'grab';
    });

    // Zoom with mouse wheel
    svg.addEventListener('wheel', (e) => {
        e.preventDefault();
        const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
        scale *= zoomFactor;
        scale = Math.max(0.1, Math.min(5, scale)); // Limit zoom
        updateTransform();
    });

    // Button controls
    zoomInBtn.addEventListener('click', () => {
        scale *= 1.2;
        scale = Math.min(5, scale);
        updateTransform();
    });

    zoomOutBtn.addEventListener('click', () => {
        scale *= 0.8;
        scale = Math.max(0.1, scale);
        updateTransform();
    });

    resetBtn.addEventListener('click', () => {
        scale = 1;
        translateX = 0;
        translateY = 0;
        updateTransform();
    });

    // Initial render
    renderMindMap();
});