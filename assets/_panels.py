"""Builds the animated panels for my profile README (Terminal M) and fills in the README template.

The profile is laid out like an airport: requests are flights, the router is air traffic control,
and the companion robot is the agent. Every panel is dark, so one file works in both GitHub themes.

Run from the repo root:  python assets/_panels.py
"""
import json, os, random, re, urllib.request
from collections import Counter

OUT = "assets/panels"
TPL = "assets/_readme.tpl.md"
BENCHMARK = "https://raw.githubusercontent.com/ManasBorole/Multiplexer/main/docs/data/benchmark.json"

BG, BG2, SURF, SURF2 = "#0A0E12", "#0D141A", "#121A20", "#16232B"
TEAL, TEALG, TEALD, AMBER, AMBERG = "#4CC9C0", "#7FE9DF", "#2C6E6A", "#E9A85A", "#F4C889"
TEXT, MUTE, LINE = "#E8EEEC", "#7E938C", "#20303A"
SANS = "font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "font-family:ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',monospace"
W = 840

DEFS = (f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<filter id="soft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="6"/></filter>'
        '<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" opacity=".025"/></pattern>')
BASE_CSS = (f"text{{{SANS}}}.m{{{MONO}}}.sig{{{MONO};font-size:11px;letter-spacing:3px;fill:{MUTE}}}"
            ".sweep{animation:sweep 7s linear infinite}@keyframes sweep{from{transform:translateY(-40px)}to{transform:translateY(600px)}}"
            ".pulse{animation:pulse 2.2s ease-in-out infinite}@keyframes pulse{50%{opacity:.35}}")


def panel(h, left, right, body, css="", defs=""):
    """Dark framed panel with corner brackets, scanlines and a slow light sweep."""
    br = lambda x, y, dx, dy, c: f'<path d="M{x},{y + dy * 18} L{x},{y} L{x + dx * 18},{y}" fill="none" stroke="{c}" stroke-width="1.6"/>'
    frame = (f'<rect width="{W}" height="{h}" rx="10" fill="url(#bg)"/><rect width="{W}" height="{h}" rx="10" fill="url(#scan)"/>'
             f'<rect class="sweep" x="0" y="0" width="{W}" height="40" fill="{TEAL}" opacity=".025"/>'
             + br(14, 14, 1, 1, TEAL) + br(W - 14, 14, -1, 1, TEAL) + br(14, h - 14, 1, -1, AMBER) + br(W - 14, h - 14, -1, -1, AMBER)
             + f'<text x="36" y="38" class="sig">{left}</text><text x="{W - 36}" y="38" class="sig" text-anchor="end">{right}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {h}" width="{W}" height="{h}">'
            f'<style>{BASE_CSS}{css}</style><defs>{DEFS}{defs}</defs><clipPath id="pc"><rect width="{W}" height="{h}" rx="10"/></clipPath>'
            f'<g clip-path="url(#pc)">{frame}{body}</g></svg>')


def appear(name, el, t, T):
    """Returns (svg, css): el fades in whole at t seconds into a T-second loop and stays until the loop resets."""
    a, b, z = 100 * t / T, 100 * (t + .25) / T, 100 * (T - .4) / T
    return (f'<g class="{name}">{el}</g>',
            f".{name}{{opacity:0;animation:{name} {T}s infinite}}@keyframes {name}{{0%,{a:.3f}%{{opacity:0}}{b:.3f}%,{z:.3f}%{{opacity:1}}100%{{opacity:0}}}}")


def robot(carry=False, wave=False):
    """The companion robot, drawn in a 220x260 box so it can be placed and scaled."""
    arm_r = (f'<g class="wave" style="transform-origin:150px 172px"><line x1="150" y1="172" x2="176" y2="128" stroke="{TEAL}" stroke-width="6" stroke-linecap="round"/></g>'
             if wave else f'<line x1="150" y1="170" x2="150" y2="215" stroke="{TEAL}" stroke-width="6" stroke-linecap="round"/>')
    doc = (f'<g transform="translate(120,180) rotate(-6)"><rect width="56" height="68" rx="4" fill="{TEXT}"/>'
           + "".join(f'<rect x="8" y="{12 + k * 11}" width="{40 - (k % 2) * 12}" height="4" rx="2" fill="{MUTE}"/>' for k in range(5))
           + f'<text x="28" y="9" font-size="7" text-anchor="middle" fill="{BG}" class="m">PO</text></g>') if carry else ""
    return (f'<ellipse cx="110" cy="252" rx="60" ry="8" fill="{TEAL}" opacity=".18" filter="url(#soft)"/>'
            f'<g class="bob"><path d="M60 250 q0 -70 50 -74 q50 4 50 74 Z" fill="{SURF2}" stroke="{TEAL}" stroke-opacity=".7"/>'
            f'<circle class="pulse" cx="110" cy="205" r="6" fill="{AMBER}" filter="url(#glow)"/>'
            f'<line x1="70" y1="170" x2="70" y2="215" stroke="{TEAL}" stroke-width="6" stroke-linecap="round"/>{arm_r}'
            f'<rect x="76" y="70" width="68" height="82" rx="24" fill="{SURF}" stroke="{TEAL}" stroke-opacity=".8"/>'
            f'<rect class="pulse" x="86" y="100" width="48" height="12" rx="6" fill="{TEAL}" filter="url(#glow)"/>'
            f'<circle cx="98" cy="106" r="2.5" fill="{BG}"/><circle cx="122" cy="106" r="2.5" fill="{BG}"/>'
            f'<line x1="110" y1="70" x2="110" y2="54" stroke="{TEAL}" stroke-width="2"/>'
            f'<circle class="pulse" cx="110" cy="50" r="4" fill="{AMBER}" filter="url(#glow)"/>{doc}</g>')


ROBOT_CSS = (".bob{animation:bob 1.1s ease-in-out infinite}@keyframes bob{50%{transform:translateY(-5px)}}"
             ".wave{animation:wv 1.4s ease-in-out infinite}@keyframes wv{50%{transform:rotate(-28deg)}}")


# ------------------------------------------------------------------ departures board, flips on a loop like a real one
def board():
    rows = [("NOW", "UK REGTECH FINTECH", "ON AIR", TEAL), ("BUILDING", "BACKCHANNEL", "BOARDING", AMBER),
            ("SHIPPING", "ODYSSEY", "BOARDING", AMBER), ("LEARNING", "VOICE AI REAL LATENCY", "IN FLIGHT", AMBER),
            ("OPEN FOR", "PROBLEMS THAT SHIP", "ON TIME", TEAL)]
    cw, ch, gap, P = 18, 30, 3, 16.0
    rnd = random.Random(7)
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    out, t = [], .3

    def flap(x, y, c, delay, col):
        s = (f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="2.5" fill="#141b21"/>'
             f'<rect x="{x}" y="{y + ch / 2 - .5}" width="{cw}" height="1" fill="#05080a"/>')
        if c == " ":
            return s
        for k in range(3):
            s += f'<text x="{x + cw / 2}" y="{y + ch - 8}" class="fc sc" fill="#56646a" style="animation-delay:{delay + k * .07:.2f}s">{rnd.choice(abc)}</text>'
        return s + f'<text x="{x + cw / 2}" y="{y + ch - 8}" class="fc fi" fill="{col}" style="animation-delay:{delay + .21:.2f}s">{c}</text>'

    def line(x, y, text, n, col):
        nonlocal t
        s = "".join(flap(x + i * (cw + gap), y, text.ljust(n)[i], t + i * .03, col) for i in range(n))
        t += .1
        return s

    out.append(f'<text x="36" y="104" font-size="40" font-weight="800" fill="{TEXT}" letter-spacing="2" filter="url(#glow)" class="m">MANAS BOROLE</text>'
               f'<text x="38" y="128" font-size="14" fill="{MUTE}">AI engineer in Pune. Real-time voice, model routing, and the systems under them.</text>')
    out.append(f'<text x="36" y="184" class="sig">FLIGHT</text><text x="{36 + 9 * (cw + gap)}" y="184" class="sig">DESTINATION</text>'
               f'<text x="{W - 36}" y="184" class="sig" text-anchor="end">STATUS</text>')
    for i, (a, b, c, col) in enumerate(rows):
        y = 204 + i * 42
        out.append(line(36, y, a, 8, TEXT) + line(36 + 9 * (cw + gap), y, b, 21, TEXT))
        out.append(f'<circle cx="{W - 152}" cy="{y + 15}" r="4" fill="{col}" class="pulse" filter="url(#glow)"/>'
                   f'<text x="{W - 36}" y="{y + 20}" class="m fi" font-size="13" letter-spacing="2" fill="{col}" text-anchor="end" style="animation-delay:{t:.2f}s">{c}</text>')
    css = (f".fc{{{MONO};font-size:19px;font-weight:700;text-anchor:middle}}"
           f".sc{{opacity:0;animation:sc {P}s steps(1,end) infinite}}@keyframes sc{{0%{{opacity:1}}.45%,100%{{opacity:0}}}}"
           f".fi{{opacity:0;animation:fi {P}s infinite}}@keyframes fi{{0%{{opacity:0}}.1%,94%{{opacity:1}}96%,100%{{opacity:0}}}}")
    return panel(432, "DEPARTURES  /  TERMINAL M", "GATE 01", "".join(out), css)


ALT = {
    "board": 'Departures board for Manas Borole, flipping on a loop. Now: UK RegTech fintech. Building: Backchannel. Shipping: Odyssey. Learning: voice AI at real latency. Open for: problems that ship.'}


PANELS = {
        "board": lambda: board(),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, build in PANELS.items():
        with open(f"{OUT}/{name}.svg", "w", encoding="utf-8") as f:
            f.write(build())
    if os.path.exists(TPL):
        md = open(TPL, encoding="utf-8").read()
        md = re.sub(r"\{\{(\w+)\}\}", lambda m: f'<img src="{OUT}/{m[1]}.svg" width="100%" alt="{ALT[m[1]]}">', md)
        open("README.md", "w", encoding="utf-8").write(md)


if __name__ == "__main__":
    main()
