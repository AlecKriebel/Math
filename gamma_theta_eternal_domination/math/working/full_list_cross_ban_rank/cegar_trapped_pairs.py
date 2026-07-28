#!/usr/bin/env python3
"""Discovery-only CEGAR for the trapped-transfer gamma-three obstruction."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SEARCH = load("trapped_search", HERE / "search_single_trapped_transfer.py")
CORE = load(
    "c157_core",
    HERE.parent
    / "full_list_nonsingleton_terminal"
    / "verify_cyclic_corridor_control.py",
)


def dominating_pairs(graph6: str):
    rows = CORE.decode_short_graph6(graph6)
    return tuple(
        pair
        for pair in itertools.combinations(range(len(rows)), 2)
        if CORE.dominates(rows, CORE.vertex_mask(pair))
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    args = parser.parse_args()

    required: set[tuple[int, int]] = set()
    trace = []
    while True:
        result = SEARCH.solve(
            args.order,
            args.solver.resolve(),
            frozenset(required),
            enforce_gamma_three=True,
        )
        row = {
            "iteration": len(trace),
            "required_pairs": [list(pair) for pair in sorted(required)],
            "status": result["status"],
            "graph6": result["graph6"],
        }
        if result["status"] != "SAT":
            trace.append(row)
            break
        pairs = dominating_pairs(result["graph6"])
        row["dominating_pairs"] = [list(pair) for pair in pairs]
        choices = tuple(pair for pair in pairs if pair not in required)
        if not choices:
            raise AssertionError("SAT model has no new dominating pair")
        chosen = min(choices)
        row["added_pair"] = list(chosen)
        trace.append(row)
        required.add(chosen)

    # Deletion-minimize the discovered set; still OBSERVED.
    changed = True
    while changed:
        changed = False
        for pair in sorted(required):
            trial = frozenset(required - {pair})
            result = SEARCH.solve(
                args.order,
                args.solver.resolve(),
                trial,
                enforce_gamma_three=True,
            )
            if result["status"] == "UNSAT":
                required.remove(pair)
                changed = True
                break

    print(
        json.dumps(
            {
                "status": "OBSERVED",
                "order": args.order,
                "trace": trace,
                "deletion_minimal_pair_set": [
                    list(pair) for pair in sorted(required)
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
