#!/usr/bin/env python3
"""ICDESK brand generator — logo inspired by the IC TEAM badge.
All text is converted to paths (flutter_svg / Linux icon themes don't need fonts)."""
import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT = TTFont(os.path.join(os.path.dirname(__file__), "BarlowSemiCondensed-Bold.ttf"))
GS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UPM = FONT["head"].unitsPerEm
CAP = FONT["OS/2"].sCapHeight or 700

C = 512  # centre in a 1024 box


def glyph_path(ch, a, b, c, d, e, f):
    """Return SVG path of glyph `ch` transformed by affine (a,b,c,d,e,f)."""
    name = CMAP[ord(ch)]
    pen = SVGPathPen(GS, lambda v: f"{v:.2f}")
    GS[name].draw(TransformPen(pen, (a, b, c, d, e, f)))
    return pen.getCommands()


def adv(ch):
    return GS[CMAP[ord(ch)]].width


def text_line(txt, cx, baseline, cap_h, track=0.0):
    """Straight text centred at cx; cap_h = desired cap height in px."""
    s = cap_h / CAP
    widths = [adv(ch) * s for ch in txt]
    total = sum(widths) + track * (len(txt) - 1)
    x = cx - total / 2
    out = []
    for ch, w in zip(txt, widths):
        if ch != " ":
            out.append(glyph_path(ch, s, 0, 0, -s, x, baseline))
        x += w + track
    return "".join(out)


def text_arc(txt, r, cap_h, track_deg=0.0, centre_deg=-90):
    """Text along the TOP of a circle of radius r (baseline), reading left->right."""
    s = cap_h / CAP
    widths = [adv(ch) * s for ch in txt]
    angs = [math.degrees(w / r) for w in widths]
    total = sum(angs) + track_deg * (len(txt) - 1)
    a = centre_deg - total / 2
    out = []
    for ch, w, da in zip(txt, widths, angs):
        mid = math.radians(a + da / 2)
        if ch != " ":
            # glyph local: x in [-w/2, w/2], baseline at 0, y up -> rotate so up points outwards
            rot = mid + math.pi / 2
            cr, sr = math.cos(rot), math.sin(rot)
            px, py = C + r * math.cos(mid), C + r * math.sin(mid)
            # local (u,v) font units: X = s*u - w/2 ; Y = -s*v
            # world = R*(X,Y) + p
            A, B = s * cr, s * sr
            Cc, D = s * sr, -s * cr
            E = px + cr * (-w / 2)
            F = py + sr * (-w / 2)
            out.append(glyph_path(ch, A, B, Cc, D, E, F))
        a += da + track_deg
    return "".join(out)


def ring(r1, r2):
    return (f"M{C-r2},{C}a{r2},{r2} 0 1,0 {2*r2},0a{r2},{r2} 0 1,0 {-2*r2},0Z"
            f"M{C-r1},{C}a{r1},{r1} 0 1,1 {2*r1},0a{r1},{r1} 0 1,1 {-2*r1},0Z")


def annular_sector(r1, r2, a1, a2):
    p = lambda r, a: (C + r * math.cos(math.radians(a)), C + r * math.sin(math.radians(a)))
    x1, y1 = p(r2, a1); x2, y2 = p(r2, a2); x3, y3 = p(r1, a2); x4, y4 = p(r1, a1)
    big = 1 if (a2 - a1) > 180 else 0
    return (f"M{x1:.2f},{y1:.2f}A{r2},{r2} 0 {big},1 {x2:.2f},{y2:.2f}"
            f"L{x3:.2f},{y3:.2f}A{r1},{r1} 0 {big},0 {x4:.2f},{y4:.2f}Z")


def radial_rect(r1, r2, ang, w):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    pts = []
    for r, k in ((r1, -1), (r2, -1), (r2, 1), (r1, 1)):
        pts.append((C + ux * r + vx * k * w / 2, C + uy * r + vy * k * w / 2))
    return "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"


def chamfer_poly(pts):
    return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"


def letters_IC(cx, cy, h):
    """Blocky chamfered 'IC' monogram (polygons), height h, centred."""
    k = h / 260.0
    st = 74 * k          # stroke
    ch = 30 * k          # chamfer
    # I : slab with serifs
    iw, sw = 150 * k, st  # total width (with serifs), stem width
    gap = 28 * k
    cw = 210 * k
    total = iw + gap + cw
    x0 = cx - total / 2
    y0 = cy - h / 2
    sx = x0 + (iw - sw) / 2
    bar = 52 * k
    I = chamfer_poly([
        (x0 + ch, y0), (x0 + iw - ch, y0), (x0 + iw, y0 + ch), (x0 + iw, y0 + bar),
        (sx + sw, y0 + bar), (sx + sw, y0 + h - bar), (x0 + iw, y0 + h - bar), (x0 + iw, y0 + h - ch),
        (x0 + iw - ch, y0 + h), (x0 + ch, y0 + h), (x0, y0 + h - ch), (x0, y0 + h - bar),
        (sx, y0 + h - bar), (sx, y0 + bar), (x0, y0 + bar), (x0, y0 + ch)])
    # C : octagonal, opening on the right
    X = x0 + iw + gap
    oc = 62 * k          # outer chamfer
    ic = 26 * k          # inner chamfer
    op = 74 * k          # arm height (how far top/bottom arms reach down/up on the right)
    Cp = chamfer_poly([
        (X + oc, y0), (X + cw - ch, y0), (X + cw, y0 + ch), (X + cw, y0 + op),
        (X + st + ic + 40 * k, y0 + op), (X + st + ic + 40 * k, y0 + st),
        (X + st + ic, y0 + st), (X + st, y0 + st + ic),
        (X + st, y0 + h - st - ic), (X + st + ic, y0 + h - st),
        (X + st + ic + 40 * k, y0 + h - st), (X + st + ic + 40 * k, y0 + h - op),
        (X + cw, y0 + h - op), (X + cw, y0 + h - ch), (X + cw - ch, y0 + h),
        (X + oc, y0 + h), (X, y0 + h - oc), (X, y0 + oc)])
    return I + Cp


DEFS = """
<defs>
  <!-- ICDESK palette: gradient #EBD7A6 -> #C5A059 -> #8A6A32, gold light #E8CE94, rich black #0D0D0D -->
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#EBD7A6"/><stop offset=".3" stop-color="#C5A059"/>
    <stop offset=".5" stop-color="#E8CE94"/><stop offset=".78" stop-color="#8A6A32"/>
    <stop offset="1" stop-color="#C5A059"/>
  </linearGradient>
  <linearGradient id="goldV" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#EBD7A6"/><stop offset=".5" stop-color="#C5A059"/>
    <stop offset="1" stop-color="#8A6A32"/>
  </linearGradient>
  <linearGradient id="goldDark" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#8A6A32"/><stop offset="1" stop-color="#4F3C1B"/>
  </linearGradient>
  <linearGradient id="silver" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#D9D9D9"/><stop offset=".3" stop-color="#7D7D7D"/>
    <stop offset=".55" stop-color="#C4C4C4"/><stop offset=".8" stop-color="#666666"/>
    <stop offset="1" stop-color="#B5B5B5"/>
  </linearGradient>
  <radialGradient id="face" cx=".5" cy=".42" r=".6">
    <stop offset="0" stop-color="#1F1F1F"/><stop offset="1" stop-color="#0D0D0D"/>
  </radialGradient>
</defs>"""

INK = "#0D0D0D"  # engraved / dark details


def badge(full=True):
    """Return SVG body (no <svg> wrapper) for 1024 box."""
    g = []
    # outer bevel + bezel
    g.append(f'<circle cx="{C}" cy="{C}" r="500" fill="url(#goldDark)"/>')
    g.append(f'<path fill="url(#gold)" fill-rule="evenodd" d="{ring(398, 490)}"/>')
    g.append(f'<circle cx="{C}" cy="{C}" r="398" fill="url(#face)"/>')
    # thin dark groove lines on the bezel
    g.append(f'<path fill="{INK}" opacity=".55" fill-rule="evenodd" d="{ring(476, 480)}{ring(408, 411)}"/>')
    # ticks
    ticks = []
    for i in range(60):
        ang = -90 + i * 6
        if i % 15 == 0:
            continue
        if full and -150 < ang < -30:
            continue  # banner region
        long = i % 5 == 0
        ticks.append(radial_rect(424 if long else 436, 462, ang, 11 if long else 7))
    g.append(f'<path fill="{INK}" d="{"".join(ticks)}"/>')
    # cardinal notches
    notch = "".join(radial_rect(462, 500, a, 20) for a in (0, 90, 180, 270))
    g.append(f'<path fill="{INK}" d="{notch}"/>')
    if full:
        # banner plaque on the bezel, top
        g.append(f'<path fill="url(#goldV)" stroke="{INK}" stroke-opacity=".6" stroke-width="4" '
                 f'd="{annular_sector(330, 472, -146, -34)}"/>')
        g.append(f'<path fill="{INK}" d="{text_arc("REMOTE ACCESS", 372, 58, track_deg=1.6)}"/>')
    # silver ring with 4 breaks
    sil = "".join(annular_sector(296, 322, a + 4, a + 86) for a in (-90 + 45, 45, 135, 225))
    ring_r_in, ring_r_out = (296, 322)
    if full:
        # in full badge the banner covers top of ring: keep ring below banner inner edge
        ring_r_in, ring_r_out = (286, 310)
        sil = "".join(annular_sector(ring_r_in, ring_r_out, a + 4, a + 86) for a in (-90 + 45, 45, 135, 225))
    g.append(f'<path fill="url(#silver)" d="{sil}"/>')
    caps = "".join(radial_rect(ring_r_in - 6, ring_r_out + 6, a, 14) for a in (-45, 45, 135, 225))
    g.append(f'<path fill="#9a9a9a" stroke="{INK}" stroke-width="2" d="{caps}"/>')
    # thin gold inner ring
    g.append(f'<path fill="url(#gold)" fill-rule="evenodd" d="{ring(262, 270)}"/>')
    # monogram
    if full:
        mono = letters_IC(C, C - 34, 210)
        g.append(f'<path transform="translate(8,10)" fill="#000" opacity=".55" d="{mono}"/>')
        g.append(f'<path fill="url(#goldV)" stroke="#5C4620" stroke-width="3" d="{mono}"/>')
        g.append(f'<path fill="url(#gold)" d="{text_line("DESK", C, C + 168, 54, track=14)}"/>')
    else:
        mono = letters_IC(C, C, 250)
        g.append(f'<path transform="translate(9,11)" fill="#000" opacity=".55" d="{mono}"/>')
        g.append(f'<path fill="url(#goldV)" stroke="#5C4620" stroke-width="3" d="{mono}"/>')
    return "".join(g)


def svg(body, vb="0 0 1024 1024", extra_defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="1024" height="1024">'
            f'{DEFS}{extra_defs}{body}</svg>')


def app_square(full=True, scale=0.86, radius=0):
    """Dark (rounded) square with badge — for macOS / iOS / Android legacy."""
    t = (1 - scale) * 512
    bg = (f'<rect width="1024" height="1024" rx="{radius}" fill="#0D0D0D"/>'
          f'<rect width="1024" height="1024" rx="{radius}" fill="url(#face)" opacity=".7"/>')
    return bg + f'<g transform="translate({t},{t}) scale({scale})">{badge(full)}</g>'


def mac_icon():
    # Apple grid: 824 box inside 1024, r≈185, with soft shadow below
    inner = (f'<rect x="100" y="112" width="824" height="824" rx="185" fill="#000" opacity=".35"/>'
             f'<rect x="100" y="100" width="824" height="824" rx="185" fill="#0D0D0D"/>'
             f'<rect x="100" y="100" width="824" height="824" rx="185" fill="url(#face)"/>')
    s = 0.74
    t = 512 - 512 * s
    return inner + f'<g transform="translate({t},{t}) scale({s})">{badge(True)}</g>'


def badge_tiny():
    """Small-size variant (<=48px): gold bezel, dark face, big IC."""
    g = [f'<circle cx="{C}" cy="{C}" r="504" fill="url(#goldDark)"/>',
         f'<path fill="url(#gold)" fill-rule="evenodd" d="{ring(380, 494)}"/>',
         f'<circle cx="{C}" cy="{C}" r="380" fill="url(#face)"/>']
    mono = letters_IC(C, C, 330)
    g.append(f'<path fill="url(#goldV)" stroke="#5C4620" stroke-width="4" d="{mono}"/>')
    return "".join(g)


def mono_glyph(color="#000"):
    """Single-colour silhouette (tray / Android notification / monochrome)."""
    g = [f'<path fill="{color}" fill-rule="evenodd" d="{ring(380, 490)}"/>']
    g.append(f'<path fill="{color}" d="{letters_IC(C, C, 330)}"/>')
    return "".join(g)


def wordmark(dark_text=False):
    """Horizontal logo 1500x300: badge + ICDESK wordmark (for assets/logo*.png & banner)."""
    txt_fill = "#0D0D0D" if dark_text else "url(#gold)"
    b = f'<g transform="translate(10,10) scale({280/1024})">{badge(False)}</g>'
    # wordmark: IC in gold block letters + DESK in font
    w = letters_IC(0, 0, 150)
    ic = f'<path transform="translate(450,150)" fill="url(#goldV)" stroke="#5C4620" stroke-width="2" d="{w}"/>'
    desk = text_line("DESK", 0, 0, 150, track=10)
    # measure DESK width roughly
    s = 150 / CAP
    dw = sum(adv(c) * s for c in "DESK") + 30
    d = f'<path transform="translate({600 + dw/2:.1f},225)" fill="{txt_fill}" d="{desk}"/>'
    tag = text_line("REMOTE ACCESS", 0, 0, 34, track=12)
    t = f'<path transform="translate({(330 + 600 + dw)/2:.1f},282)" fill="{txt_fill}" opacity=".75" d="{tag}"/>'
    return b + ic + d + t, 600 + dw + 20


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "svg")
    os.makedirs(out, exist_ok=True)
    W = lambda n, s: open(os.path.join(out, n), "w").write(s)
    W("badge_full.svg", svg(badge(True)))
    W("badge_tiny.svg", svg(badge_tiny()))
    W("app_square_simple.svg", svg(app_square(False, 0.9)))
    W("badge_simple.svg", svg(badge(False)))
    W("app_square_full.svg", svg(app_square(True, 0.9)))
    W("android_fg.svg", svg(f'<g transform="translate(184,184) scale(.640625)">{badge(False)}</g>'))
    W("mac_icon.svg", svg(mac_icon()))
    W("mono_black.svg", svg(mono_glyph("#000")))
    W("mono_white.svg", svg(mono_glyph("#fff")))
    for dark in (False, True):
        body, width = wordmark(dark_text=dark)
        W("wordmark_%s.svg" % ("light" if dark else "dark"),
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} 300" width="{width:.0f}" height="300">{DEFS}{body}</svg>')
    print("ok")
