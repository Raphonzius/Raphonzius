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
    b.append(f'<g class="w" {D(t)}>' + txt(xl, 90, "RAFAEL PEREIRA", "sf", 50) + "</g>")
    b.append(f'<g class="w" {D(t+st)}>' + txt(xl, 118, "SOFTWARE ENGINEER · GETNET · SÃO PAULO", "mu b", 13) + "</g>")
    b.append(f'<g class="w" {D(t+2*st)}>' + txt(xl, 138, "OPEN FINANCE APIS · PIX · AI CHAMPION, 9 SQUADS", "mu", 13) + "</g>")
    b.append(f'<line class="w" {D(t+3*st)} x1="{xl}" y1="158" x2="{xr}" y2="158" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    items = [("01  Event-Driven Architecture", "enthusiast"), ("02  gRPC", "user"),
             ("03  Java", "enthusiast"), ("04  Rust", "high performance"),
             ("05  AI tokens", "minimized")]
    y = 192
    for i, (l, r) in enumerate(items):
        b.append(row(xl, xr, y, l, r, 16.5, t + (4 + i) * st))
        y += 34
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


# ------------------------------------------------------------------ focus (paper tape)
def focus() -> str:
    H, T, TH = 500, 104, 214
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{PAPER}" stroke="{RULE}"/>']
    b.append(f'<g class="w" {D(0)}>' + txt(40, 60, "How I build", "sf", 44) + "</g>")
    b.append(f'<g class="w" {D(120)}>' + txt(40, 86, "Open Finance APIs under P95/P99 and TPS targets · RabbitMQ · Azure Service Bus · Event Hubs", "mu", 13) + "</g>")
    b.append(f'<g class="w" {D(220)}><rect x="0" y="{T}" width="{W}" height="{TH}" fill="{TAPE}"/>')
    for yy in (T + 12, T + TH - 12):
        for x in range(16, W, 22):
            b.append(f'<circle cx="{x}" cy="{yy}" r="3.2" fill="{PAPER}"/>')
    b.append("</g>")
    m = T + 84                      # main axis
    ca, cb = m - 40, m + 40         # consumers
    dq = m + 78                     # dlq centre
    ar = f'<marker id="osA" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{INK}"/></marker>'
    arr = f'<marker id="osR" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{RED}"/></marker>'
    ln = f'fill="none" stroke="{INK}" stroke-width="1.6" marker-end="url(#osA)"'
    lr = f'fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#osR)"'
    bx = {"api": 40, "out": 208, "brk": 376, "con": 600}
    nw, nh = 128, 52
    b.append(f'<g class="w" {D(650)}>'
             f'<path d="M168 {m} H206" {ln}/><path d="M336 {m} H374" {ln}/>'
             f'<path d="M504 {m} H552 V{ca} H598" {ln}/><path d="M552 {m} V{cb} H598" {ln}/></g>')
    bq = dq - nh // 2
    b.append(f'<g class="w" {D(1100)}><path d="M440 {m+nh//2} V{bq-2}" {lr}/>'
             f'<path d="M376 {dq} H358 V{m+14} H374" {lr}/>'
             + txt(450, (m + nh // 2 + bq) // 2 + 4, "on failure", "rd", 12)
             + txt(350, dq - 30, "retry", "rd", 12, "end") + "</g>")
    # packets: drawn before nodes so they slide behind the boxes
    def packet(path, color, begin):
        return (f'<g visibility="hidden"><set attributeName="visibility" to="visible" begin="{begin}s"/>'
                f'<rect x="-8" y="-5" width="16" height="10" rx="1" fill="{color}"/>'
                f'<line x1="-8" y1="-5" x2="0" y2="1" stroke="{PAPER}" stroke-width="1"/><line x1="8" y1="-5" x2="0" y2="1" stroke="{PAPER}" stroke-width="1"/>'
                f'<animateMotion dur="10s" begin="{begin}s" repeatCount="indefinite" path="{path}" calcMode="linear"/></g>')
    pa = f"M104 {m} H552 V{ca} H680"
    pb = f"M104 {m} H552 V{cb} H680"
    pf = f"M104 {m} H440 V{dq} H358 V{m+14} H440"
    b.append(packet(pa, INK, 2.6) + packet(pb, INK, 5.9) + packet(pf, RED, 4.2))

    def node(x, cy, w, name, sub, d, red=False):
        stroke = RED if red else INK
        return (f'<g class="f" {D(d)}><rect x="{x}" y="{cy-nh//2}" width="{w}" height="{nh}" rx="3" fill="{PAPER}" stroke="{stroke}" stroke-width="1.8"/>'
                + txt(x + w / 2, cy - 2, name, "b rd" if red else "b", 14, "middle")
                + txt(x + w / 2, cy + 16, sub, "mu", 11, "middle") + "</g>")
    b.append(node(bx["api"], m, nw, "API", "business tx", 500))
    b.append(node(bx["out"], m, nw, "OUTBOX", "same transaction", 580))
    b.append(node(bx["brk"], m, nw, "BROKER", "pub/sub", 660))
    b.append(node(bx["con"], ca, 160, "CONSUMER A", "idempotent", 740))
    b.append(node(bx["con"], cb, 160, "CONSUMER B", "idempotent", 800))
    b.append(node(bx["brk"], dq, nw, "DLQ", "retry with backoff", 880, True))
    # token strip: what runs before the model
    y0 = T + TH + 44
    b.append(f'<g class="w" {D(1150)}>' + txt(40, y0, "Before the model", "sf it", 30)
             + txt(W - 40, y0, "fewer tokens, same answer", "mu", 13, "end") + "</g>")
    b.append(f'<line class="w" {D(1200)} x1="40" y1="{y0+16}" x2="{W-40}" y2="{y0+16}" stroke="{RED}" stroke-width="1.6"/>')
    steps = [("CAG cache", ["answered from", "cache"]), ("Scripts", ["plain code,", "exact answer"]),
             ("Qdrant", ["only the context", "that matters"]), ("Jev / Laya", ["routes to the", "cheapest model"]),
             ("Model", ["only what", "is left"])]
    cw = (W - 80) / len(steps)
    for i, (nm, ds) in enumerate(steps):
        x = 40 + i * cw
        last = i == len(steps) - 1
        g_ = [txt(x, y0 + 50, f"{i+1}", "mu b", 13), txt(x + 18, y0 + 50, nm, "b rd" if last else "b", 16)]
        g_ += [txt(x, y0 + 74 + k * 18, l, "mu", 12.5) for k, l in enumerate(ds)]
        if not last:
            g_.append(txt(x + cw - 18, y0 + 50, "→", "mu", 16))
        b.append(f'<g class="w" {D(1300 + i * 110)}>' + "".join(g_) + "</g>")
    return lib.svg("osFocus", W, H, "".join(b), css("osFocus"),
                   "How I build: API writes to an outbox in the same transaction, the broker fans out to two idempotent consumers, failures go to a DLQ and retry. Before the model: CAG cache, scripts, Qdrant, Jev / Laya routing, then the model gets only what is left.", ar + arr)


# ------------------------------------------------------------------ projects (catalog cards)
def projects() -> str:
    s = lib.summary(lib.data())
    rl = s["repo_lang"]
    items = [("poc-grpc", "Client and server on one shared Protobuf contract."),
             ("grpc-common", "The canonical Protobuf library for every team."),
             ("grpc-server", "Server side of the gRPC POC."),
             ("Demo-SpringSecurity6-JWT", "Stateless auth: Spring Security 6 and JWT."),
             ("spring-and-vue", "Spring Boot API with a Vue front end."),
             ("Capstone-Project", "AWS Academy Cloud Architecting capstone.")]
    cw, ch, g, m = 264, 124, 14, 20
    H = m * 2 + ch * 2 + g
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="#2a2722"/>']
    for i, (nm, ds) in enumerate(items):
        x = m + (i % 3) * (cw + g)
        y = m + (i // 3) * (ch + g)
        d = 100 + i * 90
        lang = rl.get(nm, "")
        g_ = [f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="3" fill="{PAPER}"/>',
              txt(x + 16, y + 28, nm, "b", 14.5),
              f'<line x1="{x}" y1="{y+40}" x2="{x+cw}" y2="{y+40}" stroke="{RED}" stroke-width="1.6"/>']
        for k, line in enumerate(textwrap.wrap(ds, 31)[:2]):
            yy = y + 64 + k * 21
            g_.append(txt(x + 16, yy, line, "", 12.5))
        for k in range(2):
            yy = y + 64 + k * 21 + 6
            g_.append(f'<line x1="{x}" y1="{yy}" x2="{x+cw}" y2="{yy}" stroke="{RULE}" stroke-width="1"/>')
        if lang:
            g_.append(txt(x + 16, y + ch - 12, lang, "mu b", 11.5))
        g_.append(f'<circle cx="{x+cw/2}" cy="{y+ch-14}" r="5" fill="#2a2722"/>')
        b.append(f'<g class="f" {D(d)}>' + "".join(g_) + "</g>")
    return lib.svg("osProj", W, H, "".join(b), css("osProj"),
                   "Library catalog cards: poc-grpc, grpc-common, grpc-server, Demo-SpringSecurity6-JWT, spring-and-vue, Capstone-Project.")


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
    b.append(f'<g class="w" {D(0)}>' + txt(46, 44, head, "b", 15) + txt(814, 44, "LAST 12 MONTHS", "mu", 13, "end") + "</g>")
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
    b.append(f'<g class="w" {D(1100)}>' + txt(46, 282, mix, "b", 12.5) + txt(814, 282, "A BIGGER HOLE = MORE", "mu", 12, "end") + "</g>")
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
    # Five cards: the token strip lives in focus, the totals in the punched card header.
    for old in ("tokens.svg", "stats.svg"):
        (out_dir / old).unlink(missing_ok=True)
    for n, f in [("hero", hero), ("record", record), ("focus", focus),
                 ("projects", projects), ("punch", punch)]:
        write(out_dir, f"{n}.svg", f())


if __name__ == "__main__":
    build(lib.ROOT / "assets" / "oldschool")
    print("ok")
