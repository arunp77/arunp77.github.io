import re
import os

root = os.path.join(os.path.dirname(__file__), '..')
root = os.path.abspath(root)
modified = []

for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(dirpath, fn)
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
        orig = s
        # Add rel where target="_blank" and no rel in same tag
        s = re.sub(r'target="_blank"(?![^>]*\brel=)', 'target="_blank" rel="noopener noreferrer"', s, flags=re.IGNORECASE)
        # Remove placeholder integrity attributes containing 'your-integrity' or obvious placeholders
        s = re.sub(r'\s*integrity="[^"]*your[^"]*"', '', s, flags=re.IGNORECASE)
        # Remove CDN bootstrap@5.5.0 references (css/js)
        s = re.sub(r"<link[^>]*bootstrap@5\.5\.0[^>]*>\s*", '', s, flags=re.IGNORECASE)
        s = re.sub(r"<script[^>]*bootstrap@5\.5\.0[^>]*>\s*</script>\s*", '', s, flags=re.IGNORECASE)
        # If changed, write back
        if s != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(s)
            modified.append(os.path.relpath(path, root))

print('Modified files:')
for m in modified:
    print(m)
print('Done. Total:', len(modified))
