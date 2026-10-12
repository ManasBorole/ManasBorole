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


# ------------------------------------------------------------------ customs: the companion is the agent, and a person stamps it through
def customs():
    H, floor, T = 360, 300, 13.0
    pc = lambda t: f"{100 * t / T:.3f}%"
    checks = [(250, "stock", 1.1), (350, "budget", 1.9), (450, "risks", 2.8)]
    desk = 600
    body = f'<line x1="36" y1="{floor}" x2="{W - 36}" y2="{floor}" stroke="{LINE}" stroke-width="2"/>'
    for x, label, t in checks:
        body += (f'<line x1="{x}" y1="{floor}" x2="{x}" y2="{floor - 120}" stroke="{LINE}" stroke-width="3"/>'
                 f'<circle cx="{x}" cy="{floor - 128}" r="7" fill="{SURF2}" stroke="{LINE}"/>'
                 f'<circle cx="{x}" cy="{floor - 128}" r="7" fill="{TEAL}" filter="url(#glow)" style="opacity:0;animation:lamp {T}s infinite;animation-delay:{t:.1f}s"/>'
                 f'<text x="{x}" y="{floor - 146}" text-anchor="middle" class="sig">{label.upper()}</text>')
    # the officer: a stickman behind the desk who lifts the stamp and brings it down
    sx_, sy_ = desk + 58, floor - 108  # shoulder
    stick = f'stroke="{TEXT}" stroke-width="3" stroke-linecap="round" fill="none"'
    body += (f'<circle cx="{sx_}" cy="{floor - 132}" r="11" {stick}/>'
             f'<path d="M{sx_},{floor - 121} L{sx_},{floor - 60} M{sx_},{sy_} L{sx_ + 22},{floor - 80}" {stick}/>'
             f'<g class="chop" style="transform-origin:{sx_}px {sy_}px"><path d="M{sx_},{sy_} L{sx_ - 28},{sy_ + 16}" {stick}/>'
             f'<rect x="{sx_ - 38}" y="{sy_ + 10}" width="14" height="16" rx="2" fill="{AMBER}"/></g>'
             f'<rect x="{desk - 10}" y="{floor - 70}" width="110" height="70" rx="4" fill="{SURF}" stroke="{LINE}"/>'
             f'<text x="{desk + 45}" y="{floor - 30}" text-anchor="middle" class="sig">CUSTOMS</text>')
    # the stamp: comes down hard, leaves its mark
    body += (f'<g class="stamp" style="transform-origin:{desk - 70}px {floor - 168}px">'
             f'<rect x="{desk - 129}" y="{floor - 185}" width="118" height="34" rx="4" fill="{BG}" stroke="{AMBER}" stroke-width="2.5" transform="rotate(-8 {desk - 70} {floor - 168})"/>'
             f'<text x="{desk - 70}" y="{floor - 163}" class="m" font-size="15" font-weight="800" fill="{AMBERG}" text-anchor="middle" letter-spacing="3" transform="rotate(-8 {desk - 70} {floor - 168})">APPROVED</text></g>')
    # the barrier lifts once it is stamped
    body += (f'<line x1="{desk + 112}" y1="{floor}" x2="{desk + 112}" y2="{floor - 64}" stroke="{TEXT}" stroke-width="3"/>'
             f'<g class="bar" style="transform-origin:{desk + 112}px {floor - 58}px"><rect x="{desk + 112}" y="{floor - 62}" width="96" height="8" rx="3" fill="{AMBER}"/>'
             + "".join(f'<rect x="{desk + 124 + k * 22}" y="{floor - 62}" width="10" height="8" fill="{BG}"/>' for k in range(4)) + '</g>'
             f'<text x="{W - 40}" y="{floor + 24}" text-anchor="end" class="sig">TO XERO / HUBSPOT</text>')
    # the agent itself, carrying the purchase order; a waiting bubble while nobody has said yes
    body += (f'<g class="walk"><g transform="translate(60,{floor - 140}) scale(.56)">{robot(carry=True)}</g>'
             f'<g class="wait"><rect x="130" y="{floor - 186}" width="58" height="26" rx="13" fill="{SURF2}" stroke="{TEAL}"/>'
             + "".join(f'<circle cx="{146 + k * 13}" cy="{floor - 173}" r="3" fill="{TEALG}" style="animation:pulse 1s ease-in-out {k * .2:.1f}s infinite"/>' for k in range(3))
             + '</g></g>')
    body += f'<text x="36" y="{H - 24}" font-size="12" fill="{MUTE}">How Odyssey handles a purchase order: the model proposes, a person signs off, then it writes to HubSpot and Xero.</text>'
    css = (ROBOT_CSS
           + f".walk{{animation:walk {T}s infinite}}@keyframes walk{{0%{{transform:translateX(0);opacity:0}}3%{{opacity:1}}"
             f"{pc(3.4)},{pc(8.2)}{{transform:translateX({desk - 200}px)}}{pc(10.6)}{{transform:translateX({desk + 60}px);opacity:1}}{pc(11.4)},100%{{transform:translateX({desk + 60}px);opacity:0}}}}"
           + f".wait{{opacity:0;animation:wait {T}s infinite}}@keyframes wait{{0%,{pc(3.5)}{{opacity:0}}{pc(3.8)},{pc(7.0)}{{opacity:1}}{pc(7.2)},100%{{opacity:0}}}}"
           + f"@keyframes lamp{{0%{{opacity:0}}2%,{100 - 100 * 1.8 / T:.1f}%{{opacity:1}}100%{{opacity:0}}}}"
           + f".stamp{{opacity:0;animation:stamp {T}s infinite}}@keyframes stamp{{0%,{pc(7.0)}{{opacity:0;transform:scale(2.2)}}{pc(7.25)}{{opacity:1;transform:scale(.94)}}{pc(7.4)},{pc(12.4)}{{opacity:1;transform:scale(1)}}100%{{opacity:0}}}}"
           + f".chop{{animation:chop {T}s infinite}}@keyframes chop{{0%,{pc(5.6)}{{transform:rotate(-20deg)}}{pc(6.5)},{pc(6.75)}{{transform:rotate(125deg)}}"
             f"{pc(7.0)}{{transform:rotate(-12deg)}}{pc(7.6)},100%{{transform:rotate(-20deg)}}}}"
           + f".bar{{animation:bar {T}s infinite}}@keyframes bar{{0%,{pc(7.6)}{{transform:rotate(0)}}{pc(8.2)},{pc(11.6)}{{transform:rotate(-75deg)}}{pc(12.2)},100%{{transform:rotate(0)}}}}")
    return panel(H, "CUSTOMS  /  ODYSSEY", "NOTHING CLEARS WITHOUT A PERSON", body, css)


# ------------------------------------------------------------------ arrivals: the companion waves you in
def arrivals():
    H = 300
    body = (f'<g transform="translate(70,40) scale(.92)">{robot(wave=True)}</g>'
            f'<text x="330" y="132" font-size="30" font-weight="800" fill="{TEXT}" class="m" letter-spacing="2" filter="url(#glow)">ARRIVALS</text>'
            f'<text x="332" y="166" font-size="15" fill="{MUTE}">If you are building something or stuck on something hard,</text>'
            f'<text x="332" y="188" font-size="15" fill="{MUTE}">this is where you land. Say hi.</text>'
            f'<circle cx="340" cy="222" r="4" fill="{TEAL}" class="pulse" filter="url(#glow)"/>'
            f'<text x="354" y="227" class="m" font-size="13" letter-spacing="2" fill="{TEAL}">YOU  /  ON TIME</text>')
    return panel(H, "ARRIVALS  /  TERMINAL M", "GATE 01", body, ROBOT_CSS)


PAPER, PINK = "#F4EFE4", "#1B2329"


# ------------------------------------------------------------------ Christopher: airmail postcards, one slip, one correction, in six scripts
def postcards():
    H, per = 380, 4.5
    lessons = [("ES", "Español", ("Ayer yo ", "voy", " al mercado."), ("Casi. Ayer ", "fui", " al mercado.")),
               ("FR", "Français", ("Hier je ", "vais", " au marché."), ("Presque. Hier je ", "suis allé", " au marché.")),
               ("HI", "हिन्दी", ("कल मैं बाज़ार ", "जाता हूँ", "।"), ("लगभग! कल मैं बाज़ार ", "गया था", "।")),
               ("JA", "日本語", ("昨日、市場に", "行きます", "。"), ("おしい！昨日、市場に", "行きました", "。")),
               ("DE", "Deutsch", ("Gestern ", "gehe ich", " zum Markt."), ("Fast! Gestern ", "bin ich", " zum Markt gegangen.")),
               ("PT", "Português", ("Ontem eu ", "vou", " ao mercado."), ("Quase! Ontem eu ", "fui", " ao mercado."))]
    T = per * len(lessons)
    pc = lambda t: f"{100 * t / T:.3f}%"
    cx, cy, cw, chh = 150, 78, 540, 236
    rnd = random.Random(11)
    stripes = "".join(f'<path d="M{k},0 l14,0 l-14,14 l-14,0 z" fill="{AMBER if (k // 28) % 2 else TEAL}"/>' for k in range(0, cw + 28, 28))

    def card(code, name, you, fix, i):
        wave = ""
        for k in range(46):
            h = 4 + 16 * rnd.random()
            slip = 20 <= k <= 28
            wave += (f'<rect x="{40 + k * 6}" y="{120 - h / 2:.1f}" width="3" height="{h:.1f}" rx="1.5" fill="{AMBER if slip else "#9aa4a8"}"'
                     + (' class="slip"/>' if slip else "/>"))
        a, b, c = you
        d, e, f = fix
        return (f'<g class="card c{i}">'
                f'<rect x="4" y="6" width="{cw}" height="{chh}" rx="6" fill="#000" opacity=".35" filter="url(#soft)"/>'
                f'<rect width="{cw}" height="{chh}" rx="6" fill="{PAPER}"/>'
                f'<clipPath id="ce{i}"><rect width="{cw}" height="{chh}" rx="6"/></clipPath>'
                f'<g clip-path="url(#ce{i})"><g>{stripes}</g><g transform="translate(0,{chh - 14})">{stripes}</g></g>'
                f'<rect x="{cw - 96}" y="26" width="70" height="80" rx="3" fill="#fff" stroke="{PINK}" stroke-dasharray="3 3"/>'
                f'<text x="{cw - 61}" y="66" font-size="26" font-weight="800" fill="{TEAL}" text-anchor="middle" class="m">{code}</text>'
                f'<text x="{cw - 61}" y="90" font-size="12" fill="{PINK}" text-anchor="middle">{name}</text>'
                f'<text x="40" y="58" class="m" font-size="11" letter-spacing="2" fill="#6b7478">YOU SAID</text>'
                f'<text x="40" y="90" font-size="23" fill="{PINK}">{a}<tspan fill="{AMBER}" font-weight="700" text-decoration="underline">{b}</tspan>{c}</text>'
                f'{wave}<text x="40" y="146" font-size="11" fill="#6b7478">the slip, heard in the audio rather than read from a transcript</text>'
                f'<g class="reply r{i}"><text x="40" y="172" class="m" font-size="11" letter-spacing="2" fill="#6b7478">CHRISTOPHER</text>'
                f'<text x="40" y="202" font-size="23" fill="{PINK}">{d}<tspan fill="{TEAL}" font-weight="700">{e}</tspan>{f}</text></g></g>')

    body = ""
    for k in range(3):  # cards already delivered, stacked behind
        body += (f'<rect x="{cx + 10 + k * 8}" y="{cy - 6 + k * 6}" width="{cw}" height="{chh}" rx="6" fill="{PAPER}" '
                 f'opacity="{.07 + k * .04:.2f}" transform="rotate({-3 + k * 2.2} {cx + cw / 2} {cy + chh / 2})"/>')
    css = ".slip{animation:pulse 1s ease-in-out infinite}"
    for i, (code, name, you, fix) in enumerate(lessons):
        body += f'<g transform="translate({cx},{cy})">{card(code, name, you, fix, i)}</g>'
        t0 = i * per
        a0, a1, h1, l1 = t0, t0 + .6, t0 + per - .5, t0 + per
        css += (f".c{i}{{opacity:0;transform-box:fill-box;transform-origin:center;animation:c{i} {T}s infinite}}"
                f"@keyframes c{i}{{0%,{pc(a0)}{{opacity:0;transform:translate(640px,-80px) rotate(14deg)}}"
                f"{pc(a1)},{pc(h1)}{{opacity:1;transform:translate(0,0) rotate(-1.5deg)}}"
                f"{pc(l1)},100%{{opacity:0;transform:translate(-640px,60px) rotate(-16deg)}}}}"
                f".r{i}{{opacity:0;animation:r{i} {T}s infinite}}@keyframes r{i}{{0%,{pc(t0 + 1.9)}{{opacity:0}}{pc(t0 + 2.3)},{pc(h1)}{{opacity:1}}{pc(l1)},100%{{opacity:0}}}}")
    body += f'<text x="36" y="{H - 24}" font-size="12" fill="{MUTE}">One slip on the past tense, caught by ear and corrected, the way Christopher\'s own demo plays it across 14 languages.</text>'
    return panel(H, "AIRMAIL  /  CHRISTOPHER", "183 LANGUAGES", body, css)


# ------------------------------------------------------------------ where I've been: boarding passes printing out of a kiosk
def passes():
    H, T = 420, 15.0
    pc = lambda t: f"{100 * t / T:.3f}%"
    legs = [("NSK", "2020", "B.Tech, CS (AI/ML)", "Sandip University", "CGPA 8.27, ran hackathons"),
            ("NSK", "2022", "Founder, co-founder", "B&amp;B Fashion, Gullak", "learned what shipping costs"),
            ("PNQ", "2024", "Software engineer", "IQCPL", "20+ clients, ~30% less chasing"),
            ("PNQ", "2026", "Software engineer", "UK RegTech fintech, remote", "7 endpoints closed, 450+ tests")]
    pw, ph, gap, top = 180, 290, 16, 66
    x0 = (W - (4 * pw + 3 * gap)) / 2
    rnd = random.Random(5)
    body = (f'<rect x="{x0 - 14}" y="{top - 14}" width="{4 * pw + 3 * gap + 28}" height="14" rx="7" fill="#05080a" stroke="{LINE}"/>'
            f'<rect x="{x0 - 14}" y="{top - 14}" width="{4 * pw + 3 * gap + 28}" height="3" rx="1.5" fill="{TEAL}" opacity=".5" class="pulse"/>')
    css = ""
    for i, (code, yr, role, org, note) in enumerate(legs):
        x = x0 + i * (pw + gap)
        bars = "".join(f'<rect x="{14 + k * 5}" y="{ph - 44}" width="{rnd.choice((1.5, 2.5, 3.5))}" height="26" fill="{PINK}"/>' for k in range(20))
        p = (f'<rect width="{pw}" height="{ph}" rx="6" fill="{PAPER}"/>'
             f'<rect width="{pw}" height="34" rx="6" fill="{TEAL}"/><rect y="20" width="{pw}" height="14" fill="{TEAL}"/>'
             f'<text x="14" y="22" class="m" font-size="10" font-weight="700" letter-spacing="2" fill="{BG}">BOARDING PASS</text>'
             f'<text x="{pw - 14}" y="22" class="m" font-size="10" fill="{BG}" text-anchor="end">MB {yr}</text>'
             f'<text x="14" y="58" class="m" font-size="9" letter-spacing="1" fill="#6b7478">PASSENGER</text>'
             f'<text x="14" y="72" class="m" font-size="12" font-weight="700" fill="{PINK}">BOROLE / MANAS</text>'
             f'<text x="14" y="122" class="m" font-size="44" font-weight="800" fill="{PINK}">{code}</text>'
             f'<text x="{pw - 14}" y="122" class="m" font-size="16" font-weight="700" fill="{AMBER}" text-anchor="end">{yr}</text>'
             f'<text x="14" y="152" font-size="13" font-weight="700" fill="{PINK}">{role}</text>'
             f'<text x="14" y="170" font-size="12" fill="{PINK}">{org}</text>'
             f'<text x="14" y="194" font-size="11" fill="#6b7478">{note}</text>'
             f'<line x1="8" y1="{ph - 62}" x2="{pw - 8}" y2="{ph - 62}" stroke="#9aa4a8" stroke-dasharray="4 4"/>'
             f'<g class="stub s{i}">{bars}<text x="{pw - 14}" y="{ph - 22}" class="m" font-size="10" fill="#6b7478" text-anchor="end">GATE 0{i + 1}</text></g>')
        body += (f'<clipPath id="slot{i}"><rect x="{x - 4}" y="{top}" width="{pw + 8}" height="{ph + 30}"/></clipPath>'
                 f'<g clip-path="url(#slot{i})"><g transform="translate({x},{top})"><g class="pr p{i}">{p}</g></g></g>')
        t0 = .4 + i * 1.6
        css += (f".p{i}{{animation:p{i} {T}s infinite}}@keyframes p{i}{{0%,{pc(t0)}{{transform:translateY(-{ph + 10}px);animation-timing-function:steps(12,end)}}"
                f"{pc(t0 + 1.4)},{pc(T - .8)}{{transform:translateY(0);opacity:1}}100%{{transform:translateY(0);opacity:0}}}}"
                f".s{i}{{transform-box:fill-box;transform-origin:left top;animation:s{i} {T}s infinite}}"
                f"@keyframes s{i}{{0%,{pc(t0 + 4.6)}{{transform:none}}{pc(t0 + 5.1)},{pc(T - .8)}{{transform:translate(4px,12px) rotate(4deg)}}100%{{transform:none}}}}")
    body += (f'<circle cx="{W - 250}" cy="{H - 29}" r="4" fill="{AMBER}" class="pulse" filter="url(#glow)"/>'
             f'<text x="{W - 238}" y="{H - 24}" class="m" font-size="12" letter-spacing="2" fill="{AMBERG}">NEXT: A COMPANY OF MY OWN</text>')
    return panel(H, "BOARDING PASSES  /  HOW I GOT HERE", "2020 TO NOW", body, css)


# ------------------------------------------------------------------ Backchannel: a call where the agent steps on the caller, then the same call with the fix
def backchannel():
    H, X0, X1, SEC = 470, 150, 800, 10.0
    sx = lambda t: X0 + (X1 - X0) * t / SEC
    T = SEC + 3
    pc = lambda t: f"{100 * t / T:.3f}%"
    rnd = random.Random(8)
    lanes = {"before": (112, 160), "after": (300, 348)}  # caller y, agent y
    caller = [(0.3, 2.5), (3.0, 4.6)]                     # a thinking pause inside one sentence
    agent_before = [(2.7, 4.1), (7.7, 9.4)]               # jumps into the pause, then 3.1 s of dead air
    agent_after = [(5.2, 7.4)]                            # waits for the caller to finish, then answers

    def bars(spans, y, col):
        out = ""
        for a, b in spans:
            t = a
            while t < b:
                h = 5 + 24 * rnd.random() * (0.45 + 0.55 * abs(((t * 6) % 2) - 1))
                out += f'<rect x="{sx(t):.1f}" y="{y - h / 2:.1f}" width="3" height="{h:.1f}" rx="1.5" fill="{col}"/>'
                t += .05
        return out

    def lane_labels(key, title):
        cy, ay = lanes[key]
        return (f'<text x="36" y="{cy - 52}" class="sig">{title}</text>'
                f'<text x="{X0 - 16}" y="{cy + 4}" class="sig" text-anchor="end">CALLER</text>'
                f'<text x="{X0 - 16}" y="{ay + 4}" class="sig" text-anchor="end">AGENT</text>'
                f'<line x1="{X0}" y1="{cy}" x2="{X1}" y2="{cy}" stroke="{LINE}"/><line x1="{X0}" y1="{ay}" x2="{X1}" y2="{ay}" stroke="{LINE}"/>')

    cy, ay = lanes["before"]
    flags = (f'<rect x="{sx(3.0):.1f}" y="{cy - 22}" width="{sx(4.1) - sx(3.0):.1f}" height="{ay - cy + 44}" fill="{AMBER}" opacity=".12"/>'
             f'<line x1="{sx(2.7):.1f}" y1="{cy - 24}" x2="{sx(2.7):.1f}" y2="{ay + 22}" stroke="{AMBER}" stroke-dasharray="2 3"/>'
             f'<path d="M{sx(4.6):.1f},{ay + 26} l0,6 L{sx(7.7):.1f},{ay + 32} l0,-6" fill="none" stroke="{AMBER}"/>')
    tags = [("fa", f'<text x="{sx(2.7) - 6:.1f}" y="{cy - 28}" font-size="12" font-weight="700" fill="{AMBERG}" text-anchor="end">cut off mid-sentence</text>', 2.7),
            ("fb", f'<text x="{sx(3.55):.1f}" y="{ay + 36}" font-size="12" font-weight="700" fill="{AMBERG}" text-anchor="middle">talking over, 1.1 s</text>', 4.1),
            ("fc", f'<text x="{sx(6.15):.1f}" y="{ay + 48}" font-size="12" font-weight="700" fill="{AMBERG}" text-anchor="middle">dead air, 3.1 s</text>', 7.7)]
    cy2, ay2 = lanes["after"]
    tags.append(("fd", f'<circle cx="{sx(5.2) + 6:.1f}" cy="{ay2 + 34}" r="9" fill="{TEAL}" opacity=".2"/>'
                       f'<path d="M{sx(5.2) + 2:.1f},{ay2 + 34} l3,3 l6,-7" fill="none" stroke="{TEALG}" stroke-width="2"/>'
                       f'<text x="{sx(5.2) + 22:.1f}" y="{ay2 + 38}" font-size="12" font-weight="700" fill="{TEALG}">waits for the caller to finish. no cut-offs, no dead air</text>', 7.4))
    tag_svg, tag_css = "", ""
    for nm, el, t in tags:
        a_, b_ = appear(nm, el, t, T)
        tag_svg += a_; tag_css += b_
    body = (lane_labels("before", "THE CALL AS IT HAPPENED") + lane_labels("after", "THE SAME CALL, SIMULATED WITH THE FIX")
            + f'<g clip-path="url(#rv)">{bars(caller, cy, TEALG)}{bars(agent_before, ay, AMBER)}{flags}'
            + f'{bars(caller, cy2, TEALG)}{bars(agent_after, ay2, AMBER)}</g>{tag_svg}'
            + f'<line class="ph" x1="{X0}" y1="{cy - 26}" x2="{X0}" y2="{ay2 + 26}" stroke="{AMBERG}" stroke-width="1.4" filter="url(#glow)"/>'
            + f'<text x="{X0}" y="{H - 44}" class="m" font-size="12" fill="{TEXT}">fix: wait longer after a mid-sentence pause, answer sooner once the caller is done</text>'
            + f'<text x="36" y="{H - 22}" font-size="12" fill="{MUTE}">Illustrated. Backchannel measures these moments from each audio channel, to the millisecond. In active development.</text>')
    css = (tag_css + f".rv{{animation:rv {T}s linear infinite}}@keyframes rv{{0%{{width:0}}{pc(SEC)},100%{{width:{X1 - X0 + 60}px}}}}"
           f".ph{{animation:ph {T}s linear infinite}}@keyframes ph{{0%{{transform:translateX(0)}}{pc(SEC)}{{transform:translateX({X1 - X0}px);opacity:1}}"
           f"{pc(SEC + .4)},100%{{transform:translateX({X1 - X0}px);opacity:0}}}}")
    return panel(H, "CONTROL TOWER  /  BACKCHANNEL", "STEPPED-ON TRANSMISSIONS", body, css,
                 f'<clipPath id="rv"><rect class="rv" x="{X0 - 140}" y="0" width="0" height="{H}"/></clipPath>')


ALT = {
    "board": 'Departures board for Manas Borole, flipping on a loop. Now: UK RegTech fintech. Building: Backchannel. Shipping: Odyssey. Learning: voice AI at real latency. Open for: problems that ship.',
    "atc": 'Air traffic control for Multiplexer: 500 real routing decisions replayed. It tries every model, settles on one, loses it at request 300 and recovers within about 50 requests, spending $0.07 where the flagship would cost $1.81.',
    "customs": 'The companion robot, as Odyssey, carries a purchase order past stock, budget and risk checks, waits at customs until a person stamps it approved, then goes on to Xero and HubSpot.',
    "arrivals": 'The companion robot waves at arrivals. Say hi.',
    "postcards": 'Airmail postcards in Spanish, French, Hindi, Japanese, German and Portuguese. In each, the learner slips on the past tense, Christopher hears it in the audio and replies with the correction.',
    "passes": 'Four boarding passes print from a kiosk: Nashik 2020, B.Tech at Sandip University. Nashik 2022, founder and co-founder at B&B Fashion and Gullak. Pune 2024, software engineer at IQCPL. Pune 2026, software engineer, remote, for a UK RegTech fintech. Next: a company of my own.',
    "backchannel": 'A voice call replayed on two channels. The agent cuts the caller off during a thinking pause, talks over them for 1.1 seconds, then leaves 3.1 seconds of dead air. Below, the same call simulated with the fix: no cut-offs, no dead air.'}

# GitHub only plays videos uploaded through its own editor, so these are user-attachments links
VIDEO = {"mx": "https://github.com/user-attachments/assets/b7ba15a4-9953-4809-a1cf-742aad85d560",
         "ch": "https://github.com/user-attachments/assets/e55e59c2-414e-442f-bcac-faf303a24627"}
POSTER = {"mx": "assets/projects/multiplexer-trailer-poster.jpg", "ch": "assets/projects/christopher-trailer-poster.jpg"}


PANELS = {
        "board": lambda: board(),
        "atc": lambda: atc(*load_benchmark()),
        "customs": lambda: customs(),
        "arrivals": lambda: arrivals(),
        "postcards": lambda: postcards(),
        "passes": lambda: passes(),
        "backchannel": lambda: backchannel(),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, build in PANELS.items():
        with open(f"{OUT}/{name}.svg", "w", encoding="utf-8") as f:
            f.write(build())
    if os.path.exists(TPL):
        md = open(TPL, encoding="utf-8").read()
        md = re.sub(r"\{\{video:(\w+)\}\}", lambda m: f'<video src="{VIDEO[m[1]]}" poster="{POSTER[m[1]]}" controls playsinline width="100%"></video>', md)
        md = re.sub(r"\{\{(\w+)\}\}", lambda m: f'<img src="{OUT}/{m[1]}.svg" width="100%" alt="{ALT[m[1]]}">', md)
        open("README.md", "w", encoding="utf-8").write(md)


if __name__ == "__main__":
    main()
