// Agent Skills Directory Browser
const CATALOG_URL = 'https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json';

let catalog = null;
let filteredSkills = [];

// DOM Elements
const searchInput = document.getElementById('search');
const providerFilter = document.getElementById('provider-filter');
const categoryFilter = document.getElementById('category-filter');
const skillsGrid = document.getElementById('skills-grid');
const modal = document.getElementById('skill-modal');
const modalBody = document.getElementById('modal-body');

// Stats elements
const totalSkillsEl = document.getElementById('total-skills');
const totalProvidersEl = document.getElementById('total-providers');
const totalCategoriesEl = document.getElementById('total-categories');
const filteredCountEl = document.getElementById('filtered-count');
const lastUpdatedEl = document.getElementById('last-updated');

// Initialize
async function init() {
    try {
        const response = await fetch(CATALOG_URL);
        catalog = await response.json();
        
        populateFilters();
        updateStats();
        renderSkills(catalog.skills);
        
        // Update last updated date
        const date = new Date(catalog.generated_at);
        lastUpdatedEl.textContent = date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    } catch (error) {
        console.error('Failed to load catalog:', error);
        skillsGrid.innerHTML = `
            <div class="no-results">
                <p>Failed to load skills catalog.</p>
                <p style="margin-top: 0.5rem; font-size: 0.85rem;">
                    Try refreshing or check <a href="${CATALOG_URL}" target="_blank">the source</a>.
                </p>
            </div>
        `;
    }
}

function populateFilters() {
    // Populate providers
    Object.entries(catalog.providers).forEach(([id, provider]) => {
        const option = document.createElement('option');
        option.value = id;
        option.textContent = `${provider.name} (${provider.skills_count})`;
        providerFilter.appendChild(option);
    });

    // Populate categories
    catalog.categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category.charAt(0).toUpperCase() + category.slice(1);
        categoryFilter.appendChild(option);
    });
}

function updateStats() {
    totalSkillsEl.textContent = catalog.total_skills;
    totalProvidersEl.textContent = Object.keys(catalog.providers).length;
    totalCategoriesEl.textContent = catalog.categories.length;
}

function filterSkills() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    const provider = providerFilter.value;
    const category = categoryFilter.value;

    filteredSkills = catalog.skills.filter(skill => {
        // Search filter
        const matchesSearch = !searchTerm || 
            skill.name.toLowerCase().includes(searchTerm) ||
            skill.description.toLowerCase().includes(searchTerm) ||
            (skill.tags && skill.tags.some(tag => tag.toLowerCase().includes(searchTerm)));

        // Provider filter
        const matchesProvider = !provider || skill.provider === provider;

        // Category filter
        const matchesCategory = !category || skill.category === category;

        return matchesSearch && matchesProvider && matchesCategory;
    });

    filteredCountEl.textContent = filteredSkills.length;
    renderSkills(filteredSkills);
}

function renderSkills(skills) {
    if (skills.length === 0) {
        skillsGrid.innerHTML = `
            <div class="no-results">
                <p>No skills found matching your criteria.</p>
                <p style="margin-top: 0.5rem; font-size: 0.85rem;">Try adjusting your search or filters.</p>
            </div>
        `;
        return;
    }

    skillsGrid.innerHTML = skills.map(skill => `
        <article class="skill-card" data-skill-id="${skill.id}">
            <div class="skill-header">
                <h3 class="skill-name">${escapeHtml(skill.name)}</h3>
                <span class="skill-provider ${skill.provider}">${skill.provider}</span>
            </div>
            <p class="skill-description">${escapeHtml(skill.description)}</p>
            <div class="skill-meta">
                <span class="skill-category">📁 ${skill.category}</span>
                ${(skill.tags || []).slice(0, 3).map(tag => 
                    `<span class="skill-tag">#${escapeHtml(tag)}</span>`
                ).join('')}
            </div>
            ${renderFeatures(skill)}
        </article>
    `).join('');

    // Add click handlers
    document.querySelectorAll('.skill-card').forEach(card => {
        card.addEventListener('click', () => {
            const skillId = card.dataset.skillId;
            const skill = catalog.skills.find(s => s.id === skillId);
            if (skill) showSkillModal(skill);
        });
    });

    // Update filtered count
    filteredCountEl.textContent = skills.length;
}

function renderFeatures(skill) {
    const features = [];
    if (skill.has_scripts) features.push('<span class="feature-badge scripts">📜 scripts</span>');
    if (skill.has_references) features.push('<span class="feature-badge references">📚 references</span>');
    if (skill.has_assets) features.push('<span class="feature-badge assets">📦 assets</span>');
    
    if (features.length === 0) return '';
    
    return `<div class="skill-features">${features.join('')}</div>`;
}

function showSkillModal(skill) {
    const providerInfo = catalog.providers[skill.provider];
    
    modalBody.innerHTML = `
        <div class="modal-header">
            <h2>${escapeHtml(skill.name)}</h2>
            <span class="skill-provider ${skill.provider}">${skill.provider}</span>
            <span class="skill-category">📁 ${skill.category}</span>
        </div>

        <div class="modal-section">
            <h3>Description</h3>
            <p>${escapeHtml(skill.description)}</p>
        </div>

        ${skill.tags && skill.tags.length > 0 ? `
            <div class="modal-section">
                <h3>Tags</h3>
                <div class="modal-tags">
                    ${skill.tags.map(tag => `<span class="skill-tag">#${escapeHtml(tag)}</span>`).join('')}
                </div>
            </div>
        ` : ''}

        <div class="modal-section">
            <h3>Features</h3>
            <div class="modal-tags">
                ${skill.has_scripts ? '<span class="feature-badge scripts">📜 Has scripts</span>' : ''}
                ${skill.has_references ? '<span class="feature-badge references">📚 Has references</span>' : ''}
                ${skill.has_assets ? '<span class="feature-badge assets">📦 Has assets</span>' : ''}
                ${!skill.has_scripts && !skill.has_references && !skill.has_assets ? '<span class="skill-category">SKILL.md only</span>' : ''}
            </div>
        </div>

        ${skill.license ? `
            <div class="modal-section">
                <h3>License</h3>
                <p>${escapeHtml(skill.license)}</p>
            </div>
        ` : ''}

        ${skill.compatibility ? `
            <div class="modal-section">
                <h3>Compatibility</h3>
                <p>${escapeHtml(skill.compatibility)}</p>
            </div>
        ` : ''}

        <div class="modal-section">
            <h3>Source</h3>
            <p style="font-family: monospace; font-size: 0.85rem; color: var(--text-muted);">
                ${escapeHtml(skill.source.path)}
            </p>
        </div>

        <div class="modal-links">
            <a href="${skill.source.skill_md_url}" target="_blank" class="modal-link">
                📄 View SKILL.md
            </a>
            <a href="${skill.source.repo}/tree/main/${skill.source.path}" target="_blank" class="modal-link secondary">
                📂 Browse on GitHub
            </a>
        </div>

        <div class="modal-section" style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border);">
            <h3>Install with Mother Skills MCP</h3>
            <code style="display: block; background: var(--bg); padding: 1rem; border-radius: 8px; font-size: 0.9rem;">
                install_skill("${escapeHtml(skill.name)}")
            </code>
        </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event Listeners
searchInput.addEventListener('input', debounce(filterSkills, 200));
providerFilter.addEventListener('change', filterSkills);
categoryFilter.addEventListener('change', filterSkills);

document.querySelector('.modal-close').addEventListener('click', closeModal);
modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
});
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
});

// Main Navigation Tabs
document.querySelectorAll('.main-tab[data-tab]').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabId = tab.dataset.tab;
        
        // Update active tab
        document.querySelectorAll('.main-tab[data-tab]').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Show corresponding panel
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        const targetPanel = document.getElementById(`tab-${tabId}`);
        if (targetPanel) {
            targetPanel.classList.add('active');
        }
    });
});

// Method Tabs (inside How to Use)
document.querySelectorAll('.method-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Update active tab
        document.querySelectorAll('.method-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Show corresponding content
        const method = tab.dataset.method;
        document.querySelectorAll('.method-content').forEach(content => {
            content.classList.add('hidden');
        });
        document.getElementById(`method-${method}`).classList.remove('hidden');
    });
});

// Utility: Debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Start
init();
