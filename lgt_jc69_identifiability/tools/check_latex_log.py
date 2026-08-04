#!/usr/bin/env python3
"""Fail on LaTeX diagnostics that compromise an author-facing PDF."""
from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = {
    "overfull box": re.compile(r"Overfull \\[hv]box"),
    "undefined reference": re.compile(r"undefined references?|Reference .* undefined", re.I),
    "undefined citation": re.compile(r"Citation .* undefined|undefined citations?", re.I),
    "missing file": re.compile(r"LaTeX Error: File .* not found", re.I),
    "fatal error": re.compile(r"Fatal error occurred|Emergency stop", re.I),
}


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: check_latex_log.py LOG ...", file=sys.stderr)
        return 2
    failures: list[str] = []
    for name in argv:
        path = Path(name)
        if not path.is_file():
            failures.append(f"{name}: log missing")
            continue
        text = path.read_text(errors="replace")
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{name}: {label}")
    if failures:
        print("FAIL LaTeX log audit")
        for item in failures:
            print("  " + item)
        return 1
    print("PASS LaTeX logs: no overfull boxes, undefined references/citations, or fatal diagnostics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
