"""oldschool: a Pix receipt and the paper artifacts of an old bank office.

Typefaces: IBM Plex Mono (receipt lines) + Instrument Serif (display). Accent: rubber-stamp red.

Layout (spec: specs/oldschool-v3.md): every card is 420 wide and the README places them in pairs
with <img width="410">. GitHub caps images at max-width:100%, so on desktop a pair sits side by
side at ~1:1 and on a phone each card wraps to full width (~0.8 scale), which keeps 14px text
readable. Pairs share one height.

Motion (GitHub shows each card as an <img>: CSS keyframes and SMIL run, hover and scripts do not):
- Entrances, once, ease-out, stagger 60ms: the receipt slides out of the printer while its lines
  print, the photo develops, stamps are struck (scale 1.15 -> 1), catalog cards rise out of their
  drawer. Cards below the fold finish in under ~1s, since they play on image load.
- Explanatory loops: the desk terminal types a session and clears; the LVC event store appends
  one event at a time (hold, then a short ease-in-out step), labelled illustrative.
- One live signal per card at most: a blinking cursor, shown once its line has printed.
- prefers-reduced-motion: entrances become a short fade, loops stop on a complete frame.

Material: paper gradient, static grain and a soft shadow on still surfaces; moving surfaces get a
cheap offset shadow and no filters. Fonts are subset per card to the glyphs it uses.
"""
from __future__ import annotations

import html
import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import lib  # noqa: E402
from lib import esc  # noqa: E402

PAPER, PAPER_2, DESK, DESK_2 = "#f6f1e6", "#ebe2cd", "#1f1d19", "#2a2722"
INK, MUT, RULE, RED = "#1b1a17", "#57503f", "#d3c9b2", "#b3261e"
FOLD, FOLD_D, FOLD_E = "#e4cf98", "#d2ba7c", "#c5ab6a"
W = 420          # every card
RX = 10          # card corner radius
STAG = 60        # ms between staggered items


# ------------------------------------------------------------------ shared style
def _glyphs(body: str) -> str:
    return html.unescape("".join(re.findall(r">([^<>]+)</text>", body)))


def fonts(body: str) -> str:
    """Embed only the faces this card uses, each subset to the card's glyphs."""
    text = _glyphs(body)
    classes = " ".join(re.findall(r'class="([^"]*)"', body)).split()
    serif = [c for c in re.findall(r'class="([^"]*\bsf\b[^"]*)"', body)]
    out = [lib.font("IBM Plex Mono", 400, alias="Plex", text=text)]
    if "b" in classes:
        out.append(lib.font("IBM Plex Mono", 600, alias="Plex", text=text))
    if any("it" not in c.split() for c in serif):
        out.append(lib.font("Instrument Serif", 400, alias="Serif", text=text))
    if any("it" in c.split() for c in serif):
        out.append(lib.font("Instrument Serif", 400, italic=True, alias="Serif", text=text))
    return "".join(out)


def css(sid: str, body: str, extra: str = "") -> str:
    s = f"#{sid}"
    return (fonts(body) + f"""
{s} text{{font-family:'Plex',monospace;fill:{INK}}}
{s} .b{{font-weight:600}} {s} .mu{{fill:{MUT}}} {s} .rd{{fill:{RED}}} {s} .pp{{fill:{PAPER}}}
{s} .sf{{font-family:'Serif',serif;letter-spacing:-0.02em}} {s} .it{{font-style:italic}}
{s} .cap{{letter-spacing:.07em}}
{s} .w,{s} .f,{s} .up,{s} .st{{animation-fill-mode:both;animation-timing-function:{lib.EASE_OUT}}}
{s} .w{{animation-name:{sid}wipe;animation-duration:380ms}}
{s} .f{{animation-name:{sid}rise;animation-duration:400ms}}
{s} .up{{animation-name:{sid}up;animation-duration:560ms}}
{s} .st{{animation-name:{sid}stamp;animation-duration:200ms;transform-box:fill-box;transform-origin:center}}
{s} .cur{{animation:{sid}blink 1.1s steps(1) infinite}}
@keyframes {sid}wipe{{from{{clip-path:inset(-8px 100% -8px -8px)}}to{{clip-path:inset(-8px -8px -8px -8px)}}}}
@keyframes {sid}rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@keyframes {sid}up{{from{{transform:translateY(32px)}}to{{transform:none}}}}
@keyframes {sid}stamp{{from{{opacity:0;transform:scale(1.15)}}to{{opacity:1;transform:none}}}}
@keyframes {sid}blink{{0%,50%{{opacity:1}}50.01%,100%{{opacity:0}}}}
@keyframes {sid}fade{{from{{opacity:0}}to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{
  {s} .w,{s} .f,{s} .up,{s} .st{{animation:{sid}fade 300ms {lib.EASE_OUT} both !important;animation-delay:0ms !important}}
  {s} .cur,{s} .loop{{animation:none !important;opacity:1}}
  {s} .dev{{animation:none !important;opacity:0}}
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
    """Still paper: blurred shadow, gradient, grain. `shape` lacks fill and close."""
    return (f'{shape} fill="#000" filter="url(#{sid}S)"/>'
            f'{shape} fill="url(#{sid}{fill})"/>'
            f'{shape} fill="#fff" filter="url(#{sid}G)"/>')


def sheet_moving(sid: str, shape: str) -> str:
    """Paper that animates: offset shadows and gradient only, no filters."""
    return (f'<g transform="translate(0 6)" opacity=".28">{shape} fill="#000"/></g>'
            f'<g transform="translate(0 3)" opacity=".22">{shape} fill="#000"/></g>'
            f'{shape} fill="url(#{sid}P)"/>')


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
    assert r_start - l_end >= 8, f"row too tight: {left!r} / {right!r}"
    return (f'<g class="w" {D(delay)}>' + txt(xl, y, left, lcls, size) + leader(l_end, r_start, y)
            + txt(xr, y, right, rcls, size, "end") + "</g>")


def stamp(x, y, rot, w, h, line1, line2, delay) -> str:
    sub = (f'<text x="0" y="16" text-anchor="middle" font-size="11.5" class="rd cap">{esc(line2)}</text>' if line2 else "")
    y1 = 0 if line2 else 8
    return (f'<g transform="translate({x} {y}) rotate({rot})"><g class="st" {D(delay)}><g opacity=".9">'
            f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="4" fill="none" stroke="{RED}" stroke-width="3.5"/>'
            f'<rect x="{-w/2+6}" y="{-h/2+6}" width="{w-12}" height="{h-12}" rx="2" fill="none" stroke="{RED}" stroke-width="1.2"/>'
            f'<text x="0" y="{y1}" text-anchor="middle" font-size="{18 if line2 else 21}" class="b rd" style="letter-spacing:.08em">{esc(line1)}</text>'
            f'{sub}</g></g></g>')


def cue(x, y, s, delay=0, anchor="end") -> str:
    return f'<g class="w" {D(delay)}>' + txt(x, y, s, "rd b cap", 13, anchor) + "</g>"


def bg(h: int, color: str = DESK) -> str:
    return f'<rect width="{W}" height="{h}" rx="{RX}" fill="{color}"/>'


def card(sid: str, h: int, body: str, label: str, extra_css: str = "", extra_defs: str = "") -> str:
    return lib.svg(sid, W, h, body, css(sid, body, extra_css), label, defs(sid) + extra_defs)


def write(out: Path, name: str, s: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / name).write_text(s, encoding="utf-8")


# ------------------------------------------------------------------ row 1: hero
HERO_H = 520


def hero_receipt() -> str:
    sid, H = "osHeroR", HERO_H
    rx, rw, top, bot = 16, 388, 40, 480
    teeth, x, up = [], rx, False
    while x < rx + rw:
        x += 10
        teeth.append(f"{min(x, rx + rw)},{bot + (0 if up else 8)}")
        up = not up
    path = f"M{rx},{top} H{rx+rw} V{bot} " + " ".join(f"L{p}" for p in reversed(teeth)) + f" L{rx},{bot} Z"
    xl, xr = 36, 388
    b = [bg(H)]
    r = [sheet_moving(sid, f'<path d="{path}"')]
    t, st = 350, 55
    r.append(f'<g class="w" {D(t-st)}>' + txt(xl, 72, "HELLO THERE! I'M", "b cap", 13) + "</g>")
    r.append(f'<g class="w" {D(t)}>' + txt(xl, 114, "RAFAEL PEREIRA", "sf", 44, extra='style="letter-spacing:-0.01em"') + "</g>")
    r.append(f'<g class="w" {D(t+st)}>' + txt(xl, 138, "SOFTWARE ENGINEER · GETNET · SÃO PAULO", "mu b", 12.5) + "</g>")
    r.append(f'<g class="w" {D(t+2*st)}>' + txt(xl, 156, "OPEN FINANCE · PIX · AI CHAMPION, 9 SQUADS", "mu", 12.5) + "</g>")
    r.append(f'<line class="w" {D(t+3*st)} x1="{xl}" y1="174" x2="{xr}" y2="174" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    items = [("01 Event-Driven Architecture", "enthusiast"), ("02 gRPC", "user"), ("03 Java", "enthusiast"),
             ("04 Rust", "high performance"), ("05 AI tokens", "minimized")]
    y = 204
    for i, (l, rr) in enumerate(items):
        r.append(row(xl, xr, y, l, rr, 14, t + (4 + i) * st))
        y += 30
    r.append(f'<g class="w" {D(t+9*st)}><line x1="{xl}" y1="{y-12}" x2="{xr}" y2="{y-12}" stroke="{INK}" stroke-width="3"/>'
             f'<line x1="{xl}" y1="{y-7}" x2="{xr}" y2="{y-7}" stroke="{INK}" stroke-width="1"/></g>')
    y += 22
    r.append(row(xl, xr, y, "METHOD", "deterministic first", 14, t + 10 * st, rcls="b"))
    y += 38
    t_last = t + 11 * st
    r.append(f'<g class="w" {D(t_last)}>' + txt(xl, y, "@Raphonzius", "b", 14) + "</g>")
    r.append(f'<g class="f" {D(t_last + 380)}><rect class="cur" x="{xl + 11 * 8.4 + 5:.0f}" y="{y-11}" width="8" height="13" fill="{INK}"/></g>')
    r.append(f'<line x1="{rx}" y1="{bot-14}" x2="{rx+rw}" y2="{bot-14}" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="1 5" stroke-linecap="round" opacity=".7"/>')
    r.append(stamp(304, y + 4, -6, 152, 44, "APPROVED", "", 1350))
    b.append(f'<clipPath id="{sid}C"><rect x="0" y="{top}" width="{W}" height="{H}"/></clipPath>'
             f'<g clip-path="url(#{sid}C)"><g class="f" style="animation-name:{sid}print;animation-duration:1100ms;'
             f'animation-delay:150ms;will-change:transform">' + "".join(r) + "</g></g>")
    b.append(f'<rect x="6" y="14" width="408" height="30" rx="7" fill="{DESK_2}"/>'
             f'<rect x="6" y="14" width="408" height="2" rx="1" fill="#3a3630"/>'
             f'<rect x="12" y="37" width="396" height="5" rx="2" fill="#0d0c0a"/>'
             f'<circle cx="398" cy="26" r="3" fill="{RED}"/>')
    return card(sid, H, "".join(b),
                "Hello there! I'm Rafael Pereira, Software Engineer at Getnet, São Paulo: Event-Driven Architecture enthusiast, gRPC user, Java enthusiast, Rust for high performance, AI tokens minimized. Method: deterministic first. Opens LinkedIn.",
                f"@keyframes {sid}print{{from{{transform:translateY(-{bot-top+20}px)}}to{{transform:none}}}}")


def hero_quote() -> str:
    sid, H, d = "osHeroQ", HERO_H, lib.data()
    b = [bg(H)]
    b.append(f'<g class="f" {D(150)}><g transform="rotate(2 210 150)">'
             + sheet_moving(sid, '<rect x="112" y="36" width="196" height="226"')
             + f'<image href="{d["avatar"]}" x="122" y="46" width="176" height="176" preserveAspectRatio="xMidYMid slice"/>'
             f'<rect class="dev" x="122" y="46" width="176" height="176" fill="{PAPER}" opacity="0" '
             f'style="animation:{sid}dev 1.6s {lib.EASE_OUT} 400ms both"/>'
             f'<text x="210" y="248" text-anchor="middle" font-size="19" class="sf it">São Paulo, Brazil</text>'
             f'<rect x="175" y="26" width="70" height="22" fill="#e9dfc4" opacity=".8" transform="rotate(-4 210 37)"/>'
             "</g></g>")
    for i, l in enumerate(["If it can be", "deterministic,", "it should not", "be inference."]):
        b.append(f'<g class="w" {D(300 + i * STAG)}>' + txt(210, 334 + i * 42, l, "sf pp", 42, "middle",
                                                         'style="letter-spacing:-0.015em;word-spacing:.06em"') + "</g>")
    b.append(cue(210, 494, "CONNECT ON LINKEDIN →", 600, "middle"))
    return card(sid, H, "".join(b),
                "Polaroid of Rafael's avatar, São Paulo, Brazil. Tagline: if it can be deterministic, it should not be inference. Opens LinkedIn.",
                f"@keyframes {sid}dev{{from{{opacity:1}}to{{opacity:0}}}}")


# ------------------------------------------------------------------ row 2: LVC, an open folder
LVC_H = 640
LOG = [("14:02:31", "LIVE", "bus · CHECKIN"), ("14:02:30", "VIRTUAL", "area · MISSION_TRIGGER"),
       ("14:02:28", "CONSTR.", "drone · TELEMETRY"), ("14:02:27", "LIVE", "cgesp · FLOOD_ALERT")]


def _folder(sid: str, H: int, tab: bool) -> list[str]:
    b = [bg(H)]
    if tab:
        b.append(f'<path d="M16,64 V50 Q16,36 30,36 H290 Q302,36 308,48 L316,64 Z" fill="{FOLD_E}"/>')
    b.append(sheet(sid, f'<rect x="16" y="62" width="{W-32}" height="{H-86}" rx="5"', "F"))
    b.append(f'<g transform="rotate({1.2 if tab else -1.0} 210 340)">' + sheet(sid, f'<rect x="36" y="84" width="{W-72}" height="{H-128}" rx="2"') + "</g>")
    b.append(sheet(sid, f'<rect x="32" y="80" width="{W-64}" height="{H-122}" rx="2"'))
    return b


def lvc_cover() -> str:
    sid, H = "osLvcA", LVC_H
    b = _folder(sid, H, tab=True)
    b.append(txt(32, 56, "FULL PAPER · LATINOWARE 2026", "b cap", 13))
    b.append(f'<path d="M72,64 v52 a9,9 0 0 0 18,0 v-46 a5,5 0 0 0 -10,0 v40" fill="none" stroke="#8d8a83" stroke-width="3" stroke-linecap="round"/>')
    x = 56
    b.append(f'<g class="w" {D(80)}>' + txt(x, 160, "Open Source LVC", "sf", 42) + "</g>")
    b.append(f'<g class="w" {D(140)}>' + txt(x, 204, "Simulation", "sf it", 42) + "</g>")
    b.append(f'<g class="w" {D(200)}>' + txt(x, 248, "Architecture", "sf it", 42) + "</g>")
    b.append(f'<g class="w" {D(260)}>' + txt(x, 280, "First author · Mackenzie", "mu b", 13.5)
             + txt(x, 299, "Campus Living Lab · open source", "mu b", 13.5) + "</g>")
    b.append(f'<line class="w" {D(300)} x1="{x}" y1="318" x2="{W-56}" y2="318" stroke="{RED}" stroke-width="1.6"/>')
    abstract = ("Live, Virtual and Constructive simulation without HLA or DIS: Event Sourcing, CQRS "
                "and one gRPC contract for Java, Python and Rust.")
    for i, l in enumerate(textwrap.wrap(abstract, 36)):
        b.append(f'<g class="w" {D(340 + i * STAG)}>' + txt(x, 346 + i * 23, l, "", 14.5) + "</g>")
    b.append(stamp(210, 488, -6, 220, 58, "PRESENTED", "PROCEEDINGS SOON", 700))
    b.append(cue(W - 56, H - 62, "READ THE PAPER →", 800))
    return card(sid, H, "".join(b),
                "Full paper, Latinoware 2026: Open Source LVC Simulation Architecture. First author. Live, Virtual and Constructive simulation without HLA or DIS: Event Sourcing, CQRS and one gRPC contract for Java, Python and Rust. Presented, proceedings soon. Opens the paper site.")


def lvc_contents() -> str:
    sid, H = "osLvcB", LVC_H
    b = _folder(sid, H, tab=False)
    x, xr = 56, W - 56
    b.append(f'<g class="w" {D(80)}>' + txt(x, 114, "SIX MODULES", "mu b cap", 13) + "</g>")
    mods = [("live-ms-java", "Java"), ("virtual-ms-java", "Java"), ("constructive-ms-python", "Python"),
            ("event-hub-ms-rust", "Rust"), ("proto-shared", "gRPC"), ("infra-local-shared", "Compose")]
    for i, (m, l) in enumerate(mods):
        b.append(row(x, xr, 140 + i * 24, m, l, 13.5, 120 + i * STAG, rcls="mu", lcls="b"))
    b.append(f'<g class="w" {D(300)}>' + txt(x, 298, "VALIDATED ON", "mu b cap", 13) + "</g>")
    val = [("Traceability", "replay the log"), ("Reproducible", "compose up"),
           ("Multi-language", "one .proto"), ("Real sources", "AIS, CGESP")]
    for i, (k, v) in enumerate(val):
        b.append(row(x, xr, 324 + i * 24, k, v, 13.5, 340 + i * STAG, rcls="mu", lcls="b"))
    ly, rh, shown = 432, 24, 4
    b.append(f'<g class="w" {D(520)}>' + txt(x, ly, "EVENT STORE", "mu b cap", 13)
             + txt(xr, ly, "illustrative", "mu it", 13, "end") + "</g>")
    wy, wh = ly + 12, rh * shown + 14
    b.append(f'<g class="f" {D(560)}><rect x="{x-8}" y="{wy}" width="{xr-x+16}" height="{wh}" rx="3" fill="{DESK}"/>')
    b.append(f'<clipPath id="{sid}L"><rect x="{x-8}" y="{wy}" width="{xr-x+16}" height="{wh}" rx="3"/></clipPath>')
    lines = []
    for k, (tm, dom, ev) in enumerate(LOG * 2):
        yy = wy + 24 + k * rh
        col = {"LIVE": "#e98d74", "VIRTUAL": "#dcc890", "CONSTR.": "#bccfae"}[dom]
        lines.append(f'<text x="{x+4}" y="{yy}" font-size="12" style="fill:#9a9384">{tm}</text>'
                     f'<text x="{x+72}" y="{yy}" font-size="12.5" class="b" style="fill:{col}">{dom}</text>'
                     f'<text x="{x+136}" y="{yy}" font-size="12.5" style="fill:{PAPER}">{esc(ev)}</text>')
    b.append(f'<g clip-path="url(#{sid}L)"><g class="loop" style="animation:{sid}log 10s infinite">'
             + "".join(lines) + "</g></g></g>")
    b.append(cue(xr, H - 62, "SOURCE CODE →", 700))
    n = len(LOG)
    steps = "".join(f"{k/n*100:.1f}%,{(k+0.8)/n*100:.1f}%{{transform:translateY(-{k*rh}px)}}" for k in range(n))
    extra = (f"@keyframes {sid}log{{{steps}100%{{transform:translateY(-{n*rh}px)}}}}"
             f"#{sid} .loop{{animation-timing-function:{lib.EASE_IN_OUT} !important}}")
    return card(sid, H, "".join(b),
                "Inside the folder: six modules (live-ms-java, virtual-ms-java, constructive-ms-python, event-hub-ms-rust, proto-shared, infra-local-shared); validated on traceability, reproducibility, multi-language and real sources; an illustrative event store. Opens the source code on GitHub.",
                extra)


# ------------------------------------------------------------------ row 3-4: projects
PROJECTS = [
    ("poc-grpc", "Java", ["gRPC client and server on one", "shared Protobuf contract."]),
    ("Demo-SpringSecurity6-JWT", "Java", ["Stateless auth: Spring Security 6,", "OAuth2 resource server, RSA JWT."]),
    ("spring-and-vue", "Java · Vue", ["Spring Boot API with a Vue", "front end."]),
    ("cachyos-setup", "Shell", ["Reproducible CachyOS setup: KDE,", "dotfiles and package lists."]),
]


def project(i: int) -> str:
    name, lang, desc = PROJECTS[i]
    H, sid = 172, f"osPrj{i}"
    b = [bg(H, DESK_2), f'<clipPath id="{sid}C"><rect x="0" y="0" width="{W}" height="{H-20}"/></clipPath>']
    c = [sheet_moving(sid, f'<rect x="14" y="14" width="{W-28}" height="{H-28}" rx="3"'),
         txt(32, 46, name, "b", 17),
         f'<line x1="14" y1="60" x2="{W-14}" y2="60" stroke="{RED}" stroke-width="1.6"/>']
    for k, l in enumerate(desc):
        yy = 86 + k * 23
        c.append(txt(32, yy, l, "", 14))
        c.append(f'<line x1="14" y1="{yy+7}" x2="{W-14}" y2="{yy+7}" stroke="{RULE}" stroke-width="1"/>')
    c.append(txt(32, H - 36, lang, "mu b", 13))
    c.append(txt(W - 32, H - 36, "→", "rd b", 17, "end"))
    b.append(f'<g clip-path="url(#{sid}C)"><g class="up" {D(80 + i * STAG)}>' + "".join(c) + "</g></g>")
    b.append(f'<path d="M0,{H-22} H{W} V{H-RX} Q{W},{H} {W-RX},{H} H{RX} Q0,{H} 0,{H-RX} Z" fill="#191714"/>'
             f'<rect x="{W/2-28}" y="{H-15}" width="56" height="7" rx="3.5" fill="#3a3630"/>')
    return card(sid, H, "".join(b), f"{name}: {' '.join(desc)} {lang}. Opens the repository.")


# ------------------------------------------------------------------ row 5: desk
DESK_H = 450
SCREEN_LINES = [("$ whoami", True), ("rafael · backend java", False), ("$ java --version", True),
                ("openjdk 21", False), ("$ cat focus.txt", True), ("events, grpc, rust,", False),
                ("fewer tokens", False)]


def desk_computer() -> str:
    sid, H = "osDeskC", DESK_H
    BEIGE, BEIGE_D, SCREEN, PHOS, DIM = "#d9cfb8", "#bfb397", "#1c211b", "#e9e2cf", "#aaa391"
    ox, oy = 5, 42
    b = [bg(H)]
    c = [f'<ellipse cx="{205+ox}" cy="{338+oy}" rx="160" ry="10" fill="#000" opacity=".4"/>',
         f'<rect x="{70+ox}" y="{40+oy}" width="270" height="206" rx="14" fill="{BEIGE}"/>',
         f'<rect x="{70+ox}" y="{40+oy}" width="270" height="6" rx="3" fill="#e6dcc6"/>',
         f'<rect x="{92+ox}" y="{60+oy}" width="226" height="160" rx="8" fill="{SCREEN}"/>',
         f'<rect x="{92+ox}" y="{60+oy}" width="226" height="160" rx="8" fill="url(#{sid}Gl)"/>',
         f'<rect x="{180+ox}" y="{246+oy}" width="50" height="18" fill="{BEIGE_D}"/>',
         f'<rect x="{120+ox}" y="{262+oy}" width="170" height="14" rx="3" fill="{BEIGE}"/>',
         f'<rect x="{262+ox}" y="{229+oy}" width="58" height="5" rx="2" fill="{BEIGE_D}"/>',
         f'<circle cx="{96+ox}" cy="{232+oy}" r="3.5" fill="{RED}"/>',
         f'<path d="M{60+ox},{328+oy} L{84+ox},{288+oy} H{326+ox} L{350+ox},{328+oy} Z" fill="{BEIGE}"/>',
         f'<path d="M{60+ox},{328+oy} H{350+ox} V{336+oy} H{60+ox} Z" fill="{BEIGE_D}"/>']
    for r in range(3):
        y = 296 + oy + r * 10
        x0, x1 = 92 + ox - r * 6, 318 + ox + r * 6
        for k in range(14):
            kx = x0 + k * (x1 - x0) / 14
            c.append(f'<rect x="{kx+1:.1f}" y="{y}" width="{(x1-x0)/14-3:.1f}" height="6" rx="1" fill="{BEIGE_D}"/>')
    b.append(f'<g class="f" {D(0)}>' + "".join(c) + "</g>")
    cyc, extra = 11.0, []
    tx = 106 + ox
    for i, (l, cmd) in enumerate(SCREEN_LINES):
        a = (0.5 + i * 0.85) / cyc * 100
        extra.append(f"@keyframes {sid}L{i}{{0%,{a:.1f}%{{clip-path:inset(-4px 100% -4px -4px);opacity:1}}"
                     f"{a+4:.1f}%,90%{{clip-path:inset(-4px -4px -4px -4px);opacity:1}}"
                     f"95%,100%{{clip-path:inset(-4px -4px -4px -4px);opacity:0}}}}"
                     f"#{sid} .l{i}{{animation:{sid}L{i} {cyc}s linear infinite}}")
        b.append(f'<g class="loop l{i}"><text x="{tx}" y="{84 + oy + i * 18}" font-size="12.5" class="{"b" if cmd else ""}" '
                 f'style="fill:{PHOS if cmd else DIM}">{esc(l)}</text></g>')
    yl = 84 + oy + len(SCREEN_LINES) * 18
    b.append(f'<text x="{tx}" y="{yl}" font-size="12.5" class="b" style="fill:{PHOS}">$</text>'
             f'<rect class="cur" x="{tx+13}" y="{yl-11}" width="8" height="13" fill="{PHOS}"/>')
    gl = (f'<radialGradient id="{sid}Gl" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#fff" stop-opacity=".07"/>'
          f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
    return card(sid, H, "".join(b),
                "A retro computer typing a terminal session: whoami, rafael, backend java; java --version, openjdk 21; cat focus.txt, events, grpc, rust, fewer tokens. Opens all repositories.",
                "".join(extra), gl)


def desk_tools() -> str:
    sid, H = "osDeskT", DESK_H
    sx, sy, swid, sh = 20, 30, 380, 394
    xl, xr = sx + 28, sx + swid - 28
    slip = [sheet(sid, f'<rect x="{sx}" y="{sy}" width="{swid}" height="{sh}" rx="2"')]
    slip.append(f'<g class="w" {D(120)}>' + txt(xl, sy + 54, "Daily Tools", "sf", 38) + "</g>")
    slip.append(f'<line class="w" {D(160)} x1="{xl}" y1="{sy+70}" x2="{xr}" y2="{sy+70}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    y = sy + 98
    groups = [("PROGRAMMING", ["Java · Spring · Bash", "JavaScript · Python"]),
              ("OS", ["Linux · Ubuntu · Red Hat · Windows"]),
              ("UTILITIES", ["AWS · Git · Podman · Jenkins", "Postman"])]
    for i, (g, vals) in enumerate(groups):
        g_ = [txt(xl, y, g, "mu b cap", 13)] + [txt(xl, y + 21 + k * 20, v, "b", 14) for k, v in enumerate(vals)]
        slip.append(f'<g class="w" {D(220 + i * STAG)}>' + "".join(g_) + "</g>")
        y += 21 + len(vals) * 20 + 12
    slip.append(f'<line class="w" {D(420)} x1="{xl}" y1="{y-6}" x2="{xr}" y2="{y-6}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    for i, (k, v) in enumerate([("BEFORE", "~3 years at Samsung SDS"), ("OFF THE CLOCK", "Scout volunteer")]):
        slip.append(row(xl, xr, y + 18 + i * 25, k, v, 13, 480 + i * STAG, rcls="", lcls="mu b"))
    slip.append(cue(xr, sy + sh - 20, "ALL REPOSITORIES →", 620))
    pin = (f'<circle cx="{sx+swid/2}" cy="{sy+12}" r="7" fill="{RED}"/>'
           f'<circle cx="{sx+swid/2-2}" cy="{sy+10}" r="2.2" fill="#fff" opacity=".55"/>')
    b = [bg(H), f'<g transform="rotate(-0.8 {sx+swid/2} {sy})">' + "".join(slip) + pin + "</g>"]
    return card(sid, H, "".join(b),
                "Daily Tools. Programming: Java, Spring, Bash, JavaScript, Python. OS: Linux, Ubuntu, Red Hat, Windows. Utilities: AWS, Git, Podman, Jenkins, Postman. Before: about 3 years at Samsung SDS. Off the clock: Scout volunteer. Opens all repositories.")


# ------------------------------------------------------------------ row 6: record
REC_H = 340
RECORD = [("2 days", "Java 17 to 21, Spring Boot 3.5 to 4.1, with AI agents. Other squads: 2 sprints.", True),
          ("USD 37k", "a year saved on AWS at Samsung SDS (rightsizing, arm64).", False),
          ("670k+", "SMS and WhatsApp messages a month, in 4 countries.", False),
          ("45%", "of subtasks sent to the cheapest mode by the task routing plugin at Getnet's Devin Enterprise.", False)]


def record(half: int) -> str:
    sid, H, m = f"osRec{half}", REC_H, 16
    b = [bg(H), sheet(sid, f'<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m-6}" rx="3"')]
    if half == 0:
        b.append(f'<g class="w" {D(0)}>' + txt(m + 20, m + 30, "SHIPPED, IN NUMBERS", "mu b cap", 13) + "</g>")
    else:
        b.append(cue(W - m - 20, m + 30, "CV ON LINKEDIN →", 0))
    b.append(f'<line x1="{m}" y1="{m+44}" x2="{W-m}" y2="{m+44}" stroke="{RULE}" stroke-width="1"/>')
    colw = (W - 2 * m) / 2
    for j in range(2):
        big, small, red = RECORD[half * 2 + j]
        x = m + j * colw
        g_ = [txt(x + 20, 126, big, "sf rd" if red else "sf", 52, extra='style="letter-spacing:-0.025em"')]
        for k, line in enumerate(textwrap.wrap(small, 17)):
            g_.append(txt(x + 20, 160 + k * 21, line, "", 15))
        b.append(f'<g class="f" {D(80 + j * STAG)}>' + "".join(g_) + "</g>")
    xm = m + colw
    b.append(f'<line x1="{xm}" y1="{m+52}" x2="{xm}" y2="{H-m-14}" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="1 5" stroke-linecap="round"/>'
             f'<circle cx="{xm}" cy="{H-m-6}" r="8" fill="{DESK}"/>')
    label = "; ".join(f"{a} {c}" for a, c, _r in RECORD[half * 2: half * 2 + 2])
    return card(sid, H, "".join(b), ("Shipped, in numbers: " if half == 0 else "") + label + " Opens LinkedIn.")


# ------------------------------------------------------------------ row 7: contact tickets
def ticket(sid: str, stub: str, label: str, value: str, red: bool = False) -> str:
    H, sw = 86, 104
    b = [bg(H),
         sheet(sid, f'<rect x="10" y="10" width="{W-20}" height="{H-26}" rx="3"'),
         f'<line x1="{10+sw}" y1="16" x2="{10+sw}" y2="{H-22}" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="1 5" stroke-linecap="round"/>',
         f'<circle cx="{10+sw}" cy="10" r="6" fill="{DESK}"/><circle cx="{10+sw}" cy="{H-16}" r="6" fill="{DESK}"/>']
    b.append(f'<g class="f" {D(0)}>'
             + txt(10 + sw / 2, (H - 6) / 2 + 5, stub, ("b rd" if red else "b") + " cap", 14, "middle")
             + txt(sw + 30, 35, label, "mu", 13) + txt(sw + 30, 58, value, "b", 14)
             + txt(W - 26, 58, "→", "rd b", 16, "end") + "</g>")
    return card(sid, H, "".join(b), f"{label}: {value}", f"#{sid} .f{{animation-duration:240ms}}")


def build(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.svg"):
        old.unlink()
    cards = {"hero-receipt": hero_receipt(), "hero-quote": hero_quote(),
             "lvc-cover": lvc_cover(), "lvc-contents": lvc_contents(),
             "desk-computer": desk_computer(), "desk-tools": desk_tools(),
             "record-1": record(0), "record-2": record(1),
             "link-mail": ticket("osLnkMail", "EMAIL", "Email Rafael", "rafael.informa@gmail.com"),
             "link-linkedin": ticket("osLnkIn", "LINKEDIN", "LinkedIn profile", "in/rafaelrodriguespereira")}
    for i in range(len(PROJECTS)):
        cards[f"project-{i+1}"] = project(i)
    for n, s in cards.items():
        write(out_dir, f"{n}.svg", s)


if __name__ == "__main__":
    build(lib.ROOT / "assets" / "oldschool")
    print("ok")
