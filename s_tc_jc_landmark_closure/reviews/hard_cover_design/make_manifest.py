#!/usr/bin/env python3
"""Create or verify the hard-cover design review manifest."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


SKIP = {"MANIFEST.sha256"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_lines(root: Path) -> list[str]:
    lines = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative in SKIP:
            continue
        lines.append(f"{sha256(path)}  {relative}")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("choose exactly one of --write or --check")
    root = Path(__file__).resolve().parent
    path = root / "MANIFEST.sha256"
    text = "\n".join(manifest_lines(root)) + "\n"
    if args.write:
        path.write_text(text)
        print(f"wrote {path}")
        return 0
    if not path.is_file():
        raise SystemExit("MANIFEST.sha256 is missing")
    current = path.read_text()
    if current != text:
        raise SystemExit("MANIFEST.sha256 is stale")
    print("MANIFEST.sha256 OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
