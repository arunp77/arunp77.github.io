import os, re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
html_files = list(root.rglob('*.html'))

img_no_alt = []
missing_assets = []
blank_rel = []
placeholder_integrity = []

img_re = re.compile(r'<img\s+[^>]*>', re.IGNORECASE)
attr_re = re.compile(r'(\w+)\s*=\s*([\"\'])(.*?)\2', re.IGNORECASE)
link_href_re = re.compile(r'<link[^>]+href\s*=\s*(["\'])(.*?)\1', re.IGNORECASE)
src_re = re.compile(r'<script[^>]+src\s*=\s*(["\'])(.*?)\1', re.IGNORECASE)
img_src_re = re.compile(r'<img[^>]+src\s*=\s*(["\'])(.*?)\1', re.IGNORECASE)
anchor_re = re.compile(r'<a\s+[^>]*target\s*=\s*(["\"])_blank\1[^>]*>', re.IGNORECASE)

for fn in html_files:
    text = fn.read_text(encoding='utf-8')
    # images without alt or empty alt
    for m in img_re.finditer(text):
        tag = m.group(0)
        attrs = dict((a.lower(), v) for a, q, v in attr_re.findall(tag))
        if 'alt' not in attrs or attrs.get('alt','').strip()=='' :
            # attempt to find src
            srcm = img_src_re.search(tag)
            src = srcm.group(2) if srcm else ''
            img_no_alt.append((str(fn.relative_to(root)), src.strip()))
    # link href assets
    for lm in link_href_re.finditer(text):
        href = lm.group(2).strip()
        if href.startswith('http') or href.startswith('//'):
            # check for placeholder integrity
            if 'integrity' in lm.group(0) and 'your' in lm.group(0).lower():
                placeholder_integrity.append((str(fn.relative_to(root)), href))
            continue
        # local asset
        asset_path = (fn.parent / href).resolve()
        if not asset_path.exists():
            missing_assets.append((str(fn.relative_to(root)), href))
    # script src
    for sm in src_re.finditer(text):
        src = sm.group(2).strip()
        if src.startswith('http') or src.startswith('//'):
            # placeholder integrity check
            if 'integrity' in sm.group(0) and 'your' in sm.group(0).lower():
                placeholder_integrity.append((str(fn.relative_to(root)), src))
            continue
        asset_path = (fn.parent / src).resolve()
        if not asset_path.exists():
            missing_assets.append((str(fn.relative_to(root)), src))
    # anchors with target blank but missing rel
    for am in anchor_re.finditer(text):
        tag = am.group(0)
        if re.search(r'\brel\s*=\s*(["\'])(.*?)\1', tag, re.IGNORECASE):
            continue
        # find href for context
        hrefm = re.search(r'href\s*=\s*(["\'])(.*?)\1', tag, re.IGNORECASE)
        href = hrefm.group(2) if hrefm else ''
        blank_rel.append((str(fn.relative_to(root)), href))

# Deduplicate
img_no_alt = list(dict.fromkeys(img_no_alt))
missing_assets = list(dict.fromkeys(missing_assets))
blank_rel = list(dict.fromkeys(blank_rel))
placeholder_integrity = list(dict.fromkeys(placeholder_integrity))

print('Scan root:', root)
print('Total HTML files scanned:', len(html_files))
print()
print('Images missing alt (file, src) count:', len(img_no_alt))
for f,s in img_no_alt[:200]:
    print('-', f, '->', s)
print()
print('Missing local assets (file, href/src) count:', len(missing_assets))
for f,p in missing_assets[:200]:
    print('-', f, '->', p)
print()
print('Anchors target="_blank" missing rel count:', len(blank_rel))
for f,h in blank_rel[:200]:
    print('-', f, '->', h)
print()
print('Placeholder integrity attributes found count:', len(placeholder_integrity))
for f,u in placeholder_integrity[:200]:
    print('-', f, '->', u)

# Exit code 0
