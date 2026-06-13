import urllib.parse
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import sqlite3
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# ============================================================
# SECTION CONFIG  — controls what appears in the email and order
# ============================================================
SECTIONS = [
    {'key': 'vc-inflow',     'label': 'VC & DEALS',        'accent': '#7c3aed', 'count': 3},
    {'key': 'tech-specs',    'label': 'TECH & AI',          'accent': '#2563eb', 'count': 2},
    {'key': 'stocks-arena',  'label': 'MARKETS',            'accent': '#dc2626', 'count': 2},
    {'key': 'global-dial',   'label': 'GLOBAL MACRO',       'accent': '#d97706', 'count': 2},
    {'key': 'deep-reads',    'label': 'DEEP READ OF THE DAY', 'accent': '#0891b2', 'count': 1},
]


# ============================================================
# HELPERS
# ============================================================
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def format_email_time(time_str):
    if not time_str:
        return ""
    if "T" not in time_str:
        return time_str
    try:
        dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = now - dt
        total_seconds = int(delta.total_seconds())
        if total_seconds < 0:
            return "JUST NOW"
        minutes = total_seconds // 60
        if minutes < 60:
            return f"{minutes}M AGO"
        hours = minutes // 60
        if hours < 24:
            return f"{hours}H AGO"
        return dt.strftime("%b %d, %I:%M %p").upper()
    except Exception:
        return time_str


def smart_truncate(text, length=240):
    """Truncate text at a sentence or word boundary for clean previews."""
    if not text:
        return ""
    # Strip trailing ellipsis already in the text
    text = text.rstrip('.')
    if len(text) <= length:
        return text
    chunk = text[:length]
    # Try to end at a sentence
    for sep in ['. ', '! ', '? ', '.\n']:
        last = chunk.rfind(sep)
        if last > int(length * 0.55):
            return chunk[:last + 1].strip()
    # Fall back to word boundary
    last_space = chunk.rfind(' ')
    if last_space > 0:
        return chunk[:last_space].strip() + '…'
    return chunk + '…'


def get_article_url(story):
    url = story.get('articleUrl', '').strip()
    if url:
        return url
    query = f"{story.get('headline', '')} {story.get('source', '')}"
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)


def get_stories():
    if not os.path.exists('alpha.db'):
        print("Database not found.")
        return None
    conn = sqlite3.connect('alpha.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stories ORDER BY lead DESC, time DESC')
    rows = cursor.fetchall()
    conn.close()

    stories = {}
    for row in rows:
        cat = row.pop('category')
        if cat not in stories:
            stories[cat] = []
        stories[cat].append(row)
    return stories


# ============================================================
# HTML BUILDERS
# ============================================================
def render_lead_story(story):
    tag = story.get('tag', 'LATEST')
    source = story.get('source', '')
    time_label = format_email_time(story.get('time'))
    headline = story.get('headline', '')
    body = smart_truncate(story.get('body', ''), 360)
    url = get_article_url(story)

    return f"""
    <div style="border-left: 4px solid #059669; padding: 0 0 30px 24px; margin-bottom: 36px;">
        <div style="font-size: 10px; font-weight: bold; color: #059669; text-transform: uppercase;
                    letter-spacing: 2px; margin-bottom: 10px;">
            LEAD STORY &nbsp;|&nbsp;
            <span style="color: #6b7280;">{tag} &bull; {source} &bull; {time_label}</span>
        </div>
        <a href="{url}" style="font-size: 26px; font-weight: bold; font-family: Georgia, serif;
                               color: #111827; text-decoration: none; display: block;
                               line-height: 1.3; margin-bottom: 14px;">
            {headline}
        </a>
        <p style="font-size: 15px; line-height: 1.7; color: #374151; margin: 0 0 16px 0;">
            {body}
        </p>
        <a href="{url}" style="font-size: 11px; font-weight: bold; color: #059669;
                               text-decoration: none; text-transform: uppercase; letter-spacing: 1px;">
            Read Full Story &rarr;
        </a>
    </div>
    """


def render_section_header(label, accent):
    return f"""
    <div style="border-top: 2px solid {accent}; padding-top: 6px; margin: 36px 0 20px 0;">
        <span style="font-size: 10px; font-weight: bold; color: {accent};
                     text-transform: uppercase; letter-spacing: 3px; font-family: Arial, sans-serif;">
            {label}
        </span>
    </div>
    """


def render_story_card(story, accent, brief_length=220, is_deep_read=False):
    tag = story.get('tag', 'NEWS')
    source = story.get('source', '')
    time_label = format_email_time(story.get('time'))
    headline = story.get('headline', '')
    body = smart_truncate(story.get('body', ''), brief_length if not is_deep_read else 340)
    url = get_article_url(story)

    headline_size = "17px" if not is_deep_read else "20px"
    body_size = "13px" if not is_deep_read else "14px"

    return f"""
    <div style="margin-bottom: 24px; padding-bottom: 24px;
                border-bottom: 1px solid #f3f4f6;">
        <div style="font-size: 10px; font-weight: bold; color: #9ca3af;
                    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 7px;">
            {source}
            <span style="color: #d1d5db;">&nbsp;&bull;&nbsp;</span>
            <span style="color: {accent};">{tag}</span>
            <span style="color: #d1d5db;">&nbsp;&bull;&nbsp;</span>
            {time_label}
        </div>
        <a href="{url}" style="font-size: {headline_size}; font-weight: bold;
                               font-family: Georgia, serif; color: #111827;
                               text-decoration: none; display: block;
                               line-height: 1.35; margin-bottom: 10px;">
            {headline}
        </a>
        <p style="font-size: {body_size}; line-height: 1.65; color: #4b5563; margin: 0 0 10px 0;">
            {body}
        </p>
        <a href="{url}" style="font-size: 10px; font-weight: bold; color: {accent};
                               text-decoration: none; text-transform: uppercase; letter-spacing: 1px;">
            Read More &rarr;
        </a>
    </div>
    """


# ============================================================
# MAIN EMAIL GENERATOR
# ============================================================
def generate_email_html(stories):
    today = datetime.now().strftime("%A, %B %d, %Y").upper()
    issue_num = datetime.now().timetuple().tm_yday  # rough issue number

    # ---- Lead story: best recent story from all-news, else any category ----
    all_flat = []
    for cat_stories in stories.values():
        all_flat.extend(cat_stories)

    # Prefer an explicitly marked lead, else pick newest
    lead_story = next((s for s in all_flat if s.get('lead')), None)
    if not lead_story and all_flat:
        lead_story = all_flat[0]

    # ---- Build HTML ----
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>The Alpha — {today}</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f9fafb;
                 color: #111827; margin: 0; padding: 20px 0;">

        <div style="max-width: 620px; margin: 0 auto; background-color: #ffffff;
                    border: 1px solid #e5e7eb;">

            <!-- ====== HEADER ====== -->
            <div style="background-color: #111827; padding: 28px 36px;">
                <div style="font-size: 10px; font-weight: bold; color: #9ca3af;
                            text-transform: uppercase; letter-spacing: 4px; margin-bottom: 8px;">
                    INTEGRATED INTELLIGENCE
                </div>
                <div style="font-size: 36px; font-weight: bold; color: #ffffff;
                            letter-spacing: -1px; font-family: Georgia, serif;">
                    THE ALPHA
                </div>
                <div style="margin-top: 12px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 11px; color: #6b7280; text-transform: uppercase;
                                 letter-spacing: 2px;">{today}</span>
                    <span style="font-size: 10px; color: #4b5563; letter-spacing: 1px;">
                        ISSUE #{issue_num}
                    </span>
                </div>
            </div>

            <!-- ====== BODY ====== -->
            <div style="padding: 36px 36px 12px 36px;">
    """

    # Lead story
    if lead_story:
        html += render_lead_story(lead_story)
    
    # Sections
    for section in SECTIONS:
        cat_stories = stories.get(section['key'], [])
        # Exclude lead story from sections to avoid duplication
        cat_stories = [s for s in cat_stories if s != lead_story]
        if not cat_stories:
            continue

        top_stories = cat_stories[:section['count']]
        html += render_section_header(section['label'], section['accent'])

        for i, story in enumerate(top_stories):
            is_last = (i == len(top_stories) - 1)
            is_deep = section['key'] == 'deep-reads'
            html += render_story_card(
                story,
                accent=section['accent'],
                brief_length=220 if not is_deep else 340,
                is_deep_read=is_deep
            )

    # Dashboard CTA
    html += """
            </div>

            <!-- ====== CTA ====== -->
            <div style="padding: 0 36px 36px 36px; text-align: center;">
                <a href="http://localhost:3333/dashboard"
                   style="display: inline-block; background-color: #111827; color: #ffffff;
                          padding: 14px 32px; text-decoration: none; font-size: 12px;
                          font-weight: bold; letter-spacing: 2px; text-transform: uppercase;
                          margin-top: 12px;">
                    VIEW FULL DASHBOARD &rarr;
                </a>
            </div>

            <!-- ====== FOOTER ====== -->
            <div style="background-color: #f9fafb; border-top: 1px solid #e5e7eb;
                        padding: 20px 36px; text-align: center;">
                <p style="font-size: 10px; color: #9ca3af; text-transform: uppercase;
                           letter-spacing: 1px; margin: 0;">
                    &copy; 2026 The Alpha Intelligence Group &nbsp;&bull;&nbsp;
                    Auto-generated daily briefing
                </p>
            </div>

        </div>
    </body>
    </html>
    """
    return html


# ============================================================
# SEND
# ============================================================
def send_email():
    if not all([SENDER_EMAIL, SENDER_PASSWORD]):
        print("ERROR: Missing SENDER_EMAIL or SENDER_APP_PASSWORD in .env")
        return False

    print("Reading news from alpha.db...")
    stories = get_stories()
    if not stories:
        print("Failed to load stories.")
        return False

    print("Generating email HTML...")
    html_content = generate_email_html(stories)

    # Load subscribers
    try:
        with open('subscribers.json', 'r') as f:
            subs = json.load(f)
    except Exception:
        subs = []

    if RECEIVER_EMAIL and RECEIVER_EMAIL not in subs:
        subs.append(RECEIVER_EMAIL)

    if not subs:
        print("No subscribers found.")
        return False

    subject = f"The Alpha Daily Briefing — {datetime.now().strftime('%B %d, %Y')}"
    print(f"Connecting to SMTP... dispatching to {len(subs)} subscriber(s).")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        for email in subs:
            print(f"  Sending to {email}...")
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"The Alpha Terminal <{SENDER_EMAIL}>"
            msg['To'] = email
            msg.attach(MIMEText(html_content, 'html'))
            server.sendmail(SENDER_EMAIL, email, msg.as_string())

        server.quit()
        print("Email dispatched successfully to all subscribers!")
        return True

    except Exception as e:
        print(f"SMTP Error: {e}")
        return False


if __name__ == "__main__":
    send_email()
