#!/usr/bin/env python3
"""Enumerate physical/dynamic patterns of the three critical witnesses.

Each of vertices 12,13,14 is forced to be a common complement neighbor of
one critical cross-gate pair.  The three mask bits decide whether that
witness is physical (an H-edge) or dynamic (a G-edge) to its omitted
anchor.  This is a bounded discovery sweep, not a certificate theorem.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile


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
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--full-gates", action="store_true")
    args = parser.parse_args()

    probe = load_probe()
    cnf, metadata = probe.build(
        (0, 1, 2),
        (1, 1, 1),
        enforce_gamma=False,
        spare_vertices=3,
        full_gates=args.full_gates,
        all_two_lists=True,
    )
    edge = metadata["edge"]
    family = metadata["family"]
    assert isinstance(edge, dict)
    assert isinstance(family, dict)
    first_spare = int(metadata["order"]) - 3
    critical = (
        (4, 6, first_spare),
        (5, 7, first_spare + 1),
        (3, 8, first_spare + 2),
    )

    fixed = []
    for u, v, q in critical:
        fixed.extend((edge[probe.pair(u, q)], edge[probe.pair(v, q)]))

    rows = []
    with tempfile.TemporaryDirectory() as directory:
        instance = Path(directory) / "pattern.cnf"
        model = Path(directory) / "pattern.model"
        for mask in range(8):
            units = list(fixed)
            for anchor, (_, _, q) in enumerate(critical):
                literal = edge[probe.pair(anchor, q)]
                units.append(literal if mask & (1 << anchor) else -literal)
            old = cnf.clauses
            cnf.clauses = old + [(literal,) for literal in units]
            try:
                instance.write_text(cnf.dimacs(), encoding="ascii")
            finally:
                cnf.clauses = old
            run = subprocess.run(
                [
                    str(args.solver),
                    "--quiet",
                    "--binary=false",
                    "-w",
                    str(model),
                    str(instance),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            status = (
                "SAT"
                if run.returncode == 10
                else "UNSAT"
                if run.returncode == 20
                else f"EXIT_{run.returncode}"
            )
            if status not in {"SAT", "UNSAT"}:
                raise RuntimeError(status)
            assignment: dict[int, bool] = {}
            if status == "SAT":
                literals = [
                    int(piece)
                    for line in model.read_text(encoding="ascii").splitlines()
                    if line.startswith("v ")
                    for piece in line.split()[1:]
                    if piece != "0"
                ]
                assignment = {
                    abs(literal): literal > 0 for literal in literals
                }
            rows.append(
                {
                    "mask": mask,
                    "anchor_incidence": [
                        "physical" if mask & (1 << anchor) else "dynamic"
                        for anchor in range(3)
                    ],
                    "status": status,
                    "witness_lists": [
                        [
                            omitted
                            for omitted in range(3)
                            if assignment.get(
                                family[
                                    tuple(
                                        sorted(
                                            ({0, 1, 2} - {omitted}) | {q}
                                        )
                                    )
                                ],
                                False,
                            )
                        ]
                        for _, _, q in critical
                    ]
                    if status == "SAT"
                    else [],
                }
            )

    result = {
        "schema": "critical-three-witness-pattern-sweep-v1",
        "status": "OBSERVED_BOUNDED",
        "order": int(metadata["order"]),
        "full_gates": args.full_gates,
        "rows": rows,
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        " ".join(f"{row['mask']}:{row['status']}" for row in rows)
    )


if __name__ == "__main__":
    main()
