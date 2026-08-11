# -*- coding: utf-8 -*-
"""
Asset generator for the Manas Borole GitHub profile README.

Produces every themed, animated SVG asset from ONE place so the whole profile
reads as a single system (NieR / Ghost-in-the-Shell filmic teal + amber).

Why SVG: GitHub markdown strips CSS/JS from the page, but an SVG referenced via
<img src="...raw.githubusercontent..."> is rendered as its own document, so CSS
@keyframes and SMIL animations INSIDE the SVG still run. That is the whole trick.

Run:  python assets/_generate.py
Edit palette / copy below, re-run, commit. Nothing else to touch.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# PALETTE  (edit here -> re-run -> whole profile restyles)
#
# Every color token now resolves to a CSS variable, so a single injected
# <style> block themes the whole SVG. prefers-color-scheme lets each asset
# follow the visitor's GitHub theme: dark stays as designed, light gets a
# GitHub-light-friendly palette. Scenes/terminal opt out (adaptive=False).
# ----------------------------------------------------------------------------
P = {
    "__BG__":     "var(--bg)",
    "__BG2__":    "var(--bg2)",
    "__SURF__":   "var(--surf)",
    "__SURF2__":  "var(--surf2)",
    "__TEAL__":   "var(--teal)",
    "__TEALG__":  "var(--tealg)",
    "__TEALD__":  "var(--teald)",
    "__AMBER__":  "var(--amber)",
    "__AMBERG__": "var(--amberg)",
    "__TEXT__":   "var(--text)",
    "__MUTE__":   "var(--mute)",
    "__LINE__":   "var(--line)",
}

# Dark values (design baseline) + light overrides for light-mode visitors.
_DARK = {
    "bg": "#0A0E12", "bg2": "#0D141A", "surf": "#121A20", "surf2": "#16232B",
    "teal": "#4CC9C0", "tealg": "#7FE9DF", "teald": "#2C6E6A",
    "amber": "#E9A85A", "amberg": "#F4C889",
    "text": "#E8EEEC", "mute": "#7E938C", "line": "#20303A",
}
# Light: GitHub light surface, deepened accents that read on white, ink text.
_LIGHT = {
    "bg": "#F6F8FA", "bg2": "#FFFFFF", "surf": "#FFFFFF", "surf2": "#F2F5F8",
    "teal": "#0E7C74", "tealg": "#0E8C82", "teald": "#8FB7B3",
    "amber": "#B9761A", "amberg": "#C98A2A",
    "text": "#1F2328", "mute": "#57606A", "line": "#D0D7DE",
}


def _theme_style(adaptive):
    root = ";".join("--%s:%s" % (k, v) for k, v in _DARK.items())
    block = "<style>:root{%s}" % root
    if adaptive:
        light = ";".join("--%s:%s" % (k, v) for k, v in _LIGHT.items())
        # In light mode also calm the neon: hide scanlines, soften glow.
        block += ("@media(prefers-color-scheme:light){:root{%s}"
                  ".scanpanel{opacity:0}}" % light)
    return block + "</style>"


SANS = "'Segoe UI', -apple-system, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', 'Cascadia Code', 'Consolas', monospace"


def save(relpath, svg, extra=None, adaptive=True):
    tokens = dict(P)
    if extra:
        tokens.update(extra)
    for k, v in tokens.items():
        svg = svg.replace(k, v)
    # Inject the theme <style> right after the opening <svg ...> tag.
    i = svg.find(">", svg.find("<svg"))
    if i != -1:
        svg = svg[:i + 1] + "\n  " + _theme_style(adaptive) + svg[i + 1:]
    path = os.path.join(HERE, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg.strip() + "\n")
    print("  +", relpath)


# Shared <defs>: soft glow filters + gradients. Kept token-free where possible.
def defs():
    return """
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="__BG2__"/>
      <stop offset="1" stop-color="__BG__"/>
    </linearGradient>
    <linearGradient id="tealGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="__TEAL__"/>
      <stop offset="1" stop-color="__TEALG__"/>
    </linearGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="__TEAL__" stop-opacity="0"/>
      <stop offset="0.5" stop-color="__TEAL__" stop-opacity="1"/>
      <stop offset="1" stop-color="__AMBER__" stop-opacity="0"/>
    </linearGradient>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
"""


# Faint scanline overlay used across many assets.
def scanlines(w, h, opacity="0.05"):
    return (
        '<g class="scanpanel" opacity="%s">' % opacity
        + "".join(
            '<rect x="0" y="%d" width="%d" height="1" fill="__TEAL__"/>' % (y, w)
            for y in range(0, h, 4)
        )
        + "</g>"
    )


# ----------------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------------
def hero():
    w, h = 1200, 380
    # skyline: two parallax silhouette layers
    import_ = ""
    far = ["<polygon points='"]
    # build a jagged skyline procedurally (deterministic, no randomness)
    xs = list(range(0, w + 1, 40))
    heights_far = [120, 90, 150, 70, 130, 100, 165, 85, 140, 95, 155, 75,
                   135, 110, 160, 80, 145, 90, 150, 70, 130, 100, 165, 88,
                   142, 96, 158, 78, 138, 112, 162]
    pts_far = "0,%d " % h
    for i, x in enumerate(xs):
        pts_far += "%d,%d " % (x, h - heights_far[i % len(heights_far)])
    pts_far += "%d,%d" % (w, h)
    heights_near = [200, 150, 240, 120, 210, 170, 260, 140, 230, 160, 250,
                    130, 220, 180, 255, 135, 235, 158, 248, 128]
    pts_near = "0,%d " % h
    xs2 = list(range(0, w + 1, 66))
    for i, x in enumerate(xs2):
        pts_near += "%d,%d " % (x, h - heights_near[i % len(heights_near)])
    pts_near += "%d,%d" % (w, h)

    # window lights (deterministic grid, some lit amber/teal)
    windows = ""
    lit = 0
    for gx in range(30, w, 66):
        for gy in range(h - 250, h - 20, 22):
            lit += 1
            if lit % 7 == 0:
                col, op, dur = "__AMBER__", "0.5", "3.2s"
            elif lit % 5 == 0:
                col, op, dur = "__TEALG__", "0.45", "2.4s"
            else:
                continue
            windows += (
                '<rect class="win" x="%d" y="%d" width="3" height="6" fill="%s" '
                'opacity="%s" style="animation-duration:%s"/>'
                % (gx + (gy % 11), gy, col, op, dur)
            )

    stars = "".join(
        '<circle class="star" cx="%d" cy="%d" r="%.1f" fill="__TEALG__" '
        'style="animation-delay:%.1fs"/>'
        % ((i * 83) % w, 30 + (i * 47) % 140, 0.8 + (i % 3) * 0.4, (i % 9) * 0.4)
        for i in range(46)
    )

    css = """
  <style>
    .star{animation:tw 3.4s ease-in-out infinite}
    @keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}
    .win{animation:flick 3s steps(2) infinite}
    @keyframes flick{0%,100%{opacity:.15}50%{opacity:.7}}
    .title{font:800 76px __SANS__;letter-spacing:8px;fill:__TEXT__}
    .kick{font:600 15px __MONO__;letter-spacing:6px;fill:__AMBER__}
    .tag{font:400 21px __SANS__;fill:__MUTE__}
    .type{font:600 22px __MONO__;fill:__TEALG__}
    .cur{animation:blink 1s steps(1) infinite}
    @keyframes blink{50%{opacity:0}}
    .rise{opacity:0;animation:rise 1.1s ease-out forwards}
    @keyframes rise{to{opacity:1;transform:translateY(0)}}
    .sweep{animation:sweep 6s linear infinite}
    @keyframes sweep{0%{transform:translateY(-30px);opacity:0}
      10%{opacity:.5}90%{opacity:.5}100%{transform:translateY(410px);opacity:0}}
  </style>
"""
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Manas Borole - AI Engineer hero banner">
  __DEFS__
  __CSS__
  <rect width="__W__" height="__H__" fill="url(#bgGrad)"/>
  <g>__STARS__</g>
  <!-- horizon glow -->
  <ellipse cx="600" cy="__H__" rx="620" ry="150" fill="__TEALD__" opacity="0.18" filter="url(#softGlow)"/>
  <polygon points="__FAR__" fill="#0e1a20" opacity="0.9"/>
  <polygon points="__NEAR__" fill="#0a1418"/>
  <g>__WINDOWS__</g>
  __SCAN__
  <!-- scanning sweep line -->
  <rect class="sweep" x="0" y="0" width="__W__" height="2" fill="__TEAL__" opacity="0.5"/>
  <!-- HUD corner brackets -->
  <path d="M24 24 h46 M24 24 v46" stroke="__TEAL__" stroke-width="2" fill="none" opacity="0.8"/>
  <path d="M1176 24 h-46 M1176 24 v46" stroke="__TEAL__" stroke-width="2" fill="none" opacity="0.8"/>
  <path d="M24 356 h46 M24 356 v-46" stroke="__AMBER__" stroke-width="2" fill="none" opacity="0.6"/>
  <path d="M1176 356 h-46 M1176 356 v-46" stroke="__AMBER__" stroke-width="2" fill="none" opacity="0.6"/>
  <!-- copy -->
  <g transform="translate(80,120)">
    <text class="kick rise" style="animation-delay:.1s">AI  ENGINEER</text>
    <text class="title rise" y="78" style="animation-delay:.3s" filter="url(#glow)">MANAS BOROLE</text>
    <text class="tag rise" y="128" style="animation-delay:.6s">Systems that survive contact with production.</text>
    <text class="type" y="182" style="animation-delay:.9s">&gt; real-time voice &#183; LLM routing &#183; the backends that keep them honest<tspan class="cur" fill="__AMBER__">_</tspan></text>
  </g>
</svg>
"""
    svg = (svg.replace("__W__", str(w)).replace("__H__", str(h))
           .replace("__DEFS__", defs()).replace("__CSS__", css)
           .replace("__STARS__", stars).replace("__WINDOWS__", windows)
           .replace("__FAR__", pts_far).replace("__NEAR__", pts_near)
           .replace("__SCAN__", scanlines(w, h))
           .replace("__SANS__", SANS).replace("__MONO__", MONO))
    save("hero/hero-banner.svg", svg, adaptive=False)


# ----------------------------------------------------------------------------
# SECTION HEADERS  (reusable)
# ----------------------------------------------------------------------------
def section_header(key, kicker, title):
    w, h = 1000, 116
    css = """
  <style>
    .k{font:600 13px __MONO__;letter-spacing:6px;fill:__AMBER__}
    .t{font:800 42px __SANS__;letter-spacing:2px;fill:__TEXT__}
    .bar{animation:pulse 2.6s ease-in-out infinite}
    @keyframes pulse{0%,100%{opacity:.55}50%{opacity:1}}
    .dash{stroke-dasharray:6 10;animation:march 8s linear infinite}
    @keyframes march{to{stroke-dashoffset:-160}}
    .node{animation:np 2.6s ease-in-out infinite}
    @keyframes np{0%,100%{r:3;opacity:.6}50%{r:5;opacity:1}}
  </style>
"""
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="__TITLE__">
  __DEFS__
  __CSS__
  <rect width="__W__" height="__H__" fill="__BG__"/>
  __SCAN__
  <rect class="bar" x="0" y="20" width="6" height="76" rx="3" fill="url(#tealGrad)" filter="url(#glow)"/>
  <text class="k" x="28" y="46">__KICK__</text>
  <text class="t" x="26" y="88" filter="url(#glow)">__TITLE__</text>
  <line class="dash" x1="28" y1="104" x2="972" y2="104" stroke="__LINE__" stroke-width="1.5"/>
  <circle class="node" cx="972" cy="104" r="4" fill="__AMBER__" filter="url(#glow)"/>
  <circle class="node" cx="28"  cy="104" r="4" fill="__TEAL__" style="animation-delay:1.3s" filter="url(#glow)"/>
</svg>
"""
    svg = (svg.replace("__W__", str(w)).replace("__H__", str(h))
           .replace("__DEFS__", defs()).replace("__CSS__", css)
           .replace("__SCAN__", scanlines(w, h, "0.04"))
           .replace("__KICK__", kicker).replace("__TITLE__", title)
           .replace("__SANS__", SANS).replace("__MONO__", MONO))
    save("sections/header-%s.svg" % key, svg)


# ----------------------------------------------------------------------------
# DIVIDERS
# ----------------------------------------------------------------------------
def divider_scanline():
    w, h = 1000, 40
    css = """<style>.s{animation:mv 5s linear infinite}
    @keyframes mv{0%{transform:translateX(-1000px)}100%{transform:translateX(1000px)}}</style>"""
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="divider">
  __DEFS__ __CSS__
  <line x1="0" y1="20" x2="__W__" y2="20" stroke="__LINE__" stroke-width="1"/>
  <rect class="s" x="0" y="18" width="240" height="3" fill="url(#fade)" filter="url(#glow)"/>
  <circle cx="500" cy="20" r="3" fill="__AMBER__" filter="url(#glow)"/>
</svg>"""
    save("dividers/divider-scanline.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css))


def divider_rain():
    w, h = 1000, 90
    drops = ""
    for i in range(60):
        x = (i * 167) % w
        d = 0.9 + (i % 5) * 0.25
        delay = (i % 11) * 0.18
        drops += ('<line class="d" x1="%d" y1="-14" x2="%d" y2="0" stroke="__TEAL__" '
                  'stroke-width="1" opacity="0.5" style="animation-duration:%ss;animation-delay:-%ss"/>'
                  % (x, x - 6, d, delay))
    css = """<style>.d{animation:fall linear infinite}
    @keyframes fall{0%{transform:translateY(0);opacity:0}
      10%{opacity:.6}100%{transform:translateY(104px);opacity:0}}</style>"""
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="rain divider">
  __DEFS__ __CSS__
  <g>__DROPS__</g>
  <line x1="0" y1="70" x2="__W__" y2="70" stroke="__LINE__" stroke-width="1"/>
</svg>"""
    save("dividers/divider-rain.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css).replace("__DROPS__", drops))


def divider_particles():
    w, h = 1000, 70
    ps = ""
    for i in range(40):
        x = (i * 211) % w
        y = 10 + (i * 37) % 50
        r = 0.8 + (i % 3) * 0.6
        ps += ('<circle class="p" cx="%d" cy="%d" r="%.1f" fill="%s" style="animation-delay:-%ss"/>'
               % (x, y, r, "__AMBER__" if i % 4 == 0 else "__TEAL__", (i % 8) * 0.5))
    css = """<style>.p{animation:fl 6s ease-in-out infinite}
    @keyframes fl{0%,100%{transform:translateY(0);opacity:.2}50%{transform:translateY(-10px);opacity:.9}}</style>"""
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="particle divider">
  __DEFS__ __CSS__ <g filter="url(#glow)">__PS__</g>
</svg>"""
    save("dividers/divider-particles.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css).replace("__PS__", ps))


def divider_fog():
    w, h = 1000, 80
    css = """<style>.f{animation:drift 12s ease-in-out infinite}
    @keyframes drift{0%,100%{transform:translateX(-40px);opacity:.12}50%{transform:translateX(40px);opacity:.28}}
    .f2{animation:drift2 16s ease-in-out infinite}
    @keyframes drift2{0%,100%{transform:translateX(30px);opacity:.1}50%{transform:translateX(-30px);opacity:.22}}</style>"""
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="fog divider">
  __DEFS__ __CSS__
  <ellipse class="f"  cx="380" cy="46" rx="360" ry="26" fill="__TEAL__" filter="url(#softGlow)"/>
  <ellipse class="f2" cx="680" cy="40" rx="320" ry="22" fill="__TEALD__" filter="url(#softGlow)"/>
  <line x1="0" y1="62" x2="__W__" y2="62" stroke="__LINE__" stroke-width="1"/>
</svg>"""
    save("dividers/divider-fog.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css))


def divider_neon():
    w, h = 1000, 30
    css = """<style>.g{animation:gl 3s ease-in-out infinite}
    @keyframes gl{0%,100%{opacity:.5}50%{opacity:1}}</style>"""
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="neon divider">
  __DEFS__ __CSS__
  <line class="g" x1="120" y1="15" x2="880" y2="15" stroke="url(#fade)" stroke-width="2" filter="url(#glow)"/>
  <polygon class="g" points="500,6 512,15 500,24 488,15" fill="__AMBER__" filter="url(#glow)"/>
</svg>"""
    save("dividers/divider-neon.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css))


def divider_stars():
    w, h = 1000, 70
    st = "".join(
        '<circle class="st" cx="%d" cy="%d" r="%.1f" fill="__TEALG__" style="animation-delay:-%ss"/>'
        % ((i * 139) % w, 8 + (i * 53) % 54, 0.7 + (i % 3) * 0.5, (i % 7) * 0.5)
        for i in range(50))
    css = """<style>.st{animation:tw 3s ease-in-out infinite}
    @keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}</style>"""
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="stars divider">
  __DEFS__ __CSS__ <g>__ST__</g>
</svg>"""
    save("dividers/divider-stars.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css).replace("__ST__", st))


# ----------------------------------------------------------------------------
# PROJECT BANNER
# ----------------------------------------------------------------------------
def project_banner(key, codename, title, subtitle, tags, status, accent="__TEAL__"):
    w, h = 1000, 200
    chips = ""
    x = 34
    for t in tags:
        cw = 20 + len(t) * 9
        chips += ('<g transform="translate(%d,150)">'
                  '<rect width="%d" height="26" rx="13" fill="__SURF2__" stroke="__LINE__"/>'
                  '<text x="%d" y="17" font="500 12px __MONO__" fill="__MUTE__" text-anchor="middle" '
                  'font-family=%s font-size="12">%s</text></g>'
                  % (x, cw, cw // 2, repr(MONO), t))
        x += cw + 10
    css = """
  <style>
    .code{font:600 13px __MONO__;letter-spacing:5px;fill:__ACCENT__}
    .ttl{font:800 40px __SANS__;letter-spacing:1px;fill:__TEXT__}
    .sub{font:400 16px __SANS__;fill:__MUTE__}
    .live{animation:bp 1.8s ease-in-out infinite}
    @keyframes bp{0%,100%{opacity:.4;r:5}50%{opacity:1;r:7}}
    .scan{animation:sc 7s linear infinite}
    @keyframes sc{0%{transform:translateX(-1000px)}100%{transform:translateX(1000px)}}
  </style>
"""
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="__TTL__ project banner">
  __DEFS__ __CSS__
  <rect x="1" y="1" width="998" height="198" rx="16" fill="__SURF__" stroke="__LINE__"/>
  <rect x="1" y="1" width="998" height="198" rx="16" fill="url(#bgGrad)" opacity="0.5"/>
  __SCAN__
  <rect class="scan" x="0" y="0" width="200" height="__H__" fill="__ACCENT__" opacity="0.04"/>
  <rect x="0" y="0" width="5" height="__H__" fill="__ACCENT__" filter="url(#glow)"/>
  <!-- corner ticks -->
  <path d="M978 16 h6 v6 M978 184 h6 v-6" stroke="__ACCENT__" stroke-width="2" fill="none" opacity="0.7"/>
  <text class="code" x="34" y="46">__CODE__</text>
  <text class="ttl"  x="32" y="92" filter="url(#glow)">__TTL__</text>
  <text class="sub"  x="34" y="122">__SUB__</text>
  <g transform="translate(820,38)">
    <circle class="live" cx="8" cy="6" r="6" fill="__ACCENT__" filter="url(#glow)"/>
    <text x="24" y="11" font-family=__MONOQ__ font-size="12" letter-spacing="2" fill="__ACCENT__">__STATUS__</text>
  </g>
  __CHIPS__
</svg>
"""
    svg = (svg.replace("__W__", str(w)).replace("__H__", str(h))
           .replace("__DEFS__", defs()).replace("__CSS__", css)
           .replace("__SCAN__", scanlines(w, h, "0.05"))
           .replace("__CODE__", codename).replace("__TTL__", title)
           .replace("__SUB__", subtitle).replace("__STATUS__", status)
           .replace("__CHIPS__", chips).replace("__ACCENT__", accent)
           .replace("__MONOQ__", repr(MONO))
           .replace("__SANS__", SANS).replace("__MONO__", MONO))
    save("projects/%s-banner.svg" % key, svg)


# ----------------------------------------------------------------------------
# ARCHITECTURE DIAGRAMS  (custom per project)
# ----------------------------------------------------------------------------
def _box(x, y, w, h, title, sub="", accent="__TEAL__"):
    g = '<g transform="translate(%d,%d)">' % (x, y)
    g += '<rect width="%d" height="%d" rx="10" fill="__SURF2__" stroke="%s" stroke-opacity="0.6"/>' % (w, h, accent)
    g += '<rect width="4" height="%d" rx="2" fill="%s"/>' % (h, accent)
    g += ('<text x="%d" y="%d" text-anchor="middle" font-family=%s font-size="15" '
          'font-weight="700" fill="__TEXT__">%s</text>' % (w // 2, 26 if sub else h // 2 + 5, repr(SANS), title))
    if sub:
        g += ('<text x="%d" y="46" text-anchor="middle" font-family=%s font-size="11" '
              'fill="__MUTE__">%s</text>' % (w // 2, repr(MONO), sub))
    g += "</g>"
    return g


def _arrow(x1, y1, x2, y2, label="", accent="__TEAL__", delay="0s"):
    a = ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6" '
         'stroke-opacity="0.55"/>' % (x1, y1, x2, y2, accent))
    a += ('<line class="flow" x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.2" '
          'stroke-dasharray="4 12" style="animation-delay:%s" filter="url(#glow)"/>'
          % (x1, y1, x2, y2, accent, delay))
    if label:
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2 - 6
        a += ('<text x="%d" y="%d" text-anchor="middle" font-family=%s font-size="10" '
              'fill="__MUTE__">%s</text>' % (mx, my, repr(MONO), label))
    return a


def arch_multiplexer():
    w, h = 1000, 440
    css = """<style>.flow{animation:fl 2.4s linear infinite}
    @keyframes fl{to{stroke-dashoffset:-160}}
    .hdr{font:700 15px __MONO__;letter-spacing:3px;fill:__AMBER__}</style>"""
    body = ""
    body += _box(40, 60, 150, 70, "Client", "any app / SDK", "__AMBER__")
    body += _box(260, 40, 200, 110, "Multiplexer", "routing gateway", "__TEAL__")
    body += ('<text x="360" y="118" text-anchor="middle" font-family=%s font-size="10" '
             'fill="__MUTE__">LinUCB bandit &#183; semantic cache</text>' % repr(MONO))
    body += _box(300, 200, 120, 44, "Circuit breaker", "", "__TEAL__")
    body += _box(560, 30, 170, 46, "GPT-class", "", "__TEALD__")
    body += _box(560, 96, 170, 46, "Frontier-class", "", "__TEALD__")
    body += _box(560, 162, 170, 46, "Open / local", "", "__TEALD__")
    body += _box(800, 96, 160, 70, "Best answer", "min cost + latency", "__AMBER__")
    body += _box(300, 300, 400, 60, "Reward loop", "log latency + cost + quality -> update policy per request", "__AMBER__")
    body += _arrow(190, 95, 260, 95, "request")
    body += _arrow(460, 78, 560, 53, "score", "__TEAL__", "-.4s")
    body += _arrow(460, 95, 560, 119, "score", "__TEAL__", "-.8s")
    body += _arrow(460, 112, 560, 185, "score", "__TEAL__", "-1.2s")
    body += _arrow(730, 53, 800, 120, "", "__TEALG__", "-.2s")
    body += _arrow(730, 119, 800, 131, "", "__TEALG__", "-.6s")
    body += _arrow(730, 185, 800, 142, "", "__TEALG__", "-1s")
    body += _arrow(360, 150, 360, 200, "fallback", "__TEAL__")
    body += _arrow(880, 166, 880, 330, "", "__AMBER__", "-.5s")
    body += _arrow(700, 330, 500, 330, "learn", "__AMBER__", "-.3s")
    body += _arrow(300, 330, 130, 130, "policy", "__AMBER__", "-.9s")
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Multiplexer architecture">
  __DEFS__ __CSS__
  <rect width="__W__" height="__H__" rx="14" fill="__BG__" stroke="__LINE__"/>
  __SCAN__
  <text class="hdr" x="40" y="34">MULTIPLEXER - ONLINE MODEL ROUTING</text>
  __BODY__
</svg>"""
    save("projects/multiplexer-arch.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css)
         .replace("__SCAN__", scanlines(w, h, "0.03"))
         .replace("__BODY__", body).replace("__SANS__", SANS).replace("__MONO__", MONO))


def arch_christopher():
    w, h = 1000, 440
    css = """<style>.flow{animation:fl 2.4s linear infinite}
    @keyframes fl{to{stroke-dashoffset:-160}}
    .hdr{font:700 15px __MONO__;letter-spacing:3px;fill:__AMBER__}
    .wave{animation:wv 1.6s ease-in-out infinite}
    @keyframes wv{0%,100%{transform:scaleY(.4)}50%{transform:scaleY(1)}}</style>"""
    body = ""
    body += _box(40, 70, 150, 80, "Learner", "mic + speaker", "__AMBER__")
    # waveform glyph
    wf = '<g transform="translate(70,180)">'
    for i in range(9):
        wf += ('<rect class="wave" x="%d" y="-14" width="4" height="28" rx="2" fill="__TEAL__" '
               'style="transform-origin:center;animation-delay:-%ss"/>' % (i * 9, i * 0.13))
    wf += "</g>"
    body += wf
    body += _box(260, 60, 180, 100, "WebRTC", "low-latency audio", "__TEAL__")
    body += _box(500, 40, 200, 140, "Realtime API", "speech-to-speech", "__TEAL__")
    body += ('<text x="600" y="120" text-anchor="middle" font-family=%s font-size="10" '
             'fill="__MUTE__">180+ languages</text>' % repr(MONO))
    body += _box(760, 30, 200, 56, "Pronunciation score", "", "__TEALD__")
    body += _box(760, 100, 200, 56, "Live transcript", "", "__TEALD__")
    body += _box(500, 250, 200, 70, "Memory store", "recall across sessions", "__AMBER__")
    body += _box(260, 250, 180, 70, "Session state", "context + progress", "__AMBER__")
    body += _arrow(190, 110, 260, 110, "audio")
    body += _arrow(440, 110, 500, 110, "stream", "__TEAL__", "-.4s")
    body += _arrow(700, 90, 760, 58, "", "__TEALG__", "-.3s")
    body += _arrow(700, 130, 760, 128, "", "__TEALG__", "-.7s")
    body += _arrow(600, 180, 600, 250, "persist", "__AMBER__")
    body += _arrow(500, 285, 440, 285, "", "__AMBER__", "-.5s")
    body += _arrow(350, 250, 350, 160, "context", "__AMBER__", "-.9s")
    body += _arrow(600, 320, 600, 380, "", "__AMBER__", "-.2s")
    body += _arrow(600, 380, 115, 380, "next lesson", "__AMBER__", "-.6s")
    body += _arrow(115, 380, 115, 150, "", "__AMBER__", "-1s")
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Christopher architecture">
  __DEFS__ __CSS__
  <rect width="__W__" height="__H__" rx="14" fill="__BG__" stroke="__LINE__"/>
  __SCAN__
  <text class="hdr" x="40" y="34">CHRISTOPHER - REAL-TIME VOICE TUTOR</text>
  __BODY__
</svg>"""
    save("projects/christopher-arch.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css)
         .replace("__SCAN__", scanlines(w, h, "0.03"))
         .replace("__BODY__", body).replace("__SANS__", SANS).replace("__MONO__", MONO))


# ----------------------------------------------------------------------------
# TECH LABORATORY CARDS
# ----------------------------------------------------------------------------
def lab_card(key, title, items, accent="__TEAL__"):
    w = 470
    rows = (len(items) + 1) // 2
    h = 92 + rows * 30
    css = """
  <style>
    .h{font:700 18px __SANS__;letter-spacing:1px;fill:__TEXT__}
    .k{font:600 11px __MONO__;letter-spacing:4px;fill:__ACCENT__}
    .it{font:500 14px __MONO__;fill:__MUTE__}
    .dot{animation:p 2.4s ease-in-out infinite}
    @keyframes p{0%,100%{opacity:.4}50%{opacity:1}}
  </style>
"""
    body = ""
    for i, it in enumerate(items):
        col = i % 2
        row = i // 2
        ix = 34 + col * 215
        iy = 108 + row * 30
        body += ('<circle class="dot" cx="%d" cy="%d" r="3" fill="__ACCENT__" style="animation-delay:-%ss"/>'
                 % (ix, iy - 4, (i % 5) * 0.4))
        body += '<text class="it" x="%d" y="%d">%s</text>' % (ix + 12, iy, it)
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="__T__ stack">
  __DEFS__ __CSS__
  <rect x="1" y="1" width="__W1__" height="__H1__" rx="14" fill="__SURF__" stroke="__LINE__"/>
  <rect x="1" y="1" width="__W1__" height="__H1__" rx="14" fill="url(#bgGrad)" opacity="0.4"/>
  __SCAN__
  <rect x="0" y="0" width="4" height="__H__" fill="__ACCENT__" filter="url(#glow)"/>
  <text class="k" x="30" y="36">__K__</text>
  <text class="h" x="28" y="66" filter="url(#glow)">__T__</text>
  <line x1="28" y1="82" x2="__LX__" y2="82" stroke="__LINE__"/>
  __BODY__
</svg>
"""
    svg = (svg.replace("__W1__", str(w - 2)).replace("__H1__", str(h - 2))
           .replace("__W__", str(w)).replace("__H__", str(h))
           .replace("__LX__", str(w - 30))
           .replace("__DEFS__", defs()).replace("__CSS__", css)
           .replace("__SCAN__", scanlines(w, h, "0.04"))
           .replace("__K__", "LAB // " + key.upper()).replace("__T__", title)
           .replace("__BODY__", body).replace("__ACCENT__", accent)
           .replace("__SANS__", SANS).replace("__MONO__", MONO))
    save("lab/lab-%s.svg" % key, svg)


# ----------------------------------------------------------------------------
# EXPERIMENTS CONSOLE
# ----------------------------------------------------------------------------
def experiments():
    w, h = 1000, 320
    rows = [
        ("Team workspace + operational agent", 60, "__AMBER__"),
        ("Decisions and actions as a durable record", 52, "__TEAL__"),
        ("Agent execution across business tools", 44, "__TEAL__"),
        ("Voice-native agents", 70, "__AMBER__"),
    ]
    css = """
  <style>
    .hdr{font:700 15px __MONO__;letter-spacing:3px;fill:__AMBER__}
    .lbl{font:500 15px __MONO__;fill:__TEXT__}
    .pct{font:600 13px __MONO__;fill:__MUTE__}
    .fill{animation:load 2.4s ease-out forwards;transform-origin:left}
    @keyframes load{from{transform:scaleX(0)}to{transform:scaleX(1)}}
    .cur{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}
    .dot{animation:p 1.8s ease-in-out infinite}@keyframes p{0%,100%{opacity:.4}50%{opacity:1}}
  </style>
"""
    body = ""
    y = 96
    for i, (name, pct, col) in enumerate(rows):
        bw = 620
        body += '<circle class="dot" cx="40" cy="%d" r="4" fill="%s" style="animation-delay:-%ss"/>' % (y - 4, col, i * 0.4)
        body += '<text class="lbl" x="56" y="%d">%s</text>' % (y, name)
        body += '<rect x="700" y="%d" width="%d" height="8" rx="4" fill="__SURF2__"/>' % (y - 10, bw and 220)
        body += ('<rect class="fill" x="700" y="%d" width="%d" height="8" rx="4" fill="%s" '
                 'style="transform:scaleX(%.2f);animation-delay:%ss" filter="url(#glow)"/>'
                 % (y - 10, 220, col, pct / 100, 0.2 + i * 0.2))
        body += '<text class="pct" x="932" y="%d">%d%%</text>' % (y, pct)
        y += 52
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Active research console">
  __DEFS__ __CSS__
  <rect width="__W__" height="__H__" rx="14" fill="__BG__" stroke="__LINE__"/>
  __SCAN__
  <circle cx="26" cy="26" r="5" fill="#ff5f56"/><circle cx="46" cy="26" r="5" fill="__AMBER__"/><circle cx="66" cy="26" r="5" fill="__TEAL__"/>
  <text class="hdr" x="92" y="31">research://active</text>
  <line x1="0" y1="52" x2="__W__" y2="52" stroke="__LINE__"/>
  <text class="lbl" x="40" y="80" fill="__AMBER__" font-size="13">ACTIVE RESEARCH<tspan class="cur"> &#9608;</tspan></text>
  __BODY__
</svg>"""
    save("experiments/console.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css)
         .replace("__SCAN__", scanlines(w, h, "0.03"))
         .replace("__BODY__", body).replace("__SANS__", SANS).replace("__MONO__", MONO))


# ----------------------------------------------------------------------------
# INTERACTIVE TERMINAL  (staggered typing reveal)
# ----------------------------------------------------------------------------
def terminal():
    w, h = 1000, 452
    lines = [
        ("$ whoami", "__TEAL__"),
        ("manas.borole // AI engineer, building things that people use", "__TEXT__"),
        ("$ current_focus", "__TEAL__"),
        ("an AI team workspace where decisions and actions become a record", "__TEXT__"),
        ("an embedded agent then executes across business tools, with approval", "__TEXT__"),
        ("$ currently_building", "__TEAL__"),
        ("structured collaboration + safe, traceable automation", "__TEXT__"),
        ("$ stack --top", "__TEAL__"),
        ("typescript &#183; node &#183; java/spring &#183; python &#183; postgres", "__TEXT__"),
        ("$ available_for", "__TEAL__"),
        ("hard problems &#183; ambitious products &#183; AI systems", "__AMBER__"),
        ("$ next_goal", "__TEAL__"),
        ("a company of my own, built around the workspace and its agent", "__AMBER__"),
        ("$ _", "__TEAL__"),
    ]
    # each line fades/reveals in sequence
    css = """
  <style>
    .l{font:500 16px __MONO__;opacity:0;animation:show .01s linear forwards}
    @keyframes show{to{opacity:1}}
    .cur{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}
    .hdr{font:600 13px __MONO__;letter-spacing:2px;fill:__MUTE__}
  </style>
"""
    body = ""
    y = 92
    for i, (txt, col) in enumerate(lines):
        delay = 0.5 + i * 0.55
        cur = '<tspan class="cur" fill="__AMBER__">&#9608;</tspan>' if i == len(lines) - 1 else ""
        body += ('<text class="l" x="34" y="%d" fill="%s" style="animation-delay:%ss">%s%s</text>'
                 % (y, col, delay, txt, cur))
        y += 26
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Interactive terminal">
  __DEFS__ __CSS__
  <rect width="__W__" height="__H__" rx="14" fill="#080d10" stroke="__LINE__"/>
  <rect width="__W__" height="46" rx="14" fill="__SURF__"/>
  <rect y="30" width="__W__" height="16" fill="__SURF__"/>
  <circle cx="26" cy="23" r="5" fill="#ff5f56"/><circle cx="46" cy="23" r="5" fill="__AMBER__"/><circle cx="66" cy="23" r="5" fill="__TEAL__"/>
  <text class="hdr" x="__MID__" y="28" text-anchor="middle">visitor@github - manas.borole - zsh</text>
  __SCAN__
  __BODY__
</svg>"""
    save("terminal/terminal.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h)).replace("__MID__", str(w // 2))
         .replace("__DEFS__", defs()).replace("__CSS__", css)
         .replace("__SCAN__", scanlines(w, h, "0.04"))
         .replace("__BODY__", body).replace("__SANS__", SANS).replace("__MONO__", MONO),
         adaptive=False)


# ----------------------------------------------------------------------------
# TIMELINE
# ----------------------------------------------------------------------------
def timeline():
    w, h = 900, 560
    nodes = [
        ("2020", "First lines of code", "B.Tech in AI/ML begins. Curiosity ahead of the syllabus.", "__TEAL__"),
        ("2022", "Founder, B&amp;B Fashion", "Ran a real business end to end. Learned what shipping costs.", "__AMBER__"),
        ("2023", "Co-founder, Gullak", "Investing platform for first-timers. Owned scope and delivery.", "__AMBER__"),
        ("2024", "Software Engineer, IQCPL", "Certification and audit platform. Java, Spring, React, Postgres, at scale.", "__TEAL__"),
        ("2026", "AI, shipped", "Multiplexer and Christopher live in production. Voice, routing, memory.", "__TEAL__"),
        ("Next", "A company of my own", "A team workspace where collaboration and an operational AI agent run as one system.", "__AMBER__"),
    ]
    css = """
  <style>
    .yr{font:700 15px __MONO__;letter-spacing:2px}
    .tt{font:700 19px __SANS__;fill:__TEXT__}
    .ds{font:400 13px __SANS__;fill:__MUTE__}
    .ln{stroke-dasharray:4 8;animation:m 6s linear infinite}
    @keyframes m{to{stroke-dashoffset:-120}}
    .nd{animation:np 2.6s ease-in-out infinite}
    @keyframes np{0%,100%{opacity:.6}50%{opacity:1}}
  </style>
"""
    body = '<line x1="60" y1="40" x2="60" y2="520" stroke="__LINE__" stroke-width="2"/>'
    body += '<line class="ln" x1="60" y1="40" x2="60" y2="520" stroke="__TEAL__" stroke-width="2" filter="url(#glow)"/>'
    y = 60
    for i, (yr, title, desc, col) in enumerate(nodes):
        body += '<circle class="nd" cx="60" cy="%d" r="8" fill="__BG__" stroke="%s" stroke-width="2.5" style="animation-delay:-%ss" filter="url(#glow)"/>' % (y, col, i * 0.4)
        body += '<circle cx="60" cy="%d" r="3" fill="%s"/>' % (y, col)
        body += '<text class="yr" x="100" y="%d" fill="%s">%s</text>' % (y - 6, col, yr)
        body += '<text class="tt" x="100" y="%d">%s</text>' % (y + 16, title)
        body += '<text class="ds" x="100" y="%d">%s</text>' % (y + 38, desc)
        y += 82
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Engineering timeline">
  __DEFS__ __CSS__
  <rect width="__W__" height="__H__" fill="__BG__"/>
  __SCAN__
  __BODY__
</svg>"""
    save("timeline/timeline.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css)
         .replace("__SCAN__", scanlines(w, h, "0.03"))
         .replace("__BODY__", body).replace("__SANS__", SANS).replace("__MONO__", MONO))


# ----------------------------------------------------------------------------
# ENGINEERING PRINCIPLES  (single contained panel, responsive at width=100%)
# ----------------------------------------------------------------------------
def principles():
    items = [
        "Understand the problem before writing the solution.",
        "Prefer clarity to cleverness. The next reader is you.",
        "Reliability is designed in, not added on later.",
        "Ship with intention. Every change should earn its place.",
        "Simple systems outlast complex ones. Complexity is a cost paid forever.",
    ]
    w, pad, rowh = 1000, 34, 62
    h = pad * 2 + len(items) * rowh
    css = """
  <style>
    .idx{font:700 13px __MONO__;letter-spacing:2px}
    .pr{font:600 20px __SANS__;fill:__TEXT__}
    .tick{animation:pl 2.8s ease-in-out infinite}
    @keyframes pl{0%,100%{opacity:.5}50%{opacity:1}}
  </style>
"""
    body = ""
    for i, text in enumerate(items):
        y = pad + i * rowh
        accent = "__TEAL__" if i % 2 == 0 else "__AMBER__"
        cy = y + rowh // 2
        body += ('<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="__SURF2__" '
                 'stroke="__LINE__"/>' % (pad, y, w - pad * 2, rowh - 14))
        body += '<rect class="tick" x="%d" y="%d" width="4" height="%d" rx="2" fill="%s" filter="url(#glow)"/>' % (pad, y, rowh - 14, accent)
        body += '<text class="idx" x="%d" y="%d" fill="%s">%02d</text>' % (pad + 22, cy - 3, accent, i + 1)
        body += '<text class="pr" x="%d" y="%d">%s</text>' % (pad + 66, cy - 2, text)
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Engineering principles">
  __DEFS__ __CSS__
  <rect width="__W__" height="__H__" rx="16" fill="__BG__"/>
  __SCAN__
  __BODY__
</svg>"""
    save("principles/principles.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css)
         .replace("__SCAN__", scanlines(w, h, "0.03"))
         .replace("__BODY__", body).replace("__SANS__", SANS).replace("__MONO__", MONO))


# ----------------------------------------------------------------------------
# COMPANION  (original geometric android assistant)
# ----------------------------------------------------------------------------
def companion(pose):
    w, h = 220, 260
    # base android bust: shoulders + head + visor slit + chest core
    css = """
  <style>
    .visor{animation:sc 3s ease-in-out infinite}
    @keyframes sc{0%,100%{opacity:.55}50%{opacity:1}}
    .core{animation:cp 2.2s ease-in-out infinite}
    @keyframes cp{0%,100%{opacity:.5;r:5}50%{opacity:1;r:7}}
    .float{animation:fl 4s ease-in-out infinite}
    @keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
    .blip{animation:bp 1.6s ease-in-out infinite}
    @keyframes bp{0%,100%{opacity:.2}50%{opacity:1}}
  </style>
"""
    S = "__TEAL__"
    # arm + accessory per pose
    extra = ""
    head_tf = "translate(0,0)"
    arm = ""
    if pose == "standing":
        arm = '<line x1="70" y1="170" x2="70" y2="215" stroke="%s" stroke-width="6" stroke-linecap="round"/><line x1="150" y1="170" x2="150" y2="215" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % (S, S)
    elif pose == "coding":
        arm = ('<line x1="70" y1="170" x2="88" y2="205" stroke="%s" stroke-width="6" stroke-linecap="round"/>'
               '<line x1="150" y1="170" x2="132" y2="205" stroke="%s" stroke-width="6" stroke-linecap="round"/>'
               '<rect x="80" y="205" width="60" height="26" rx="5" fill="__SURF2__" stroke="%s"/>' % (S, S, S))
        extra = ('<g class="float"><text x="150" y="70" font-family=%s font-size="16" fill="__AMBER__" class="blip">&lt;/&gt;</text></g>' % repr(MONO))
    elif pose == "thinking":
        head_tf = "rotate(-8 110 110)"
        arm = ('<line x1="70" y1="170" x2="70" y2="215" stroke="%s" stroke-width="6" stroke-linecap="round"/>'
               '<line x1="150" y1="170" x2="130" y2="120" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % (S, S))
        extra = ('<g class="float"><circle cx="165" cy="55" r="4" fill="__AMBER__" class="blip"/>'
                 '<circle cx="178" cy="40" r="6" fill="__AMBER__" class="blip" style="animation-delay:.4s"/>'
                 '<text x="172" y="30" font-family=%s font-size="14" fill="__AMBER__">?</text></g>' % repr(SANS))
    elif pose == "explaining":
        arm = ('<line x1="70" y1="170" x2="70" y2="215" stroke="%s" stroke-width="6" stroke-linecap="round"/>'
               '<line x1="150" y1="170" x2="185" y2="150" stroke="%s" stroke-width="6" stroke-linecap="round"/>'
               '<circle cx="188" cy="148" r="5" fill="%s"/>' % (S, S, S))
        extra = ('<path class="blip" d="M175 120 q25 25 0 60" stroke="__AMBER__" stroke-width="2" fill="none"/>')
    elif pose == "wave":
        arm = ('<line x1="70" y1="170" x2="70" y2="215" stroke="%s" stroke-width="6" stroke-linecap="round"/>'
               '<g class="float" style="transform-origin:150px 170px"><line x1="150" y1="170" x2="175" y2="120" stroke="%s" stroke-width="6" stroke-linecap="round"/>'
               '<circle cx="177" cy="116" r="6" fill="%s"/></g>' % (S, S, S))
        extra = ('<text x="150" y="90" font-family=%s font-size="13" fill="__AMBER__" class="blip">bye</text>' % repr(MONO))

    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="companion __POSE__">
  __DEFS__ __CSS__
  <g class="float">
    <!-- ground glow -->
    <ellipse cx="110" cy="248" rx="60" ry="8" fill="__TEAL__" opacity="0.15" filter="url(#softGlow)"/>
    <!-- shoulders / body -->
    <path d="M60 250 q0 -70 50 -74 q50 4 50 74 Z" fill="__SURF2__" stroke="__TEAL__" stroke-opacity="0.7"/>
    <circle class="core" cx="110" cy="205" r="6" fill="__AMBER__" filter="url(#glow)"/>
    __ARM__
    <!-- head -->
    <g transform="__HEADTF__">
      <rect x="76" y="70" width="68" height="82" rx="24" fill="__SURF__" stroke="__TEAL__" stroke-opacity="0.8"/>
      <rect x="76" y="70" width="68" height="82" rx="24" fill="none" stroke="__TEALG__" stroke-opacity="0.25"/>
      <!-- visor slit -->
      <rect class="visor" x="86" y="100" width="48" height="12" rx="6" fill="__TEAL__" filter="url(#glow)"/>
      <circle class="visor" cx="98" cy="106" r="2.5" fill="__BG__"/>
      <circle class="visor" cx="122" cy="106" r="2.5" fill="__BG__"/>
      <!-- antenna -->
      <line x1="110" y1="70" x2="110" y2="54" stroke="__TEAL__" stroke-width="2"/>
      <circle class="core" cx="110" cy="50" r="4" fill="__AMBER__" filter="url(#glow)"/>
    </g>
    __EXTRA__
  </g>
</svg>"""
    save("characters/companion-%s.svg" % pose,
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css)
         .replace("__ARM__", arm).replace("__EXTRA__", extra)
         .replace("__HEADTF__", head_tf).replace("__POSE__", pose)
         .replace("__SANS__", SANS).replace("__MONO__", MONO))


# ----------------------------------------------------------------------------
# PLACEHOLDER FRAMES  (so README never shows a broken image before real art)
# ----------------------------------------------------------------------------
def placeholder(relpath, w, h, label, sub, accent="__TEAL__"):
    css = """
  <style>
    .lb{font:700 22px __SANS__;letter-spacing:3px;fill:__MUTE__}
    .sb{font:500 12px __MONO__;letter-spacing:2px;fill:__ACCENT__}
    .scan{animation:sc 6s linear infinite}
    @keyframes sc{0%{transform:translateX(-__W__px)}100%{transform:translateX(__W__px)}}
  </style>
"""
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="__LB__ placeholder">
  __DEFS__ __CSS__
  <rect x="1" y="1" width="__W1__" height="__H1__" rx="14" fill="url(#bgGrad)" stroke="__LINE__"/>
  __SCAN__
  <rect class="scan" x="0" y="0" width="180" height="__H__" fill="__ACCENT__" opacity="0.05"/>
  <!-- crop marks -->
  <path d="M20 20 h30 M20 20 v30" stroke="__ACCENT__" stroke-width="2" fill="none" opacity="0.6"/>
  <path d="M__CR1__ 20 h-30 M__CR1__ 20 v30" stroke="__ACCENT__" stroke-width="2" fill="none" opacity="0.6"/>
  <path d="M20 __CB__ h30 M20 __CB__ v-30" stroke="__ACCENT__" stroke-width="2" fill="none" opacity="0.6"/>
  <path d="M__CR1__ __CB__ h-30 M__CR1__ __CB__ v-30" stroke="__ACCENT__" stroke-width="2" fill="none" opacity="0.6"/>
  <circle cx="__MIDX__" cy="__ICY__" r="26" fill="none" stroke="__ACCENT__" stroke-width="2" opacity="0.5"/>
  <path d="M__PX1__ __PY__ l14 10 l-14 10 Z" fill="__ACCENT__" opacity="0.7"/>
  <text class="sb" x="__MIDX__" y="__SBY__" text-anchor="middle">__SUB__</text>
  <text class="lb" x="__MIDX__" y="__LBY__" text-anchor="middle">__LB__</text>
</svg>"""
    svg = (svg.replace("__W1__", str(w - 2)).replace("__H1__", str(h - 2))
           .replace("__W__", str(w)).replace("__H__", str(h))
           .replace("__CR1__", str(w - 20)).replace("__CB__", str(h - 20))
           .replace("__MIDX__", str(w // 2)).replace("__ICY__", str(h // 2 - 26))
           .replace("__PX1__", str(w // 2 - 5)).replace("__PY__", str(h // 2 - 36))
           .replace("__SBY__", str(h // 2 + 24)).replace("__LBY__", str(h // 2 + 52))
           .replace("__DEFS__", defs()).replace("__CSS__", css)
           .replace("__SCAN__", scanlines(w, h, "0.03"))
           .replace("__LB__", label).replace("__SUB__", sub).replace("__ACCENT__", accent)
           .replace("__SANS__", SANS).replace("__MONO__", MONO))
    save(relpath, svg)


# ----------------------------------------------------------------------------
# ENDING SCENE
# ----------------------------------------------------------------------------
def ending():
    w, h = 1200, 300
    stars = "".join(
        '<circle class="star" cx="%d" cy="%d" r="%.1f" fill="__TEALG__" style="animation-delay:-%ss"/>'
        % ((i * 97) % w, 20 + (i * 61) % 150, 0.7 + (i % 3) * 0.4, (i % 8) * 0.5)
        for i in range(50))
    css = """
  <style>
    .star{animation:tw 3.4s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}
    .big{font:800 40px __SANS__;letter-spacing:3px;fill:__TEXT__}
    .sub{font:500 16px __MONO__;letter-spacing:3px;fill:__AMBER__}
    .cur{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}
  </style>
"""
    xs = list(range(0, w + 1, 50))
    heights = [70, 50, 90, 40, 80, 60, 100, 45, 85, 55, 95, 42, 78, 62, 98,
               48, 88, 52, 92, 44, 74, 64, 96, 46, 82]
    pts = "0,%d " % h
    for i, x in enumerate(xs):
        pts += "%d,%d " % (x, h - heights[i % len(heights)])
    pts += "%d,%d" % (w, h)
    svg = """
<svg viewBox="0 0 __W__ __H__" width="__W__" height="__H__" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ending scene">
  __DEFS__ __CSS__
  <rect width="__W__" height="__H__" fill="url(#bgGrad)"/>
  <g>__STARS__</g>
  <ellipse cx="600" cy="__H__" rx="600" ry="120" fill="__TEALD__" opacity="0.16" filter="url(#softGlow)"/>
  <polygon points="__PTS__" fill="#0a1418"/>
  __SCAN__
  <text class="sub" x="600" y="120" text-anchor="middle">// END OF LINE</text>
  <text class="big" x="600" y="168" text-anchor="middle" filter="url(#glow)">Let us build something real.<tspan class="cur" fill="__AMBER__">_</tspan></text>
</svg>"""
    save("backgrounds/ending-scene.svg",
         svg.replace("__W__", str(w)).replace("__H__", str(h))
         .replace("__DEFS__", defs()).replace("__CSS__", css)
         .replace("__STARS__", stars).replace("__PTS__", pts)
         .replace("__SCAN__", scanlines(w, h, "0.04"))
         .replace("__SANS__", SANS).replace("__MONO__", MONO),
         adaptive=False)


# ----------------------------------------------------------------------------
# RUN
# ----------------------------------------------------------------------------
def main():
    print("Generating assets ...")
    hero()

    for key, kick, title in [
        ("mission",     "01 // TRANSMISSION",     "Mission Statement"),
        ("current",     "02 // STATUS",           "Current Mission"),
        ("philosophy",  "03 // CORE",             "Engineering Philosophy"),
        ("projects",    "04 // BUILDS",           "Featured Projects"),
        ("architecture","05 // SCHEMATICS",       "Architecture Gallery"),
        ("lab",         "06 // INVENTORY",        "Tech Laboratory"),
        ("experiments", "07 // R&amp;D",          "Current Experiments"),
        ("timeline",    "08 // LOGS",             "Engineering Timeline"),
        ("terminal",    "09 // SHELL",            "Interactive Terminal"),
        ("principles",  "10 // DOCTRINE",         "Engineering Principles"),
        ("contact",     "11 // UPLINK",           "Contact"),
    ]:
        section_header(key, kick, title)

    divider_scanline(); divider_rain(); divider_particles()
    divider_fog(); divider_neon(); divider_stars()

    project_banner("multiplexer", "PROJECT // 001", "Multiplexer",
                   "An LLM gateway that learns, per request, which model to call.",
                   ["TypeScript", "Node", "LinUCB", "Semantic cache", "Live"],
                   "LIVE", "__TEAL__")
    project_banner("christopher", "PROJECT // 002", "Christopher",
                   "A voice tutor you can actually talk to, out loud, in real time.",
                   ["WebRTC", "Realtime API", "180+ langs", "Memory", "Live"],
                   "LIVE", "__AMBER__")
    arch_multiplexer(); arch_christopher()

    lab_card("core",     "Core &amp; Languages",  ["TypeScript", "JavaScript", "Java", "Python", "SQL", "Node.js"], "__TEAL__")
    lab_card("ai",       "AI / ML",           ["LLM systems", "OpenAI Realtime", "RAG", "Contextual bandits", "Prompt eng.", "Voice agents"], "__AMBER__")
    lab_card("backend",  "Backend",           ["Spring Boot", "Express", "REST APIs", "Auth / RBAC", "WebRTC", "Websockets"], "__TEAL__")
    lab_card("data",     "Databases",         ["PostgreSQL", "Prisma", "Neon", "Redis-style cache"], "__TEAL__")
    lab_card("frontend", "Frontend",          ["React", "Next.js", "Tailwind", "Zustand", "Framer Motion"], "__AMBER__")
    lab_card("infra",    "Infra &amp; Cloud",     ["Vercel", "Neon", "Clerk", "CI basics", "Observability"], "__TEAL__")
    lab_card("tools",    "Developer Tools",   ["Git", "Postman", "Linux", "VS Code", "Figma"], "__AMBER__")

    experiments()
    terminal()
    timeline()
    principles()

    for pose in ["standing", "coding", "thinking", "explaining", "wave"]:
        companion(pose)

    placeholder("projects/multiplexer-cover.svg", 1000, 480, "MULTIPLEXER", "SCREEN CAPTURE // routing dashboard", "__TEAL__")
    placeholder("projects/christopher-cover.svg", 1000, 480, "CHRISTOPHER", "SCREEN CAPTURE // live voice session", "__AMBER__")
    placeholder("projects/kazumi-thumb.svg", 480, 300, "KAZUMI", "AI wellbeing // team of 5", "__TEAL__")
    placeholder("projects/cryptchain-thumb.svg", 480, 300, "CRYPTCHAIN", "blockchain in pure Java", "__AMBER__")
    placeholder("projects/credit-thumb.svg", 480, 300, "CREDIT CLASSIFIER", "random forest // 85%+ acc", "__TEAL__")
    placeholder("projects/music-thumb.svg", 480, 300, "MUSIC RECS", "Spotify API // recommender", "__AMBER__")

    ending()
    print("Done.")


if __name__ == "__main__":
    main()
