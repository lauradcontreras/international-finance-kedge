"""Draws the payoff diagram on the slide "Why the payoff diagram is the whole
lesson" as inline SVG. The SVG is pasted into the .qmd, so this file is only
needed to regenerate it after changing the strike, premium or multiplier below.

    python3 _payoff-diagram.py out.html

then replace the block inside ```{=html} ... ``` on that slide with out.html.
The beamer branch of the slide still uses the ggplot version.
"""
import io, os, sys, math

# ---- geometry -------------------------------------------------------------
X0A, X0B, W = 86, 880, 560          # panel left edges, plot width
Y0, H        = 82, 300              # plot top, plot height
Y1, X1A, X1B = Y0 + H, X0A + W, X0B + W
SMIN, SMAX, K, PREM, MULT = 105, 130, 115, 2000, 400
PX   = W / float(SMAX - SMIN)
SLOPE = math.degrees(math.atan2(MULT * (SMAX - SMIN) / 40.0, W))   # line angle
YT = [-6000, -4000, -2000, 0, 2000, 4000, 6000]
XT = [105, 110, 115, 120, 125, 130]

def xa(s): return X0A + (s - SMIN) * PX
def xb(s): return X0B + (s - SMIN) * PX
def yp(p): return Y1 - (p + 6000) / 12000.0 * H
def n(v):  return ("%.1f" % v).rstrip("0").rstrip(".")
def pts(pairs): return " ".join("%s,%s" % (n(a), n(b)) for a, b in pairs)
def thin(v): return ("−" if v < 0 else "") + format(abs(v), ",d").replace(",", " ")

fut_l = [(xa(s), yp((s - K) * MULT)) for s in (SMIN, SMAX)]
call  = [(xa(SMIN), yp(-PREM)), (xa(K), yp(-PREM)), (xa(SMAX), yp((SMAX - K) * MULT - PREM))]
fut_s = [(xb(s), yp((K - s) * MULT)) for s in (SMIN, SMAX)]
put   = [(xb(SMIN), yp((K - SMIN) * MULT - PREM)), (xb(K), yp(-PREM)), (xb(SMAX), yp(-PREM))]

o = []
a = o.append
a('<div class="payoff">')
a('<svg viewBox="4 0 1456 490" role="img" aria-labelledby="pfT pfD"')
a('     style="width:100%;height:auto;max-height:440px;display:block;margin:0 auto;'
  'font-family:inherit" preserveAspectRatio="xMidYMid meet">')
a('<title id="pfT">Payoff diagrams: option against future</title>')
a('<desc id="pfD">Left panel: a long futures position is a straight line through '
  'the strike of 115; a bought call follows that line above the strike and goes '
  'flat at minus 2 000 below it, so it ends 2 000 below the future on the upside. '
  'Right panel: the mirror image, a short future and a bought put.</desc>')
a('<style>')
a('.pf-grid{stroke:#E8EDEC;stroke-width:1}')
a('.pf-zero{stroke:#9AA7A4;stroke-width:1.3}')
a('.pf-strike{stroke:#63716E;stroke-width:1.4;stroke-dasharray:6 5}')
a('.pf-fut{fill:none;stroke:#40607D;stroke-width:3.6;stroke-linejoin:round;stroke-linecap:round}')
a('.pf-opt{fill:none;stroke:#B4573C;stroke-width:3.6;stroke-linejoin:round;stroke-linecap:round}')
a('.pf-title{fill:#0E5250;font-size:25px;font-weight:700}')
a('.pf-ptitle{fill:#0E5250;font-size:20px;font-weight:700}')
a('.pf-tick{fill:#63716E;font-size:15px}')
a('.pf-axis{fill:#63716E;font-size:16px}')
a('.pf-lfut{fill:#40607D;font-size:19px;font-weight:600}')
a('.pf-lopt{fill:#B4573C;font-size:19px;font-weight:600}')
a('.pf-note{fill:#63716E;font-size:15px}')
a('.pf-brk{stroke:#63716E;stroke-width:1.2;fill:none}')
a('.pf-dot{fill:#B4573C}')
a('</style>')

a('<text class="pf-title" x="732" y="32" text-anchor="middle">The option has a floor. The future does not.</text>')

for x0, x1, ttl in ((X0A, X1A, "Call option and long future"),
                    (X0B, X1B, "Put option and short future")):
    a('<text class="pf-ptitle" x="%d" y="%d">%s</text>' % (x0, Y0 - 14, ttl))
    for p in YT:
        a('<line class="%s" x1="%d" y1="%s" x2="%d" y2="%s"/>'
          % ("pf-zero" if p == 0 else "pf-grid", x0, n(yp(p)), x1, n(yp(p))))
    xk = x0 + (K - SMIN) * PX
    a('<line class="pf-strike" x1="%s" y1="%d" x2="%s" y2="%d"/>' % (n(xk), Y0, n(xk), Y1))
    a('<text class="pf-note" x="%s" y="%d">strike 115</text>' % (n(xk + 8), Y0 + 15))
    for p in YT:
        a('<text class="pf-tick" x="%d" y="%s" text-anchor="end">%s</text>'
          % (x0 - 10, n(yp(p) + 5), thin(p)))
    for s in XT:
        a('<text class="pf-tick" x="%s" y="%d" text-anchor="middle">%d</text>'
          % (n(x0 + (s - SMIN) * PX), Y1 + 26, s))
    a('<text class="pf-axis" x="%s" y="%d" text-anchor="middle">Price at expiration</text>'
      % (n(x0 + W / 2.0), Y1 + 54))
    a('<text class="pf-axis" x="%d" y="%d" text-anchor="middle" transform="rotate(-90 %d %d)">'
      'Profit</text>' % (x0 - 64, Y0 + H // 2, x0 - 64, Y0 + H // 2))

def bracket(x, ya, yb, tip=-6):
    a('<path class="pf-brk" d="M%s %s H%s V%s H%s"/>'
      % (n(x + tip), n(ya), n(x), n(yb), n(x + tip)))

# ---- panel A --------------------------------------------------------------
a('<polyline class="pf-fut" points="%s"/>' % pts(fut_l))
a('<polyline class="pf-opt" points="%s"/>' % pts(call))
a('<circle class="pf-dot" cx="%s" cy="%s" r="5"/>' % (n(xa(K)), n(yp(-PREM))))
px_, py_ = xa(121), yp((121 - K) * MULT)
a('<text class="pf-lfut" x="%s" y="%s" text-anchor="middle" transform="rotate(%s %s %s)">'
  'Long future</text>' % (n(px_), n(py_ - 13), n(-SLOPE), n(px_), n(py_)))
px_, py_ = xa(125), yp((125 - K) * MULT - PREM)
a('<text class="pf-lopt" x="%s" y="%s" text-anchor="middle" transform="rotate(%s %s %s)">'
  'Bought call</text>' % (n(px_), n(py_ + 24), n(-SLOPE), n(px_), n(py_)))
bracket(X1A + 12, yp(6000), yp(4000), tip=6)
a('<text class="pf-note" x="%s" y="%s">premium 2 000</text>'
  % (n(X1A + 24), n((yp(6000) + yp(4000)) / 2 + 5)))

# ---- panel B --------------------------------------------------------------
a('<polyline class="pf-fut" points="%s"/>' % pts(fut_s))
a('<polyline class="pf-opt" points="%s"/>' % pts(put))
a('<circle class="pf-dot" cx="%s" cy="%s" r="5"/>' % (n(xb(K)), n(yp(-PREM))))
px_, py_ = xb(124), yp((K - 124) * MULT)
a('<text class="pf-lfut" x="%s" y="%s" text-anchor="middle" transform="rotate(%s %s %s)">'
  'Short future</text>' % (n(px_), n(py_ + 24), n(SLOPE), n(px_), n(py_)))
a('<text class="pf-lopt" x="%s" y="%s">Bought put</text>' % (n(xb(121.5)), n(yp(-PREM) - 14)))
bracket(xb(106), yp((K - 106) * MULT), yp((K - 106) * MULT - PREM))
a('<text class="pf-note" x="%s" y="%s">premium 2 000</text>'
  % (n(xb(106) - 8), n(yp((K - 106) * MULT) - 14)))

a('<text class="pf-note" x="732" y="472" text-anchor="middle">Strike 115, premium 2\u2009000 per contract, '
  'multiplier 400. Profit at expiration, before transaction costs.</text>')
a('</svg>')
a('</div>')

svg = "\n".join(o) + "\n"
out = sys.argv[1] if len(sys.argv) > 1 else "payoff.svg.html"
io.open(out, "w", encoding="utf-8").write(svg)
print(svg.count("\n"), "lines ->", out)
