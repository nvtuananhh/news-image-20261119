#!/usr/bin/env python3
"""Entry point for the news-image-20261119 competition.

Copies the pre-rendered poster (poster.png, produced deterministically
by gen_poster.py) to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).

Standard library only. No network, no randomness, no timestamps:
running this twice produces byte-identical output.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "poster.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
