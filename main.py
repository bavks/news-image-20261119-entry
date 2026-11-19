#!/usr/bin/env python3
"""make.fun entry: "Sum up 19 November's world news in one image".

The repository commits the finished front page as entry.png (drawn and
typeset by render_image.py).  This program's whole job is to deliver
those exact bytes to the grader: it copies entry.png into the output
directory -- $MAKEFUN_OUTPUT_DIR when set, otherwise /output -- using
only the standard library, with no network, so every run produces a
byte-identical file.
"""

import os
import shutil
from pathlib import Path


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    target = output_dir() / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
