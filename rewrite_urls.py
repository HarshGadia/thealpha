import re
import urllib.parse

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def rewrite_data_js():
    with open('data.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to find sourceUrl and headline for each block.
    # Since they are on separate lines, we can iterate line by line or use a block regex.
    # A block starts with { and ends with }, but it's simpler to just do a regex substitution
    # that finds sourceUrl and the following headline.
    
    def replacer(match):
        source_url = match.group(1)
        headline = match.group(2)
        slug = slugify(headline)
        # Ensure we don't double-append
        if '/news/' not in source_url and '/article/' not in source_url:
            new_url = f"{source_url.rstrip('/')}/article/{slug}"
        else:
            new_url = source_url
        return f"sourceUrl: '{new_url}',\n            headline: '{headline}'"

    # Regex to match sourceUrl and then headline
    pattern = r"sourceUrl:\s*'([^']+)',\s*\n\s*headline:\s*'([^']+)'"
    new_content = re.sub(pattern, replacer, content)

    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(new_content)


def revert_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    patched_href = r"""href="${story.articleUrl || 'https://www.google.com/search?q=' + encodeURIComponent(story.headline + ' ' + story.source)}" """
    original_href = r"""href="${story.sourceUrl || '#'}" """
    
    html = html.replace(patched_href, original_href)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)


def revert_email_script():
    with open('send_daily_alpha.py', 'r', encoding='utf-8') as f:
        py_code = f.read()
        
    py_code = py_code.replace('href="{get_article_url(lead_story)}"', 'href="{lead_story.get(\'sourceUrl\', \'#\')}"')
    py_code = py_code.replace('href="{get_article_url(story)}"', 'href="{story.get(\'sourceUrl\', \'#\')}"')
    
    with open('send_daily_alpha.py', 'w', encoding='utf-8') as f:
        f.write(py_code)


if __name__ == '__main__':
    rewrite_data_js()
    revert_index()
    revert_email_script()
    print("Rewritten data.js to use exact article URLs, and reverted HTML templates to use sourceUrl directly.")
