#!/usr/bin/env python3
"""Discovery-only CEGAR for the global pair obligations in QQ1.

This repeatedly asks ``probe_simultaneous.py`` for a model under the
currently selected pair-nondomination constraints, finds a dominating
pair in that model, and blocks it.  A finite UNSAT sequence is heuristic
proof-extraction evidence only.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import tempfile
from pathlib import Path


def pair_text(pair: tuple[int, int]) -> str:
    return f"{pair[0]}-{pair[1]}"


def graph_from_result(result: dict) -> list[set[int]]:
    graph = [set() for _ in range(result["order"])]
    for left, right in result["edges"]:
        graph[left].add(right)
        graph[right].add(left)
    return graph


def dominating_pairs(graph: list[set[int]]) -> list[tuple[int, int]]:
    pairs = []
    for left, right in itertools.combinations(range(len(graph)), 2):
        if all(
            target in (left, right)
            or target in graph[left]
            or target in graph[right]
            for target in range(len(graph))
        ):
            pairs.append((left, right))
    return pairs


def run_probe(
    probe: Path,
    solver: Path,
    order: int,
    ud: str,
    pairs: list[tuple[int, int]],
    directory: Path,
) -> dict:
    cnf = directory / "instance.cnf"
    result = directory / "result.json"
    command = [
        "python3",
        str(probe),
        "--order",
        str(order),
        "--ud",
        ud,
        "--pairs",
        ",".join(map(pair_text, pairs)),
        "--solver",
        str(solver),
        "--cnf",
        str(cnf),
        "--result",
        str(result),
    ]
    completed = subprocess.run(
        command,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return json.loads(result.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--ud", choices=("edge", "nonedge"), required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--iterations", type=int, default=200)
    parser.add_argument("--minimize", action="store_true")
    parser.add_argument(
        "--probe",
        type=Path,
        default=Path(__file__).with_name("probe_simultaneous.py"),
    )
    arguments = parser.parse_args()

    active: list[tuple[int, int]] = [(0, 1)]
    trace = []
    with tempfile.TemporaryDirectory(prefix="qq1-inner-cegar.") as raw:
        directory = Path(raw)
        for iteration in range(arguments.iterations + 1):
            result = run_probe(
                arguments.probe,
                arguments.solver,
                arguments.order,
                arguments.ud,
                active,
                directory,
            )
            row = {
                "iteration": iteration,
                "status": result["status"],
                "active_pairs": [list(pair) for pair in active],
            }
            trace.append(row)
            if result["status"] == "UNSAT":
                break
            graph = graph_from_result(result)
            candidates = [
                pair
                for pair in dominating_pairs(graph)
                if pair not in active
            ]
            if not candidates:
                row["termination"] = "model has no dominating pair"
                break
            candidates.sort(
                key=lambda pair: (
                    -sum(vertex < 10 for vertex in pair),
                    pair,
                )
            )
            chosen = candidates[0]
            row["chosen_pair"] = list(chosen)
            row["dominating_pair_count"] = len(candidates)
            active.append(chosen)

        minimization = []
        if arguments.minimize and trace[-1]["status"] == "UNSAT":
            for pair in reversed(tuple(active[1:])):
                trial = [candidate for candidate in active if candidate != pair]
                result = run_probe(
                    arguments.probe,
                    arguments.solver,
                    arguments.order,
                    arguments.ud,
                    trial,
                    directory,
                )
                removed = result["status"] == "UNSAT"
                minimization.append(
                    {
                        "pair": list(pair),
                        "status_without_pair": result["status"],
                        "removed": removed,
                    }
                )
                if removed:
                    active = trial

    output = {
        "schema": "QQ1-inner-pair-CEGAR-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "order": arguments.order,
        "ud": arguments.ud,
        "status": trace[-1]["status"],
        "final_pairs": [list(pair) for pair in active],
        "trace": trace,
        "minimization": minimization,
    }
    arguments.result.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "order": arguments.order,
                "ud": arguments.ud,
                "status": output["status"],
                "pairs": output["final_pairs"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
