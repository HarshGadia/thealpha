import sqlite3
import urllib.request
import urllib.parse
import re
import time

def fetch_actual_urls():
    conn = sqlite3.connect('alpha.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, headline, source FROM stories WHERE articleUrl IS NULL OR articleUrl = ""')
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} stories to update.")
    
    for row in rows:
        story_id, headline, source = row
        query = f"{headline} {source if source else ''}"
        
        try:
            print(f"Searching: {query.encode('ascii', 'ignore').decode('ascii')}")
        except:
            pass
            
        try:
            data = urllib.parse.urlencode({'q': query}).encode('utf-8')
            req = urllib.request.Request('https://lite.duckduckgo.com/lite/', data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
            
            # Find all urls
            urls = re.findall(r'href="(https?://[^"]+)"', html)
            valid_url = None
            for u in urls:
                if 'duckduckgo.com' not in u and 'w3.org' not in u:
                    valid_url = u
                    break
                    
            if valid_url:
                print(f" -> Found: {valid_url}")
                cursor.execute('UPDATE stories SET articleUrl = ? WHERE id = ?', (valid_url, story_id))
                conn.commit()
            else:
                print(" -> No external URLs found.")
        except Exception as e:
            print(f" -> Error: {e}")
            
        time.sleep(1.5)
            
    conn.close()
    print("Done updating URLs.")

if __name__ == '__main__':
    fetch_actual_urls()
