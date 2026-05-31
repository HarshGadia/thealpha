html_content = r"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>THE ALPHA | Integrated Intelligence</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&amp;family=Inter:wght@400;500;600&amp;family=JetBrains+Mono:wght@500;600&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "surface-tint": "#5d5e62",
                    "surface-container-high": "#ebe7e7",
                    "on-tertiary-fixed-variant": "#005235",
                    "on-secondary-container": "#63635f",
                    "surface-bright": "#fcf8f8",
                    "on-surface": "#1c1b1c",
                    "on-secondary": "#ffffff",
                    "on-primary-fixed-variant": "#45474a",
                    "inverse-on-surface": "#f4f0f0",
                    "on-primary": "#ffffff",
                    "on-background": "#1c1b1c",
                    "on-secondary-fixed-variant": "#474744",
                    "on-tertiary-container": "#42926c",
                    "on-surface-variant": "#45474a",
                    "surface-container-low": "#f6f3f2",
                    "primary-fixed": "#e2e2e6",
                    "tertiary-fixed": "#a2f4c7",
                    "error": "#ba1a1a",
                    "secondary-fixed": "#e4e2dd",
                    "outline": "#76777b",
                    "inverse-surface": "#313030",
                    "on-primary-container": "#838487",
                    "secondary-fixed-dim": "#c8c6c2",
                    "on-error-container": "#93000a",
                    "secondary": "#5e5e5b",
                    "on-tertiary": "#ffffff",
                    "on-error": "#ffffff",
                    "surface-variant": "#e5e2e1",
                    "on-tertiary-fixed": "#002113",
                    "error-container": "#ffdad6",
                    "tertiary": "#000000",
                    "inverse-primary": "#c6c6ca",
                    "surface-container-highest": "#e5e2e1",
                    "primary": "#000000",
                    "surface-container-lowest": "#ffffff",
                    "secondary-container": "#e1dfdb",
                    "outline-variant": "#c6c6ca",
                    "surface-dim": "#ddd9d9",
                    "tertiary-container": "#002113",
                    "primary-fixed-dim": "#c6c6ca",
                    "tertiary-fixed-dim": "#86d7ac",
                    "surface": "#fcf8f8",
                    "on-secondary-fixed": "#1b1c19",
                    "background": "#fcf8f8",
                    "surface-container": "#f1eded",
                    "on-primary-fixed": "#1a1c1f",
                    "primary-container": "#1a1c1f"
            },
            "borderRadius": {
                    "DEFAULT": "0.25rem",
                    "lg": "0.5rem",
                    "xl": "0.75rem",
                    "full": "9999px"
            },
            "spacing": {
                    "max-width": "1440px",
                    "margin-mobile": "16px",
                    "margin-desktop": "64px",
                    "unit": "4px",
                    "gutter": "24px"
            },
            "fontFamily": {
                    "body-md": ["Inter"],
                    "headline-lg": ["Playfair Display"],
                    "body-lg": ["Inter"],
                    "headline-md": ["Playfair Display"],
                    "data-label": ["JetBrains Mono"],
                    "ticker-val": ["JetBrains Mono"],
                    "headline-lg-mobile": ["Playfair Display"],
                    "display-lg": ["Playfair Display"]
            },
            "fontSize": {
                    "body-md": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
                    "headline-lg": ["32px", {"lineHeight": "40px", "fontWeight": "700"}],
                    "body-lg": ["18px", {"lineHeight": "28px", "fontWeight": "400"}],
                    "headline-md": ["24px", {"lineHeight": "30px", "fontWeight": "600"}],
                    "data-label": ["12px", {"lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "500"}],
                    "ticker-val": ["14px", {"lineHeight": "18px", "fontWeight": "600"}],
                    "headline-lg-mobile": ["28px", {"lineHeight": "34px", "fontWeight": "700"}],
                    "display-lg": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700"}]
            }
          },
        },
      }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            display: inline-block;
            vertical-align: middle;
        }
        body {
            background-color: #fcf8f8;
            color: #1c1b1c;
            -webkit-font-smoothing: antialiased;
        }
        .editorial-accent {
            border-left: 1px solid #000000;
        }
        .ticker-scroll {
            display: flex;
            animation: ticker 30s linear infinite;
        }
        @keyframes ticker {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }
        .data-grid-row:nth-child(even) { background-color: #f6f3f2; }
    </style>
</head>
<body class="font-body-md text-body-md">
<!-- TopAppBar -->
<header class="docked full-width top-0 z-50 bg-surface border-b border-outline-variant sticky">
<div class="flex flex-col w-full max-w-max-width mx-auto px-margin-desktop">
<div class="flex items-center justify-between py-6">
<div class="flex items-center gap-8">
<h1 class="font-display-lg text-display-lg uppercase tracking-tight text-primary">THE ALPHA</h1>
<div id="tab-nav" class="hidden md:flex items-center gap-6">
<!-- Tabs rendered via JS -->
</div>
</div>
<div class="flex items-center gap-4">
<button class="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-low p-2 transition-colors">light_mode</button>
<button onclick="location.reload()" class="bg-primary text-on-primary px-6 py-2 font-data-label text-data-label uppercase tracking-widest hover:opacity-80 active:scale-98 transition-all">Refresh Now</button>
</div>
</div>
</div>
</header>
<!-- Global Market Ticker -->
<div class="bg-surface-variant text-on-surface-variant py-2 overflow-hidden whitespace-nowrap border-y border-outline">
<div class="ticker-scroll" id="ticker-track">
<!-- Ticker items rendered via JS -->
</div>
</div>
<!-- Main Content Canvas -->
<main class="max-w-max-width mx-auto px-margin-desktop py-12">
<div class="grid grid-cols-12 gap-gutter">
<!-- News Feed (Left & Center) -->
<div class="col-span-12 lg:col-span-8 space-y-12" id="content-area">
    <!-- Tab content injected here -->
</div>
<!-- Integrated Intelligence (Right Rail Integrated) -->
<div class="col-span-12 lg:col-span-4 space-y-10 lg:pl-gutter lg:border-l lg:border-outline-variant">
<!-- Market Snapshot -->
<section>
<div class="flex items-center justify-between mb-4">
<h3 class="font-data-label text-data-label uppercase font-bold tracking-widest">Market Snapshot</h3>
<span class="material-symbols-outlined text-primary text-[18px]">show_chart</span>
</div>
<div class="space-y-px">
<div class="data-grid-row flex justify-between p-3 border-t border-outline-variant">
<span class="font-body-md">NIFTY 50</span>
<div class="text-right">
  <div id="nifty-val" class="font-ticker-val">23,547.75</div>
  <div id="nifty-chg" class="font-ticker-val text-[11px]">▼ -1.50%</div>
</div>
</div>
<div class="data-grid-row flex justify-between p-3 border-t border-outline-variant">
<span class="font-body-md">SENSEX</span>
<div class="text-right">
  <div id="sensex-val" class="font-ticker-val">74,775.74</div>
  <div id="sensex-chg" class="font-ticker-val text-[11px]">▼ -1.44%</div>
</div>
</div>
<div class="data-grid-row flex justify-between p-3 border-t border-outline-variant">
<span class="font-body-md">GOLD</span>
<div class="text-right">
  <div id="gold-val" class="font-ticker-val">₹1,56,463</div>
  <div id="gold-chg" class="font-ticker-val text-[11px] text-tertiary-fixed-variant">▲ +1.47%</div>
</div>
</div>
</div>
</section>
<!-- Yield Curve Intelligence -->
<section>
<div class="flex items-center justify-between mb-4">
<h3 class="font-data-label text-data-label uppercase font-bold tracking-widest">Yields & Forex</h3>
<span class="material-symbols-outlined text-primary text-[18px]">trending_up</span>
</div>
<div class="grid grid-cols-2 gap-4">
<div class="p-3 bg-surface-container-low border border-outline-variant">
<p class="font-data-label text-[10px] text-on-surface-variant">US 10Y</p>
<p id="us10y-val" class="font-ticker-val text-body-lg font-bold">4.45%</p>
<p id="us10y-chg" class="font-ticker-val text-[11px] text-tertiary-fixed-variant">▲ +7 bps</p>
</div>
<div class="p-3 bg-surface-container-low border border-outline-variant">
<p class="font-data-label text-[10px] text-on-surface-variant">IN 10Y</p>
<p id="in10y-val" class="font-ticker-val text-body-lg font-bold">7.00%</p>
<p id="in10y-chg" class="font-ticker-val text-[11px] text-error">▼ -4 bps</p>
</div>
<div class="p-3 bg-surface-container-low border border-outline-variant">
<p class="font-data-label text-[10px] text-on-surface-variant">USD / INR</p>
<p id="usdinr-val" class="font-ticker-val text-body-lg font-bold">₹84.96</p>
<p id="usdinr-chg" class="font-ticker-val text-[11px] text-tertiary-fixed-variant">▲ +0.54%</p>
</div>
<div class="p-3 bg-surface-container-low border border-outline-variant">
<p class="font-data-label text-[10px] text-on-surface-variant">Spread (IN - US)</p>
<p id="spread-val" class="font-ticker-val text-body-lg font-bold">255 bps</p>
<p id="spread-chg" class="font-ticker-val text-[11px] text-error">▼ -11 bps</p>
</div>
</div>
</section>
</div>
</div>
</main>
<!-- Footer -->
<footer class="bg-surface border-t border-outline-variant mt-20 py-12">
<div class="max-w-max-width mx-auto px-margin-desktop">
<div class="grid grid-cols-1 md:grid-cols-4 gap-10">
<div class="col-span-1 md:col-span-2 space-y-6">
<h2 class="font-display-lg text-[24px] uppercase tracking-tight text-primary">THE ALPHA</h2>
<p class="text-on-surface-variant max-w-sm">The definitive source for institutional-grade intelligence, bridging the gap between high-level editorial and live market execution.</p>
</div>
</div>
<div class="flex flex-col md:flex-row justify-between items-center mt-16 pt-8 border-t border-outline-variant gap-4">
<p class="font-data-label text-[10px] text-on-surface-variant uppercase">© 2026 THE ALPHA INTELLIGENCE GROUP. ALL RIGHTS RESERVED.</p>
</div>
</div>
</footer>

<script src="data.js"></script>
<script>
// ==================== TABS CONFIG ====================
const TABS = [
    { id: 'all-news',          label: 'All News' },
    { id: 'ib-transactions',   label: 'IB Deals' },
    { id: 'tech-specs',        label: 'Tech' },
    { id: 'energy-grid',       label: 'Energy & Grid' },
    { id: 'stocks-arena',      label: 'Markets' },
    { id: 'metal-shine',       label: 'Commodities' },
    { id: 'vc-inflow',         label: 'VC & Private' },
    { id: 'regulation-patrol', label: 'Regulation' },
    { id: 'global-dial',       label: 'Global Macro' },
];

function renderTabs() {
    const nav = document.getElementById('tab-nav');
    nav.innerHTML = TABS.map((tab, i) => {
        const activeClass = i === 0 ? 'text-primary font-bold border-b-2 border-primary pb-1' : 'text-on-surface-variant font-medium hover:text-primary transition-colors';
        return `<button class="${activeClass} font-body-md text-body-md tab-btn" data-tab="${tab.id}" onclick="switchTab('${tab.id}')">${tab.label}</button>`;
    }).join('');
}

function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        if (btn.dataset.tab === tabId) {
            btn.className = 'text-primary font-bold border-b-2 border-primary pb-1 font-body-md text-body-md tab-btn';
        } else {
            btn.className = 'text-on-surface-variant font-medium hover:text-primary transition-colors font-body-md text-body-md tab-btn';
        }
    });
    
    document.querySelectorAll('.tab-content').forEach(content => {
        content.style.display = content.id === `tab-${tabId}` ? 'block' : 'none';
    });
}

function renderLeadStory(story) {
    return `
    <article class="group cursor-pointer mb-12">
        <div class="flex flex-col md:flex-row gap-8 items-start">
            <div class="w-full md:w-3/5 space-y-4 editorial-accent pl-6">
                <div class="flex items-center gap-3">
                    <span class="font-data-label text-data-label border border-primary px-2 py-0.5 uppercase">${story.tag || 'LATEST'}</span>
                    <span class="font-data-label text-data-label text-on-surface-variant">${story.time || '10 MIN AGO'}</span>
                </div>
                <h2 class="font-headline-lg text-headline-lg group-hover:text-primary/70 transition-colors"><a href="${story.sourceUrl || '#'}" target="_blank">${story.headline}</a></h2>
                <p class="font-body-lg text-body-lg text-secondary leading-relaxed">${story.body}</p>
                <div class="flex items-center gap-4 pt-4">
                    <span class="font-data-label text-data-label font-bold uppercase">${story.source}</span>
                </div>
            </div>
        </div>
    </article>
    <hr class="border-outline-variant mb-12"/>
    `;
}

function renderBentoStory(story) {
    return `
    <article class="space-y-4 group">
        <span class="font-data-label text-data-label border border-primary px-2 py-0.5 uppercase">${story.tag || 'NEWS'}</span>
        <h3 class="font-headline-md text-headline-md leading-snug group-hover:underline"><a href="${story.sourceUrl || '#'}" target="_blank">${story.headline}</a></h3>
        <p class="text-on-surface-variant line-clamp-3">${story.body}</p>
        <div class="font-data-label text-[10px] text-on-surface-variant mt-2">${story.source} · ${story.time}</div>
    </article>
    `;
}

function renderDeepDiveStory(story) {
    return `
    <div class="p-4 bg-surface-container-lowest border border-outline-variant hover:border-primary transition-colors cursor-pointer" onclick="window.open('${story.sourceUrl || '#'}', '_blank')">
        <p class="font-data-label text-data-label text-on-tertiary-container mb-2 uppercase">${story.tag || 'INSIGHT'}</p>
        <h5 class="font-headline-md text-[18px] leading-tight mb-4">${story.headline}</h5>
        <span class="text-on-surface-variant text-[12px]">${story.source}</span>
    </div>
    `;
}

function renderTabContent(tabConfig) {
    const stories = STORIES[tabConfig.id] || [];
    if (stories.length === 0) return '';
    
    // Sort to put lead stories first
    const sorted = [...stories].sort((a, b) => (b.lead ? 1 : 0) - (a.lead ? 1 : 0));
    
    let html = `<div class="tab-content" id="tab-${tabConfig.id}">`;
    
    // 1. Lead Story
    if (sorted.length > 0) {
        html += renderLeadStory(sorted[0]);
    }
    
    // 2. Bento Grid
    if (sorted.length > 1) {
        html += `<div class="grid grid-cols-1 md:grid-cols-2 gap-10 mb-12">`;
        const bentoCount = Math.min(sorted.length - 1, 2);
        for(let i=1; i<=bentoCount; i++) {
            html += renderBentoStory(sorted[i]);
        }
        html += `</div>`;
        
        if (sorted.length > 3) html += `<hr class="border-outline-variant mb-12"/>`;
    }
    
    // 3. Deep Dive Grid
    if (sorted.length > 3) {
        html += `
        <div class="space-y-8">
            <div class="flex justify-between items-end border-b border-primary pb-2">
                <h4 class="font-headline-md text-headline-md">More from ${tabConfig.label}</h4>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        `;
        for(let i=3; i<sorted.length; i++) {
            html += renderDeepDiveStory(sorted[i]);
        }
        html += `</div></div>`;
    }
    
    html += `</div>`;
    return html;
}

function renderAllContent() {
    const area = document.getElementById('content-area');
    area.innerHTML = TABS.map(tab => renderTabContent(tab)).join('');
    
    // Hide all except first
    document.querySelectorAll('.tab-content').forEach((content, i) => {
        if (i !== 0) content.style.display = 'none';
    });
}

function renderTicker() {
    const tickerData = [
        { label: 'S&P 500', value: '5,234.12', change: '+0.45%', dir: 'up' },
        { label: 'NASDAQ', value: '16,428.82', change: '+0.82%', dir: 'up' },
        { label: 'NIFTY', value: '23,547.75', change: '-1.50%', dir: 'down', id: 'ticker-nifty-val' },
        { label: 'SENSEX', value: '74,775.74', change: '-1.44%', dir: 'down', id: 'ticker-sensex-val' },
        { label: 'USD/JPY', value: '151.34', change: '+0.12%', dir: 'up' },
        { label: 'GOLD', value: '₹1,56,463', change: '+1.47%', dir: 'up' },
        { label: 'WTI CRUDE', value: '$81.35', change: '-0.48%', dir: 'down' },
        { label: 'BRENT', value: '$91.70', change: '-0.8%', dir: 'down' },
    ];
    
    const items = tickerData.map(d => {
        const colorClass = d.dir === 'up' ? 'text-tertiary-fixed-dim' : 'text-error';
        const arrow = d.dir === 'up' ? '▲' : '▼';
        const idStr = d.id ? ` id="${d.id}"` : '';
        return `<span class="flex items-center gap-2 font-data-label text-data-label mr-12"><span class="font-bold">${d.label}</span> <span class="${colorClass}"${idStr}>${arrow} ${d.value} (${d.change})</span></span>`;
    }).join('');
    
    document.getElementById('ticker-track').innerHTML = `<div class="flex px-4 items-center">${items}</div><div class="flex px-4 items-center">${items}</div>`;
}

// ==================== LIVE MARKET DATA ENGINE ====================
const MARKET_DATA = {
    nifty:   { base: 23755.20, prev: 23907.15, fmt: v => v.toLocaleString('en-IN', { maximumFractionDigits: 2 }), el: 'nifty-val',  chgEl: 'nifty-chg',  kind: 'index',     yahoo: '%5ENSEI' },
    sensex:  { base: 75200.10, prev: 75867.80, fmt: v => v.toLocaleString('en-IN', { maximumFractionDigits: 2 }), el: 'sensex-val', chgEl: 'sensex-chg', kind: 'index',     yahoo: '%5EBSESN' },
    usdinr:  { base: 84.85,    prev: 84.50,    fmt: v => '₹' + v.toFixed(2),          el: 'usdinr-val', chgEl: 'usdinr-chg', kind: 'fx',        yahoo: 'USDINR%3DX' },
    gold:    { base: 158200,   prev: 154200,   fmt: v => '₹' + v.toLocaleString('en-IN', { maximumFractionDigits: 0 }), el: 'gold-val', chgEl: 'gold-chg', kind: 'commodity', yahoo: 'GC%3DF' },
    us10y:   { base: 4.38,     prev: 4.38,     fmt: v => v.toFixed(2) + '%',          el: 'us10y-val', chgEl: 'us10y-chg', kind: 'yield',     yahoo: '%5ETNX', bps: true },
    in10y:   { base: 7.02,     prev: 7.04,     fmt: v => v.toFixed(2) + '%',          el: 'in10y-val', chgEl: 'in10y-chg', kind: 'yield',     bps: true },
    spread:  { base: 255,      prev: 266,      fmt: v => Math.round(v) + ' bps',      el: 'spread-val', chgEl: 'spread-chg', kind: 'spread',   bps: true },
};
const MARKET_LIVE = {};
Object.keys(MARKET_DATA).forEach(k => { MARKET_LIVE[k] = MARKET_DATA[k].base; });

const YF_SYMBOLS = {
    nifty:  '^NSEI',
    sensex: '^BSESN',
    usdinr: 'USDINR=X',
    gold:   'GC=F',
    us10y:  '^TNX',
};

async function fetchYahooQuote(symbol) {
    const url = `https://corsproxy.io/?https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?interval=1m&range=1d`;
    try {
        const res = await fetch(url, { mode: 'cors' });
        if (!res.ok) return null;
        const json = await res.json();
        const meta = json?.chart?.result?.[0]?.meta;
        if (!meta) return null;
        return {
            price: meta.regularMarketPrice ?? meta.previousClose,
            prev:  meta.previousClose,
            open:  meta.regularMarketOpen,
        };
    } catch (e) {
        return null;
    }
}

async function fetchAllLiveMarketData() {
    const fetches = Object.entries(YF_SYMBOLS).map(async ([key, sym]) => {
        const data = await fetchYahooQuote(sym);
        if (data && data.price) {
            MARKET_LIVE[key] = data.price;
            MARKET_DATA[key].prev = data.prev;
        }
    });
    await Promise.all(fetches);

    if (MARKET_LIVE['in10y'] && MARKET_LIVE['us10y']) {
        MARKET_LIVE['spread'] = (MARKET_LIVE['in10y'] - MARKET_LIVE['us10y']) * 100;
    }

    Object.keys(MARKET_DATA).forEach(k => renderMarketWidgetValue(k));
}

function nudge(val, kind) {
    let pct;
    if (kind === 'yield') pct = (Math.random() - 0.5) * 0.002;
    else if (kind === 'fx') pct = (Math.random() - 0.5) * 0.0003;
    else if (kind === 'spread') return val + (Math.random() - 0.5) * 0.5;
    else pct = (Math.random() - 0.5) * 0.0015;
    return val * (1 + pct);
}

function renderMarketWidgetValue(key) {
    const cfg = MARKET_DATA[key];
    const val = MARKET_LIVE[key];
    const prev = cfg.prev || cfg.base;

    const diff = val - prev;
    const direction = diff >= 0 ? 'up' : 'down';
    const arrow = direction === 'up' ? '▲' : '▼';

    const valEl = document.getElementById(cfg.el);
    const chgEl = document.getElementById(cfg.chgEl);
    if (!valEl || !chgEl) return;

    valEl.textContent = cfg.fmt(val);

    if (cfg.bps) {
        const bpsDiff = Math.abs(Math.round(diff * (cfg.kind === 'spread' ? 1 : 100)));
        chgEl.textContent = `${arrow} ${direction === 'up' ? '+' : '−'}${bpsDiff} bps`;
    } else {
        const pct = (diff / prev) * 100;
        chgEl.textContent = `${arrow} ${direction === 'up' ? '+' : ''}${pct.toFixed(2)}%`;
    }
    
    // Tailwind color mapping
    const colorClass = direction === 'up' ? 'text-tertiary-fixed-variant' : 'text-error';
    chgEl.className = `font-ticker-val text-[11px] ${colorClass}`;
}

function updateMarketWidget(key) {
    const cfg = MARKET_DATA[key];
    const oldVal = MARKET_LIVE[key];
    let newVal;
    if (cfg.kind === 'spread') {
        newVal = (MARKET_LIVE['in10y'] - MARKET_LIVE['us10y']) * 100;
    } else {
        newVal = nudge(oldVal, cfg.kind);
    }
    MARKET_LIVE[key] = newVal;

    renderMarketWidgetValue(key);
}

function tickMarket() {
    Object.keys(MARKET_DATA).forEach(k => updateMarketWidget(k));
}

function init() {
    renderTabs();
    renderAllContent();
    renderTicker();
    
    Object.keys(MARKET_DATA).forEach(k => renderMarketWidgetValue(k));
    fetchAllLiveMarketData();
    setInterval(tickMarket, 6000);
    setInterval(fetchAllLiveMarketData, 60000);
}

document.addEventListener('DOMContentLoaded', init);
</script>
</body></html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("index.html rewritten successfully!")
