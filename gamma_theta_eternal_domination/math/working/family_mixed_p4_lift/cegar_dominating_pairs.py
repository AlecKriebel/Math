#!/usr/bin/env python3
"""Discovery CEGAR: add one currently dominating pair at a time."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import subprocess
import tempfile
from pathlib import Path


SOURCE = Path(__file__).with_name("synthesize.py")
SPEC = importlib.util.spec_from_file_location("family_mixed_p4_synthesize", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load synthesize.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
make_formula = MODULE.make_formula
parse_model = MODULE.parse_model


def solve(order: int, pairs: set[tuple[int, int]], solver: Path):
    formula, metadata = make_formula(order, pairs)
    with tempfile.NamedTemporaryFile(suffix=".cnf") as handle:
        formula.write(Path(handle.name))
        run = subprocess.run(
            [str(solver), handle.name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    return parse_model(run.stdout), metadata


def model_edges(metadata: dict, model: set[int]) -> set[tuple[int, int]]:
    edges = set()
    for name, variable in metadata["edge_vars"].items():
        if variable in model:
            _, left, right = name.split(":")
            edges.add((int(left), int(right)))
    return edges


def dominating_pairs(order: int, edges: set[tuple[int, int]]):
    adjacency = [set() for _ in range(order)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    result = []
    for pair in itertools.combinations(range(order), 2):
        covered = set(pair) | adjacency[pair[0]] | adjacency[pair[1]]
        if len(covered) == order:
            result.append(pair)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=12)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()

    selected: set[tuple[int, int]] = set()
    rounds = []
    while True:
        model, metadata = solve(args.order, selected, args.solver)
        if model is None:
            status = "UNSAT"
            break
        edges = model_edges(metadata, model)
        bad = dominating_pairs(args.order, edges)
        if not bad:
            status = "SAT_EQUALITY_CONTROL"
            break

        # Prefer a pair wholly inside the seven distinguished vertices,
        # then one touching them, before a purely anonymous pair.
        bad.sort(
            key=lambda pair: (
                sum(vertex >= 7 for vertex in pair),
                pair,
            )
        )
        chosen = bad[0]
        selected.add(chosen)
        rounds.append(
            {
                "round": len(rounds) + 1,
                "chosen_pair": list(chosen),
                "dominating_pair_count": len(bad),
                "dominating_pairs": [list(pair) for pair in bad],
                "edge_count": len(edges),
            }
        )
        print(json.dumps(rounds[-1]), flush=True)

    result = {
        "schema": "family-mixed-p4-dominating-pair-cegar-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "order": args.order,
        "status": status,
        "selected_pairs": [list(pair) for pair in sorted(selected)],
        "rounds": rounds,
    }
    args.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
