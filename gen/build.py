"""Build the animated SVG sections of the profile README.

Technique (reverse-engineered from GitSkins): every section is a standalone SVG.
GitHub serves README images through its camo proxy, which strips scripts but keeps
inline CSS animations and SMIL. So all motion lives in <style> keyframes and
<animateMotion>, and every section respects prefers-reduced-motion.

Static sections (hero, event flow, token budget, projects) carry hand-written
content. Live sections (stats, stack, stream) read the GitHub API.

Usage:
    python gen/build.py static          # writes assets/*.svg
    python gen/build.py live  OUT_DIR   # needs GITHUB_TOKEN, writes stats/stack/stream
Stdlib only.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import urllib.request
from datetime import date
from html import escape
from pathlib import Path

USER = "Raphonzius"
W = 860

# Palette: deep navy glass, teal = flow, amber = Java, violet = AI, rose = DLQ.
BG0, BG1, BG2 = "#070b1a", "#0f1a33", "#0a1226"
TEAL, AMBER, VIOLET, ROSE, SKY = "#2dd4bf", "#f59e0b", "#a78bfa", "#fb7185", "#38bdf8"
INK, MUTED, LINE = "#e6edf3", "#8b9bb4", "#24324f"
SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code',Consolas,'Liberation Mono',monospace"

# Repos to feature. Experiments (agent-kit, explaining-ai, Jarvis, tsp-graph,
# my-llm-orchestration) are excluded on purpose.
FEATURED = [
    ("poc-grpc", "gRPC POC: one Protobuf contract shared by teams and stacks", ["gRPC", "Protobuf", "Java"]),
    ("grpc-common", "Canonical Protobuf contract library", ["Protobuf", "Java"]),
    ("grpc-server", "Server side of the gRPC POC", ["gRPC", "Java"]),
    ("Demo-SpringSecurity6-JWT", "Stateless auth with Spring Security 6 and JWT", ["Spring", "JWT"]),
    ("spring-and-vue", "Spring Boot API with a Vue front end", ["Spring", "Vue"]),
    ("Capstone-Project", "AWS Academy Cloud Architecting capstone", ["AWS"]),
]
EXCLUDED = {"agent-kit", "explaining-ai", "Jarvis", "tsp-graph", "my-llm-orchestration"}
LANG_COLORS = {"Java": AMBER, "Python": SKY, "Shell": TEAL, "Vue": "#42b883", "HTML": ROSE,
               "Scala": "#dc322f", "Jupyter Notebook": "#f37626", "Rust": "#dea584",
               "JavaScript": "#f1e05a", "Kotlin": VIOLET}


# ---------------------------------------------------------------- shared frame
def frame(sid: str, h: int, body: str, css: str = "", label: str = "") -> str:
    """Glass card: gradient base, drifting orbs, inner bordered panel."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{escape(label or sid)}">
<defs>
  <linearGradient id="{sid}-bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG0}"/><stop offset=".55" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/>
  </linearGradient>
  <radialGradient id="{sid}-o1"><stop offset="0" stop-color="{TEAL}" stop-opacity=".45"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>
  <radialGradient id="{sid}-o2"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".40"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <radialGradient id="{sid}-o3"><stop offset="0" stop-color="{AMBER}" stop-opacity=".22"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>
  <linearGradient id="{sid}-edge" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{TEAL}" stop-opacity=".9"/><stop offset=".5" stop-color="{VIOLET}" stop-opacity=".5"/><stop offset="1" stop-color="{AMBER}" stop-opacity=".8"/>
  </linearGradient>
  <clipPath id="{sid}-clip"><rect width="{W}" height="{h}" rx="18"/></clipPath>
</defs>
<style>
  #{sid} text {{ font-family: {SANS}; }}
  #{sid} .mono {{ font-family: {MONO}; }}
  #{sid} .o1 {{ animation: {sid}-fa 10s ease-in-out infinite; }}
  #{sid} .o2 {{ animation: {sid}-fb 13s ease-in-out infinite; }}
  #{sid} .o3 {{ animation: {sid}-fa 16s ease-in-out infinite reverse; }}
  #{sid} .in {{ animation: {sid}-in .7s ease-out both; }}
  #{sid} .cur {{ animation: {sid}-blink 1.1s step-end infinite; }}
  @keyframes {sid}-fa {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(34px,-18px); }} }}
  @keyframes {sid}-fb {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(-30px,16px); }} }}
  @keyframes {sid}-in {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  @keyframes {sid}-blink {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}
  {css}
  @media (prefers-reduced-motion: reduce) {{ #{sid} * {{ animation: none !important; }} }}
</style>
<g id="{sid}" clip-path="url(#{sid}-clip)">
  <rect width="{W}" height="{h}" fill="url(#{sid}-bg)"/>
  <ellipse class="o1" cx="120" cy="30" rx="260" ry="120" fill="url(#{sid}-o1)"/>
  <ellipse class="o2" cx="740" cy="{h - 20}" rx="300" ry="130" fill="url(#{sid}-o2)"/>
  <ellipse class="o3" cx="520" cy="10" rx="220" ry="90" fill="url(#{sid}-o3)"/>
  <rect x="14" y="14" width="{W - 28}" height="{h - 28}" rx="14" fill="#0b1224" fill-opacity=".55" stroke="{LINE}"/>
  <rect x="14" y="14" width="{W - 28}" height="2" fill="url(#{sid}-edge)"/>
{body}
</g>
</svg>
"""


def kicker(x: int, y: int, text: str, right: str = "") -> str:
    out = f'<text x="{x}" y="{y}" fill="{TEAL}" font-size="11" font-weight="700" letter-spacing="3" class="mono">{escape(text)}</text>'
    if right:
        out += f'<text x="{W - 40}" y="{y}" fill="{MUTED}" font-size="11" text-anchor="end" class="mono">{escape(right)}</text>'
    return out


def chip(x: int, y: int, text: str, color: str, delay: float, cls: str = "in") -> tuple[str, int]:
    w = int(len(text) * 7.4 + 26)
    s = (f'<g class="{cls}" style="animation-delay:{delay:.2f}s">'
         f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".6"/>'
         f'<circle cx="{x + 13}" cy="{y + 13}" r="3.5" fill="{color}"/>'
         f'<text x="{x + 22}" y="{y + 17.5}" fill="{INK}" font-size="12" font-weight="600">{escape(text)}</text></g>')
    return s, w


# ---------------------------------------------------------------- hero
def avatar_data() -> str:
    try:
        with urllib.request.urlopen(f"https://github.com/{USER}.png?size=240", timeout=20) as r:
            return "data:image/png;base64," + base64.b64encode(r.read()).decode()
    except OSError:
        return ""


def hero() -> str:
    sid, h = "hero", 280
    roles = [
        "Event-Driven Architecture enthusiast",
        "gRPC user, one contract for every stack",
        "Java enthusiast, Rust for high performance",
        "Fewer AI tokens, more deterministic code",
    ]
    n, slot = len(roles), 3.2
    total = n * slot
    css = []
    lines = []
    for i, r in enumerate(roles):
        a, b = i / n * 100, (i + 1) / n * 100
        css.append(f"#{sid} .r{i} {{ animation: {sid}-r{i} {total}s linear infinite; }}"
                   f"@keyframes {sid}-r{i} {{ 0% {{ opacity:0 }} {a:.2f}% {{ opacity:0; transform:translateY(6px) }}"
                   f" {a + 2:.2f}% {{ opacity:1; transform:translateY(0) }} {b - 2:.2f}% {{ opacity:1; transform:translateY(0) }}"
                   f" {b:.2f}% {{ opacity:0; transform:translateY(-6px) }} 100% {{ opacity:0 }} }}")
        lines.append(f'<text class="r{i} mono" x="230" y="168" fill="{TEAL}" font-size="17" opacity="0">&gt; {escape(r)}</text>')
    css.append(f"#{sid} .spin {{ animation: {sid}-spin 14s linear infinite; transform-origin: 770px 120px; }}"
               f"@keyframes {sid}-spin {{ to {{ transform: rotate(360deg); }} }}"
               f"#{sid} .ring {{ animation: {sid}-ring 4s ease-in-out infinite; transform-origin: 120px 125px; }}"
               f"@keyframes {sid}-ring {{ 0%,100% {{ opacity:.35; transform:scale(1) }} 50% {{ opacity:.9; transform:scale(1.04) }} }}")
    av = avatar_data()
    avatar = (f'<clipPath id="{sid}-av"><circle cx="120" cy="125" r="62"/></clipPath>'
              f'<circle class="ring" cx="120" cy="125" r="70" fill="none" stroke="{TEAL}" stroke-width="2"/>'
              + (f'<image href="{av}" x="58" y="63" width="124" height="124" clip-path="url(#{sid}-av)"/>' if av else
                 f'<circle cx="120" cy="125" r="62" fill="{BG1}"/>'))
    chips, x = [], 230
    for i, (t, c) in enumerate([("Java 21", AMBER), ("Spring Boot", "#6db33f"), ("gRPC", SKY),
                                ("Rust", "#dea584"), ("Event-Driven", TEAL), ("AI agents", VIOLET)]):
        s, w = chip(x, 196, t, c, 0.4 + i * 0.12)
        chips.append(s)
        x += w + 8
    # orbit: three "services" circling a broker
    orbit = (f'<circle cx="770" cy="120" r="60" fill="none" stroke="{LINE}" stroke-dasharray="3 6"/>'
             f'<circle cx="770" cy="120" r="34" fill="none" stroke="{LINE}"/>'
             f'<rect x="744" y="106" width="52" height="28" rx="7" fill="{BG1}" stroke="{TEAL}"/>'
             f'<text x="770" y="124.5" fill="{INK}" font-size="10" text-anchor="middle" class="mono">broker</text>'
             f'<g class="spin"><circle cx="830" cy="120" r="7" fill="{AMBER}"/><circle cx="740" cy="68" r="6" fill="{VIOLET}"/>'
             f'<circle cx="740" cy="172" r="6" fill="{SKY}"/></g>')
    body = f"""{avatar}
  <text class="in mono" x="230" y="72" fill="{TEAL}" font-size="13" letter-spacing="2">@{USER.lower()}  ·  São Paulo, BR</text>
  <text class="in" x="228" y="124" fill="{INK}" font-size="44" font-weight="800" style="animation-delay:.1s">Rafael Pereira</text>
  <text class="in" x="230" y="146" fill="{MUTED}" font-size="14" style="animation-delay:.2s">Software Engineer @ Getnet · Open Finance · AI Champion</text>
  {''.join(lines)}
  {''.join(chips)}
  {orbit}
"""
    return frame(sid, h, body, "\n".join(css), "Rafael Pereira, Software Engineer")


# ---------------------------------------------------------------- event flow
def event_flow() -> str:
    sid, h = "flow", 300
    nodes = [  # x, y, w, label, sub, color
        (40, 120, 110, "Pix API", "Open Finance", AMBER),
        (190, 120, 110, "Outbox", "same TX", TEAL),
        (340, 120, 130, "Broker", "RabbitMQ · ASB", SKY),
        (530, 70, 140, "Consumer A", "idempotent", TEAL),
        (530, 170, 140, "Consumer B", "idempotent", TEAL),
        (720, 120, 100, "DLQ", "retry", ROSE),
    ]
    boxes = []
    for i, (x, y, w, t, s, c) in enumerate(nodes):
        boxes.append(f'<g class="in" style="animation-delay:{0.15 * i:.2f}s">'
                     f'<rect x="{x}" y="{y}" width="{w}" height="54" rx="10" fill="{BG1}" stroke="{c}" stroke-opacity=".8"/>'
                     f'<text x="{x + w / 2}" y="{y + 24}" fill="{INK}" font-size="14" font-weight="700" text-anchor="middle">{t}</text>'
                     f'<text x="{x + w / 2}" y="{y + 42}" fill="{MUTED}" font-size="11" text-anchor="middle" class="mono">{s}</text></g>')
    paths = {
        "p1": "M150 147 L190 147",
        "p2": "M300 147 L340 147",
        "p3": "M470 140 C500 140 500 97 530 97",
        "p4": "M470 154 C500 154 500 197 530 197",
        "p5": "M670 197 C700 197 690 147 720 147",
        "p6": "M770 174 C770 260 405 260 405 174",  # retry back to broker
    }
    dashed = ' stroke-dasharray="5 5"'
    wires = "".join(f'<path d="{d}" fill="none" stroke="{ROSE if k in ("p5", "p6") else LINE}" '
                    f'stroke-width="2"{dashed if k in ("p5", "p6") else ""}/>' for k, d in paths.items())

    cycle = 10.0

    def packet(route: list[str], color: str, begin: float, seg: float = 1.1) -> str:
        # One motion along the joined route, repeated every `cycle` seconds.
        # The packet travels during the first `frac` of the cycle, then hides.
        d = " ".join(paths[k] for k in route)
        frac = min(0.95, len(route) * seg / cycle)
        return (f'<circle r="5" fill="{color}" opacity="0">'
                f'<animate attributeName="opacity" values="1;0" keyTimes="0;{frac:.3f}" calcMode="discrete" dur="{cycle}s" begin="{begin}s" repeatCount="indefinite"/>'
                f'<animateMotion path="{d}" keyPoints="0;1;1" keyTimes="0;{frac:.3f};1" calcMode="linear" dur="{cycle}s" begin="{begin}s" repeatCount="indefinite"/></circle>')

    packets = (packet(["p1", "p2", "p3"], TEAL, 0.0) + packet(["p1", "p2", "p4"], AMBER, 1.6)
               + packet(["p1", "p2", "p4", "p5", "p6"], ROSE, 3.2) + packet(["p1", "p2", "p3"], SKY, 6.4))
    loop = ""
    body = f"""{kicker(40, 50, "EVENT FLOW", "outbox → broker → idempotent consumers")}
  <text x="40" y="80" fill="{INK}" font-size="20" font-weight="800">Messages that never get lost or processed twice</text>
  {wires}{''.join(boxes)}{packets}{loop}
  <text x="588" y="262" fill="{ROSE}" font-size="11" class="mono">poison message → DLQ → retry</text>
  <text x="40" y="270" fill="{MUTED}" font-size="11" class="mono">pub/sub · Azure Service Bus · Event Hubs · P95/P99 latency budgets</text>
"""
    return frame(sid, h, body, label="Event-driven flow: outbox, broker, idempotent consumers, DLQ with retry")


# ---------------------------------------------------------------- token budget
def token_budget() -> str:
    sid, h = "tokens", 330
    stages = [  # label, how, width fraction (illustrative, not measured), color
        ("Raw request", "everything the agent could read", 1.00, ROSE),
        ("CAG cache", "repeated context served from cache", 0.74, AMBER),
        ("Scripts", "fixed queries replace model-written ones", 0.52, SKY),
        ("Qdrant", "vector search keeps only what matters", 0.33, TEAL),
        ("Jev / Laya", "route simple subtasks to the cheap model", 0.20, VIOLET),
    ]
    maxw = 430
    rows, css = [], []
    for i, (t, how, f, c) in enumerate(stages):
        y = 104 + i * 40
        w = int(maxw * f)
        css.append(f"#{sid} .b{i} {{ animation: {sid}-grow 1.1s cubic-bezier(.2,.8,.2,1) both {0.3 + i * 0.35:.2f}s; transform-box: fill-box; transform-origin: left; }}")
        rows.append(f'<g class="in" style="animation-delay:{0.2 + i * 0.35:.2f}s">'
                    f'<text x="40" y="{y + 17}" fill="{INK}" font-size="14" font-weight="700">{t}</text>'
                    f'<text x="40" y="{y + 32}" fill="{MUTED}" font-size="10.5">{how}</text></g>'
                    f'<rect x="330" y="{y + 4}" width="{maxw}" height="20" rx="10" fill="{LINE}" fill-opacity=".45"/>'
                    f'<rect class="b{i}" x="330" y="{y + 4}" width="{w}" height="20" rx="10" fill="{c}" fill-opacity=".85"/>')
    css.append(f"@keyframes {sid}-grow {{ from {{ transform: scaleX(0); opacity:.2 }} 40% {{ opacity:1 }} to {{ transform: scaleX(1); opacity:1 }} }}")
    # scanning line that sweeps the bars, like a filter passing over the context
    css.append(f"#{sid} .scan {{ animation: {sid}-scan 4.5s ease-in-out infinite; }}"
               f"@keyframes {sid}-scan {{ 0% {{ transform: translateX(0) }} 50% {{ transform: translateX({maxw - 6}px) }} 100% {{ transform: translateX(0) }} }}")
    body = f"""{kicker(40, 50, "TOKEN BUDGET", "deterministic first, inference last")}
  <text x="40" y="80" fill="{INK}" font-size="20" font-weight="800">If it can be deterministic, it should not be inference</text>
  {''.join(rows)}
  <rect class="scan" x="330" y="104" width="3" height="190" rx="1.5" fill="{TEAL}" fill-opacity=".55"/>
  <text x="{W - 40}" y="{h - 26}" fill="{MUTED}" font-size="10" text-anchor="end" class="mono">bar widths are illustrative</text>
"""
    return frame(sid, h, body, "\n".join(css), "Token budget: cache, scripts, vector search and routing before the model")


# ---------------------------------------------------------------- projects
def projects(langs: dict[str, str]) -> str:
    sid = "projects"
    rowh = 54
    h = 110 + rowh * len(FEATURED)
    rows = []
    for i, (name, desc, tags) in enumerate(FEATURED):
        y = 96 + i * rowh
        lang = langs.get(name) or ""
        lc = LANG_COLORS.get(lang, MUTED)
        tx = 520
        tag_svg = []
        for t in tags:
            tw = int(len(t) * 6.6 + 16)
            tag_svg.append(f'<rect x="{tx}" y="{y + 10}" width="{tw}" height="20" rx="6" fill="{LINE}" fill-opacity=".6"/>'
                           f'<text x="{tx + tw / 2}" y="{y + 24}" fill="{INK}" font-size="10.5" text-anchor="middle" class="mono">{t}</text>')
            tx += tw + 6
        rows.append(f'<g class="in" style="animation-delay:{0.25 + i * 0.12:.2f}s">'
                    f'<rect x="32" y="{y}" width="{W - 64}" height="{rowh - 8}" rx="9" fill="{BG1}" fill-opacity=".7" stroke="{LINE}"/>'
                    f'<text x="50" y="{y + 20}" fill="{SKY}" font-size="14" font-weight="700" class="mono">{escape(name)}</text>'
                    f'<text x="50" y="{y + 37}" fill="{MUTED}" font-size="11.5">{escape(desc)}</text>'
                    + (f'<circle cx="{W - 140}" cy="{y + 20}" r="5" fill="{lc}"/><text x="{W - 130}" y="{y + 24}" fill="{MUTED}" font-size="11">{escape(lang)}</text>' if lang else "")
                    + "".join(tag_svg) + "</g>")
    body = f"""<circle cx="44" cy="44" r="6" fill="{ROSE}"/><circle cx="64" cy="44" r="6" fill="{AMBER}"/><circle cx="84" cy="44" r="6" fill="#22c55e"/>
  <text x="110" y="48.5" fill="{MUTED}" font-size="12" class="mono">~/raphonzius $ ls --featured</text>
  <text x="{W - 40}" y="48.5" fill="{TEAL}" font-size="12" text-anchor="end" class="mono">{len(FEATURED)} projects<tspan class="cur"> ▌</tspan></text>
  <rect x="32" y="66" width="{W - 64}" height="1" fill="{LINE}"/>
  {''.join(rows)}
"""
    return frame(sid, h, body, label="Featured projects")


# ---------------------------------------------------------------- live data
def gql(query: str, token: str) -> dict:
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": query}).encode(),
                                 headers={"Authorization": f"bearer {token}", "User-Agent": USER})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def fetch(token: str) -> dict:
    q = """{ user(login: "%s") {
      followers { totalCount }
      repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false) {
        totalCount
        nodes { name stargazerCount primaryLanguage { name }
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } } }
      contributionsCollection { totalCommitContributions restrictedContributionsCount
        contributionCalendar { totalContributions weeks { contributionDays { contributionCount date } } } } } }""" % USER
    return gql(q, token)["user"]


def stats(u: dict) -> str:
    sid, h = "stats", 200
    repos = [r for r in u["repositories"]["nodes"] if r["name"] not in EXCLUDED]
    cc = u["contributionsCollection"]
    cal = cc["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    active = sum(1 for d in days if d["contributionCount"] > 0)
    best = max(days, key=lambda d: d["contributionCount"]) if days else {"contributionCount": 0}
    cards = [("Contributions", cal["totalContributions"], "last 12 months", TEAL),
             ("Commits", cc["totalCommitContributions"] + cc["restrictedContributionsCount"], "public + private", AMBER),
             ("Active days", active, f"busiest: {best['contributionCount']}", VIOLET),
             ("Public repos", len(repos), f"{u['followers']['totalCount']} followers", SKY)]
    cw = (W - 64 - 3 * 12) / 4
    out = []
    for i, (t, v, s, c) in enumerate(cards):
        x = 32 + i * (cw + 12)
        out.append(f'<g class="in" style="animation-delay:{0.15 + i * 0.12:.2f}s">'
                   f'<rect x="{x:.0f}" y="76" width="{cw:.0f}" height="94" rx="12" fill="{BG1}" fill-opacity=".75" stroke="{LINE}"/>'
                   f'<rect x="{x:.0f}" y="76" width="4" height="94" rx="2" fill="{c}"/>'
                   f'<text x="{x + 20:.0f}" y="102" fill="{MUTED}" font-size="11" letter-spacing="1.5" class="mono">{t.upper()}</text>'
                   f'<text x="{x + 20:.0f}" y="140" fill="{INK}" font-size="32" font-weight="800">{v}</text>'
                   f'<text x="{x + 20:.0f}" y="160" fill="{MUTED}" font-size="11">{escape(s)}</text></g>')
    body = f"""{kicker(40, 50, "PROFILE SIGNAL", f"updated {date.today().isoformat()}")}
  {''.join(out)}"""
    return frame(sid, h, body, label="GitHub stats")


def stack(u: dict) -> str:
    sid = "stack"
    totals: dict[str, int] = {}
    for r in u["repositories"]["nodes"]:
        if r["name"] in EXCLUDED:
            continue
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            if n in ("HTML", "CSS", "Jupyter Notebook", "Dockerfile", "Batchfile"):
                continue  # markup and notebooks are not the stack
            totals[n] = totals.get(n, 0) + e["size"]
    top = sorted(totals.items(), key=lambda kv: -kv[1])[:6]
    s = sum(v for _, v in top) or 1
    h = 92 + 34 * len(top)
    rows, css = [], []
    for i, (n, v) in enumerate(top):
        y = 84 + i * 34
        pct = v / s * 100
        c = LANG_COLORS.get(n, MUTED)
        bw = 470 * pct / 100
        css.append(f"#{sid} .b{i} {{ animation: {sid}-g 1.2s cubic-bezier(.2,.8,.2,1) both {0.2 + i * 0.12:.2f}s; transform-box: fill-box; transform-origin: left; }}")
        rows.append(f'<circle cx="46" cy="{y + 9}" r="5" fill="{c}"/>'
                    f'<text x="62" y="{y + 14}" fill="{INK}" font-size="14" font-weight="700">{escape(n)}</text>'
                    f'<text x="250" y="{y + 14}" fill="{c}" font-size="13" text-anchor="end" class="mono">{pct:.0f}%</text>'
                    f'<rect x="272" y="{y + 2}" width="470" height="14" rx="7" fill="{LINE}" fill-opacity=".5"/>'
                    f'<rect class="b{i}" x="272" y="{y + 2}" width="{bw:.1f}" height="14" rx="7" fill="{c}"/>')
    css.append(f"@keyframes {sid}-g {{ from {{ transform: scaleX(0) }} to {{ transform: scaleX(1) }} }}")
    body = f"""{kicker(40, 50, "LANGUAGE STACK", "public repos, experiments excluded")}
  {''.join(rows)}"""
    return frame(sid, h, body, "\n".join(css), "Language stack")


def stream(u: dict) -> str:
    """Contribution calendar drawn as an event stream: a consumer sweeps the
    weeks left to right and each day lights up as it is 'consumed'."""
    sid = "stream"
    weeks = u["contributionsCollection"]["contributionCalendar"]["weeks"]
    cell, gap = 11, 3
    x0, y0 = 40, 84
    h = y0 + 7 * (cell + gap) + 60
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=1) or 1
    levels = [LINE, "#134e4a", "#0f766e", "#14b8a6", TEAL]
    cells, css = [], []
    sweep = 6.0
    n = len(weeks)
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            dow = date.fromisoformat(d["date"]).isoweekday() % 7
            c = d["contributionCount"]
            lv = 0 if c == 0 else min(4, 1 + int(3 * c / peak))
            x, y = x0 + wi * (cell + gap), y0 + dow * (cell + gap)
            cls = f' class="c" style="animation-delay:{wi / n * sweep:.2f}s"' if lv else ""
            cells.append(f'<rect{cls} x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{levels[lv]}"/>')
    width = n * (cell + gap)
    css.append(f"#{sid} .c {{ animation: {sid}-hit {sweep}s ease-out infinite; }}"
               f"@keyframes {sid}-hit {{ 0% {{ fill:{AMBER} }} 8% {{ fill:{AMBER} }} 30% {{ }} 100% {{ }} }}"
               f"#{sid} .head {{ animation: {sid}-mv {sweep}s linear infinite; }}"
               f"@keyframes {sid}-mv {{ from {{ transform: translateX(0) }} to {{ transform: translateX({width}px) }} }}")
    total = u["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    body = f"""{kicker(40, 50, "CONTRIBUTION STREAM", f"{total} events consumed this year")}
  {''.join(cells)}
  <g class="head"><rect x="{x0 - 4}" y="{y0 - 8}" width="2" height="{7 * (cell + gap) + 12}" fill="{AMBER}" fill-opacity=".9"/>
  <text x="{x0 - 3}" y="{y0 + 7 * (cell + gap) + 18}" fill="{AMBER}" font-size="10" text-anchor="middle" class="mono">consumer</text></g>
"""
    return frame(sid, h, body, "\n".join(css), "Contribution calendar as an event stream")


# ---------------------------------------------------------------- main
def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "static"
    root = Path(__file__).resolve().parent.parent
    if mode == "static":
        out = root / "assets"
        out.mkdir(exist_ok=True)
        langs = {}
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            u = fetch(token)
            langs = {r["name"]: (r["primaryLanguage"] or {}).get("name", "") for r in u["repositories"]["nodes"]}
        for name, svg in (("hero", hero()), ("event-flow", event_flow()), ("token-budget", token_budget()),
                          ("projects", projects(langs))):
            (out / f"{name}.svg").write_text(svg, encoding="utf-8")
            print("wrote", name)
    elif mode == "live":
        out = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "output"
        out.mkdir(parents=True, exist_ok=True)
        u = fetch(os.environ["GITHUB_TOKEN"])
        for name, svg in (("stats", stats(u)), ("stack", stack(u)), ("stream", stream(u))):
            (out / f"{name}.svg").write_text(svg, encoding="utf-8")
            print("wrote", name)
    else:
        raise SystemExit(f"unknown mode {mode}")


if __name__ == "__main__":
    main()
