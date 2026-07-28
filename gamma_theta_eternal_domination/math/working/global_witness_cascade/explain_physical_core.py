#!/usr/bin/env python3
"""Translate the trimmed physical-witness UNSAT core symbolically."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[2]
SOURCE = CAMPAIGN / "math" / "working" / "three_gate_odd_holonomy"


def load_probe():
    path = SOURCE / "probe_boundary_cycle.py"
    spec = importlib.util.spec_from_file_location("boundary_probe", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--show-clauses", action="store_true")
    args = parser.parse_args()

    probe = load_probe()
    cnf, _ = probe.build(
        (0, 1, 2),
        (1, 1, 1),
        enforce_gamma=False,
        spare_vertices=1,
        full_gates=True,
        all_two_lists=True,
    )
    clauses = [
        tuple(map(int, line.split()[:-1]))
        for line in args.core.read_text(encoding="ascii").splitlines()
        if line and line[0] not in "cp"
    ]
    values: dict[int, bool] = {}

    def label(literal: int) -> str:
        prefix = "not " if literal < 0 else ""
        return prefix + cnf.names[abs(literal)]

    if args.show_clauses:
        for index, clause in enumerate(clauses, start=1):
            print(
                f"C{index:02d}: "
                + " OR ".join(label(literal) for literal in clause)
            )
        print("--- unit propagation ---")

    while True:
        progress = False
        for index, clause in enumerate(clauses, start=1):
            if any(
                values.get(abs(literal)) == (literal > 0)
                for literal in clause
            ):
                continue
            undecided = [
                literal for literal in clause if abs(literal) not in values
            ]
            if not undecided:
                print(f"CONTRADICTION clause {index}")
                print("  " + " OR ".join(label(lit) for lit in clause))
                return
            if len(undecided) != 1:
                continue
            literal = undecided[0]
            values[abs(literal)] = literal > 0
            print(f"{len(values):03d}. {label(literal)} [clause {index}]")
            progress = True
        if not progress:
            print("STALLED")
            return


if __name__ == "__main__":
    main()
