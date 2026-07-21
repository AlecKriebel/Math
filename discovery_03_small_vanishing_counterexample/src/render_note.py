#!/usr/bin/env python3
"""Compile the TeX source into the public PDF with Tectonic."""
from __future__ import annotations
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "symmetric_keller_and_vanishing.tex"
OUT_DIR = ROOT / "output" / "pdf"

def render():
    compiler = shutil.which("tectonic") or "/Users/alec/.local/bin/tectonic"
    if not Path(compiler).exists():
        raise SystemExit("Tectonic is required to build the paper")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [compiler, str(SOURCE), "--outdir", str(OUT_DIR), "--keep-logs"],
        cwd=ROOT,
        check=True,
    )
    print(OUT_DIR / "symmetric_keller_and_vanishing.pdf")

if __name__ == "__main__":
    render()
