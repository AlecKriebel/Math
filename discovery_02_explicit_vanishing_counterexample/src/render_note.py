#!/usr/bin/env python3
"""Compile the arXiv-ready TeX source into the public PDF."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "explicit_vanishing_counterexample.tex"
OUT_DIR = ROOT / "output" / "pdf"


def render() -> None:
    compiler = shutil.which("tectonic")
    if compiler is None:
        raise SystemExit(
            "tectonic is required to build the paper; install it with "
            "`brew install tectonic` or your package manager"
        )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [compiler, str(SOURCE), "--outdir", str(OUT_DIR), "--keep-logs"],
        cwd=ROOT,
        check=True,
    )
    print(OUT_DIR / "explicit_vanishing_counterexample.pdf")


if __name__ == "__main__":
    render()
