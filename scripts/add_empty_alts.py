import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = list(root.rglob('*.html'))

img_tag_re = re.compile(r'(<img\s+)([^>]*?)>', re.IGNORECASE | re.DOTALL)
modified = []

for f in files:
    s = f.read_text(encoding='utf-8')

    def repl(match):
        prefix = match.group(1)
        body = match.group(2)
        # if alt present, return original
        if re.search(r"\balt\s*=", body, re.IGNORECASE):
            return match.group(0)
        # insert alt="" before the closing
        new = prefix + body + ' alt=""' + '>'
        return new

    s2 = img_tag_re.sub(repl, s)
    if s2 != s:
        f.write_text(s2, encoding='utf-8')
        modified.append(str(f.relative_to(root)))

print('Added empty alt to', len(modified), 'files')
for m in modified[:200]:
    print('-', m)
