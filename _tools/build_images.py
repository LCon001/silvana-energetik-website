"""Erzeugt alle Bilder der Website in assets/img/ aus den Quellfotos in _archiv/.

Aufruf (im Projektordner):  python3 _tools/build_images.py
Benötigt: Pillow (pip install pillow)
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
KI = ROOT / "_archiv" / "fotos-ki-optimiert"
ORIGINAL = ROOT / "_archiv" / "fotos-original"
OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

CREAM = (255, 252, 249)
ROSE_LIGHT = (255, 238, 230)

# Name im Web -> (Quelldatei, Gamma, Rosé-Anteil)
PHOTOS = {
    "silvana-workshop": ("Silvana bei einem Workshop optimiert (KI).jpg", 0.96, 0.05),
    "behandlungsraum": ("Behandlungsraum optimiert dezent (KI).jpg", 0.98, 0.03),
    "behandlungsraum-stark": ("Behandlungsraum optimiert (KI).jpg", 0.96, 0.03),
    "fussanwendung": ("Fußanwendung Fußsohlen optimiert (KI).jpg", 0.96, 0.05),
    "koerperkerzen-sirona": ("Körperkerzen mit Sirona Essenzen optimiert (KI).jpg", 0.96, 0.05),
    "workshop-koerperkerzen": ("Workshop Körperkerzen optimiert (KI).jpg", 0.96, 0.05),
    "fuesse-im-bach": ("Füße im Bach optimiert (KI).jpg", 0.72, 0.08),
    "babyfuesse": ("Fußanwendung Babyfüße optimiert (KI).jpg", 0.96, 0.05),
    "sprays": ("Sprays und Körperkerzen optimiert (KI).jpg", 0.96, 0.05),
    "koerperkerze-kind": ("Körperkerzenbehandlung Kind optimiert (KI).jpg", 0.8, 0.07),
    "kinderfuesse": ("Fußanwendung Kinderfüße optimiert (KI).jpg", 0.96, 0.05),
    "fussanwendung-kunde": ("Fußanwendung Kunde optimiert (KI).jpg", 0.96, 0.05),
}
WIDTHS = (480, 960, 1400)


def grade(im, gamma, tint):
    """Einheitlicher Website-Look: Schatten leicht anheben und einen Hauch Rosé-Wärme."""
    lut = [round(255 * (i / 255) ** gamma) for i in range(256)]
    im = im.point(lut * 3)
    return Image.blend(im, Image.new("RGB", im.size, ROSE_LIGHT), tint)


def white_to_alpha(im):
    im = im.convert("RGB")
    px = im.load()
    out = Image.new("RGBA", im.size)
    opx = out.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            a = 255 - min(r, g, b)
            if a < 8:
                opx[x, y] = (255, 255, 255, 0)
                continue
            f = 255 / a
            opx[x, y] = tuple(
                max(0, min(255, round(255 - (255 - c) * f))) for c in (r, g, b)
            ) + (a,)
    return out


def on_background(im, size, bg=CREAM, scale=0.8):
    canvas = Image.new("RGBA", size, bg + (255,))
    fit = im.copy()
    fit.thumbnail((int(size[0] * scale), int(size[1] * scale)), Image.LANCZOS)
    canvas.alpha_composite(fit, ((size[0] - fit.width) // 2, (size[1] - fit.height) // 2))
    return canvas.convert("RGB")


def build_photos():
    for name, (src, gamma, tint) in PHOTOS.items():
        im = grade(Image.open(KI / src).convert("RGB"), gamma, tint)
        widths = sorted({min(w, im.width) for w in WIDTHS})
        for w in widths:
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).save(OUT / f"{name}-{w}.webp", quality=78, method=6)
        print(f"{name}: {widths}  ({im.width}x{im.height})")


def build_logo():
    src = Image.open(ORIGINAL / "Logo Silvana Liebhart (korrigiert).png").convert("RGB")
    logo = white_to_alpha(src.crop((160, 170, 1882, 1892)).resize((900, 900), Image.LANCZOS))
    logo.save(OUT / "logo.webp", quality=90, method=6)
    logo.resize((600, 600), Image.LANCZOS).save(OUT / "logo-600.webp", quality=90, method=6)

    tree = white_to_alpha(src.crop((770, 275, 1290, 960)).resize((240, 316), Image.LANCZOS))
    tree.save(OUT / "logo-baum.webp", quality=90, method=6)
    tree.resize((120, 158), Image.LANCZOS).save(OUT / "logo-baum.png", optimize=True)

    tree_icon = white_to_alpha(src.crop((700, 230, 1360, 960)))
    for size, name in ((32, "favicon-32.png"), (192, "icon-192.png")):
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        fit = tree_icon.copy()
        fit.thumbnail((size, size), Image.LANCZOS)
        canvas.alpha_composite(fit, ((size - fit.width) // 2, (size - fit.height) // 2))
        canvas.save(OUT / name, optimize=True)
    on_background(tree_icon, (180, 180), scale=0.78).save(OUT / "apple-touch-icon.png", optimize=True)

    og = Image.new("RGBA", (1200, 630), (251, 240, 236, 255))
    fit = logo.copy()
    fit.thumbnail((560, 560), Image.LANCZOS)
    og.alpha_composite(fit, ((1200 - fit.width) // 2, (630 - fit.height) // 2))
    og.convert("RGB").save(OUT / "og-image.jpg", quality=85, optimize=True)
    print("Logo, Favicons und og-image erstellt")


if __name__ == "__main__":
    build_photos()
    build_logo()
