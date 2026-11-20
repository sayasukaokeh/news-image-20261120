"""Front-page entry for Friday 20 November 2026.

The finished page lives in this repository as assets/entry.png
("THE WORLD" front page: Trump-Xi-Putin peace declaration in Shenzhen,
ICJ genocide ruling on Myanmar, Anthropic's record IPO, the Kerch Bridge
strike, and the day's other top stories). This program only copies those
exact bytes to /output/entry.png, so every run produces the same file.
It reads nothing from the network and uses no clock or random data.
"""

import hashlib
import os
import shutil
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
FINISHED_PAGE = REPO_DIR / "assets" / "entry.png"
MAX_BYTES = 1_048_576


def _digest(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            block = stream.read(65536)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def main():
    if not FINISHED_PAGE.is_file():
        raise FileNotFoundError(f"finished front page missing: {FINISHED_PAGE}")
    if FINISHED_PAGE.stat().st_size > MAX_BYTES:
        raise ValueError("finished front page is over the 1 MiB limit")
    with open(FINISHED_PAGE, "rb") as stream:
        if stream.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ValueError("finished front page is not a PNG file")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    written = output_dir / "entry.png"
    shutil.copyfile(FINISHED_PAGE, written)
    if _digest(written) != _digest(FINISHED_PAGE):
        raise ValueError("written entry.png differs from the finished page")


if __name__ == "__main__":
    main()
