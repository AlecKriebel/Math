#!/usr/bin/env python3
"""Check the hostile-review artifact manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "REVIEW_MANIFEST.json"


def digest(path: Path) -> str:
    checksum = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            checksum.update(block)
    return checksum.hexdigest()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["verdict"] != "UNCONDITIONAL_PASS":
        raise AssertionError("review verdict changed")
    for relative, expected in manifest["files_sha256"].items():
        actual = digest(HERE / relative)
        if actual != expected:
            raise AssertionError(
                f"{relative}: expected {expected}, obtained {actual}"
            )
    print("QQ1 anchor-auxiliary hostile review manifest: VERIFIED")


if __name__ == "__main__":
    main()
