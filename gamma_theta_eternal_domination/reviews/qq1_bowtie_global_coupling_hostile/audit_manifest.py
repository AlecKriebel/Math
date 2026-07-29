#!/usr/bin/env python3
"""Verify the immutable hostile-review manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
    for relative, expected in manifest["sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(
                f"hash mismatch for {relative}: {actual} != {expected}"
            )
    print("QQ1 global-coupling hostile-review manifest: VERIFIED")


if __name__ == "__main__":
    main()
