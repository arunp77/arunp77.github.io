import os, re
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
modified = []
for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        if not fn.endswith('.html'): continue
        path = os.path.join(dirpath, fn)
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
        if 'kit.fontawesome.com' in s and 'cdnjs.cloudflare.com/ajax/libs/font-awesome' in s:
            # remove the cdn font-awesome <link ...> line(s)
            s2 = re.sub(r"\n?\s*<link[^>]*cdnjs\.cloudflare\.com/ajax/libs/font-awesome[^>]*>\s*\n?","\n", s)
            if s2 != s:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(s2)
                modified.append(os.path.relpath(path, root))
print('Removed CDN CSS from files with kit:')
for m in modified:
    print(m)
print('Total:', len(modified))
