#!/usr/bin/env python3
"""Generate the release SHA-256 manifest in deterministic path order."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"
IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "tmp"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def included(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if path == MANIFEST or not path.is_file():
        return False
    if any(part in IGNORED_PARTS for part in rel.parts):
        return False
    if path.suffix in IGNORED_SUFFIXES or path.name == ".DS_Store":
        return False
    return True


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    paths = sorted((p for p in ROOT.rglob("*") if included(p)), key=lambda p: p.relative_to(ROOT).as_posix())
    body = "".join(f"{digest(path)}  {path.relative_to(ROOT).as_posix()}\n" for path in paths)
    MANIFEST.write_text(body, encoding="utf-8")
    print(f"WROTE {MANIFEST} ({len(paths)} files)")


if __name__ == "__main__":
    main()
