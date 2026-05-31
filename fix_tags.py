import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the broken script tag issue
text = text.replace('<script src="data.js"></script>\n// ==================== RENDERING ENGINE ====================', '// ==================== RENDERING ENGINE ====================')

text = text.replace('<script>\n/* ================================================================', 
'<script src="data.js"></script>\n<script>\n/* ================================================================')

# Wait, let's just make sure it's perfect by checking if data.js is already above:
if '<script src="data.js"></script>\n<script>' not in text:
    text = text.replace('<script>\n/* ================================================================', 
'<script src="data.js"></script>\n<script>\n/* ================================================================')

# Remove any stray <script src="data.js"></script> inside the script block
text = re.sub(r'(?<=<script>).*?<script src="data\.js"></script>', '', text, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed script tags!")
