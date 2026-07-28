#!/usr/bin/env python3
"""Check the immutable candidate package manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "CANDIDATE_MANIFEST.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema") != "adjacent-pair-repair-dichotomy-manifest-v1":
        raise AssertionError("wrong manifest schema")
    expected = data.get("files")
    if not isinstance(expected, dict) or not expected:
        raise AssertionError("manifest has no file table")
    actual = {name: digest(HERE / name) for name in sorted(expected)}
    if actual != expected:
        raise AssertionError(
            "manifest mismatch\n"
            f"expected={json.dumps(expected, sort_keys=True)}\n"
            f"actual={json.dumps(actual, sort_keys=True)}"
        )
    print("Adjacent-pair repair candidate manifest: VERIFIED")


if __name__ == "__main__":
    main()
