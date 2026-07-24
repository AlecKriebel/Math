#!/usr/bin/env python3
"""Proof-free internal-triangle count split for greedy 3^14 1 CNFs."""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import resource
import sys
import time
from collections import Counter
from pathlib import Path

import pysat
from pysat import solvers


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import automorphism_orbit_cnf as orbit_cnf  # noqa: E402
from residual_completion_glucose import parse_dimacs  # noqa: E402


WORKER_ID = "ramsey55_order3_internal_count_split_observation_v1"
SOLVERS = {
    name: getattr(solvers, name)
    for name in ("Glucose3", "Glucose4", "MapleChrono", "Cadical195")
}


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def internal_variables() -> tuple[int, ...]:
    permutation = orbit_cnf.canonical_permutation(3, 14)
    edge_variable, _ = orbit_cnf.edge_orbit_table(permutation)
    variables = tuple(
        edge_variable[(3 * cycle, 3 * cycle + 1)]
        for cycle in range(14)
    )
    if len(set(variables)) != 14:
        raise AssertionError("internal edge variables are not distinct")
    return variables


def count_assumptions(
    root_cycles: int, neighbor_true: int, nonneighbor_true: int
) -> tuple[int, ...]:
    variables = internal_variables()
    result: list[int] = []
    for index, variable in enumerate(variables[:root_cycles]):
        result.append(variable if index < neighbor_true else -variable)
    for index, variable in enumerate(variables[root_cycles:]):
        result.append(variable if index < nonneighbor_true else -variable)
    return tuple(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--root-cycles", type=int, choices=(6, 7), required=True)
    parser.add_argument("--solver", choices=sorted(SOLVERS), required=True)
    parser.add_argument("--conflict-budget", type=int, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    if args.conflict_budget <= 0:
        parser.error("--conflict-budget must be positive")

    started = time.monotonic()
    variable_count, clauses = parse_dimacs(args.cnf)
    solver_class = SOLVERS[args.solver]
    records: list[dict[str, object]] = []
    with solver_class(bootstrap_with=clauses, use_timer=True) as solver:
        for neighbor_true in range(args.root_cycles + 1):
            for nonneighbor_true in range(15 - args.root_cycles):
                assumptions = count_assumptions(
                    args.root_cycles, neighbor_true, nonneighbor_true
                )
                before = solver.accum_stats()
                case_started = time.monotonic()
                solver.conf_budget(args.conflict_budget)
                outcome = solver.solve_limited(assumptions=assumptions)
                after = solver.accum_stats()
                status = (
                    "SAT"
                    if outcome is True
                    else "OBSERVED_UNSAT_UNCHECKED"
                    if outcome is False
                    else "BUDGET_EXHAUSTED"
                )
                record = {
                    "neighbor_internal_true": neighbor_true,
                    "nonneighbor_internal_true": nonneighbor_true,
                    "assumptions": list(assumptions),
                    "status": status,
                    "negative_certified": False,
                    "conflict_budget": args.conflict_budget,
                    "conflicts": (
                        after.get("conflicts", 0)
                        - before.get("conflicts", 0)
                    ),
                    "decisions": (
                        after.get("decisions", 0)
                        - before.get("decisions", 0)
                    ),
                    "propagations": (
                        after.get("propagations", 0)
                        - before.get("propagations", 0)
                    ),
                    "runtime_seconds": time.monotonic() - case_started,
                }
                records.append(record)
                if outcome is True:
                    break
            if records[-1]["status"] == "SAT":
                break
    statuses = Counter(record["status"] for record in records)
    result = {
        "worker": WORKER_ID,
        "evidence_label": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "negative_certified": False,
        "claim_boundary": (
            "Solver-reported negative cases have no proof artifacts. Even a "
            "complete observed split is not a certified exclusion."
        ),
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256_file(args.cnf),
        "variable_count": variable_count,
        "clause_count": len(clauses),
        "root_neighbor_cycle_count": args.root_cycles,
        "internal_variables": list(internal_variables()),
        "case_count": (
            (args.root_cycles + 1) * (15 - args.root_cycles)
        ),
        "visited_case_count": len(records),
        "conflict_budget_per_case": args.conflict_budget,
        "solver": args.solver,
        "solver_class_source": inspect.getfile(solver_class),
        "pysat_version": pysat.__version__,
        "status_counts": dict(sorted(statuses.items())),
        "records": records,
        "runtime_seconds": time.monotonic() - started,
        "maximum_resident_set_bytes": resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss,
    }
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in result.items() if key != "records"}, sort_keys=True))
    return 10 if statuses.get("SAT") else 0


if __name__ == "__main__":
    raise SystemExit(main())
