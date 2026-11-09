"""oldschool: a Pix receipt and the paper artifacts of an old bank office.

Typefaces: IBM Plex Mono (receipt lines) + Instrument Serif (display). Accent: rubber-stamp red.

Motion (GitHub shows each card as an <img>: CSS keyframes and SMIL run, hover and scripts do not):
- Entrances, once: the receipt slides out of the printer while its lines print (clip-path wipe),
  the photo develops, stamps land, catalog cards slide up out of their drawer.
- Explanatory loops: the terminal on the desk types a session and clears; the LVC event store
  scrolls new events in (append-only log, marked illustrative).
- One live signal per card at most: a blinking cursor.
- prefers-reduced-motion: entrances become a short fade, loops stop on their final frame.

Material: every paper surface gets a warm gradient, static fractal-noise grain and a soft shadow.
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import lib  # noqa: E402
from lib import esc  # noqa: E402

PAPER, PAPER_2, DESK, DESK_2 = "#f6f1e6", "#ebe2cd", "#1f1d19", "#2a2722"
INK, MUT, RULE, RED = "#1b1a17", "#5e574a", "#d3c9b2", "#b3261e"
FOLD, FOLD_D, FOLD_E = "#e4cf98", "#d2ba7c", "#c5ab6a"
W = 860


# ------------------------------------------------------------------ shared style
def fonts() -> str:
    return "".join([
        lib.font("IBM Plex Mono", 400, alias="Plex"),
        lib.font("IBM Plex Mono", 600, alias="Plex"),
        lib.font("Instrument Serif", 400, alias="Serif"),
        lib.font("Instrument Serif", 400, italic=True, alias="Serif"),
    ])


def css(sid: str, extra: str = "") -> str:
    s = f"#{sid}"
    return (fonts() + f"""
{s} text{{font-family:'Plex',monospace;fill:{INK}}}
{s} .b{{font-weight:600}} {s} .mu{{fill:{MUT}}} {s} .rd{{fill:{RED}}} {s} .pp{{fill:{PAPER}}}
{s} .sf{{font-family:'Serif',serif;letter-spacing:-0.03em}} {s} .it{{font-style:italic}}
{s} .cap{{letter-spacing:.07em}}
{s} .w,{s} .f,{s} .up{{animation-fill-mode:both;animation-timing-function:{lib.EASE_OUT}}}
{s} .w{{animation-name:{sid}wipe;animation-duration:620ms}}
{s} .f{{animation-name:{sid}rise;animation-duration:560ms}}
{s} .up{{animation-name:{sid}up;animation-duration:900ms}}
{s} .cur{{animation:{sid}blink 1.1s steps(1) infinite}}
@keyframes {sid}wipe{{from{{clip-path:inset(-8px 100% -8px -8px)}}to{{clip-path:inset(-8px -8px -8px -8px)}}}}
@keyframes {sid}rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@keyframes {sid}up{{from{{transform:translateY(46px)}}to{{transform:none}}}}
@keyframes {sid}blink{{50%{{opacity:0}}}}
@keyframes {sid}fade{{from{{opacity:0}}to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{
  {s} .w,{s} .f,{s} .up{{animation:{sid}fade 300ms linear both !important}}
  {s} .cur,{s} .loop{{animation:none !important}}
}}
""" + extra)


def defs(sid: str) -> str:
    """Paper gradient, static grain and a soft drop shadow, scoped to one card."""
    return (f'<linearGradient id="{sid}P" x1="0" y1="0" x2="0.3" y2="1">'
            f'<stop offset="0" stop-color="{PAPER}"/><stop offset="1" stop-color="{PAPER_2}"/></linearGradient>'
            f'<linearGradient id="{sid}F" x1="0" y1="0" x2="0.2" y2="1">'
            f'<stop offset="0" stop-color="{FOLD}"/><stop offset="1" stop-color="{FOLD_D}"/></linearGradient>'
            f'<filter id="{sid}G" x="0" y="0" width="1" height="1">'
            f'<feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="11" stitchTiles="stitch"/>'
            f'<feColorMatrix values="0 0 0 0 .36  0 0 0 0 .30  0 0 0 0 .22  0 0 0 .16 0"/>'
            f'<feComposite in2="SourceAlpha" operator="in"/></filter>'
            f'<filter id="{sid}S" x="-10%" y="-10%" width="120%" height="130%">'
            f'<feGaussianBlur in="SourceAlpha" stdDeviation="7"/><feOffset dy="7"/>'
            f'<feComponentTransfer><feFuncA type="linear" slope=".55"/></feComponentTransfer></filter>')


def sheet(sid: str, shape: str, fill: str = "P") -> str:
    """A paper surface: shadow, gradient fill, grain. `shape` is an element without fill,
    e.g. '<rect x="0" y="0" width="10" height="10"'."""
    return (f'{shape} fill="#000" filter="url(#{sid}S)"/>'
            f'{shape} fill="url(#{sid}{fill})"/>'
            f'{shape} fill="#fff" filter="url(#{sid}G)"/>')


def D(ms: float) -> str:
    return f'style="animation-delay:{int(ms)}ms"'


def txt(x, y, s, cls="", size=14, anchor="start", extra="") -> str:
    a = "" if anchor == "start" else f' text-anchor="{anchor}"'
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}"{a} {extra}>{esc(s)}</text>'


def leader(x1, x2, y, color=INK) -> str:
    return (f'<line x1="{x1}" y1="{y-4}" x2="{x2}" y2="{y-4}" stroke="{color}" stroke-width="1.6" '
            f'stroke-dasharray="0.1 5" stroke-linecap="round"/>')


def row(xl, xr, y, left, right, size, delay, rcls="mu", lcls="b") -> str:
    cw = size * 0.6
    l_end = xl + len(left) * cw + 8
    r_start = xr - len(right) * cw - 8
    return (f'<g class="w" {D(delay)}>' + txt(xl, y, left, lcls, size) + leader(l_end, r_start, y)
            + txt(xr, y, right, rcls, size, "end") + "</g>")


def stamp(x, y, rot, w, h, line1, line2, delay) -> str:
    sub = (f'<text x="0" y="15" text-anchor="middle" font-size="10.5" class="rd cap">{esc(line2)}</text>' if line2 else "")
    y1 = -1 if line2 else 8
    return (f'<g transform="translate({x} {y}) rotate({rot})"><g class="f" {D(delay)}><g opacity=".9">'
            f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="4" fill="none" stroke="{RED}" stroke-width="3.5"/>'
            f'<rect x="{-w/2+6}" y="{-h/2+6}" width="{w-12}" height="{h-12}" rx="2" fill="none" stroke="{RED}" stroke-width="1.2"/>'
            f'<text x="0" y="{y1}" text-anchor="middle" font-size="{17 if line2 else 22}" class="b rd" style="letter-spacing:.08em">{esc(line1)}</text>'
            f'{sub}</g></g></g>')


def write(out: Path, name: str, s: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / name).write_text(s, encoding="utf-8")


# ------------------------------------------------------------------ hero: receipt out of a printer
def hero() -> str:
    sid, d = "osHero", lib.data()
    H = 528
    rx, rw, top, bot = 40, 500, 40, 488
    teeth, x, up = [], rx, False
    while x < rx + rw:
        x += 10
        teeth.append(f"{x},{bot + (0 if up else 8)}")
        up = not up
    path = f"M{rx},{top} H{rx+rw} V{bot} " + " ".join(f"L{p}" for p in reversed(teeth)) + f" L{rx},{bot} Z"
    xl, xr = 68, 512
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{DESK}"/>']
    # receipt: slides out of the slot while it prints
    r = [sheet(sid, f'<path d="{path}"')]
    t, st = 550, 85
    r.append(f'<g class="w" {D(t-st)}>' + txt(xl, 74, "HELLO THERE! I'M", "b cap", 12.5) + "</g>")
    r.append(f'<g class="w" {D(t)}>' + txt(xl, 114, "RAFAEL PEREIRA", "sf", 46) + "</g>")
    r.append(f'<g class="w" {D(t+st)}>' + txt(xl, 138, "SOFTWARE ENGINEER · GETNET · SÃO PAULO", "mu b", 13) + "</g>")
    r.append(f'<g class="w" {D(t+2*st)}>' + txt(xl, 156, "OPEN FINANCE APIS · PIX · AI CHAMPION, 9 SQUADS", "mu", 13) + "</g>")
    r.append(f'<line class="w" {D(t+3*st)} x1="{xl}" y1="174" x2="{xr}" y2="174" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    items = [("01  Event-Driven Architecture", "enthusiast"), ("02  gRPC", "user"),
             ("03  Java", "enthusiast"), ("04  Rust", "high performance"), ("05  AI tokens", "minimized")]
    y = 206
    for i, (l, rr) in enumerate(items):
        r.append(row(xl, xr, y, l, rr, 16.5, t + (4 + i) * st))
        y += 33
    r.append(f'<g class="w" {D(t+9*st)}><line x1="{xl}" y1="{y-12}" x2="{xr}" y2="{y-12}" stroke="{INK}" stroke-width="3"/>'
             f'<line x1="{xl}" y1="{y-7}" x2="{xr}" y2="{y-7}" stroke="{INK}" stroke-width="1"/></g>')
    y += 22
    r.append(row(xl, xr, y, "METHOD", "deterministic first", 16.5, t + 10 * st, rcls="b"))
    y += 40
    r.append(f'<g class="w" {D(t+11*st)}>' + txt(xl, y, "@Raphonzius", "b", 14) + "</g>")
    r.append(f'<rect class="cur" x="{xl + 11 * 8.4 + 5:.0f}" y="{y-11}" width="8" height="13" fill="{INK}"/>')
    r.append(f'<line x1="{rx}" y1="{bot-14}" x2="{rx+rw}" y2="{bot-14}" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="1 5" stroke-linecap="round" opacity=".7"/>')
    r.append(stamp(430, y + 6, -6, 168, 48, "APPROVED", "", t + 12 * st + 250))
    b.append(f'<clipPath id="{sid}C"><rect x="0" y="{top}" width="{W}" height="{H}"/></clipPath>'
             f'<g clip-path="url(#{sid}C)"><g class="f" style="animation-name:{sid}print;animation-duration:1500ms;animation-delay:150ms">'
             + "".join(r) + "</g></g>")
    # printer on top (drawn after, so the receipt comes out of the slot)
    b.append(f'<rect x="22" y="14" width="536" height="30" rx="7" fill="{DESK_2}"/>'
             f'<rect x="22" y="14" width="536" height="2" rx="1" fill="#3a3630"/>'
             f'<rect x="34" y="37" width="512" height="5" rx="2" fill="#0d0c0a"/>'
             f'<circle cx="536" cy="26" r="3" fill="{RED}"/>')
    # polaroid with tape; the photo develops
    b.append(f'<g class="f" {D(500)}><g transform="rotate(2 690 150)">'
             + sheet(sid, '<rect x="596" y="36" width="196" height="226"')
             + f'<image href="{d["avatar"]}" x="606" y="46" width="176" height="176" preserveAspectRatio="xMidYMid slice"/>'
             f'<rect x="606" y="46" width="176" height="176" fill="{PAPER}" opacity="0" style="animation:{sid}dev 2.4s {lib.EASE_OUT} 700ms both"/>'
             f'<text x="694" y="248" text-anchor="middle" font-size="19" class="sf it">São Paulo, Brazil</text>'
             f'<rect x="660" y="26" width="70" height="22" fill="#e9dfc4" opacity=".8" transform="rotate(-4 695 37)"/>'
             "</g></g>")
    for i, l in enumerate(["If it can be", "deterministic,", "it should not", "be inference."]):
        b.append(f'<g class="w" {D(1700+i*150)}>' + txt(590, 336 + i * 38, l, "sf pp", 37) + "</g>")
    extra = (f"@keyframes {sid}print{{from{{transform:translateY(-{bot-top+20}px)}}to{{transform:none}}}}"
             f"@keyframes {sid}dev{{from{{opacity:1}}to{{opacity:0}}}}")
    return lib.svg(sid, W, H, "".join(b), css(sid, extra),
                   "Hello there! I'm Rafael Pereira, Software Engineer at Getnet: Event-Driven Architecture enthusiast, gRPC user, Java enthusiast, Rust for high performance, AI tokens minimized with deterministic solutions.",
                   defs(sid))


# ------------------------------------------------------------------ LVC paper: manila folder + live event log
LOG = [("14:02:31", "LIVE", "bus · CHECKIN · Caio Prado"),
       ("14:02:30", "VIRTUAL", "area · MISSION_TRIGGER · Caio Prado"),
       ("14:02:28", "CONSTR.", "drone · TELEMETRY · alt 30 m"),
       ("14:02:27", "LIVE", "cgesp · FLOOD_ALERT · CRITICAL")]


def lvc() -> str:
    sid = "osLvc"
    H = 690
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{DESK}"/>']
    # folder back, tab and body
    b.append(f'<path d="M24,64 V50 Q24,36 38,36 H306 Q318,36 324,48 L332,64 Z" fill="{FOLD_E}"/>')
    b.append(sheet(sid, f'<rect x="24" y="62" width="{W-48}" height="{H-86}" rx="5"', "F"))
    b.append(f'<g class="w" {D(80)}>' + txt(44, 56, "FULL PAPER · LATINOWARE 2026", "b cap", 12.5) + "</g>")
    # a second sheet peeking out, then the paper
    b.append(f'<g transform="rotate(1.2 430 360)">' + sheet(sid, f'<rect x="50" y="84" width="{W-100}" height="{H-128}" rx="2"') + "</g>")
    b.append(sheet(sid, f'<rect x="44" y="80" width="{W-88}" height="{H-122}" rx="2"'))
    # paper clip
    b.append(f'<path d="M108,64 v52 a9,9 0 0 0 18,0 v-46 a5,5 0 0 0 -10,0 v40" fill="none" stroke="#8d8a83" stroke-width="3" stroke-linecap="round"/>')
    x = 72
    b.append(f'<g class="w" {D(200)}>' + txt(x, 152, "Open Source LVC", "sf", 46) + "</g>")
    b.append(f'<g class="w" {D(300)}>' + txt(x, 196, "Simulation Architecture", "sf it", 46) + "</g>")
    b.append(f'<g class="w" {D(420)}>' + txt(x, 226, "First author · Mackenzie Campus Living Lab · open source end to end", "mu b", 13) + "</g>")
    b.append(f'<line class="w" {D(480)} x1="{x}" y1="244" x2="{W-72}" y2="244" stroke="{RED}" stroke-width="1.6"/>')
    for i, l in enumerate(["Live, Virtual and Constructive simulation without HLA or DIS:",
                           "Event Sourcing, CQRS and one gRPC contract for Java, Python and Rust."]):
        b.append(f'<g class="w" {D(560 + i * 110)}>' + txt(x, 272 + i * 22, l, "", 14) + "</g>")
    mods = [("live-ms-java", "Java"), ("virtual-ms-java", "Java"), ("constructive-ms-python", "Python"),
            ("event-hub-ms-rust", "Rust"), ("proto-shared", "gRPC"), ("infra-local-shared", "Compose")]
    y = 336
    b.append(f'<g class="w" {D(760)}>' + txt(x, y - 4, "SIX MODULES", "mu b cap", 11.5)
             + txt(500, y - 4, "VALIDATED ON", "mu b cap", 11.5) + "</g>")
    for i, (m, l) in enumerate(mods):
        b.append(row(x, 440, y + 26 + i * 25, m, l, 13, 840 + i * 70, rcls="mu", lcls="b"))
    for i, v in enumerate(["Traceability: replay an immutable log", "Reproducibility: docker compose up",
                           "Multi-language: one .proto, 3 stacks", "Real sources: AIS, OlhoVivo, CGESP"]):
        k, rest = v.split(":", 1)
        b.append(f'<g class="w" {D(900 + i * 90)}>' + txt(500, y + 26 + i * 38, k, "b", 13)
                 + txt(500, y + 26 + i * 38 + 17, rest.strip(), "mu", 12) + "</g>")
    # event store: new events keep arriving (explanatory loop)
    ly, rh, rows_shown = 530, 22, 4
    b.append(f'<g class="w" {D(1300)}>' + txt(x, ly, "EVENT STORE · APPEND-ONLY", "mu b cap", 11.5)
             + txt(W - 72, ly, "illustrative", "mu it", 12, "end") + "</g>")
    win_y = ly + 12
    b.append(f'<g class="f" {D(1400)}><rect x="{x}" y="{win_y}" width="{W-144}" height="{rh*rows_shown+12}" rx="3" fill="{DESK}"/>')
    b.append(f'<clipPath id="{sid}L"><rect x="{x}" y="{win_y}" width="{W-144}" height="{rh*rows_shown+12}" rx="3"/></clipPath>')
    lines = []
    for k, (tm, dom, ev) in enumerate(LOG * 2):
        yy = win_y + 22 + k * rh
        col = {"LIVE": "#e4876f", "VIRTUAL": "#d9c58f", "CONSTR.": "#b6c9a8"}[dom]
        lines.append(f'<text x="{x+16}" y="{yy}" font-size="12.5" style="fill:#8f887a">{tm}</text>'
                     f'<text x="{x+104}" y="{yy}" font-size="12.5" class="b" style="fill:{col}">{dom}</text>'
                     f'<text x="{x+196}" y="{yy}" font-size="12.5" style="fill:{PAPER}">{esc(ev)}</text>')
    b.append(f'<g clip-path="url(#{sid}L)"><g class="loop" style="animation:{sid}log 9s linear infinite">'
             + "".join(lines) + "</g></g></g>")
    b.append(stamp(676, 138, -7, 208, 52, "PRESENTED", "PROCEEDINGS SOON", 1600))
    extra = f"@keyframes {sid}log{{from{{transform:translateY(0)}}to{{transform:translateY(-{rh*len(LOG)}px)}}}}"
    return lib.svg(sid, W, H, "".join(b), css(sid, extra),
                   "Full paper, Latinoware 2026: Open Source LVC Simulation Architecture. Event Sourcing, CQRS and one gRPC contract for Java, Python and Rust, in six open source modules. Proceedings coming soon.",
                   defs(sid))


# ------------------------------------------------------------------ desk: computer + daily tools
SCREEN_LINES = [("$ whoami", True), ("rafael · backend java", False), ("$ java --version", True),
                ("openjdk 21", False), ("$ cat focus.txt", True), ("events, grpc, rust,", False),
                ("fewer tokens", False)]


def desk() -> str:
    sid = "osDesk"
    H = 384
    BEIGE, BEIGE_D, SCREEN, PHOS, DIM = "#d9cfb8", "#bfb397", "#1c211b", "#e9e2cf", "#a9a28f"
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{DESK}"/>']
    c = [f'<ellipse cx="205" cy="338" rx="160" ry="10" fill="#000" opacity=".4"/>',
         f'<rect x="70" y="40" width="270" height="206" rx="14" fill="{BEIGE}"/>',
         f'<rect x="70" y="40" width="270" height="6" rx="3" fill="#e6dcc6"/>',
         f'<rect x="92" y="60" width="226" height="160" rx="8" fill="{SCREEN}"/>',
         f'<rect x="92" y="60" width="226" height="160" rx="8" fill="url(#{sid}Gl)"/>',
         f'<rect x="180" y="246" width="50" height="18" fill="{BEIGE_D}"/>',
         f'<rect x="120" y="262" width="170" height="14" rx="3" fill="{BEIGE}"/>',
         f'<rect x="262" y="229" width="58" height="5" rx="2" fill="{BEIGE_D}"/>',
         f'<circle cx="96" cy="232" r="3.5" fill="{RED}"/>',
         f'<path d="M60,328 L84,288 H326 L350,328 Z" fill="{BEIGE}"/>',
         f'<path d="M60,328 H350 V336 H60 Z" fill="{BEIGE_D}"/>']
    for r in range(3):
        y = 296 + r * 10
        x0, x1 = 92 - r * 6, 318 + r * 6
        for k in range(14):
            kx = x0 + k * (x1 - x0) / 14
            c.append(f'<rect x="{kx+1:.1f}" y="{y}" width="{(x1-x0)/14-3:.1f}" height="6" rx="1" fill="{BEIGE_D}"/>')
    b.append(f'<g class="f" {D(80)}>' + "".join(c) + "</g>")
    # terminal session: types line by line, holds, clears, repeats
    cyc, extra = 11.0, []
    for i, (l, cmd) in enumerate(SCREEN_LINES):
        a = (0.5 + i * 0.85) / cyc * 100
        extra.append(f"@keyframes {sid}L{i}{{0%,{a:.1f}%{{clip-path:inset(-4px 100% -4px -4px);opacity:1}}"
                     f"{a+4:.1f}%,90%{{clip-path:inset(-4px -4px -4px -4px);opacity:1}}"
                     f"95%,100%{{clip-path:inset(-4px -4px -4px -4px);opacity:0}}}}"
                     f"#{sid} .l{i}{{animation:{sid}L{i} {cyc}s linear infinite}}")
        b.append(f'<g class="loop l{i}"><text x="106" y="{84 + i * 18}" font-size="12" class="{"b" if cmd else ""}" '
                 f'style="fill:{PHOS if cmd else DIM}">{esc(l)}</text></g>')
    b.append(f'<text x="106" y="{84 + len(SCREEN_LINES) * 18}" font-size="12" class="b" style="fill:{PHOS}">$</text>'
             f'<rect class="cur" x="118" y="{84 + len(SCREEN_LINES) * 18 - 11}" width="8" height="13" fill="{PHOS}"/>')
    # pinned slip
    sx, sy, swid, sh = 392, 30, 432, 324
    slip = [sheet(sid, f'<rect x="{sx}" y="{sy}" width="{swid}" height="{sh}" rx="2"')]
    xl = sx + 28
    slip.append(f'<g class="w" {D(320)}>' + txt(xl, sy + 54, "Daily Tools", "sf", 36) + "</g>")
    slip.append(f'<line class="w" {D(400)} x1="{xl}" y1="{sy+70}" x2="{sx+swid-28}" y2="{sy+70}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    y = sy + 98
    for i, (g, v) in enumerate([("PROGRAMMING", "Java · Spring · Bash · JavaScript · Python"),
                                ("OS", "Linux · Ubuntu · Red Hat · Windows"),
                                ("UTILITIES", "AWS · Git · Podman · Jenkins · Postman")]):
        slip.append(f'<g class="w" {D(500 + i * 140)}>' + txt(xl, y, g, "mu b cap", 11.5) + txt(xl, y + 20, v, "b", 14) + "</g>")
        y += 50
    slip.append(f'<line class="w" {D(950)} x1="{xl}" y1="{y-8}" x2="{sx+swid-28}" y2="{y-8}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    for i, (k, v) in enumerate([("BEFORE", "~3 years at Samsung SDS, Java on AWS"), ("OFF THE CLOCK", "Scout volunteer")]):
        slip.append(row(xl, sx + swid - 28, y + 18 + i * 26, k, v, 12.5, 1050 + i * 120, rcls="", lcls="mu b"))
    pin = (f'<circle cx="{sx+swid/2}" cy="{sy+12}" r="7" fill="{RED}"/>'
           f'<circle cx="{sx+swid/2-2}" cy="{sy+10}" r="2.2" fill="#fff" opacity=".55"/>')
    b.append(f'<g class="f" {D(200)}><g transform="rotate(-0.8 {sx+swid/2} {sy})">' + "".join(slip) + pin + "</g></g>")
    gl = (f'<radialGradient id="{sid}Gl" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#fff" stop-opacity=".07"/>'
          f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
    return lib.svg(sid, W, H, "".join(b), css(sid, "".join(extra)),
                   "Daily Tools. Programming: Java, Spring, Bash, JavaScript, Python. OS: Linux, Ubuntu, Red Hat, Windows. Utilities: AWS, Git, Podman, Jenkins, Postman.",
                   defs(sid) + gl)


# ------------------------------------------------------------------ projects: catalog cards in a drawer
PROJECTS = [
    ("poc-grpc", "Java", ["gRPC client and server on one shared", "Protobuf contract (+ grpc-common, grpc-server)."]),
    ("Demo-SpringSecurity6-JWT", "Java", ["Stateless auth with Spring Security 6:", "OAuth2 resource server, RSA-signed JWT."]),
    ("spring-and-vue", "Java · Vue", ["Spring Boot API with a Vue front end", "(+ vue-frontend)."]),
    ("cachyos-setup", "Shell", ["Reproducible CachyOS machine: KDE Plasma,", "dotfiles and package lists in one script."]),
]


def project(i: int) -> str:
    name, lang, desc = PROJECTS[i]
    w, H = 420, 158
    sid = f"osPrj{i}"
    b = [f'<rect width="{w}" height="{H}" rx="6" fill="{DESK_2}"/>',
         f'<rect x="0" y="{H-20}" width="{w}" height="20" rx="0" fill="#191714"/>',
         f'<clipPath id="{sid}C"><rect x="0" y="0" width="{w}" height="{H-20}"/></clipPath>']
    c = [sheet(sid, f'<rect x="14" y="14" width="{w-28}" height="{H-28}" rx="3"'),
         txt(32, 44, name, "b", 15), txt(w - 32, 44, f"No. {i+1:02d}", "mu", 11.5, "end"),
         f'<line x1="14" y1="58" x2="{w-14}" y2="58" stroke="{RED}" stroke-width="1.6"/>']
    for k, l in enumerate(desc):
        yy = 82 + k * 21
        c.append(txt(32, yy, l, "", 12.5))
        c.append(f'<line x1="14" y1="{yy+6}" x2="{w-14}" y2="{yy+6}" stroke="{RULE}" stroke-width="1"/>')
    c.append(txt(32, H - 36, lang, "mu b", 11.5))
    c.append(txt(w - 32, H - 36, "→", "rd", 16, "end"))
    c.append(f'<circle cx="{w/2}" cy="{H-40}" r="5" fill="{DESK_2}"/>')
    b.append(f'<g clip-path="url(#{sid}C)"><g class="up" {D(150 + i * 90)}>' + "".join(c) + "</g></g>")
    # drawer front lip, over the card bottom
    b.append(f'<rect x="0" y="{H-22}" width="{w}" height="22" rx="0" fill="#191714"/>'
             f'<rect x="{w/2-28}" y="{H-15}" width="56" height="7" rx="3.5" fill="#3a3630"/>')
    return lib.svg(sid, w, H, "".join(b), css(sid), f"{name}: {' '.join(desc)}", defs(sid))


# ------------------------------------------------------------------ tickets (links)
def ticket(sid: str, stub: str, label: str, value: str, w: int = 420, red: bool = False) -> str:
    """A perforated ticket, used as a clickable link (wrapped in <a> in the README)."""
    H, sw = 84, 104
    b = [f'<rect width="{w}" height="{H}" rx="6" fill="{DESK}"/>',
         sheet(sid, f'<rect x="10" y="10" width="{w-20}" height="{H-26}" rx="3"'),
         f'<line x1="{10+sw}" y1="16" x2="{10+sw}" y2="{H-22}" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="1 5" stroke-linecap="round"/>',
         f'<circle cx="{10+sw}" cy="10" r="6" fill="{DESK}"/><circle cx="{10+sw}" cy="{H-16}" r="6" fill="{DESK}"/>']
    b.append(f'<g class="w" {D(100)}>' + txt(10 + sw / 2, (H - 6) / 2 + 5, stub, ("b rd" if red else "b") + " cap", 14, "middle") + "</g>")
    b.append(f'<g class="w" {D(220)}>' + txt(sw + 30, 34, label, "mu", 12) + "</g>")
    b.append(f'<g class="w" {D(320)}>' + txt(sw + 30, 56, value, "b", 15) + "</g>")
    return lib.svg(sid, w, H, "".join(b), css(sid), f"{label}: {value}", defs(sid))


# ------------------------------------------------------------------ record: four tickets
def record() -> str:
    sid = "osRecord"
    H = 300
    tickets = [("2 days", "Java 17 to 21 and Spring Boot 3.5.4 to 4.1.0, migrated with AI agents. Other squads took 2 sprints.", True),
               ("USD 37k", "a year saved on AWS at Samsung SDS: rightsizing and x86_64 to arm64, 20-32% faster instances.", False),
               ("670k+", "SMS and WhatsApp messages a month through notification microservices in 4 countries.", False),
               ("45%", "of execution subtasks sent to Devin Lite, the cheapest mode, by the task routing plugin at Getnet's Devin Enterprise.", False)]
    m = 20
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{DESK}"/>',
         sheet(sid, f'<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m-6}" rx="3"')]
    for i, (big, small, red) in enumerate(tickets):
        x = m + i * (W - 2 * m) / 4
        g_ = [txt(x + 20, 96, big, "sf rd" if red else "sf", 58)]
        for k, line in enumerate(textwrap.wrap(small, 21)):
            g_.append(txt(x + 20, 130 + k * 20, line, "", 13))
        b.append(f'<g class="f" {D(100 + i * 120)}>' + "".join(g_) + "</g>")
        if i:
            b.append(f'<line x1="{x}" y1="{m+8}" x2="{x}" y2="{H-m-14}" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="1 5" stroke-linecap="round"/>'
                     f'<circle cx="{x}" cy="{m}" r="8" fill="{DESK}"/><circle cx="{x}" cy="{H-m-6}" r="8" fill="{DESK}"/>')
    return lib.svg(sid, W, H, "".join(b), css(sid),
                   "Four tickets: 2 days for a migration other squads did in 2 sprints, USD 37k a year saved on AWS, 670k+ messages a month, 45% of subtasks sent to the cheapest mode by the task routing plugin at Getnet's Devin Enterprise.",
                   defs(sid))


def build(out_dir: Path) -> None:
    for old in ("tokens.svg", "stats.svg", "focus.svg", "projects.svg", "punch.svg"):
        (out_dir / old).unlink(missing_ok=True)
    cards = {"hero": hero(), "lvc": lvc(), "desk": desk(), "record": record(),
             "link-code": ticket("osLnkCode", "CODE", "Source code, 6 modules", "github.com/tcc-modern-lvc-arch"),
             "link-paper": ticket("osLnkPaper", "PAPER", "Full paper, Latinoware 2026", "tcc-modern-lvc-arch.github.io", red=True),
             "link-mail": ticket("osLnkMail", "EMAIL", "Write to me", "rafael.informa@gmail.com"),
             "link-linkedin": ticket("osLnkIn", "LINKEDIN", "Connect", "in/rafaelrodriguespereira")}
    for i in range(len(PROJECTS)):
        cards[f"project-{i+1}"] = project(i)
    for n, s in cards.items():
        write(out_dir, f"{n}.svg", s)


if __name__ == "__main__":
    build(lib.ROOT / "assets" / "oldschool")
    print("ok")
