#!/usr/bin/env python3
"""Generic pinned Glucose3 -> DRAT -> LRAT certification pipeline."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from residual_completion import (  # noqa: E402
    DEFAULT_DRAT_TRIM,
    DEFAULT_LRAT_CHECK,
    DEFAULT_PYSAT_PATH,
    DEFAULT_PYTHON,
    PINNED_HASHES,
    PINNED_PYSAT_VERSION,
    Toolchain,
    WorkflowError,
    checker_says_verified,
    parse_single_json_line,
    run_bounded,
    sha256_file,
    verify_toolchain,
    write_json,
)


PIPELINE_ID = "ramsey55_pinned_glucose_drat_lrat_pipeline_v1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--lrat", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=600.0)
    parser.add_argument("--proof-check-time-limit", type=float, default=1200.0)
    parser.add_argument("--python", type=Path, default=DEFAULT_PYTHON)
    parser.add_argument("--pysat-path", type=Path, default=DEFAULT_PYSAT_PATH)
    parser.add_argument("--drat-trim", type=Path, default=DEFAULT_DRAT_TRIM)
    parser.add_argument("--lrat-check", type=Path, default=DEFAULT_LRAT_CHECK)
    args = parser.parse_args()
    if args.time_limit <= 0 or args.proof_check_time_limit <= 0:
        raise WorkflowError("time limits must be positive")

    toolchain = Toolchain(
        args.python,
        args.pysat_path,
        args.drat_trim,
        args.lrat_check,
        PINNED_HASHES,
    )
    tool_metadata = verify_toolchain(toolchain)
    cnf_sha256 = sha256_file(args.cnf)
    args.proof.unlink(missing_ok=True)
    args.lrat.unlink(missing_ok=True)
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONPATH": str(toolchain.pysat_path),
            "PYTHONHASHSEED": "0",
            "LC_ALL": "C",
        }
    )
    worker = ROOT / "src" / "residual_completion_glucose.py"
    state, solved, solve_wall = run_bounded(
        (
            str(toolchain.python),
            str(worker),
            str(args.cnf),
            "--proof",
            str(args.proof),
        ),
        timeout=args.time_limit,
        environment=environment,
    )
    base = {
        "pipeline": PIPELINE_ID,
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": cnf_sha256,
        "time_limit_seconds": args.time_limit,
        "proof_check_time_limit_seconds": args.proof_check_time_limit,
        "toolchain": tool_metadata,
        "solver_wall_seconds": solve_wall,
    }
    if state == "TIMEOUT":
        args.proof.unlink(missing_ok=True)
        args.lrat.unlink(missing_ok=True)
        result = {
            **base,
            "status": "TIMEOUT",
            "proof_written": False,
            "lrat_written": False,
        }
        write_json(args.result, result)
        print(json.dumps(result, sort_keys=True))
        return 2

    assert solved is not None
    if solved.returncode not in {10, 20}:
        raise WorkflowError(
            f"Glucose worker failed ({solved.returncode}): {solved.stderr}"
        )
    solver_result = parse_single_json_line(solved.stdout)
    if (
        solver_result.get("cnf_sha256") != cnf_sha256
        or solver_result.get("pysat_version") != PINNED_PYSAT_VERSION
    ):
        raise WorkflowError("worker runtime or CNF fingerprint mismatch")
    if solved.returncode == 10:
        result = {
            **base,
            "status": "SAT",
            "solver_result": solver_result,
            "true_variables": solver_result["true_variables"],
            "proof_written": False,
            "lrat_written": False,
        }
        write_json(args.result, result)
        print(json.dumps(result, sort_keys=True))
        return 10

    if not args.proof.is_file():
        raise WorkflowError("UNSAT worker produced no proof file")
    proof_sha256 = sha256_file(args.proof)
    if solver_result.get("proof_sha256") != proof_sha256:
        raise WorkflowError("worker proof hash mismatch")
    drat_state, drat, drat_wall = run_bounded(
        (
            str(toolchain.drat_trim),
            str(args.cnf),
            str(args.proof),
            "-I",
            "-L",
            str(args.lrat),
        ),
        timeout=args.proof_check_time_limit,
    )
    drat_valid = (
        drat_state == "COMPLETED"
        and drat is not None
        and drat.returncode == 0
        and checker_says_verified(drat.stdout + drat.stderr)
    )
    lrat = None
    lrat_wall = None
    lrat_valid = False
    if drat_valid and args.lrat.is_file():
        lrat_state, lrat, lrat_wall = run_bounded(
            (
                str(toolchain.lrat_check),
                str(args.cnf),
                str(args.lrat),
            ),
            timeout=args.proof_check_time_limit,
        )
        lrat_valid = (
            lrat_state == "COMPLETED"
            and lrat is not None
            and lrat.returncode == 0
            and checker_says_verified(lrat.stdout + lrat.stderr)
        )
    status = "CERTIFIED_UNSAT" if drat_valid and lrat_valid else "UNSAT_UNCERTIFIED"
    result = {
        **base,
        "status": status,
        "solver_result": solver_result,
        "proof_written": args.proof.is_file(),
        "proof_path": str(args.proof.resolve()),
        "proof_sha256": proof_sha256,
        "proof_bytes": args.proof.stat().st_size,
        "drat_trim_valid": drat_valid,
        "drat_trim_wall_seconds": drat_wall,
        "drat_trim_returncode": drat.returncode if drat is not None else None,
        "drat_trim_stdout": drat.stdout if drat is not None else None,
        "drat_trim_stderr": drat.stderr if drat is not None else None,
        "lrat_written": args.lrat.is_file(),
        "lrat_path": str(args.lrat.resolve()),
        "lrat_sha256": sha256_file(args.lrat) if args.lrat.is_file() else None,
        "lrat_bytes": args.lrat.stat().st_size if args.lrat.is_file() else None,
        "lrat_check_valid": lrat_valid,
        "lrat_check_wall_seconds": lrat_wall,
        "lrat_check_returncode": lrat.returncode if lrat is not None else None,
        "lrat_check_stdout": lrat.stdout if lrat is not None else None,
        "lrat_check_stderr": lrat.stderr if lrat is not None else None,
    }
    write_json(args.result, result)
    print(json.dumps(result, sort_keys=True))
    return 20 if status == "CERTIFIED_UNSAT" else 3


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except WorkflowError as error:
        print(
            json.dumps(
                {"pipeline": PIPELINE_ID, "status": "ERROR", "error": str(error)},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)
