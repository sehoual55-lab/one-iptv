#!/usr/bin/env python3
"""Generate original abstract SVG artwork for ONE IPTV (no third-party logos/marks)."""
import math, os, random

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
os.makedirs(OUT, exist_ok=True)


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote", name, os.path.getsize(path), "bytes")


def defs(uid, c1, c2, c3):
    return f"""
  <defs>
    <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="55%" stop-color="{c2}"/>
      <stop offset="100%" stop-color="{c3}"/>
    </linearGradient>
    <radialGradient id="gl{uid}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff2b3b" stop-opacity=".55"/>
      <stop offset="100%" stop-color="#ff2b3b" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="fade{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="40%" stop-color="#07070a" stop-opacity="0"/>
      <stop offset="100%" stop-color="#07070a" stop-opacity=".92"/>
    </linearGradient>
  </defs>"""


def poster(uid, w, h, seed, c1="#12121a", c2="#0c0c12", c3="#1a0a10", glyph=""):
    """Abstract cinematic poster: dark base, red bloom, geometric light streaks."""
    rnd = random.Random(seed)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">',
        defs(uid, c1, c2, c3),
        f'<rect width="{w}" height="{h}" fill="url(#bg{uid})"/>',
    ]
    # soft red blooms
    for i in range(3):
        cx = rnd.uniform(0.15, 0.9) * w
        cy = rnd.uniform(0.1, 0.75) * h
        r = rnd.uniform(0.28, 0.6) * w
        op = rnd.uniform(0.35, 0.8)
        parts.append(
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#gl{uid})" opacity="{op:.2f}"/>'
        )
    # diagonal light streaks
    for i in range(rnd.randint(4, 7)):
        x = rnd.uniform(-0.2, 1.1) * w
        wd = rnd.uniform(1, 5)
        op = rnd.uniform(0.05, 0.22)
        skew = rnd.uniform(-0.35, 0.35) * w
        parts.append(
            f'<path d="M{x:.0f} 0 L{x + skew:.0f} {h} L{x + skew + wd:.0f} {h} L{x + wd:.0f} 0 Z" '
            f'fill="#ffffff" opacity="{op:.2f}"/>'
        )
    # concentric arcs (signal motif)
    ax, ay = w * rnd.uniform(0.2, 0.8), h * rnd.uniform(0.25, 0.7)
    for i in range(1, 5):
        r = i * w * 0.11
        parts.append(
            f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="{r:.0f}" fill="none" '
            f'stroke="#ff2b3b" stroke-opacity="{0.22 - i*0.04:.2f}" stroke-width="1.5"/>'
        )
    # fine grid
    step = max(28, w // 14)
    g = []
    for x in range(0, w + step, step):
        g.append(f"M{x} 0V{h}")
    for y in range(0, h + step, step):
        g.append(f"M0 {y}H{w}")
    parts.append(f'<path d="{" ".join(g)}" stroke="#ffffff" stroke-opacity=".035" stroke-width="1" fill="none"/>')
    if glyph:
        parts.append(glyph)
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#fade{uid})"/>')
    parts.append("</svg>")
    return "".join(parts)


# ---- category glyphs (simple, original line art) -----------------------------
def glyph_play(cx, cy, s, op=".85"):
    return (f'<g opacity="{op}" transform="translate({cx},{cy})">'
            f'<circle r="{s}" fill="none" stroke="#ff2b3b" stroke-width="2.5"/>'
            f'<path d="M{-s*0.28} {-s*0.42} L{s*0.5} 0 L{-s*0.28} {s*0.42} Z" fill="#ff2b3b"/></g>')


def glyph_ball(cx, cy, s):
    pts = []
    for i in range(6):
        a = math.radians(i * 60 - 90)
        pts.append(f"{cx + s*0.62*math.cos(a):.1f},{cy + s*0.62*math.sin(a):.1f}")
    lines = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{p.split(",")[0]}" y2="{p.split(",")[1]}" stroke="#ff2b3b" stroke-width="2" stroke-opacity=".7"/>'
        for p in pts
    )
    return (f'<g opacity=".85"><circle cx="{cx}" cy="{cy}" r="{s}" fill="none" stroke="#ff2b3b" stroke-width="2.5"/>'
            f'<polygon points="{" ".join(pts)}" fill="none" stroke="#ff2b3b" stroke-width="2"/>{lines}</g>')


def glyph_film(cx, cy, s):
    holes = "".join(
        f'<rect x="{cx - s + 6}" y="{cy - s*0.62 + i*(s*0.42)}" width="{s*0.22:.1f}" height="{s*0.22:.1f}" rx="2" fill="#ff2b3b" fill-opacity=".8"/>'
        f'<rect x="{cx + s - 6 - s*0.22}" y="{cy - s*0.62 + i*(s*0.42)}" width="{s*0.22:.1f}" height="{s*0.22:.1f}" rx="2" fill="#ff2b3b" fill-opacity=".8"/>'
        for i in range(4)
    )
    return (f'<g opacity=".9"><rect x="{cx-s}" y="{cy-s*0.78}" width="{s*2}" height="{s*1.56}" rx="8" '
            f'fill="none" stroke="#ff2b3b" stroke-width="2.5"/>{holes}</g>')


def glyph_grid(cx, cy, s):
    r = ""
    for i in range(2):
        for j in range(2):
            r += (f'<rect x="{cx - s + j*(s*1.08)}" y="{cy - s*0.7 + i*(s*0.78)}" '
                  f'width="{s*0.92:.1f}" height="{s*0.62:.1f}" rx="5" fill="none" stroke="#ff2b3b" stroke-width="2.2" stroke-opacity=".85"/>')
    return f'<g>{r}</g>'


def glyph_wave(cx, cy, s):
    d = f"M{cx-s} {cy}"
    for i in range(1, 9):
        x = cx - s + i * (2 * s / 8)
        y = cy + (s * 0.5 if i % 2 else -s * 0.5) * (0.4 + 0.6 * math.sin(i))
        d += f" Q{x - s/8:.1f} {y:.1f} {x:.1f} {cy:.1f}"
    return f'<path d="{d}" fill="none" stroke="#ff2b3b" stroke-width="2.6" stroke-linecap="round" opacity=".85"/>'


def glyph_globe(cx, cy, s):
    return (f'<g opacity=".85" fill="none" stroke="#ff2b3b" stroke-width="2.4">'
            f'<circle cx="{cx}" cy="{cy}" r="{s}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{s*0.44}" ry="{s}"/>'
            f'<line x1="{cx-s}" y1="{cy}" x2="{cx+s}" y2="{cy}"/>'
            f'<path d="M{cx-s*0.92} {cy-s*0.45} H{cx+s*0.92} M{cx-s*0.92} {cy+s*0.45} H{cx+s*0.92}"/></g>')


CATS = [
    ("live-tv", glyph_play(150, 230, 46), 101),
    ("sports", glyph_ball(150, 230, 46), 202),
    ("movies", glyph_film(150, 230, 46), 303),
    ("series", glyph_grid(150, 230, 44), 404),
    ("entertainment", glyph_wave(150, 230, 50), 505),
    ("news", glyph_globe(150, 230, 46), 606),
    ("kids", glyph_play(150, 230, 44), 707),
    ("documentaries", glyph_globe(150, 230, 44), 808),
]

for name, glyph, seed in CATS:
    write(f"cat-{name}.svg", poster(name.replace("-", ""), 300, 400, seed, glyph=glyph))

# ---- blog thumbnails (16:9) --------------------------------------------------
BLOG = [
    ("beginners-guide", 911),
    ("smart-tv-setup", 922),
    ("smart-one-iptv", 933),
    ("one-month-plans", 944),
    ("uk-guide", 955),
    ("app-download", 966),
    ("tv-setup", 977),
]
for name, seed in BLOG:
    write(f"blog-{name}.svg", poster("b" + name.replace("-", ""), 800, 450, seed))


# ---- hero screen (cinematic UI mock, original) --------------------------------
def hero_screen():
    w, h = 1280, 800
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">',
         """<defs>
    <linearGradient id="hbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#141420"/><stop offset="50%" stop-color="#0a0a10"/><stop offset="100%" stop-color="#1d0a11"/>
    </linearGradient>
    <radialGradient id="hglow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff2b3b" stop-opacity=".6"/><stop offset="100%" stop-color="#ff2b3b" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="hcard" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity=".13"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".03"/>
    </linearGradient>
    <linearGradient id="hred" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff2b3b"/><stop offset="100%" stop-color="#8f0009"/>
    </linearGradient>
    <linearGradient id="hshade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="30%" stop-color="#07070a" stop-opacity="0"/><stop offset="100%" stop-color="#07070a" stop-opacity=".85"/>
    </linearGradient>
  </defs>""",
         f'<rect width="{w}" height="{h}" fill="url(#hbg)"/>',
         '<circle cx="980" cy="180" r="420" fill="url(#hglow)" opacity=".75"/>',
         '<circle cx="180" cy="700" r="360" fill="url(#hglow)" opacity=".35"/>']
    # grid
    g = []
    for x in range(0, w + 80, 80):
        g.append(f"M{x} 0V{h}")
    for y in range(0, h + 80, 80):
        g.append(f"M0 {y}H{w}")
    p.append(f'<path d="{" ".join(g)}" stroke="#fff" stroke-opacity=".035" fill="none"/>')

    # top bar
    p.append('<rect x="46" y="40" width="1188" height="56" rx="16" fill="url(#hcard)"/>')
    p.append('<rect x="66" y="56" width="24" height="24" rx="7" fill="url(#hred)"/>')
    p.append('<rect x="100" y="62" width="86" height="12" rx="6" fill="#fff" fill-opacity=".85"/>')
    for i, wd in enumerate([48, 62, 54, 44]):
        p.append(f'<rect x="{240 + i*90}" y="64" width="{wd}" height="9" rx="4.5" fill="#fff" fill-opacity=".3"/>')
    p.append('<rect x="1094" y="54" width="120" height="28" rx="14" fill="url(#hred)" opacity=".9"/>')

    # featured banner
    p.append('<rect x="46" y="122" width="1188" height="332" rx="22" fill="#0e0e16"/>')
    p.append('<rect x="46" y="122" width="1188" height="332" rx="22" fill="url(#hcard)"/>')
    p.append('<circle cx="1050" cy="200" r="240" fill="url(#hglow)" opacity=".55"/>')
    # streaks inside banner
    for i in range(6):
        x = 640 + i * 105
        p.append(f'<path d="M{x} 122 L{x-120} 454 L{x-112} 454 L{x+8} 122 Z" fill="#fff" opacity="{0.05 + i*0.012:.3f}"/>')
    p.append('<rect x="86" y="176" width="112" height="26" rx="13" fill="#ff2b3b" fill-opacity=".9"/>')
    p.append('<rect x="98" y="185" width="88" height="8" rx="4" fill="#fff" fill-opacity=".95"/>')
    p.append('<rect x="86" y="226" width="430" height="26" rx="8" fill="#fff" fill-opacity=".92"/>')
    p.append('<rect x="86" y="266" width="340" height="26" rx="8" fill="#fff" fill-opacity=".62"/>')
    p.append('<rect x="86" y="316" width="250" height="10" rx="5" fill="#fff" fill-opacity=".28"/>')
    p.append('<rect x="86" y="336" width="300" height="10" rx="5" fill="#fff" fill-opacity=".2"/>')
    p.append('<rect x="86" y="378" width="150" height="44" rx="22" fill="url(#hred)"/>')
    p.append('<path d="M120 392 L146 400 L120 408 Z" fill="#fff"/>')
    p.append('<rect x="252" y="378" width="150" height="44" rx="22" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="1.5"/>')

    # row label
    p.append('<rect x="46" y="492" width="180" height="14" rx="7" fill="#fff" fill-opacity=".8"/>')
    p.append('<rect x="46" y="516" width="64" height="3" rx="1.5" fill="#ff2b3b"/>')

    # card row
    for i in range(6):
        x = 46 + i * 202
        p.append(f'<rect x="{x}" y="548" width="180" height="230" rx="14" fill="#12121b"/>')
        p.append(f'<rect x="{x}" y="548" width="180" height="230" rx="14" fill="url(#hcard)"/>')
        p.append(f'<circle cx="{x+130}" cy="600" r="90" fill="url(#hglow)" opacity="{0.3 + (i%3)*0.14:.2f}"/>')
        p.append(f'<circle cx="{x+90}" cy="640" r="26" fill="none" stroke="#ff2b3b" stroke-opacity=".55" stroke-width="2"/>')
        p.append(f'<path d="M{x+82} {640-11} L{x+104} {640} L{x+82} {640+11} Z" fill="#ff2b3b" fill-opacity=".75"/>')
        p.append(f'<rect x="{x+16}" y="716" width="{120 - (i%3)*22}" height="10" rx="5" fill="#fff" fill-opacity=".7"/>')
        p.append(f'<rect x="{x+16}" y="736" width="{72 + (i%2)*20}" height="8" rx="4" fill="#fff" fill-opacity=".28"/>')

    p.append(f'<rect width="{w}" height="{h}" fill="url(#hshade)"/>')
    p.append("</svg>")
    return "".join(p)


write("hero-screen.svg", hero_screen())


# ---- Open Graph image --------------------------------------------------------
def og():
    w, h = 1200, 630
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="ob" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#101018"/><stop offset="55%" stop-color="#07070a"/><stop offset="100%" stop-color="#1e0a11"/>
    </linearGradient>
    <radialGradient id="og" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff2b3b" stop-opacity=".65"/><stop offset="100%" stop-color="#ff2b3b" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="or" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff2b3b"/><stop offset="100%" stop-color="#8f0009"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#ob)"/>
  <circle cx="960" cy="120" r="420" fill="url(#og)" opacity=".7"/>
  <circle cx="140" cy="560" r="300" fill="url(#og)" opacity=".3"/>
  <g opacity=".05" stroke="#fff" fill="none">
    {"".join(f'<path d="M{x} 0V{h}"/>' for x in range(0, w+80, 80))}
    {"".join(f'<path d="M0 {y}H{w}"/>' for y in range(0, h+80, 80))}
  </g>
  <rect x="80" y="86" width="66" height="66" rx="18" fill="url(#or)"/>
  <path d="M104 108 L128 119 L104 130 Z" fill="#fff"/>
  <text x="166" y="132" font-family="Inter, Arial, sans-serif" font-size="38" font-weight="800" fill="#fff">ONE <tspan fill="#ff2b3b">IPTV</tspan></text>
  <text x="80" y="300" font-family="Inter, Arial, sans-serif" font-size="72" font-weight="800" fill="#fff">Premium IPTV Service</text>
  <text x="80" y="382" font-family="Inter, Arial, sans-serif" font-size="72" font-weight="800" fill="#ff2b3b">for Smart TVs &amp; Devices</text>
  <text x="80" y="452" font-family="Inter, Arial, sans-serif" font-size="28" fill="#b7b7c4">Live TV, movies, series and more on compatible devices.</text>
  <rect x="80" y="500" width="300" height="62" rx="31" fill="url(#or)"/>
  <text x="230" y="540" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="24" font-weight="700" fill="#fff">one-iptv.website</text>
  <text x="410" y="540" font-family="Inter, Arial, sans-serif" font-size="22" fill="#83838f">Simple • Fast • Flexible • Multi-Device</text>
</svg>"""


write("og-image.svg", og())

# ---- favicon -----------------------------------------------------------------
write("favicon.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs><linearGradient id="f" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ff2b3b"/><stop offset="100%" stop-color="#8f0009"/>
  </linearGradient></defs>
  <rect width="64" height="64" rx="16" fill="#07070a"/>
  <rect x="6" y="6" width="52" height="52" rx="13" fill="url(#f)"/>
  <path d="M25 21 L45 32 L25 43 Z" fill="#fff"/>
</svg>""")

print("done")
