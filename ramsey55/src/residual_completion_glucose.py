#!/usr/bin/env python3
"""Pinned PySAT/Glucose proof-producing worker for residual completion.

The parent workflow enforces a wall-clock timeout and independently checks
every UNSAT proof.  This worker has no project-specific graph logic: it reads
one explicit DIMACS formula, solves it deterministically, and emits either a
complete SAT model or an ASCII DRAT trace.
"""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import os
import tempfile
import time
from pathlib import Path

import pysat
from pysat.solvers import Glucose3


WORKER_ID = "ramsey55_pysat_glucose3_proof_worker_v1"


class DimacsError(ValueError):
    pass


def parse_dimacs(path: Path) -> tuple[int, list[list[int]]]:
    variable_count: int | None = None
    declared_clause_count: int | None = None
    clauses: list[list[int]] = []
    pending: list[int] = []
    for line_number, raw in enumerate(
        path.read_text(encoding="ascii").splitlines(), start=1
    ):
        fields = raw.split()
        if not fields or fields[0] == "c":
            continue
        if fields[0] == "p":
            if (
                variable_count is not None
                or len(fields) != 4
                or fields[1] != "cnf"
            ):
                raise DimacsError(f"invalid DIMACS header at line {line_number}")
            variable_count = int(fields[2])
            declared_clause_count = int(fields[3])
            continue
        if variable_count is None:
            raise DimacsError(f"clause before header at line {line_number}")
        for field in fields:
            literal = int(field)
            if literal:
                if not 1 <= abs(literal) <= variable_count:
                    raise DimacsError(
                        f"literal outside declared range at line {line_number}"
                    )
                pending.append(literal)
            else:
                clauses.append(pending)
                pending = []
    if (
        variable_count is None
        or declared_clause_count is None
        or pending
        or len(clauses) != declared_clause_count
    ):
        raise DimacsError("malformed or incomplete DIMACS")
    return variable_count, clauses


def model_satisfies(model: list[int], clauses: list[list[int]]) -> bool:
    values = {abs(literal): literal > 0 for literal in model}
    return all(
        any(values.get(abs(literal), False) == (literal > 0) for literal in clause)
        for clause in clauses
    )


def write_proof_atomic(path: Path, records: list[str]) -> tuple[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="ascii",
            newline="\n",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            for record in records:
                stream.write(record)
                stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)
    return hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_size


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--proof", type=Path, required=True)
    args = parser.parse_args()

    cnf_bytes = args.cnf.read_bytes()
    cnf_sha256 = hashlib.sha256(cnf_bytes).hexdigest()
    variable_count, clauses = parse_dimacs(args.cnf)
    started = time.monotonic()
    with Glucose3(
        bootstrap_with=clauses,
        with_proof=True,
        use_timer=True,
    ) as solver:
        satisfiable = solver.solve()
        stats = solver.accum_stats()
        solver_cpu_seconds = solver.time_accum()
        if satisfiable:
            model = solver.get_model()
            proof: list[str] | None = None
        else:
            model = None
            proof = solver.get_proof()

    result: dict[str, object] = {
        "worker": WORKER_ID,
        "solver": "Glucose3",
        "pysat_version": pysat.__version__,
        "pysat_solvers_source": inspect.getfile(Glucose3),
        "status": "SAT" if satisfiable else "UNSAT",
        "cnf_sha256": cnf_sha256,
        "variable_count": variable_count,
        "clause_count": len(clauses),
        "runtime_seconds": time.monotonic() - started,
        "solver_cpu_seconds": solver_cpu_seconds,
        **stats,
    }
    if satisfiable:
        assert model is not None
        if not model_satisfies(model, clauses):
            raise AssertionError("Glucose model failed an independent clause check")
        result["true_variables"] = sorted(
            abs(literal) for literal in model if literal > 0
        )
        result["model_literal_count"] = len(model)
        result["proof_written"] = False
        return_code = 10
    else:
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

    print(json.dumps(result, sort_keys=True))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
