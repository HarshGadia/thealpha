import sqlite3
import time
from googlesearch import search

def fill_missing():
    conn = sqlite3.connect('alpha.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, headline, source FROM stories WHERE articleUrl IS NULL OR articleUrl = "" OR articleUrl = "#"')
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} stories needing URLs...")
    
    for row in rows:
        story_id, headline, source = row
        query = f"{headline} {source if source else ''}"
        
        try:
            print(f"Searching Google for: {query.encode('ascii', 'ignore').decode()}")
            # num_results=1
            results = list(search(query, num_results=1, sleep_interval=2))
            if results:
                url = results[0]
                print(f" -> Found: {url}")
                cursor.execute('UPDATE stories SET articleUrl = ? WHERE id = ?', (url, story_id))
                conn.commit()
            else:
                print(" -> No results found.")
        except Exception as e:
            print(f" -> Error: {e}")
            time.sleep(3)
            
    conn.close()
    print("Finished.")

if __name__ == '__main__':
    fill_missing()
