#!/usr/bin/env python3
"""Strict hash audit for the candidate package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
    for name, expected in manifest["sha256"].items():
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError((name, expected, actual))
    print("QQ1 bow-tie global coupling manifest: VERIFIED")


if __name__ == "__main__":
    main()
