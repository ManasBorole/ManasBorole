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


def load_benchmark():
    """Multiplexer's own benchmark: the real routing code over 500 requests, with simulated model answers."""
    run = json.loads(urllib.request.urlopen(BENCHMARK, timeout=30).read())["runsData"][0]
    return run, run["rows"]


def short(model):
    n = model.split("/")[1].replace(":free", "")
    return n if len(n) <= 26 else n[:25] + "\u2026"


# ------------------------------------------------------------------ air traffic control: Multiplexer's 500 real decisions
def atc(run, rows):
    H, X0, X1, R0, RH = 540, 290, 800, 116, 18
    S0, S1, PLAY, HOLD = 396, 466, 22, 5
    n, T = len(rows), PLAY + HOLD
    x = lambda i: X0 + (X1 - X0) * i / n
    order = [m for m, _ in Counter(r["model"] for r in rows).most_common()]
    y = {m: R0 + k * RH for k, m in enumerate(order)}
    off, m_off = run["offlineAt"], run["offlineModel"]
    pct = lambda s: f"{100 * s / T:.3f}%"
    at = lambda i: 100 * (i / n) * PLAY / T

    b = []
    for m in order:
        b.append(f'<rect x="{X0}" y="{y[m] - 6}" width="{X1 - X0}" height="12" rx="2" fill="{SURF}" opacity=".7"/>'
                 f'<line x1="{X0 + 4}" y1="{y[m]}" x2="{X1 - 4}" y2="{y[m]}" stroke="{LINE}" stroke-dasharray="6 6"/>'
                 f'<text x="{X0 - 14}" y="{y[m] + 4}" class="m" font-size="11" fill="{MUTE}" text-anchor="end">{short(m)}</text>')
    marks = "".join(f'<rect x="{x(i):.1f}" y="{y[r["model"]] - 4}" width="1.2" height="8" fill="{TEALG}"/>' for i, r in enumerate(rows))
    fl, ro, cf, cr = [], [], 0, 0
    tot = sum(r["flagshipCost"] for r in rows)
    for i, r in enumerate(rows):
        cf += r["flagshipCost"]; cr += r["cost"]
        if i % 5 == 4 or i == n - 1:
            fl.append((x(i + 1), S1 - (S1 - S0) * cf / tot)); ro.append((x(i + 1), S1 - (S1 - S0) * cr / tot))
    P = lambda pts: "M" + " L".join(f"{a:.1f},{c:.1f}" for a, c in pts)
    xo = x(off)
    reveal = (marks
              + f'<path d="{P([(X0, S1)] + fl)}" fill="none" stroke="{MUTE}" stroke-width="1.5" stroke-dasharray="4 4"/>'
              + f'<path d="{P([(X0, S1)] + ro + [(X1, S1)])}" fill="{AMBER}" opacity=".15"/>'
              + f'<path d="{P([(X0, S1)] + ro)}" fill="none" stroke="{AMBER}" stroke-width="2.2" filter="url(#glow)"/>'
              + f'<line x1="{xo:.1f}" y1="{R0 - 12}" x2="{xo:.1f}" y2="{S1}" stroke="{AMBER}" stroke-dasharray="2 3"/>')
    ly = y[order[6]]
    sec = lambda xx: (xx - X0) / (X1 - X0) * PLAY
    labels = [
        ("la", f'<text x="{X0 + 30}" y="{ly}" font-size="12" fill="{TEXT}">tries every runway once, then</text>'
               f'<text x="{X0 + 30}" y="{ly + 16}" font-size="12" fill="{MUTE}">one model wins on value for this</text>'
               f'<text x="{X0 + 30}" y="{ly + 32}" font-size="12" fill="{MUTE}">prompt mix, so it earns the traffic</text>', sec(X0 + 30) + .6),
        ("lb", f'<text x="{xo + 12:.1f}" y="{ly}" font-size="12" fill="{TEXT}">runway closed. nothing fails:</text>'
               f'<text x="{xo + 12:.1f}" y="{ly + 16}" font-size="12" fill="{MUTE}">it spreads across three runways,</text>'
               f'<text x="{xo + 12:.1f}" y="{ly + 32}" font-size="12" fill="{MUTE}">then settles within ~50 flights</text>', sec(xo) + .3),
        ("lc", f'<text x="{X1}" y="{fl[-1][1] - 8:.1f}" font-size="12" fill="{MUTE}" text-anchor="end">every request on the flagship: ${tot:.2f}</text>'
               f'<text x="{X1}" y="{S1 - 10}" font-size="12" font-weight="700" fill="{AMBERG}" text-anchor="end">routed: ${cr:.2f}, {100 * cr / tot:.0f}% of that</text>', PLAY)]
    lab_svg, lab_css = "", ""
    for nm, el, t in labels:
        a_, b_ = appear(nm, el, t, T)
        lab_svg += a_; lab_css += b_
    # the closed runway gets a stamp the moment the playhead reaches it
    stamp = (f'<g class="stamp" style="transform-origin:{xo + 70:.0f}px {y[m_off]}px">'
             f'<rect x="{xo + 14:.0f}" y="{y[m_off] - 12}" width="118" height="24" rx="3" fill="{BG}" stroke="{AMBER}" stroke-width="2"/>'
             f'<text x="{xo + 73:.0f}" y="{y[m_off] + 5}" class="m" font-size="12" font-weight="700" fill="{AMBER}" text-anchor="middle" letter-spacing="2">CLOSED</text></g>')
    hops, last = [], None
    for i, r in enumerate(rows):
        if r["model"] != last:
            hops.append((i, y[r["model"]])); last = r["model"]
    kd = "".join(f"{at(i):.3f}%{{transform:translateY({yy}px)}}" for i, yy in hops)
    # incoming flights on approach: a steady trickle into the controller
    ry = 72  # approach lane along the top, into the router, down the feeder to every runway
    approach = "".join(f'<circle r="2.6" fill="{TEALG}" filter="url(#glow)"><animateMotion dur="1.8s" begin="{k * .36:.2f}s" repeatCount="indefinite" '
                       f'path="M36,{ry} L{X0 - 70},{ry}"/></circle>' for k in range(5))
    ctl = (f'<line x1="{X0 - 52}" y1="{ry}" x2="{X0 - 6}" y2="{ry}" stroke="{TEAL}" stroke-opacity=".5"/>'
           f'<line x1="{X0 - 6}" y1="{ry}" x2="{X0 - 6}" y2="{y[order[-1]]}" stroke="{TEAL}" stroke-opacity=".35"/>'
           f'<circle cx="{X0 - 62}" cy="{ry}" r="14" fill="none" stroke="{TEAL}" stroke-width="1.5" class="pulse"/>'
           f'<circle cx="{X0 - 62}" cy="{ry}" r="5" fill="{TEAL}" filter="url(#glow)"/>'
           f'<text x="{X0 - 62}" y="{ry + 32}" text-anchor="middle" class="sig">ROUTER</text>'
           f'<text x="36" y="{ry - 14}" class="sig">APPROACH</text>')
    body = ("".join(b) + approach + ctl + f'<line x1="{X0}" y1="{S1}" x2="{X1}" y2="{S1}" stroke="{LINE}"/>'
            + f'<text x="{X0 - 14}" y="{S0 + 4}" class="sig" text-anchor="end">SPEND</text>'
            + f'<g clip-path="url(#rv)">{reveal}</g>{lab_svg}{stamp}'
            + f'<g class="ph"><rect x="{X0 - 10}" y="{R0 - 14}" width="20" height="{S1 - R0 + 14}" fill="{AMBER}" opacity=".07"/>'
            + f'<line x1="{X0}" y1="{R0 - 14}" x2="{X0}" y2="{S1}" stroke="{AMBER}" stroke-width="1.4" filter="url(#glow)"/>'
            + f'<g class="dot"><circle cx="{X0}" cy="0" r="10" fill="{AMBER}" opacity=".22" filter="url(#soft)"/><circle cx="{X0}" cy="0" r="4.2" fill="{AMBERG}" filter="url(#glow)"/></g></g>'
            + f'<text x="36" y="{H - 24}" font-size="12" fill="{MUTE}">500 requests replayed from Multiplexer\'s own benchmark: the real routing code, simulated model answers, list prices.</text>')
    css = (lab_css + f".rv{{animation:rv {T}s linear infinite}}@keyframes rv{{0%{{width:0}}{pct(PLAY)},100%{{width:{X1 - X0 + 6}px}}}}"
           f".ph{{animation:ph {T}s linear infinite}}@keyframes ph{{0%{{transform:translateX(0)}}{pct(PLAY)}{{transform:translateX({X1 - X0}px);opacity:1}}{pct(PLAY + .6)},100%{{transform:translateX({X1 - X0}px);opacity:0}}}}"
           f".dot{{animation:dot {T}s steps(1,end) infinite}}@keyframes dot{{{kd}{pct(PLAY)},100%{{transform:translateY({y[rows[-1]['model']]}px)}}}}"
           f".stamp{{opacity:0;animation:stamp {T}s infinite}}@keyframes stamp{{0%,{at(off):.3f}%{{opacity:0;transform:scale(1.8)}}"
           f"{at(off) + .8:.3f}%{{opacity:1;transform:scale(1)}}{100 - 100 * .4 / T:.3f}%{{opacity:1}}100%{{opacity:0}}}}")
    defs = f'<clipPath id="rv"><rect class="rv" x="{X0 - 2}" y="0" width="0" height="{H}"/></clipPath>'
    return panel(H, "AIR TRAFFIC CONTROL  /  MULTIPLEXER", "500 ARRIVALS  /  13 RUNWAYS", body, css, defs)


ALT = {
    "board": 'Departures board for Manas Borole, flipping on a loop. Now: UK RegTech fintech. Building: Backchannel. Shipping: Odyssey. Learning: voice AI at real latency. Open for: problems that ship.',
    "atc": 'Air traffic control for Multiplexer: 500 real routing decisions replayed. It tries every model, settles on one, loses it at request 300 and recovers within about 50 requests, spending $0.07 where the flagship would cost $1.81.'}


PANELS = {
        "board": lambda: board(),
        "atc": lambda: atc(*load_benchmark()),
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
