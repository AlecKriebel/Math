#!/usr/bin/env python3
"""Greedy discovery-only minimization of domination-pair constraints.

This imports the direct probe encoding, keeps i>=3 and alpha<=3, and asks
which explicit pair-nondomination groups are still needed for UNSAT at a
fixed finite order.  The result is a heuristic proof-extraction aid, not a
certificate and not a mathematical claim.
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


def solve(module, order: int, case: str, pairs, solver: Path, cnf_path: Path):
    cnf, _ = module.build(
        order,
        case,
        require_alpha=True,
        require_gamma=False,
        require_i=True,
        required_pairs=tuple(pairs),
    )
    cnf.write(cnf_path)
    completed = subprocess.run(
        [str(solver), str(cnf_path)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    status, _ = module.parse_model(completed.stdout)
    return status, cnf.next_variable - 1, len(cnf.clauses)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True)
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument(
        "--probe",
        type=Path,
        default=Path(__file__).with_name("probe_cases.py"),
    )
    arguments = parser.parse_args()
    module = load_probe(arguments.probe)
    active = list(itertools.combinations(range(arguments.order), 2))
    initial, _, _ = solve(
        module,
        arguments.order,
        arguments.case,
        active,
        arguments.solver,
        arguments.cnf,
    )
    if initial != "UNSAT":
        raise RuntimeError(f"initial formula is {initial}, not UNSAT")

    attempts = []
    for pair in list(active):
        trial = [candidate for candidate in active if candidate != pair]
        status, variables, clauses = solve(
            module,
            arguments.order,
            arguments.case,
            trial,
            arguments.solver,
            arguments.cnf,
        )
        removed = status == "UNSAT"
        if removed:
            active = trial
        attempts.append(
            {
                "pair": list(pair),
                "status_without_pair": status,
                "removed": removed,
                "remaining": len(active),
                "variables": variables,
                "clauses": clauses,
            }
        )

    final_status, variables, clauses = solve(
        module,
        arguments.order,
        arguments.case,
        active,
        arguments.solver,
        arguments.cnf,
    )
    result = {
        "schema": "rank-one-greedy-pair-core-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "case": arguments.case,
        "order": arguments.order,
        "status": final_status,
        "pair_core": [list(pair) for pair in active],
        "variables": variables,
        "clauses": clauses,
        "attempts": attempts,
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
                "status": final_status,
                "pair_core": result["pair_core"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
