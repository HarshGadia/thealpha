from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import sqlite3
import urllib.request
from urllib.error import URLError

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
scheduler = BackgroundScheduler(timezone='Asia/Kolkata')
try:
    from live_aggregator import fetch_and_store
    from send_daily_alpha import send_email
    
    # 1. Run the news aggregator immediately, then every 30 minutes
    scheduler.add_job(func=fetch_and_store, trigger="interval", minutes=30, next_run_time=datetime.now())
    
    # 2. Send the daily email every morning at 8:00 AM IST
    scheduler.add_job(func=send_email, trigger="cron", hour=8, minute=0)
    
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
    
    conn = sqlite3.connect(ALPHA_DB)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stories ORDER BY lead DESC, time DESC')
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
    
    stories['all-news'] = dedup_all_news[:45]
    
    # Slice other categories to the latest 30 stories to keep payload small and fast
    for k in stories:
        if k != 'all-news':
            stories[k] = stories[k][:30]
            
    return jsonify(stories)

@app.route('/api/market-data')
def api_market_data():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'No symbol provided'}), 400
    
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
