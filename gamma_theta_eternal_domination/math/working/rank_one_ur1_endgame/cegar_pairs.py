#!/usr/bin/env python3
"""Discovery-only CEGAR for domination-pair constraints in QQ1/AQ1.

Start from the direct rank-one collision encoding with alpha <= 3 and
i >= 3, but without gamma >= 3.  Whenever a model has a dominating
pair, add the exact requirement that this pair have an external common
nonneighbor.  Stop at UNSAT or at a fixed iteration budget.

The resulting pair sequence is heuristic proof-extraction evidence.  It
is not a certificate and is never promoted as a mathematical claim.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import subprocess
from pathlib import Path


def load_probe(path: Path):
    spec = importlib.util.spec_from_file_location("rank_one_probe_cases", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_edges(metadata, positive):
    edges = set()
    for name, number in metadata["edge_variables"].items():
        if number in positive:
            _, left, right = name.split(":")
            edge = (int(left), int(right))
            edges.add(edge)
            edges.add(edge[::-1])
    return edges


def dominating_pairs(order, edges):
    result = []
    for pair in itertools.combinations(range(order), 2):
        if all(
            target in pair
            or any((guard, target) in edges for guard in pair)
            for target in range(order)
        ):
            result.append(pair)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("QQ1", "AQ1"), required=True)
    parser.add_argument("--order", type=int, default=16)
    parser.add_argument("--iterations", type=int, default=200)
    parser.add_argument(
        "--minimize",
        action="store_true",
        help="greedily delete pairs from an UNSAT CEGAR sequence",
    )
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument(
        "--probe",
        type=Path,
        default=Path(__file__).parents[1]
        / "rank_one_remaining_endgame"
        / "probe_cases.py",
    )
    arguments = parser.parse_args()
    module = load_probe(arguments.probe)
    active = []
    trace = []

    for iteration in range(arguments.iterations + 1):
        cnf, metadata = module.build(
            arguments.order,
            arguments.case,
            require_alpha=True,
            require_gamma=False,
            require_i=True,
            required_pairs=tuple(active),
        )
        cnf.write(arguments.cnf)
        completed = subprocess.run(
            [str(arguments.solver), str(arguments.cnf)],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        status, positive = module.parse_model(completed.stdout)
        row = {
            "iteration": iteration,
            "status": status,
            "active_pairs": [list(pair) for pair in active],
            "variables": cnf.next_variable - 1,
            "clauses": len(cnf.clauses),
        }
        trace.append(row)
        if status == "UNSAT":
            break

        edges = parse_edges(metadata, positive)
        candidates = [
            pair
            for pair in dominating_pairs(arguments.order, edges)
            if pair not in active
        ]
        if not candidates:
            row["termination"] = "model has no unblocked dominating pair"
            break

        labels = metadata["labels"]
        named = set(labels.values())
        candidates.sort(
            key=lambda pair: (
                -sum(vertex in named for vertex in pair),
                pair,
            )
        )
        chosen = candidates[0]
        row["chosen_pair"] = list(chosen)
        active.append(chosen)

    minimization = []
    if arguments.minimize and trace[-1]["status"] == "UNSAT":
        for pair in reversed(tuple(active)):
            trial = [candidate for candidate in active if candidate != pair]
            cnf, _ = module.build(
                arguments.order,
                arguments.case,
                require_alpha=True,
                require_gamma=False,
                require_i=True,
                required_pairs=tuple(trial),
            )
            cnf.write(arguments.cnf)
            completed = subprocess.run(
                [str(arguments.solver), str(arguments.cnf)],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            status, _ = module.parse_model(completed.stdout)
            removed = status == "UNSAT"
            minimization.append(
                {
                    "pair": list(pair),
                    "status_without_pair": status,
                    "removed": removed,
                }
            )
            if removed:
                active = trial

    result = {
        "schema": "rank-one-ur1-pair-cegar-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "case": arguments.case,
        "order": arguments.order,
        "final_status": trace[-1]["status"],
        "pair_sequence": [list(pair) for pair in active],
        "minimization": minimization,
        "trace": trace,
    }
    arguments.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "case": arguments.case,
                "order": arguments.order,
                "status": trace[-1]["status"],
                "pair_sequence": result["pair_sequence"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
