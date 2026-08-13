#!/usr/bin/env python3
"""Build a deterministic hash manifest for this package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha256(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    ignored = {"MANIFEST.sha256"}
    files = [path for path in HERE.rglob("*")
             if path.is_file() and path.name not in ignored and
             "__pycache__" not in path.parts]
    rows = [f"{sha256(path)}  {path.relative_to(HERE)}"
            for path in sorted(files, key=lambda item: str(item.relative_to(HERE)))]
    (HERE / "MANIFEST.sha256").write_text("\n".join(rows) + "\n")
    print(f"manifest rows: {len(rows)}")


if __name__ == "__main__":
    main()
