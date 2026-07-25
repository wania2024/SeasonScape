// ── STATE ──────────────────────────────────────────────────────────────
const state = {
  name: '',
  mood: null,
  location_type: null,
  temperature: null,
  crowd: null,
  budget: null
};

const stepCount = 4;

// ── NAVIGATION ─────────────────────────────────────────────────────────
function nextStep(n) {
  // Validate current step
  if (n === 1 && !document.getElementById('user-name').value.trim()) {
    shakeEl(document.getElementById('user-name'));
    return;
  }
  if (n === 2 && !state.mood) { shakeGrid('mood-grid'); return; }
  if (n === 3 && !state.location_type) { return; }
  if (n === 4 && (!state.temperature || !state.crowd || !state.budget)) {
    return;
  }

  if (n === 4) { buildProfileSummary(); }

  document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
  const target = document.getElementById('step-' + n);
  if (target) { target.classList.add('active'); }
}

function shakeEl(el) {
  el.style.animation = 'none';
  el.style.borderColor = 'rgba(255,100,100,0.6)';
  setTimeout(() => { el.style.borderColor = ''; }, 1200);
}

function shakeGrid(id) {
  const grid = document.getElementById(id);
  grid.style.opacity = '0.5';
  setTimeout(() => { grid.style.opacity = '1'; }, 300);
}

// ── SELECTION ──────────────────────────────────────────────────────────
function select(card, field) {
  const grid = card.closest('.options-grid');
  grid.querySelectorAll('.option-card').forEach(c => c.classList.remove('selected'));
  card.classList.add('selected');
  state[field] = card.dataset.value;

  // Enable next buttons
  if (field === 'mood')          enableNext('next-1');
  if (field === 'location_type') enableNext('next-2');
}

function selectSlider(btn) {
  const field = btn.dataset.field;
  // deselect siblings
  btn.closest('.slider-options').querySelectorAll('.slider-opt').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  state[field] = btn.dataset.value;

  // enable next-3 only when all three are chosen
  if (state.temperature && state.crowd && state.budget) enableNext('next-3');
}

function enableNext(id) {
  const btn = document.getElementById(id);
  if (btn) { btn.disabled = false; }
}

// ── PROFILE SUMMARY ────────────────────────────────────────────────────
const icons = {
  mood: '🎭', location_type: '📍', temperature: '🌡️', crowd: '👥', budget: '💰'
};

const labels = {
  mood: { relax:'Relax', explore:'Explore', social:'Social', focus:'Focus',
          romantic:'Romantic', adventure:'Adventure', family:'Family', solo:'Solo' },
  location_type: { mountain:'Mountain', beach:'Beach', park:'Park / Lake', indoor:'Indoor / Café' },
  temperature: { cool:'Cool', mild:'Mild', warm:'Warm' },
  crowd: { low:'Quiet', medium:'Some people', high:'Lively' },
  budget: { low:'Budget-friendly', medium:'Mid-range', high:'Premium' }
};

function buildProfileSummary() {
  state.name = document.getElementById('user-name').value.trim() || 'Explorer';
  const box = document.getElementById('profile-summary');
  box.innerHTML = Object.entries(state)
    .filter(([k]) => k !== 'name')
    .map(([k, v]) => `
      <div class="profile-tag">
        <span class="tag-icon">${icons[k]}</span>
        <span>${labels[k]?.[v] || v}</span>
      </div>
    `).join('');
}

// ── FIND MATCHES ───────────────────────────────────────────────────────
async function findMatches() {
  // Save state to sessionStorage so results page can use it
  sessionStorage.setItem('seasonscape_prefs', JSON.stringify(state));

  const btnText   = document.getElementById('btn-find-text');
  const btnLoader = document.getElementById('btn-loader');
  btnText.style.display = 'none';
  btnLoader.style.display = 'block';

  try {
    const res = await fetch('/api/match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state)
    });

    const data = await res.json();
    sessionStorage.setItem('seasonscape_results', JSON.stringify(data));
    window.location.href = '/results';
  } catch (err) {
    alert('Something went wrong. Make sure the Flask server is running.');
    btnText.style.display = 'inline';
    btnLoader.style.display = 'none';
  }
}

// ── PARTICLES ─────────────────────────────────────────────────────────
(function spawnParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  for (let i = 0; i < 40; i++) {
    const dot = document.createElement('div');
    const size = Math.random() * 2 + 1;
    dot.style.cssText = `
      position:absolute;
      width:${size}px; height:${size}px;
      background:rgba(200,169,110,${Math.random() * 0.4 + 0.1});
      border-radius:50%;
      left:${Math.random()*100}%;
      top:${Math.random()*100}%;
      animation: twinkle ${3 + Math.random()*5}s ease-in-out infinite alternate;
      animation-delay: ${Math.random()*4}s;
    `;
    container.appendChild(dot);
  }

  const style = document.createElement('style');
  style.textContent = `
    @keyframes twinkle {
      from { opacity: 0.1; transform: scale(1); }
      to   { opacity: 0.8; transform: scale(1.5); }
    }
  `;
  document.head.appendChild(style);
})();
