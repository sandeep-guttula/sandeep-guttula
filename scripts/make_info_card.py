#!/usr/bin/env python3
"""
Generate a neofetch-style info card SVG with staggered fade-in lines.
Set STATIC=1 to emit a frozen frame for local previews.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

CANVAS_W = 490
CANVAS_H = 420
PAD = 20
TITLEBAR_H = 30
LINE_H = 22

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#e6edf3"

COLORS = {
    "label": "#22d3ee",
    "value": "#e6edf3",
    "accent": "#39d353",
    "warn": "#f2cc60",
    "dim": "#7d8590",
}

ROWS = [
    ("OS", "Linux x86_64", "label", "value"),
    ("Host", "GitHub Profile README", "label", "value"),
    ("Now", "Front End Developer", "label", "accent"),
    ("Prev", "CS Student @ Aditya Engineering", "label", "value"),
    ("Location", "India", "label", "value"),
    ("Stack", "React · React Native · TypeScript", "label", "value"),
    ("", "Next.js · Node · Python · Figma", "dim", "dim"),
    ("Focus", "UI/UX · Responsive Web Apps", "label", "accent"),
    ("Highlights", "Open source enthusiast", "label", "value"),
    ("", "Building with modern JS tooling", "dim", "dim"),
]

STATIC = bool(os.environ.get("STATIC"))
STAGGER = 0.12
DUR = 0.45

css = f"""
@keyframes fadein {{
  0%   {{ opacity: 0; transform: translateX(-8px); }}
  100% {{ opacity: 1; transform: translateX(0); }}
}}
.l {{ opacity: 0; animation: fadein {DUR:.2f}s ease-out both; }}
""".strip()

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f"<style>{css}</style>",
    "<defs>"
    f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
    "</defs>",
    f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
    f'fill="none" stroke="{FRAME}" stroke-width="1"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(
    f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
    f'text-anchor="middle">sandeep@github: ~$ neofetch</text>'
)

logo_y = TITLEBAR_H + 24
parts.append(
    f'<text x="{PAD}" y="{logo_y}" fill="{COLORS["accent"]}" font-size="14" font-weight="700">'
    f"sandeep@github</text>"
)
parts.append(
    f'<text x="{PAD}" y="{logo_y + 18}" fill="{MUTED}" font-size="11">'
    f"────────────────────────────</text>"
)

content_top = logo_y + 36
for i, (label, value, lk, vk) in enumerate(ROWS):
    y = content_top + i * LINE_H
    delay = i * STAGGER
    style = "" if STATIC else f' class="l" style="animation-delay:{delay:.2f}s"'
    if label:
        parts.append(
            f'<text x="{PAD}" y="{y}" font-size="12"{style}>'
            f'<tspan fill="{COLORS[lk]}">{label}</tspan>'
            f'<tspan fill="{MUTED}">: </tspan>'
            f'<tspan fill="{COLORS[vk]}">{value}</tspan></text>'
        )
    else:
        parts.append(
            f'<text x="{PAD + 12}" y="{y}" fill="{COLORS[vk]}" font-size="12"{style}>{value}</text>'
        )

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes)")
