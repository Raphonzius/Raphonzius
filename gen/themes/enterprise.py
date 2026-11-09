"""enterprise: an architecture-review one-pager. Apple-like restraint.

Inter + Inter Tight, one accent, hairlines, light and dark pair for every card.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "gen"))
import lib  # noqa: E402
from lib import esc  # noqa: E402

W = 860
PAL = {
    "light": dict(bg="#fbfbfd", surf="#ffffff", text="#1d1d1f", sub="#6e6e73", line="#d2d2d7",
                  acc="#0071e3", track="#ececf0", lvl=[0.28, 0.5, 0.75, 1.0], empty="#ebebf0"),
    "dark": dict(bg="#161618", surf="#1c1c1e", text="#f5f5f7", sub="#a1a1a6", line="#3a3a3d",
                 acc="#2997ff", track="#2c2c2e", lvl=[0.3, 0.52, 0.76, 1.0], empty="#2a2a2d"),
}


def css(sid: str, p: dict, fonts: bool = True) -> str:
    f = "".join([lib.font("Inter", 400), lib.font("Inter", 600), lib.font("Inter Tight", 600)]) if fonts else ""
    s = f"#{sid}"
    return f + (
        f"{s} text{{font-family:'Inter',sans-serif;font-weight:400;fill:{p['text']};letter-spacing:0}}"
        f"{s} .d{{font-family:'Inter Tight','Inter',sans-serif;font-weight:600;letter-spacing:-0.035em}}"
        f"{s} .b{{font-weight:600}}"
        f"{s} .s{{fill:{p['sub']}}}"
        f"{s} .a{{fill:{p['acc']}}}"
        f"{s} .cap{{font-size:11px;font-weight:600;letter-spacing:.06em;fill:{p['sub']}}}"
        f"{s} .card{{fill:{p['bg']};stroke:{p['line']};stroke-width:1}}"
        f"{s} .box{{fill:{p['surf']};stroke:{p['line']};stroke-width:1}}"
        f"{s} .hl{{stroke:{p['line']};stroke-width:1;fill:none}}"
        f"{s} .in{{opacity:0;animation:{sid}-rise 600ms {lib.EASE_OUT} both}}"
        f"@keyframes {sid}-rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}"
        f"@keyframes {sid}-fade{{from{{opacity:0}}to{{opacity:1}}}}"
        f"@media (prefers-reduced-motion:reduce){{{s} .in{{animation:{sid}-fade 200ms linear both;animation-delay:0ms!important}}"
        f"{s} .pk{{display:none}}}}"
    )


def T(x, y, txt, size, cls="", anchor="start", delay=None, extra=""):
    st = f' style="animation-delay:{delay}ms"' if delay is not None else ""
    c = (cls + (" in" if delay is not None else "")).strip()
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" class="{c}"{st} {extra}>{esc(txt)}</text>')


def G(inner, delay):
    return f'<g class="in" style="animation-delay:{delay}ms">{inner}</g>'


def card(h):
    return f'<rect class="card" x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="20"/>'


def marker(sid, name, color):
    return (f'<marker id="{sid}-{name}" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" orient="auto" '
            f'markerUnits="userSpaceOnUse"><path d="M1.5,1.5 L7.5,4.5 L1.5,7.5" fill="none" stroke="{color}" '
            f'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></marker>')


# ------------------------------------------------------------------ hero
def hero(mode):
    p = PAL[mode]; sid = f"ent-hero-{mode}"; H = 480
    d = lib.data(); av = d["avatar"]
    b = card(H)
    b += (f'<g class="in" style="animation-delay:0ms"><circle cx="80" cy="76" r="33" fill="{p["surf"]}" stroke="{p["line"]}"/>'
          f'<image href="{av}" x="48" y="44" width="64" height="64" clip-path="url(#{sid}-av)" preserveAspectRatio="xMidYMid slice"/></g>')
    b += T(812, 72, "S\u00e3o Paulo, Brazil", 14, "s", "end", 60)
    b += T(812, 92, "@Raphonzius", 14, "s", "end", 100)
    b += T(46, 196, "Rafael Pereira", 76, "d", delay=80)
    b += T(48, 236, "Software Engineer \u00b7 Getnet \u00b7 Open Finance", 22, "b", delay=140)
    b += T(48, 270, "If it can be deterministic, it should not be inference.", 18, "s", delay=200)
    b += T(48, 302, "Event-Driven Architecture enthusiast \u00b7 gRPC user \u00b7 Java enthusiast \u00b7 Rust for high performance",
           14.5, "s", delay=250)
    b += '<line class="hl" x1="48" y1="336" x2="812" y2="336"/>'
    cols = [
        ("2", " days", "Java 21 + Spring Boot 4.1", "vs 2 sprints, other squads"),
        ("9", " squads", "on the AI agent harness", "I maintain as AI Champion"),
        ("45", "%", "of execution subtasks sent to", "the cheapest mode, 11 repos"),
        ("$37k", " /yr", "AWS saved by rightsizing", "to arm64 at Samsung SDS"),
    ]
    for i, (n, u, l1, l2) in enumerate(cols):
        x = 48 + i * 214; dl = 320 + i * 60
        inner = (f'<text x="{x - 2}" y="398" font-size="52" class="d">{esc(n)}<tspan font-size="22" class="s" '
                 f'style="letter-spacing:-0.01em;font-family:Inter;font-weight:400"> {esc(u.strip())}</tspan></text>'
                 f'<text x="{x}" y="430" font-size="13" class="s">{esc(l1)}</text>'
                 f'<text x="{x}" y="448" font-size="13" class="s">{esc(l2)}</text>')
        b += G(inner, dl)
    defs = f'<clipPath id="{sid}-av"><circle cx="80" cy="76" r="32"/></clipPath>'
    return sid, lib.svg(sid, W, H, b, css(sid, p), "Rafael Pereira. Software Engineer at Getnet, Open Finance. 2 days versus 2 sprints migration, 9 squads, 45% of subtasks to the cheapest mode, USD 37k per year saved.", defs)


# ------------------------------------------------------------------ event flow
def flow(mode):
    p = PAL[mode]; sid = f"ent-flow-{mode}"; H = 440; cy = 232
    ln, ac = p["line"], p["acc"]
    defs = marker(sid, "ah", p["sub"]) + marker(sid, "ac", ac)
    b = card(H)
    b += T(48, 64, "Event-Driven Architecture", 30, "d", delay=0)
    b += T(48, 92, "Transactional outbox, idempotent consumers, DLQ with retry. RabbitMQ, Azure Service Bus, Azure Event Hubs.",
           14.5, "s", delay=50)

    def zone(x, y, w, h, label, dl):
        return G(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="{ln}" stroke-dasharray="3 4"/>'
                 f'<text x="{x + 14}" y="{y + 20}" class="cap">{esc(label.upper())}</text>', dl)

    def bx(x, y, w, h, t1, t2, dl, stroke=None):
        s = f' style="stroke:{stroke}"' if stroke else ""
        return G(f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"{s}/>'
                 f'<text x="{x + 14}" y="{y + h / 2 - 2}" font-size="14.5" class="b">{esc(t1)}</text>'
                 f'<text x="{x + 14}" y="{y + h / 2 + 15}" font-size="12" class="s">{esc(t2)}</text>', dl)

    b += zone(36, 170, 344, 106, "Producer service", 120)
    b += zone(624, 132, 200, 186, "Consumers", 120)
    # connectors (static), arrowheads in secondary
    def ln_(d, m="ah", col=None, dash=""):
        c = col or p["sub"]
        return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.2" marker-end="url(#{sid}-{m})"{dash}/>'
    conn = (ln_(f"M188,{cy} H226") + ln_(f"M368,{cy} H406") + ln_(f"M548,{cy} H590 V274 H638") +
            f'<path d="M590,{cy} V190 H638" fill="none" stroke="{p["sub"]}" stroke-width="1.2" marker-end="url(#{sid}-ah)"/>' +
            ln_("M726,300 V372 H550", "ah") + ln_("M478,342 V264", "ac", ac))
    b += G(conn, 260)
    b += bx(48, cy - 30, 140, 60, "API", "Open Finance", 200)
    b += bx(228, cy - 30, 140, 60, "Outbox", "same DB transaction", 250)
    b += bx(408, cy - 30, 140, 60, "Broker", "pub/sub", 300)
    b += bx(640, 164, 172, 52, "Idempotent consumer", "Consumer A", 350)
    b += bx(640, 248, 172, 52, "Idempotent consumer", "Consumer B", 400)
    b += bx(408, 342, 140, 60, "DLQ", "dead-letter queue", 450, stroke=ac)
    b += G(T(640, 366, "on failure", 12, "s", "middle") + T(490, 306, "retry", 12, "a b"), 500)
    path = f"M118,{cy} H590 V274 H726 V372 H478 V{cy} H590 V190 H726"
    b += (f'<g class="pk"><circle r="5.5" fill="{ac}" opacity="0"><animateMotion dur="14s" begin="1.8s" repeatCount="indefinite" '
          f'path="{path}" calcMode="linear"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.02;0.97;1" '
          f'dur="14s" begin="1.8s" repeatCount="indefinite"/></circle></g>')
    return sid, lib.svg(sid, W, H, b, css(sid, p), "Event flow: API writes to the outbox, the outbox publishes to the broker, idempotent consumers process, failures go to the DLQ and retry back to the broker.", defs)


# ------------------------------------------------------------------ token pipeline
def tokens(mode):
    p = PAL[mode]; sid = f"ent-tok-{mode}"; H = 520; ac = p["acc"]
    b = card(H)
    b += T(48, 64, "Deterministic first, inference last.", 30, "d", delay=0)
    b += T(48, 92, "A request walks down the stack and reaches the model only if nothing above could answer it.", 14.5, "s", delay=50)
    rows = [
        ("CAG cache", "Cache-augmented generation: known context is loaded once and reused."),
        ("Scripts", "Plain code for anything that has a rule: parse, validate, transform."),
        ("Qdrant", "Vector search returns only the context that matters."),
        ("Jev / Laya", "Routing sends each LLM task to the model that fits it."),
        ("Model", "Inference, only for what is left."),
    ]
    y0, rh, gap = 128, 58, 6
    cyl = [y0 + i * (rh + gap) + rh / 2 for i in range(5)]
    b += f'<line x1="76" y1="{cyl[0]}" x2="76" y2="{cyl[-1]}" stroke="{p["line"]}" stroke-width="1.2"/>'
    for i, (n, dsc) in enumerate(rows):
        y = y0 + i * (rh + gap); last = i == 4
        stroke = f' style="stroke:{ac};stroke-width:1.5"' if last else ""
        dot = (f'<circle cx="76" cy="{cyl[i]}" r="5" fill="{ac}" stroke="{ac}"/>' if last
               else f'<circle cx="76" cy="{cyl[i]}" r="5" fill="{p["surf"]}" stroke="{p["sub"]}" stroke-width="1.2"/>')
        b += G(f'<rect class="box" x="96" y="{y}" width="716" height="{rh}" rx="12"{stroke}/>'
               f'{dot}<text x="116" y="{cyl[i] + 6}" font-size="17" class="b">{esc(n)}</text>'
               f'<text x="290" y="{cyl[i] + 5}" font-size="14.5" class="s">{esc(dsc)}</text>', 120 + i * 60)
    kp = "0;0;0.25;0.25;0.5;0.5;0.75;0.75;1;1"; kt = "0;0.08;0.2;0.28;0.4;0.48;0.6;0.68;0.8;1"
    b += (f'<g class="pk"><circle r="5" fill="{ac}" opacity="0"><animateMotion dur="10s" begin="1.6s" repeatCount="indefinite" '
          f'path="M76,{cyl[0]} V{cyl[-1]}" calcMode="linear" keyPoints="{kp}" keyTimes="{kt}"/>'
          f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.02;0.98;1" dur="10s" begin="1.6s" repeatCount="indefinite"/></circle></g>')
    b += '<line class="hl" x1="48" y1="460" x2="812" y2="460"/>'
    b += T(48, 492, "cloud-orchestrator, Oct 2026: 45% of execution subtasks went to the cheapest mode, across 11 repos.", 14.5, "s", delay=520)
    return sid, lib.svg(sid, W, H, b, css(sid, p), "Deterministic first, inference last: CAG cache, scripts, Qdrant, Jev and Laya routing, then the model.")


# ------------------------------------------------------------------ projects
def projects(mode):
    p = PAL[mode]; sid = f"ent-proj-{mode}"
    rows = [
        ("poc-grpc", "gRPC proof of concept on a shared Protobuf contract", "Java \u00b7 gRPC"),
        ("grpc-common", "Canonical Protobuf contract library", "Java \u00b7 Protobuf"),
        ("grpc-server", "Server side of the gRPC POC", "gRPC"),
        ("Demo-SpringSecurity6-JWT", "Stateless auth with Spring Security 6 and JWT", "Java \u00b7 JWT"),
        ("spring-and-vue", "Spring Boot API with a Vue front end", "Java \u00b7 Vue"),
        ("Capstone-Project", "AWS Academy Cloud Architecting capstone", "AWS"),
    ]
    top = 140; rh = 52; H = top + rh * len(rows) + 32
    b = card(H)
    b += T(48, 64, "Featured projects", 30, "d", delay=0)
    b += T(812, 62, "github.com/Raphonzius", 14, "s", "end", 50)
    b += G(f'<text x="48" y="116" class="cap">REPOSITORY</text><text x="300" y="116" class="cap">WHAT IT IS</text>'
           f'<text x="700" y="116" class="cap">STACK</text><line class="hl" x1="48" y1="{top - 8}" x2="812" y2="{top - 8}"/>', 100)
    for i, (n, dsc, st) in enumerate(rows):
        y = top - 8 + i * rh
        b += G(f'<text x="48" y="{y + 32}" font-size="15.5" class="b">{esc(n)}</text>'
               f'<text x="300" y="{y + 32}" font-size="14.5" class="s">{esc(dsc)}</text>'
               f'<text x="700" y="{y + 32}" font-size="14.5">{esc(st)}</text>'
               + (f'<line class="hl" x1="48" y1="{y + rh}" x2="812" y2="{y + rh}"/>' if i < len(rows) - 1 else ""),
               160 + i * 50)
    return sid, lib.svg(sid, W, H, b, css(sid, p), "Featured projects: poc-grpc, grpc-common, grpc-server, Demo-SpringSecurity6-JWT, spring-and-vue, Capstone-Project.")


# ------------------------------------------------------------------ dashboard
def dash(mode):
    p = PAL[mode]; sid = f"ent-dash-{mode}"; H = 582; ac = p["acc"]
    s = lib.summary(lib.data())
    b = card(H)
    b += T(48, 52, "Activity", 17, "b", delay=0) + T(812, 52, "Last 12 months, live from GitHub", 14, "s", "end", 30)
    stats = [(s["contributions"], "contributions"), (s["commits"], "commits"),
             (s["active_days"], "active days"), (s["busiest"], "most in one day")]
    for i, (n, l) in enumerate(stats):
        x = 48 + i * 214
        b += G(f'<text x="{x - 2}" y="112" font-size="48" class="d">{n}</text><text x="{x}" y="136" font-size="13.5" class="s">{l}</text>', 80 + i * 55)
    b += '<line class="hl" x1="48" y1="164" x2="812" y2="164"/>'
    b += T(48, 198, "Language stack", 15, "b", delay=300) + T(620, 198, "Profile", 15, "b", delay=300)
    for i, (n, share, _c) in enumerate(s["stack"][:5]):
        y = 232 + i * 30
        wfill = max(3, round(340 * share, 1))
        b += G(f'<text x="48" y="{y + 5}" font-size="14.5">{esc(n)}</text>'
               f'<rect x="170" y="{y - 3}" width="340" height="6" rx="3" fill="{p["track"]}"/>'
               f'<rect x="170" y="{y - 3}" width="{wfill}" height="6" rx="3" fill="{ac if i == 0 else p["sub"]}"/>'
               f'<text x="524" y="{y + 5}" font-size="13.5" class="s">{round(share * 100)}%</text>', 340 + i * 50)
    b += G(f'<text x="618" y="256" font-size="34" class="d">{s["repos"]}</text><text x="620" y="278" font-size="13.5" class="s">public repositories</text>'
           f'<text x="618" y="324" font-size="34" class="d">{s["followers"]}</text><text x="620" y="346" font-size="13.5" class="s">followers</text>', 400)
    b += '<line class="hl" x1="48" y1="376" x2="812" y2="376"/>'
    b += T(48, 410, "Contribution calendar", 15, "b", delay=560)
    mx = max(1, s["busiest"])
    cal = ""
    for ci, wk in enumerate(s["weeks"]):
        cells = ""
        for di, dd in enumerate(wk["contributionDays"]):
            c = dd["contributionCount"]
            if c == 0:
                fill, op = p["empty"], 1
            else:
                lv = min(3, int((c / mx) * 4 - 1e-9))
                fill, op = ac, p["lvl"][lv]
            cells += f'<rect x="{48 + ci * 14}" y="{428 + di * 14}" width="11" height="11" rx="2.5" fill="{fill}" opacity="{op}"/>'
        cal += f'<g class="in" style="animation-delay:{620 + ci * 11}ms">{cells}</g>'
    b += cal
    lx = 812 - 34
    leg = f'<text x="{lx - 5 * 14 - 8}" y="549" font-size="12" class="s" text-anchor="end">Less</text>'
    for k in range(5):
        fill, op = (p["empty"], 1) if k == 0 else (ac, p["lvl"][k - 1])
        leg += f'<rect x="{lx - 5 * 14 + k * 14 - 3}" y="539" width="11" height="11" rx="2.5" fill="{fill}" opacity="{op}"/>'
    leg += f'<text x="{lx + 2}" y="549" font-size="12" class="s">More</text>'
    b += G(leg, 1200)
    return sid, lib.svg(sid, W, H, b, css(sid, p), "GitHub activity: contributions, commits, active days, language stack and contribution calendar.")


CARDS = {"hero": hero, "event-flow": flow, "token-pipeline": tokens, "projects": projects, "stats": dash}


def build(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, fn in CARDS.items():
        for mode in ("light", "dark"):
            _sid, svg = fn(mode)
            (out_dir / f"{name}-{mode}.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    build(ROOT / "assets" / "enterprise")
