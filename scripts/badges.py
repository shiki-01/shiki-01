"""README 用のバッジ（紺の単色・角丸）を assets/badges/ に生成する。

使い方:
    npm pack simple-icons && tar xzf simple-icons-*.tgz   # アイコン集を取得（package/icons/ に展開される）
    python3 scripts/badges.py package/icons

- バッジを追加するときは BADGES に (出力名, 表示文字, アイコン) を足して再実行する
- アイコンは Simple Icons の slug か、リポジトリ内の SVG ファイルのパス（.svg で終わるもの）
- 文字幅の計測に DejaVu Sans を使う（textLength で幅を固定するので、表示側のフォントが違っても崩れない）
"""

import os
import re
import sys

from PIL import ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "badges")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BG = "#153f63"
FG = "#ffffff"

BADGES = [
    ("portfolio", "shiki-01.com", "assets/badges/icons/shiki.svg"),
    ("github", "@shiki-01", "github"),
    ("sponsor", "Sponsor", "githubsponsors"),
    ("typescript", "TypeScript", "typescript"),
    ("rust", "Rust", "rust"),
    ("csharp", "C#", "dotnet"),
    ("svelte", "Svelte", "svelte"),
    ("tauri", "Tauri", "tauri"),
    ("bun", "Bun", "bun"),
    ("cloudflare", "Cloudflare", "cloudflare"),
    ("unity", "Unity", "unity"),
    ("blender", "Blender", "blender"),
]


def load_icon(icon, icons_dir):
    path = os.path.join(ROOT, icon) if icon.endswith(".svg") else os.path.join(icons_dir, f"{icon}.svg")
    svg = open(path, encoding="utf-8").read()
    view_box = re.search(r'viewBox="([^"]+)"', svg).group(1)
    paths = re.findall(r'<path[^>]*\sd="([^"]+)"', svg)
    return view_box, paths


def render(label, view_box, paths, font):
    text_w = round(font.getlength(label))
    h, icon_x, icon_s, gap, pad = 20, 6, 14, 5, 7
    text_x = icon_x + icon_s + gap
    w = text_x + text_w + pad
    body = "".join(f'<path fill="{FG}" d="{d}"/>' for d in paths)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">\n'
        f"<title>{label}</title>\n"
        f'<rect width="{w}" height="{h}" rx="5" fill="{BG}"/>\n'
        f'<svg x="{icon_x}" y="3" width="{icon_s}" height="{icon_s}" viewBox="{view_box}">{body}</svg>\n'
        f'<text x="{text_x}" y="14" fill="{FG}" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11" '
        f'textLength="{text_w}" lengthAdjust="spacingAndGlyphs">{label}</text>\n'
        "</svg>\n"
    )


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python3 scripts/badges.py <simple-icons の icons ディレクトリ>")
    icons_dir = sys.argv[1]
    font = ImageFont.truetype(FONT, 11)
    os.makedirs(OUT, exist_ok=True)
    for name, label, icon in BADGES:
        view_box, paths = load_icon(icon, icons_dir)
        with open(os.path.join(OUT, f"{name}.svg"), "w", encoding="utf-8") as f:
            f.write(render(label, view_box, paths, font))
        print(f"{name}.svg")


if __name__ == "__main__":
    main()
