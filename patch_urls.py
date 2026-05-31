import re

def patch_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace the generic sourceUrl with dynamic search URL in the JS template literal
    patched_href = r"""href="${story.articleUrl || 'https://www.google.com/search?q=' + encodeURIComponent(story.headline + ' ' + story.source)}" """
    
    # We replace exact occurrences of href="${story.sourceUrl || '#'}" 
    html = html.replace('href="${story.sourceUrl || \'#\'}"', patched_href)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

def patch_email_script():
    with open('send_daily_alpha.py', 'r', encoding='utf-8') as f:
        py_code = f.read()
        
    if "import urllib.parse" not in py_code:
        py_code = "import urllib.parse\n" + py_code
        
    if "def get_article_url" not in py_code:
        # Insert helper function before generate_email_html
        helper = """
def get_article_url(story):
    article_url = story.get('articleUrl')
    if article_url:
        return article_url
    query = f"{story.get('headline', '')} {story.get('source', '')}"
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)

"""
        py_code = py_code.replace("def generate_email_html", helper + "def generate_email_html")
        
    # Replace hrefs in the f-strings
    py_code = py_code.replace('href="{lead_story.get(\'sourceUrl\', \'#\')}"', 'href="{get_article_url(lead_story)}"')
    py_code = py_code.replace('href="{story.get(\'sourceUrl\', \'#\')}"', 'href="{get_article_url(story)}"')
    
    with open('send_daily_alpha.py', 'w', encoding='utf-8') as f:
        f.write(py_code)

if __name__ == '__main__':
    patch_index()
    patch_email_script()
