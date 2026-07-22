#!/usr/bin/env python3
"""Compile the unified Discovery 07 paper with Tectonic."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "unified_consequences.tex"
OUTPUT = HERE / "output" / "pdf"


def main() -> None:
    compiler = shutil.which("tectonic") or "/opt/homebrew/bin/tectonic"
    if not Path(compiler).exists():
        raise SystemExit("Tectonic is required to build the paper")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [compiler, str(SOURCE), "--outdir", str(OUTPUT), "--keep-logs"],
        cwd=HERE,
        check=True,
    )
    print(OUTPUT / "unified_consequences.pdf")


if __name__ == "__main__":
    main()
