from playwright.sync_api import sync_playwright
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out_dir = root / 'reports' / 'screenshots'
out_dir.mkdir(parents=True, exist_ok=True)

pages = [
    'index.html',
    'Data-engineering.html',
    'apache-spark.html',
    'deep-learning.html',
    'bootstrap.html',
    'flask.html',
    'machine-learning.html',
    'data_etl_tools.html'
]

base = 'http://127.0.0.1:8000/'

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width':1280, 'height':900})
    page = context.new_page()
    for pth in pages:
        url = base + pth
        try:
            page.goto(url, timeout=30000)
            page.wait_for_load_state('networkidle', timeout=10000)
            filename = out_dir / (pth.replace('/', '_'))
            page.screenshot(path=str(filename)+'.png', full_page=True)
            print('Saved', filename.with_suffix('.png'))
        except Exception as e:
            print('Failed', pth, e)
    browser.close()
