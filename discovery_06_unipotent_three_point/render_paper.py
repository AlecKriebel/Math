#!/usr/bin/env python3
"""Compile the Discovery 06 paper with Tectonic."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "unipotent_three_point.tex"
OUTPUT = ROOT / "output" / "pdf"


def main() -> None:
    compiler = shutil.which("tectonic") or "/opt/homebrew/bin/tectonic"
    if not Path(compiler).exists():
        raise SystemExit("Tectonic is required to build the paper")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [compiler, str(SOURCE), "--outdir", str(OUTPUT), "--keep-logs"],
        cwd=ROOT,
        check=True,
    )
    print(OUTPUT / "unipotent_three_point.pdf")


if __name__ == "__main__":
    main()
