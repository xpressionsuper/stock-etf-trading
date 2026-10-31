import json, sys
d = json.load(open(sys.argv[1]))
out = sys.argv[2]
c = [x["close"] for x in d]
sma = lambda n, i: sum(c[i-n+1:i+1]) / n
N = 130
base = len(d) - N
win = d[base:]

# ---------- hero chart ----------
W, H, L, R, T, B = 1000, 380, 44, 16, 18, 30
lo, hi = 260, 410
X = lambda k: L + (W-L-R) * k / (N-1)
Y = lambda p: T + (H-T-B) * (hi-p) / (hi-lo)
pts = lambda f: " ".join(f"{X(k):.1f},{Y(f(base+k)):.1f}" for k in range(N))
g = [f'<svg id="hc" tabindex="0" viewBox="0 0 {W} {H}" role="img" aria-label="GOOG 최근 130거래일 종가 차트. 좌우 화살표 키로 날짜별 종가를 확인합니다">']
for p in range(275, 410, 25):
    g.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(p):.1f}" y2="{Y(p):.1f}" class="h-grid"/><text x="{L-8}" y="{Y(p)+4:.1f}" class="h-ax" text-anchor="end">{p}</text>')
seen = set()
for k, x in enumerate(win):
    m = x["date"][5:7]
    if m not in seen and k > 2:
        g.append(f'<text x="{X(k):.1f}" y="{H-8}" class="h-ax" text-anchor="middle">{int(m)}월</text>')
    seen.add(m)
g.append(f'<rect x="{L}" width="{W-L-R}" y="{Y(276):.1f}" height="{Y(271)-Y(276):.1f}" class="h-sup"/>')
g.append(f'<text x="{X(46):.1f}" y="{Y(276)-8:.1f}" class="h-lab h-g">지지대 271–276 · 2025-11, 2026-03 저점에 이어 세 번째 시험</text>')
gx = X(N-2) - (X(1)-X(0))/2
g.append(f'<rect x="{gx:.1f}" width="{W-R-gx:.1f}" y="{Y(319.68):.1f}" height="{Y(286.43)-Y(319.68):.1f}" class="h-gap"/>')
g.append(f'<text x="{gx-8:.1f}" y="{Y(303):.1f}" class="h-lab h-r" text-anchor="end">미체결 갭 286.4–319.7</text>')
g.append(f'<polyline points="{pts(lambda i: sma(200, i))}" class="h-ma200"/>')
g.append(f'<polyline points="{pts(lambda i: sma(50, i))}" class="h-ma50"/>')
g.append(f'<polyline points="{pts(lambda i: c[i])}" class="h-px"/>')
g.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(287):.1f}" y2="{Y(287):.1f}" class="h-trig"/>')
g.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(268.5):.1f}" y2="{Y(268.5):.1f}" class="h-stop"/>')
g.append(f'<text x="{gx-8:.1f}" y="{Y(287)-6:.1f}" class="h-lab h-g" text-anchor="end">매수 트리거 287.00</text>')
g.append(f'<text x="{gx-8:.1f}" y="{Y(268.5)+15:.1f}" class="h-lab h-r" text-anchor="end">손절 268.50</text>')
g.append(f'<line id="hx" x1="0" x2="0" y1="{T}" y2="{H-B}" class="h-cross" visibility="hidden"/>')
g.append(f'<circle id="hd" cx="{X(N-1):.1f}" cy="{Y(c[-1]):.1f}" r="5" class="h-end"/>')
g.append(f'<rect x="{L}" y="{T}" width="{W-L-R}" height="{H-T-B}" fill="transparent" id="hz"/>')
g.append('</svg>')
hero_svg = "".join(g)
series = json.dumps([[x["date"], round(x["close"], 2)] for x in win])
geom = json.dumps(dict(W=W, L=L, R=R, T=T, B=B, H=H, lo=lo, hi=hi, N=N))

# ---------- price ladder ----------
LW, LH, lt, lb = 520, 560, 20, 20
plo, phi = 240, 345
LY = lambda p: lt + (LH-lt-lb) * (phi-p) / (phi-plo)
ax = 112  # axis x
lad = [f'<svg viewBox="0 0 {LW} {LH}" role="img" aria-label="가격 사다리: 손절 268.50, 매수 287.00, 목표 314와 320, 주요 지지와 저항">']
lad.append(f'<rect x="{ax-14}" width="28" y="{LY(287):.1f}" height="{LY(268.5)-LY(287):.1f}" class="l-risk"/>')
lad.append(f'<rect x="{ax-14}" width="28" y="{LY(320):.1f}" height="{LY(287)-LY(320):.1f}" class="l-rew"/>')
lad.append(f'<line x1="{ax}" x2="{ax}" y1="{lt}" y2="{LH-lb}" class="l-axis"/>')
for p in range(240, 346, 10):
    lad.append(f'<line x1="{ax-4}" x2="{ax+4}" y1="{LY(p):.1f}" y2="{LY(p):.1f}" class="l-tick"/><text x="{ax-22}" y="{LY(p)+4:.1f}" class="l-ax" text-anchor="end">{p}</text>')
def band(a, b, cls):
    lad.append(f'<rect x="{ax+18}" width="10" y="{LY(b):.1f}" height="{max(LY(a)-LY(b),2):.1f}" class="{cls}"/>')
def level(p, label, sub, cls, y=None):
    yy = LY(p) if y is None else y
    lad.append(f'<line x1="{ax-14}" x2="{ax+34}" y1="{LY(p):.1f}" y2="{LY(p):.1f}" class="l-lv {cls}"/>')
    lad.append(f'<text x="{ax+44}" y="{yy+4:.1f}" class="l-lab {cls}"><tspan class="l-p">{label}</tspan><tspan dx="10" class="l-sub">{sub}</tspan></text>')
band(335.7, 338.7, "l-b-r"); level(337.2, "335.7–338.7", "50·200일선 밀집", "c-r")
level(320, "320.00", "목표 2 · 갭 상단", "c-g")
level(314, "314.00", "목표 1 · 절반 익절", "c-g")
level(287, "287.00", "매수 트리거", "c-a")
level(278.22, "278.22", "10/30 종가", "c-f")
band(271, 276, "l-b-g"); level(273.5, "271–276", "이중 바닥 지지대", "c-g")
level(268.5, "268.50", "손절", "c-r", y=LY(268.5)+8)
band(245, 255, "l-b-g"); level(250, "245–255", "다음 지지 (근사)", "c-m")
lad.append(f'<text x="{ax-58}" y="{(LY(287)+LY(268.5))/2+4:.1f}" class="l-r" text-anchor="end">-1R</text>')
lad.append(f'<text x="{ax-58}" y="{(LY(320)+LY(287))/2+4:.1f}" class="l-w" text-anchor="end">+1.78R</text>')
lad.append(f'<circle cx="{ax}" cy="{LY(278.22):.1f}" r="5" class="l-now"/>')
lad.append('</svg>')
ladder = "".join(lad)

# ---------- macro bars ----------
comps = [("시장 집중도", "RSP/SPY", 50, "이동평균 수렴, 방향 미정"),
         ("수익률 곡선", "10Y–2Y", 50, "스티프닝 (SHY/TLT 대용치)"),
         ("신용", "HYG/LQD", 43, "신용 조건 조이는 중"),
         ("규모", "IWM/SPY", 69, "대형주 우위로 이동"),
         ("주식·채권", "SPY/TLT", 10, "상관 안정"),
         ("섹터 로테이션", "XLY/XLP", 60, "방어주 쪽으로 이동")]
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
