import urllib.request, urllib.parse, re
query = 'Nifty, Sensex Bleed 1.5% MSCI Rebalancing Hits Harder Than Expected Business Standard'
data = urllib.parse.urlencode({'q': query}).encode('utf-8')
req = urllib.request.Request('https://lite.duckduckgo.com/lite/', data=data, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
with open('ddg.html', 'w', encoding='utf-8') as f:
    f.write(html)
urls = re.findall(r'href="(https?://[^"]+)"', html)
print(urls[:5])
