#!/usr/bin/env python3
"""Proof-capable PySAT worker with deterministic conflict-bounded pilots."""

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

from residual_completion_glucose import (
    model_satisfies,
    parse_dimacs,
    write_proof_atomic,
)


WORKER_ID = "ramsey55_global_proof_solver_worker_v1"
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
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--conflict-budget", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.conflict_budget is not None and args.conflict_budget <= 0:
        raise SystemExit("--conflict-budget must be positive")

    cnf_sha256 = hashlib.sha256(args.cnf.read_bytes()).hexdigest()
    variable_count, clauses = parse_dimacs(args.cnf)
    solver_class = SOLVERS[args.solver]
    started = time.monotonic()
    with solver_class(
        bootstrap_with=clauses,
        with_proof=True,
        use_timer=True,
    ) as solver:
        if args.conflict_budget is None:
            status = solver.solve()
        else:
            solver.conf_budget(args.conflict_budget)
            status = solver.solve_limited()
        stats = solver.accum_stats()
        solver_cpu = solver.time_accum()
        if status is True:
            model = solver.get_model()
            proof = None
        elif status is False:
            model = None
            proof = solver.get_proof()
        else:
            model = None
            proof = None

    result: dict[str, object] = {
        "worker": WORKER_ID,
        "solver": args.solver,
        "solver_class_source": inspect.getfile(solver_class),
        "pysat_version": pysat.__version__,
        "status": (
            "SAT"
            if status is True
            else "UNSAT"
            if status is False
            else "BUDGET_EXHAUSTED"
        ),
        "cnf_sha256": cnf_sha256,
        "variable_count": variable_count,
        "clause_count": len(clauses),
        "conflict_budget": args.conflict_budget,
        "runtime_seconds": time.monotonic() - started,
        "solver_cpu_seconds": solver_cpu,
        "maximum_resident_set_bytes": resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss,
        **stats,
    }
    if status is True:
        assert model is not None
        if not model_satisfies(model, clauses):
            raise AssertionError("solver model failed direct clause evaluation")
        result["true_variables"] = sorted(
            abs(literal) for literal in model if literal > 0
        )
        result["model_literal_count"] = len(model)
        result["proof_written"] = False
        return_code = 10
    elif status is False:
        assert proof is not None
        proof_sha256, proof_bytes = write_proof_atomic(args.proof, proof)
        result.update(
            {
                "proof_written": True,
                "proof_path": str(args.proof.resolve()),
                "proof_record_count": len(proof),
                "proof_bytes": proof_bytes,
                "proof_sha256": proof_sha256,
            }
        )
        return_code = 20
    else:
        args.proof.unlink(missing_ok=True)
        result["proof_written"] = False
        return_code = 2

    rendered = json.dumps(result, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(rendered)
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
