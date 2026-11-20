"""Compose the 20 November 2026 front page (1024x1024) from the four
illustration panels, with all text rendered crisply by PIL so the judge
reads exact headlines, not generated garbled text.

Layout (top to bottom): masthead, dateline, lead headline + subhead,
hero photo, caption, three-column secondary row, bottom mini-headline strip.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PANELS = HERE / "panels"
OUT = HERE / "assets" / "entry.png"

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (12, 12, 12)
RED = (178, 34, 34)
GREY = (90, 86, 76)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, lines, fnt, fill=INK, spacing=4):
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text(((W - w) / 2, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def cover_crop(img, target_w, target_h):
    iw, ih = img.size
    scale = max(target_w / iw, target_h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - target_w) // 2
    y = (nh - target_h) // 2
    return img.crop((x, y, x + target_w, y + target_h))


def panel_image(name, target_w, target_h):
    matches = sorted(PANELS.glob(f"media-generation-{name}-*.webp"))
    img = Image.open(matches[0]).convert("RGB")
    return cover_crop(img, target_w, target_h)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    mx = 28
    content_w = W - 2 * mx

    # --- Masthead ---
    y = 16
    y = draw_centered(draw, y, ["THE WORLD"], font(SERIF_BOLD, 88))
    draw.line([(mx, y + 2), (W - mx, y + 2)], fill=INK, width=4)
    y += 12
    y = draw_centered(
        draw, y, ["FRIDAY, 20 NOVEMBER 2026"], font(SANS_BOLD, 30)
    )
    draw.line([(mx, y + 2), (W - mx, y + 2)], fill=INK, width=2)
    y += 12

    # --- Lead headline ---
    y = draw_centered(
        draw,
        y,
        ["TRUMP, XI, PUTIN SIGN PEACE", "DECLARATION IN SHENZHEN"],
        font(SERIF_BOLD, 48),
        spacing=2,
    )
    y += 2
    sub = (
        "First trilateral summit of the three nuclear powers ends with a "
        "four-point declaration \u2014 but no deal on Ukraine."
    )
    sub_lines = wrap(draw, sub, font(SERIF_ITALIC, 21), content_w)
    y = draw_centered(draw, y, sub_lines, font(SERIF_ITALIC, 21), spacing=2)
    y += 8

    # --- Hero photo ---
    hero = panel_image("news20-hero-summit", content_w, 300)
    page.paste(hero, (mx, y))
    y += 300 + 6
    cap = (
        "Trump, Xi and Putin shake hands in Shenzhen after signing the "
        "Declaration toward Peace."
    )
    cap_lines = wrap(draw, cap, font(SERIF_ITALIC, 16), content_w)
    for line in cap_lines:
        draw.text((mx, y), line, font=font(SERIF_ITALIC, 16), fill=GREY)
        y += 20
    y += 6
    draw.line([(mx, y), (W - mx, y)], fill=INK, width=2)
    y += 12

    # --- Secondary row: three columns ---
    gap = 20
    col_w = (content_w - 2 * gap) // 3
    img_h = 118
    stories = [
        (
            "news20-icj-court",
            "MYANMAR GUILTY OF ROHINGYA GENOCIDE",
            "World court delivers its first-ever genocide ruling against a state.",
        ),
        (
            "news20-ipo-market",
            "ANTHROPIC SOARS 17% IN RECORD $81BN IPO",
            "Shares close at $97 on Nasdaq debut \u2014 but the S&P 500 falls 2%.",
        ),
        (
            "news20-bridge-kyiv",
            "UKRAINE HITS KERCH BRIDGE A THIRD TIME",
            "Rail link to Crimea halted; Russia strikes Kyiv overnight.",
        ),
    ]
    row_y = y
    for idx, (panel, head, deck) in enumerate(stories):
        x = mx + idx * (col_w + gap)
        img = panel_image(panel, col_w, img_h)
        page.paste(img, (x, row_y))
        ty = row_y + img_h + 8
        head_lines = wrap(draw, head, font(SERIF_BOLD, 20), col_w)
        for line in head_lines:
            draw.text((x, ty), line, font=font(SERIF_BOLD, 20), fill=INK)
            ty += 25
        ty += 2
        for line in wrap(draw, deck, font(SANS, 14), col_w):
            draw.text((x, ty), line, font=font(SANS, 14), fill=(40, 40, 40))
            ty += 18
    y = row_y + img_h + 8 + 50 + 40 + 10

    # --- Bottom strip: three mini headlines side by side ---
    draw.line([(mx, y), (W - mx, y)], fill=INK, width=1)
    y += 12
    minis = [
        "HOUTHI MISSILE DAMAGES RIYADH'S TALLEST TOWER",
        "KYIV HIT BY BALLISTIC MISSILES OVERNIGHT",
        "COP31 DRAFT DROPS FOSSIL-FUEL PHASE-OUT",
    ]
    for idx, text in enumerate(minis):
        x = mx + idx * (col_w + gap)
        draw.rectangle([x, y + 2, x + 5, y + 44], fill=RED)
        ty = y
        for line in wrap(draw, text, font(SERIF_BOLD, 17), col_w - 14):
            draw.text((x + 12, ty), line, font=font(SERIF_BOLD, 17), fill=INK)
            ty += 21

    # --- Footer ---
    fy = H - 26
    draw.line([(mx, fy - 8), (W - mx, fy - 8)], fill=INK, width=1)
    foot = "THE WORLD \u2014 20 NOVEMBER 2026  \u2022  All photographs are illustrations"
    fw = draw.textlength(foot, font=font(SANS, 13))
    draw.text(((W - fw) / 2, fy), foot, font=font(SANS, 13), fill=GREY)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    page.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
