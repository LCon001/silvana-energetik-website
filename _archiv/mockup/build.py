"""Bettet die Bilder aus mockup/assets/ ein und schreibt das eigenständige mockup-mobile.svg."""
import base64
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "mockup-mobile.src.svg"
OUT = HERE / "mockup-mobile.svg"
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def inline(match):
    path = HERE / match.group(1)
    data = base64.b64encode(path.read_bytes()).decode()
    return f'href="data:{MIME[path.suffix.lower()]};base64,{data}"'


svg = re.sub(r'href="(assets/[^"]+)"', inline, SRC.read_text(encoding="utf-8"))
OUT.write_text(svg, encoding="utf-8")
print(f"{OUT.name}: {OUT.stat().st_size / 1024:.0f} KB")
