#!/usr/bin/env python3
"""Audit terminology and outreach-length requirements in source text."""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Constructed from pieces so the audit source does not contain its own targets.
TARGETS = [
    "F_" + "lit",
    "literal finite" + "-table map",
    "generically non" + "identifiable",
    "Conjecture 4.1" + " is true",
    "the problem" + " statement",
    "the proposed" + " counterexample",
    "the autonomous" + " research program",
    "broad literature" + " was not searched",
    "final technical" + " summary",
    "the original" + " model is wrong",
]
EXTENSIONS = {".tex", ".md", ".txt", ".py", ".json", ".mk", ".yml", ".yaml"}


def text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.name == "Makefile" or path.suffix.lower() in EXTENSIONS:
            yield path


def main(argv: list[str]) -> int:
    root = Path(argv[0] if argv else ".").resolve()
    failures: list[str] = []
    for path in text_files(root):
        text = path.read_text(errors="replace")
        low = text.lower()
        for target in TARGETS:
            if target.lower() in low:
                failures.append(f"{path.relative_to(root)}: prohibited phrase {target!r}")
        # The imprecise shorthand is intentionally eliminated package-wide.
        if re.search(r"\bempty branch\b", low):
            failures.append(f"{path.relative_to(root)}: use 'ancestrally unoccupied branch'")

    email = root / "EMAIL_DRAFT.txt"
    if not email.is_file():
        failures.append("EMAIL_DRAFT.txt: missing")
    else:
        words = re.findall(r"\b[\w'-]+\b", email.read_text())
        if not 200 <= len(words) <= 250:
            failures.append(f"EMAIL_DRAFT.txt: {len(words)} words, expected 200--250")

    if failures:
        print("FAIL wording audit")
        for failure in failures:
            print("  " + failure)
        return 1
    print("PASS wording audit and 200--250-word email length")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
