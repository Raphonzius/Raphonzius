"""dystopia: a city-wide message control authority where inference is rationed.
Rafael is an operator unit. Industrial terminal, one acid accent, one dim secondary."""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import lib  # noqa: E402
from lib import esc  # noqa: E402

W = 860
BG = "#07080a"
FG = "#e8e6df"
ACC = "#d7ff3a"
DIM = "#8b9086"
LINE = "#23272c"
D = "'BSD', 'Oswald', 'Arial Narrow', Impact, sans-serif"
M = "'JBM', 'Consolas', monospace"

_fonts = None


def fonts() -> str:
    global _fonts
    if _fonts is None:
        _fonts = (lib.font("Big Shoulders Display", 900, alias="BSD") + lib.font("JetBrains Mono", 400, alias="JBM"))
    return _fonts


BASE_CSS = """
#{s} text{{font-family:{M};fill:{FG}}}
#{s} .d{{font-family:{D};font-weight:900;letter-spacing:-0.02em}}
#{s} .m{{font-family:{M};font-weight:400}}
#{s} .dim{{fill:{DIM}}}
#{s} .acc{{fill:{ACC}}}
#{s} .in{{animation:{s}-rise 700ms {EO} both}}
@keyframes {s}-rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion: reduce){{
 #{s} .in{{animation:{s}-fade 200ms linear both;animation-delay:0ms!important}}
 #{s} .pk,#{s} .sweep,#{s} .bar{{display:none}}
}}
@keyframes {s}-fade{{from{{opacity:0}}to{{opacity:1}}}}
"""


def css(s: str, extra: str = "") -> str:
    return fonts() + BASE_CSS.format(s=s, M=M, D=D, FG=FG, DIM=DIM, ACC=ACC, EO=lib.EASE_OUT) + extra


def frame(h: int) -> str:
    """Card ground: near-black field, hairline border, static scanlines at restraint."""
    return (f'<rect width="{W}" height="{h}" rx="6" fill="{BG}"/>'
            f'<rect width="{W}" height="{h}" rx="6" fill="url(#scan)"/>'
            f'<rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="6" fill="none" stroke="{LINE}"/>')


def defs(extra: str = "") -> str:
    return ('<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">'
            '<rect width="4" height="1" fill="#fff" fill-opacity=".022"/></pattern>' + extra)


def delay(i: int, base: int = 0, step: int = 60) -> str:
    return f'style="animation-delay:{base + i * step}ms"'


def heading(sid: str, text: str, sub: str, y: int = 100) -> str:
    return (f'<text class="d in" x="36" y="{y}" font-size="96" {delay(0)}>{esc(text)}</text>'
            f'<text class="m dim in" x="38" y="{y+30}" font-size="14" {delay(1)}>{esc(sub)}</text>')


# ------------------------------------------------------------------ hero
def hero() -> str:
    sid = "dys-hero"
    H = 600
    av = lib.data()["avatar"]
    rows = [("EVENT-DRIVEN ARCHITECTURE", "ENTHUSIAST"), ("gRPC", "USER"), ("JAVA", "ENTHUSIAST"),
            ("RUST", "FOR HIGH PERFORMANCE"), ("FOCUS", "AI TOKEN MINIMIZING")]
    total = 58
    body = frame(H)
    body += (f'<text class="m dim in" x="36" y="46" font-size="14" {delay(0)}>OPERATOR UNIT  /  @Raphonzius  /  '
             f'SOFTWARE ENGINEER, GETNET  /  S\u00c3O PAULO, BR</text>')
    body += f'<text class="d in" x="30" y="268" font-size="262" {delay(1,0,80)}>RAFAEL</text>'
    body += f'<text class="d in" x="35" y="378" font-size="104" {delay(2,0,80)}>RODRIGUES PEREIRA</text>'
    body += f'<rect class="in" x="36" y="404" width="788" height="1" fill="{LINE}" {delay(3,0,80)}/>'
    y = 440
    for i, (k, v) in enumerate(rows):
        dots = "." * (total - len(k) - len(v) - 2)
        body += (f'<text class="m in" x="36" y="{y}" font-size="16" {delay(4+i,0,70)}>'
                 f'<tspan class="acc">+</tspan> {esc(k)} <tspan class="dim">{dots}</tspan> {esc(v)}</text>')
        y += 26
    body += (f'<text class="m acc in" x="36" y="{y+22}" font-size="16" {delay(10,0,70)}>&gt; IF IT CAN BE DETERMINISTIC, IT SHOULD NOT BE INFERENCE.</text>')
    cx = 36 + 9.6 * 58 + 6
    body += f'<rect x="{cx:.1f}" y="{y+8}" width="10" height="18" fill="{ACC}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite" begin="2s"/></rect>'
    # avatar: greyscale unit portrait
    body += (f'<g class="in" {delay(6,0,70)}><clipPath id="avc"><rect x="676" y="426" width="148" height="148"/></clipPath>'
             f'<image href="{av}" x="676" y="426" width="148" height="148" preserveAspectRatio="xMidYMid slice" clip-path="url(#avc)" filter="url(#gray)"/>'
             f'<rect x="676.5" y="426.5" width="147" height="147" fill="none" stroke="{ACC}" stroke-opacity=".9"/></g>')
    # one slow sweep on entrance
    body += (f'<g class="sweep" style="animation:{sid}-sw 1500ms {lib.EASE_IN_OUT} 150ms both" clip-path="url(#sweepclip)">'
             f'<rect x="0" y="-60" width="{W}" height="60" fill="url(#sg)"/><rect x="0" y="-1" width="{W}" height="2" fill="{ACC}"/></g>')
    d = defs(f'<clipPath id="sweepclip"><rect width="{W}" height="{H}" rx="6"/></clipPath>'
             f'<linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACC}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{ACC}" stop-opacity=".14"/></linearGradient>'
             '<filter id="gray"><feColorMatrix type="saturate" values="0"/></filter>')
    extra = (f"@keyframes {sid}-sw{{0%{{transform:translateY(0);opacity:0}}8%{{opacity:1}}92%{{opacity:1}}"
             f"100%{{transform:translateY({H+60}px);opacity:0}}}}")
    return lib.svg(sid, W, H, body, css(sid, extra), "Rafael Rodrigues Pereira, operator terminal readout", d)


# ------------------------------------------------------------------ event bus
def _path_len(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def _d(pts):
    return "M" + " L".join(f"{x},{y}" for x, y in pts)


def event_flow() -> str:
    sid = "dys-bus"
    H = 560
    API, OUT, BRK = (110, 260), (290, 260), (470, 260)
    FORK = (520, 260)
    C1, C2 = (660, 190), (660, 330)
    DLQ = (470, 450)
    main = [API, OUT, BRK, FORK, (590, 190), C1]
    lower = [API, OUT, BRK, FORK, (590, 330), C2]
    dlq = [BRK, DLQ]
    retry = [DLQ, (540, 450), C2]
    poison = [API, OUT, BRK, DLQ, (540, 450), C2]

    body = frame(H)
    body += heading(sid, "EVENT BUS", "Open Finance APIs under Banco Central rules. P95/P99 and TPS are the contract.")
    ln = f'fill="none" stroke-linejoin="round" stroke-linecap="round"'
    body += f'<g class="in" {delay(2,0,70)}>'
    body += f'<path d="{_d(main)}" {ln} stroke="{FG}" stroke-width="6"/>'
    body += f'<path d="{_d(lower)}" {ln} stroke="{FG}" stroke-width="6"/>'
    body += f'<path d="{_d(dlq)}" {ln} stroke="{DIM}" stroke-width="6" stroke-dasharray="2 12"/>'
    body += f'<path d="{_d(retry)}" {ln} stroke="{ACC}" stroke-width="3" stroke-dasharray="10 8"/>'
    body += '</g>'
    # stations
    def st(p, r=10, fill=BG, stroke=FG):
        return f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="5"/>'
    body += f'<g class="in" {delay(4,0,70)}>' + st(API) + st(OUT) + st(BRK, 15) + st(C1) + st(C2)
    body += (f'<rect x="{DLQ[0]-13}" y="{DLQ[1]-13}" width="26" height="26" fill="{BG}" stroke="{ACC}" stroke-width="4" stroke-dasharray="6 4"/></g>')
    # labels
    def lab(x, name, lines, anchor="middle", y=222, delay_i=5):
        t = f'<g class="in" {delay(delay_i,0,70)}><text class="d" x="{x}" y="{y}" font-size="34" text-anchor="{anchor}">{esc(name)}</text>'
        for i, l in enumerate(lines):
            t += f'<text class="m dim" x="{x}" y="{y+22+i*16}" font-size="12" text-anchor="{anchor}">{esc(l)}</text>'
        return t + '</g>'
    body += lab(API[0], "API", ["Open Finance", "request in"], y=170, delay_i=5)
    body += lab(OUT[0], "OUTBOX", ["written in the", "same transaction"], y=170, delay_i=6)
    body += lab(BRK[0], "BROKER", ["RabbitMQ, Service Bus,", "Event Hubs"], y=170, delay_i=7)
    body += lab(C1[0] + 22, "CONSUMER A", ["idempotent:", "duplicate = no-op"], anchor="start", y=165, delay_i=8)
    body += lab(C2[0] + 22, "CONSUMER B", ["idempotent:", "duplicate = no-op"], anchor="start", y=305, delay_i=9)
    body += lab(DLQ[0] - 30, "QUARANTINE", ["DLQ. poison message held", "until it is retried"], anchor="end", y=445, delay_i=10)
    body += f'<text class="m acc in" x="520" y="474" font-size="12" {delay(11,0,70)}>RETRY</text>'
    # packets
    def pk(pts, begin, dur, f, size=10, hollow=False, extra_kp=None):
        if extra_kp:
            kp, kt = extra_kp
        else:
            kp, kt = f"0;1;1", f"0;{f:.3f};1"
        fill = f'fill="{BG}" stroke="{FG}" stroke-width="2.5"' if hollow else f'fill="{ACC}"'
        s = size / 2
        op_kt = f"0;{kt.split(';')[-2]};{float(kt.split(';')[-2])+0.03:.3f};1"
        return (f'<rect class="pk" x="{-s}" y="{-s}" width="{size}" height="{size}" {fill} opacity="0">'
                f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" calcMode="linear" '
                f'keyPoints="{kp}" keyTimes="{kt}" path="{_d(pts)}"/>'
                f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="{op_kt}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></rect>')
    DUR = 12
    sp = 100.0
    fa, fb = _path_len(main) / sp / DUR, _path_len(lower) / sp / DUR
    body += '<g>'
    for b in (0, 6):
        body += pk(main, b, DUR, fa)
    for b in (3, 9):
        body += pk(lower, b, DUR, fb)
    # poison: travel, hold in quarantine, retry, arrive
    L = _path_len(poison)
    p_hold = _path_len([API, OUT, BRK, DLQ]) / L
    t1 = _path_len([API, OUT, BRK, DLQ]) / sp / DUR
    t2 = t1 + 0.20
    t3 = t2 + (L * (1 - p_hold)) / sp / DUR
    body += pk(poison, 1.5, DUR, 0, size=14, hollow=True,
               extra_kp=(f"0;{p_hold:.3f};{p_hold:.3f};1;1", f"0;{t1:.3f};{t2:.3f};{t3:.3f};1"))
    body += '</g>'
    # legend
    body += (f'<g class="in" {delay(12,0,70)}><rect x="38" y="524" width="10" height="10" fill="{ACC}"/>'
             f'<text class="m dim" x="58" y="533" font-size="12">message</text>'
             f'<rect x="150" y="522" width="14" height="14" fill="{BG}" stroke="{FG}" stroke-width="2.5"/>'
             f'<text class="m dim" x="174" y="533" font-size="12">poison message: diverted to quarantine, re-admitted by retry</text></g>')
    return lib.svg(sid, W, H, body, css(sid), "Event bus as a transit map: API, outbox, broker, idempotent consumers, DLQ quarantine and retry", defs())


# ------------------------------------------------------------------ rationing
def rationing() -> str:
    sid = "dys-ration"
    H = 470
    RY = 280
    gates = [(150, "CAG CACHE", ["answer cached", "in context"]),
             (300, "SCRIPTS", ["if code can answer,", "code answers"]),
             (450, "QDRANT", ["vector lookup", "before generating"]),
             (600, "JEV / LAYA", ["routes each task", "to cheapest mode"])]
    MX = 700
    body = frame(H)
    body += heading(sid, "INFERENCE RATIONING", "Every request passes the checkpoints in order. Only what survives reaches the model.")
    body += f'<rect class="in" x="40" y="{RY-1}" width="{MX-40}" height="2" fill="{DIM}" {delay(2,0,70)}/>'
    body += f'<text class="m dim in" x="38" y="{RY-14}" font-size="12" {delay(2,0,70)}>REQUEST</text>'
    for i, (gx, name, ls) in enumerate(gates):
        g = f'<g class="in" {delay(3+i,0,70)}>'
        g += f'<rect x="{gx-5}" y="{RY-70}" width="10" height="62" fill="{FG}"/><rect x="{gx-5}" y="{RY+8}" width="10" height="62" fill="{FG}"/>'
        g += f'<text class="d" x="{gx}" y="{RY-88}" font-size="30" text-anchor="middle">{esc(name)}</text>'
        for j, l in enumerate(ls):
            g += f'<text class="m dim" x="{gx}" y="{RY+98+j*16}" font-size="12" text-anchor="middle">{esc(l)}</text>'
        body += g + '</g>'
    body += (f'<g class="in" {delay(7,0,70)}><rect x="{MX}" y="{RY-60}" width="120" height="120" fill="{ACC}"/>'
             f'<text class="d" x="{MX+60}" y="{RY+14}" font-size="40" text-anchor="middle" style="fill:{BG}">MODEL</text>'
             f'<text class="m" x="{MX+60}" y="{RY+98}" font-size="12" text-anchor="middle" style="fill:{DIM}">only what survived</text></g>')
    body += f'<rect class="in" x="{MX-30}" y="{RY-1}" width="30" height="2" fill="{ACC}" {delay(7,0,70)}/>'
    # packets
    DUR, SP, X0 = 12, 110.0, 40
    pk = ""
    plan = [(0, 0), (1.6, 1), (3.2, 2), (4.8, 3), (6.4, None), (8.0, 0)]
    for b, k in plan:
        if k is None:
            pts = [(X0, RY), (MX + 60, RY)]
        else:
            gx = gates[k][0]
            pts = [(X0, RY), (gx - 18, RY), (gx - 18, RY + 56)]
        f = _path_len(pts) / SP / DUR
        fill = ACC
        pk += (f'<rect class="pk" x="-5" y="-5" width="10" height="10" fill="{fill}" opacity="0">'
               f'<animateMotion dur="{DUR}s" begin="{b}s" repeatCount="indefinite" calcMode="linear" keyPoints="0;1;1" keyTimes="0;{f:.3f};1" path="{_d(pts)}"/>'
               f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{f:.3f};{f+0.04:.3f};1" dur="{DUR}s" begin="{b}s" repeatCount="indefinite"/></rect>')
    body += pk
    body += (f'<text class="m dim in" x="38" y="{H-26}" font-size="12" {delay(8,0,70)}>A packet stops where the question already has an answer. If it can be deterministic, it is not inference.</text>')
    return lib.svg(sid, W, H, body, css(sid), "Inference rationing: requests pass CAG cache, scripts, Qdrant and Jev/Laya routing before the model", defs())


# ------------------------------------------------------------------ projects
def projects() -> str:
    sid = "dys-proj"
    items = [("poc-grpc", "gRPC proof of concept on one shared Protobuf contract.", "JAVA / gRPC"),
             ("grpc-common", "Canonical Protobuf contract library for every team.", "JAVA / PROTOBUF"),
             ("grpc-server", "Server side of the gRPC POC.", "gRPC"),
             ("Demo-SpringSecurity6-JWT", "Stateless auth with Spring Security 6 and JWT.", "JAVA / SPRING"),
             ("spring-and-vue", "Spring Boot API with a Vue front end.", "JAVA / VUE"),
             ("Capstone-Project", "AWS Academy Cloud Architecting capstone.", "AWS")]
    RH = 84
    top = 150
    H = top + RH * len(items) + 24
    body = frame(H)
    body += heading(sid, "DOSSIERS", "Public repositories filed under @Raphonzius.")
    extra = ""
    for i, (n, desc, tag) in enumerate(items):
        y = top + i * RH
        body += f'<g class="in" {delay(i,200,90)}>'
        body += f'<rect x="36" y="{y}" width="788" height="1" fill="{LINE}"/>'
        body += f'<text class="d dim" x="36" y="{y+60}" font-size="52">{i+1:02d}</text>'
        body += f'<text class="d" x="112" y="{y+44}" font-size="44">{esc(n.upper())}</text>'
        body += f'<text class="m dim" x="114" y="{y+66}" font-size="13">{esc(desc)}</text>'
        body += f'<text class="m acc" x="824" y="{y+30}" font-size="12" text-anchor="end">{esc(tag)}</text>'
        body += '</g>'
        # redaction bar slides off to the right, once
        body += (f'<rect class="bar" x="108" y="{y+8}" width="716" height="68" fill="{BG}" '
                 f'style="animation:{sid}-red 650ms {lib.EASE_IN_OUT} {500+i*110}ms both"/>')
    body += f'<rect x="36" y="{top+RH*len(items)}" width="788" height="1" fill="{LINE}"/>'
    extra = f"@keyframes {sid}-red{{from{{transform:translateX(0)}}to{{transform:translateX(760px)}}}}"
    return lib.svg(sid, W, H, body, css(sid, extra), "Featured projects: poc-grpc, grpc-common, grpc-server, Demo-SpringSecurity6-JWT, spring-and-vue, Capstone-Project", defs())


# ------------------------------------------------------------------ telemetry
def telemetry() -> str:
    sid = "dys-tele"
    d = lib.data()
    s = lib.summary(d)
    H = 600
    body = frame(H)
    body += heading(sid, "TELEMETRY", "Last 12 months, read from the GitHub API.")
    stats = [("CONTRIBUTIONS", s["contributions"]), ("COMMITS", s["commits"]),
             ("ACTIVE DAYS", s["active_days"]), ("BUSIEST DAY", s["busiest"])]
    cw = 197
    for i, (k, v) in enumerate(stats):
        x = 36 + i * cw
        body += (f'<g class="in" {delay(i+2,0,70)}><text class="d{" acc" if i == 0 else ""}" x="{x-3}" y="262" font-size="120">{v}</text>'
                 f'<text class="m dim" x="{x}" y="288" font-size="12">{k}</text></g>')
    # heat grid
    cell, gap = 11, 3
    gx0, gy0 = 59, 316
    mx = max(1, s["busiest"])
    def lvl(c):
        if c == 0:
            return "#14171b", 1
        r = c / mx
        return ACC, (.28 if r <= .25 else .5 if r <= .5 else .75 if r <= .75 else 1)
    step = 26
    for wi, w in enumerate(s["weeks"]):
        col = f'<g class="in" style="animation-delay:{600+wi*step//1}ms;animation-duration:400ms">'
        for di, day in enumerate(w["contributionDays"]):
            c, o = lvl(day["contributionCount"])
            col += f'<rect x="{gx0+wi*(cell+gap)}" y="{gy0+di*(cell+gap)}" width="{cell}" height="{cell}" fill="{c}" fill-opacity="{o}"/>'
        body += col + '</g>'
    gw = len(s["weeks"]) * (cell + gap)
    sweep_ms = 600 + len(s["weeks"]) * step
    body += (f'<rect class="sweep" x="{gx0-2}" y="{gy0-8}" width="2" height="{7*(cell+gap)+14}" fill="{ACC}" '
             f'style="animation:{sid}-scan {sweep_ms-600+400}ms linear 600ms both"/>')
    body += f'<text class="m dim in" x="{gx0}" y="{gy0+7*(cell+gap)+22}" font-size="12" {delay(9,0,70)}>{s["contributions"]} contributions across {s["active_days"]} active days. Brighter cell, more contributions.</text>'
    # stack
    sy = 490
    ab = {"JavaScript": "JS"}
    x = 36.0
    tw = 788.0
    n = len(s["stack"])
    tot = sum(sh for _, sh, _ in s["stack"])
    ops = [1, .7, .5, .32, .18, .12]
    body += f'<g class="in" {delay(10,0,70)}>'
    for i, (name, sh, _c) in enumerate(s["stack"]):
        wseg = max(6.0, tw * sh / tot - 3)
        fill = ACC if i == 0 else FG
        o = 1 if i == 0 else ops[i]
        body += f'<rect x="{x:.1f}" y="{sy}" width="{wseg:.1f}" height="34" fill="{fill}" fill-opacity="{o}"/>'
        lab = f'{ab.get(name, name).upper()} {round(sh*100)}%'
        if i == n - 1:
            body += f'<text class="m dim" x="{x+wseg:.1f}" y="{sy+54}" font-size="12" text-anchor="end">{esc(lab)}</text>'
        else:
            body += f'<text class="m dim" x="{x:.1f}" y="{sy+54}" font-size="12">{esc(lab)}</text>'
        x += wseg + 3
    body += '</g>'
    body += (f'<text class="m dim in" x="36" y="{H-24}" font-size="12" {delay(11,0,70)}>{s["repos"]} public repositories, {s["followers"]} followers. Language share by bytes, excluding markup.</text>')
    extra = f"@keyframes {sid}-scan{{0%{{transform:translateX(0);opacity:1}}95%{{opacity:1}}100%{{transform:translateX({gw}px);opacity:0}}}}"
    return lib.svg(sid, W, H, body, css(sid, extra), f"Telemetry: {s['contributions']} contributions, {s['commits']} commits, {s['active_days']} active days", defs())


# ------------------------------------------------------------------ tools
def tools() -> str:
    sid = "dys-tools"
    groups = [("PROGRAMMING", ["Java", "Spring", "Bash", "JavaScript", "Python"]),
              ("OS", ["Linux", "Ubuntu", "Red Hat", "Windows"]),
              ("UTILITIES", ["AWS", "Git", "Podman", "Jenkins", "Postman"])]
    top = 150
    RH = 110
    H = top + RH * len(groups) + 10
    body = frame(H)
    body += heading(sid, "TOOL REGISTRY", "Licensed for daily use.")
    for gi, (g, ts) in enumerate(groups):
        y = top + gi * RH
        body += f'<g class="in" {delay(gi,200,120)}><rect x="36" y="{y}" width="788" height="1" fill="{LINE}"/>'
        body += f'<text class="d" x="36" y="{y+36}" font-size="24" style="fill:{DIM}">{g}</text>'
        x = 36
        for t in ts:
            w = int(len(t) * 14 + 40)
            body += (f'<rect x="{x}" y="{y+50}" width="{w}" height="46" fill="none" stroke="{FG}" stroke-opacity=".55"/>'
                     f'<rect x="{x+10}" y="{y+69}" width="7" height="7" fill="{ACC}"/>'
                     f'<text class="d" x="{x+26}" y="{y+83}" font-size="26">{esc(t.upper())}</text>')
            x += w + 10
        body += '</g>'
    return lib.svg(sid, W, H, body, css(sid), "Daily tools: Java, Spring, Bash, JavaScript, Python, Linux, Ubuntu, Red Hat, Windows, AWS, Git, Podman, Jenkins, Postman", defs())


# ------------------------------------------------------------------ record
def record() -> str:
    sid = "dys-rec"
    cells = [("2 DAYS", ["Java 17 to 21 and Spring Boot 3.5.4 to 4.1.0,", "done with AI agents. Other squads took 2 sprints.", "Zero critical or high vulnerabilities, no new", "bug, inside SonarQube gates."]),
             ("45%", ["of execution subtasks went to Devin Lite, the", "cheapest mode, through the cloud-orchestrator", "plugin. Ran on 11 repos, Oct 2026."]),
             ("USD 37K", ["saved per year at Samsung SDS with AWS", "rightsizing and x86_64 to arm64, on instances", "20 to 32% faster."]),
             ("670K+", ["SMS and WhatsApp messages per month across", "4 countries. Spring Cloud Gateway, Eureka,", "OAuth, AWS SNS."])]
    top = 150
    RH = 190
    H = top + RH * 2 + 14
    body = frame(H)
    body += heading(sid, "RECORD", "Filed outcomes.")
    for i, (big, ls) in enumerate(cells):
        cx = 36 + (i % 2) * 400
        y = top + (i // 2) * RH
        body += f'<g class="in" {delay(i,200,120)}><rect x="{cx}" y="{y}" width="388" height="1" fill="{LINE}"/>'
        body += f'<text class="d{" acc" if i == 1 else ""}" x="{cx-2}" y="{y+82}" font-size="86">{esc(big)}</text>'
        for j, l in enumerate(ls):
            body += f'<text class="m dim" x="{cx}" y="{y+112+j*17}" font-size="12">{esc(l)}</text>'
        body += '</g>'
    return lib.svg(sid, W, H, body, css(sid), "Record: 2 days vs 2 sprints migration, 45% of subtasks to the cheapest mode, USD 37k per year saved, 670k+ messages per month", defs())


ALL = {"hero": hero, "event-flow": event_flow, "token-budget": rationing, "projects": projects,
       "telemetry": telemetry, "tools": tools, "record": record}


def build(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, fn in ALL.items():
        (out_dir / f"{name}.svg").write_text(fn(), encoding="utf-8")


if __name__ == "__main__":
    build(lib.ROOT / "assets" / "dystopia")
