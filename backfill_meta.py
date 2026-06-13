import sqlite3
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import os
import sys

# Ensure print supports all unicode characters on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DB_FILE = 'alpha.db'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

def fetch_meta_description(url, headline=""):
    if not url or not url.startswith("http"):
        return ""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
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
        print(f"      Fetch failed: {e}")
    return ""

def is_similar(str1, str2):
    if not str1 or not str2:
        return False
    s1 = ''.join(c for c in str1 if c.isalnum()).lower()
    s2 = ''.join(c for c in str2 if c.isalnum()).lower()
    return s1 == s2

def main():
    if not os.path.exists(DB_FILE):
        print(f"Database {DB_FILE} not found.")
        return

    # 1. Fetch matching story details and close connection immediately
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cutoff_time = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
    cursor.execute("""
        SELECT id, headline, articleUrl, source, time, body 
        FROM stories 
        WHERE time >= ?
        ORDER BY time DESC
    """, (cutoff_time,))
    rows = cursor.fetchall()
    conn.close()

    # Filter candidates in Python using similarity check
    candidates = []
    for row in rows:
        story_id, headline, url, source, t, body_val = row
        body = body_val or ""
        if not body or len(body.strip()) < 30 or is_similar(body, headline):
            candidates.append(row)

    total = len(candidates)
    print(f"Found {total} stories needing a description backfill.\n")

    updated_count = 0
    for idx, (story_id, headline, url, source, t, body_val) in enumerate(candidates):
        print(f"[{idx+1}/{total}] Processing: {headline[:60]} ({source}, {t})")
        print(f"  URL: {url}")
        
        # Slow network request done without holding any DB connection open
        desc = fetch_meta_description(url, headline)
        if desc:
            # Quick database write
            try:
                write_conn = sqlite3.connect(DB_FILE, timeout=30.0)
                write_cursor = write_conn.cursor()
                write_cursor.execute("UPDATE stories SET body = ? WHERE id = ?", (desc, story_id))
                write_conn.commit()
                write_conn.close()
                updated_count += 1
                print(f"  -> SUCCESS: Added {len(desc)} characters of brief summary.")
            except Exception as write_err:
                print(f"  -> SQLite Write Error: {write_err}")
        else:
            print("  -> SKIPPED (no description found)")
        print()

    print(f"Backfill complete! Updated {updated_count} out of {total} stories.")

if __name__ == "__main__":
    main()
