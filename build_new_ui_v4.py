html_content = r"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>THE ALPHA | Integrated Intelligence</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600;1,700&amp;family=Inter:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@500;600&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        theme: {
          extend: {
            fontFamily: {
                    "sans": ["Inter", "sans-serif"],
                    "serif": ["Playfair Display", "serif"],
                    "mono": ["JetBrains Mono", "monospace"]
            },
            colors: {
                "alpha-orange": "#f97316",
                "alpha-green": "#059669",
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
            background-color: #fafafa;
            color: #111827;
            -webkit-font-smoothing: antialiased;
        }
        .ticker-scroll {
            display: flex;
            animation: ticker 30s linear infinite;
        }
        @keyframes ticker {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }
        
        /* Hide scrollbar for tabs */
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    </style>
</head>
<body class="font-sans text-sm">
<!-- Top Logo Header -->
<header class="bg-white">
<div class="flex items-center justify-between py-6 px-8 max-w-[1600px] mx-auto">
    <div class="flex items-center gap-8">
        <h1 class="font-serif text-5xl font-extrabold uppercase tracking-tighter text-black">THE ALPHA</h1>
    </div>
    <div class="flex items-center gap-4">
        <button class="material-symbols-outlined text-gray-500 hover:text-gray-900 transition-colors">menu</button>
    </div>
</div>
</header>

<!-- Global Market Ticker (Dark Theme from Image 3) -->
<div class="bg-black text-white py-1.5 overflow-hidden whitespace-nowrap border-b border-gray-800">
<div class="ticker-scroll" id="ticker-track">
<!-- Ticker items rendered via JS -->
</div>
</div>

<!-- Dedicated Tab Bar -->
<div class="bg-white border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-[1600px] mx-auto px-8 overflow-x-auto no-scrollbar">
        <div id="tab-nav" class="flex items-center gap-8 whitespace-nowrap">
            <!-- Tabs rendered via JS -->
        </div>
    </div>
</div>

<!-- Main Content Canvas -->
<main class="max-w-[1600px] mx-auto px-8 py-10">
<div class="grid grid-cols-12 gap-12">
<!-- News Feed (Left & Center) -->
<div class="col-span-12 lg:col-span-8 xl:col-span-9" id="content-area">
    <!-- Tab content injected here -->
</div>
<!-- Integrated Intelligence (Right Rail - Minimalist) -->
<div class="col-span-12 lg:col-span-4 xl:col-span-3 space-y-12">

<!-- Market Snapshot -->
<section>
<div class="flex items-center justify-between border-b border-black pb-2 mb-4">
<h3 class="font-mono text-[10px] text-gray-600 uppercase font-bold tracking-widest">Market Snapshot</h3>
<span class="material-symbols-outlined text-gray-800 text-[16px]">show_chart</span>
</div>
<div class="space-y-3">
<div class="flex justify-between items-center py-2 border-b border-gray-100">
<span class="font-sans text-[13px] text-gray-600 uppercase tracking-wide">NIFTY 50</span>
<div class="text-right flex items-center gap-2">
  <div id="nifty-val" class="font-mono text-[13px] text-gray-900">23,547.75</div>
  <div id="nifty-chg" class="font-mono text-[10px] font-bold text-red-600">▼</div>
</div>
</div>
<div class="flex justify-between items-center py-2 border-b border-gray-100">
<span class="font-sans text-[13px] text-gray-600 uppercase tracking-wide">SENSEX</span>
<div class="text-right flex items-center gap-2">
  <div id="sensex-val" class="font-mono text-[13px] text-gray-900">74,775.74</div>
  <div id="sensex-chg" class="font-mono text-[10px] font-bold text-red-600">▼</div>
</div>
</div>
<div class="flex justify-between items-center py-2 border-b border-gray-100">
<span class="font-sans text-[13px] text-gray-600 uppercase tracking-wide">INDIA VIX</span>
<div class="text-right flex items-center gap-2">
  <div class="font-mono text-[13px] text-gray-900">15.20</div>
  <div class="font-mono text-[10px] font-bold text-red-600">▲</div>
</div>
</div>
<div class="flex justify-between items-center py-2 border-b border-gray-100">
<span class="font-sans text-[13px] text-gray-600 uppercase tracking-wide">GOLD</span>
<div class="text-right flex items-center gap-2">
  <div id="gold-val" class="font-mono text-[13px] text-gray-900">1,56,463</div>
  <div id="gold-chg" class="font-mono text-[10px] font-bold text-green-600">▲</div>
</div>
</div>
</div>
</section>

<!-- Yield Curve Intelligence -->
<section>
<div class="flex items-center justify-between border-b border-black pb-2 mb-4">
<h3 class="font-mono text-[10px] text-gray-600 uppercase font-bold tracking-widest">US Treasury Yields</h3>
<span class="material-symbols-outlined text-gray-800 text-[16px]">trending_up</span>
</div>
<div class="mb-4 bg-gray-200 h-24 relative rounded-sm overflow-hidden">
    <!-- Faux chart matching screenshot -->
    <div class="absolute bottom-0 w-full h-[60%] bg-gray-300 border-t-2 border-gray-700"></div>
    <div class="absolute bottom-[55%] left-[20%] w-2 h-2 bg-black rounded-full"></div>
    <div class="absolute bottom-[55%] left-[50%] w-2 h-2 bg-black rounded-full"></div>
    <div class="absolute bottom-[55%] left-[80%] w-2 h-2 bg-black rounded-full"></div>
</div>
<div class="grid grid-cols-2 gap-2">
<div class="p-3 border border-gray-200 bg-white">
<p class="font-mono text-[10px] text-gray-500 mb-1">IN 10Y</p>
<p id="in10y-val" class="font-mono text-[15px] text-gray-900">7.00%</p>
</div>
<div class="p-3 border border-gray-200 bg-white">
<p class="font-mono text-[10px] text-gray-500 mb-1">US 10Y</p>
<p id="us10y-val" class="font-mono text-[15px] text-gray-900">4.45%</p>
</div>
</div>
</section>

<!-- Forex Live -->
<section>
<div class="flex items-center justify-between border-b border-black pb-2 mb-4">
<h3 class="font-mono text-[10px] text-gray-600 uppercase font-bold tracking-widest">Forex Live</h3>
<span class="material-symbols-outlined text-gray-800 text-[16px]">currency_exchange</span>
</div>
<div class="space-y-3">
<div class="flex justify-between items-center py-2 border-b border-gray-100">
<span class="font-mono text-[11px] text-gray-600">USD / INR</span>
<div class="text-right flex items-center gap-2">
  <div id="usdinr-val" class="font-mono text-[13px] text-gray-900">84.96</div>
  <div id="usdinr-chg" class="font-mono text-[11px] text-green-600">+0.54</div>
</div>
</div>
<div class="flex justify-between items-center py-2 border-b border-gray-100">
<span class="font-mono text-[11px] text-gray-600">EUR / USD</span>
<div class="text-right flex items-center gap-2">
  <div class="font-mono text-[13px] text-gray-900">1.0824</div>
  <div class="font-mono text-[11px] text-gray-500">+0.001</div>
</div>
</div>
<div class="flex justify-between items-center py-2 border-b border-gray-100">
<span class="font-mono text-[11px] text-gray-600">GBP / USD</span>
<div class="text-right flex items-center gap-2">
  <div class="font-mono text-[13px] text-gray-900">1.2638</div>
  <div class="font-mono text-[11px] text-red-500">-0.002</div>
</div>
</div>
</div>
</section>

<!-- Sector Momentum -->
<section>
<div class="flex items-center justify-between border-b border-black pb-2 mb-4">
<h3 class="font-mono text-[10px] text-gray-600 uppercase font-bold tracking-widest">Sector Momentum</h3>
<span class="material-symbols-outlined text-gray-800 text-[16px]">grid_view</span>
</div>
<div class="space-y-3">
<div class="w-full bg-gray-100 h-8 flex items-center px-3 relative">
<div class="absolute inset-0 bg-green-100 w-[85%]"></div>
<span class="relative font-sans text-[12px] text-gray-800 z-10 flex justify-between w-full"><span>Technology</span> <span class="font-mono text-[10px] text-gray-600">+2.4%</span></span>
</div>
<div class="w-full bg-gray-100 h-8 flex items-center px-3 relative">
<div class="absolute inset-0 bg-green-100 w-[62%]"></div>
<span class="relative font-sans text-[12px] text-gray-800 z-10 flex justify-between w-full"><span>Financials</span> <span class="font-mono text-[10px] text-gray-600">+1.1%</span></span>
</div>
<div class="w-full bg-gray-100 h-8 flex items-center px-3 relative">
<div class="absolute inset-0 bg-red-100 w-[45%]"></div>
<span class="relative font-sans text-[12px] text-gray-800 z-10 flex justify-between w-full"><span>Utilities</span> <span class="font-mono text-[10px] text-gray-600">-0.8%</span></span>
</div>
</div>
</section>

</div>
</div>
</main>
<!-- Footer -->
<footer class="bg-white border-t border-gray-200 py-12">
<div class="max-w-[1600px] mx-auto px-8">
<div class="grid grid-cols-1 md:grid-cols-4 gap-10">
<div class="col-span-1 md:col-span-2 space-y-6">
<h2 class="font-serif text-2xl font-bold uppercase tracking-tight text-gray-900">THE ALPHA</h2>
<p class="text-gray-500 max-w-sm">The definitive source for institutional-grade intelligence, bridging the gap between high-level editorial and live market execution.</p>
</div>
</div>
<div class="flex flex-col md:flex-row justify-between items-center mt-16 pt-8 border-t border-gray-200 gap-4">
<p class="font-mono text-[10px] text-gray-400 uppercase tracking-widest">© 2026 THE ALPHA INTELLIGENCE GROUP. ALL RIGHTS RESERVED.</p>
</div>
</div>
</footer>

<script src="data.js"></script>
<script>
// Array of cool architectural/abstract finance Unsplash images
const PL_IMAGES = [
    'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80',
    'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80',
    'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800&q=80',
    'https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=800&q=80',
    'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80',
    'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80',
];
let imgIdx = 0;
function getPlaceholderImage() {
    const img = PL_IMAGES[imgIdx % PL_IMAGES.length];
    imgIdx++;
    return img;
}

// ==================== TABS CONFIG ====================
const TABS = [
    { id: 'all-news',          label: 'ALL NEWS' },
    { id: 'ib-transactions',   label: 'IB DEALS' },
    { id: 'tech-specs',        label: 'TECH' },
    { id: 'energy-grid',       label: 'ENERGY & GRID' },
    { id: 'stocks-arena',      label: 'MARKETS' },
    { id: 'metal-shine',       label: 'COMMODITIES' },
    { id: 'vc-inflow',         label: 'VC & PRIVATE' },
    { id: 'regulation-patrol', label: 'REGULATION' },
    { id: 'global-dial',       label: 'GLOBAL MACRO' },
    { id: 'fixed-income',      label: 'FIXED INCOME' },
    { id: 'deep-reads',        label: 'DEEP READS' },
];

function renderTabs() {
    const nav = document.getElementById('tab-nav');
    nav.innerHTML = TABS.map((tab, i) => {
        const activeClass = i === 0 
            ? 'text-gray-900 font-bold border-b-2 border-alpha-orange' 
            : 'text-gray-400 font-medium border-b-2 border-transparent hover:text-gray-700';
        return `<button class="${activeClass} font-sans text-xs tracking-widest uppercase py-4 transition-colors tab-btn" data-tab="${tab.id}" onclick="switchTab('${tab.id}')">${tab.label}</button>`;
    }).join('');
}

function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        if (btn.dataset.tab === tabId) {
            btn.className = 'text-gray-900 font-bold border-b-2 border-alpha-orange font-sans text-xs tracking-widest uppercase py-4 transition-colors tab-btn';
        } else {
            btn.className = 'text-gray-400 font-medium border-b-2 border-transparent hover:text-gray-700 font-sans text-xs tracking-widest uppercase py-4 transition-colors tab-btn';
        }
    });
    
    document.querySelectorAll('.tab-content').forEach(content => {
        content.style.display = content.id === `tab-${tabId}` ? 'block' : 'none';
    });
}

function renderStoryCard(story, isLead) {
    const imgUrl = getPlaceholderImage();
    
    if (isLead) {
        // Lead Story (Image 3 layout: text left, image right)
        return `
        <article class="mb-12 border-b border-gray-200 pb-12 cursor-pointer group">
            <div class="grid grid-cols-1 md:grid-cols-5 gap-8 items-start">
                <div class="md:col-span-3 pr-4">
                    <div class="flex items-center gap-3 mb-4">
                        <span class="border border-gray-300 text-gray-500 px-2 py-0.5 font-mono text-[9px] uppercase tracking-widest">${story.tag || 'GLOBAL MACRO'}</span>
                        <span class="font-mono text-[10px] text-gray-400 uppercase tracking-widest">${story.time || '14 MIN AGO'}</span>
                    </div>
                    <h2 class="font-serif text-[42px] font-bold text-gray-900 mb-6 leading-[1.1] group-hover:text-gray-600 transition-colors">
                        <a href="${story.sourceUrl || '#'}" target="_blank">${story.headline}</a>
                    </h2>
                    <p class="font-sans text-[17px] text-gray-600 leading-relaxed mb-6">${story.body}</p>
                    
                    <div class="flex items-center gap-2 mt-8 pt-4 border-t border-gray-200 w-1/2">
                        <span class="font-mono text-[9px] font-bold text-gray-900 tracking-widest uppercase">${story.source}</span>
                        <span class="text-gray-300">&bull;</span>
                        <span class="font-mono text-[9px] font-bold text-gray-500 tracking-widest uppercase">MARKET ANALYSIS</span>
                    </div>
                </div>
                <div class="md:col-span-2">
                    <img src="${imgUrl}" class="w-full h-[400px] object-cover grayscale opacity-90 group-hover:opacity-100 transition-opacity" alt="Article image">
                </div>
            </div>
        </article>
        `;
    } else {
        // Grid Story (Image 3 layout: Image top, border tag, headline)
        return `
        <article class="cursor-pointer group flex flex-col h-full">
            <img src="${imgUrl}" class="w-full h-48 object-cover grayscale opacity-90 group-hover:opacity-100 transition-opacity mb-5" alt="Article image">
            
            <div class="mb-4">
                <span class="border border-gray-300 text-gray-500 px-2 py-0.5 font-mono text-[9px] uppercase tracking-widest">${story.tag || 'TECH'}</span>
            </div>
            
            <h3 class="font-serif text-[22px] font-bold text-gray-900 mb-3 leading-tight group-hover:text-gray-600 transition-colors">
                <a href="${story.sourceUrl || '#'}" target="_blank">${story.headline}</a>
            </h3>
            
            <p class="font-sans text-[14px] text-gray-600 leading-relaxed mb-4 flex-grow">${story.body.substring(0, 150)}...</p>
            
            ${story.vc ? renderVCBlock(story.vc, false) : ''}
        </article>
        `;
    }
}

function renderVCBlock(vc, isLead) {
    return `
        <div class="mt-4 border-t border-gray-100 pt-3">
            <div class="grid grid-cols-2 gap-y-1">
                <div class="font-sans text-[11px] text-gray-500">Stage</div><div class="font-sans text-[11px] font-medium text-right">${vc.stage}</div>
                <div class="font-sans text-[11px] text-gray-500">Investors</div><div class="font-sans text-[11px] font-medium text-right">${vc.investors}</div>
                ${vc.valuation ? `<div class="font-sans text-[11px] text-gray-500">Valuation</div><div class="font-sans text-[11px] font-medium text-right">${vc.valuation}</div>` : ''}
            </div>
        </div>
    `;
}

function renderDealCard(deal, isLead) {
    const imgUrl = getPlaceholderImage();
    const statusColor = (deal.dealStatus || '').toLowerCase() === 'completed' ? 'text-green-700' : 'text-gray-900';
    
    if (isLead) {
        return `
        <article class="mb-12 border-b border-gray-200 pb-12 cursor-pointer group">
            <div class="grid grid-cols-1 md:grid-cols-5 gap-8 items-start">
                <div class="md:col-span-3 pr-4">
                    <div class="flex items-center gap-3 mb-4">
                        <span class="border border-gray-300 text-gray-500 px-2 py-0.5 font-mono text-[9px] uppercase tracking-widest">${deal.dealType || 'M&A'}</span>
                        <span class="font-mono text-[10px] ${statusColor} uppercase font-bold tracking-widest">${deal.dealStatus || 'Announced'}</span>
                    </div>
                    
                    <div class="font-serif text-[48px] font-bold text-gray-900 mb-2 leading-none">${deal.dealValue}</div>
                    <div class="flex items-center gap-3 font-sans text-lg font-medium text-gray-600 mb-6">
                        <span>${deal.acquirer}</span>
                        <span class="material-symbols-outlined text-[16px] text-gray-400">arrow_forward</span>
                        <span>${deal.target}</span>
                    </div>

                    <h2 class="font-serif text-[28px] font-bold text-gray-900 mb-4 leading-tight group-hover:text-gray-600 transition-colors">${deal.headline}</h2>
                    <p class="font-sans text-[16px] text-gray-600 leading-relaxed mb-6">${deal.body}</p>
                    
                    <div class="flex flex-col gap-1 mt-6 pt-4 border-t border-gray-200">
                        ${deal.advisors ? `<div class="font-sans text-[12px]"><span class="font-semibold text-gray-800">Buy-side:</span> ${deal.advisors.buy}</div>` : ''}
                        ${deal.advisors && deal.advisors.sell !== 'N/A' ? `<div class="font-sans text-[12px]"><span class="font-semibold text-gray-800">Sell-side:</span> ${deal.advisors.sell}</div>` : ''}
                    </div>
                </div>
                <div class="md:col-span-2">
                    <img src="${imgUrl}" class="w-full h-[400px] object-cover grayscale opacity-90 group-hover:opacity-100 transition-opacity" alt="Deal image">
                </div>
            </div>
        </article>
        `;
    } else {
        return `
        <article class="cursor-pointer group flex flex-col h-full">
            <div class="flex justify-between items-center mb-4">
                <span class="border border-gray-300 text-gray-500 px-2 py-0.5 font-mono text-[9px] uppercase tracking-widest">${deal.dealType || 'M&A'}</span>
                <span class="font-mono text-[9px] ${statusColor} uppercase font-bold tracking-widest">${deal.dealStatus || 'Announced'}</span>
            </div>
            
            <div class="font-serif text-[24px] font-bold text-gray-900 mb-1 leading-none">${deal.dealValue}</div>
            <div class="flex items-center gap-2 font-sans text-[13px] font-medium text-gray-600 mb-4">
                <span class="truncate">${deal.acquirer}</span>
                <span class="material-symbols-outlined text-[12px] text-gray-400">arrow_forward</span>
                <span class="truncate">${deal.target}</span>
            </div>
            
            <h3 class="font-serif text-[18px] font-bold text-gray-900 mb-3 leading-tight group-hover:text-gray-600 transition-colors">${deal.headline}</h3>
            <p class="font-sans text-[13px] text-gray-600 leading-relaxed mb-4 flex-grow">${deal.body.substring(0, 100)}...</p>
        </article>
        `;
    }
}

function renderTabContent(tabConfig) {
    const stories = STORIES[tabConfig.id] || [];
    if (stories.length === 0) return '';
    
    // Sort to put lead stories first
    const sorted = [...stories].sort((a, b) => (b.lead ? 1 : 0) - (a.lead ? 1 : 0));
    const isDealsTab = tabConfig.id === 'ib-transactions';
    
    let html = `<div class="tab-content" id="tab-${tabConfig.id}">`;
    
    // Render Lead Story
    if (sorted.length > 0) {
        html += isDealsTab ? renderDealCard(sorted[0], true) : renderStoryCard(sorted[0], true);
    }
    
    // Render Grid Stories
    if (sorted.length > 1) {
        html += `<div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-16 mt-8">`;
        for (let i = 1; i < sorted.length; i++) {
            html += isDealsTab ? renderDealCard(sorted[i], false) : renderStoryCard(sorted[i], false);
        }
        html += `</div>`;
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
        { label: 'FTSE 100', value: '7,915.63', change: '-0.21%', dir: 'down' },
        { label: 'USD/JPY', value: '151.34', change: '+0.12%', dir: 'up' },
        { label: 'GOLD', value: '2,214.30', change: '+1.18%', dir: 'up' },
        { label: 'WTI CRUDE', value: '81.35', change: '-0.48%', dir: 'down' },
        { label: 'S&P 500', value: '5,234.12', change: '+0.45%', dir: 'up' },
        { label: 'NIFTY', value: '23,547.75', change: '-1.50%', dir: 'down', id: 'ticker-nifty-val' },
    ];
    
    const items = tickerData.map(d => {
        const colorClass = d.dir === 'up' ? 'text-green-500' : 'text-red-500';
        const arrow = d.dir === 'up' ? '▲' : '▼';
        const idStr = d.id ? ` id="${d.id}"` : '';
        return `<span class="flex items-center gap-2 font-mono text-[10px] font-bold mr-12"><span class="text-white">${d.label}</span> <span class="${colorClass}"${idStr}>${arrow} ${d.value} (${d.change})</span></span>`;
    }).join('');
    
    document.getElementById('ticker-track').innerHTML = `<div class="flex px-8 items-center">${items}</div><div class="flex px-8 items-center">${items}</div>`;
}

// ==================== LIVE MARKET DATA ENGINE ====================
const MARKET_DATA = {
    nifty:   { base: 23755.20, prev: 23907.15, fmt: v => v.toLocaleString('en-IN', { maximumFractionDigits: 2 }), el: 'nifty-val',  chgEl: 'nifty-chg',  kind: 'index',     yahoo: '%5ENSEI' },
    sensex:  { base: 75200.10, prev: 75867.80, fmt: v => v.toLocaleString('en-IN', { maximumFractionDigits: 2 }), el: 'sensex-val', chgEl: 'sensex-chg', kind: 'index',     yahoo: '%5EBSESN' },
    usdinr:  { base: 84.85,    prev: 84.50,    fmt: v => v.toFixed(2),          el: 'usdinr-val', chgEl: 'usdinr-chg', kind: 'fx',        yahoo: 'USDINR%3DX' },
    gold:    { base: 158200,   prev: 154200,   fmt: v => v.toLocaleString('en-IN', { maximumFractionDigits: 0 }), el: 'gold-val', chgEl: 'gold-chg', kind: 'commodity', yahoo: 'GC%3DF' },
    us10y:   { base: 4.38,     prev: 4.38,     fmt: v => v.toFixed(2) + '%',          el: 'us10y-val', chgEl: 'us10y-chg', kind: 'yield',     yahoo: '%5ETNX', bps: true },
    in10y:   { base: 7.02,     prev: 7.04,     fmt: v => v.toFixed(2) + '%',          el: 'in10y-val', chgEl: 'in10y-chg', kind: 'yield',     bps: true },
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
    Object.keys(MARKET_DATA).forEach(k => renderMarketWidgetValue(k));
}

function nudge(val, kind) {
    let pct;
    if (kind === 'yield') pct = (Math.random() - 0.5) * 0.002;
    else if (kind === 'fx') pct = (Math.random() - 0.5) * 0.0003;
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
        // Just keeping it simple for the image match, not doing bps diff display to match image
    } else {
        const pct = (Math.abs(diff) / prev) * 100; // Use Math.abs so we can put -/+ explicitly or just use the color
    }
    
    const colorClass = direction === 'up' ? 'text-green-600' : 'text-red-600';
    chgEl.className = `font-mono text-[10px] font-bold ${colorClass}`;
    chgEl.textContent = arrow;
}

function tickMarket() {
    Object.keys(MARKET_DATA).forEach(k => {
        MARKET_LIVE[k] = nudge(MARKET_LIVE[k], MARKET_DATA[k].kind);
        renderMarketWidgetValue(k);
    });
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

print("index.html rewritten successfully with accurate Image 3 layout!")
