from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import sqlite3
import urllib.request
from urllib.error import URLError

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

DB_FILE = 'subscribers.json'

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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/api/stories')
def api_stories():
    if not os.path.exists('alpha.db'):
        return jsonify({})
    
    conn = sqlite3.connect('alpha.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stories ORDER BY lead DESC, id ASC')
    rows = cursor.fetchall()
    conn.close()
    
    # Group by category
    stories = {}
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
        
        if cat not in stories:
            stories[cat] = []
        stories[cat].append(row)
        
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

if __name__ == '__main__':
    # Run on 0.0.0.0 so it can be accessed from the phone on the same Wi-Fi
    app.run(host='0.0.0.0', port=3333, debug=True)
