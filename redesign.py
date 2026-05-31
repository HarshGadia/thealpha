import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fonts
html = re.sub(
    r'<link href=\"https://fonts.googleapis.com/css2\?family=Playfair\+Display[^>]+>',
    '<link href=\"https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400;1,700;1,900&family=Inter:wght@300..700&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap\" rel=\"stylesheet\">',
    html
)
html = html.replace("'Playfair Display', Georgia, 'Times New Roman', serif", "'Merriweather', Georgia, serif")
html = html.replace("'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif", "'Inter', -apple-system, BlinkMacSystemFont, sans-serif")

# 2. Convert to Light Theme as Default and remove neon accents
# We will just replace the :root colors completely.
light_theme_css = """
        :root {
            --bg-primary: #FFFFFF;
            --bg-surface: #F9F9FB;
            --bg-elevated: #F4F4F7;
            --bg-hover: #F0F0F5;
            --bg-card: #FFFFFF;
            --bg-masthead: rgba(255, 255, 255, 0.95);
            --bg-masthead-border: #E5E5E5;

            --accent-mint: #0F5132;
            --accent-purple: #3A3A3A;
            --accent-gold: #856404;
            --accent-cyan: #052C65;
            --accent-rose: #842029;
            --accent-red: #842029;
            --accent-green: #0F5132;
            --accent-slate: #475569;
            --accent-yellow: #856404;

            --text-primary: #111111;
            --text-secondary: #444444;
            --text-tertiary: #777777;
            --text-muted: #A0A0A0;
            --text-on-dark: #FFFFFF;

            --border-subtle: #E5E5E5;
            --border-card: #E5E5E5;
            --border-hover: #CCCCCC;

            --glass-bg: rgba(255, 255, 255, 0.98);
            --glass-border: rgba(0, 0, 0, 0.05);
            --glass-blur: 8px;

            --shadow-card: none;
            --shadow-card-hover: 0 4px 12px rgba(0,0,0,0.05);
            --shadow-elevated: 0 4px 20px rgba(0, 0, 0, 0.08);
            --shadow-widget: none;

            --radius-sm: 0px;
            --radius-md: 0px;
            --radius-lg: 0px;

            --font-headline: 'Merriweather', Georgia, 'Times New Roman', serif;
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'IBM Plex Mono', 'Fira Code', 'Consolas', monospace;

            --transition-fast: 150ms ease;
            --transition-med: 250ms ease;
            --transition-slow: 400ms cubic-bezier(0.4, 0, 0.2, 1);
        }
"""

# Replace the :root block
html = re.sub(r':root\s*\{[^}]+\}', light_theme_css.strip(), html, count=1)

# Remove the dark mode theme toggler because we want it strictly professional/light.
# Or just let the second theme block remain but it won't be used.

# 3. Add borders to cards and remove border-radius everywhere
html = html.replace('border-radius: var(--radius-lg);', 'border-radius: 0; border: 1px solid var(--border-card);')
html = html.replace('border-radius: var(--radius-md);', 'border-radius: 0; border: 1px solid var(--border-card);')

# 4. Save
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
