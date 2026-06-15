import feedparser
from bs4 import BeautifulSoup
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import urllib.request

# ============================================================
# FEED REGISTRY
# Each feed has:
#   url          - RSS/Atom endpoint
#   category     - maps to a dashboard tab
#   source       - display name shown in the UI
#   tag          - badge label shown on each card
#   max_age_hours- 24h for news sites, 72h for newsletters/blogs
#   pre_delay    - seconds to sleep BEFORE fetching (for rate-limited sources)
# ============================================================

FEEDS = [

    # ============================================================
    # INDIA STARTUP & VC  →  vc-inflow
    # ============================================================
    {
        'url': 'https://inc42.com/feed/',
        'category': 'vc-inflow',
        'source': 'Inc42',
        'tag': 'INDIA VC',
        'max_age_hours': 24,
    },
    {
        'url': 'https://yourstory.com/feed',
        'category': 'vc-inflow',
        'source': 'YourStory',
        'tag': 'INDIA',
        'max_age_hours': 24,
    },
    {
        'url': 'https://entrackr.com/feed/',
        'category': 'vc-inflow',
        'source': 'Entrackr',
        'tag': 'INDIA VC',
        'max_age_hours': 24,
    },
    {
        'url': 'https://economictimes.indiatimes.com/tech/startups/rssfeeds/107115.cms',
        'category': 'vc-inflow',
        'source': 'Economic Times',
        'tag': 'STARTUP',
        'max_age_hours': 24,
    },
    {
        'url': 'https://www.vccircle.com/feed',
        'category': 'vc-inflow',
        'source': 'VCCircle',
        'tag': 'INDIA VC',
        'max_age_hours': 24,
    },

    # ============================================================
    # GLOBAL STARTUP & VC  →  vc-inflow
    # ============================================================
    {
        'url': 'https://techcrunch.com/category/startups/feed/',
        'category': 'vc-inflow',
        'source': 'TechCrunch',
        'tag': 'SEED',
        'max_age_hours': 24,
    },
    {
        'url': 'https://techcrunch.com/category/venture/feed/',
        'category': 'vc-inflow',
        'source': 'TechCrunch',
        'tag': 'SERIES A',
        'max_age_hours': 24,
    },
    {
        'url': 'https://news.crunchbase.com/feed/',
        'category': 'vc-inflow',
        'source': 'Crunchbase',
        'tag': 'FUNDING',
        'max_age_hours': 24,
    },
    {
        'url': 'https://sifted.eu/feed',
        'category': 'vc-inflow',
        'source': 'Sifted',
        'tag': 'EUROPE VC',
        'max_age_hours': 24,
    },
    {
        'url': 'https://www.techinasia.com/feed',
        'category': 'vc-inflow',
        'source': 'Tech in Asia',
        'tag': 'ASIA VC',
        'max_age_hours': 24,
    },

    # ============================================================
    # REDDIT COMMUNITY — rate-sensitive, add pre_delay
    # ============================================================
    {
        'url': 'https://www.reddit.com/r/venturecapital/.rss',
        'category': 'vc-inflow',
        'source': 'Reddit r/vc',
        'tag': 'COMMUNITY',
        'max_age_hours': 24,
        'pre_delay': 4,
    },
    {
        'url': 'https://www.reddit.com/r/startups/.rss',
        'category': 'vc-inflow',
        'source': 'Reddit r/startups',
        'tag': 'COMMUNITY',
        'max_age_hours': 24,
        'pre_delay': 4,
    },
    {
        'url': 'https://www.reddit.com/r/privateequity/.rss',
        'category': 'vc-inflow',
        'source': 'Reddit r/PE',
        'tag': 'COMMUNITY',
        'max_age_hours': 24,
        'pre_delay': 4,
    },

    # ============================================================
    # TECH & SEMICONDUCTORS  →  tech-specs
    # ============================================================
    {
        'url': 'https://venturebeat.com/feed/',
        'category': 'tech-specs',
        'source': 'VentureBeat',
        'tag': 'AI TECH',
        'max_age_hours': 24,
    },
    {
        'url': 'https://semianalysis.substack.com/feed',
        'category': 'tech-specs',
        'source': 'SemiAnalysis',
        'tag': 'CHIPS',
        'max_age_hours': 72,
    },
    {
        'url': 'https://asianometry.substack.com/feed',
        'category': 'tech-specs',
        'source': 'Asianometry',
        'tag': 'ASIA TECH',
        'max_age_hours': 72,
    },

    # ============================================================
    # EQUITY MARKETS  →  stocks-arena
    # ============================================================
    {
        'url': 'https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms',
        'category': 'stocks-arena',
        'source': 'Economic Times',
        'tag': 'EQUITY',
        'max_age_hours': 24,
    },
    {
        'url': 'https://www.livemint.com/rss/markets',
        'category': 'stocks-arena',
        'source': 'Mint',
        'tag': 'EQUITY',
        'max_age_hours': 24,
    },
    {
        'url': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
        'category': 'stocks-arena',
        'source': 'Wall Street Journal',
        'tag': 'MARKETS',
        'max_age_hours': 24,
    },

    # ============================================================
    # GENERAL / CORPORATE NEWS  →  all-news
    # ============================================================
    {
        'url': 'https://finance.yahoo.com/news/rssindex',
        'category': 'all-news',
        'source': 'Yahoo Finance',
        'tag': 'MACRO',
        'max_age_hours': 24,
    },
    {
        'url': 'https://www.livemint.com/rss/companies',
        'category': 'all-news',
        'source': 'Mint',
        'tag': 'CORP',
        'max_age_hours': 24,
    },
    {
        'url': 'https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml',
        'category': 'all-news',
        'source': 'Wall Street Journal',
        'tag': 'BUSINESS',
        'max_age_hours': 24,
    },
    {
        'url': 'https://www.ft.com/companies?format=rss',
        'category': 'all-news',
        'source': 'Financial Times',
        'tag': 'GLOBAL',
        'max_age_hours': 24,
    },
    {
        'url': 'https://www.moneycontrol.com/rss/business.xml',
        'category': 'all-news',
        'source': 'Moneycontrol',
        'tag': 'INDIA',
        'max_age_hours': 24,
    },

    # ============================================================
    # GLOBAL MACRO & ECONOMICS  →  global-dial
    # ============================================================
    {
        'url': 'https://feeds.bloomberg.com/economics/news.rss',
        'category': 'global-dial',
        'source': 'Bloomberg',
        'tag': 'MACRO',
        'max_age_hours': 24,
    },
    {
        'url': 'https://noahpinion.substack.com/feed',
        'category': 'global-dial',
        'source': 'Noahpinion',
        'tag': 'ECONOMICS',
        'max_age_hours': 72,
    },
    {
        'url': 'https://sinocism.substack.com/feed',
        'category': 'global-dial',
        'source': 'Sinocism',
        'tag': 'CHINA',
        'max_age_hours': 72,
    },
    {
        'url': 'https://mindslice.substack.com/feed',
        'category': 'global-dial',
        'source': 'Mindslice',
        'tag': 'GLOBAL',
        'max_age_hours': 72,
    },

    # ============================================================
    # DEEP READS / THOUGHT LEADERSHIP  →  deep-reads
    # ============================================================
    {
        'url': 'https://www.notboring.co/feed',
        'category': 'deep-reads',
        'source': 'Not Boring',
        'tag': 'ANALYSIS',
        'max_age_hours': 72,
    },
    {
        'url': 'https://avc.com/feed/',
        'category': 'deep-reads',
        'source': 'AVC',
        'tag': 'VC THESIS',
        'max_age_hours': 72,
    },
    {
        'url': 'https://sajithpai.substack.com/feed',
        'category': 'deep-reads',
        'source': 'Sajith Pai',
        'tag': 'INDIA VC',
        'max_age_hours': 72,
    },
    {
        'url': 'https://tigerfeathers.substack.com/feed',
        'category': 'deep-reads',
        'source': 'Tiger Feathers',
        'tag': 'INDIA',
        'max_age_hours': 72,
    },
    {
        'url': 'https://notes.alexkehayias.com/index.xml',
        'category': 'deep-reads',
        'source': 'Alex Kehayias',
        'tag': 'STARTUP',
        'max_age_hours': 72,
    },
    
    # ============================================================
    # IB DEALS  →  ib-transactions
    # ============================================================
    {
        'url': 'https://techcrunch.com/category/mergers-and-acquisitions/feed/',
        'category': 'ib-transactions',
        'source': 'TechCrunch',
        'tag': 'M&A',
        'max_age_hours': 72,
    },
    {
        'url': 'https://news.google.com/rss/search?q=Mergers+Acquisitions+M%26A+when:7d',
        'category': 'ib-transactions',
        'source': 'Google News',
        'tag': 'DEALS',
        'max_age_hours': 72,
    },

    # ============================================================
    # ENERGY & GRID  →  energy-grid
    # ============================================================
    {
        'url': 'https://www.livemint.com/rss/industry/energy',
        'category': 'energy-grid',
        'source': 'Mint',
        'tag': 'ENERGY',
        'max_age_hours': 72,
    },
    {
        'url': 'https://economictimes.indiatimes.com/industry/energy/rssfeeds/13358371.cms',
        'category': 'energy-grid',
        'source': 'Economic Times',
        'tag': 'POWER',
        'max_age_hours': 72,
    },

    # ============================================================
    # COMMODITIES  →  metal-shine
    # ============================================================
    {
        'url': 'https://economictimes.indiatimes.com/markets/commodities/rssfeeds/11417036.cms',
        'category': 'metal-shine',
        'source': 'Economic Times',
        'tag': 'METALS',
        'max_age_hours': 72,
    },
    {
        'url': 'https://news.google.com/rss/search?q=Commodities+Gold+Oil+Metals+when:7d',
        'category': 'metal-shine',
        'source': 'Google News',
        'tag': 'COMMODITIES',
        'max_age_hours': 72,
    },

    # ============================================================
    # REGULATION  →  regulation-patrol
    # ============================================================
    {
        'url': 'https://www.livemint.com/rss/politics',
        'category': 'regulation-patrol',
        'source': 'Mint',
        'tag': 'POLICY',
        'max_age_hours': 72,
    },
    {
        'url': 'https://news.google.com/rss/search?q=SEC+Regulation+Compliance+FTC+when:7d',
        'category': 'regulation-patrol',
        'source': 'Google News',
        'tag': 'REGULATION',
        'max_age_hours': 72,
    },

    # ============================================================
    # FIXED INCOME  →  fixed-income
    # ============================================================
    {
        'url': 'https://news.google.com/rss/search?q=Fixed+Income+Bonds+Treasury+Yields+when:7d',
        'category': 'fixed-income',
        'source': 'Google News',
        'tag': 'BONDS',
        'max_age_hours': 72,
    },
]

import os
DATA_DIR = os.environ.get('DATA_DIR', '.')
DB_FILE = os.path.join(DATA_DIR, 'alpha.db')

# ============================================================
# USER AGENT — avoids 403/406 on many sites
# ============================================================
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=' ', strip=True)
    return text[:300] + "..." if len(text) > 300 else text


def is_similar(str1, str2):
    if not str1 or not str2:
        return False
    s1 = ''.join(c for c in str1 if c.isalnum()).lower()
    s2 = ''.join(c for c in str2 if c.isalnum()).lower()
    return s1 == s2


def fetch_meta_description(url, headline=""):
    if not url or not url.startswith("http"):
        return ""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        # Only read up to 150KB to make it fast
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read(150000)
            soup = BeautifulSoup(html, 'html.parser')
            meta_desc = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
            desc = ""
            if meta_desc and meta_desc.get('content'):
                desc = meta_desc['content'].strip()
                desc = desc.replace('\u200c', '').replace('\u200b', '')

            # If description is empty or duplicates the headline, extract paragraphs
            if not desc or (headline and is_similar(desc, headline)):
                paragraphs = []
                for p in soup.find_all('p'):
                    text = p.get_text(separator=' ', strip=True)
                    if len(text) < 80:
                        continue
                    lower_text = text.lower()
                    if any(w in lower_text for w in [
                        "subscribe", "privacy policy", "terms of use", "cookie policy", 
                        "all rights reserved", "copyright", "advertisement", "click here",
                        "follow us", "sign up", "download our app", "catch all", "read more"
                    ]):
                        continue
                    paragraphs.append(text)
                    if len(paragraphs) >= 2:
                        break
                if paragraphs:
                    desc = " ".join(paragraphs)

            if desc:
                return desc[:300] + "..." if len(desc) > 300 else desc
    except Exception as e:
        print(f"      -> Meta description fetch failed for {url}: {e}")
    return ""


def parse_entry_date(entry):
    """Return a UTC-aware datetime for a feed entry, or None."""
    dt = None

    # 1. feedparser's pre-parsed struct (most reliable)
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        try:
            dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        except Exception:
            pass

    # 2. Raw RFC-2822 string
    if not dt and hasattr(entry, 'published') and entry.published:
        try:
            dt = parsedate_to_datetime(entry.published)
            dt = dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except Exception:
            pass

    # 3. updated_parsed fallback
    if not dt and hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        try:
            dt = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
        except Exception:
            pass

    return dt


def fetch_and_store():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('PRAGMA journal_mode=WAL;')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        lead BOOLEAN DEFAULT 0,
        tag TEXT,
        tagColor TEXT,
        source TEXT,
        sourceUrl TEXT,
        headline TEXT,
        subline TEXT,
        body TEXT,
        time TEXT,
        articleUrl TEXT,
        dealType TEXT,
        dealStatus TEXT,
        dealValue TEXT,
        acquirer TEXT,
        target TEXT,
        metrics_json TEXT,
        advisors_json TEXT,
        vc_stage TEXT,
        vc_investors TEXT,
        vc_valuation TEXT,
        vc_thesis TEXT,
        vc_comparable TEXT
    )
    ''')
    new_stories_count = 0
    error_count = 0
    now_utc = datetime.now(timezone.utc)

    for feed_info in FEEDS:
        source_name = feed_info['source']
        category = feed_info['category']
        max_age = feed_info.get('max_age_hours', 24)
        cutoff_time = now_utc - timedelta(hours=max_age)

        # Rate-limit delay before fetching (e.g. Reddit)
        delay = feed_info.get('pre_delay', 0)
        if delay:
            time.sleep(delay)

        print(f"  Fetching [{source_name}] ({category}, {max_age}h)...")

        try:
            feed = feedparser.parse(
                feed_info['url'],
                request_headers={'User-Agent': UA}
            )
        except Exception as e:
            print(f"    -> Fetch error: {e}")
            error_count += 1
            continue

        if not feed.entries:
            print(f"    -> No entries returned (feed may be paywalled or empty)")
            continue

        # Process entries oldest-first so auto-incremented IDs flow newest→highest
        for entry in reversed(feed.entries):
            dt = parse_entry_date(entry)

            if not dt:
                dt = now_utc  # fallback: treat as just published

            # Enforce UTC and cap future timestamps
            if not dt.tzinfo:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
            dt = min(dt, now_utc)

            # Skip if older than the per-source window
            if dt < cutoff_time:
                continue

            headline = entry.get('title', '').strip()
            article_url = entry.get('link', '').strip()
            summary_html = entry.get('summary', '') or entry.get('content', [{}])[0].get('value', '')
            body = clean_html(summary_html)

            # Enrich empty, short, or title-matching body descriptions with meta description
            if not body or len(body.strip()) < 30 or is_similar(body, headline):
                meta_desc = fetch_meta_description(article_url, headline)
                if meta_desc:
                    body = meta_desc

            if not headline:
                continue

            # Deduplicate by headline OR URL
            cursor.execute(
                "SELECT id FROM stories WHERE headline = ? OR articleUrl = ?",
                (headline, article_url)
            )
            if cursor.fetchone():
                continue

            cursor.execute('''
                INSERT INTO stories (
                    category, lead, tag, tagColor, source, sourceUrl,
                    headline, subline, body, time, articleUrl
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                feed_info['category'],
                False,
                feed_info['tag'],
                'purple',
                source_name,
                feed_info['url'],
                headline,
                '',
                body,
                dt.isoformat(),
                article_url
            ))
            new_stories_count += 1

        # Commit after each feed to release the SQLite lock
        conn.commit()

    # Clean up old stories (older than 72 hours) to prevent DB bloat
    cursor.execute("DELETE FROM stories WHERE time < datetime('now', '-3 days')")
    conn.commit()

    conn.close()

    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n[{ts}] Aggregation complete — {new_stories_count} new stories added, {error_count} feed errors.\n")


def run_loop():
    total = len(FEEDS)
    print(f"Starting Live Aggregator with {total} feeds...")
    print("News sites: 24h window | Newsletters/blogs: 72h window")
    print("-" * 60)
    while True:
        try:
            fetch_and_store()
        except Exception as e:
            print(f"[CRITICAL] Aggregation loop error: {e}")

        # Sleep 30 minutes before next cycle
        print("Sleeping 30 minutes until next cycle...")
        time.sleep(1800)


if __name__ == '__main__':
    run_loop()
