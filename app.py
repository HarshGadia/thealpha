from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

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
def serve_index():
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

if __name__ == '__main__':
    # Run on 0.0.0.0 so it can be accessed from the phone on the same Wi-Fi
    app.run(host='0.0.0.0', port=3333, debug=True)
