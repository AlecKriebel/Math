#!/usr/bin/env python3
"""Certify one-vertex nonextendibility for every graph in a graph6 catalog.

The producer and checker are separate executables with independent graph6
decoders, clause reconstruction, unit propagation, and proof traversal.  This
orchestrator enforces exact catalog coverage and records every proof hash.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


BATCH_ID = "ramsey55_catalog42_fixed_extension_batch_v1"
ROOT = Path(__file__).resolve().parents[1]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_single_json(
    completed: subprocess.CompletedProcess[str],
    label: str,
    allowed_returncodes: set[int] | None = None,
) -> dict:
    allowed = {0} if allowed_returncodes is None else allowed_returncodes
    if completed.returncode not in allowed:
        raise RuntimeError(
            f"{label} exited {completed.returncode}: {completed.stderr.strip()}"
        )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise RuntimeError(f"{label} did not emit exactly one JSON line")
    try:
        result = json.loads(lines[0])
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{label} emitted invalid JSON: {error}") from error
    if not isinstance(result, dict):
        raise RuntimeError(f"{label} JSON is not an object")
    return result


def solve_and_check(
    index: int,
    catalog: Path,
    proof_dir: Path,
    solver: Path,
    checker_python: Path,
    checker: Path,
    seconds_limit: float,
    reuse_existing_proofs: bool,
) -> dict:
    line_number = index + 1
    proof = proof_dir / f"line_{line_number:03d}.extdpll"
    existing_proof = proof.is_file()
    if existing_proof and not reuse_existing_proofs:
        raise RuntimeError(f"proof already exists at line {line_number}")
    replay_proof = proof_dir / f"line_{line_number:03d}.replay.extdpll"
    if replay_proof.exists():
        raise RuntimeError(f"stale replay proof exists at line {line_number}")
    solver_proof = replay_proof if existing_proof else proof
    solver_run = subprocess.run(
        (
            str(solver),
            "--graph",
            str(catalog),
            "--line",
            str(line_number),
            "--proof",
            str(solver_proof),
            "--seconds-limit",
            str(seconds_limit),
        ),
        check=False,
        capture_output=True,
        text=True,
    )
    solver_result = parse_single_json(
        solver_run,
        f"extension solver line {line_number}",
        allowed_returncodes={2, 10, 20},
    )
    status = solver_result.get("status")
    if solver_result.get("graph_line") != line_number:
        raise RuntimeError(f"solver line echo mismatch at {line_number}")
    record: dict[str, object] = {
        "catalog_index_zero_based": index,
        "catalog_line_one_based": line_number,
        "solver": solver_result,
        "proof_replay_identical": None,
    }
    if status == "SAT":
        if solver_proof.exists():
            raise RuntimeError(f"SAT line {line_number} left a proof artifact")
        if existing_proof:
            raise RuntimeError(
                f"replay found SAT but a retained proof exists at line {line_number}"
            )
        record["checker"] = None
        record["proof"] = None
        return record
    if status == "LIMIT":
        if solver_proof.exists():
            raise RuntimeError(f"limited line {line_number} left a proof artifact")
        if existing_proof:
            raise RuntimeError(
                f"replay hit LIMIT but a retained proof exists at line {line_number}"
            )
        record["checker"] = None
        record["proof"] = None
        return record
    if status != "UNSAT":
        raise RuntimeError(f"unknown solver status at line {line_number}: {status}")
    if not solver_proof.is_file():
        raise RuntimeError(f"UNSAT line {line_number} produced no proof")
    if existing_proof:
        replay_identical = solver_proof.read_bytes() == proof.read_bytes()
        solver_proof.unlink()
        if not replay_identical:
            raise RuntimeError(f"proof replay differs at line {line_number}")
        record["proof_replay_identical"] = True

    checker_run = subprocess.run(
        (
            str(checker_python),
            str(checker),
            "--graph",
            str(catalog),
            "--line",
            str(line_number),
            "--proof",
            str(proof),
        ),
        check=False,
        capture_output=True,
        text=True,
    )
    checker_result = parse_single_json(
        checker_run, f"extension checker line {line_number}"
    )
    if (
        checker_result.get("status") != "VERIFIED_UNSAT_FIXED_EXTENSION_CNF"
        or checker_result.get("graph_line") != line_number
        or checker_result.get("proof_sha256") != sha256_bytes(proof.read_bytes())
        or checker_result.get("clauses") != solver_result.get("clauses")
        or checker_result.get("tree_nodes") != solver_result.get("nodes")
        or checker_result.get("tree_leaves") != solver_result.get("leaves")
    ):
        raise RuntimeError(f"solver/checker disagreement at line {line_number}")
    record["checker"] = checker_result
    record["proof"] = {
        "path": str(proof),
        "bytes": proof.stat().st_size,
        "sha256": checker_result["proof_sha256"],
    }
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--proof-dir", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=328)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--seconds-limit", type=float, default=60.0)
    parser.add_argument(
        "--solver",
        type=Path,
        default=ROOT / "build" / "extension_sat_proof_solver",
    )
    parser.add_argument(
        "--checker",
        type=Path,
        default=ROOT / "verify" / "extension_sat_proof_check.py",
    )
    parser.add_argument("--checker-python", type=Path, default=Path(sys.executable))
    parser.add_argument(
        "--reuse-existing-proofs",
        action="store_true",
        help=(
            "retain an exact pre-existing proof set, reproduce every proof into a "
            "temporary file, require byte-for-byte identity, and then check it"
        ),
    )
    args = parser.parse_args()
    if args.jobs < 1 or args.seconds_limit <= 0:
        parser.error("--jobs and --seconds-limit must be positive")
    if (
        not args.reuse_existing_proofs
        and args.proof_dir.exists()
        and any(args.proof_dir.iterdir())
    ):
        raise SystemExit("proof directory exists and is not empty")

    started = time.monotonic()
    catalog_bytes = args.catalog.read_bytes()
    catalog_sha256 = sha256_bytes(catalog_bytes)
    if catalog_sha256 != args.expected_sha256:
        raise SystemExit("catalog SHA-256 mismatch")
    lines = [
        line.strip()
        for line in catalog_bytes.decode("ascii").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if len(lines) != args.expected_count or len(set(lines)) != len(lines):
        raise SystemExit("catalog count or uniqueness check failed")
    args.proof_dir.mkdir(parents=True, exist_ok=True)
    expected_proof_names = {
        f"line_{line_number:03d}.extdpll"
        for line_number in range(1, len(lines) + 1)
    }
    if args.reuse_existing_proofs:
        actual_proof_names = {
            path.name for path in args.proof_dir.iterdir() if path.is_file()
        }
        if actual_proof_names != expected_proof_names:
            missing = sorted(expected_proof_names - actual_proof_names)
            unexpected = sorted(actual_proof_names - expected_proof_names)
            raise SystemExit(
                "existing proof set is not exact: "
                f"missing={missing[:5]} unexpected={unexpected[:5]}"
            )

    records: list[dict | None] = [None] * len(lines)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(
                solve_and_check,
                index,
                args.catalog,
                args.proof_dir,
                args.solver,
                args.checker_python,
                args.checker,
                args.seconds_limit,
                args.reuse_existing_proofs,
            ): index
            for index in range(len(lines))
        }
        for future in concurrent.futures.as_completed(futures):
            index = futures[future]
            records[index] = future.result()
    complete = [record for record in records if record is not None]
    statuses = [record["solver"]["status"] for record in complete]
    unsat_count = statuses.count("UNSAT")
    sat_count = statuses.count("SAT")
    limit_count = statuses.count("LIMIT")
    proofs = [record["proof"] for record in complete if record["proof"] is not None]
    result = {
        "batch": BATCH_ID,
        "status": (
            "SAT_FOUND"
            if sat_count
            else "CERTIFIED_ALL_FIXED_EXTENSIONS_UNSAT"
            if unsat_count == len(lines)
            else "INCOMPLETE"
        ),
        "catalog_path": str(args.catalog),
        "catalog_sha256": catalog_sha256,
        "catalog_graph_count": len(lines),
        "coverage_lines_one_based": [record["catalog_line_one_based"] for record in complete],
        "coverage_exact": [record["catalog_line_one_based"] for record in complete]
        == list(range(1, len(lines) + 1)),
        "sat_count": sat_count,
        "unsat_count": unsat_count,
        "limit_count": limit_count,
        "checked_unsat_count": sum(record["checker"] is not None for record in complete),
        "proof_count": len(proofs),
        "proof_bytes_total": sum(proof["bytes"] for proof in proofs),
        "proof_bundle_sha256": sha256_bytes(
            "".join(proof["sha256"] + "\n" for proof in proofs).encode("ascii")
        ),
        "solver_nodes_total": sum(record["solver"]["nodes"] for record in complete),
        "solver_leaves_total": sum(record["solver"]["leaves"] for record in complete),
        "solver_unit_assignments_total": sum(
            record["solver"]["unit_assignments"] for record in complete
        ),
        "solver_elapsed_seconds_sum": sum(
            record["solver"]["elapsed_seconds"] for record in complete
        ),
        "checker_elapsed_seconds_sum": sum(
            record["checker"]["checker_elapsed_seconds"]
            for record in complete
            if record["checker"] is not None
        ),
        "reuse_existing_proofs": args.reuse_existing_proofs,
        "proof_replay_identical_count": sum(
            record["proof_replay_identical"] is True for record in complete
        ),
        "wall_seconds": time.monotonic() - started,
        "jobs": args.jobs,
        "seconds_limit_per_instance": args.seconds_limit,
        "solver_path": str(args.solver),
        "solver_sha256": sha256_bytes(args.solver.read_bytes()),
        "checker_path": str(args.checker),
        "checker_sha256": sha256_bytes(args.checker.read_bytes()),
        "records": complete,
    }
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "batch": BATCH_ID,
                "status": result["status"],
                "sat_count": sat_count,
                "unsat_count": unsat_count,
                "limit_count": limit_count,
                "wall_seconds": result["wall_seconds"],
                "result": str(args.result),
            },
            sort_keys=True,
        )
    )
    if sat_count:
        return 10
    return 0 if result["status"] == "CERTIFIED_ALL_FIXED_EXTENSIONS_UNSAT" else 2


if __name__ == "__main__":
    raise SystemExit(main())
