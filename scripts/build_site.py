"""reports/html/*.html 을 site/ 로 복사하고 최신순 목록 페이지(index.html)를 만든다.

GitHub Actions(pages.yml)에서 실행되며, 로컬에서도 `py scripts/build_site.py`로 미리 볼 수 있다.
"""
import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "reports" / "html"
OUT = ROOT / "site"
NAME = re.compile(r"^(?P<ticker>[A-Z0-9.\-]+)_(?P<kind>[a-z]+)_(?P<date>\d{4}-\d{2}-\d{2})\.html$")


def text_of(pattern, src):
    m = re.search(pattern, src, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""


def collect():
    rows = []
    for f in SRC.glob("*.html"):
        m = NAME.match(f.name)
        if not m:
            continue
        src = f.read_text(encoding="utf-8")
        rows.append(dict(file=f.name, **m.groupdict(),
                         title=text_of(r"<h1[^>]*>(.*?)</h1>", src) or text_of(r"<title>(.*?)</title>", src)))
    return sorted(rows, key=lambda r: (r["date"], r["ticker"]), reverse=True)


SKELETON = ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
            'body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style>'
            '</head><body>\n')

PAGE = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>페이퍼 트레이딩 리포트</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@800&family=IBM+Plex+Sans+KR:wght@400;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
:root{--bg:#eef1f5;--surface:#fff;--ink:#0f1a2a;--muted:#536075;--line:#d3dae4;--accent:#1f4f8a;
  --h-bg:#0c1522;--h-bg2:#13233a;--h-fg:#eef2f8;--h-muted:#9aa8bd;
  --display:"Nanum Myeongjo","Batang",serif;--sans:"IBM Plex Sans KR","Malgun Gothic",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Consolas,monospace}
@media (prefers-color-scheme:dark){:root{--bg:#0a0f17;--surface:#111a26;--ink:#e7ecf3;--muted:#95a2b6;--line:#223042;--accent:#86b2ee;--h-bg:#070c14;--h-bg2:#0f1c2f;color-scheme:dark}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6;word-break:keep-all}
.in{max-width:820px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
header{background:radial-gradient(120% 90% at 85% 0%,var(--h-bg2),var(--h-bg) 60%);color:var(--h-fg)}
header .in{padding-block:calc(40px + env(safe-area-inset-top,0px)) 32px}
h1{font-family:var(--display);font-weight:800;font-size:clamp(1.7rem,6vw,2.4rem);margin:0;line-height:1.25}
header p{color:var(--h-muted);margin:10px 0 0;font-size:.92rem}
ol{list-style:none;margin:0;padding:28px 0 48px;display:grid;gap:10px}
a{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;align-items:baseline;padding:16px 18px;background:var(--surface);
  border:1px solid var(--line);border-radius:10px;color:inherit;text-decoration:none}
a:hover,a:focus-visible{border-color:var(--accent);outline:none}
.t{font-family:var(--mono);font-weight:500;font-size:1.05rem}
.d{font-family:var(--mono);font-size:.85rem;color:var(--muted);text-align:right}
.h{grid-column:1/-1;font-size:.95rem}
.empty{color:var(--muted);padding:28px 0}
</style></head><body>
<header><div class="in"><h1>페이퍼 트레이딩 리포트</h1>
<p>Plan → Trade → Record 루프로 만든 종목 분석 {count}건 · 최신순. 연습용이며 투자 권유가 아닙니다.</p></div></header>
<main class="in">{body}</main>
</body></html>
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    rows = collect()
    for r in rows:
        src = (SRC / r["file"]).read_text(encoding="utf-8")
        if not src.lstrip().lower().startswith("<!doctype"):
            src = SKELETON + src + "\n</body></html>\n"  # 아티팩트용 본문에는 head가 없다
        (OUT / r["file"]).write_text(src, encoding="utf-8")
    items = "".join(
        f'<li><a href="{html.escape(r["file"])}"><span class="t">{html.escape(r["ticker"])}</span>'
        f'<span class="d">{r["date"]}</span><span class="h">{html.escape(r["title"])}</span></a></li>'
        for r in rows)
    body = f"<ol>{items}</ol>" if rows else '<p class="empty">아직 리포트가 없습니다.</p>'
    (OUT / "index.html").write_text(PAGE.replace("{count}", str(len(rows))).replace("{body}", body), encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    print(f"site/: {len(rows)} reports + index.html")


if __name__ == "__main__":
    main()
