"""Shared helpers for the profile SVG themes. Stdlib only.

- data():   GitHub profile data (GraphQL), cached in gen/.cache/data.json for local work.
- font():   a Google Fonts face subset to printable ASCII + Latin-1, as an @font-face rule
            with a base64 woff2 data URI. Fonts inside an <img> SVG cannot load from the
            network, so they must be embedded.
- svg():    wraps a body in an <svg> root with a scoped <style>.
- preview(): renders a markdown file to PNG with every local SVG inlined (Edge headless).
"""
from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import urllib.parse
import urllib.request
from html import escape as _esc
from pathlib import Path

USER = "Raphonzius"
ROOT = Path(__file__).resolve().parent.parent
CACHE = Path(__file__).resolve().parent / ".cache"
EXCLUDED = {"agent-kit", "explaining-ai", "Jarvis", "tsp-graph", "my-llm-orchestration"}

# Emil Kowalski / Apple curves.
EASE_OUT = "cubic-bezier(0.23, 1, 0.32, 1)"
EASE_IN_OUT = "cubic-bezier(0.77, 0, 0.175, 1)"

GLYPHS = "".join(chr(c) for c in range(32, 127)) + "ÀÁÂÃÇÉÊÍÓÔÕÚàáâãçéêíóôõú·—–→←↑↓×•…%"


def esc(s: object) -> str:
    return _esc(str(s), quote=True)


# ------------------------------------------------------------------ data
def _gql(query: str, token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": USER})
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.load(r)
    if "errors" in out:
        raise RuntimeError(out["errors"])
    return out["data"]


def data(refresh: bool = False) -> dict:
    """Returns {'user': ..., 'avatar': data-uri}. Needs GITHUB_TOKEN unless cached."""
    cache = CACHE / "data.json"
    if cache.exists() and not refresh and not os.environ.get("CI"):
        return json.loads(cache.read_text(encoding="utf-8"))
    token = os.environ["GITHUB_TOKEN"]
    q = """{ user(login: "%s") {
      name followers { totalCount }
      repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false) {
        nodes { name description stargazerCount pushedAt primaryLanguage { name color }
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } } }
      contributionsCollection { totalCommitContributions restrictedContributionsCount
        contributionCalendar { totalContributions weeks { contributionDays { contributionCount date } } } } } }""" % USER
    user = _gql(q, token)["user"]
    with urllib.request.urlopen(f"https://github.com/{USER}.png?size=256", timeout=20) as r:
        avatar = "data:image/png;base64," + base64.b64encode(r.read()).decode()
    out = {"user": user, "avatar": avatar}
    CACHE.mkdir(exist_ok=True)
    cache.write_text(json.dumps(out), encoding="utf-8")
    return out


def summary(d: dict) -> dict:
    """Derived numbers every theme can use. All real, from the API."""
    u = d["user"]
    repos = [r for r in u["repositories"]["nodes"] if r["name"] not in EXCLUDED]
    cc = u["contributionsCollection"]
    cal = cc["contributionCalendar"]
    days = [x for w in cal["weeks"] for x in w["contributionDays"]]
    langs: dict[str, list] = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            if n in ("HTML", "CSS", "Jupyter Notebook", "Dockerfile", "Batchfile"):
                continue
            langs.setdefault(n, [0, e["node"]["color"]])[0] += e["size"]
    total = sum(v[0] for v in langs.values()) or 1
    stack = [(n, v[0] / total, v[1]) for n, v in sorted(langs.items(), key=lambda kv: -kv[1][0])][:6]
    return {
        "contributions": cal["totalContributions"],
        "commits": cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        "active_days": sum(1 for x in days if x["contributionCount"]),
        "busiest": max((x["contributionCount"] for x in days), default=0),
        "repos": len(repos),
        "followers": u["followers"]["totalCount"],
        "weeks": cal["weeks"],
        "stack": stack,  # [(name, share 0..1, github color)]
        "repo_lang": {r["name"]: (r["primaryLanguage"] or {}).get("name", "") for r in repos},
    }


# ------------------------------------------------------------------ fonts
def font(family: str, weight: int = 400, italic: bool = False, alias: str | None = None,
         text: str | None = None) -> str:
    """@font-face rule with an embedded, subset woff2. Cached on disk.
    `text`: subset to exactly these characters (one card's glyphs), which keeps each SVG small."""
    import hashlib
    CACHE.mkdir(exist_ok=True)
    glyphs = "".join(sorted(set(text + " "))) if text is not None else GLYPHS
    tag = hashlib.sha1(glyphs.encode()).hexdigest()[:10] if text is not None else "all"
    key = re.sub(r"\W+", "_", f"{family}_{weight}_{int(italic)}_{tag}")
    f = CACHE / f"{key}.woff2"
    if not f.exists():
        spec = f"{family}:ital,wght@{int(italic)},{weight}"
        url = ("https://fonts.googleapis.com/css2?family=" + urllib.parse.quote(spec, safe=":,@;")
               + "&text=" + urllib.parse.quote(glyphs) + "&display=block")
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": ua}), timeout=30).read().decode()
        src = re.search(r"url\((https://[^)]+)\)", css).group(1)
        f.write_bytes(urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent": ua}), timeout=30).read())
    b64 = base64.b64encode(f.read_bytes()).decode()
    return (f"@font-face{{font-family:'{alias or family}';font-weight:{weight};font-style:{'italic' if italic else 'normal'};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")


# ------------------------------------------------------------------ svg
def svg(sid: str, w: int, h: int, body: str, css: str = "", label: str = "", defs: str = "") -> str:
    """Root element. `sid` scopes the CSS so several SVGs never clash when inlined."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(label or sid)}"><title>{esc(label or sid)}</title>'
            f'<defs>{defs}</defs><style>{css}</style><g id="{sid}">{body}</g></svg>\n')


# ------------------------------------------------------------------ preview
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def preview(md_path: Path, png_path: Path, height: int = 4200, wait_ms: int = 6000, static: bool = False,
            width: int = 930, bg: str = "#0d1117", reduced_motion: bool = False, column: int = 880) -> None:
    """GitHub-markdown render of md_path with local SVGs inlined, screenshot to png_path.
    Uses `gh api markdown`, so `gh` must be logged in.
    static=True turns CSS animations off, so the shot shows every card's resting (final) state;
    headless capture otherwise often lands mid-entrance. width: browser window (400 ~ a phone).
    bg: page colour (#ffffff for GitHub light). reduced_motion: emulate prefers-reduced-motion."""
    md = md_path.read_text(encoding="utf-8")
    tmp = png_path.with_suffix(".req.json")
    tmp.write_text(json.dumps({"text": md, "mode": "markdown"}), encoding="utf-8")
    html = subprocess.run(["gh", "api", "markdown", "--input", str(tmp)], capture_output=True, check=True).stdout.decode("utf-8")
    tmp.unlink()

    def inline(m: re.Match) -> str:
        tag = m.group(0)
        src = re.search(r'src="([^"]+\.svg)"', tag).group(1)
        wm = re.search(r'width="(\d+%?)"', tag)
        w_attr = wm.group(1) if wm else "100%"
        w_css = w_attr if w_attr.endswith("%") else f"{w_attr}px"
        p = (md_path.parent / src).resolve()
        if not p.exists():
            p = (ROOT / src.lstrip("/")).resolve()  # "/assets/..." is repo-root relative on GitHub
        if p.exists() and p.suffix == ".svg":
            s = p.read_text(encoding="utf-8")
            # honour the <img width>, like GitHub does, so side-by-side cards stay side by side
            s = s.replace("<svg ", '<svg style="width:100%;height:auto;display:block" ', 1)
            # GitHub: <img width="410"> plus img{max-width:100%}; same here, so pairs wrap on narrow windows
            return f'<span style="display:inline-block;vertical-align:top;width:{w_css};max-width:100%">{s}</span>'
        return tag

    html = re.sub(r'<img[^>]*?src="[^"]+\.svg"[^>]*>', inline, html)
    fg = "#1f2328" if bg.lower() in ("#fff", "#ffffff") else "#e6edf3"
    page = ("<html><head><meta charset='utf-8'><style>body{background:" + bg + ";color:" + fg + ";"
            "font-family:-apple-system,Segoe UI,Arial;max-width:" + str(column) + "px;margin:24px auto;padding:0 16px;line-height:1.5}"
            "a{color:#4493f8}h1,h2{border-bottom:1px solid #30363d;padding-bottom:.3em}img{max-width:100%}"
            "p{margin:0 0 16px}" + ("*{animation:none!important}" if static else "")
            + "</style></head><body>" + html + "</body></html>")
    hp = png_path.with_suffix(".html")
    hp.write_text(page, encoding="utf-8")
    args = [EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", f"--virtual-time-budget={wait_ms}",
            f"--window-size={width},{height}", f"--screenshot={png_path}"]
    if reduced_motion:
        args.append("--force-prefers-reduced-motion")
    subprocess.run(args + [hp.as_uri()], capture_output=True)
    hp.unlink()
