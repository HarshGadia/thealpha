import sqlite3
import subprocess
import json
import os

DB_FILE = 'alpha.db'

def get_stories():
    """Extract the STORIES object from data.js securely using Node.js."""
    script = """
    const fs = require('fs');
    const code = fs.readFileSync('data.js', 'utf8');
    eval(code.replace('const STORIES', 'global.STORIES'));
    console.log(JSON.stringify(global.STORIES));
    """
    result = subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True, encoding='utf-8')
    return json.loads(result.stdout)

def setup_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE stories (
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
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS edition_stories (
        story_id INTEGER PRIMARY KEY,
        edition TEXT,
        category TEXT
    )
    ''')
    
    stories = get_stories()
    
    for category, category_stories in stories.items():
        for story in category_stories:
            lead = 1 if story.get('lead') else 0
            tag = story.get('tag')
            tagColor = story.get('tagColor')
            source = story.get('source')
            sourceUrl = story.get('sourceUrl')
            headline = story.get('headline')
            subline = story.get('subline')
            body = story.get('body')
            time = story.get('time')
            articleUrl = story.get('articleUrl')
            
            # Deal specific
            dealType = story.get('dealType')
            dealStatus = story.get('dealStatus')
            dealValue = story.get('dealValue')
            acquirer = story.get('acquirer')
            target = story.get('target')
            metrics_json = json.dumps(story.get('metrics')) if story.get('metrics') else None
            advisors_json = json.dumps(story.get('advisors')) if story.get('advisors') else None
            
            # VC specific
            vc = story.get('vc', {})
            vc_stage = vc.get('stage')
            vc_investors = vc.get('investors')
            vc_valuation = vc.get('valuation')
            vc_thesis = vc.get('thesis')
            vc_comparable = vc.get('comparable')
            
            cursor.execute('''
            INSERT INTO stories (
                category, lead, tag, tagColor, source, sourceUrl, headline, subline, body, time, articleUrl,
                dealType, dealStatus, dealValue, acquirer, target, metrics_json, advisors_json,
                vc_stage, vc_investors, vc_valuation, vc_thesis, vc_comparable
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                category, lead, tag, tagColor, source, sourceUrl, headline, subline, body, time, articleUrl,
                dealType, dealStatus, dealValue, acquirer, target, metrics_json, advisors_json,
                vc_stage, vc_investors, vc_valuation, vc_thesis, vc_comparable
            ))
            
    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == '__main__':
    setup_db()
