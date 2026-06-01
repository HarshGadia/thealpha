import sqlite3

def update_data():
    conn = sqlite3.connect('alpha.db')
    cursor = conn.cursor()
    
    # Insert new VC story
    cursor.execute('''
        INSERT INTO stories (
            category, lead, tag, tagColor, source, sourceUrl, headline, subline, body, time,
            vc_stage, vc_investors, vc_valuation, vc_thesis, vc_comparable
        ) VALUES (
            'vc-inflow', 1, 'LATE STAGE', 'purple', 'YourStory', 'https://yourstory.com',
            '💸 Anveshan Raises ₹121 Cr from Vertex & Titan Capital',
            'Anveshan secures ₹121 crore to expand its D2C food and agriculture footprint.',
            'Funding in Indian startups hit a slow week, but Anveshan broke the silence raising ₹121 crore from top tier investors including Vertex Ventures and Titan Capital. The D2C food brand is scaling up aggressive offline expansion.',
            '9:00 AM',
            'Growth', 'Vertex Ventures, Titan Capital, Aman Gupta', 'Undisclosed', 'Premium D2C food brands scaling offline', 'Country Delight'
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Added new story to alpha.db!")

if __name__ == '__main__':
    update_data()
