with open('data.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
sources = []
for line in lines:
    if 'source:' in line:
        s = line.split('source:')[1].strip()
        if s.startswith("'") or s.startswith('"'):
            s = s[1:]
        if s.endswith("',"):
            s = s[:-2]
        if s.endswith("', "):
            s = s[:-3]
        if s.endswith("',"):
            s = s[:-2]
        if s.endswith("'"):
            s = s[:-1]
        
        sources.append(s)

unique_sources = sorted(list(set(sources)))
for s in unique_sources:
    print(f"- {s}")
