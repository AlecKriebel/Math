#!/usr/bin/env python3
"""Proof-free matched baseline for the degree-19/20 anchor-union formulas.

Each job loads the same audited global CNF and uses only the exact
complement/minimum-degree branch assumptions.  It is intentionally a bounded
solver observation, not a proof or a negative result.
"""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import resource
import time
from pathlib import Path

import pysat
from pysat import solvers

from global_minmax_degree_cover import branch_units, units_sha256
from residual_completion_glucose import model_satisfies, parse_dimacs


WORKER_ID = "ramsey55_global_anchor_matched_baseline_v1"
DEGREES = (19, 20)
SOLVERS = {
    name: getattr(solvers, name)
    for name in ("Cadical195", "Glucose4", "MapleChrono")
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--solver", choices=sorted(SOLVERS), default="MapleChrono")
    parser.add_argument("--conflict-budget", type=int, default=50_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.conflict_budget <= 0:
        parser.error("--conflict-budget must be positive")

    base_sha256 = sha256_file(args.base_cnf)
    variable_count, clauses = parse_dimacs(args.base_cnf)
    solver_class = SOLVERS[args.solver]
    records: list[dict[str, object]] = []
    for degree in DEGREES:
        assumptions = branch_units(degree)
        started = time.monotonic()
        with solver_class(bootstrap_with=clauses, use_timer=True) as solver:
            solver.conf_budget(args.conflict_budget)
            outcome = solver.solve_limited(assumptions=assumptions)
            statistics = solver.accum_stats()
            solver_cpu_seconds = solver.time_accum()
            model = solver.get_model() if outcome is True else None
        status = (
            "SAT"
            if outcome is True
            else "OBSERVED_UNSAT_UNCHECKED"
            if outcome is False
            else "BUDGET_EXHAUSTED"
        )
        record: dict[str, object] = {
            "degree": degree,
            "degree_interval": [degree, 42 - degree],
            "assumption_count": len(assumptions),
            "assumptions_sha256": units_sha256(assumptions),
            "status": status,
            "negative_certified": False,
            "wall_seconds": time.monotonic() - started,
            "solver_cpu_seconds": solver_cpu_seconds,
            **statistics,
        }
        if outcome is True:
            assert model is not None
            model_assignment = {
                abs(literal): literal > 0 for literal in model
            }
            if not model_satisfies(model, clauses) or not all(
                model_assignment[abs(literal)] == (literal > 0)
                for literal in assumptions
            ):
                raise AssertionError("reported SAT model failed replay")
            record["model_satisfies_base_and_assumptions"] = True
        records.append(record)

    result = {
        "worker": WORKER_ID,
        "evidence_label": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "status": "MATCHED_BOUNDED_BASELINES_NO_PROOF",
        "base_cnf_path": str(args.base_cnf.resolve()),
        "base_cnf_sha256": base_sha256,
        "base_variable_count": variable_count,
        "base_clause_count": len(clauses),
        "solver": args.solver,
        "solver_class_source": inspect.getfile(solver_class),
        "pysat_version": pysat.__version__,
        "conflict_budget_per_job": args.conflict_budget,
        "maximum_resident_set_bytes": resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss,
        "records": records,
        "claim_limit": (
            "These two bounded proof-free jobs are matched performance "
            "baselines only.  Budget exhaustion and unchecked UNSAT outcomes "
            "have no negative mathematical force."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
