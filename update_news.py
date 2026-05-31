import re
import datetime

def update_data():
    with open('data.js', 'r', encoding='utf-8') as f:
        content = f.read()

    new_vc_story = """
        {
            lead: true,
            tag: 'LATE STAGE',
            tagColor: 'purple',
            source: 'YourStory',
            sourceUrl: 'https://yourstory.com',
            headline: '💸 Anveshan Raises ₹121 Cr from Vertex & Titan Capital',
            subline: 'Anveshan secures ₹121 crore to expand its D2C food and agriculture footprint.',
            body: 'Funding in Indian startups hit a slow week, but Anveshan broke the silence raising ₹121 crore from top tier investors including Vertex Ventures and Titan Capital. The D2C food brand is scaling up aggressive offline expansion.',
            time: '9:00 AM',
            vc: { stage: 'Growth', investors: 'Vertex Ventures, Titan Capital, Aman Gupta', valuation: 'Undisclosed', thesis: 'Premium D2C food brands scaling offline', comparable: 'Country Delight' }
        },"""

    # Inject into vc-inflow just after the bracket
    content = content.replace("'vc-inflow': [", f"'vc-inflow': [{new_vc_story}")
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    update_data()
