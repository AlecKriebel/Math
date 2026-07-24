#!/usr/bin/env python3
"""Exact coverage/status audit for the storage-capped k=2 pilot."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_catalog_batch import atomic_json, sha256_file  # noqa: E402
from core_completion_k2_pilot import (  # noqa: E402
    FAILED_SAT,
    LIMIT,
    OBSERVED_UNSAT,
    VERIFIED_SAT,
    parse_pairs,
)


CHECKER_ID = "ramsey55_core_completion_k2_pilot_coverage_v1"


def artifact_hashes_valid(record: dict[str, object]) -> bool:
    for path_key, hash_key in (
        ("model_path", "model_sha256"),
        ("candidate_graph6_path", "candidate_graph6_sha256"),
        ("candidate_canonical_path", "candidate_canonical_sha256"),
        ("verification_path", "verification_sha256"),
    ):
        path = Path(str(record.get(path_key)))
        if not path.is_file() or sha256_file(path) != record.get(hash_key):
            return False
    return True


def record_valid(record: dict[str, object]) -> bool:
    solver = record.get("solver_result")
    if not isinstance(solver, dict):
        return False
    selected = (
        int(record["catalog_line"]),
        int(record["deleted_left"]),
        int(record["deleted_right"]),
    )
    solver_selected = (
        solver.get("catalog_line"),
        solver.get("deleted_left"),
        solver.get("deleted_right"),
    )
    common = (
        selected == solver_selected
        and 1 <= selected[0] <= 328
        and 0 <= selected[1] < selected[2] < 42
        and solver.get("input_n") == 42
        and solver.get("core_n") == 40
        and solver.get("added_vertices") == 3
        and solver.get("variables") == 123
        and solver.get("clauses")
        == solver.get("negative_clauses", -1)
        + solver.get("positive_clauses", -1)
        and record.get("negative_certified") is False
        and record.get("proof_generated") is False
        and record.get("proof_checked") is False
    )
    classification = record.get("classification")
    if classification == OBSERVED_UNSAT:
        specific = (
            solver.get("status") == "UNSAT"
            and record.get("evidence_category")
            == "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        )
    elif classification == LIMIT:
        specific = (
            solver.get("status") == "LIMIT"
            and record.get("evidence_category")
            == "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        )
    elif classification == VERIFIED_SAT:
        specific = (
            solver.get("status") == "SAT"
            and record.get("dual_verified") is True
            and record.get("evidence_category") == "CERTIFIED"
            and artifact_hashes_valid(record)
        )
    elif classification == FAILED_SAT:
        specific = False
    else:
        specific = False
    return common and specific


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--solver", required=True, type=Path)
    parser.add_argument("--runner", required=True, type=Path)
    parser.add_argument("--pairs", required=True, type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    expected = [
        selected
        for path in args.pairs
        for selected in parse_pairs(path)
    ]
    records = summary.get("records")
    if not isinstance(records, list):
        raise SystemExit("summary has no record list")
    actual = [
        (
            int(record["catalog_line"]),
            int(record["deleted_left"]),
            int(record["deleted_right"]),
        )
        for record in records
    ]
    exact_coverage = (
        len(expected) == len(set(expected))
        and actual == expected
        and summary.get("expected_pair_count") == len(expected)
        and summary.get("actual_pair_count") == len(actual)
        and summary.get("exact_coverage") is True
    )
    records_valid = all(record_valid(record) for record in records)
    counts = {
        classification: sum(
            record.get("classification") == classification
            for record in records
        )
        for classification in (
            OBSERVED_UNSAT,
            VERIFIED_SAT,
            FAILED_SAT,
            LIMIT,
        )
    }
    pair_hashes = [sha256_file(path) for path in args.pairs]
    planned_shards = plan.get("shards")
    plan_pair_hashes = (
        [shard.get("pairs_sha256") for shard in planned_shards]
        if isinstance(planned_shards, list)
        else []
    )
    catalog_sha256 = sha256_file(args.catalog)
    solver_sha256 = sha256_file(args.solver)
    runner_sha256 = sha256_file(args.runner)
    plan_checks = {
        "catalog_sha256": plan.get("catalog_sha256") == catalog_sha256,
        "solver_binary_sha256": plan.get("solver_binary_sha256")
        == solver_sha256,
        "runner_source_sha256": plan.get("runner_source_sha256")
        == runner_sha256,
        "pair_hashes": plan_pair_hashes == pair_hashes,
        "pair_count": plan.get("pilot_pair_count") == len(expected),
    }
    output_dir = args.summary.parent
    output_bytes_before_audit = sum(
        path.stat().st_size
        for path in output_dir.rglob("*")
        if path.is_file() and path != args.output
    )
    resource_checks = {
        "output_cap": (
            summary.get("output_byte_cap") == plan.get("output_byte_cap")
            and output_bytes_before_audit <= plan.get("output_byte_cap", -1)
        ),
        "disk_preflight": (
            summary.get("free_disk_before_bytes", 0)
            >= plan.get("free_disk_reserve_bytes", 0)
            + plan.get("output_byte_cap", 0)
        ),
        "limits": (
            summary.get("seconds_limit_per_instance")
            == plan.get("seconds_limit_per_instance")
            and summary.get("node_limit_per_instance")
            == plan.get("node_limit_per_instance")
            and summary.get("max_wall_seconds")
            == plan.get("max_wall_seconds")
        ),
        "worker_errors": summary.get("worker_errors") == [],
        "negative_certified_count": (
            summary.get("negative_certified_count") == 0
        ),
        "proof_disabled": (
            summary.get("proof_generation") is False
            and summary.get("proof_replay") is False
        ),
        "counts": summary.get("counts")
        == {
            **counts,
            "PILOT_ERROR": 0,
        },
    }
    valid = (
        exact_coverage
        and records_valid
        and all(plan_checks.values())
        and all(resource_checks.values())
        and counts[FAILED_SAT] == 0
    )
    result = {
        "checker": CHECKER_ID,
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "valid": valid,
        "scope": (
            "exact selected delete-two/add-three fixed cores only; unchecked "
            "negative statuses are observations, not certificates or global"
        ),
        "catalog_sha256": catalog_sha256,
        "plan": str(args.plan.resolve()),
        "plan_sha256": sha256_file(args.plan),
        "summary": str(args.summary.resolve()),
        "summary_sha256": sha256_file(args.summary),
        "expected_pair_count": len(expected),
        "actual_pair_count": len(actual),
        "exact_coverage": exact_coverage,
        "duplicate_pair_count": len(actual) - len(set(actual)),
        "records_valid": records_valid,
        "classification_counts": counts,
        "negative_certified_count": 0,
        "plan_checks": plan_checks,
        "resource_checks": resource_checks,
        "output_bytes_before_audit": output_bytes_before_audit,
        "output_byte_cap": plan.get("output_byte_cap"),
        "runtime_seconds": time.monotonic() - started,
        "checker_source_sha256": sha256_file(Path(__file__)),
    }
    if args.output:
        if args.output.exists():
            raise SystemExit("coverage output already exists")
        atomic_json(args.output, result)
    print(json.dumps(result, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
