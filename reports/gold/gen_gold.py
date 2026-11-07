import json, sys
# 금(GC=F) 버전: reports/html/_design/gen_report.py와 같은 구조, 수치·문구만 금으로 교체
d = json.load(open(sys.argv[1]))
out = sys.argv[2]
c = [x["close"] for x in d]
sma = lambda n, i: sum(c[i-n+1:i+1]) / n
N = 130
base = len(d) - N
win = d[base:]
K = 10.95  # 금 / GLD 가격 비율 (최근 5일 평균 근사)

# ---------- hero chart ----------
W, H, L, R, T, B = 1000, 380, 48, 16, 18, 30
lo, hi = 3780, 4860
X = lambda k: L + (W-L-R) * k / (N-1)
Y = lambda p: T + (H-T-B) * (hi-p) / (hi-lo)
pts = lambda f: " ".join(f"{X(k):.1f},{Y(f(base+k)):.1f}" for k in range(N))
g = [f'<svg id="hc" tabindex="0" viewBox="0 0 {W} {H}" role="img" aria-label="금 선물 최근 130거래일 종가 차트. 좌우 화살표 키로 날짜별 종가를 확인합니다">']
for p in range(3900, 4801, 150):
    g.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(p):.1f}" y2="{Y(p):.1f}" class="h-grid"/><text x="{L-8}" y="{Y(p)+4:.1f}" class="h-ax" text-anchor="end">{p:,}</text>')
seen = set()
for k, x in enumerate(win):
    m = x["date"][5:7]
    if m not in seen and k > 2:
        g.append(f'<text x="{X(k):.1f}" y="{H-8}" class="h-ax" text-anchor="middle">{int(m)}월</text>')
    seen.add(m)
# 되찾은 지지대 3955–4000 (6/30, 7/17, 7/29 저점)
g.append(f'<rect x="{L}" width="{W-L-R}" y="{Y(4000):.1f}" height="{Y(3955)-Y(4000):.1f}" class="h-sup"/>')
g.append(f'<text x="{X(58):.1f}" y="{Y(3955)+16:.1f}" class="h-lab h-g">되찾은 지지대 3,955–4,000 · 6/30, 7/17, 7/29 저점</text>')
# 저항 4091–4156
g.append(f'<rect x="{L}" width="{W-L-R}" y="{Y(4156):.1f}" height="{Y(4091)-Y(4156):.1f}" class="h-gap"/>')
g.append(f'<text x="{X(80):.1f}" y="{Y(4156)-7:.1f}" class="h-lab h-r">저항 4,091–4,156</text>')
g.append(f'<polyline points="{pts(lambda i: sma(200, i))}" class="h-ma200"/>')
g.append(f'<polyline points="{pts(lambda i: sma(50, i))}" class="h-ma50"/>')
g.append(f'<polyline points="{pts(lambda i: c[i])}" class="h-px"/>')
g.append(f'<line x1="{X(N-30):.1f}" x2="{W-R}" y1="{Y(353.5*K):.1f}" y2="{Y(353.5*K):.1f}" class="h-stop"/>')
g.append(f'<text x="{X(N-1)-14:.1f}" y="{Y(353.5*K)+16:.1f}" class="h-lab h-r" text-anchor="end">GLD 손절 ≈ 3,871</text>')
lo_k = min(range(N), key=lambda k: win[k]["low"])
g.append(f'<text x="{X(lo_k):.1f}" y="{Y(win[lo_k]["low"])+36:.1f}" class="h-lab h-r" text-anchor="middle">10/30 저점 3,879</text>')
g.append(f'<line id="hx" x1="0" x2="0" y1="{T}" y2="{H-B}" class="h-cross" visibility="hidden"/>')
g.append(f'<circle id="hd" cx="{X(N-1):.1f}" cy="{Y(c[-1]):.1f}" r="5" class="h-end"/>')
g.append(f'<rect x="{L}" y="{T}" width="{W-L-R}" height="{H-T-B}" fill="transparent" id="hz"/>')
g.append('</svg>')
hero_svg = "".join(g)
series = json.dumps([[x["date"], round(x["close"], 1)] for x in win])
geom = json.dumps(dict(W=W, L=L, R=R, T=T, B=B, H=H, lo=lo, hi=hi, N=N))

# ---------- price ladder (금 가격, GLD 포지션을 금 가격으로 환산) ----------
LW, LH, lt, lb = 520, 600, 20, 20
plo, phi = 3700, 4400
LY = lambda p: lt + (LH-lt-lb) * (phi-p) / (phi-plo)
ax = 112
e, s, t1, t2 = 369.58*K, 353.5*K, 380*K, 390*K
lad = [f'<svg viewBox="0 0 {LW} {LH}" role="img" aria-label="금 가격 사다리: GLD 포지션 진입 약 4,047, 손절 약 3,871, 목표 약 4,161과 4,271, 주요 지지와 저항">']
lad.append(f'<rect x="{ax-14}" width="28" y="{LY(e):.1f}" height="{LY(s)-LY(e):.1f}" class="l-risk"/>')
lad.append(f'<rect x="{ax-14}" width="28" y="{LY(t2):.1f}" height="{LY(e)-LY(t2):.1f}" class="l-rew"/>')
lad.append(f'<line x1="{ax}" x2="{ax}" y1="{lt}" y2="{LH-lb}" class="l-axis"/>')
for p in range(3700, 4401, 100):
    lad.append(f'<line x1="{ax-4}" x2="{ax+4}" y1="{LY(p):.1f}" y2="{LY(p):.1f}" class="l-tick"/><text x="{ax-22}" y="{LY(p)+4:.1f}" class="l-ax" text-anchor="end">{p:,}</text>')
def band(a, b, cls):
    lad.append(f'<rect x="{ax+18}" width="10" y="{LY(b):.1f}" height="{max(LY(a)-LY(b),2):.1f}" class="{cls}"/>')
def level(p, label, sub, cls, dy=0):
    lad.append(f'<line x1="{ax-14}" x2="{ax+34}" y1="{LY(p):.1f}" y2="{LY(p):.1f}" class="l-lv {cls}"/>')
    lad.append(f'<text x="{ax+44}" y="{LY(p)+4+dy:.1f}" class="l-lab {cls}"><tspan class="l-p">{label}</tspan><tspan dx="10" class="l-sub">{sub}</tspan></text>')
level(4329, "4,329", "9/2 저점 · 그다음 저항", "c-m")
level(t2, f"{t2:,.0f}", "목표 2 · GLD 390", "c-g", -6)
band(4230, 4242, "l-b-r"); level(4236, "4,230–4,242", "50일선 · 10/12 고점", "c-r", 8)
level(t1, f"{t1:,.0f}", "목표 1 · GLD 380", "c-g", -8)
band(4091, 4156, "l-b-r"); level(4120, "4,091–4,156", "1차 저항", "c-r", 4)
level(4074.9, "4,074.9", "11/6 종가 (현물 ≈ 4,069)", "c-f", 6)
level(e, f"{e:,.0f}", "GLD 진입 369.58", "c-a", 10)
band(3955, 4000, "l-b-g"); level(3978, "3,955–4,000", "되찾은 지지대", "c-g", 6)
level(s, f"{s:,.0f}", "GLD 손절 353.50", "c-r", 12)
band(3750, 3850, "l-b-g"); level(3800, "3,750–3,850", "다음 지지 (2025-09)", "c-m")
lad.append(f'<text x="{ax-58}" y="{(LY(e)+LY(s))/2+4:.1f}" class="l-r" text-anchor="end">-1R</text>')
lad.append(f'<text x="{ax-58}" y="{(LY(t2)+LY(e))/2+4:.1f}" class="l-w" text-anchor="end">+1.27R</text>')
lad.append(f'<circle cx="{ax}" cy="{LY(4074.9):.1f}" r="5" class="l-now"/>')
lad.append('</svg>')
ladder = "".join(lad)

# ---------- macro bars (2026-11-07 실행분) ----------
comps = [("시장 집중도", "RSP/SPY", 70, "확산 확정, 이번 달 골든크로스"),
         ("수익률 곡선", "10Y–2Y", 50, "플래트닝"),
         ("신용", "HYG/LQD", 49, "신용 조건 조이는 중"),
         ("규모", "IWM/SPY", 45, "대형주 우위 약해지는 중"),
         ("주식·채권", "SPY/TLT", 52, "리스크 오프 쪽으로 이동"),
         ("섹터 로테이션", "XLY/XLP", 60, "방어주 선호 확정")]
macro_rows = "".join(
    f'<div class="mrow"><div class="mname"><b>{a}</b><span>{b}</span></div>'
    f'<div class="mtrack"><i style="width:{s_}%"></i></div><div class="mval num">{s_}</div><div class="mnote">{n}</div></div>'
    for a, b, s_, n in comps)

html = open(sys.argv[3], encoding="utf-8").read()
for k, v in {"{{HERO}}": hero_svg, "{{LADDER}}": ladder, "{{MACRO}}": macro_rows,
             "{{SERIES}}": series, "{{GEOM}}": geom}.items():
    html = html.replace(k, v)
open(out, "w", encoding="utf-8").write(html)
print("ok", len(html), round(e), round(s), round(t1), round(t2))
