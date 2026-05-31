import urllib.parse
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def get_stories():
    """Extract the STORIES object from data.js securely using Node.js."""
    try:
        # Evaluate data.js and print the STORIES object as JSON
        script = """
        const fs = require('fs');
        const code = fs.readFileSync('data.js', 'utf8');
        eval(code.replace('const STORIES', 'global.STORIES'));
        console.log(JSON.stringify(global.STORIES));
        """
        result = subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True, encoding='utf-8')
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Node JS Parse Error: {e}")
    
    return None


def get_article_url(story):
    article_url = story.get('articleUrl')
    if article_url:
        return article_url
    query = f"{story.get('headline', '')} {story.get('source', '')}"
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)

def generate_email_html(stories):
    today = datetime.now().strftime("%B %d, %Y")
    
    # We will pick the "all-news" category for the newsletter
    feed = stories.get("all-news", []) if stories else []
    
    lead_story = next((s for s in feed if s.get("lead")), None)
    if not lead_story and feed:
        lead_story = feed[0]
        
    other_stories = [s for s in feed if s != lead_story]
    
    # Build HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #fafafa; color: #111827; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 40px; border: 1px solid #e5e7eb; }}
            .header {{ border-bottom: 2px solid #111827; padding-bottom: 20px; margin-bottom: 30px; text-align: center; }}
            .logo {{ font-size: 32px; font-weight: bold; letter-spacing: -1px; margin: 0; }}
            .date {{ font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 2px; margin-top: 10px; }}
            .lead-story {{ border-bottom: 1px solid #e5e7eb; padding-bottom: 30px; margin-bottom: 30px; }}
            .tag {{ font-size: 10px; font-weight: bold; color: #059669; text-transform: uppercase; letter-spacing: 1px; }}
            .lead-headline {{ font-size: 28px; font-weight: bold; font-family: Georgia, serif; margin: 10px 0; color: #111827; text-decoration: none; display: block; }}
            .body-text {{ font-size: 15px; line-height: 1.6; color: #4b5563; margin-bottom: 20px; }}
            .read-more {{ font-size: 12px; font-weight: bold; color: #f97316; text-decoration: none; text-transform: uppercase; }}
            
            .grid-story {{ margin-bottom: 25px; }}
            .grid-headline {{ font-size: 18px; font-weight: bold; font-family: Georgia, serif; margin: 5px 0; color: #111827; text-decoration: none; display: block; }}
            .grid-text {{ font-size: 14px; line-height: 1.5; color: #6b7280; margin-bottom: 10px; }}
            .footer {{ text-align: center; font-size: 10px; color: #9ca3af; margin-top: 40px; border-top: 1px solid #e5e7eb; padding-top: 20px; text-transform: uppercase; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 class="logo">THE ALPHA</h1>
                <div class="date">{today} | DAILY DISPATCH</div>
            </div>
    """
    
    if lead_story:
        html += f"""
            <div class="lead-story">
                <span class="tag">{lead_story.get('tag', 'LATEST')} &bull; {lead_story.get('source', 'NEWS')}</span>
                <a href="{get_article_url(lead_story)}" class="lead-headline">{lead_story.get('headline', 'No Headline')}</a>
                <p class="body-text">{lead_story.get('body', 'No content available.')}</p>
                <a href="{get_article_url(lead_story)}" class="read-more">Read Full Story &rarr;</a>
            </div>
        """
        
    for story in other_stories:
        html += f"""
            <div class="grid-story">
                <span class="tag" style="color: #6b7280;">{story.get('tag', 'LATEST')}</span>
                <a href="{get_article_url(story)}" class="grid-headline">{story.get('headline', 'No Headline')}</a>
                <p class="grid-text">{story.get('body', '')[:150]}...</p>
            </div>
        """
        
    html += """
            <div style="text-align: center; margin: 40px 0;">
                <a href="http://192.168.1.23:3333" style="background-color: #111827; color: #ffffff; padding: 12px 24px; text-decoration: none; font-size: 14px; font-weight: bold; letter-spacing: 1px; display: inline-block;">VIEW FULL DASHBOARD &rarr;</a>
            </div>
            
            <div class="footer">
                &copy; 2026 THE ALPHA INTELLIGENCE GROUP.<br>
                This email was auto-generated by your terminal workflow.
            </div>
        </div>
    </body>
    </html>
    """
    return html

def send_email():
    if not all([SENDER_EMAIL, SENDER_PASSWORD]):
        print("ERROR: Missing credentials in .env file.")
        print("Please ensure SENDER_EMAIL and SENDER_APP_PASSWORD are set.")
        return False
        
    print("Reading news from data.js...")
    stories = get_stories()
    if not stories:
        print("Failed to load stories.")
        return False
    
    print("Generating HTML template...")
    html_content = generate_email_html(stories)
    
    try:
        with open('subscribers.json', 'r') as f:
            subs = json.load(f)
    except Exception:
        subs = []
        
    if RECEIVER_EMAIL and RECEIVER_EMAIL not in subs:
        subs.append(RECEIVER_EMAIL)
        
    if not subs:
        print("No subscribers to send to.")
        return False
    
    print(f"Connecting to SMTP server to send to {len(subs)} subscribers...")
    
    try:
        # Assuming Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        for email in subs:
            print(f"Dispatching to {email}...")
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"The Alpha Daily Briefing - {datetime.now().strftime('%B %d')}"
            msg['From'] = f"The Alpha Terminal <{SENDER_EMAIL}>"
            msg['To'] = email
            
            part = MIMEText(html_content, 'html')
            msg.attach(part)
            
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            
        server.quit()
        print("Email dispatched successfully to all subscribers!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    send_email()
