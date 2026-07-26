#!/usr/bin/env python3
"""Verify every SHA-256 entry in the reconciliation freeze."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import sys


if not __debug__:
    print("FAIL: assertions are required; do not run with -O", file=sys.stderr)
    raise SystemExit(2)


here = Path(__file__).resolve().parent
text = (here / "FREEZE.md").read_text(encoding="utf-8")
entries = re.findall(r"^([0-9a-f]{64})  (.+)$", text, flags=re.MULTILINE)
assert len(entries) >= 10

for expected, relative in entries:
    path = (here / relative).resolve()
    assert path.is_file(), relative
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == expected, (relative, expected, actual)

print(f"DELTA_GE3_RECONCILIATION_FREEZE_PASS_{len(entries)}_HASHES")
