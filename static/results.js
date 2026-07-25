// ── LOAD RESULTS ───────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  const raw = sessionStorage.getItem('seasonscape_results');
  if (!raw) {
    // No data — redirect home
    window.location.href = '/';
    return;
  }

  const data = JSON.parse(raw);
  animateLoadingSteps(() => renderResults(data));
});

// ── LOADING ANIMATION ──────────────────────────────────────────────────
function animateLoadingSteps(callback) {
  const steps = ['ls1','ls2','ls3','ls4'];
  let i = 0;

  const interval = setInterval(() => {
    if (i > 0) {
      document.getElementById(steps[i-1]).classList.remove('active');
      document.getElementById(steps[i-1]).classList.add('done');
      document.getElementById(steps[i-1]).textContent =
        '✓ ' + document.getElementById(steps[i-1]).textContent.replace('✓ ','');
    }
    if (i < steps.length) {
      document.getElementById(steps[i]).classList.add('active');
      i++;
    } else {
      clearInterval(interval);
      setTimeout(() => {
        document.getElementById('loading-state').style.display = 'none';
        document.getElementById('results-state').style.display  = 'block';
        callback();
      }, 400);
    }
  }, 700);
}

// ── RENDER RESULTS ─────────────────────────────────────────────────────
const placeIcons = { mountain:'🏔️', beach:'🏖️', park:'🌳', indoor:'☕', cafe:'☕', lake:'🏞️' };

const labels = {
  mood: { relax:'Relax', explore:'Explore', social:'Social', focus:'Focus',
          romantic:'Romantic', adventure:'Adventure', family:'Family', solo:'Solo' },
  location_type: { mountain:'Mountain', beach:'Beach', park:'Park/Lake', indoor:'Indoor' },
  temperature:   { cool:'Cool', mild:'Mild', warm:'Warm' },
  crowd:         { low:'Quiet', medium:'Some people', high:'Lively' },
  budget:        { low:'Budget-friendly', medium:'Mid-range', high:'Premium' }
};

function renderResults(data) {
  const { user_prefs, matches, ai_analysis } = data;

  // Heading
  document.getElementById('results-heading').textContent =
    `${user_prefs.name}'s Perfect Matches`;
  document.getElementById('results-sub').textContent =
    `Here are your top ${matches.length} places based on your preferences`;

  // Preference tags
  const tagFields = ['mood','location_type','temperature','crowd','budget'];
  document.getElementById('pref-tags').innerHTML = tagFields
    .map(k => `<div class="pref-tag">${labels[k]?.[user_prefs[k]] || user_prefs[k]}</div>`)
    .join('');

  // Place cards
  const cardsEl = document.getElementById('place-cards');
  cardsEl.innerHTML = matches.map((p, i) => buildPlaceCard(p, i)).join('');

  // Animate match bars
  setTimeout(() => {
    document.querySelectorAll('.match-fill').forEach(bar => {
      bar.style.width = bar.dataset.pct + '%';
    });
  }, 200);

  // AI Analysis
  document.getElementById('ai-body').innerHTML =
    `<p>${ai_analysis}</p>`;

  // Comparison table
  buildCompareTable(matches);
}

function buildPlaceCard(p, idx) {
  const rankLabel = idx === 0 ? '#1 Best Match' : idx === 1 ? '#2' : '#3';
  const icon = placeIcons[p.image_icon] || '📍';
  const pct  = p.match_score;

  const bdHtml = buildBreakdown(p.breakdown);

  return `
  <div class="place-card ${idx === 0 ? 'rank-1' : ''}" style="animation-delay:${idx*0.12}s">
    <div class="place-rank">
      <div class="rank-badge">${rankLabel}</div>
      <div class="place-icon">${icon}</div>
    </div>
    <div class="place-info">
      <div class="place-name">${p.name}</div>
      <div class="place-city">${p.city}</div>
      <p class="place-desc">${p.description}</p>
      <div class="place-meta">
        <span class="meta-tag">🌡️ ${cap(p.temp)}</span>
        <span class="meta-tag">👥 ${cap(p.crowd)} crowd</span>
        <span class="meta-tag">💰 ${cap(p.budget)}</span>
        <span class="meta-tag">📅 ${p.best_time}</span>
        ${p.activities.map(a => `<span class="meta-tag">• ${a}</span>`).join('')}
      </div>
      <div class="match-bar-wrap">
        <div class="match-label">
          <span>Environment match</span>
          <span class="match-pct">${pct}%</span>
        </div>
        <div class="match-bar">
          <div class="match-fill" data-pct="${pct}" style="width:0%"></div>
        </div>
      </div>
      <div class="breakdown-row">${bdHtml}</div>
    </div>
  </div>`;
}  

function buildBreakdown(bd) {
  const fieldNames = {
    location:'Location', temperature:'Temperature',
    crowd:'Crowd', budget:'Budget', mood:'Mood'
  };
  return Object.entries(bd).map(([k, v]) => {
    const hit = v > 0;
    return `<span class="bd-tag ${hit ? '' : 'miss'}">${hit ? '✓' : '✗'} ${fieldNames[k]}</span>`;
  }).join('');
}

function buildCompareTable(matches) {
  const rows = [
    ['City',        m => m.city],
    ['Temperature', m => cap(m.temp)],
    ['Crowd level', m => cap(m.crowd)],
    ['Budget',      m => cap(m.budget)],
    ['Best time',   m => m.best_time],
    ['Activities',  m => m.activities.join(', ')],
    ['Match score', m => m.match_score + '%'],
  ];

  const headerRow = `<tr>
    <th>Criteria</th>
    ${matches.map(m => `<th>${m.name}</th>`).join('')}
  </tr>`;

  const bodyRows = rows.map(([label, fn]) => {
    const cells = matches.map((m, i) => {
      const val = fn(m);
      let cls = '';
      if (label === 'Match score') {
        cls = i === 0 ? 'val-good' : i === 1 ? 'val-ok' : 'val-miss';
      }
      return `<td class="${cls}">${val}</td>`;
    }).join('');
    return `<tr><td>${label}</td>${cells}</tr>`;
  }).join('');

  document.getElementById('compare-table').innerHTML = headerRow + bodyRows;
}

function cap(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}
