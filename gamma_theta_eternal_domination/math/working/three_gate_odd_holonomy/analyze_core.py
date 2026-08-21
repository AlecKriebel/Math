#!/usr/bin/env python3
"""Print a symbolic unit-propagation trace for a boundary-cycle core."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


def load_probe(path: Path):
    spec = importlib.util.spec_from_file_location("boundary_probe", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--types", default="012")
    parser.add_argument("--lengths", default="1,1,1")
    parser.add_argument("--spare-vertices", type=int, default=0)
    args = parser.parse_args()

    probe_path = Path(__file__).with_name("probe_boundary_cycle.py")
    probe = load_probe(probe_path)
    types = tuple(int(char) for char in args.types)
    lengths = tuple(int(piece) for piece in args.lengths.split(","))
    cnf, _ = probe.build(
        types,
        lengths,
        enforce_gamma=True,
        spare_vertices=args.spare_vertices,
    )
    clauses = [
        tuple(map(int, line.split()[:-1]))
        for line in args.core.read_text(encoding="ascii").splitlines()
        if line and line[0] not in "cp"
    ]

    values: dict[int, bool] = {}

    def format_literal(literal: int) -> str:
        return ("not " if literal < 0 else "") + cnf.names[abs(literal)]

    while True:
        progress = False
        for index, clause in enumerate(clauses, start=1):
            if any(
                values.get(abs(literal)) == (literal > 0)
                for literal in clause
            ):
                continue
            unassigned = [
                literal for literal in clause if abs(literal) not in values
            ]
            if not unassigned:
                print(f"CONTRADICTION at clause {index}")
                print("  " + " OR ".join(format_literal(lit) for lit in clause))
                return
            if len(unassigned) != 1:
                continue
            literal = unassigned[0]
            values[abs(literal)] = literal > 0
            print(
                f"{len(values):03d}. {format_literal(literal)}"
                f"    [clause {index}]"
            )
            progress = True
        if not progress:
            print("STALLED")
            return


if __name__ == "__main__":
    main()
