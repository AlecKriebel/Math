#!/usr/bin/env python3
"""Write the addition-only subsequence of an ASCII DRAT proof."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()

    additions: list[str] = []
    for raw in args.source.read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if line and not line.startswith("d "):
            additions.append(line)
    args.target.write_text("\n".join(additions) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
