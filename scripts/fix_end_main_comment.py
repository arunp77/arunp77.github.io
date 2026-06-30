import re
from pathlib import Path
root = Path(__file__).resolve().parents[1]
files = list(root.rglob('*.html'))
modified = []
pattern = re.compile(r'</main>\s*<!--\s*End #main\s*--\s*\n?', re.IGNORECASE)
for f in files:
    s = f.read_text(encoding='utf-8')
    s2 = pattern.sub('</main><!-- End #main -->\n', s)
    if s2 != s:
        f.write_text(s2, encoding='utf-8')
        modified.append(str(f.relative_to(root)))
print('Fixed files:', len(modified))
for m in modified[:200]:
    print('-', m)
