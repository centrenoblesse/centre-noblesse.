import re

with open('app/templates/public/index.html', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '\ufffd' in l:
        print(f'Line {i+1}: {l.encode("ascii", "ignore").decode("ascii").strip()}')
