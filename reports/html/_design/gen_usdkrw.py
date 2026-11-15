import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
out = sys.argv[2]
c = [x["close"] for x in d]
sma = lambda n, i: sum(c[i-n+1:i+1]) / n
N = 130
base = len(d) - N
win = d[base:]

# ---------- hero chart ----------
W, H, L, R, T, B = 1000, 380, 54, 16, 18, 30
lo, hi = 1300, 1480
X = lambda k: L + (W-L-R) * k / (N-1)
Y = lambda p: T + (H-T-B) * (hi-p) / (hi-lo)
pts = lambda f: " ".join(f"{X(k):.1f},{Y(f(base+k)):.1f}" for k in range(N))
g = [f'<svg id="hc" tabindex="0" viewBox="0 0 {W} {H}" role="img" aria-label="USD/KRW 최근 130거래일 종가 차트. 좌우 화살표 키로 날짜별 종가를 확인합니다">']
for p in range(1300, 1481, 30):
    g.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(p):.1f}" y2="{Y(p):.1f}" class="h-grid"/><text x="{L-8}" y="{Y(p)+4:.1f}" class="h-ax" text-anchor="end">{p}</text>')
seen = set()
for k, x in enumerate(win):
    m = x["date"][5:7]
    if m not in seen and k > 2:
        g.append(f'<text x="{X(k):.1f}" y="{H-8}" class="h-ax" text-anchor="middle">{int(m)}월</text>')
    seen.add(m)
# support band 1321-1335 (double-bottom zone)
g.append(f'<rect x="{L}" width="{W-L-R}" y="{Y(1335):.1f}" height="{Y(1321)-Y(1335):.1f}" class="h-sup"/>')
g.append(f'<text x="{X(46):.1f}" y="{Y(1335)-8:.1f}" class="h-lab h-g">지지 구간 1,321–1,335 · 10/26 저점 1,321.76</text>')
# resistance zone around MA60 1349
g.append(f'<rect x="{L}" width="{W-L-R}" y="{Y(1364):.1f}" height="{Y(1349)-Y(1364):.1f}" class="h-gap"/>')
g.append(f'<text x="{X(70):.1f}" y="{Y(1364)-6:.1f}" class="h-lab h-r">저항 1,349–1,364 · MA60 + 11/6 비석형 고점</text>')
g.append(f'<polyline points="{pts(lambda i: sma(200, i))}" class="h-ma200"/>')
g.append(f'<polyline points="{pts(lambda i: sma(50, i))}" class="h-ma50"/>')
g.append(f'<polyline points="{pts(lambda i: c[i])}" class="h-px"/>')
# short trigger & stop
g.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(1349):.1f}" y2="{Y(1349):.1f}" class="h-trig"/>')
g.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(1355):.1f}" y2="{Y(1355):.1f}" class="h-stop"/>')
g.append(f'<text x="{W-R-8}" y="{Y(1349)-6:.1f}" class="h-lab h-g" text-anchor="end">숏 트리거 1,349</text>')
g.append(f'<text x="{W-R-8}" y="{Y(1355)+15:.1f}" class="h-lab h-r" text-anchor="end">숏 손절 1,355 종가</text>')
g.append(f'<line id="hx" x1="0" x2="0" y1="{T}" y2="{H-B}" class="h-cross" visibility="hidden"/>')
g.append(f'<circle id="hd" cx="{X(N-1):.1f}" cy="{Y(c[-1]):.1f}" r="5" class="h-end"/>')
g.append(f'<rect x="{L}" y="{T}" width="{W-L-R}" height="{H-T-B}" fill="transparent" id="hz"/>')
g.append('</svg>')
hero_svg = "".join(g)
series = json.dumps([[x["date"], round(x["close"], 2)] for x in win])
geom = json.dumps(dict(W=W, L=L, R=R, T=T, B=B, H=H, lo=lo, hi=hi, N=N))

# ---------- price ladder ----------
LW, LH, lt, lb = 520, 560, 20, 20
plo, phi = 1290, 1460
LY = lambda p: lt + (LH-lt-lb) * (phi-p) / (phi-plo)
ax = 118
lad = [f'<svg viewBox="0 0 {LW} {LH}" role="img" aria-label="가격 사다리: 숏 손절 1355, 숏 트리거 1349, 목표 1322와 1300, 주요 저항">']
# risk (red) 1349->1355, reward (green) 1349->1300
lad.append(f'<rect x="{ax-14}" width="28" y="{LY(1355):.1f}" height="{LY(1349)-LY(1355):.1f}" class="l-risk"/>')
lad.append(f'<rect x="{ax-14}" width="28" y="{LY(1349):.1f}" height="{LY(1300)-LY(1349):.1f}" class="l-rew"/>')
lad.append(f'<line x1="{ax}" x2="{ax}" y1="{lt}" y2="{LH-lb}" class="l-axis"/>')
for p in range(1290, 1461, 20):
    lad.append(f'<line x1="{ax-4}" x2="{ax+4}" y1="{LY(p):.1f}" y2="{LY(p):.1f}" class="l-tick"/><text x="{ax-22}" y="{LY(p)+4:.1f}" class="l-ax" text-anchor="end">{p:,}</text>')
def band(a, b, cls):
    lad.append(f'<rect x="{ax+18}" width="10" y="{LY(b):.1f}" height="{max(LY(a)-LY(b),2):.1f}" class="{cls}"/>')
def level(p, label, sub, cls, y=None):
    yy = LY(p) if y is None else y
    lad.append(f'<line x1="{ax-14}" x2="{ax+34}" y1="{LY(p):.1f}" y2="{LY(p):.1f}" class="l-lv {cls}"/>')
    lad.append(f'<text x="{ax+44}" y="{yy+4:.1f}" class="l-lab {cls}"><tspan class="l-p">{label}</tspan><tspan dx="10" class="l-sub">{sub}</tspan></text>')
band(1417, 1441, "l-b-r"); level(1429, "1,417–1,441", "MA120 · MA200 장기 저항", "c-r")
level(1364, "1,364.72", "11/6 비석형 고점 (강저항)", "c-r")
level(1355, "1,355.00", "숏 손절 (종가)", "c-r", y=LY(1355)-6)
level(1349, "1,349.35", "숏 트리거 · MA60", "c-a")
level(1336.2, "1,336.20", "현재가 (11/15)", "c-f")
band(1321, 1335, "l-b-g"); level(1328, "1,321–1,335", "지지 (MA5·MA20 수렴)", "c-g")
level(1322, "1,322.00", "목표 1 · 52주 저점 재시험", "c-g")
level(1300, "1,300.00", "목표 2 · 심리적 지지", "c-g", y=LY(1300)+12)
lad.append(f'<text x="{ax-58}" y="{(LY(1355)+LY(1349))/2+4:.1f}" class="l-r" text-anchor="end">-1R</text>')
lad.append(f'<text x="{ax-58}" y="{(LY(1349)+LY(1300))/2+4:.1f}" class="l-w" text-anchor="end">+8.2R</text>')
lad.append(f'<circle cx="{ax}" cy="{LY(1336.2):.1f}" r="5" class="l-now"/>')
lad.append('</svg>')
ladder = "".join(lad)

# ---------- macro bars (FX/USD context) ----------
comps = [("달러 사이클", "DXY 1y", 30, "9월 피크 이후 완만한 하락"),
         ("한미 금리차", "US10Y – KR10Y", 35, "스프레드 축소 중 (원화 우호)"),
         ("리스크 선호", "KOSPI 1m", 60, "아시아 위험자산 반등"),
         ("원자재", "유가 1m", 45, "WTI 60~65 박스 (중립)"),
         ("자본 유입", "외인 순매수", 55, "삼성전자·SK하이닉스 중심 유입"),
         ("매크로 국면", "macro-regime", 47, "Transitional (46.8) — 국면 전환 중")]
macro_rows = "".join(
    f'<div class="mrow"><div class="mname"><b>{a}</b><span>{b}</span></div>'
    f'<div class="mtrack"><i style="width:{s}%"></i></div><div class="mval num">{s}</div><div class="mnote">{n}</div></div>'
    for a, b, s, n in comps)

html = open(sys.argv[3], encoding="utf-8").read()
for k, v in {"{{HERO}}": hero_svg, "{{LADDER}}": ladder, "{{MACRO}}": macro_rows,
             "{{SERIES}}": series, "{{GEOM}}": geom}.items():
    html = html.replace(k, v)
open(out, "w", encoding="utf-8").write(html)
print("ok", len(html))
