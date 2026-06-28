import urllib.parse
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import sqlite3
import socket
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
DASHBOARD_URL = os.getenv("DASHBOARD_URL", "http://localhost:3333/dashboard")

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
    url = (story.get('articleUrl') or '').strip()
    if url:
        return url
    headline = story.get('headline') or ''
    source = story.get('source') or ''
    query = f"{headline} {source}"
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)


def get_stories(edition_filter=None):
    data_dir = os.environ.get('DATA_DIR', '.')
    db_path = os.path.join(data_dir, 'alpha.db')
    if not os.path.exists(db_path):
        print("Database not found.")
        return None
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    if edition_filter:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='edition_stories'")
        if cursor.fetchone():
            cursor.execute('''
                SELECT s.* FROM stories s
                JOIN edition_stories e ON s.id = e.story_id
                WHERE e.edition = ?
                ORDER BY s.lead DESC, s.time DESC
            ''', (edition_filter,))
        else:
            cursor.execute('SELECT * FROM stories ORDER BY lead DESC, time DESC')
    else:
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
    tag = story.get('tag') or 'LATEST'
    source = story.get('source') or ''
    time_label = format_email_time(story.get('time'))
    headline = story.get('headline') or ''
    body = smart_truncate(story.get('body') or '', 360)
    url = get_article_url(story)

    return f"""
    <div style="padding-bottom: 25px; margin-bottom: 25px; border-bottom: 1px solid #e2e8f0;">
        <div style="margin-bottom: 10px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1;">
            <span style="color: #059669; font-size: 10px; font-weight: bold; text-transform: uppercase; letter-spacing: 1.5px; display: inline-block;">
                {tag}
            </span>
            <span style="font-size: 10.5px; color: #64748b; font-weight: 500; margin-left: 8px; display: inline-block; vertical-align: middle;">
                {source} &bull; {time_label}
            </span>
        </div>
        <a href="{url}" style="font-size: 26px; font-weight: bold; font-family: Georgia, serif;
                               color: #111827; text-decoration: none; display: block;
                               line-height: 1.3; margin-bottom: 14px;">
            {headline}
        </a>
        <p style="font-size: 14.5px; line-height: 1.65; color: #374151; margin: 0 0 16px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            {body}
        </p>
    </div>
    """


def render_section_header(label, accent):
    return f"""
    <div style="border-bottom: 2px solid #111827; padding-bottom: 4px; margin: 25px 0 16px 0;">
        <span style="font-size: 12px; font-weight: bold; color: #111827;
                     text-transform: uppercase; letter-spacing: 2px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            {label}
        </span>
    </div>
    """


def render_story_card(story, accent, brief_length=220, is_deep_read=False):
    tag = story.get('tag') or 'NEWS'
    source = story.get('source') or ''
    time_label = format_email_time(story.get('time'))
    headline = story.get('headline') or ''
    body = smart_truncate(story.get('body') or '', brief_length if not is_deep_read else 340)
    url = get_article_url(story)

    headline_size = "16px" if not is_deep_read else "19px"
    body_size = "12.5px" if not is_deep_read else "13.5px"
    margin_bottom = "16px" if not is_deep_read else "24px"

    return f"""
    <div style="margin-bottom: {margin_bottom}; padding-bottom: 16px; border-bottom: 1px solid #f1f5f9;">
        <div style="margin-bottom: 6px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1;">
            <span style="color: {accent}; font-size: 9px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; display: inline-block;">
                {tag}
            </span>
            <span style="font-size: 10px; color: #64748b; font-weight: 500; margin-left: 6px; display: inline-block; vertical-align: middle;">
                {source} &bull; {time_label}
            </span>
        </div>
        <a href="{url}" style="font-size: {headline_size}; font-weight: bold;
                               font-family: Georgia, serif; color: #111827;
                               text-decoration: none; display: block;
                               line-height: 1.35; margin-bottom: 8px;">
            {headline}
        </a>
        <p style="font-size: {body_size}; line-height: 1.6; color: #475569; margin: 0 0 12px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            {body}
        </p>
    </div>
    """


# ============================================================
# MAIN EMAIL GENERATOR
# ============================================================
def generate_email_html(stories):
    today = datetime.now().strftime("%A, %B %d, %Y").upper()
    issue_num = datetime.now().timetuple().tm_yday

    all_flat = []
    for cat_stories in stories.values():
        all_flat.extend(cat_stories)

    # Prefer an explicitly marked lead, else pick newest
    lead_story = next((s for s in all_flat if s.get('lead')), None)
    if not lead_story and all_flat:
        lead_story = all_flat[0]

    # Custom caps for the morning edition sections
    caps = {
        'vc-inflow': 2,
        'stocks-arena': 1,
        'tech-specs': 2,
        'global-dial': 1,
        'deep-reads': 1
    }

    # Helper to render a category block
    def render_cat_block(cat_key):
        cat_stories = stories.get(cat_key, [])
        cat_stories = [s for s in cat_stories if s != lead_story]
        if not cat_stories:
            return ""
        section = next((s for s in SECTIONS if s['key'] == cat_key), None)
        if not section:
            return ""
        
        limit = caps.get(cat_key, 2)
        top_stories = cat_stories[:limit]
        block = render_section_header(section['label'], section['accent'])
        for story in top_stories:
            block += render_story_card(story, accent=section['accent'])
        return block

    # Split main content into 2 columns for laptop width
    left_html = render_cat_block('vc-inflow') + render_cat_block('stocks-arena')
    right_html = render_cat_block('tech-specs') + render_cat_block('global-dial')
    
    # Deep reads (full width at bottom)
    deep_reads_html = ""
    cat_key = 'deep-reads'
    if cat_key in stories:
        cat_stories = [s for s in stories[cat_key] if s != lead_story]
        if cat_stories:
            section = next((s for s in SECTIONS if s['key'] == cat_key), None)
            if section:
                limit = caps.get(cat_key, 1)
                top_stories = cat_stories[:limit]
                deep_reads_html += """
                <div style="text-align: center; border-top: 1.5px solid #111827; border-bottom: 1.5px solid #111827; padding: 6px 0; margin: 30px 0 20px 0;">
                    <span style="font-size: 13px; font-weight: bold; color: #111827; text-transform: uppercase; letter-spacing: 3px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
                        DEEP READ OF THE DAY
                    </span>
                </div>
                """
                for story in top_stories:
                    deep_reads_html += render_story_card(story, accent=section['accent'], is_deep_read=True)

    # ---- Build HTML ----
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Newtella — {today}</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #fdfbf7 !important;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
            }}
            table, td {{
                border-collapse: collapse;
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
            }}
            @media only screen and (max-width: 680px) {{
                .container {{
                    width: 100% !important;
                    border: none !important;
                    border-radius: 0px !important;
                    margin: 0px !important;
                }}
                .responsive-col {{
                    display: block !important;
                    width: 100% !important;
                    padding-left: 0 !important;
                    padding-right: 0 !important;
                    box-sizing: border-box !important;
                }}
                .responsive-table {{
                    width: 100% !important;
                }}
                .inner-body {{
                    padding: 24px 20px !important;
                }}
                .header-padding {{
                    padding: 24px 20px 0px 20px !important;
                }}
            }}
        </style>
    </head>
    <body style="margin: 0; padding: 0; background-color: #fdfbf7;">

        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #fdfbf7; padding: 20px 0;">
            <tr>
                <td align="center">
                    <div class="container" style="width: 95%; max-width: 880px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 4px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03); overflow: hidden;">
                        
                        <!-- ====== HEADER ====== -->
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff;">
                            <tr>
                                <td class="header-padding" style="padding: 36px 45px 0px 45px; text-align: center;">
                                    <div style="font-size: 10px; font-weight: bold; color: #64748b; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 8px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
                                        DAILY DISPATCH &bull; FINANCIAL TERMINAL
                                    </div>
                                    <div style="font-size: 42px; font-weight: bold; color: #111827; letter-spacing: -1.5px; font-family: Georgia, serif; line-height: 1.0; margin-bottom: 12px;">
                                        Newtella Terminal
                                    </div>
                                    
                                    <!-- Double rule date divider -->
                                    <div style="border-top: 2.5px solid #111827; border-bottom: 0.5px solid #111827; padding: 6px 0; margin-top: 15px;">
                                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
                                                <td align="left" style="font-size: 10.5px; color: #111827; text-transform: uppercase; letter-spacing: 2px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-weight: bold;">
                                                    {today}
                                                </td>
                                                <td align="right" style="font-size: 10.5px; color: #111827; letter-spacing: 1.5px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-weight: bold;">
                                                    ISSUE #{issue_num}
                                                </td>
                                            </tr>
                                        </table>
                                    </div>
                                </td>
                            </tr>
                        </table>

                        <!-- ====== BODY ====== -->
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
                                <td class="inner-body" style="padding: 20px 45px 12px 45px; background-color: #ffffff;">
                                    
                                    <!-- Lead Story -->
                                    {render_lead_story(lead_story) if lead_story else ''}

                                    <!-- Grid Sections -->
                                    <table class="responsive-table" role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;">
                                        <tr>
                                            <!-- Left Column -->
                                            <td class="responsive-col" width="48%" valign="top" style="padding-right: 20px; vertical-align: top;">
                                                {left_html}
                                            </td>
                                            <!-- Right Column -->
                                            <td class="responsive-col" width="48%" valign="top" style="padding-left: 20px; vertical-align: top;">
                                                {right_html}
                                            </td>
                                        </tr>
                                    </table>

                                    <!-- Full Width Deep Reads -->
                                    {deep_reads_html}

                                </td>
                            </tr>
                        </table>

                        <!-- ====== CTA ====== -->
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff;">
                            <tr>
                                <td align="center" style="padding: 10px 45px 36px 45px;">
                                    <a href="{DASHBOARD_URL}" style="display: inline-block; background-color: #111827; color: #ffffff; padding: 13px 32px; text-decoration: none; font-size: 11px; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; border-radius: 2px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
                                        ACCESS FULL TERMINAL &rarr;
                                    </a>
                                </td>
                            </tr>
                        </table>

                        <!-- ====== FOOTER ====== -->
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff; border-top: 1px solid #e2e8f0;">
                            <tr>
                                <td style="padding: 24px 45px; text-align: center;">
                                    <p style="font-size: 10px; color: #64748b; text-transform: uppercase; letter-spacing: 1.5px; margin: 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-weight: bold;">
                                        &copy; 2026 Newtella &nbsp;&bull;&nbsp; Auto-generated Daily briefing
                                    </p>
                                </td>
                            </tr>
                        </table>

                    </div>
                </td>
            </tr>
        </table>
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
    stories = get_stories(edition_filter='morning')
    if not stories:
        print("Failed to load stories.")
        return False

    print("Generating email HTML...")
    html_content = generate_email_html(stories)

    # Load subscribers
    data_dir = os.environ.get('DATA_DIR', '.')
    subs_path = os.path.join(data_dir, 'subscribers.json')
    try:
        with open(subs_path, 'r') as f:
            subs = json.load(f)
    except Exception:
        subs = []

    if RECEIVER_EMAIL and RECEIVER_EMAIL not in subs:
        subs.append(RECEIVER_EMAIL)

    if not subs:
        print("No subscribers found.")
        return (False, "No subscribers found")

    subject = f"Newtella Daily Briefing — {datetime.now().strftime('%B %d, %Y')}"
    print(f"Connecting to SMTP... dispatching to {len(subs)} subscriber(s).")

    try:
        # Force IPv4 resolution to prevent "Network is unreachable" on platforms without IPv6 (like Railway)
        smtp_host = socket.gethostbyname('smtp.gmail.com')
        server = smtplib.SMTP(smtp_host, 587)
        server.ehlo('smtp.gmail.com') # Let gmail know who we are since we are connecting via IP
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        for email in subs:
            print(f"  Sending to {email}...")
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"Newtella Terminal <{SENDER_EMAIL}>"
            msg['To'] = email
            msg.attach(MIMEText(html_content, 'html'))
            server.sendmail(SENDER_EMAIL, email, msg.as_string())

        server.quit()
        print("Email dispatched successfully to all subscribers!")
        return (True, subs)

    except Exception as e:
        print(f"SMTP Error: {e}")
        return (False, str(e))


def generate_evening_email_html(stories):
    today = datetime.now().strftime("%A, %B %d, %Y").upper()
    issue_num = datetime.now().timetuple().tm_yday

    # Custom caps for the evening update sections (VC:2, Markets:2, Tech:2, Macro:2)
    caps = {
        'vc-inflow': 2,
        'stocks-arena': 2,
        'tech-specs': 2,
        'global-dial': 2
    }

    # Helper for evening category block
    def render_evening_cat_block(cat_key):
        cat_stories = stories.get(cat_key, [])
        if not cat_stories:
            return ""
        section = next((s for s in SECTIONS if s['key'] == cat_key), None)
        if not section:
            return ""
        
        limit = caps.get(cat_key, 2)
        top_stories = cat_stories[:limit]
        block = render_section_header(section['label'], "#991b1b")
        for story in top_stories:
            block += render_story_card(story, accent="#991b1b")
        return block

    # Split main content into columns
    left_html = render_evening_cat_block('vc-inflow') + render_evening_cat_block('stocks-arena')
    right_html = render_evening_cat_block('tech-specs') + render_evening_cat_block('global-dial')
    
    # ---- Build HTML ----
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Newtella Evening Update — {today}</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #fdfbf7 !important;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
            }}
            table, td {{
                border-collapse: collapse;
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
            }}
            @media only screen and (max-width: 680px) {{
                .container {{
                    width: 100% !important;
                    border: none !important;
                    border-radius: 0px !important;
                    margin: 0px !important;
                }}
                .responsive-col {{
                    display: block !important;
                    width: 100% !important;
                    padding-left: 0 !important;
                    padding-right: 0 !important;
                    box-sizing: border-box !important;
                }}
                .responsive-table {{
                    width: 100% !important;
                }}
                .inner-body {{
                    padding: 24px 20px !important;
                }}
                .header-padding {{
                    padding: 24px 20px 0px 20px !important;
                }}
            }}
        </style>
    </head>
    <body style="margin: 0; padding: 0; background-color: #fdfbf7;">

        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #fdfbf7; padding: 20px 0;">
            <tr>
                <td align="center">
                    <div class="container" style="width: 95%; max-width: 880px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 4px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03); overflow: hidden;">
                        
                        <!-- ====== HEADER ====== -->
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff;">
                            <tr>
                                <td class="header-padding" style="padding: 36px 45px 0px 45px; text-align: center;">
                                    <div style="font-size: 10px; font-weight: bold; color: #b91c1c; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 8px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
                                        LATE-BREAKING INTELLIGENCE &bull; EVENING EDITION
                                    </div>
                                    <div style="font-size: 42px; font-weight: bold; color: #991b1b; letter-spacing: -1.5px; font-family: Georgia, serif; line-height: 1.0; margin-bottom: 12px;">
                                        Newtella: Late Update
                                    </div>
                                    
                                    <!-- Double rule date divider (dark red) -->
                                    <div style="border-top: 2.5px solid #991b1b; border-bottom: 0.5px solid #991b1b; padding: 6px 0; margin-top: 15px;">
                                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
                                                <td align="left" style="font-size: 10.5px; color: #991b1b; text-transform: uppercase; letter-spacing: 2px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-weight: bold;">
                                                    {today}
                                                </td>
                                                <td align="right" style="font-size: 10.5px; color: #991b1b; letter-spacing: 1.5px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-weight: bold;">
                                                    LATE EDITION
                                                </td>
                                            </tr>
                                        </table>
                                    </div>
                                </td>
                            </tr>
                        </table>

                        <!-- ====== BODY ====== -->
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
                                <td class="inner-body" style="padding: 20px 45px 12px 45px; background-color: #ffffff;">
                                    
                                    <!-- Grid Sections -->
                                    <table class="responsive-table" role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;">
                                        <tr>
                                            <!-- Left Column -->
                                            <td class="responsive-col" width="48%" valign="top" style="padding-right: 20px; vertical-align: top;">
                                                {left_html}
                                            </td>
                                            <!-- Right Column -->
                                            <td class="responsive-col" width="48%" valign="top" style="padding-left: 20px; vertical-align: top;">
                                                {right_html}
                                            </td>
                                        </tr>
                                    </table>

                                </td>
                            </tr>
                        </table>

                        <!-- ====== CTA ====== -->
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff;">
                            <tr>
                                <td align="center" style="padding: 10px 45px 36px 45px;">
                                    <a href="{DASHBOARD_URL}" style="display: inline-block; background-color: #991b1b; color: #ffffff; padding: 13px 32px; text-decoration: none; font-size: 11px; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; border-radius: 2px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
                                        ACCESS FULL TERMINAL &rarr;
                                    </a>
                                </td>
                            </tr>
                        </table>

                        <!-- ====== FOOTER ====== -->
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff; border-top: 1px solid #e2e8f0;">
                            <tr>
                                <td style="padding: 24px 45px; text-align: center;">
                                    <p style="font-size: 10px; color: #991b1b; text-transform: uppercase; letter-spacing: 1.5px; margin: 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-weight: bold;">
                                        &copy; 2026 Newtella &nbsp;&bull;&nbsp; Auto-generated Evening update
                                    </p>
                                </td>
                            </tr>
                        </table>

                    </div>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html


def send_evening_email():
    if not all([SENDER_EMAIL, SENDER_PASSWORD]):
        print("ERROR: Missing SENDER_EMAIL or SENDER_APP_PASSWORD in .env")
        return False

    print("Reading evening news from alpha.db...")
    stories = get_stories(edition_filter='evening')
    if not stories or not any(stories.values()):
        print("No new evening stories found. Skipping evening email.")
        return False

    print("Generating evening email HTML...")
    html_content = generate_evening_email_html(stories)

    # Load subscribers
    data_dir = os.environ.get('DATA_DIR', '.')
    subs_path = os.path.join(data_dir, 'subscribers.json')
    try:
        with open(subs_path, 'r') as f:
            subs = json.load(f)
    except Exception:
        subs = []

    if RECEIVER_EMAIL and RECEIVER_EMAIL not in subs:
        subs.append(RECEIVER_EMAIL)

    if not subs:
        print("No subscribers found.")
        return (False, "No subscribers found")

    subject = f"Newtella Evening Update — {datetime.now().strftime('%B %d, %Y')}"
    print(f"Connecting to SMTP... dispatching to {len(subs)} subscriber(s).")

    try:
        smtp_host = socket.gethostbyname('smtp.gmail.com')
        server = smtplib.SMTP(smtp_host, 587)
        server.ehlo('smtp.gmail.com')
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        for email in subs:
            print(f"  Sending evening update to {email}...")
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"Newtella Terminal <{SENDER_EMAIL}>"
            msg['To'] = email
            msg.attach(MIMEText(html_content, 'html'))
            server.sendmail(SENDER_EMAIL, email, msg.as_string())

        server.quit()
        print("Evening email dispatched successfully to all subscribers!")
        return (True, subs)

    except Exception as e:
        print(f"SMTP Error: {e}")
        return (False, str(e))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'evening':
        send_evening_email()
    else:
        send_email()
