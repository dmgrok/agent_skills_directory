// Agent Skills Directory Browser
const CATALOG_URL_CDN = 'https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json';
const CATALOG_URL_LOCAL = './catalog.json';
const BUNDLES_URL_CDN = 'https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/bundles.json';
const BUNDLES_URL_LOCAL = './bundles.json';
// Use local file when testing on localhost, otherwise use CDN
const CATALOG_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? CATALOG_URL_LOCAL 
    : CATALOG_URL_CDN;
const BUNDLES_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? BUNDLES_URL_LOCAL 
    : BUNDLES_URL_CDN;

let catalog = null;
let bundles = null;
let filteredSkills = [];
let filteredBundles = [];

// Pagination state
const SKILLS_PER_PAGE = 24;
let currentPage = 1;

// Search optimization: pre-built index and cache
let searchIndex = null;
let searchCache = new Map();
const SEARCH_CACHE_MAX_SIZE = 50;

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

// Bundles elements
const bundlesGrid = document.getElementById('bundles-grid');
const bundleCategoryFilter = document.getElementById('bundle-category-filter');
const totalBundlesEl = document.getElementById('total-bundles');

// Parse URL query parameters for filtering
// Supports: ?id=xxx, ?provider=xxx, ?category=xxx, ?search=xxx, ?tags=a,b,c
function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        id: params.get('id'),
        provider: params.get('provider'),
        category: params.get('category'),
        search: params.get('search') || params.get('q'),
        tags: params.get('tags')?.split(',').map(t => t.trim().toLowerCase()) || []
    };
}

// Apply URL query params to filters and trigger filtering
function applyQueryParams() {
    const params = getQueryParams();
    
    if (params.search) {
        searchInput.value = params.search;
    }
    if (params.provider && providerFilter.querySelector(`option[value="${params.provider}"]`)) {
        providerFilter.value = params.provider;
    }
    if (params.category && categoryFilter.querySelector(`option[value="${params.category}"]`)) {
        categoryFilter.value = params.category;
    }
    
    // If id param, show that skill's modal directly
    if (params.id) {
        const skill = catalog.skills.find(s => s.id === params.id || s.name === params.id);
        if (skill) {
            setTimeout(() => showSkillModal(skill), 100);
        }
    }
    
    // Tags filter applied in filterSkills
    filterSkills();
}

// Update URL when filters change (without page reload)
function updateURLParams() {
    const params = new URLSearchParams();
    if (searchInput.value) params.set('search', searchInput.value);
    if (providerFilter.value) params.set('provider', providerFilter.value);
    if (categoryFilter.value) params.set('category', categoryFilter.value);
    
    const newURL = params.toString() 
        ? `${window.location.pathname}?${params.toString()}`
        : window.location.pathname;
    window.history.replaceState({}, '', newURL);
}

// Initialize
async function init() {
    const loader = document.getElementById('loading-spinner');
    
    try {
        // Show loader
        if (loader) loader.style.display = 'flex';
        
        // Load catalog and bundles in parallel
        const [catalogResponse, bundlesResponse] = await Promise.all([
            fetch(CATALOG_URL, { cache: 'no-cache' }),
            fetch(BUNDLES_URL, { cache: 'no-cache' }).catch(() => null)
        ]);
        
        catalog = await catalogResponse.json();
        
        if (bundlesResponse && bundlesResponse.ok) {
            bundles = await bundlesResponse.json();
            initBundles();
        } else if (typeof bundlesGrid !== 'undefined' && bundlesGrid) {
            // Provide feedback when bundles fail to load or are unavailable
            bundlesGrid.innerHTML = `
                <div class="no-results">
                    <p>No bundles available or failed to load bundles.</p>
                    <p style="margin-top: 0.5rem; font-size: 0.85rem;">
                        Try refreshing or check <a href="${BUNDLES_URL}" target="_blank">the bundles source</a>.
                    </p>
                </div>
            `;
        }
        
        populateFilters();
        buildSearchIndex(); // Build search index for fast lookups
        updateStats();
        applyQueryParams(); // Apply URL params after loading
        
        // Update last updated date
        const date = new Date(catalog.generated_at);
        lastUpdatedEl.textContent = date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        // Hide loader
        if (loader) loader.style.display = 'none';
    } catch (error) {
        console.error('Failed to load catalog:', error);
        
        // Hide loader
        if (loader) loader.style.display = 'none';
        
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
    // Populate providers (sorted by stars descending, then by name)
    const sortedProviders = Object.entries(catalog.providers)
        .sort((a, b) => {
            const starsA = a[1].stars || 0;
            const starsB = b[1].stars || 0;
            if (starsB !== starsA) return starsB - starsA;
            return a[1].name.localeCompare(b[1].name);
        });
    
    sortedProviders.forEach(([id, provider]) => {
        const option = document.createElement('option');
        option.value = id;
        const starsText = provider.stars ? ` ⭐${formatStars(provider.stars)}` : '';
        option.textContent = `${provider.name} (${provider.skills_count})${starsText}`;
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

// Format star count (e.g., 1234 -> 1.2k)
function formatStars(stars) {
    if (stars >= 1000) {
        return (stars / 1000).toFixed(1) + 'k';
    }
    return stars.toString();
}

function updateStats() {
    totalSkillsEl.textContent = catalog.total_skills;
    totalProvidersEl.textContent = Object.keys(catalog.providers).length;
    totalCategoriesEl.textContent = catalog.categories.length;
}

// Build search index for O(1) lookups on pre-processed text
function buildSearchIndex() {
    searchIndex = catalog.skills.map((skill, index) => {
        // Pre-concatenate and lowercase all searchable fields
        const tagsText = (skill.tags || []).join(' ').toLowerCase();
        const searchText = `${skill.name.toLowerCase()} ${skill.description.toLowerCase()} ${tagsText}`;
        
        return {
            index,
            searchText,
            tagsLower: (skill.tags || []).map(t => t.toLowerCase()),
            provider: skill.provider,
            category: skill.category
        };
    });
    
    // Clear cache when index is rebuilt
    searchCache.clear();
}

// Get cache key for current filter state
function getSearchCacheKey(searchTerm, provider, category, urlTags) {
    return `${searchTerm}|${provider}|${category}|${urlTags.join(',')}`;
}

function filterSkills() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    const provider = providerFilter.value;
    const category = categoryFilter.value;
    const urlTags = getQueryParams().tags;
    
    // Check cache first
    const cacheKey = getSearchCacheKey(searchTerm, provider, category, urlTags);
    if (searchCache.has(cacheKey)) {
        filteredSkills = searchCache.get(cacheKey);
        filteredCountEl.textContent = filteredSkills.length;
        currentPage = 1;
        updateURLParams();
        renderSkills(filteredSkills);
        return;
    }

    // Use search index for fast filtering
    const matchingIndices = [];
    const hasSearch = searchTerm.length > 0;
    const hasProvider = provider.length > 0;
    const hasCategory = category.length > 0;
    const hasUrlTags = urlTags.length > 0;
    
    for (let i = 0; i < searchIndex.length; i++) {
        const entry = searchIndex[i];
        
        // Provider filter (fastest - direct comparison)
        if (hasProvider && entry.provider !== provider) continue;
        
        // Category filter (fast - direct comparison)
        if (hasCategory && entry.category !== category) continue;
        
        // Search filter (use pre-built searchText)
        if (hasSearch && entry.searchText.indexOf(searchTerm) === -1) continue;
        
        // Tags filter from URL
        if (hasUrlTags) {
            let allTagsMatch = true;
            for (const t of urlTags) {
                let found = false;
                for (const st of entry.tagsLower) {
                    if (st.indexOf(t) !== -1) {
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    allTagsMatch = false;
                    break;
                }
            }
            if (!allTagsMatch) continue;
        }
        
        matchingIndices.push(entry.index);
    }
    
    // Map indices back to skills
    filteredSkills = matchingIndices.map(i => catalog.skills[i]);
    
    // Cache the result (with LRU-style eviction)
    if (searchCache.size >= SEARCH_CACHE_MAX_SIZE) {
        const firstKey = searchCache.keys().next().value;
        searchCache.delete(firstKey);
    }
    searchCache.set(cacheKey, filteredSkills);

    filteredCountEl.textContent = filteredSkills.length;
    currentPage = 1; // Reset to first page when filters change
    updateURLParams();
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
        renderPagination(0, 0);
        return;
    }

    // Pagination calculations
    const totalPages = Math.ceil(skills.length / SKILLS_PER_PAGE);
    const startIndex = (currentPage - 1) * SKILLS_PER_PAGE;
    const endIndex = startIndex + SKILLS_PER_PAGE;
    const paginatedSkills = skills.slice(startIndex, endIndex);

    skillsGrid.innerHTML = paginatedSkills.map(skill => {
        const updatedLabel = formatDate(skill.last_updated_at);
        const provider = catalog.providers[skill.provider];
        const starsHtml = provider && provider.stars 
            ? `<span class="skill-stars" title="${provider.stars.toLocaleString()} GitHub stars">⭐ ${formatStars(provider.stars)}</span>` 
            : '';
        
        // Generate duplicate badge if skill is annotated
        let duplicateBadge = '';
        if (skill.duplicate_status) {
            const badgeClass = skill.duplicate_status === 'mirror' ? 'duplicate-badge-mirror' : 'duplicate-badge-probable';
            const badgeText = skill.duplicate_status === 'mirror' ? '🔄 Mirror' : '⚠️ Probable Duplicate';
            duplicateBadge = `<span class="duplicate-badge ${badgeClass}" title="${escapeHtml(skill.duplicate_annotation || '')}">${badgeText}</span>`;
        }

        return `
        <article class="skill-card ${skill.duplicate_status ? 'skill-card-duplicate' : ''}" data-skill-id="${skill.id}">
            <div class="skill-header">
                <h3 class="skill-name">${escapeHtml(skill.name)}</h3>
                <div class="skill-header-badges">
                    <span class="skill-provider ${skill.provider}">${skill.provider}</span>
                    ${starsHtml}
                    ${duplicateBadge}
                </div>
            </div>
            <p class="skill-description">${escapeHtml(skill.description)}</p>
            <div class="skill-meta">
                <span class="skill-category">📁 ${skill.category}</span>
                ${(skill.tags || []).slice(0, 3).map(tag => 
                    `<span class="skill-tag">#${escapeHtml(tag)}</span>`
                ).join('')}
            </div>
            ${updatedLabel ? `<p class="skill-updated">⏱ Updated ${updatedLabel}</p>` : ''}
            ${renderFeatures(skill)}
        </article>
    `;
    }).join('');

    // Add click handlers
    document.querySelectorAll('.skill-card').forEach(card => {
        card.addEventListener('click', () => {
            const skillId = card.dataset.skillId;
            const skill = catalog.skills.find(s => s.id === skillId);
            if (skill) showSkillModal(skill);
        });
    });

    // Update filtered count and render pagination
    filteredCountEl.textContent = skills.length;
    renderPagination(skills.length, totalPages);
}

function renderPagination(totalSkills, totalPages) {
    // Remove existing pagination
    const existingPagination = document.querySelector('.pagination');
    if (existingPagination) existingPagination.remove();

    if (totalPages <= 1) return;

    const pagination = document.createElement('div');
    pagination.className = 'pagination';

    // Previous button
    const prevBtn = document.createElement('button');
    prevBtn.className = 'pagination-btn';
    prevBtn.innerHTML = '← Prev';
    prevBtn.disabled = currentPage === 1;
    prevBtn.addEventListener('click', () => goToPage(currentPage - 1));

    // Page info
    const pageInfo = document.createElement('span');
    pageInfo.className = 'pagination-info';
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;

    // Page numbers
    const pageNumbers = document.createElement('div');
    pageNumbers.className = 'pagination-numbers';
    
    const maxVisiblePages = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
    
    if (endPage - startPage < maxVisiblePages - 1) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    if (startPage > 1) {
        pageNumbers.appendChild(createPageBtn(1));
        if (startPage > 2) {
            const ellipsis = document.createElement('span');
            ellipsis.className = 'pagination-ellipsis';
            ellipsis.textContent = '...';
            pageNumbers.appendChild(ellipsis);
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        pageNumbers.appendChild(createPageBtn(i));
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            const ellipsis = document.createElement('span');
            ellipsis.className = 'pagination-ellipsis';
            ellipsis.textContent = '...';
            pageNumbers.appendChild(ellipsis);
        }
        pageNumbers.appendChild(createPageBtn(totalPages));
    }

    // Next button
    const nextBtn = document.createElement('button');
    nextBtn.className = 'pagination-btn';
    nextBtn.innerHTML = 'Next →';
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.addEventListener('click', () => goToPage(currentPage + 1));

    pagination.appendChild(prevBtn);
    pagination.appendChild(pageNumbers);
    pagination.appendChild(pageInfo);
    pagination.appendChild(nextBtn);

    // Insert after skills grid
    skillsGrid.parentNode.insertBefore(pagination, skillsGrid.nextSibling);
}

function createPageBtn(pageNum) {
    const btn = document.createElement('button');
    btn.className = 'pagination-page' + (pageNum === currentPage ? ' active' : '');
    btn.textContent = pageNum;
    btn.addEventListener('click', () => goToPage(pageNum));
    return btn;
}

function goToPage(page) {
    currentPage = page;
    renderSkills(filteredSkills);
    // Scroll to top of skills section
    document.querySelector('.skills-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderFeatures(skill) {
    const features = [];
    if (skill.has_scripts) features.push('<span class="feature-badge scripts">📜 scripts</span>');
    if (skill.has_references) features.push('<span class="feature-badge references">📚 references</span>');
    if (skill.has_assets) features.push('<span class="feature-badge assets">📦 assets</span>');
    
    if (features.length === 0) return '';
    
    return `<div class="skill-features">${features.join('')}</div>`;
}

    function formatDate(dateString) {
        if (!dateString) return null;
        const date = new Date(dateString);
        if (Number.isNaN(date.getTime())) return null;
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

function showSkillModal(skill) {
    const updatedLabel = formatDate(skill.last_updated_at);
    const provider = catalog.providers[skill.provider];
    const starsHtml = provider && provider.stars 
        ? `<span class="modal-stars">⭐ ${formatStars(provider.stars)} stars</span>` 
        : '';
    
    modalBody.innerHTML = `
        <div class="modal-header">
            <h2>${escapeHtml(skill.name)}</h2>
            <div class="modal-header-badges">
                <span class="skill-provider ${skill.provider}">${skill.provider}</span>
                ${starsHtml}
                <span class="skill-category">📁 ${skill.category}</span>
            </div>
        </div>

        <div class="modal-section">
            <p class="skill-description-large">${escapeHtml(skill.description)}</p>
        </div>

        ${updatedLabel ? `
            <div class="modal-meta">
                <span>⏱ Updated ${updatedLabel}</span>
                ${skill.license ? `<span>📜 ${escapeHtml(skill.license)}</span>` : ''}
            </div>
        ` : ''}

        ${skill.tags && skill.tags.length > 0 ? `
            <div class="modal-tags">
                ${skill.tags.map(tag => `<span class="skill-tag">#${escapeHtml(tag)}</span>`).join('')}
            </div>
        ` : ''}

        <div class="modal-actions">
            <button class="modal-action-btn primary" onclick="copyInstallCommand('${escapeHtml(skill.id)}')">
                📋 Copy Install Command
            </button>
            <a href="${skill.source.repo}/tree/main/${skill.source.path}" target="_blank" class="modal-action-btn secondary">
                📂 View on GitHub
            </a>
        </div>

        <div class="modal-section skill-content-section">
            <div class="skill-content-header">
                <h3>📄 SKILL.md</h3>
                <button class="btn-toggle-raw" onclick="toggleRawView()">View Raw</button>
            </div>
            <div id="skill-content" class="skill-content">
                <div class="loading-content">Loading skill content...</div>
            </div>
            <div id="skill-content-raw" class="skill-content-raw" style="display: none;">
                <pre><code class="loading-content">Loading...</code></pre>
            </div>
        </div>

        ${skill.similar_skills && skill.similar_skills.length > 0 ? `
            <div class="modal-section similar-skills-section">
                <h3>🔗 Similar Skills</h3>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.75rem;">
                    Other implementations with different content:
                </p>
                <div class="similar-skills-list">
                    ${skill.similar_skills.map(s => `
                        <div class="similar-skill-item" data-skill-id="${escapeHtml(s.id)}">
                            <span class="skill-provider ${s.provider}">${s.provider}</span>
                            <span class="similar-skill-id">${escapeHtml(s.id)}</span>
                            <span class="similarity-badge">${Math.round(s.similarity * 100)}% similar</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        ` : ''}
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Fetch and render SKILL.md content
    fetchSkillContent(skill.source.skill_md_url);
    
    // Add click handlers for similar skill items
    document.querySelectorAll('.similar-skill-item').forEach(item => {
        item.addEventListener('click', () => {
            const skillId = item.dataset.skillId;
            const similarSkill = catalog.skills.find(s => s.id === skillId);
            if (similarSkill) showSkillModal(similarSkill);
        });
    });
}

// Fetch and render SKILL.md content
async function fetchSkillContent(url) {
    const contentEl = document.getElementById('skill-content');
    const rawEl = document.getElementById('skill-content-raw');
    
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch');
        
        const rawContent = await response.text();
        
        // Remove YAML frontmatter if present
        let content = rawContent;
        if (content.startsWith('---')) {
            const endOfFrontmatter = content.indexOf('---', 3);
            if (endOfFrontmatter !== -1) {
                content = content.substring(endOfFrontmatter + 3).trim();
            }
        }
        
        // Render markdown
        if (typeof marked !== 'undefined') {
            contentEl.innerHTML = marked.parse(content);
        } else {
            // Fallback: basic formatting
            contentEl.innerHTML = `<pre>${escapeHtml(content)}</pre>`;
        }
        
        // Store raw content
        rawEl.innerHTML = `<pre><code>${escapeHtml(rawContent)}</code></pre>`;
        
    } catch (error) {
        contentEl.innerHTML = `
            <div class="content-error">
                <p>Unable to load skill content.</p>
                <a href="${url}" target="_blank">View on GitHub →</a>
            </div>
        `;
        rawEl.innerHTML = `<pre><code>Error loading content</code></pre>`;
    }
}

// Toggle between rendered and raw view
function toggleRawView() {
    const contentEl = document.getElementById('skill-content');
    const rawEl = document.getElementById('skill-content-raw');
    const btn = document.querySelector('.btn-toggle-raw');
    
    if (rawEl.style.display === 'none') {
        rawEl.style.display = 'block';
        contentEl.style.display = 'none';
        btn.textContent = 'View Rendered';
    } else {
        rawEl.style.display = 'none';
        contentEl.style.display = 'block';
        btn.textContent = 'View Raw';
    }
}

// Copy install command to clipboard
function copyInstallCommand(skillId) {
    const command = `skillsdir install ${skillId}`;
    navigator.clipboard.writeText(command).then(() => {
        const btn = document.querySelector('.modal-action-btn.primary');
        const originalText = btn.innerHTML;
        btn.innerHTML = '✓ Copied!';
        setTimeout(() => btn.innerHTML = originalText, 2000);
    });
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

// ===== BUNDLES FUNCTIONALITY =====

function initBundles() {
    if (!bundles || !bundles.bundles) return;
    
    // Populate category filter
    const categories = [...new Set(bundles.bundles.map(b => b.category))].sort();
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category.charAt(0).toUpperCase() + category.slice(1);
        bundleCategoryFilter.appendChild(option);
    });
    
    // Update total
    totalBundlesEl.textContent = bundles.total_bundles;
    
    // Initial render
    filterBundles();
    
    // Add event listener
    bundleCategoryFilter.addEventListener('change', filterBundles);
}

function filterBundles() {
    if (!bundles || !bundles.bundles) return;
    
    const category = bundleCategoryFilter.value;
    
    filteredBundles = bundles.bundles.filter(bundle => {
        return !category || bundle.category === category;
    });
    
    renderBundles(filteredBundles);
}

function renderBundles(bundlesList) {
    if (!bundlesList || bundlesList.length === 0) {
        bundlesGrid.innerHTML = `
            <div class="no-results">
                <p>No bundles found matching your criteria.</p>
            </div>
        `;
        return;
    }

    bundlesGrid.innerHTML = bundlesList.map(bundle => `
        <article class="bundle-card" data-bundle-id="${bundle.id}">
            <div class="bundle-header">
                <span class="bundle-icon">${bundle.icon || '📦'}</span>
                <div class="bundle-title-group">
                    <h3 class="bundle-name">${escapeHtml(bundle.name)}</h3>
                    <span class="bundle-category-badge">${bundle.category}</span>
                </div>
            </div>
            <p class="bundle-description">${escapeHtml(bundle.description)}</p>
            
            <div class="bundle-skills">
                <span class="bundle-skills-label">📚 ${bundle.skills.length} skills included:</span>
                <div class="bundle-skills-list">
                    ${bundle.skills.slice(0, 4).map(skill => 
                        `<span class="bundle-skill-item">${escapeHtml(skill)}</span>`
                    ).join('')}
                    ${bundle.skills.length > 4 ? `<span class="bundle-skill-more">+${bundle.skills.length - 4} more</span>` : ''}
                </div>
            </div>
            
            <div class="bundle-use-cases">
                <span class="bundle-use-cases-label">💡 Use cases:</span>
                <div class="bundle-use-cases-list">
                    ${bundle.use_cases.map(uc => `<span class="bundle-use-case">${escapeHtml(uc)}</span>`).join('')}
                </div>
            </div>
            
            <div class="bundle-tags">
                ${bundle.tags.map(tag => `<span class="bundle-tag">#${escapeHtml(tag)}</span>`).join('')}
            </div>
        </article>
    `).join('');

    // Add click handlers
    document.querySelectorAll('.bundle-card').forEach(card => {
        card.addEventListener('click', () => {
            const bundleId = card.dataset.bundleId;
            const bundle = bundles.bundles.find(b => b.id === bundleId);
            if (bundle) showBundleModal(bundle);
        });
    });
}

function showBundleModal(bundle) {
    modalBody.innerHTML = `
        <div class="modal-header">
            <span class="bundle-icon-large">${bundle.icon || '📦'}</span>
            <h2>${escapeHtml(bundle.name)}</h2>
            <span class="bundle-category-badge">${bundle.category}</span>
        </div>

        <div class="modal-section">
            <h3>Description</h3>
            <p>${escapeHtml(bundle.description)}</p>
        </div>

        <div class="modal-section">
            <h3>📚 Included Skills (${bundle.skills.length})</h3>
            <div class="bundle-skills-grid">
                ${bundle.skills.map(skill => {
                    const skillData = catalog?.skills?.find(s => s.id === skill || s.name === (skill.split('/')[1] ?? skill));
                    return `
                        <div class="bundle-skill-card ${skillData ? 'clickable' : ''}" data-skill-id="${skillData?.id || ''}">
                            <span class="bundle-skill-name">${escapeHtml(skill)}</span>
                            ${skillData ? `<span class="bundle-skill-provider ${skillData.provider}">${skillData.provider}</span>` : '<span class="bundle-skill-missing">not in catalog</span>'}
                        </div>
                    `;
                }).join('')}
            </div>
        </div>

        <div class="modal-section">
            <h3>💡 Use Cases</h3>
            <ul class="bundle-use-cases-modal">
                ${bundle.use_cases.map(uc => `<li>${escapeHtml(uc)}</li>`).join('')}
            </ul>
        </div>

        <div class="modal-section">
            <h3>Tags</h3>
            <div class="modal-tags">
                ${bundle.tags.map(tag => `<span class="skill-tag">#${escapeHtml(tag)}</span>`).join('')}
            </div>
        </div>

        <div class="modal-section" style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border);">
            <h3>Install Bundle with Mother Skills MCP</h3>
            <code style="display: block; background: var(--bg); padding: 1rem; border-radius: 8px; font-size: 0.9rem;">
                install_bundle("${escapeHtml(bundle.id)}")
            </code>
            <p style="margin-top: 0.75rem; font-size: 0.85rem; color: var(--text-muted);">
                Or install skills individually:
            </p>
            <code style="display: block; background: var(--bg); padding: 1rem; border-radius: 8px; font-size: 0.85rem; margin-top: 0.5rem; white-space: pre-wrap;">
${bundle.skills.map(s => `install_skill("${s.split('/')[1] ?? s}")`).join('\n')}</code>
        </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Add click handlers for skill cards that exist in catalog
    document.querySelectorAll('.bundle-skill-card.clickable').forEach(card => {
        card.addEventListener('click', (e) => {
            e.stopPropagation();
            const skillId = card.dataset.skillId;
            const skill = catalog.skills.find(s => s.id === skillId);
            if (skill) showSkillModal(skill);
        });
    });
}

// Method tabs (How to Use section)
document.querySelectorAll('.method-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const methodId = tab.dataset.method;
        
        // Update tabs
        document.querySelectorAll('.method-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Update content
        document.querySelectorAll('.method-content').forEach(content => {
            content.classList.add('hidden');
        });
        const targetContent = document.getElementById(`method-${methodId}`);
        if (targetContent) {
            targetContent.classList.remove('hidden');
        }
    });
});

// Quickstart tabs functionality
document.querySelectorAll('.quickstart-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const target = tab.dataset.quickstart;
        
        // Update tabs
        document.querySelectorAll('.quickstart-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Update panels
        document.querySelectorAll('.quickstart-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        document.querySelector(`[data-quickstart-panel="${target}"]`).classList.add('active');
    });
});

// Command category filtering
let currentCategory = 'all';
let currentSearchQuery = '';

document.querySelectorAll('.category-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        currentCategory = btn.dataset.category;
        
        // Update buttons
        document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        filterCommands();
    });
});

// Command search
const commandSearchInput = document.getElementById('command-search');
if (commandSearchInput) {
    commandSearchInput.addEventListener('input', (e) => {
        currentSearchQuery = e.target.value.toLowerCase();
        filterCommands();
    });
}

function filterCommands() {
    document.querySelectorAll('.cli-command').forEach(cmd => {
        const category = cmd.dataset.category || 'all';
        const commandText = cmd.textContent.toLowerCase();
        
        const categoryMatch = currentCategory === 'all' || category === currentCategory;
        const searchMatch = currentSearchQuery === '' || commandText.includes(currentSearchQuery);
        
        if (categoryMatch && searchMatch) {
            cmd.style.display = 'block';
        } else {
            cmd.style.display = 'none';
        }
    });
}

// Copy code functionality
function copyCode(button) {
    const codeBlock = button.previousElementSibling;
    const code = codeBlock.querySelector('code').textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        // Visual feedback
        const originalText = button.querySelector('.copy-text').textContent;
        button.classList.add('copied');
        button.querySelector('.copy-text').textContent = 'Copied!';
        button.querySelector('.copy-icon').textContent = '✓';
        
        setTimeout(() => {
            button.classList.remove('copied');
            button.querySelector('.copy-text').textContent = originalText;
            button.querySelector('.copy-icon').textContent = '📋';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        button.querySelector('.copy-text').textContent = 'Failed';
        setTimeout(() => {
            button.querySelector('.copy-text').textContent = 'Copy';
        }, 2000);
    });
}

// Make copyCode available globally
window.copyCode = copyCode;

// Accordion toggle functionality
function toggleAccordion(button) {
    const accordionItem = button.parentElement;
    const isActive = accordionItem.classList.contains('active');
    
    // Close all accordion items
    document.querySelectorAll('.accordion-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Open clicked item if it wasn't already open
    if (!isActive) {
        accordionItem.classList.add('active');
    }
}

// Make toggleAccordion available globally
window.toggleAccordion = toggleAccordion;

// Start
init();
