#!/usr/bin/env python3
"""Compile the Ramsey endpoint-capacity note with Tectonic."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "ramsey55_endpoint_capacity.tex"
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
    print(OUTPUT / "ramsey55_endpoint_capacity.pdf")


if __name__ == "__main__":
    main()
