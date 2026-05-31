import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update fonts to Lora and Montserrat (Very premium)
text = text.replace("Georgia, 'Times New Roman', serif", "'Lora', Georgia, serif")
text = text.replace("'Helvetica Neue', Helvetica, Arial, sans-serif", "'Montserrat', sans-serif")
text = text.replace('<link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400;1,700;1,900&family=Inter:wght@300..700&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">',
'<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Montserrat:ital,wght@0,300..800;1,300..800&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">')

# Also fix the font variables if they weren't matched exactly
text = re.sub(r"--font-headline:\s*[^;]+;", "--font-headline: 'Lora', Georgia, serif;", text)
text = re.sub(r"--font-sans:\s*[^;]+;", "--font-sans: 'Montserrat', sans-serif;", text)


# 2. Remove Print Button
text = re.sub(r'<button class="btn-control" id="btn-print".*?</button>', '', text, flags=re.DOTALL)
text = re.sub(r'<a href="#" id="btn-print-edition".*?</a>', '', text, flags=re.DOTALL)

# 3. Strip out QUOTES, STORIES, READING_ROOM and insert data.js
# We need to find where QUOTES starts and READING_ROOM ends.
m_quotes = re.search(r'// ==================== INVESTOR QUOTES ====================', text)
m_reading = re.search(r'// ==================== RENDERING ENGINE ====================', text)

if m_quotes and m_reading:
    start_idx = m_quotes.start()
    end_idx = m_reading.start()
    
    script_tag = "<script src=\"data.js\"></script>\n"
    
    text = text[:start_idx] + script_tag + text[end_idx:]

# 4. Update Market Data baseline to May 31, 2026 (Live data mock)
text = text.replace("nifty:   { base: 23547.75", "nifty:   { base: 23755.20")
text = text.replace("sensex:  { base: 74775.74", "sensex:  { base: 75200.10")
text = text.replace("usdinr:  { base: 84.96", "usdinr:  { base: 84.85")
text = text.replace("gold:    { base: 156463", "gold:    { base: 158200")
text = text.replace("us10y:   { base: 4.45", "us10y:   { base: 4.38")
text = text.replace("in10y:   { base: 7.00", "in10y:   { base: 7.02")

# To fix CORS issue in Yahoo Finance fetch, we prepend a public CORS proxy
text = text.replace("https://query1.finance.yahoo.com", "https://corsproxy.io/?https://query1.finance.yahoo.com")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# Also, ensure QUOTES is in data.js since we removed it from index.html!
with open('data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

if 'const QUOTES' not in data_js:
    quotes_str = """
const QUOTES = [
    { text: "The stock market is a device for transferring money from the impatient to the patient.", author: "Warren Buffett" },
    { text: "Price is what you pay. Value is what you get.", author: "Warren Buffett" },
    { text: "Time in the market beats timing the market.", author: "Ken Fisher" },
];\n
"""
    data_js = quotes_str + data_js
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(data_js)

print("Applied fixes!")
