#!/usr/bin/env python3
"""Discovery-only static satisfiability probe for the QQ1/AQ1 incidences.

This deliberately omits every eternal-family variable and transition.
It tests which candidate implications genuinely use game dynamics.
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("QQ1", "AQ1"), required=True)
    parser.add_argument("--order", type=int, default=16)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    arguments = parser.parse_args()
    probe_path = (
        Path(__file__).parents[1]
        / "rank_one_remaining_endgame"
        / "probe_cases.py"
    )
    module = load_probe(probe_path)
    cnf = module.CNF()
    labels = {
        "u": 0,
        "x": 1,
        "p": 2,
        "q": 3,
        "r": 4,
        "y_u": 5,
        "y_p": 6,
        "y_q": 7,
        "w": 8,
        "v": 9,
    }
    vertices = tuple(range(arguments.order))

    def edge(left, right):
        left, right = sorted((left, right))
        return cnf.variable(f"e:{left}:{right}")

    def force(left, right, present):
        literal = edge(labels[left], labels[right])
        cnf.add(literal if present else -literal)

    for left, right in itertools.combinations(("x", "p", "q"), 2):
        force(left, right, False)
    force("u", "x", True)
    force("r", "u", True)
    force("r", "x", arguments.case == "AQ1")
    force("r", "p", True)
    force("r", "q", True)
    for mover in ("u", "p", "q"):
        witness = f"y_{mover}"
        force(witness, mover, True)
        force(witness, "r", False)
        for other in ("u", "p", "q"):
            if other != mover:
                force(witness, other, False)
    force("w", "u", False)
    force("w", "x", False)
    force("v", "x", False)
    force("v", "r", False)

    # alpha <= 3 and i >= 3.
    for four in itertools.combinations(vertices, 4):
        cnf.add(*(edge(*pair) for pair in itertools.combinations(four, 2)))
    for left, right in itertools.combinations(vertices, 2):
        extensions = []
        for third in vertices:
            if third in (left, right):
                continue
            selector = cnf.variable(f"extend:{left}:{right}:{third}")
            extensions.append(selector)
            cnf.add(-selector, -edge(left, third))
            cnf.add(-selector, -edge(right, third))
        cnf.add(edge(left, right), *extensions)

    # T and B dominate.  These are static consequences of the setup.
    for state in (
        (labels["x"], labels["p"], labels["q"]),
        (labels["u"], labels["p"], labels["q"]),
    ):
        for target in vertices:
            if target not in state:
                cnf.add(*(edge(guard, target) for guard in state))

    cnf.write(arguments.cnf)
    completed = subprocess.run(
        [str(arguments.solver), str(arguments.cnf)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    status, positive = module.parse_model(completed.stdout)
    result = {
        "schema": "rank-one-ur1-static-probe-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "case": arguments.case,
        "order": arguments.order,
        "status": status,
        "variables": cnf.next_variable - 1,
        "clauses": len(cnf.clauses),
    }
    if status == "SAT":
        result["edges"] = [
            list(map(int, name.split(":")[1:]))
            for name, number in cnf.by_name.items()
            if name.startswith("e:") and number in positive
        ]
    arguments.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
