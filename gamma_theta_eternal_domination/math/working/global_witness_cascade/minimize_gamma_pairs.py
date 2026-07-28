#!/usr/bin/env python3
"""Greedily extract an inclusion-minimal gamma-pair set.

The result is a bounded discovery artifact.  A selected pair ``{u,v}``
means that the SAT formula requires some common complement neighbor of
``u`` and ``v``.  Requiring this for every pair is exactly
``gamma(G) >= 3``.  A small core helps expose the finite witness cascade,
but does not by itself prove an arbitrary-order theorem.
"""

from __future__ import annotations

import argparse
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
import tempfile
import time


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


def solve(
    solver: Path,
    cnf,
    clauses: list[tuple[int, ...]],
    instance: Path,
) -> str:
    old = cnf.clauses
    cnf.clauses = clauses
    try:
        instance.write_text(cnf.dimacs(), encoding="ascii")
    finally:
        cnf.clauses = old
    run = subprocess.run(
        [str(solver), "--quiet", str(instance)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if run.returncode == 10:
        return "SAT"
    if run.returncode == 20:
        return "UNSAT"
    raise RuntimeError(f"solver exited {run.returncode}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--spares", type=int, default=6)
    parser.add_argument(
        "--order",
        choices=("forward", "reverse", "shuffle"),
        default="forward",
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    probe = load_probe()
    cnf, metadata = probe.build(
        (0, 1, 2),
        (1, 1, 1),
        enforce_gamma=False,
        spare_vertices=args.spares,
        all_two_lists=True,
    )
    base = list(cnf.clauses)
    order = int(metadata["order"])
    edge = metadata["edge"]
    witness = metadata["witness"]
    assert isinstance(edge, dict)
    assert isinstance(witness, dict)

    pairs = list(combinations(range(order), 2))
    groups: dict[tuple[int, int], list[tuple[int, ...]]] = {}
    for u, v in pairs:
        choices = tuple(w for w in range(order) if w not in (u, v))
        clauses = [
            tuple(witness[(u, v, w)] for w in choices),
        ]
        for w in choices:
            marker = witness[(u, v, w)]
            clauses.append((-marker, edge[probe.pair(u, w)]))
            clauses.append((-marker, edge[probe.pair(v, w)]))
        groups[(u, v)] = clauses

    deletion_order = list(pairs)
    if args.order == "reverse":
        deletion_order.reverse()
    elif args.order == "shuffle":
        random.Random(args.seed).shuffle(deletion_order)

    active = set(pairs)
    tests: list[dict[str, object]] = []
    started = time.monotonic()
    with tempfile.TemporaryDirectory() as directory:
        instance = Path(directory) / "core.cnf"

        def active_clauses(selected: set[tuple[int, int]]):
            return base + [
                clause
                for pair in pairs
                if pair in selected
                for clause in groups[pair]
            ]

        initial = solve(
            args.solver,
            cnf,
            active_clauses(active),
            instance,
        )
        if initial != "UNSAT":
            raise RuntimeError(f"full gamma formula is {initial}, not UNSAT")

        for index, pair in enumerate(deletion_order, start=1):
            candidate = active - {pair}
            status = solve(
                args.solver,
                cnf,
                active_clauses(candidate),
                instance,
            )
            removed = status == "UNSAT"
            if removed:
                active = candidate
            tests.append(
                {
                    "pair": list(pair),
                    "without_pair": status,
                    "removed": removed,
                    "active_count": len(active),
                }
            )
            if index % 20 == 0:
                print(
                    f"tested={index}/{len(pairs)} active={len(active)}",
                    flush=True,
                )

    result = {
        "schema": "global-witness-gamma-pair-core-v1",
        "status": "OBSERVED_BOUNDED",
        "spares": args.spares,
        "graph_order": order,
        "deletion_order": args.order,
        "seed": args.seed,
        "base_clause_count": len(base),
        "all_pair_count": len(pairs),
        "core_pair_count": len(active),
        "core_pairs": [list(pair) for pair in sorted(active)],
        "tests": tests,
        "wall_seconds": time.monotonic() - started,
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"order={order} core={len(active)} "
        f"wall={result['wall_seconds']:.2f}s"
    )


if __name__ == "__main__":
    main()
