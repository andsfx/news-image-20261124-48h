#!/usr/bin/env python3
"""Copy the prebuilt entry image into the directory chosen by the harness."""

import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DESTINATION_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    """Create the output folder and place a byte-identical copy of entry.png."""
    DESTINATION_DIR.mkdir(parents=True, exist_ok=True)
    target = DESTINATION_DIR / "entry.png"
    shutil.copyfile(SOURCE, target)
    target.chmod(0o644)


if __name__ == "__main__":
    main()
