"""oldschool: a Pix receipt and the paper artifacts of an old bank office.

Typefaces: IBM Plex Mono (receipt lines) + Instrument Serif (display). Accent: rubber-stamp red.
Entrances: clip-path wipes (a line "printing") and opacity + 8px rise. Only the flow card loops.
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import lib  # noqa: E402
from lib import esc  # noqa: E402

PAPER, DESK, DESK_L = "#f4efe4", "#1f1d19", "#e6dec9"
INK, MUT, RULE, RED = "#1b1a17", "#5e574a", "#cfc6b0", "#b3261e"
TAPE = "#e8dfc9"
W = 860


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
{s} .w,{s} .f{{animation-fill-mode:both;animation-timing-function:{lib.EASE_OUT}}}
{s} .w{{animation-name:{sid}wipe;animation-duration:620ms}}
{s} .f{{animation-name:{sid}rise;animation-duration:560ms}}
@keyframes {sid}wipe{{from{{clip-path:inset(-8px 100% -8px -8px)}}to{{clip-path:inset(-8px -8px -8px -8px)}}}}
@keyframes {sid}rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@keyframes {sid}fade{{from{{opacity:0}}to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{{s} .w,{s} .f{{animation:{sid}fade 300ms linear both !important}}}}
""" + extra)


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


def write(out: Path, name: str, s: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / name).write_text(s, encoding="utf-8")


# ------------------------------------------------------------------ hero
def hero() -> str:
    d = lib.data()
    H = 508
    rx, rw, top, bot = 40, 500, 30, 470
    teeth = [f"{rx},{bot}"]
    x, up = rx, False
    while x < rx + rw:
        x += 10
        teeth.append(f"{x},{bot + (0 if up else 8)}")
        up = not up
    path = f"M{rx},{top} H{rx+rw} V{bot} " + " ".join(f"L{p}" for p in reversed(teeth[1:])) + f" L{rx},{bot} Z"
    xl, xr = 68, 512
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{DESK}"/>',
         f'<path d="{path}" fill="#000" opacity=".35" transform="translate(5 5)"/>',
         f'<path d="{path}" fill="{PAPER}"/>']
    t, st = 200, 95
    # header
    b.append(f'<g class="w" {D(t-st)}>' + txt(xl, 64, "HELLO THERE! I'M", "b", 13) + "</g>")
    b.append(f'<g class="w" {D(t)}>' + txt(xl, 104, "RAFAEL PEREIRA", "sf", 46) + "</g>")
    b.append(f'<g class="w" {D(t+st)}>' + txt(xl, 128, "SOFTWARE ENGINEER · GETNET · SÃO PAULO", "mu b", 13) + "</g>")
    b.append(f'<g class="w" {D(t+2*st)}>' + txt(xl, 146, "OPEN FINANCE APIS · PIX · AI CHAMPION, 9 SQUADS", "mu", 13) + "</g>")
    b.append(f'<line class="w" {D(t+3*st)} x1="{xl}" y1="164" x2="{xr}" y2="164" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    items = [("01  Event-Driven Architecture", "enthusiast"), ("02  gRPC", "user"),
             ("03  Java", "enthusiast"), ("04  Rust", "high performance"),
             ("05  AI tokens", "minimized")]
    y = 196
    for i, (l, r) in enumerate(items):
        b.append(row(xl, xr, y, l, r, 16.5, t + (4 + i) * st))
        y += 33
    b.append(f'<line class="w" {D(t+9*st)} x1="{xl}" y1="{y-12}" x2="{xr}" y2="{y-12}" stroke="{INK}" stroke-width="3" />')
    b.append(f'<line class="w" {D(t+9*st)} x1="{xl}" y1="{y-7}" x2="{xr}" y2="{y-7}" stroke="{INK}" stroke-width="1" />')
    y += 22
    b.append(row(xl, xr, y, "METHOD", "deterministic first", 16.5, t + 10 * st, rcls="b"))
    y += 40
    b.append(f'<g class="w" {D(t+11*st)}>' + txt(xl, y, "@Raphonzius", "b", 14) + "</g>")
    # perforation above the torn edge
    b.append(f'<line x1="{rx}" y1="{bot-14}" x2="{rx+rw}" y2="{bot-14}" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="1 5" stroke-linecap="round" opacity=".7"/>')
    # stamp: outer g rotates (static), inner g animates
    b.append(f'<g transform="translate(430 {y+6}) rotate(-6)"><g class="f" {D(t+12*st+250)}>'
             f'<rect x="-84" y="-24" width="168" height="48" rx="4" fill="none" stroke="{RED}" stroke-width="3.5"/>'
             f'<rect x="-78" y="-18" width="156" height="36" rx="2" fill="none" stroke="{RED}" stroke-width="1.2"/>'
             f'<text x="0" y="8" text-anchor="middle" font-size="22" class="b rd" style="letter-spacing:.08em">EFETIVADO</text></g></g>')
    # right column: print + quote
    b.append(f'<g class="f" {D(400)}><g transform="rotate(2 690 150)">'
             f'<rect x="596" y="36" width="196" height="226" fill="{PAPER}"/>'
             f'<image href="{d["avatar"]}" x="606" y="46" width="176" height="176" preserveAspectRatio="xMidYMid slice"/>'
             f'<text x="694" y="248" text-anchor="middle" font-size="19" class="sf it">São Paulo, Brazil</text>'
             "</g></g>")
    q = ["If it can be", "deterministic,", "it should not", "be inference."]
    for i, l in enumerate(q):
        b.append(f'<g class="w" {D(1300+i*150)}>' + txt(590, 318 + i * 38, l, "sf pp", 37) + "</g>")
    return lib.svg("osHero", W, H, "".join(b), css("osHero"),
                   "Pix receipt for Rafael Pereira, Software Engineer at Getnet: Event-Driven Architecture enthusiast, gRPC user, Java enthusiast, Rust for high performance, focused on AI token minimizing with deterministic solutions.")


# ------------------------------------------------------------------ small paper tickets (links)
def ticket(sid: str, stub: str, label: str, value: str, w: int = 420, red: bool = False) -> str:
    """A perforated ticket. Used as a clickable link (wrapped in <a> in the README)."""
    H, sw = 76, 104
    b = [f'<rect width="{w}" height="{H}" rx="6" fill="{DESK}"/>',
         f'<rect x="8" y="8" width="{w-16}" height="{H-16}" rx="3" fill="{PAPER}"/>',
         f'<line x1="{8+sw}" y1="14" x2="{8+sw}" y2="{H-14}" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="1 5" stroke-linecap="round"/>',
         f'<circle cx="{8+sw}" cy="8" r="6" fill="{DESK}"/><circle cx="{8+sw}" cy="{H-8}" r="6" fill="{DESK}"/>']
    b.append(f'<g class="w" {D(100)}>' + txt(8 + sw / 2, H / 2 + 5, stub, "b rd" if red else "b", 14, "middle",
                                            'style="letter-spacing:.08em"') + "</g>")
    b.append(f'<g class="w" {D(220)}>' + txt(sw + 28, 34, label, "mu", 12) + "</g>")
    b.append(f'<g class="w" {D(320)}>' + txt(sw + 28, 56, value, "b", 15) + "</g>")
    return lib.svg(sid, w, H, "".join(b), css(sid), f"{label}: {value}")


# ------------------------------------------------------------------ LVC paper (manila folder)
def lvc() -> str:
    H = 540
    FOLD, FOLD_D = "#e7d6a8", "#d8c48f"
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{DESK}"/>',
         # folder tab + body
         f'<path d="M24,58 V46 Q24,34 36,34 H300 Q310,34 316,44 L326,58 Z" fill="{FOLD_D}"/>',
         f'<rect x="24" y="58" width="{W-48}" height="{H-82}" rx="4" fill="{FOLD}"/>',
         f'<rect x="44" y="76" width="{W-88}" height="{H-118}" rx="2" fill="{PAPER}"/>']
    b.append(f'<g class="w" {D(80)}>' + txt(42, 52, "FULL PAPER · LATINOWARE 2026", "b", 12.5, extra='style="letter-spacing:.06em"') + "</g>")
    x = 72
    b.append(f'<g class="w" {D(200)}>' + txt(x, 136, "Open Source LVC", "sf", 46) + "</g>")
    b.append(f'<g class="w" {D(300)}>' + txt(x, 180, "Simulation Architecture", "sf it", 46) + "</g>")
    b.append(f'<g class="w" {D(420)}>' + txt(x, 210, "First author · Mackenzie Campus Living Lab · open source end to end", "mu b", 13) + "</g>")
    b.append(f'<line class="w" {D(480)} x1="{x}" y1="228" x2="{W-72}" y2="228" stroke="{RED}" stroke-width="1.6"/>')
    abstract = ["Live, Virtual and Constructive simulation without HLA or DIS:",
                "Event Sourcing, CQRS and one gRPC contract for Java, Python and Rust."]
    for i, l in enumerate(abstract):
        b.append(f'<g class="w" {D(560 + i * 110)}>' + txt(x, 256 + i * 22, l, "", 14) + "</g>")
    # modules (left) and validation (right), as receipt rows
    mods = [("live-ms-java", "Java"), ("virtual-ms-java", "Java"), ("constructive-ms-python", "Python"),
            ("event-hub-ms-rust", "Rust"), ("proto-shared", "gRPC"), ("infra-local-shared", "Compose")]
    y = 318
    b.append(f'<g class="w" {D(760)}>' + txt(x, y - 4, "SIX MODULES", "mu b", 11.5, extra='style="letter-spacing:.06em"')
             + txt(500, y - 4, "VALIDATED ON", "mu b", 11.5, extra='style="letter-spacing:.06em"') + "</g>")
    for i, (m, l) in enumerate(mods):
        b.append(row(x, 440, y + 26 + i * 25, m, l, 13, 840 + i * 70, rcls="mu", lcls="b"))
    val = ["Traceability: replay an immutable log", "Reproducibility: docker compose up",
           "Multi-language: one .proto, 3 stacks", "Real sources: AIS, OlhoVivo, CGESP"]
    for i, v in enumerate(val):
        k, rest = v.split(":", 1)
        b.append(f'<g class="w" {D(900 + i * 90)}>' + txt(500, y + 26 + i * 38, k, "b", 13)
                 + txt(500, y + 26 + i * 38 + 17, rest.strip(), "mu", 12) + "</g>")
    # stamp: the proceedings are not out yet
    b.append(f'<g transform="translate(676 122) rotate(-7)"><g class="f" {D(1500)}>'
             f'<rect x="-104" y="-26" width="208" height="52" rx="4" fill="none" stroke="{RED}" stroke-width="3.5"/>'
             f'<rect x="-98" y="-20" width="196" height="40" rx="2" fill="none" stroke="{RED}" stroke-width="1.2"/>'
             f'<text x="0" y="-1" text-anchor="middle" font-size="17" class="b rd" style="letter-spacing:.08em">PRESENTED</text>'
             f'<text x="0" y="15" text-anchor="middle" font-size="10.5" class="rd" style="letter-spacing:.06em">PROCEEDINGS SOON</text></g></g>')
    return lib.svg("osLvc", W, H, "".join(b), css("osLvc"),
                   "Full paper, Latinoware 2026: Open Source LVC Simulation Architecture. Event Sourcing, CQRS and one gRPC contract for Java, Python and Rust, in six open source modules. Proceedings coming soon.")


# ------------------------------------------------------------------ desk: computer + daily tools
def desk() -> str:
    H = 380
    BEIGE, BEIGE_D, SCREEN, PHOS = "#d9cfb8", "#bfb397", "#1c211b", "#e9e2cf"
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{DESK}"/>']
    # retro computer, drawn (no external GIF)
    c = [f'<rect x="64" y="300" width="290" height="10" rx="5" fill="#000" opacity=".35"/>',
         f'<rect x="70" y="40" width="270" height="206" rx="14" fill="{BEIGE}"/>',
         f'<rect x="92" y="60" width="226" height="160" rx="8" fill="{SCREEN}"/>',
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
    screen = ["$ whoami", "rafael · backend java", "$ java --version", "openjdk 21", "$ cat focus.txt",
              "events, grpc, rust,", "fewer tokens"]
    for i, l in enumerate(screen):
        cls = "b" if l.startswith("$") else ""
        b.append(f'<g class="w" {D(350 + i * 170)}><text x="106" y="{84 + i * 18}" font-size="12" class="{cls}" '
                 f'style="fill:{PHOS if cls else "#a9a28f"}">{esc(l)}</text></g>')
    # the only live signal: a blinking cursor
    b.append(f'<rect class="cur" x="106" y="{84 + len(screen) * 18 - 11}" width="8" height="13" fill="{PHOS}"/>')
    # paper slip
    sx, sy, swid, sh = 392, 28, 432, 324
    b.append(f'<g class="f" {D(200)}><rect x="{sx+5}" y="{sy+5}" width="{swid}" height="{sh}" fill="#000" opacity=".35"/>'
             f'<rect x="{sx}" y="{sy}" width="{swid}" height="{sh}" fill="{PAPER}"/></g>')
    xl = sx + 28
    b.append(f'<g class="w" {D(320)}>' + txt(xl, sy + 52, "Daily Tools", "sf", 36) + "</g>")
    b.append(f'<line class="w" {D(400)} x1="{xl}" y1="{sy+68}" x2="{sx+swid-28}" y2="{sy+68}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    groups = [("PROGRAMMING", "Java · Spring · Bash · JavaScript · Python"),
              ("OS", "Linux · Ubuntu · Red Hat · Windows"),
              ("UTILITIES", "AWS · Git · Podman · Jenkins · Postman")]
    y = sy + 96
    for i, (g, v) in enumerate(groups):
        b.append(f'<g class="w" {D(500 + i * 140)}>' + txt(xl, y, g, "mu b", 11.5, extra='style="letter-spacing:.06em"')
                 + txt(xl, y + 20, v, "b", 14) + "</g>")
        y += 50
    b.append(f'<line class="w" {D(950)} x1="{xl}" y1="{y-8}" x2="{sx+swid-28}" y2="{y-8}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    about = [("BEFORE", "~3 years at Samsung SDS, Java on AWS"), ("OFF THE CLOCK", "Scout volunteer")]
    for i, (k, v) in enumerate(about):
        b.append(row(xl, sx + swid - 28, y + 18 + i * 26, k, v, 12.5, 1050 + i * 120, rcls="", lcls="mu b"))
    return lib.svg("osDesk", W, H, "".join(b), css("osDesk", f"#osDesk .cur{{animation:osDeskBlink 1.1s steps(1) infinite}}"
                                                     f"@keyframes osDeskBlink{{50%{{opacity:0}}}}"
                                                     f"@media (prefers-reduced-motion:reduce){{#osDesk .cur{{animation:none}}}}"),
                   "Daily Tools. Programming: Java, Spring, Bash, JavaScript, Python. OS: Linux, Ubuntu, Red Hat, Windows. Utilities: AWS, Git, Podman, Jenkins, Postman.")


# ------------------------------------------------------------------ projects: one catalog card per repo
PROJECTS = [
    ("poc-grpc", "Java", ["gRPC client and server on one shared", "Protobuf contract (+ grpc-common, grpc-server)."]),
    ("Demo-SpringSecurity6-JWT", "Java", ["Stateless auth with Spring Security 6:", "OAuth2 resource server, RSA-signed JWT."]),
    ("spring-and-vue", "Java · Vue", ["Spring Boot API with a Vue front end", "(+ vue-frontend)."]),
    ("cachyos-setup", "Shell", ["Reproducible CachyOS machine: KDE Plasma,", "dotfiles and package lists in one script."]),
]


def project(i: int) -> str:
    name, lang, desc = PROJECTS[i]
    w, H = 420, 150
    sid = f"osPrj{i}"
    b = [f'<rect width="{w}" height="{H}" rx="6" fill="#2a2722"/>',
         f'<g class="f" {D(80 + i * 80)}><rect x="12" y="12" width="{w-24}" height="{H-24}" rx="3" fill="{PAPER}"/>',
         txt(30, 42, name, "b", 15),
         f'<line x1="12" y1="56" x2="{w-12}" y2="56" stroke="{RED}" stroke-width="1.6"/>']
    for k, l in enumerate(desc):
        yy = 80 + k * 21
        b.append(txt(30, yy, l, "", 12.5))
        b.append(f'<line x1="12" y1="{yy+6}" x2="{w-12}" y2="{yy+6}" stroke="{RULE}" stroke-width="1"/>')
    b.append(txt(30, H - 22, lang, "mu b", 11.5))
    b.append(txt(w - 30, H - 22, "→", "rd", 16, "end"))
    b.append(f'<circle cx="{w/2}" cy="{H-26}" r="5" fill="#2a2722"/></g>')
    return lib.svg(sid, w, H, "".join(b), css(sid), f"{name}: {' '.join(desc)}")


# ------------------------------------------------------------------ punched card
def punch() -> str:
    s = lib.summary(lib.data())
    weeks = s["weeks"]
    nz = sorted(x["contributionCount"] for w in weeks for x in w["contributionDays"] if x["contributionCount"])
    q = [nz[int(len(nz) * f)] for f in (0.25, 0.5, 0.75)] if nz else [1, 2, 3]

    def lvl(c):
        return 0 if c == 0 else 1 + sum(c > t for t in q)
    H, x0, y0, px, py = 300, 46, 118, 14.5, 20
    cut = 34
    card = f"M{cut},0 H{W} V{H} H0 V{cut} Z"
    b = [f'<path d="{card}" fill="#efe6cf" stroke="{RULE}"/>']
    head = f"{s['contributions']} CONTRIBUTIONS · {s['commits']} COMMITS · {s['active_days']} ACTIVE DAYS"
    b.append(f'<g class="w" {D(0)}>' + txt(46, 44, head, "b", 15) + txt(814, 44, "THIS ACCOUNT · 12 MONTHS", "mu", 12.5, "end") + "</g>")
    b.append(f'<line x1="0" y1="62" x2="{W}" y2="62" stroke="{RULE}"/>')
    last = ""
    for i, w in enumerate(weeks):
        mo = w["contributionDays"][0]["date"][5:7]
        if mo != last:
            last = mo
            names = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
            b.append(txt(x0 + i * px, 100, names[int(mo) - 1], "mu", 10.5))
    for i, w in enumerate(weeks):
        g_ = []
        for j, dday in enumerate(w["contributionDays"]):
            cx, cy = x0 + i * px + 3.5, y0 + j * py + 8
            L = lvl(dday["contributionCount"])
            if L == 0:
                g_.append(f'<rect x="{cx-1}" y="{cy-1}" width="2" height="2" fill="{MUT}" opacity=".5"/>')
            else:
                hw, hh = 3 + L * 0.9, 8 + L * 1.6
                g_.append(f'<rect x="{cx-hw/2:.1f}" y="{cy-hh/2:.1f}" width="{hw:.1f}" height="{hh:.1f}" rx="1" fill="{DESK}"/>')
        b.append(f'<g class="f" {D(250 + i * 16)}>' + "".join(g_) + "</g>")
    mix = " · ".join(f"{n.upper()} {sh*100:.0f}%" for n, sh, _c in s["stack"][:4])
    b.append(f'<g class="w" {D(1100)}>' + txt(46, 282, mix, "b", 12.5) + txt(814, 282, "MOST OF MY WORK LIVES IN PRIVATE ENTERPRISE ORGS", "rd", 12, "end") + "</g>")
    return lib.svg("osPunch", W, H, "".join(b), css("osPunch"),
                   f"Punched card of the last 53 weeks: a hole for every day with contributions, {s['active_days']} active days.")


# ------------------------------------------------------------------ record (tickets)
def record() -> str:
    H = 280
    tickets = [("2 days", "Java 17 to 21 and Spring Boot 3.5.4 to 4.1.0, migrated with AI agents. Other squads took 2 sprints.", True),
               ("USD 37k", "a year saved on AWS at Samsung SDS: rightsizing and x86_64 to arm64, 20-32% faster instances.", False),
               ("670k+", "SMS and WhatsApp messages a month through notification microservices in 4 countries.", False),
               ("45%", "of execution subtasks sent to Devin Lite, the cheapest mode, by the cloud-orchestrator plugin on 11 repos.", False)]
    m, tw = 20, 205
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{DESK_L}"/>',
         f'<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}" fill="{PAPER}"/>']
    for i, (big, small, red) in enumerate(tickets):
        x = m + i * (W - 2 * m) / 4
        d = 100 + i * 120
        g_ = [txt(x + 20, 96, big, "sf rd" if red else "sf", 58)]
        for k, line in enumerate(textwrap.wrap(small, 21)):
            g_.append(txt(x + 20, 130 + k * 20, line, "", 13))
        b.append(f'<g class="f" {D(d)}>' + "".join(g_) + "</g>")
        if i:
            b.append(f'<line x1="{x}" y1="{m+6}" x2="{x}" y2="{H-m-6}" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="1 5" stroke-linecap="round"/>')
            b.append(f'<circle cx="{x}" cy="{m}" r="8" fill="{DESK_L}"/><circle cx="{x}" cy="{H-m}" r="8" fill="{DESK_L}"/>')
    return lib.svg("osRecord", W, H, "".join(b), css("osRecord"),
                   "Four tickets: 2 days for a migration other squads did in 2 sprints, USD 37k a year saved on AWS, 670k+ messages a month, 45% of subtasks sent to the cheapest mode.")


def build(out_dir: Path) -> None:
    for old in ("tokens.svg", "stats.svg", "focus.svg", "projects.svg"):
        (out_dir / old).unlink(missing_ok=True)
    cards = {"hero": hero(), "lvc": lvc(), "desk": desk(), "record": record(), "punch": punch(),
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
