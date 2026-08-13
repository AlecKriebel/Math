#!/usr/bin/env python3
"""Verify exact proof-note bytes before building the technical supplement."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path


PUBLICATION = Path(__file__).resolve().parent
PROJECT = PUBLICATION.parent
MANIFEST = PUBLICATION / "supplement-manifest.txt"


def main() -> None:
    checked = 0
    for raw_line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not raw_line or raw_line.startswith("#"):
            continue
        index, source, expected, _title = raw_line.split("|", 3)
        path = PROJECT / source
        actual = sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(
                f"supplement hash mismatch for {index} {source}: "
                f"expected {expected}, found {actual}"
            )
        checked += 1
    if checked == 0:
        raise SystemExit("empty supplement manifest")
    print(f"verified {checked} exact proof-note files")


if __name__ == "__main__":
    main()
