#!/usr/bin/env python3
"""Discovery-only ablation audit for the QQ1 auxiliary-pair probe.

This script deliberately imports the existing discovery encoder and removes
selected *classes of assumptions* before solving.  Its output is diagnostic
only: SAT gives a real model of the weakened encoding, while UNSAT is not
promoted without a proof log and independent reconstruction.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROBE = HERE.parent / "qq1_inner_global_attack" / "probe_simultaneous.py"


def load_probe():
    spec = importlib.util.spec_from_file_location("qq1_probe", PROBE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {PROBE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=16)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument(
        "--ablate",
        choices=(
            "none",
            "alpha",
            "i-extension",
            "family-closure",
            "activity",
            "omitted-O",
            "named-states",
            "hot-states",
            "U",
            "R",
            "I",
            "A",
            "K",
            "E",
            "F",
        ),
        default="none",
    )
    arguments = parser.parse_args()

    probe = load_probe()
    collision = probe.load_collision()
    order = arguments.order
    residual = tuple(range(10, order))
    required_pairs = ((0, 1),) + tuple(
        (anchor, vertex) for anchor in (2, 3) for vertex in residual
    )
    cnf, metadata, base = collision.build(
        order,
        require_alpha=arguments.ablate != "alpha",
        require_gamma=False,
        require_i=arguments.ablate != "i-extension",
        required_pairs=required_pairs,
    )

    def edge(left: int, right: int) -> int:
        left, right = sorted((left, right))
        return cnf.variable(f"e:{left}:{right}")

    def family(state: set[int]) -> int:
        triple = tuple(sorted(state))
        index = metadata["triples"].index(triple)
        return cnf.variable(f"f:{index}")

    def force_edge(left: int, right: int, present: bool) -> None:
        literal = edge(left, right)
        cnf.add(literal if present else -literal)

    u, x, p, q, r, b, c, d, w, z = range(10)
    for left, right, present in (
        (d, x, False),
        (d, r, False),
        (d, p, True),
        (d, q, True),
        (d, b, True),
        (d, c, True),
        (u, d, True),
        (w, u, False),
        (w, d, False),
        (w, x, True),
        (w, r, True),
        (z, u, False),
        (z, x, False),
        (z, d, True),
    ):
        force_edge(left, right, present)
    cnf.add(edge(w, b), edge(w, c))
    cnf.add(edge(z, p), edge(z, q))
    cnf.add(edge(z, b), edge(z, c))

    states = {
        "U": {u, b, c},
        "R": {r, b, c},
        "I": {x, r, d},
        "A": {u, x, d},
        "K": {u, d, w},
        "E": {x, d, w},
        "F": {r, d, w},
    }
    for name, state in states.items():
        skip_all_named = arguments.ablate == "named-states"
        skip_hot = arguments.ablate == "hot-states" and name in {"A", "K", "E", "F"}
        if arguments.ablate != name and not skip_all_named and not skip_hot:
            cnf.add(family(state))
    if arguments.ablate != "omitted-O":
        cnf.add(-family({u, r, d}))

    if arguments.ablate == "family-closure":
        move_variables = {
            number
            for name, number in cnf.by_name.items()
            if name.startswith("move:")
        }
        cnf.clauses = [
            clause
            for clause in cnf.clauses
            if not any(abs(literal) in move_variables for literal in clause)
        ]

    if arguments.ablate == "activity":
        activity_clauses = set()
        for third in range(order):
            if third in (u, x, b):
                continue
            activity_clauses.add(
                (
                    edge(u, third),
                    edge(b, third),
                    family({x, b, third}),
                )
            )
        cnf.clauses = [
            clause for clause in cnf.clauses if clause not in activity_clauses
        ]

    cnf.write(arguments.cnf)
    completed = subprocess.run(
        [str(arguments.solver), str(arguments.cnf)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    status, positive = base.parse_model(completed.stdout)
    result = {
        "schema": "QQ1-auxiliary-pair-ablation-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "order": order,
        "ablation": arguments.ablate,
        "status": status,
        "variables": cnf.next_variable - 1,
        "clauses": len(cnf.clauses),
    }
    if status == "SAT":
        result["edges"] = [
            list(map(int, name.split(":")[1:]))
            for name, number in metadata["edge_variables"].items()
            if number in positive
        ]
    arguments.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in result.items() if key != "edges"}))


if __name__ == "__main__":
    main()
