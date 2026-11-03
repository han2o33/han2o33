import sys
from playwright.sync_api import sync_playwright
html,pdf,png=sys.argv[1:4]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg=b.new_page(viewport={'width':560,'height':794},device_scale_factor=3)
    pg.goto('file://'+html); pg.wait_for_timeout(500)
    pg.locator('.cover').screenshot(path=png)
    pg.pdf(path=pdf,prefer_css_page_size=True,print_background=True)
    b.close()
