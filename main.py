"""food-picture-01 entry: "Rendang, Slow-Cooked Gold".

Copies the bundled photograph of Indonesian beef rendang -- dark,
caramelised beef slow-cooked for hours in spiced coconut milk until
the sauce reduces to a glossy glaze, served with steamed white
rice -- into the output directory as entry.png.

The picture was prepared during the build: resized to fit inside
1024x1024 with the aspect ratio preserved (never cropped) and kept
under 1 MiB, so this program only copies the bytes and refuses to
run if anything about the file looks wrong.
"""

import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(BASE, "assets", "entry.png")

MAX_FILE_BYTES = 1048576  # 1 MiB, the competition cap
MAX_DIMENSION = 1024  # 1024x1024 pixels, the competition cap
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)

    with open(IMAGE, "rb") as handle:
        blob = handle.read()

    if not blob.startswith(PNG_SIGNATURE):
        fail("assets/entry.png is not a PNG file")
    if len(blob) > MAX_FILE_BYTES:
        fail(f"assets/entry.png is {len(blob)} bytes, over the 1 MiB cap")

    # The IHDR chunk holds the width and height as big-endian
    # unsigned 32-bit integers at byte offsets 16 and 20.
    width = int.from_bytes(blob[16:20], "big")
    height = int.from_bytes(blob[20:24], "big")
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        fail(
            f"assets/entry.png is {width}x{height}, "
            f"over the {MAX_DIMENSION}x{MAX_DIMENSION} cap"
        )

    # A complete PNG ends with the IEND chunk: four zero bytes for
    # the length, the letters IEND, then its CRC. A file without it
    # is truncated, so refuse it.
    if len(blob) < 12 or blob[-12:-8] != b"\x00\x00\x00\x00" or blob[-8:-4] != b"IEND":
        fail("assets/entry.png is truncated: no IEND chunk at the end")

    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(blob)

    # Read the file back and make sure what landed on disk is
    # exactly the bytes we meant to write.
    with open(target, "rb") as handle:
        written = handle.read()
    if written != blob:
        fail("output entry.png does not match the bundled image")


if __name__ == "__main__":
    main()
