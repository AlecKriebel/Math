#!/usr/bin/env python3
"""Run a pinned, proof-free PySAT solver observation on a DIMACS formula."""

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

from residual_completion_glucose import model_satisfies, parse_dimacs


WORKER_ID = "ramsey55_proof_free_cnf_solver_observation_v1"
SOLVERS = {
    name: getattr(solvers, name)
    for name in (
        "Glucose3",
        "Glucose4",
        "Glucose42",
        "Gluecard3",
        "Gluecard4",
        "Lingeling",
        "MapleChrono",
        "MapleCM",
        "Maplesat",
        "Cadical103",
        "Cadical153",
        "Cadical195",
        "Cadical300",
    )
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--solver", choices=sorted(SOLVERS), required=True)
    parser.add_argument("--conflict-budget", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.conflict_budget <= 0:
        parser.error("--conflict-budget must be positive")

    cnf_sha256 = hashlib.sha256(args.cnf.read_bytes()).hexdigest()
    variable_count, clauses = parse_dimacs(args.cnf)
    solver_class = SOLVERS[args.solver]
    started = time.monotonic()
    with solver_class(bootstrap_with=clauses, use_timer=True) as solver:
        solver.conf_budget(args.conflict_budget)
        outcome = solver.solve_limited()
        stats = solver.accum_stats()
        solver_cpu_seconds = solver.time_accum()
        model = solver.get_model() if outcome is True else None
    status = (
        "SAT"
        if outcome is True
        else "OBSERVED_UNSAT_UNCHECKED"
        if outcome is False
        else "BUDGET_EXHAUSTED"
    )
    result: dict[str, object] = {
        "worker": WORKER_ID,
        "evidence_label": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "status": status,
        "negative_certified": False,
        "solver": args.solver,
        "solver_class_source": inspect.getfile(solver_class),
        "pysat_version": pysat.__version__,
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": cnf_sha256,
        "variable_count": variable_count,
        "clause_count": len(clauses),
        "conflict_budget": args.conflict_budget,
        "runtime_seconds": time.monotonic() - started,
        "solver_cpu_seconds": solver_cpu_seconds,
        "maximum_resident_set_bytes": resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss,
        **stats,
    }
    if outcome is True:
        assert model is not None
        if not model_satisfies(model, clauses):
            raise AssertionError("SAT model failed direct clause evaluation")
        result["true_variables"] = sorted(
            abs(literal) for literal in model if literal > 0
        )
        result["model_literal_count"] = len(model)
        result["model_satisfies_cnf"] = True
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 10 if outcome is True else 20 if outcome is False else 2


if __name__ == "__main__":
    raise SystemExit(main())
