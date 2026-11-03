import sys, re, markdown, pathlib
from playwright.sync_api import sync_playwright
src, out, fontdir = map(pathlib.Path, sys.argv[1:4])
md = src.read_text()
title = re.search(r'^# (.+)$', md, re.M).group(1)
sub = re.search(r'^> (.+)$', md, re.M).group(1)
# drop the title + blockquote; we render our own title page
body_md = md.split('\n---\n', 1)[1]
body = markdown.markdown(body_md)
body = body.replace('<hr />', '<p class="sep">＊</p>')
html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>
@font-face{{font-family:NM;src:url('{(fontdir/'NanumMyeongjo-Regular.ttf').as_uri()}');}}
@font-face{{font-family:NM;font-weight:bold;src:url('{(fontdir/'NanumMyeongjo-Bold.ttf').as_uri()}');}}
@page{{size:A5;margin:20mm 17mm 20mm 17mm;
 @bottom-center{{content:counter(page);font-family:NM;font-size:8.5pt;color:#777}}}}
@page:first{{@bottom-center{{content:none}}}}
body{{font-family:NM,serif;font-size:10pt;line-height:1.85;color:#1a1a1a;word-break:keep-all;}}
p{{margin:0;text-indent:1em;text-align:justify}}
p + p{{margin-top:0.25em}}
h2{{page-break-before:always;font-size:14pt;font-weight:bold;margin:18mm 0 10mm;text-align:left;letter-spacing:0.02em}}
.sep{{text-align:center;text-indent:0;margin:1.2em 0;color:#888}}
h2 + .sep{{display:none}}
.cover{{height:165mm;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}}
.cover h1{{font-size:22pt;margin:0 0 8mm;letter-spacing:0.04em}}
.cover .sub{{max-width:80mm;font-size:9.5pt;color:#555;text-indent:0;line-height:1.7;text-align:center}}
em{{font-style:normal}}
</style></head><body>
<div class="cover"><h1>{title}</h1>
<p class="sub">{sub}</p></div>
{body}</body></html>"""
h = out.with_suffix('.html'); h.write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium') if pathlib.Path('/opt/pw-browsers/chromium').is_file() else p.chromium.launch()
    pg = b.new_page(); pg.goto(h.as_uri()); pg.wait_for_timeout(500)
    pg.pdf(path=str(out), prefer_css_page_size=True, display_header_footer=False)
    b.close()
