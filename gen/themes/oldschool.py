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
    d, s = lib.data(), None
    rx, rw, top, bot = 40, 500, 36, 556
    teeth = [f"{rx},{bot}"]
    x, up = rx, False
    while x < rx + rw:
        x += 10
        teeth.append(f"{x},{bot + (0 if up else 8)}")
        up = not up
    path = f"M{rx},{top} H{rx+rw} V{bot} " + " ".join(f"L{p}" for p in reversed(teeth[1:])) + f" L{rx},{bot} Z"
    xl, xr = 68, 512
    b = [f'<rect width="{W}" height="600" rx="6" fill="{DESK}"/>',
         f'<path d="{path}" fill="#000" opacity=".35" transform="translate(5 5)"/>',
         f'<path d="{path}" fill="{PAPER}"/>']
    t = 280
    st = 120
    # header
    b.append(f'<g class="w" {D(t)}>' + txt(xl, 104, "RAFAEL PEREIRA", "sf", 54) + "</g>")
    b.append(f'<g class="w" {D(t+st)}>' + txt(xl, 134, "SOFTWARE ENGINEER · GETNET · SÃO PAULO", "mu b", 13) + "</g>")
    b.append(f'<g class="w" {D(t+2*st)}>' + txt(xl, 156, "OPEN FINANCE APIS · PIX · CONTA DIGITAL", "mu", 13) + "</g>")
    b.append(f'<line class="w" {D(t+3*st)} x1="{xl}" y1="180" x2="{xr}" y2="180" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    items = [("01  Event-Driven Architecture", "enthusiast"), ("02  gRPC", "user"),
             ("03  Java", "enthusiast"), ("04  Rust", "high performance")]
    y = 218
    for i, (l, r) in enumerate(items):
        b.append(row(xl, xr, y, l, r, 17, t + (4 + i) * st))
        y += 38
    b.append(f'<line class="w" {D(t+8*st)} x1="{xl}" y1="{y-14}" x2="{xr}" y2="{y-14}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    y += 16
    b.append(row(xl, xr, y, "FOCUS", "AI token minimizing", 17, t + 9 * st))
    y += 38
    b.append(row(xl, xr, y, "METHOD", "deterministic solutions", 17, t + 10 * st))
    y += 30
    b.append(f'<line class="w" {D(t+11*st)} x1="{xl}" y1="{y}" x2="{xr}" y2="{y}" stroke="{INK}" stroke-width="3" />')
    b.append(f'<line class="w" {D(t+11*st)} x1="{xl}" y1="{y+5}" x2="{xr}" y2="{y+5}" stroke="{INK}" stroke-width="1" />')
    y += 36
    b.append(f'<g class="w" {D(t+12*st)}>' + txt(xl, y, "@Raphonzius", "b", 14) + "</g>")
    b.append(f'<g class="w" {D(t+13*st)}>' + txt(xl, y + 22, "SINCE JAN 2026 AT GETNET", "mu", 12.5) + "</g>")
    # perforation above the torn edge
    b.append(f'<line x1="{rx}" y1="{bot-14}" x2="{rx+rw}" y2="{bot-14}" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="1 5" stroke-linecap="round" opacity=".7"/>')
    # stamp: outer g rotates (static), inner g animates
    b.append(f'<g transform="translate(398 {y+8}) rotate(-8)"><g class="f" {D(t+13.5*st+300)}>'
             f'<rect x="-84" y="-24" width="168" height="48" rx="4" fill="none" stroke="{RED}" stroke-width="3.5"/>'
             f'<rect x="-78" y="-18" width="156" height="36" rx="2" fill="none" stroke="{RED}" stroke-width="1.2"/>'
             f'<text x="0" y="8" text-anchor="middle" font-size="22" class="b rd" style="letter-spacing:.08em">EFETIVADO</text></g></g>')
    # right column: print + quote
    b.append(f'<g class="f" {D(500)}><g transform="rotate(2 700 170)">'
             f'<rect x="590" y="40" width="224" height="268" fill="{PAPER}"/>'
             f'<image href="{d["avatar"]}" x="602" y="52" width="200" height="200" preserveAspectRatio="xMidYMid slice"/>'
             f'<text x="702" y="286" text-anchor="middle" font-size="22" class="sf it">São Paulo, Brazil</text>'
             "</g></g>")
    q = ["If it can be", "deterministic,", "it should not", "be inference."]
    for i, l in enumerate(q):
        b.append(f'<g class="w" {D(1500+i*180)}>' + txt(590, 392 + i * 44, l, "sf pp", 42) + "</g>")
    return lib.svg("osHero", W, 600, "".join(b), css("osHero"),
                   "Pix receipt for Rafael Pereira, Software Engineer at Getnet: Event-Driven Architecture enthusiast, gRPC user, Java enthusiast, Rust for high performance, focused on AI token minimizing with deterministic solutions.")


# ------------------------------------------------------------------ focus (paper tape)
def focus() -> str:
    H, T, TH = 514, 150, 250
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{PAPER}" stroke="{RULE}"/>']
    b.append(f'<g class="w" {D(0)}>' + txt(40, 76, "Event-Driven Architecture", "sf", 52) + "</g>")
    b.append(f'<g class="w" {D(140)}>' + txt(40, 108, "Regulated Open Finance APIs with strict P95/P99 and TPS targets", "mu", 14) + "</g>")
    b.append(f'<g class="w" {D(250)}><rect x="0" y="{T}" width="{W}" height="{TH}" fill="{TAPE}"/>')
    for yy in (T + 12, T + TH - 12):
        for x in range(16, W, 22):
            b.append(f'<circle cx="{x}" cy="{yy}" r="3.2" fill="{PAPER}"/>')
    b.append("</g>")
    m = T + 92                      # main axis
    ca, cb = m - 42, m + 42         # consumers
    dq = T + TH - 52 - 12 + 6       # dlq centre
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
    # typed caption
    cap = ["RabbitMQ  ·  Azure Service Bus  ·  Azure Event Hubs",
           "transactional outbox  ·  idempotent consumers  ·  DLQ with retry",
           "gRPC on one canonical Protobuf contract"]
    for i, c in enumerate(cap):
        b.append(f'<g class="w" {D(1200+i*140)}>' + txt(40, T + TH + 40 + i * 24, c, "b" if i == 0 else "mu", 14) + "</g>")
    return lib.svg("osFocus", W, H, "".join(b), css("osFocus"),
                   "Event flow on paper tape: API writes to an outbox in the same transaction, the broker fans out to two idempotent consumers, failures go to a DLQ and retry back to the broker.", ar + arr)


# ------------------------------------------------------------------ tokens (index card)
def tokens() -> str:
    H = 420
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{PAPER}" stroke="{RULE}"/>']
    b.append(f'<g class="w" {D(0)}>' + txt(40, 78, "If it can be deterministic,", "sf", 52) + "</g>")
    b.append(f'<g class="w" {D(140)}>' + txt(40, 134, "it should not be inference.", "sf it", 52) + "</g>")
    b.append(f'<line class="w" {D(300)} x1="0" y1="162" x2="{W}" y2="162" stroke="{RED}" stroke-width="2"/>')
    rows = [("1", "CAG cache", "Answered from cache. No model call."),
            ("2", "Scripts", "Plain code returns the exact answer."),
            ("3", "Qdrant", "Retrieve from the vector DB instead of re-reading."),
            ("4", "Jev / Laya", "Route the task to the cheapest model that fits."),
            ("5", "Model", "Only what is left.")]
    y = 208
    for i, (n, nm, ds) in enumerate(rows):
        d = 450 + i * 150
        b.append(f'<line class="w" {D(d)} x1="0" y1="{y+14}" x2="{W}" y2="{y+14}" stroke="{RULE}" stroke-width="1.2"/>')
        last = i == len(rows) - 1
        b.append(f'<g class="w" {D(d)}>' + txt(40, y, n, "mu b", 18) + txt(78, y, nm, "b", 20)
                 + txt(250, y, ds, "", 15.5) + "</g>")
        y += 46
    # stamp on the last row
    b.append(f'<g transform="translate(724 {y-46-4}) rotate(-6)"><g class="f" {D(1500)}>'
             f'<rect x="-70" y="-22" width="140" height="42" rx="3" fill="none" stroke="{RED}" stroke-width="3"/>'
             f'<text x="0" y="8" text-anchor="middle" font-size="20" class="b rd" style="letter-spacing:.08em">LAST</text></g></g>')
    return lib.svg("osTokens", W, H, "".join(b), css("osTokens"),
                   "Index card: CAG cache, scripts, Qdrant and Jev / Laya routing come before the model, which only gets what is left.")


# ------------------------------------------------------------------ projects (catalog cards)
def projects() -> str:
    s = lib.summary(lib.data())
    rl = s["repo_lang"]
    items = [("poc-grpc", "gRPC proof of concept. Client and server share one Protobuf contract."),
             ("grpc-common", "The canonical Protobuf contract library. One schema for every team and stack."),
             ("grpc-server", "Server side of the gRPC POC, built on the shared contract."),
             ("Demo-SpringSecurity6-JWT", "Stateless auth with Spring Security 6 and JWT."),
             ("spring-and-vue", "Spring Boot API with a Vue front end."),
             ("Capstone-Project", "AWS Academy Cloud Architecting capstone.")]
    cw, ch, g, m = 264, 176, 14, 20
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
        for k, line in enumerate(textwrap.wrap(ds, 29)[:4]):
            yy = y + 66 + k * 22
            g_.append(txt(x + 16, yy, line, "", 12.5))
        for k in range(4):
            yy = y + 66 + k * 22 + 6
            g_.append(f'<line x1="{x}" y1="{yy}" x2="{x+cw}" y2="{yy}" stroke="{RULE}" stroke-width="1"/>')
        if lang:
            g_.append(txt(x + 16, y + ch - 40, lang, "mu b", 12))
        g_.append(f'<circle cx="{x+cw/2}" cy="{y+ch-18}" r="6" fill="#2a2722"/>')
        b.append(f'<g class="f" {D(d)}>' + "".join(g_) + "</g>")
    return lib.svg("osProj", W, H, "".join(b), css("osProj"),
                   "Library catalog cards: poc-grpc, grpc-common, grpc-server, Demo-SpringSecurity6-JWT, spring-and-vue, Capstone-Project.")


# ------------------------------------------------------------------ stats (receipt totals)
def stats() -> str:
    s = lib.summary(lib.data())
    H = 400
    b = [f'<rect width="{W}" height="{H}" rx="6" fill="{PAPER}" stroke="{RULE}"/>']
    b.append(f'<g class="w" {D(0)}>' + txt(40, 72, "Totals", "sf it", 46) + "</g>")
    rows = [("CONTRIBUTIONS", s["contributions"]), ("COMMITS", s["commits"]), ("ACTIVE DAYS", s["active_days"]),
            ("BUSIEST DAY", s["busiest"]), ("PUBLIC REPOS", s["repos"]), ("FOLLOWERS", s["followers"])]
    y = 126
    xl, xr = 40, 410
    for i, (l, v) in enumerate(rows):
        b.append(row(xl, xr, y, l, str(v), 17, 150 + i * 110, rcls="b"))
        y += 40
    b.append(f'<line class="w" {D(900)} x1="{xl}" y1="{y-18}" x2="{xr}" y2="{y-18}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<line class="w" {D(900)} x1="{xl}" y1="{y-13}" x2="{xr}" y2="{y-13}" stroke="{INK}" stroke-width="1"/>')
    b.append(f'<g class="w" {D(1000)}>' + txt(xl, y + 8, "LAST 53 WEEKS", "mu", 13) + "</g>")
    # right column: big figure + language bars
    b.append(f'<g class="w" {D(300)}>' + txt(470, 190, str(s["contributions"]), "sf", 150) + "</g>")
    b.append(f'<g class="w" {D(450)}>' + txt(472, 222, "contributions on GitHub", "mu", 14) + "</g>")
    yy = 268
    for i, (n, sh, _c) in enumerate(s["stack"][:5]):
        d = 700 + i * 110
        bw = max(4, 200 * sh / s["stack"][0][1])
        b.append(f'<g class="w" {D(d)}>' + txt(470, yy, n, "b", 13)
                 + f'<rect x="570" y="{yy-11}" width="{bw:.0f}" height="12" fill="{INK}"/>'
                 + txt(830, yy, f"{sh*100:.0f}%", "mu", 13, "end") + "</g>")
        yy += 24
    return lib.svg("osStats", W, H, "".join(b), css("osStats"),
                   f"Totals: {s['contributions']} contributions, {s['commits']} commits, {s['active_days']} active days, {s['repos']} public repos.")


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
    b.append(f'<g class="w" {D(0)}>' + txt(46, 44, "RAFAEL PEREIRA", "b", 15) + txt(814, 44, f"{s['contributions']} CONTRIBUTIONS", "b", 15, "end") + "</g>")
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
    b.append(txt(46, 282, "ONE HOLE = A DAY WITH CONTRIBUTIONS · A BIGGER HOLE = MORE", "mu", 12))
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
    for n, f in [("hero", hero), ("focus", focus), ("tokens", tokens), ("projects", projects),
                 ("stats", stats), ("punch", punch), ("record", record)]:
        write(out_dir, f"{n}.svg", f())


if __name__ == "__main__":
    build(lib.ROOT / "assets" / "oldschool")
    print("ok")
