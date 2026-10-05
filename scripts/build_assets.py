"""Build every SVG used by the profile README.

Outputs (in ../assets):
  hero-dark.svg, hero-light.svg            opening banner with the knowledge-graph animation
  card-ncu-dark.svg, card-ncu-light.svg    NCU AI Discovery System card
  card-green-dark.svg, card-green-light.svg
  icon-ai.svg, icon-systems.svg, icon-apps.svg   small category icons (one file works on both themes)

Notes
- The README picks dark or light with <picture> + prefers-color-scheme, which GitHub maps to its own theme.
- An SVG shown through <img> cannot load web fonts, so text uses system font stacks.
- Animations are SMIL on a 9 s cycle and start right after each image loads (GitHub loads images
  independently, so they are not chained); every file's resting frame is the finished state.
- Cards switch to a compact layout below 320 px rendered width, the hero below 520 px.

Run:  python scripts/build_assets.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"
DUR = "9s"

SANS = "'Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,'Microsoft JhengHei','PingFang TC','Noto Sans TC',sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"

THEMES = {
    # neutral greys follow GitHub's own palette so the cards sit naturally on the page;
    # teal and amber are the only accents
    "light": dict(bg="#f6f8fa", line="#d0d7de", fg="#1f2328", mu="#59636e", te="#0e786d",
                  am="#b5690f", edge="#d0d7de", box="#ffffff"),
    "dark": dict(bg="#161b22", line="#30363d", fg="#e6edf3", mu="#8b949e", te="#4fc4b6",
                 am="#f0ae52", edge="#30363d", box="#0d1117"),
}


def style(t, extra=""):
    return f"""
  <style>
    .bg{{fill:{t['bg']};stroke:{t['line']}}}
    .fg{{fill:{t['fg']}}} .mu{{fill:{t['mu']}}} .te{{fill:{t['te']}}} .am{{fill:{t['am']}}}
    .edge{{stroke:{t['edge']};fill:none;stroke-width:1.3}} .edgef{{fill:{t['edge']}}}
    .node{{fill:{t['bg']};stroke:{t['te']};stroke-width:1.6}}
    .ring{{fill:none;stroke:{t['am']};stroke-width:1.5}}
    .box{{fill:{t['box']};stroke:{t['te']};stroke-width:1.4}}
    .pill{{fill:{t['box']};stroke:{t['edge']}}}
    .tk{{stroke:{t['te']}}} .tf{{fill:{t['te']}}} .af{{fill:{t['am']}}}
    .title{{font:700 19px {SANS}}}
    .big{{font:700 25px {SANS}}}
    .sub{{font:400 13px {SANS}}}
    .tag{{font:400 20px {SANS}}}
    .t-disp{{font-family:{SANS};font-weight:700}}
    .t-body{{font-family:{SANS}}}
    .mono,.t-mono{{font-family:{MONO}}}
    .compact{{display:none}}
{extra}
  </style>"""


def anim(attr, values, key_times):
    return (f'<animate attributeName="{attr}" values="{values}" keyTimes="{key_times}" '
            f'dur="{DUR}" repeatCount="indefinite"/>')


def wrap(w, h, label, t, body, extra_css="", rx=12):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
            f'{style(t, extra_css)}\n  <rect class="bg" x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}"/>\n'
            f'  {body}\n</svg>\n')


def arrow(x1, y, x2):
    return (f'<path class="edge" d="M{x1} {y} L{x2} {y}"/>'
            f'<path class="edge" d="M{x2-4} {y-4} L{x2} {y} L{x2-4} {y+4}"/>')


def proposal(x, y, s=1.0):
    w, h, f = 36 * s, 56 * s, 10 * s
    out = [f'<path class="box" d="M{x} {y} L{x+w-f} {y} L{x+w} {y+f} L{x+w} {y+h} L{x} {y+h} Z"/>',
           f'<path class="box" style="fill:none" d="M{x+w-f} {y} L{x+w-f} {y+f} L{x+w} {y+f}"/>']
    for i, lw in enumerate([22, 18, 22, 14]):
        out.append(f'<rect class="edgef" x="{x+6*s:.1f}" y="{y+(18+9*i)*s:.1f}" width="{lw*s:.1f}" '
                   f'height="{3*s:.1f}" rx="{1.5*s:.1f}"/>')
    return "".join(out)


def check(x, y, t0, t1, w=2.0, s=1.0):
    return (f'<path class="tk" d="M{x} {y} l{4*s} {4*s} l{7*s} {-8*s}" fill="none" stroke-width="{w}" '
            f'stroke-linecap="round">{anim("opacity", "0;0;1;1;0", f"0;{t0};{t1};.95;1")}</path>')


CARD_CSS = "    @media (max-width: 320px){ .full{display:none} .compact{display:inline} }"


# ---------------------------------------------------------------- hero
def build_hero(t):
    graph = (ROOT / "parts" / "hero_graph.svgpart").read_text(encoding="utf-8")
    graph = graph.replace("var(--amber)", t["am"]).replace("var(--edge)", t["edge"])
    graph = graph.replace('<g transform=', '<g class="graph" transform=', 1)
    body = f"""<defs><pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{t['edge']}"/></pattern></defs>
  <rect x="396" y="14" width="470" height="222" rx="10" fill="url(#dots)" opacity=".7"/>
  <text class="t-mono mu full" x="40" y="74" font-size="13">~/clairechien0627</text>
  <text class="t-disp fg name" x="40" y="126" font-size="38">Yun-Fang Chien</text>
  <text class="t-body mu full" x="40" y="160" font-size="15">簡筠方 · CSIE, National Central University</text>
  <text class="t-mono te full" x="40" y="194" font-size="12.5">llm agents · retrieval · efficient ai</text>
  <text class="t-body mu compact" x="40" y="178" font-size="26">簡筠方 · NCU CSIE</text>
  {graph}"""
    css = ("    @media (max-width: 520px){ .full{display:none} .compact{display:inline} "
           ".graph text{display:none} .name{font-size:54px} }")
    label = ("Yun-Fang Chien (簡筠方), CSIE at National Central University. "
             "Interests: LLM agents, retrieval, efficient AI.")
    return wrap(880, 250, label, t, body, css, rx=14)


# ---------------------------------------------------------------- NCU card
def build_ncu(t):
    full = ['<g class="full">',
            '<text class="title fg" x="24" y="38">NCU AI Discovery System</text>',
            '<text class="sub mu" x="24" y="60">Turns real research proposals into an interest quiz</text>',
            proposal(28, 84),
            '<text class="mono mu" x="46" y="162" font-size="11" text-anchor="middle">proposal</text>',
            arrow(72, 112, 88)]
    for i, q in enumerate(["scenario", "method", "mindset"]):
        y = 84 + i * 24
        full.append(f'<rect class="pill" x="96" y="{y}" width="134" height="19" rx="9.5"/>')
        full.append(f'<text class="mono fg" x="108" y="{y+13.5}" font-size="11">Q{i+1} · {q}</text>')
        full.append(check(208, y + 9.5, f"{.06+i*.07:.2f}", f"{.08+i*.07:.2f}"))
    full.append(arrow(238, 112, 252))
    for i, (name, w) in enumerate([("Mech. Eng.", 64), ("Earth Sci.", 30), ("Optics", 46)]):
        y = 86 + i * 24
        cls, op = ("af", .9) if i == 0 else ("tf", .55)
        full.append(f'<text class="mono mu" x="258" y="{y+10}" font-size="11">{name}</text>')
        full.append(f'<rect class="pill" style="fill:none" x="336" y="{y}" width="70" height="11" rx="3"/>')
        full.append(f'<rect class="{cls}" x="336" y="{y}" width="{w}" height="11" rx="3" opacity="{op}">'
                    f'{anim("width", f"0;0;{w};{w};0", "0;.24;.42;.95;1")}</rect>')
    full.append('</g>')
    compact = ['<g class="compact">',
               '<text class="big fg" x="28" y="56">NCU AI Discovery</text>',
               '<text class="big fg" x="28" y="88">System</text>',
               '<text class="tag mu" x="28" y="146">Research papers</text>',
               '<text class="tag mu" x="28" y="172">→ an interest quiz</text>',
               proposal(318, 104, 1.05),
               f'<circle class="tf" cx="366" cy="158" r="15"/>',
               f'<path d="M358 158 l5 5 l10 -11" fill="none" stroke="{t["box"]}" stroke-width="3" stroke-linecap="round"/>',
               '</g>']
    label = ("NCU AI Discovery System: a research proposal becomes three quiz questions, "
             "and the answers add up into department scores (example).")
    return wrap(430, 190, label, t, "\n  ".join(full + compact), CARD_CSS)


# ---------------------------------------------------------------- Green AI card
def build_green(t):
    rows = [("accuracy", .94), ("latency", .34), ("memory", .38), ("carbon", .20)]
    x0, W = 110, 290
    full = ['<g class="full">',
            '<text class="title fg" x="24" y="38">Green AI Compression Orchestrator</text>',
            '<text class="sub mu" x="24" y="60">An LLM agent searches for a better compression setting</text>']
    for i, (name, r) in enumerate(rows):
        y = 78 + i * 21
        w = round(W * r, 1)
        cls, op = ("tf", .55) if i == 0 else ("af", .85)
        full.append(f'<text class="mono {"fg" if i == 0 else "mu"}" x="24" y="{y+10.5}" font-size="12">{name}</text>')
        full.append(f'<rect class="pill" style="fill:none" x="{x0}" y="{y}" width="{W}" height="12" rx="3"/>')
        full.append(f'<rect class="{cls}" x="{x0}" y="{y}" width="{w}" height="12" rx="3" opacity="{op}">'
                    f'{anim("width", f"{W};{W};{w};{w};{W}", "0;.06;.26;.96;1")}</rect>')
    full += ['<rect class="pill" style="fill:none" x="24" y="167" width="14" height="9" rx="2"/>',
             '<text class="mono mu" x="44" y="175" font-size="11">original</text>',
             '<rect class="af" x="120" y="167" width="14" height="9" rx="2" opacity=".85"/>',
             "<text class=\"mono mu\" x=\"140\" y=\"175\" font-size=\"11\">agent's pick</text>",
             '</g>']
    compact = ['<g class="compact">',
               '<text class="big fg" x="28" y="56">Green AI Compression</text>',
               '<text class="big fg" x="28" y="88">Orchestrator</text>',
               '<text class="tag mu" x="28" y="146">Smaller, faster,</text>',
               '<text class="tag mu" x="28" y="172">greener LLMs</text>']
    for i, (_, r) in enumerate(rows):
        cls, op = ("tf", .55) if i == 0 else ("af", .85)
        compact.append(f'<rect class="{cls}" x="318" y="{112+i*15}" width="{round(84*r,1)}" height="10" rx="3" opacity="{op}"/>')
    compact.append('</g>')
    label = ("Green AI Compression Orchestrator, illustrative: accuracy stays close to the original "
             "while latency, memory and carbon shrink.")
    return wrap(430, 190, label, t, "\n  ".join(full + compact), CARD_CSS)


# ---------------------------------------------------------------- category icons (mid-tone colors that read on both themes)
ICON_TE, ICON_AM, ICON_EDGE = "#2a9d8f", "#d08a2e", "#8b9c98"
ICONS = {
    "icon-ai": f'<path d="M4 15 L10 5 L16 13 Z" fill="none" stroke="{ICON_EDGE}" stroke-width="1.4"/>'
               f'<circle cx="4" cy="15" r="2.4" fill="{ICON_AM}"/>'
               f'<circle cx="10" cy="5" r="2.4" fill="none" stroke="{ICON_TE}" stroke-width="1.6"/>'
               f'<circle cx="16" cy="13" r="2.4" fill="none" stroke="{ICON_TE}" stroke-width="1.6"/>',
    "icon-systems": f'<rect x="3" y="2.5" width="14" height="4" rx="1.5" fill="none" stroke="{ICON_TE}" stroke-width="1.4"/>'
                    f'<rect x="3" y="8" width="14" height="4" rx="1.5" fill="none" stroke="{ICON_TE}" stroke-width="1.4"/>'
                    f'<rect x="3" y="13.5" width="14" height="4" rx="1.5" fill="{ICON_AM}" stroke="{ICON_AM}" stroke-width="1.4"/>',
    "icon-apps": f'<rect x="5" y="1.5" width="10" height="17" rx="2.5" fill="none" stroke="{ICON_TE}" stroke-width="1.4"/>'
                 f'<rect x="7.5" y="11" width="1.8" height="4" rx=".6" fill="{ICON_TE}"/>'
                 f'<rect x="10.7" y="7.5" width="1.8" height="7.5" rx=".6" fill="{ICON_AM}"/>',
}


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"hero-{name}.svg").write_text(build_hero(t), encoding="utf-8")
        (OUT / f"card-ncu-{name}.svg").write_text(build_ncu(t), encoding="utf-8")
        (OUT / f"card-green-{name}.svg").write_text(build_green(t), encoding="utf-8")
    for name, body in ICONS.items():
        (OUT / f"{name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" width="20" height="20" aria-hidden="true">{body}</svg>\n',
            encoding="utf-8")
    print("\n".join(sorted(p.name for p in OUT.glob("*.svg"))))
