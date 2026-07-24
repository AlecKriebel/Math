#!/usr/bin/env python3
"""Generate a deterministic lexicographic catalog/deletion pair list."""

from __future__ import annotations

import argparse
from pathlib import Path

from core_completion_catalog_batch import atomic_write


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--line-start", required=True, type=int)
    parser.add_argument("--line-end", required=True, type=int)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not 1 <= args.line_start <= args.line_end:
        raise SystemExit("invalid catalog line range")
    if args.output.exists():
        raise SystemExit("output already exists")
    raw = "".join(
        f"{line} {deleted}\n"
        for line in range(args.line_start, args.line_end + 1)
        for deleted in range(42)
    ).encode("ascii")
    atomic_write(args.output, raw)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
