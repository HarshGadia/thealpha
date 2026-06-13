import sqlite3
import re
import os
from datetime import datetime, timedelta, timezone

DB_FILE = 'alpha.db'

def run_migration():
    if not os.path.exists(DB_FILE):
        print(f"Error: {DB_FILE} not found.")
        return
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check current stories count
    cursor.execute("SELECT count(*) FROM stories")
    total_stories = cursor.fetchone()[0]
    print(f"Total stories in database: {total_stories}")
    
    cursor.execute("SELECT id, time FROM stories")
    rows = cursor.fetchall()
    
    now = datetime.now(timezone.utc)
    updated_count = 0
    
    for story_id, t_str in rows:
        if not t_str:
            continue
            
        # Already in ISO 8601 format (e.g. starts with '202')
        if t_str.startswith('202'):
            continue
            
        new_dt = None
        
        # 1. Check for relative hours ago: "14H AGO", "3H AGO"
        m_hours = re.match(r'^(\d+)\s*H\s+AGO$', t_str.strip(), re.IGNORECASE)
        # 2. Check for relative minutes ago: "16M AGO", "0M AGO"
        m_mins = re.match(r'^(\d+)\s*M\s+AGO$', t_str.strip(), re.IGNORECASE)
        
        if m_hours:
            hours = int(m_hours.group(1))
            new_dt = now - timedelta(hours=hours)
        elif m_mins:
            mins = int(m_mins.group(1))
            new_dt = now - timedelta(minutes=mins)
        else:
            # 3. Check for mock times like "3:45 PM", "11:30 AM"
            try:
                time_part = datetime.strptime(t_str.strip(), "%I:%M %p").time()
                # Default mock stories to June 12, 2026
                new_dt = datetime.combine(datetime(2026, 6, 12), time_part).replace(tzinfo=timezone.utc)
            except Exception as e:
                pass
                
        if new_dt:
            iso_str = new_dt.isoformat()
            cursor.execute("UPDATE stories SET time = ? WHERE id = ?", (iso_str, story_id))
            updated_count += 1
            
    conn.commit()
    conn.close()
    print(f"Migration completed. Updated {updated_count} stories to ISO UTC timestamps.")

if __name__ == '__main__':
    run_migration()
