"""見出し画像（1280x670）を作る。
使い方: python3 eyecatch.py 出力.png ポーズ名 "タイトル1行目|タイトル2行目" [上ラベル] [下ラベル]
ポーズ名は cut/ フォルダのファイル名（拡張子なし）。例: 10_calendar
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H = 1280, 670
FONT_B = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_M = '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc'
NAVY_TOP = (14, 27, 51)
GREEN_BOTTOM = (16, 52, 46)
ACCENT = (126, 200, 150)   # テンプレートの緑の文字色に近い色


def background():
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]
    t = np.clip(0.55 * y + 0.45 * x, 0, 1)[..., None]
    top = np.array(NAVY_TOP)[None, None, :]
    bot = np.array(GREEN_BOTTOM)[None, None, :]
    arr = (top * (1 - t) + bot * t).astype(np.uint8)
    img = Image.fromarray(arr, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(img, 'RGBA')
    # うすい斜線とドット（テンプレートの雰囲気）
    for k in range(-H, W, 30):
        d.line([(k, H), (k + H, 0)], fill=(255, 255, 255, 5), width=1)
    for gx in range(40, 420, 18):
        for gy in range(560, 650, 18):
            d.ellipse([gx, gy, gx + 3, gy + 3], fill=(126, 200, 150, 60))
    return img


def fit_title(draw, lines, max_w, start=78, min_size=44):
    size = start
    while size >= min_size:
        f = ImageFont.truetype(FONT_B, size, index=0)
        if all(draw.textlength(l, font=f) <= max_w for l in lines):
            return f, size
        size -= 2
    return ImageFont.truetype(FONT_B, min_size, index=0), min_size


def make(out, pose, title, label='補助金 採択後の実務', sub='2026年度 最新版'):
    img = background()
    d = ImageDraw.Draw(img, 'RGBA')
    # 右側の白い円（キャラクターの台）
    cx, cy, r = 1010, 420, 300
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(244, 247, 250, 255))
    # キャラクター
    ch = Image.open(f'poses/{pose}.png').convert('RGBA')
    target_h = 560
    scale = target_h / ch.height
    ch = ch.resize((int(ch.width * scale), target_h), Image.LANCZOS)
    if ch.width > 470:
        s2 = 470 / ch.width
        ch = ch.resize((470, int(ch.height * s2)), Image.LANCZOS)
    x = cx - ch.width // 2
    y = H - ch.height
    # 円の外にはみ出した部分も見えるよう、白い縁取りを付ける
    a = ch.split()[3]
    halo = a.filter(ImageFilter.MaxFilter(9))
    halo_img = Image.new('RGBA', ch.size, (244, 247, 250, 0))
    halo_img.putalpha(halo)
    img.alpha_composite(halo_img, (x, y))
    img.alpha_composite(ch, (x, y))
    # 文字（左側）
    left, max_w = 64, 640
    f_label = ImageFont.truetype(FONT_M, 30, index=0)
    d.text((left, 150), label, font=f_label, fill=ACCENT + (255,))
    d.line([(left, 206), (left + 60, 206)], fill=ACCENT + (255,), width=4)
    lines = title.split('|')
    f_title, size = fit_title(d, lines, max_w)
    line_h = int(size * 1.35)
    ty = 232 + max(0, (3 - len(lines))) * line_h // 2
    for i, l in enumerate(lines):
        d.text((left, ty + i * line_h), l, font=f_title, fill=(255, 255, 255, 255))
    f_sub = ImageFont.truetype(FONT_M, 28, index=0)
    d.text((left, ty + len(lines) * line_h + 24), sub, font=f_sub, fill=(220, 228, 236, 255))
    img.convert('RGB').save(out)


if __name__ == '__main__':
    args = sys.argv[1:]
    make(*args)
