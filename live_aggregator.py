import feedparser
from bs4 import BeautifulSoup
import sqlite3
import time
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

FEEDS = [
    {
        'url': 'https://techcrunch.com/category/startups/feed/',
        'category': 'STARTUPS',
        'source': 'TechCrunch',
        'tag': 'SEED'
    },
    {
        'url': 'https://techcrunch.com/category/venture/feed/',
        'category': 'VC_FUNDING',
        'source': 'TechCrunch',
        'tag': 'SERIES A'
    },
    {
        'url': 'https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms',
        'category': 'MARKETS',
        'source': 'Economic Times',
        'tag': 'EQUITY'
    },
    {
        'url': 'https://finance.yahoo.com/news/rssindex',
        'category': 'TOP_NEWS',
        'source': 'Yahoo Finance',
        'tag': 'MACRO'
    }
]

DB_FILE = 'alpha.db'
MAX_AGE_HOURS = 24

def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()[:250] + "..." # Truncate to a short snippet

def get_time_ago(dt):
    delta = datetime.now(dt.tzinfo) - dt
    hours = int(delta.total_seconds() / 3600)
    if hours == 0:
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes}M AGO"
    return f"{hours}H AGO"

def fetch_and_store():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cutoff_time = datetime.now() - timedelta(hours=MAX_AGE_HOURS)
    new_stories_count = 0
    
    for feed_info in FEEDS:
        print(f"Fetching {feed_info['source']} ({feed_info['category']})...")
        feed = feedparser.parse(feed_info['url'])
        
        for entry in feed.entries:
            # Parse published date
            if hasattr(entry, 'published'):
                try:
                    dt = parsedate_to_datetime(entry.published)
                except:
                    dt = datetime.now()
            else:
                dt = datetime.now()
                
            # Filter by age
            if dt.replace(tzinfo=None) < cutoff_time:
                continue
                
            headline = entry.get('title', '')
            article_url = entry.get('link', '')
            summary_html = entry.get('summary', '')
            body = clean_html(summary_html)
            
            # Check if exists
            cursor.execute("SELECT id FROM stories WHERE headline = ? OR articleUrl = ?", (headline, article_url))
            if cursor.fetchone():
                continue
                
            time_str = get_time_ago(dt)
            
            # Insert into DB
            cursor.execute('''
                INSERT INTO stories (
                    category, lead, tag, tagColor, source, sourceUrl, 
                    headline, subline, body, time, articleUrl
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                feed_info['category'], 
                False, # Not a lead by default to keep it simple
                feed_info['tag'], 
                'purple', # default tagColor
                feed_info['source'], 
                feed_info['url'], 
                headline, 
                '', # no subline from RSS
                body, 
                time_str, 
                article_url
            ))
            new_stories_count += 1
            
    conn.commit()
    conn.close()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Aggregation complete. Added {new_stories_count} new stories.")

def run_loop():
    print("Starting Live Aggregator...")
    while True:
        try:
            fetch_and_store()
        except Exception as e:
            print(f"Error during aggregation: {e}")
        
        # Sleep for 1 hour
        time.sleep(3600)

if __name__ == '__main__':
    run_loop()
