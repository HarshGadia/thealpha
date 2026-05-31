import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update fonts to ultra-classic non-Claude stack
html = html.replace("'Merriweather', Georgia, 'Times New Roman', serif", "Georgia, 'Times New Roman', serif")
html = html.replace("'Inter', -apple-system, BlinkMacSystemFont, sans-serif", "'Helvetica Neue', Helvetica, Arial, sans-serif")

# 2. Fix the masthead logo (remove gradient, reduce size)
logo_old = r"""\.masthead-logo \{
            font-family: var\(--font-headline\);
            font-size: 36px;
            font-weight: 900;
            font-style: italic;
            letter-spacing: -1px;
            background: linear-gradient\(135deg, var\(--accent-mint\), var\(--accent-cyan\)\);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        \}"""

logo_new = """.masthead-logo {
            font-family: var(--font-headline);
            font-size: 26px;
            font-weight: bold;
            letter-spacing: -0.5px;
            color: var(--text-primary);
            text-transform: uppercase;
        }"""
html = re.sub(logo_old, logo_new, html, flags=re.MULTILINE)

# Also fix the tagline to be smaller
tagline_old = r"""\.masthead-tagline \{
            font-family: var\(--font-mono\);
            font-size: 13px;
            color: var\(--text-secondary\);
            padding-left: 16px;
            border-left: 1px solid var\(--border-subtle\);
            text-transform: uppercase;
            letter-spacing: 0\.5px;
        \}"""
tagline_new = """.masthead-tagline {
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--text-tertiary);
            padding-left: 12px;
            border-left: 1px solid var(--border-subtle);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }"""
html = re.sub(tagline_old, tagline_new, html, flags=re.MULTILINE)

masthead_top_old = r"""\.masthead-top \{
            padding: 20px 32px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        \}"""
masthead_top_new = """.masthead-top {
            padding: 12px 24px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }"""
html = re.sub(masthead_top_old, masthead_top_new, html, flags=re.MULTILINE)


# 3. Remove the Fund Tracker Widget entirely.
# I will find the lines and slice them out.
lines = html.split('\n')
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '<!-- Fund Tracker Widget -->' in line:
        start_idx = i
    if start_idx != -1 and '</div>' in line and i > start_idx + 25:
        # Looking ahead for the next widget or the end of the sidebar
        if i + 1 < len(lines) and ('</aside>' in lines[i+1] or '<!--' in lines[i+1]):
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    lines = lines[:start_idx] + lines[end_idx+1:]
else:
    print(f"Warning: Could not find Fund Tracker perfectly. Start: {start_idx}, End: {end_idx}")
    
# Let's double check if we missed the exact end. I will just use regex for the block.
html2 = '\n'.join(lines)
fund_tracker_regex = re.compile(r'<!-- Fund Tracker Widget -->.*?<div class="fund-card">.*?</div>\s*</div>\s*</div>', re.DOTALL)
html2 = re.sub(fund_tracker_regex, '', html2)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html2)

print("Updates applied successfully.")
