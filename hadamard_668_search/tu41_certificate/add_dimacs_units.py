#!/usr/bin/env python3
"""Copy a DIMACS CNF and append deterministic unit clauses.

This tiny utility is used to make independently checkable cube/shard CNFs.
It changes only the declared clause count and appends the requested literals.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("literals", nargs="+", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if any(literal == 0 for literal in args.literals):
        raise SystemExit("unit literals must be nonzero")

    with args.input.open("rb") as source:
        header = source.readline().decode("ascii").strip().split()
        if len(header) != 4 or header[:2] != ["p", "cnf"]:
            raise SystemExit("expected DIMACS 'p cnf VARIABLES CLAUSES' header")
        variables = int(header[2])
        clauses = int(header[3])
        if any(abs(literal) > variables for literal in args.literals):
            raise SystemExit("unit literal exceeds declared variable count")

        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("wb") as destination:
            destination.write(
                f"p cnf {variables} {clauses + len(args.literals)}\n".encode("ascii")
            )
            while block := source.read(1 << 20):
                destination.write(block)
            for literal in args.literals:
                destination.write(f"{literal} 0\n".encode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
