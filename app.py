from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import sqlite3
import urllib.request
from urllib.error import URLError
import feedparser
from bs4 import BeautifulSoup

from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

DATA_DIR = os.environ.get('DATA_DIR', '.')
DB_FILE = os.path.join(DATA_DIR, 'subscribers.json')
ALPHA_DB = os.path.join(DATA_DIR, 'alpha.db')

# --- Start Scheduler ---
# We use Asia/Kolkata timezone so "morning" aligns with India.
if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler = BackgroundScheduler(timezone='Asia/Kolkata')
    try:
        from live_aggregator import (
            fetch_and_store, 
            fetch_and_store_morning, 
            fetch_and_store_evening,
            ensure_edition_stories_populated
        )
        
        # Ensure edition_stories is initialized on startup
        try:
            ensure_edition_stories_populated()
        except Exception as e:
            print(f"Warning: Could not initialize edition_stories: {e}")

        # 1. Run the news aggregator interval job immediately, then every 30 minutes
        scheduler.add_job(func=fetch_and_store, trigger="interval", minutes=30, next_run_time=datetime.now())
        
        # Enable built-in cron scheduling directly in the Flask app (since we run 1 worker process)
        scheduler.add_job(func=fetch_and_store_morning, trigger="cron", hour=7, minute=30)
        scheduler.add_job(func=fetch_and_store_evening, trigger="cron", hour=17, minute=30)
        
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())
    except ImportError as e:
        print(f"Warning: Could not import jobs for scheduler: {e}")
# -----------------------

def load_subscribers():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def save_subscribers(subs):
    with open(DB_FILE, 'w') as f:
        json.dump(subs, f, indent=4)

@app.route('/')
def serve_landing():
    return send_from_directory('.', 'landing.html')

@app.route('/dashboard')
def serve_dashboard():
    return send_from_directory('.', 'index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email')
    
    if not email or '@' not in email:
        return jsonify({'error': 'Invalid email address'}), 400
        
    subs = load_subscribers()
    if email in subs:
        return jsonify({'message': 'Already subscribed!'}), 200
        
    subs.append(email)
    save_subscribers(subs)
    
    return jsonify({'message': 'Successfully subscribed!'}), 201

@app.route('/api/subscriber-count')
def api_subscriber_count():
    subs = load_subscribers()
    return jsonify({'count': len(subs)})

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/api/stories')
def api_stories():
    if not os.path.exists(ALPHA_DB):
        return jsonify({})
    
    # Ensure edition stories are populated
    try:
        from live_aggregator import ensure_edition_stories_populated
        ensure_edition_stories_populated()
    except Exception as e:
        print(f"Error ensuring edition stories populated: {e}")
        
    conn = sqlite3.connect(ALPHA_DB)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    # Determine the current time in IST
    from datetime import timezone as dt_timezone, timedelta as dt_timedelta
    IST = dt_timezone(dt_timedelta(hours=5, minutes=30))
    now_ist = datetime.now(IST)
    
    # If the current time is 6:00 PM (18:00) IST or later, show both morning and evening editions.
    # Otherwise, show only morning.
    if now_ist.hour >= 18:
        cursor.execute('''
            SELECT s.*, e.edition FROM stories s
            JOIN edition_stories e ON s.id = e.story_id
            WHERE e.edition IN ('morning', 'evening')
            ORDER BY s.lead DESC, s.time DESC
        ''')
    else:
        cursor.execute('''
            SELECT s.*, e.edition FROM stories s
            JOIN edition_stories e ON s.id = e.story_id
            WHERE e.edition = 'morning'
            ORDER BY s.lead DESC, s.time DESC
        ''')
        
    rows = cursor.fetchall()
    conn.close()
    
    # Group by category
    stories = {}
    dynamic_all_news = []
    
    for row in rows:
        cat = row.pop('category')
        
        # reconstruct nested objects
        if row.get('metrics_json'):
            row['metrics'] = json.loads(row['metrics_json'])
        if row.get('advisors_json'):
            row['advisors'] = json.loads(row['advisors_json'])
        
        vc_fields = ['vc_stage', 'vc_investors', 'vc_valuation', 'vc_thesis', 'vc_comparable']
        if any(row.get(f) for f in vc_fields):
            row['vc'] = {
                'stage': row.get('vc_stage'),
                'investors': row.get('vc_investors'),
                'valuation': row.get('vc_valuation'),
                'thesis': row.get('vc_thesis'),
                'comparable': row.get('vc_comparable')
            }
            
        # clean up raw db fields
        keys_to_remove = ['metrics_json', 'advisors_json'] + vc_fields
        for k in keys_to_remove:
            if k in row:
                del row[k]
                
        # Boolean cast
        row['lead'] = bool(row.get('lead'))
        
        # Check if the story is from evening update
        row['is_evening_update'] = (row.get('edition') == 'evening')
        if 'edition' in row:
            del row['edition']
            
        # Remove null values to keep payload clean
        row = {k: v for k, v in row.items() if v is not None}
        
        # Copy to dynamically build all-news
        row_copy = dict(row)
        row_copy['category'] = cat
        dynamic_all_news.append(row_copy)
        
        if cat not in stories:
            stories[cat] = []
        stories[cat].append(row)
        
    # Deduplicate and sort all-news dynamically
    seen_headlines = set()
    dedup_all_news = []
    for s in dynamic_all_news:
        hl = s.get('headline')
        if hl not in seen_headlines:
            seen_headlines.add(hl)
            dedup_all_news.append(s)
            
    dedup_all_news.sort(key=lambda x: (x.get('lead', False), x.get('time', '')), reverse=True)
    
    stories['all-news'] = dedup_all_news[:250]
    
    # Slice other categories to a larger limit so news persists for 24 hours
    for k in stories:
        if k != 'all-news':
            stories[k] = stories[k][:100]
            
    return jsonify(stories)

@app.route('/api/market-data')
def api_market_data():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'No symbol provided'}), 400
    
    # Query the SQLite market_rates cache table for any symbol first!
    try:
        conn = sqlite3.connect(ALPHA_DB)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT price, prev, open, updated_at 
            FROM market_rates 
            WHERE symbol = ?
        """, (symbol,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            price, prev, open_val, updated_at = row
            print(f"Serving cached rate for {symbol}: {price} (updated at {updated_at})")
            return jsonify({
                'price': price,
                'prev': prev,
                'open': open_val
            })
    except Exception as e:
        print(f"Error querying market_rates cache for {symbol}: {e}")

    # Try Twelve Data API first if key is configured
    apikey = os.getenv('TWELVE_DATA_API_KEY')
    if apikey and symbol not in ['IN10Y=X', 'REPORATE=X', 'FEDRATE=X']:
        td_symbol = symbol
        if symbol == '^NSEI':
            td_symbol = 'NSEI'
        elif symbol == '^BSESN':
            td_symbol = 'BSESN'
        elif symbol == 'USDINR=X':
            td_symbol = 'USD/INR'
        elif symbol == 'GC=F':
            td_symbol = 'XAU/USD'
        elif symbol == '^TNX':
            td_symbol = 'TNX'
            
        try:
            url = f"https://api.twelvedata.com/quote?symbol={urllib.parse.quote(td_symbol)}&apikey={apikey}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                if 'close' in data and data.get('code') != 404:
                    price = float(data['close'])
                    prev = float(data.get('previous_close') or price)
                    print(f"Serving Twelve Data quote for {symbol} ({td_symbol}): {price}")
                    return jsonify({
                        'price': price,
                        'prev': prev,
                        'open': float(data.get('open') or price)
                    })
        except Exception as e:
            print(f"Twelve Data lookup failed for {symbol}: {e}")

    if symbol == 'USDINR=X':
        try:
            req = urllib.request.Request("https://open.er-api.com/v6/latest/USD", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                rates = data.get('rates', {})
                inr_rate = rates.get('INR')
                if inr_rate:
                    prev_rate = inr_rate
                    try:
                        # Try to get previous close from Yahoo to show the daily percentage change
                        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?interval=1m&range=1d"
                        yf_req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(yf_req, timeout=2) as yf_resp:
                            yf_data = json.loads(yf_resp.read().decode())
                            meta = yf_data.get('chart', {}).get('result', [{}])[0].get('meta', {})
                            if meta.get('previousClose'):
                                prev_rate = meta.get('previousClose')
                    except Exception:
                        pass
                    return jsonify({
                        'price': inr_rate,
                        'prev': prev_rate,
                        'open': prev_rate
                    })
        except Exception as e:
            print(f"Error fetching from Exchange Rate API: {e}")
            # Fall back to Yahoo Finance if Exchange Rate API fails

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?interval=1m&range=1d"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            meta = data.get('chart', {}).get('result', [{}])[0].get('meta', {})
            return jsonify({
                'price': meta.get('regularMarketPrice') or meta.get('previousClose'),
                'prev': meta.get('previousClose'),
                'open': meta.get('regularMarketOpen')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/custom-feed')
def api_custom_feed():
    feed_url = request.args.get('url')
    if not feed_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            return jsonify({'error': 'Could not parse feed or feed is empty'}), 400
            
        source_title = feed.feed.title if 'title' in feed.feed else urllib.parse.urlparse(feed_url).netloc
        
        stories = []
        for entry in feed.entries[:15]:
            # Extract plain text from summary/description
            html_content = entry.get('summary', entry.get('description', ''))
            soup = BeautifulSoup(html_content, 'html.parser')
            body = soup.get_text(separator=' ').strip()
            if len(body) > 300:
                body = body[:297] + '...'
                
            stories.append({
                'id': entry.get('id', entry.get('link')),
                'headline': entry.get('title', 'Untitled'),
                'body': body,
                'articleUrl': entry.get('link', '#'),
                'source': source_title,
                'tag': 'CUSTOM',
                'time': entry.get('published', datetime.now().isoformat())
            })
            
        return jsonify(stories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/morning-briefing', methods=['GET', 'POST'])
def trigger_morning_briefing():
    secret_token = os.environ.get('CRON_SECRET_TOKEN')
    if secret_token:
        token = request.args.get('token') or request.headers.get('X-Cron-Token')
        if token != secret_token:
            return jsonify({'error': 'Unauthorized'}), 401

    sync = request.args.get('sync') == 'true'
    if sync:
        try:
            print("HTTP Synchronously triggering morning fetch and edition refresh...")
            from live_aggregator import fetch_and_store_morning
            recipients = fetch_and_store_morning()
            return jsonify({
                'status': 'success', 
                'message': 'Morning briefing completed successfully',
                'sender_used': os.environ.get('SENDER_EMAIL'),
                'recipients': recipients
            }), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    import threading
    def run_task():
        try:
            print("HTTP Triggered morning fetch and edition refresh...")
            from live_aggregator import fetch_and_store_morning
            fetch_and_store_morning()
        except Exception as e:
            print(f"Error in triggered morning briefing: {e}")

    threading.Thread(target=run_task).start()
    return jsonify({'status': 'success', 'message': 'Morning briefing task triggered in background'}), 200

@app.route('/api/tasks/evening-briefing', methods=['GET', 'POST'])
def trigger_evening_briefing():
    secret_token = os.environ.get('CRON_SECRET_TOKEN')
    if secret_token:
        token = request.args.get('token') or request.headers.get('X-Cron-Token')
        if token != secret_token:
            return jsonify({'error': 'Unauthorized'}), 401

    sync = request.args.get('sync') == 'true'
    if sync:
        try:
            print("HTTP Synchronously triggering evening update and edition add...")
            from live_aggregator import fetch_and_store_evening
            recipients = fetch_and_store_evening()
            return jsonify({
                'status': 'success', 
                'message': 'Evening briefing completed successfully',
                'recipients': recipients
            }), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    import threading
    def run_task():
        try:
            print("HTTP Triggered evening update and edition add...")
            from live_aggregator import fetch_and_store_evening
            fetch_and_store_evening()
        except Exception as e:
            print(f"Error in triggered evening briefing: {e}")

    threading.Thread(target=run_task).start()
    return jsonify({'status': 'success', 'message': 'Evening briefing task triggered in background'}), 200

@app.route('/api/tasks/fetch-news', methods=['GET', 'POST'])
def trigger_fetch_news():
    secret_token = os.environ.get('CRON_SECRET_TOKEN')
    if secret_token:
        token = request.args.get('token') or request.headers.get('X-Cron-Token')
        if token != secret_token:
            return jsonify({'error': 'Unauthorized'}), 401

    import threading
    def run_task():
        try:
            print("HTTP Triggered news aggregation...")
            from live_aggregator import fetch_and_store
            fetch_and_store()
        except Exception as e:
            print(f"Error in triggered news aggregation: {e}")

    threading.Thread(target=run_task).start()
    return jsonify({'status': 'success', 'message': 'News aggregation task triggered in background'}), 200

@app.route('/api/trigger_email')
def trigger_email():
    try:
        from send_daily_alpha import send_email
        success = send_email()
        if success:
            return jsonify({"status": "success", "message": "Email dispatched successfully! Check your inbox."})
        else:
            return jsonify({"status": "error", "message": "Failed to send email. Check if your SENDER_EMAIL and SENDER_APP_PASSWORD variables are set correctly in Railway."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Run on 0.0.0.0 so it can be accessed from the phone on the same Wi-Fi
    app.run(host='0.0.0.0', port=3333, debug=True)
