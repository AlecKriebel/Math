#!/usr/bin/env python3
"""Audit installed PySAT proof traces against independent DRAT/LRAT checkers."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


AUDIT_ID = "ramsey55_proof_solver_trace_audit_v1"
SOLVERS = (
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pigeonhole_cnf(pigeons: int, holes: int) -> str:
    def variable(pigeon: int, hole: int) -> int:
        return pigeon * holes + hole + 1

    clauses: list[tuple[int, ...]] = []
    for pigeon in range(pigeons):
        clauses.append(tuple(variable(pigeon, hole) for hole in range(holes)))
        for first, second in itertools.combinations(range(holes), 2):
            clauses.append(
                (-variable(pigeon, first), -variable(pigeon, second))
            )
    for hole in range(holes):
        for first, second in itertools.combinations(range(pigeons), 2):
            clauses.append((-variable(first, hole), -variable(second, hole)))
    lines = [f"p cnf {pigeons * holes} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return "\n".join(lines) + "\n"


def says_verified(output: str) -> bool:
    return any(
        "VERIFIED" in line and "NOT VERIFIED" not in line
        for line in output.splitlines()
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--pysat-path", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--lrat-check", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONPATH": str(args.pysat_path),
            "PYTHONHASHSEED": "0",
            "LC_ALL": "C",
        }
    )
    results: list[dict[str, object]] = []
    test_formula = pigeonhole_cnf(4, 3)
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory)
        cnf = temporary / "php4_3.cnf"
        cnf.write_text(test_formula, encoding="ascii")
        for solver in SOLVERS:
            proof = temporary / f"{solver}.drat"
            lrat = temporary / f"{solver}.lrat"
            started = time.monotonic()
            worker = subprocess.run(
                (
                    str(args.python),
                    str(root / "src" / "global_proof_worker.py"),
                    str(cnf),
                    "--solver",
                    solver,
                    "--proof",
                    str(proof),
                ),
                text=True,
                capture_output=True,
                check=False,
                timeout=30,
                env=environment,
            )
            record: dict[str, object] = {
                "solver": solver,
                "worker_returncode": worker.returncode,
                "worker_stderr": worker.stderr,
                "runtime_seconds": time.monotonic() - started,
            }
            if worker.stdout.strip():
                try:
                    record["worker_result"] = json.loads(worker.stdout)
                except json.JSONDecodeError:
                    record["worker_stdout"] = worker.stdout
            if worker.returncode == 20 and proof.is_file():
                drat = subprocess.run(
                    (
                        str(args.drat_trim),
                        str(cnf),
                        str(proof),
                        "-I",
                        "-L",
                        str(lrat),
                    ),
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=30,
                )
                record.update(
                    {
                        "proof_sha256": sha256(proof),
                        "proof_bytes": proof.stat().st_size,
                        "drat_trim_returncode": drat.returncode,
                        "drat_trim_valid": (
                            drat.returncode == 0
                            and says_verified(drat.stdout + drat.stderr)
                        ),
                        "drat_trim_output": drat.stdout + drat.stderr,
                    }
                )
                if record["drat_trim_valid"] and lrat.is_file():
                    checked = subprocess.run(
                        (str(args.lrat_check), str(cnf), str(lrat)),
                        text=True,
                        capture_output=True,
                        check=False,
                        timeout=30,
                    )
                    record.update(
                        {
                            "lrat_sha256": sha256(lrat),
                            "lrat_bytes": lrat.stat().st_size,
                            "lrat_check_returncode": checked.returncode,
                            "lrat_check_valid": (
                                checked.returncode == 0
                                and says_verified(
                                    checked.stdout + checked.stderr
                                )
                            ),
                        }
                    )
            results.append(record)

    approved_solvers = [
        str(record["solver"])
        for record in results
        if record.get("drat_trim_valid") is True
        and record.get("lrat_check_valid") is True
    ]
    excluded_solvers = [
        str(record["solver"])
        for record in results
        if record.get("solver") not in approved_solvers
    ]
    result = {
        "audit": AUDIT_ID,
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "acceptance_rule": (
            "worker returns UNSAT with a trace; drat-trim accepts the trace "
            "and emits LRAT; lrat-check accepts that LRAT"
        ),
        "approved_solvers": approved_solvers,
        "excluded_solvers": excluded_solvers,
        "pysat_version": "1.9.dev7",
        "pysat_path": str(args.pysat_path),
        "python_path": str(args.python),
        "python_sha256": sha256(args.python),
        "pysolvers_sha256": sha256(
            args.pysat_path / "pysolvers.cpython-311-darwin.so"
        ),
        "drat_trim_path": str(args.drat_trim),
        "drat_trim_sha256": sha256(args.drat_trim),
        "lrat_check_path": str(args.lrat_check),
        "lrat_check_sha256": sha256(args.lrat_check),
        "test_formula": "pigeonhole PHP(4,3), UNSAT without initial units",
        "test_formula_sha256": hashlib.sha256(
            test_formula.encode("ascii")
        ).hexdigest(),
        "audit_source_sha256": sha256(Path(__file__)),
        "worker_source_sha256": sha256(
            root / "src" / "global_proof_worker.py"
        ),
        "results": results,
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
