"""Erzeugt zugeschnittene, web-optimierte Bilder für das Mockup in mockup/assets/."""
from pathlib import Path

from PIL import Image

ARCHIV = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(exist_ok=True)


class _Sources:
    def __truediv__(self, name):
        for folder in ("fotos-ki-optimiert", "fotos-original"):
            if (ARCHIV / folder / name).exists():
                return ARCHIV / folder / name
        raise FileNotFoundError(name)


ROOT = _Sources()


def white_to_alpha(im):
    im = im.convert("RGB")
    px = im.load()
    w, h = im.size
    out = Image.new("RGBA", im.size)
    opx = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            a = 255 - min(r, g, b)
            if a < 8:
                opx[x, y] = (255, 255, 255, 0)
                continue
            f = 255 / a
            opx[x, y] = tuple(
                max(0, min(255, int(round(255 - (255 - c) * f)))) for c in (r, g, b)
            ) + (a,)
    return out


ROSE_LIGHT = (255, 238, 230)


def grade(im, gamma=0.96, tint=0.05):
    """Einheitlicher Website-Look: Schatten leicht anheben und einen Hauch Rosé-Wärme."""
    lut = [round(255 * (i / 255) ** gamma) for i in range(256)]
    im = im.point(lut * 3)
    return Image.blend(im, Image.new("RGB", im.size, ROSE_LIGHT), tint)


def crop_to(src, box, size, name, gamma=0.96, tint=0.05, quality=80):
    im = Image.open(ROOT / src).convert("RGB")
    if box:
        im = im.crop(box)
    im = grade(im.resize(size, Image.LANCZOS), gamma, tint)
    im.save(OUT / name, quality=quality, optimize=True, progressive=True)


logo = Image.open(ROOT / "Logo Silvana Liebhart.jpeg").crop((160, 170, 1882, 1892))
white_to_alpha(logo.resize((680, 680), Image.LANCZOS)).save(OUT / "logo.png", optimize=True)

tree = Image.open(ROOT / "Logo Silvana Liebhart.jpeg").crop((770, 275, 1290, 960))
white_to_alpha(tree.resize((120, 158), Image.LANCZOS)).save(OUT / "logo-baum.png", optimize=True)

# Quellen sind die KI-optimierten Fotos; Bildformate jeweils 2x der Darstellungsgröße im Mockup
crop_to("Silvana bei einem Workshop optimiert (KI).jpg", (216, 202, 763, 691), (684, 612), "silvana.jpg")
crop_to("Behandlungsraum optimiert (KI).jpg", None, (684, 512), "raum.jpg", tint=0.03)
crop_to("Fußanwendung Fußsohlen optimiert (KI).jpg", (0, 130, 1152, 736), (684, 360), "fuss.jpg")
crop_to("Körperkerzen mit Sirona Essenzen optimiert (KI).jpg", (140, 0, 1166, 720), (684, 480), "kerzen.jpg")
crop_to("Workshop Körperkerzen optimiert (KI).jpg", (0, 274, 864, 729), (684, 360), "workshop.jpg")
crop_to("Füße im Bach optimiert (KI).jpg", (250, 0, 898, 864), (300, 400), "galerie-bach.jpg", gamma=0.72, tint=0.08)
crop_to("Fußanwendung Babyfüße optimiert (KI).jpg", None, (300, 400), "galerie-kinderfuesse.jpg")
crop_to("Sprays und Körperkerzen optimiert (KI).jpg", None, (300, 400), "galerie-sprays.jpg")
crop_to("Körperkerzenbehandlung Kind optimiert (KI).jpg", None, (300, 400), "galerie-kerze-kind.jpg", gamma=0.8, tint=0.07)

print("Assets erstellt:", sorted(p.name for p in OUT.iterdir()))
