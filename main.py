"""news-image-20261121 entry: sum up Saturday 21 November 2026's world
news in one image.

The entry is a pre-generated newspaper front page ("SATURDAY 21
NOVEMBER 2026") drawn from scratch by gen_image.py (PIL shapes and
text, no photographs, no copied artwork). Its stories, checked
against 21 Nov 2026 reporting (OneTurn's 21 Nov day page, the Majik
Morning Brief evening update for 21 Nov, and the AP wire listings
for that day):

  LEAD  Iran strikes Bahrain: Tehran says it hit two US bases;
        Bahrain reports an industrial site ablaze, no injuries.
  1.    Mexico captures cartel boss "El Chapo Isidro" (FBI
        most-wanted) in Sinaloa; 11 killed in the operation.
  2.    A Russian missile hits Kryvyi Rih, Zelensky's hometown,
        killing a boy aged 7 and a paramedic; a Russian cargo ship,
        Sparta II, burns in the Gulf of Finland after a drone strike.
  3.    Trump, Xi and Putin meet in Shenzhen and agree to open
        nuclear risk-reduction talks; Zelensky calls Putin a killer.
  4.    COP31 in Antalya runs past its deadline; the final draft
        does not mention fossil fuels, and a deal is close late
        on Saturday.
  MARKETS  AI sell-off: the Nasdaq erases its 2026 gains in its
        worst week since March 2020; the S&P 500 and Dow enter
        correction territory.
  Bottom strip: Wolbachia mosquitoes cut dengue in Brazilian
        children by about 69%; BepiColombo reaches Mercury orbit;
        the UN court finds Myanmar responsible for the Rohingya
        genocide; the EU and Indonesia sign a trade deal; 24 die
        in a Nigeria boat capsize; Bolsonaro in intensive care;
        GTA VI earns $3.8bn on its first day.

This program validates the checked artwork (art.jpg, beside this
file) against the competition's caps and copies it to the output
directory as entry.png. The rules tell PNG from JPEG by the file's
first bytes, so the name stays entry.png while the bytes stay JPEG.

Python 3.13 standard library only. No network. Deterministic: the
output is a byte-for-byte copy of art.jpg.
"""

import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1_048_576   # the rules cap the output at 1 MiB
MAX_SIDE = 1024         # and at 1024 x 1024 pixels
ARTWORK = "art.jpg"
OUT_NAME = "entry.png"

# JPEG markers with no length field (SOI, EOI, TEM, RST0-7).
NO_LENGTH = {0x01, 0xD8, 0xD9} | set(range(0xD0, 0xD8))
# Start-of-frame markers: their segment carries width and height.
SOF_MARKERS = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
               0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}


def read_jpeg_size(path):
    """Return (width, height) from a JPEG start-of-frame segment."""
    with open(path, "rb") as fh:
        if fh.read(2) != b"\xff\xd8":
            raise ValueError("not a JPEG: missing start-of-image marker")
        while True:
            head = fh.read(2)
            if len(head) < 2 or head[0] != 0xFF:
                raise ValueError("not a JPEG: bad segment header")
            marker = head[1]
            if marker in NO_LENGTH:
                if marker == 0xD9:
                    break
                continue
            raw = fh.read(2)
            if len(raw) < 2:
                raise ValueError("not a JPEG: truncated segment")
            seg_len = struct.unpack(">H", raw)[0]
            if marker in SOF_MARKERS:
                fh.read(1)  # sample precision byte
                height, width = struct.unpack(">HH", fh.read(4))
                return width, height
            fh.seek(seg_len - 2, os.SEEK_CUR)
    raise ValueError("not a JPEG: no start-of-frame segment found")


def is_whole_jpeg(path):
    """True when the file ends with the JPEG end-of-image marker."""
    with open(path, "rb") as fh:
        fh.seek(-2, os.SEEK_END)
        return fh.read(2) == b"\xff\xd9"


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ARTWORK)
    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR")
               or os.environ.get("MAKEFUN_OUTPUT")
               or "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, OUT_NAME)

    nbytes = os.path.getsize(src)
    if not 0 < nbytes <= MAX_BYTES:
        print(f"error: {ARTWORK} is {nbytes} bytes, "
              f"outside 1..{MAX_BYTES}", file=sys.stderr)
        return 1
    try:
        width, height = read_jpeg_size(src)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"error: {ARTWORK} is {width}x{height}, "
              f"over the {MAX_SIDE}x{MAX_SIDE} cap", file=sys.stderr)
        return 1
    if not is_whole_jpeg(src):
        print(f"error: {ARTWORK} has no end-of-image marker",
              file=sys.stderr)
        return 1
    print(f"checked {ARTWORK}: {width}x{height}, {nbytes} bytes")

    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != nbytes:
        print("error: the copy's size differs from the artwork",
              file=sys.stderr)
        return 1
    with open(src, "rb") as a, open(dst, "rb") as b:
        if hashlib.sha256(a.read()).digest() != hashlib.sha256(b.read()).digest():
            print("error: the copy's bytes differ from the artwork",
                  file=sys.stderr)
            return 1
    print(f"wrote {dst}: {nbytes} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
