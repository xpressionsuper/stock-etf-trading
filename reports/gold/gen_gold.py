import json, sys
# 금 현물 근사 버전: reports/html/_design/gen_report.py와 같은 구조, 수치·문구만 금으로 교체
d = json.load(open(sys.argv[1]))
out = sys.argv[2]
# ponytail: 현물 일봉을 무료로 못 받아 GC=F에서 최근 베이시스(선물 - 현물 ≈ 6)를 일괄 차감. 현물 소스가 생기면 그 데이터로 교체
BASIS = 6.0
for x in d:
    for f in ("open", "high", "low", "close"):
        x[f] -= BASIS
c = [x["close"] for x in d]
sma = lambda n, i: sum(c[i-n+1:i+1]) / n
N = 130
base = len(d) - N
win = d[base:]

# 판단 카드 가격 (현물 기준)
E, S, T1, T2 = 3780, 3700, 3880, 3950

# ---------- hero chart ----------
W, H, L, R, T, B = 1000, 380, 48, 16, 18, 30
lo, hi = 3660, 4860
X = lambda k: L + (W-L-R) * k / (N-1)
Y = lambda p: T + (H-T-B) * (hi-p) / (hi-lo)
pts = lambda f: " ".join(f"{X(k):.1f},{Y(f(base+k)):.1f}" for k in range(N))
g = [f'<svg id="hc" tabindex="0" viewBox="0 0 {W} {H}" role="img" aria-label="금 현물(근사) 최근 130거래일 종가 차트. 좌우 화살표 키로 날짜별 종가를 확인합니다">']
for p in range(3750, 4801, 150):
    g.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(p):.1f}" y2="{Y(p):.1f}" class="h-grid"/><text x="{L-8}" y="{Y(p)+4:.1f}" class="h-ax" text-anchor="end">{p:,}</text>')
seen = set()
for k, x in enumerate(win):
    m = x["date"][5:7]
    if m not in seen and k > 2:
        g.append(f'<text x="{X(k):.1f}" y="{H-8}" class="h-ax" text-anchor="middle">{int(m)}월</text>')
    seen.add(m)
# 다시 깨진 지지대 3949–3994 → 저항
g.append(f'<rect x="{L}" width="{W-L-R}" y="{Y(3994):.1f}" height="{Y(3949)-Y(3994):.1f}" class="h-gap"/>')
g.append(f'<text x="{X(58):.1f}" y="{Y(3994)-7:.1f}" class="h-lab h-r">다시 깨진 지지대 3,949–3,994 · 이제 저항</text>')
# 매수 대기 구간 3750–3800 (2025년 9~10월 돌파 구간)
g.append(f'<rect x="{L}" width="{W-L-R}" y="{Y(3800):.1f}" height="{Y(3750)-Y(3800):.1f}" class="h-sup"/>')
g.append(f'<text x="{X(58):.1f}" y="{Y(3750)+16:.1f}" class="h-lab h-g">매수 대기 3,750–3,800 · 2025년 9~10월 돌파 구간</text>')
g.append(f'<polyline points="{pts(lambda i: sma(200, i))}" class="h-ma200"/>')
g.append(f'<polyline points="{pts(lambda i: sma(50, i))}" class="h-ma50"/>')
g.append(f'<polyline points="{pts(lambda i: c[i])}" class="h-px"/>')
g.append(f'<line x1="{X(N-30):.1f}" x2="{W-R}" y1="{Y(S):.1f}" y2="{Y(S):.1f}" class="h-stop"/>')
g.append(f'<text x="{X(N-1)-14:.1f}" y="{Y(S)+16:.1f}" class="h-lab h-r" text-anchor="end">손절 {S:,}</text>')
lo_k = min(range(N), key=lambda k: win[k]["low"])
g.append(f'<text x="{X(lo_k)-10:.1f}" y="{Y(win[lo_k]["low"])+4:.1f}" class="h-lab h-r" text-anchor="end">11/12 저점 3,852</text>')
g.append(f'<line id="hx" x1="0" x2="0" y1="{T}" y2="{H-B}" class="h-cross" visibility="hidden"/>')
g.append(f'<circle id="hd" cx="{X(N-1):.1f}" cy="{Y(c[-1]):.1f}" r="5" class="h-end"/>')
g.append(f'<rect x="{L}" y="{T}" width="{W-L-R}" height="{H-T-B}" fill="transparent" id="hz"/>')
g.append('</svg>')
hero_svg = "".join(g)
series = json.dumps([[x["date"], round(x["close"], 1)] for x in win])
geom = json.dumps(dict(W=W, L=L, R=R, T=T, B=B, H=H, lo=lo, hi=hi, N=N))

# ---------- price ladder (금 현물 가격) ----------
LW, LH, lt, lb = 520, 600, 20, 20
plo, phi = 3550, 4200
LY = lambda p: lt + (LH-lt-lb) * (phi-p) / (phi-plo)
ax = 112
lad = [f'<svg viewBox="0 0 {LW} {LH}" role="img" aria-label="금 현물 가격 사다리: 매수 {E:,}, 손절 {S:,}, 목표 {T1:,}과 {T2:,}, 주요 지지와 저항">']
lad.append(f'<rect x="{ax-14}" width="28" y="{LY(E):.1f}" height="{LY(S)-LY(E):.1f}" class="l-risk"/>')
lad.append(f'<rect x="{ax-14}" width="28" y="{LY(T2):.1f}" height="{LY(E)-LY(T2):.1f}" class="l-rew"/>')
lad.append(f'<line x1="{ax}" x2="{ax}" y1="{lt}" y2="{LH-lb}" class="l-axis"/>')
for p in range(3600, 4201, 100):
    lad.append(f'<line x1="{ax-4}" x2="{ax+4}" y1="{LY(p):.1f}" y2="{LY(p):.1f}" class="l-tick"/><text x="{ax-22}" y="{LY(p)+4:.1f}" class="l-ax" text-anchor="end">{p:,}</text>')
def band(a, b, cls):
    lad.append(f'<rect x="{ax+18}" width="10" y="{LY(b):.1f}" height="{max(LY(a)-LY(b),2):.1f}" class="{cls}"/>')
def level(p, label, sub, cls, dy=0):
    lad.append(f'<line x1="{ax-14}" x2="{ax+34}" y1="{LY(p):.1f}" y2="{LY(p):.1f}" class="l-lv {cls}"/>')
    lad.append(f'<text x="{ax+44}" y="{LY(p)+4+dy:.1f}" class="l-lab {cls}"><tspan class="l-p">{label}</tspan><tspan dx="10" class="l-sub">{sub}</tspan></text>')
band(4085, 4150, "l-b-r"); level(4118, "4,085–4,150", "2차 저항 · 11/9 고점", "c-r")
level(4029, "4,029", "20일선", "c-m")
band(3949, 3994, "l-b-r"); level(3972, "3,949–3,994", "1차 저항 (다시 깨진 지지대)", "c-r", -6)
level(T2, f"{T2:,}", "목표 2 · 저항 아래", "c-g", 10)
level(T1, f"{T1:,}", "목표 1 · 11/13 종가 부근", "c-g", -4)
level(3852, "3,852", "11/12 저점", "c-f", 10)
band(3750, 3800, "l-b-g"); level(E, f"{E:,}", "매수 (반전일 확인 후)", "c-a", -6)
level(3750, "3,750", "매수 구간 하단", "c-g", 8)
level(S, f"{S:,}", "손절", "c-r", 6)
band(3590, 3610, "l-b-g"); level(3600, "3,600", "다음 지지 (전망치)", "c-m")
lad.append(f'<text x="{ax-58}" y="{(LY(E)+LY(S))/2+4:.1f}" class="l-r" text-anchor="end">-1R</text>')
lad.append(f'<text x="{ax-58}" y="{(LY(T2)+LY(E))/2+4:.1f}" class="l-w" text-anchor="end">+{(T2-E)/(E-S):.2f}R</text>')
lad.append(f'<circle cx="{ax}" cy="{LY(c[-1]):.1f}" r="5" class="l-now"/>')
lad.append('</svg>')
ladder = "".join(lad)

# ---------- macro bars (2026-11-14 실행분) ----------
comps = [("시장 집중도", "RSP/SPY", 60, "확산 확정, 이번 달 골든크로스"),
         ("수익률 곡선", "10Y–2Y", 50, "플래트닝"),
         ("신용", "HYG/LQD", 40, "신용 조건 조이는 중"),
         ("규모", "IWM/SPY", 52, "대형주 우위 약해지는 중"),
         ("주식·채권", "SPY/TLT", 30, "리스크 온, 국면과 반대 신호"),
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
print("ok", len(html), "last", round(c[-1], 1), "sma20/50/200", round(sma(20, len(c)-1)), round(sma(50, len(c)-1)), round(sma(200, len(c)-1)))
