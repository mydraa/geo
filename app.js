// ==========================================================================
// GeoMaster — Client-side Controller & Localization Engine
// Pro Knowledge Engine for Competitive GeoGuessr
// Visual Edition: Over 2,300+ Verified Photos & Street View Clues
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  // ------------------------------------------------------------------------
  // State Initialization
  // ------------------------------------------------------------------------
  const state = {
    lang: localStorage.getItem('geoguessr_lang') || 'fr',
    theme: localStorage.getItem('geoguessr_theme') || 'dark',
    activeTab: 'tab-countries',
    selectedContinent: 'all',
    selectedDrivingSide: 'all',
    searchQuery: '',
    matrix: {
      driving: 'any',
      plate: 'any',
      car: 'any',
      pole: 'any',
      bollard: 'any'
    },
    quiz: {
      index: 0,
      score: 0,
      streak: 0,
      answered: 0,
      locked: false
    },
    activeModalCountryId: null
  };

  // Set Theme & Language on Root
  document.documentElement.setAttribute('data-theme', state.theme);
  document.documentElement.setAttribute('lang', state.lang);

  // ------------------------------------------------------------------------
  // Helper Translation & Country Accessors
  // ------------------------------------------------------------------------
  function t(key) {
    if (I18N && I18N[state.lang] && I18N[state.lang][key]) {
      return I18N[state.lang][key];
    }
    if (I18N && I18N['en'] && I18N['en'][key]) {
      return I18N['en'][key];
    }
    return key;
  }

  function getCountryName(c) {
    if (!c) return '';
    if (typeof c.name === 'object') {
      return c.name[state.lang] || c.name.en || '';
    }
    return c.name || '';
  }

  function getCountryContinent(c) {
    if (!c) return '';
    if (typeof c.continent === 'object') {
      return c.continent[state.lang] || c.continent.en || '';
    }
    return c.continent || '';
  }

  function getCountryDrivingSide(c) {
    if (!c) return '';
    if (typeof c.drivingSide === 'object') {
      return c.drivingSide[state.lang] || c.drivingSide.en || '';
    }
    return c.drivingSide || '';
  }

  function getCountryGiveaway(c) {
    if (!c) return '';
    if (typeof c.giveaway === 'object') {
      return c.giveaway[state.lang] || c.giveaway.en || '';
    }
    return c.giveaway || '';
  }

  // ------------------------------------------------------------------------
  // Lightbox Modal for Photo Zooming
  // ------------------------------------------------------------------------
  function openLightbox(src, caption) {
    const lightbox = document.getElementById('lightbox-modal');
    const img = document.getElementById('lightbox-img');
    const cap = document.getElementById('lightbox-caption');
    if (!lightbox || !img) return;

    img.src = src;
    if (cap) cap.textContent = caption || '';
    lightbox.classList.add('active');
    lightbox.setAttribute('aria-hidden', 'false');
  }
  // Expose to window for inline onclick handlers
  window.openLightbox = openLightbox;

  // ------------------------------------------------------------------------
  // Application Lifecycle & Event Binding
  // ------------------------------------------------------------------------
  initHeader();
  initNavigation();
  initSearchAndFilters();
  initMatrix();
  initQuiz();
  initModalAndLightbox();

  // Apply Current Language to UI
  applyLanguage(state.lang);

  // ------------------------------------------------------------------------
  // Language Switcher Controller
  // ------------------------------------------------------------------------
  function initHeader() {
    // Language buttons
    const langBtns = document.querySelectorAll('.lang-btn');
    langBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetLang = btn.getAttribute('data-lang');
        if (targetLang === state.lang) return;
        setLanguage(targetLang);
      });
    });

    // Theme button
    const themeBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    if (themeBtn && themeIcon) {
      themeIcon.textContent = state.theme === 'dark' ? '🌙' : '☀️';
      themeBtn.addEventListener('click', () => {
        state.theme = state.theme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', state.theme);
        localStorage.setItem('geoguessr_theme', state.theme);
        themeIcon.textContent = state.theme === 'dark' ? '🌙' : '☀️';
      });
    }
  }

  function setLanguage(lang) {
    state.lang = lang;
    localStorage.setItem('geoguessr_lang', lang);
    document.documentElement.setAttribute('lang', lang);

    // Update active button state
    document.querySelectorAll('.lang-btn').forEach(btn => {
      const isCurrent = btn.getAttribute('data-lang') === lang;
      btn.classList.toggle('active', isCurrent);
      btn.setAttribute('aria-checked', isCurrent ? 'true' : 'false');
    });

    applyLanguage(lang);
  }

  function applyLanguage(lang) {
    // Translate data-i18n elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const translation = t(key);
      if (translation) {
        el.textContent = translation;
      }
    });

    // Translate input placeholders
    document.querySelectorAll('[data-i18n-ph]').forEach(el => {
      const key = el.getAttribute('data-i18n-ph');
      const translation = t(key);
      if (translation) {
        el.setAttribute('placeholder', translation);
      }
    });

    // Update continent pills text
    updateContinentPills();

    // Re-render all views with the new language
    renderCountryCards();
    updateMatrixResults();
    renderBollards();
    renderMeta();
    renderPlates();
    renderHighways();
    renderLanguages();
    renderModes();
    renderFundamentals();
    renderQuizCard();

    // Refresh active modal if open
    if (state.activeModalCountryId) {
      openCountryModal(state.activeModalCountryId);
    }
  }

  function updateContinentPills() {
    const isFr = state.lang === 'fr';
    const pills = document.querySelectorAll('.continent-filters .filter-pill');
    pills.forEach(pill => {
      const cont = pill.getAttribute('data-continent');
      if (cont === 'all') pill.textContent = isFr ? 'Tous (122)' : 'All (122)';
      else if (cont === 'Europe') pill.textContent = isFr ? 'Europe (49)' : 'Europe (49)';
      else if (cont === 'Asia') pill.textContent = isFr ? 'Asie (30)' : 'Asia (30)';
      else if (cont === 'Africa') pill.textContent = isFr ? 'Afrique (15)' : 'Africa (15)';
      else if (cont === 'South America') pill.textContent = isFr ? 'Amér. Sud (11)' : 'South America (11)';
      else if (cont === 'North America') pill.textContent = isFr ? 'Amér. Nord (10)' : 'North America (10)';
      else if (cont === 'Oceania') pill.textContent = isFr ? 'Océanie (7)' : 'Oceania (7)';
    });

    const drivingSelect = document.getElementById('driving-side-select');
    if (drivingSelect) {
      drivingSelect.options[0].textContent = t('filterDrivingAll');
      drivingSelect.options[1].textContent = t('filterDrivingLeft');
      drivingSelect.options[2].textContent = t('filterDrivingRight');
    }
  }

  // ------------------------------------------------------------------------
  // Navigation Tabs Controller
  // ------------------------------------------------------------------------
  function initNavigation() {
    const tabs = document.querySelectorAll('.nav-tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetTab = tab.getAttribute('data-tab');
        if (targetTab === state.activeTab) return;

        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        const targetPanel = document.getElementById(targetTab);
        if (targetPanel) {
          targetPanel.classList.add('active');
        }

        state.activeTab = targetTab;
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    });
  }

  // ------------------------------------------------------------------------
  // Search & Filter Toolbar
  // ------------------------------------------------------------------------
  function initSearchAndFilters() {
    const searchInput = document.getElementById('country-search');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        state.searchQuery = e.target.value.trim().toLowerCase();
        renderCountryCards();
      });

      // Keyboard shortcut: '/' focuses search
      window.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement !== searchInput) {
          e.preventDefault();
          searchInput.focus();
        }
      });
    }

    // Continent Pills
    const continentPills = document.querySelectorAll('.continent-filters .filter-pill');
    continentPills.forEach(pill => {
      pill.addEventListener('click', () => {
        continentPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.selectedContinent = pill.getAttribute('data-continent');
        renderCountryCards();
      });
    });

    // Driving Side Select
    const drivingSelect = document.getElementById('driving-side-select');
    if (drivingSelect) {
      drivingSelect.addEventListener('change', (e) => {
        state.selectedDrivingSide = e.target.value;
        renderCountryCards();
      });
    }
  }

  // ------------------------------------------------------------------------
  // Country Cards Renderer (Photo-Rich Edition)
  // ------------------------------------------------------------------------
  function renderCountryCards() {
    const container = document.getElementById('countries-grid');
    if (!container || !Array.isArray(COUNTRIES_DATA)) return;

    const filtered = COUNTRIES_DATA.filter(c => {
      // Continent filter (checks English name which is standardized)
      const cContinentEn = typeof c.continent === 'object' ? c.continent.en : c.continent;
      if (state.selectedContinent !== 'all' && cContinentEn !== state.selectedContinent) {
        return false;
      }

      // Driving side filter
      if (state.selectedDrivingSide !== 'all') {
        const isLeftMatch = state.selectedDrivingSide === 'Left' ? c.isLeft : !c.isLeft;
        if (!isLeftMatch) return false;
      }

      // Search query across both French & English
      if (state.searchQuery) {
        const q = state.searchQuery;
        const nameFr = (c.name && c.name.fr) ? c.name.fr.toLowerCase() : '';
        const nameEn = (c.name && c.name.en) ? c.name.en.toLowerCase() : '';
        const giveawayFr = (c.giveaway && c.giveaway.fr) ? c.giveaway.fr.toLowerCase() : '';
        const giveawayEn = (c.giveaway && c.giveaway.en) ? c.giveaway.en.toLowerCase() : '';
        const tld = (c.tld || '').toLowerCase();
        const id = (c.id || '').toLowerCase();
        const textMatch = Array.isArray(c.paragraphs) && c.paragraphs.some(p => p.toLowerCase().includes(q));

        if (!nameFr.includes(q) && !nameEn.includes(q) && !giveawayFr.includes(q) && !giveawayEn.includes(q) && !tld.includes(q) && !id.includes(q) && !textMatch) {
          return false;
        }
      }

      return true;
    });

    if (filtered.length === 0) {
      container.innerHTML = `
        <div class="empty-state-box">
          <div class="empty-state-icon">🔍</div>
          <h3 class="empty-state-title">${t('noMatches')}</h3>
          <p class="empty-state-sub">${t('noMatchesSub')}</p>
        </div>
      `;
      return;
    }

    container.innerHTML = filtered.map(c => {
      const name = getCountryName(c);
      const continent = getCountryContinent(c);
      const giveaway = getCountryGiveaway(c);
      const isLeft = !!c.isLeft;
      const drivingText = isLeft ? (state.lang === 'fr' ? '🚗 Gauche' : '🚗 Left') : (state.lang === 'fr' ? '🚙 Droite' : '🚙 Right');
      const drivingClass = isLeft ? 'badge-left-drive' : 'badge-right-drive';

      // Featured photo thumbnail
      const heroImg = (c.images && c.images.length > 0) ? c.images[0].src : null;

      // Summary preview
      const countryParas = c.paragraphs 
        ? (c.paragraphs[state.lang] || (state.lang === 'fr' ? c.paragraphs.fr : c.paragraphs.en) || (Array.isArray(c.paragraphs) ? c.paragraphs : []))
        : [];
      const previewText = (countryParas && countryParas[0])
        ? countryParas[0].slice(0, 140) + '...'
        : (state.lang === 'fr' ? 'Indices complets, panneaux, plaques et méta.' : 'Complete identification clues, signs, plates, and meta.');

      return `
        <article class="country-card" data-cid="${c.id}" tabindex="0" role="button" aria-label="${name}">
          ${heroImg ? `
            <div class="card-thumb-banner">
              <img class="card-thumb-img" src="${heroImg}" alt="${name}" loading="lazy" onerror="this.parentElement.style.display='none'">
              <div class="card-thumb-overlay">
                <span class="badge-pill ${drivingClass}">${drivingText}</span>
                <span class="badge-pill badge-tld-code">${c.tld || ''}</span>
              </div>
            </div>
          ` : ''}

          <div class="card-body-content">
            <div class="card-topbar">
              <div class="card-identity">
                <div class="card-flag-badge">${c.flag || '🏳️'}</div>
                <div>
                  <h3 class="card-country-name">${name}</h3>
                  <span class="card-continent-name">${continent}</span>
                </div>
              </div>
              ${!heroImg ? `
                <div class="card-status-badges">
                  <span class="badge-pill ${drivingClass}">${drivingText}</span>
                  <span class="badge-pill badge-tld-code">${c.tld || ''}</span>
                </div>
              ` : ''}
            </div>

            ${giveaway ? `
              <div class="giveaway-callout">
                <span class="giveaway-tag">${t('giveawayTitle')}</span>
                <div class="giveaway-body">${giveaway}</div>
              </div>
            ` : ''}

            <p class="card-clue-preview">${previewText}</p>

            <div class="card-bottom-bar">
              <div class="card-counters">
                <span class="mini-chip">📸 ${c.images ? c.images.length : 0} ${t('photosCount')}</span>
                <span class="mini-chip">📝 ${c.paragraphs ? c.paragraphs.length : 0} ${t('cluesCount')}</span>
              </div>
              <span class="inspect-action">${t('inspectBtn')}</span>
            </div>
          </div>
        </article>
      `;
    }).join('');

    // Attach click handlers
    container.querySelectorAll('.country-card').forEach(card => {
      card.addEventListener('click', () => {
        const cid = card.getAttribute('data-cid');
        openCountryModal(cid);
      });
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          const cid = card.getAttribute('data-cid');
          openCountryModal(cid);
        }
      });
    });
  }

  // ------------------------------------------------------------------------
  // Interactive Clue Matrix (Tactical Meta Guesser)
  // ------------------------------------------------------------------------
  function initMatrix() {
    setupMatrixGroup('matrix-driving', 'driving');
    setupMatrixGroup('matrix-plate', 'plate');
    setupMatrixGroup('matrix-car', 'car');
    setupMatrixGroup('matrix-pole', 'pole');
    setupMatrixGroup('matrix-bollard', 'bollard');

    const resetBtn = document.getElementById('matrix-reset-action');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        state.matrix = { driving: 'any', plate: 'any', car: 'any', pole: 'any', bollard: 'any' };
        document.querySelectorAll('.matrix-options .matrix-btn').forEach(btn => {
          btn.classList.toggle('selected', btn.getAttribute('data-val') === 'any');
        });
        updateMatrixResults();
      });
    }
  }

  function setupMatrixGroup(groupId, stateProp) {
    const group = document.getElementById(groupId);
    if (!group) return;

    const btns = group.querySelectorAll('.matrix-btn');
    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        btns.forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        state.matrix[stateProp] = btn.getAttribute('data-val');
        updateMatrixResults();
      });
    });
  }

  function updateMatrixResults() {
    const container = document.getElementById('matrix-results-grid');
    const badge = document.getElementById('matrix-candidate-count');
    if (!container || !Array.isArray(COUNTRIES_DATA)) return;

    const filtered = COUNTRIES_DATA.filter(c => {
      // 1. Driving side
      if (state.matrix.driving !== 'any') {
        const isLeftMatch = state.matrix.driving === 'Left' ? c.isLeft : !c.isLeft;
        if (!isLeftMatch) return false;
      }

      // 2. License plate
      if (state.matrix.plate !== 'any') {
        const p = state.matrix.plate;
        if (p === 'yellow_both' && !['the-netherlands', 'luxembourg', 'israel'].includes(c.id)) return false;
        if (p === 'yellow_rear' && !['the-uk', 'gibraltar', 'the-isle-of-man', 'cyprus'].includes(c.id)) return false;
        if (p === 'double_blue' && !['france', 'italy', 'albania'].includes(c.id)) return false;
        if (p === 'short_front' && !['italy', 'san-marino'].includes(c.id)) return false;
        if (p === 'red_plate' && !['belgium', 'kyrgyzstan'].includes(c.id)) return false;
      }

      // 3. Car meta
      if (state.matrix.car !== 'any') {
        const car = state.matrix.car;
        if (car === 'snorkel' && c.id !== 'kenya') return false;
        if (car === 'tape' && c.id !== 'ghana') return false;
        if (car === 'mirrors' && c.id !== 'guatemala') return false;
        if (car === 'camping' && c.id !== 'mongolia') return false;
        if (car === 'rifts' && c.id !== 'senegal') return false;
        if (car === 'escort' && c.id !== 'nigeria') return false;
        if (car === 'bars' && c.id !== 'curacao') return false;
        if (car === 'buggy' && c.id !== 'bermuda') return false;
        if (car === 'kazakh_truck' && c.id !== 'kazakhstan') return false;
        if (car === 'panama_bars' && c.id !== 'panama') return false;
        if (car === 'black_ghost' && !['argentina', 'uruguay'].includes(c.id)) return false;
        if (car === 'chile_rear' && c.id !== 'chile') return false;
        if (car === 'namibia_antenna' && c.id !== 'namibia') return false;
        if (car === 'low_cam' && !['japan', 'switzerland'].includes(c.id)) return false;
      }

      // 4. Utility pole
      if (state.matrix.pole !== 'any') {
        const pol = state.matrix.pole;
        if (pol === 'holes' && !['poland', 'france', 'hungary'].includes(c.id)) return false;
        if (pol === 'ladder' && !['spain', 'portugal', 'brazil'].includes(c.id)) return false;
        if (pol === 'painted' && !['peru', 'chile', 'greece', 'indonesia'].includes(c.id)) return false;
        if (pol === 'stripes' && !['taiwan', 'japan'].includes(c.id)) return false;
      }

      // 5. Bollards
      if (state.matrix.bollard !== 'any') {
        const b = state.matrix.bollard;
        if (b === 'cylinder' && c.id !== 'france') return false;
        if (b === 'slanted_red' && c.id !== 'poland') return false;
        if (b === 'black_cap' && !['germany', 'austria', 'italy', 'spain'].includes(c.id)) return false;
        if (b === 'yellow_post' && c.id !== 'iceland') return false;
      }

      return true;
    });

    if (badge) {
      badge.textContent = state.lang === 'fr' 
        ? `${filtered.length} Pays Candidat${filtered.length > 1 ? 's' : ''}`
        : `${filtered.length} Candidate${filtered.length > 1 ? 's' : ''}`;
    }

    if (filtered.length === 0) {
      container.innerHTML = `
        <div class="empty-state-box">
          <div class="empty-state-icon">🚫</div>
          <h3 class="empty-state-title">${state.lang === 'fr' ? 'Aucune nation compatible' : 'No matching nations found'}</h3>
          <p class="empty-state-sub">${state.lang === 'fr' ? 'Cette combinaison d\'indices est impossible dans Street View. Réinitialisez un filtre.' : 'This clue combination does not exist in Street View coverage. Relax a filter.'}</p>
        </div>
      `;
      return;
    }

    container.innerHTML = filtered.map(c => {
      const name = getCountryName(c);
      const continent = getCountryContinent(c);
      const giveaway = getCountryGiveaway(c);
      const isLeft = !!c.isLeft;
      const drivingText = isLeft ? (state.lang === 'fr' ? '🚗 Gauche' : '🚗 Left') : (state.lang === 'fr' ? '🚙 Droite' : '🚙 Right');
      const drivingClass = isLeft ? 'badge-left-drive' : 'badge-right-drive';
      const heroImg = (c.images && c.images.length > 0) ? c.images[0].src : null;

      return `
        <article class="country-card" data-cid="${c.id}" tabindex="0" role="button">
          ${heroImg ? `
            <div class="card-thumb-banner">
              <img class="card-thumb-img" src="${heroImg}" alt="${name}" loading="lazy" onerror="this.parentElement.style.display='none'">
              <div class="card-thumb-overlay">
                <span class="badge-pill ${drivingClass}">${drivingText}</span>
                <span class="badge-pill badge-tld-code">${c.tld || ''}</span>
              </div>
            </div>
          ` : ''}

          <div class="card-body-content">
            <div class="card-topbar">
              <div class="card-identity">
                <div class="card-flag-badge">${c.flag || '🏳️'}</div>
                <div>
                  <h3 class="card-country-name">${name}</h3>
                  <span class="card-continent-name">${continent}</span>
                </div>
              </div>
            </div>

            ${giveaway ? `
              <div class="giveaway-callout">
                <span class="giveaway-tag">${t('giveawayTitle')}</span>
                <div class="giveaway-body">${giveaway}</div>
              </div>
            ` : ''}

            <div class="card-bottom-bar" style="margin-top:auto;">
              <span class="mini-chip">📸 ${c.images ? c.images.length : 0} ${t('photosCount')}</span>
              <span class="inspect-action">${t('inspectBtn')}</span>
            </div>
          </div>
        </article>
      `;
    }).join('');

    container.querySelectorAll('.country-card').forEach(card => {
      card.addEventListener('click', () => {
        openCountryModal(card.getAttribute('data-cid'));
      });
    });
  }

  // ------------------------------------------------------------------------
  // Photo-Enriched Reference Guides (Bollards, Meta, Plates, Highways, etc.)
  // ------------------------------------------------------------------------
  function renderBollards() {
    const container = document.getElementById('bollards-container');
    if (!container || !BOLLARDS_DATA) return;
    const list = BOLLARDS_DATA[state.lang] || BOLLARDS_DATA.en || [];

    container.innerHTML = list.map(b => `
      <div class="reference-card">
        <div class="reference-card-header">
          <span class="reference-flag">${b.flag}</span>
          <div>
            <h3 class="reference-title">${b.country}</h3>
            <span class="reference-subtitle">${b.shape}</span>
          </div>
        </div>

        ${b.image ? `
          <img class="reference-card-img" src="${b.image}" alt="${b.country} bollard" loading="lazy" onclick="openLightbox('${b.image}', '${b.country} — ${b.shape}')">
        ` : ''}

        <ul class="reference-list">
          <li><strong>${state.lang === 'fr' ? 'Réflecteur :' : 'Reflector:'}</strong> ${b.reflector}</li>
          <li><strong>${state.lang === 'fr' ? 'Indice Clé :' : 'Key Giveaway:'}</strong> ${b.giveaway}</li>
        </ul>
      </div>
    `).join('');
  }

  function renderMeta() {
    const container = document.getElementById('meta-container');
    if (!container || !META_DATA) return;
    const data = META_DATA[state.lang] || META_DATA.en;

    let html = '';

    // Master Maps
    if (data.master_maps && data.master_maps.length > 0) {
      data.master_maps.forEach(m => {
        html += `
          <div class="reference-banner-card">
            <h3 class="reference-title">🗺️ ${m.title}</h3>
            <img class="reference-banner-img" src="${m.image}" alt="${m.title}" loading="lazy" onclick="openLightbox('${m.image}', '${m.title}')">
            <p style="font-size:0.85rem; color:var(--text-muted);">${m.caption}</p>
          </div>
        `;
      });
    }

    // Camera Generations
    html += `
      <div class="reference-card" style="grid-column: 1 / -1;">
        <div class="reference-card-header">
          <span class="reference-flag">📸</span>
          <div>
            <h3 class="reference-title">${state.lang === 'fr' ? 'Générations de Caméras Google Street View' : 'Camera Generations Visual Breakdown'}</h3>
            <span class="reference-subtitle">${state.lang === 'fr' ? 'Évolution de la résolution et de la qualité visuelle de 2007 à aujourd\'hui' : 'Resolution and optical evolution from 2007 to present'}</span>
          </div>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.25rem; margin-top:0.75rem;">
          ${data.camera_generations.map(g => `
            <div style="background:var(--bg-surface-elevated); padding:1rem; border-radius:var(--radius-sm); border:1px solid var(--border-subtle);">
              <strong style="color:var(--accent-blue); font-size:0.95rem;">${g.gen}</strong>
              ${g.image ? `<img class="reference-card-img" src="${g.image}" alt="${g.gen}" loading="lazy" style="height:140px; margin:0.6rem 0;" onclick="openLightbox('${g.image}', '${g.gen}')">` : ''}
              <p style="font-size:0.85rem; color:var(--text-secondary); line-height:1.5;">${g.traits}</p>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    // Car Metas with Photos
    data.car_meta.forEach(c => {
      html += `
        <div class="reference-card">
          <div class="reference-card-header">
            <span class="reference-flag">🚗</span>
            <div>
              <h3 class="reference-title">${c.country}</h3>
              <span class="reference-subtitle">${state.lang === 'fr' ? 'Signature Google Car' : 'Vehicle Meta Signature'}</span>
            </div>
          </div>
          ${c.image ? `
            <img class="reference-card-img" src="${c.image}" alt="${c.country} car meta" loading="lazy" onclick="openLightbox('${c.image}', '${c.country} Google Car Meta')">
          ` : ''}
          <p style="font-size:0.9rem; color:var(--text-secondary); line-height:1.6;">${c.clue}</p>
        </div>
      `;
    });

    container.innerHTML = html;
  }

  function renderPlates() {
    const container = document.getElementById('plates-container');
    if (!container || !PLATES_DATA) return;
    const data = PLATES_DATA[state.lang] || PLATES_DATA.en;

    let html = '';

    // Master Maps
    if (data.master_maps && data.master_maps.length > 0) {
      data.master_maps.forEach(m => {
        html += `
          <div class="reference-banner-card">
            <h3 class="reference-title">🗺️ ${m.title}</h3>
            <img class="reference-banner-img" src="${m.image}" alt="${m.title}" loading="lazy" onclick="openLightbox('${m.image}', '${m.title}')">
            <p style="font-size:0.85rem; color:var(--text-muted);">${m.caption}</p>
          </div>
        `;
      });
    }

    // European Formats
    html += `
      <div class="reference-card" style="grid-column: 1 / -1;">
        <div class="reference-card-header">
          <span class="reference-flag">🇪🇺</span>
          <div>
            <h3 class="reference-title">${state.lang === 'fr' ? 'Formats des Plaques Européennes' : 'European License Plate Formats'}</h3>
            <span class="reference-subtitle">${state.lang === 'fr' ? 'Bandeaux bleus, teintes jaunes et spécificités nationales' : 'Blue strips, yellow hues, and national formats'}</span>
          </div>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.25rem; margin-top:0.75rem;">
          ${data.europe.map(e => `
            <div style="background:var(--bg-surface-elevated); padding:1rem; border-radius:var(--radius-sm); border:1px solid var(--border-subtle);">
              <strong style="color:var(--accent-blue); font-size:0.9rem;">${e.type}</strong>
              ${e.image ? `<img class="reference-card-img" src="${e.image}" alt="${e.type}" loading="lazy" style="height:120px; margin:0.6rem 0;" onclick="openLightbox('${e.image}', '${e.type}')">` : ''}
              <p style="font-size:0.82rem; color:var(--text-secondary); line-height:1.5;">${e.description}</p>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="reference-card" style="grid-column: 1 / -1;">
        <div class="reference-card-header">
          <span class="reference-flag">🇺🇸</span>
          <div>
            <h3 class="reference-title">${data.usa_laws.title}</h3>
            <span class="reference-subtitle">${state.lang === 'fr' ? 'Élimination immédiate d\'un demi-pays en observant l\'avant des véhicules' : 'Instant elimination of half the US by spotting front plates'}</span>
          </div>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.25rem; margin-top:0.75rem;">
          <div style="background:var(--bg-surface-elevated); padding:1rem; border-radius:var(--radius-sm); border:1px solid rgba(245,158,11,0.3);">
            <h4 style="color:var(--accent-amber); margin-bottom:0.5rem; font-size:0.9rem;">🚗 19 ${state.lang === 'fr' ? 'États : ARRIÈRE SEULEMENT' : 'States: REAR ONLY'}</h4>
            <div style="font-size:0.82rem; line-height:1.6; color:var(--text-secondary);">
              ${data.usa_laws.rear_only_states.join(' • ')}
            </div>
          </div>
          <div style="background:var(--bg-surface-elevated); padding:1rem; border-radius:var(--radius-sm); border:1px solid rgba(16,185,129,0.3);">
            <h4 style="color:var(--accent-emerald); margin-bottom:0.5rem; font-size:0.9rem;">🚙 31 ${state.lang === 'fr' ? 'États : AVANT ET ARRIÈRE' : 'States: BOTH FRONT & REAR'}</h4>
            <div style="font-size:0.82rem; line-height:1.6; color:var(--text-secondary);">
              ${data.usa_laws.both_front_rear_states.join(' • ')}
            </div>
          </div>
        </div>
      </div>
    `;

    // Canada
    if (data.canada) {
      html += `
        <div class="reference-card">
          <div class="reference-card-header">
            <span class="reference-flag">🇨🇦</span>
            <h3 class="reference-title">${state.lang === 'fr' ? 'Provinces Canadiennes' : 'Canadian Provinces'}</h3>
          </div>
          <div style="display:flex; flex-direction:column; gap:0.75rem;">
            ${data.canada.map(c => `
              <div style="background:var(--bg-surface-elevated); padding:0.75rem; border-radius:var(--radius-sm); border:1px solid var(--border-subtle);">
                <strong style="color:var(--accent-blue);">${c.province} :</strong>
                ${c.image ? `<img class="reference-card-img" src="${c.image}" alt="${c.province}" loading="lazy" style="height:110px; margin:0.4rem 0;" onclick="openLightbox('${c.image}', '${c.province}')">` : ''}
                <div style="font-size:0.82rem; color:var(--text-secondary);">${c.rule}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    // International
    if (data.international) {
      html += `
        <div class="reference-card">
          <div class="reference-card-header">
            <span class="reference-flag">🌎</span>
            <h3 class="reference-title">${state.lang === 'fr' ? 'Plaques Internationales Signatures' : 'Signature International Plates'}</h3>
          </div>
          <div style="display:flex; flex-direction:column; gap:0.75rem;">
            ${data.international.map(l => `
              <div style="background:var(--bg-surface-elevated); padding:0.75rem; border-radius:var(--radius-sm); border:1px solid var(--border-subtle);">
                <strong style="color:var(--accent-cyan);">${l.region} :</strong>
                ${l.image ? `<img class="reference-card-img" src="${l.image}" alt="${l.region}" loading="lazy" style="height:110px; margin:0.4rem 0;" onclick="openLightbox('${l.image}', '${l.region}')">` : ''}
                <div style="font-size:0.82rem; color:var(--text-secondary);">${l.description}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    container.innerHTML = html;
  }

  function renderHighways() {
    const container = document.getElementById('highways-container');
    if (!container || !HIGHWAYS_DATA) return;
    const list = HIGHWAYS_DATA[state.lang] || HIGHWAYS_DATA.en || [];

    container.innerHTML = list.map(h => `
      <div class="reference-card">
        <div class="reference-card-header">
          <span class="reference-flag">🛣️</span>
          <div>
            <h3 class="reference-title">${h.region}</h3>
            <span class="reference-subtitle">${h.system}</span>
          </div>
        </div>
        ${h.image ? `
          <img class="reference-card-img" src="${h.image}" alt="${h.region}" loading="lazy" onclick="openLightbox('${h.image}', '${h.region} — ${h.system}')">
        ` : ''}
        <ul class="reference-list">
          ${h.rules.map(r => `<li>${r}</li>`).join('')}
        </ul>
      </div>
    `).join('');
  }

  function renderLanguages() {
    const container = document.getElementById('languages-container');
    if (!container || !LANGUAGES_DATA) return;
    const data = LANGUAGES_DATA[state.lang] || LANGUAGES_DATA.en;

    let html = `
      <div class="reference-card" style="grid-column: 1 / -1;">
        <div class="reference-card-header">
          <span class="reference-flag">🔤</span>
          <div>
            <h3 class="reference-title">${state.lang === 'fr' ? 'Matrice d\'Identification des Écritures Cyrilliques' : 'Cyrillic Script Identification Matrix'}</h3>
            <span class="reference-subtitle">${state.lang === 'fr' ? 'Lettres exclusives permettant de distinguer instantanément les nations slaves' : 'Signature letters distinguishing Slavic nations in seconds'}</span>
          </div>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:1rem; margin-top:0.75rem;">
          ${data.cyrillic.map(c => `
            <div style="background:var(--bg-surface-elevated); padding:0.85rem; border-radius:var(--radius-sm); border:1px solid var(--border-subtle);">
              <strong style="color:var(--accent-blue);">${c.language} :</strong>
              <div style="font-size:0.85rem; margin-top:0.25rem; color:var(--text-secondary);">${c.alphabet}</div>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="reference-card">
        <div class="reference-card-header">
          <span class="reference-flag">🌲</span>
          <h3 class="reference-title">${state.lang === 'fr' ? 'Voyelles & Terminaisons Nordiques' : 'Nordic Vowels & Suffixes'}</h3>
        </div>
        <ul class="reference-list">
          ${data.nordic.map(n => `<li><strong>${n.language} :</strong> ${n.characters}</li>`).join('')}
        </ul>
      </div>

      <div class="reference-card">
        <div class="reference-card-header">
          <span class="reference-flag">🏛️</span>
          <h3 class="reference-title">${state.lang === 'fr' ? 'Diacritiques d\'Europe Centrale & de l\'Est' : 'Central & Eastern European Diacritics'}</h3>
        </div>
        <ul class="reference-list">
          ${data.eastern_europe.map(e => `<li><strong>${e.language} :</strong> ${e.features}</li>`).join('')}
        </ul>
      </div>

      <div class="reference-card" style="grid-column: 1 / -1;">
        <div class="reference-card-header">
          <span class="reference-flag">🌏</span>
          <h3 class="reference-title">${state.lang === 'fr' ? 'Comparateur des Écritures d\'Asie' : 'Asian Scripts Comparator'}</h3>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:1rem; margin-top:0.75rem;">
          ${data.asian_scripts.map(a => `
            <div style="background:var(--bg-surface-elevated); padding:0.85rem; border-radius:var(--radius-sm); border:1px solid var(--border-subtle);">
              <strong style="color:var(--accent-cyan);">${a.script} :</strong>
              <div style="font-size:0.85rem; margin-top:0.25rem; color:var(--text-secondary);">${a.appearance}</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  function renderModes() {
    const container = document.getElementById('modes-container');
    if (!container || !MODES_DATA) return;
    const list = MODES_DATA[state.lang] || MODES_DATA.en || [];

    const modeImages = {
      'duels': 'https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/geoguessr1.png',
      'explorer': 'https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/2023-explorer-mode.png',
      'classic': 'https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/2023-classic-maps.png',
      'single': 'https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/single.png'
    };

    container.innerHTML = list.map(m => {
      const img = modeImages[m.id] || null;
      return `
        <div class="reference-card">
          <div class="reference-card-header">
            <span class="reference-flag">🎮</span>
            <div>
              <h3 class="reference-title">${m.title}</h3>
              <span class="reference-subtitle">${m.badge}</span>
            </div>
          </div>
          ${img ? `<img class="reference-card-img" src="${img}" alt="${m.title}" loading="lazy" onclick="openLightbox('${img}', '${m.title}')">` : ''}
          <p style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:0.85rem;">${m.summary}</p>
          <ul class="reference-list">
            ${m.points.map(p => `<li>${p}</li>`).join('')}
          </ul>
        </div>
      `;
    }).join('');
  }

  function renderFundamentals() {
    const container = document.getElementById('fundamentals-container');
    if (!container || !FUNDAMENTALS_DATA) return;
    const data = FUNDAMENTALS_DATA[state.lang] || FUNDAMENTALS_DATA.en;

    let html = '';
    for (const key in data) {
      const section = data[key];
      html += `
        <div class="reference-card">
          <div class="reference-card-header">
            <span class="reference-flag">☀️</span>
            <h3 class="reference-title">${section.title}</h3>
          </div>
          ${section.image ? `
            <img class="reference-card-img" src="${section.image}" alt="${section.title}" loading="lazy" onclick="openLightbox('${section.image}', '${section.title}')">
          ` : ''}
          <ul class="reference-list">
            ${section.points.map(p => `<li>${p}</li>`).join('')}
          </ul>
        </div>
      `;
    }

    container.innerHTML = html;
  }

  // ------------------------------------------------------------------------
  // Gamified Practice Quiz Arena (with Visual Photo Clues)
  // ------------------------------------------------------------------------
  function initQuiz() {
    const nextBtn = document.getElementById('quiz-next-action');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        const questions = (QUIZ_QUESTIONS && QUIZ_QUESTIONS[state.lang]) ? QUIZ_QUESTIONS[state.lang] : [];
        if (state.quiz.index < questions.length - 1) {
          state.quiz.index++;
          state.quiz.locked = false;
          renderQuizCard();
        } else {
          // Restart Quiz
          state.quiz.index = 0;
          state.quiz.score = 0;
          state.quiz.streak = 0;
          state.quiz.answered = 0;
          state.quiz.locked = false;
          renderQuizCard();
        }
      });
    }
  }

  function renderQuizCard() {
    const queryEl = document.getElementById('quiz-query-text');
    const choicesEl = document.getElementById('quiz-choices-box');
    const verdictBox = document.getElementById('quiz-verdict-box');
    const verdictTitle = document.getElementById('quiz-verdict-title');
    const verdictText = document.getElementById('quiz-verdict-text');
    const nextBtn = document.getElementById('quiz-next-action');
    const stepEl = document.getElementById('quiz-step');
    const streakEl = document.getElementById('quiz-streak');
    const scoreEl = document.getElementById('quiz-score');
    const meterFill = document.getElementById('quiz-meter-fill');

    if (!queryEl || !choicesEl || !QUIZ_QUESTIONS) return;

    const questions = QUIZ_QUESTIONS[state.lang] || QUIZ_QUESTIONS.en || [];
    if (questions.length === 0) return;

    const currentQ = questions[state.quiz.index];
    if (!currentQ) return;

    // Update Header Stats
    if (stepEl) stepEl.textContent = `${t('quizQuestionOf')} ${state.quiz.index + 1} ${t('quizOf')} ${questions.length}`;
    if (streakEl) streakEl.textContent = `🔥 ${t('quizStreak')} : ${state.quiz.streak}`;
    if (scoreEl) {
      const pct = state.quiz.answered > 0 ? Math.round((state.quiz.score / state.quiz.answered) * 100) : 0;
      scoreEl.textContent = `${t('quizScore')} : ${state.quiz.score} / ${state.quiz.answered} (${pct}%)`;
    }
    if (meterFill) {
      meterFill.style.width = `${((state.quiz.index + 1) / questions.length) * 100}%`;
    }

    // Hide verdict & next button
    if (verdictBox) verdictBox.style.display = 'none';
    if (nextBtn) nextBtn.style.display = 'none';

    // Inject Question + Photo Clue
    let questionHtml = '';
    if (currentQ.image) {
      questionHtml += `
        <div class="quiz-photo-clue" onclick="openLightbox('${currentQ.image}', 'Indice Visuel / Photo Clue')">
          <img src="${currentQ.image}" alt="Photo Clue" loading="lazy">
        </div>
      `;
    }
    questionHtml += `<div>${currentQ.question}</div>`;
    queryEl.innerHTML = questionHtml;

    // Render Choices
    choicesEl.innerHTML = currentQ.options.map((opt, i) => `
      <button class="choice-btn" data-opt-idx="${i}">
        <span>${opt}</span>
        <span class="choice-marker" style="opacity:0.5; font-family:var(--font-mono); font-size:0.8rem;">[ ${String.fromCharCode(65 + i)} ]</span>
      </button>
    `).join('');

    // Attach listeners
    choicesEl.querySelectorAll('.choice-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        if (state.quiz.locked) return;
        state.quiz.locked = true;
        state.quiz.answered++;

        const selectedIdx = parseInt(btn.getAttribute('data-opt-idx'), 10);
        const isCorrect = selectedIdx === currentQ.answer;

        if (isCorrect) {
          state.quiz.score++;
          state.quiz.streak++;
          btn.classList.add('correct-choice');
        } else {
          state.quiz.streak = 0;
          btn.classList.add('wrong-choice');
          // Highlight correct choice
          const correctBtn = choicesEl.querySelector(`[data-opt-idx="${currentQ.answer}"]`);
          if (correctBtn) correctBtn.classList.add('correct-choice');
        }

        // Show Explanation
        if (verdictBox && verdictTitle && verdictText) {
          verdictTitle.textContent = isCorrect ? t('quizCorrectTitle') : t('quizIncorrectTitle');
          verdictTitle.className = `verdict-headline ${isCorrect ? 'is-correct' : 'is-wrong'}`;
          verdictText.textContent = currentQ.explanation;
          verdictBox.style.display = 'block';
        }

        // Show next button
        if (nextBtn) {
          const isLast = state.quiz.index === questions.length - 1;
          nextBtn.textContent = isLast 
            ? (state.lang === 'fr' ? 'Terminer & Relancer le Quiz ↺' : 'Finish & Restart Quiz ↺')
            : t('quizNextBtn');
          nextBtn.style.display = 'block';
        }

        // Update score chips
        if (streakEl) streakEl.textContent = `🔥 ${t('quizStreak')} : ${state.quiz.streak}`;
        if (scoreEl) {
          const pct = Math.round((state.quiz.score / state.quiz.answered) * 100);
          scoreEl.textContent = `${t('quizScore')} : ${state.quiz.score} / ${state.quiz.answered} (${pct}%)`;
        }
      });
    });
  }

  // ------------------------------------------------------------------------
  // Deep Intelligence Dossier Modal & Lightbox
  // ------------------------------------------------------------------------
  function initModalAndLightbox() {
    const modal = document.getElementById('dossier-modal');
    const closeBtn = document.getElementById('modal-close-btn');

    if (closeBtn) closeBtn.addEventListener('click', closeCountryModal);
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) closeCountryModal();
      });
    }

    // Lightbox
    const lightbox = document.getElementById('lightbox-modal');
    const lightboxClose = document.getElementById('lightbox-close-btn');
    const lightboxBackdrop = document.getElementById('lightbox-backdrop');

    function closeLightbox() {
      if (lightbox) {
        lightbox.classList.remove('active');
        lightbox.setAttribute('aria-hidden', 'true');
      }
    }

    if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
    if (lightboxBackdrop) lightboxBackdrop.addEventListener('click', closeLightbox);

    // Escape key closes modals
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (lightbox && lightbox.classList.contains('active')) {
          closeLightbox();
        } else if (modal && modal.classList.contains('active')) {
          closeCountryModal();
        }
      }
    });
  }

  function openCountryModal(countryId) {
    if (!COUNTRIES_DATA) return;
    const country = COUNTRIES_DATA.find(c => c.id === countryId);
    if (!country) return;

    state.activeModalCountryId = countryId;
    const modal = document.getElementById('dossier-modal');
    if (!modal) return;

    const flagEl = document.getElementById('modal-flag');
    const titleEl = document.getElementById('modal-title');
    const tagsEl = document.getElementById('modal-tags');
    const bodyEl = document.getElementById('modal-body-content');

    const name = getCountryName(country);
    const continent = getCountryContinent(country);
    const giveaway = getCountryGiveaway(country);
    const isLeft = !!country.isLeft;
    const drivingText = isLeft ? (state.lang === 'fr' ? '🚗 Conduite à gauche (RHD)' : '🚗 Drives on Left (RHD)') : (state.lang === 'fr' ? '🚙 Conduite à droite (LHD)' : '🚙 Drives on Right (LHD)');
    const drivingClass = isLeft ? 'badge-left-drive' : 'badge-right-drive';

    if (flagEl) flagEl.textContent = country.flag || '🏳️';
    if (titleEl) titleEl.textContent = name;
    if (tagsEl) {
      tagsEl.innerHTML = `
        <span class="badge-pill ${drivingClass}">${drivingText}</span>
        <span class="badge-pill badge-tld-code">${t('tldLabel')} : ${country.tld || ''}</span>
        <span class="badge-pill" style="background:var(--bg-surface-elevated); color:var(--text-secondary);">${continent}</span>
      `;
    }

    if (bodyEl) {
      let html = '';

      if (giveaway) {
        html += `
          <div class="giveaway-callout" style="padding:1rem 1.25rem;">
            <span class="giveaway-tag" style="font-size:0.75rem;">${t('giveawayTitle')}</span>
            <div class="giveaway-body" style="font-size:0.95rem;">${giveaway}</div>
          </div>
        `;
      }

      html += `<div class="dossier-section-title"><span>📋</span> ${t('modalKeyIndicators')}</div>`;

      const modalParas = country.paragraphs
        ? (country.paragraphs[state.lang] || (state.lang === 'fr' ? country.paragraphs.fr : country.paragraphs.en) || (Array.isArray(country.paragraphs) ? country.paragraphs : []))
        : [];
      if (modalParas && modalParas.length > 0) {
        modalParas.forEach(p => {
          html += `<p class="dossier-text-block">${p}</p>`;
        });
      }

      if (country.images && country.images.length > 0) {
        html += `<div class="dossier-section-title" style="margin-top:1.5rem;"><span>📸</span> ${t('modalGallery')} (${country.images.length})</div>`;
        html += `<div class="dossier-photo-grid">`;
        country.images.forEach(img => {
          html += `
            <div class="photo-cell" data-full-src="${img.src}" data-caption="${img.caption || img.alt || ''}">
              <img src="${img.src}" alt="${img.alt || name}" loading="lazy" onerror="this.parentElement.style.display='none'">
              ${img.caption ? `<div class="photo-caption">${img.caption}</div>` : ''}
            </div>
          `;
        });
        html += `</div>`;
      }

      bodyEl.innerHTML = html;

      // Attach click to zoom on images
      bodyEl.querySelectorAll('.photo-cell').forEach(cell => {
        cell.addEventListener('click', () => {
          const src = cell.getAttribute('data-full-src');
          const caption = cell.getAttribute('data-caption');
          openLightbox(src, caption);
        });
      });
    }

    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeCountryModal() {
    const modal = document.getElementById('dossier-modal');
    if (modal) {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
    }
    state.activeModalCountryId = null;
    document.body.style.overflow = '';
  }

});
