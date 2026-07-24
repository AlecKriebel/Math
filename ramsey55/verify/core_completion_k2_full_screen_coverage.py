#!/usr/bin/env python3
"""Independent exact-coverage audit for the full compact k=2 screen."""

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
from core_completion_k2_compact import (  # noqa: E402
    HEADER_BYTES,
    PAIRS_PER_LINE,
    RECORD_BYTES,
    validate_file,
)


CHECKER_ID = "ramsey55_core_completion_catalog_k2_full_coverage_v1"
OBSERVED_UNSAT = "OBSERVED_UNSAT_UNCHECKED"
LIMIT = "LIMIT_NO_CONCLUSION"


def output_bytes(path: Path, excluded: Path | None = None) -> int:
    return sum(
        item.stat().st_size
        for item in path.rglob("*")
        if item.is_file() and item != excluded
    )


def shard_filename(shard: dict[str, object]) -> str:
    return (
        f"shard_{int(shard['shard']):02d}_lines_"
        f"{int(shard['line_start']):03d}_{int(shard['line_end']):03d}"
        ".k2scrn"
    )


def check_plan_shards(
    plan: dict[str, object],
) -> tuple[list[dict[str, object]], bool]:
    raw_shards = plan.get("shards")
    if not isinstance(raw_shards, list):
        return [], False
    shards: list[dict[str, object]] = []
    expected_start = 1
    valid = True
    for expected_id, raw in enumerate(raw_shards):
        if not isinstance(raw, dict):
            return [], False
        shard = dict(raw)
        start = int(shard.get("line_start", 0))
        end = int(shard.get("line_end", 0))
        pair_count = int(shard.get("pair_count", -1))
        record_bytes = int(shard.get("record_bytes", -1))
        expected_pairs = (end - start + 1) * PAIRS_PER_LINE
        expected_bytes = HEADER_BYTES + expected_pairs * RECORD_BYTES
        valid = valid and (
            int(shard.get("shard", -1)) == expected_id
            and start == expected_start
            and end >= start
            and pair_count == expected_pairs
            and record_bytes == expected_bytes
        )
        expected_start = end + 1
        shards.append(shard)
    valid = valid and expected_start == 329 and len(shards) == 4
    valid = valid and sum(int(item["pair_count"]) for item in shards) == 282_408
    valid = valid and (
        sum(int(item["record_bytes"]) for item in shards)
        == plan.get("expected_binary_bytes")
    )
    return shards, valid


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--producer-source", required=True, type=Path)
    parser.add_argument("--included-solver-source", required=True, type=Path)
    parser.add_argument("--solver", required=True, type=Path)
    parser.add_argument("--parser-source", required=True, type=Path)
    parser.add_argument("--runner", required=True, type=Path)
    parser.add_argument("--python-executable", required=True, type=Path)
    parser.add_argument("--exhaustive-verifier", required=True, type=Path)
    parser.add_argument("--bitset-verifier", required=True, type=Path)
    parser.add_argument("--catalog-audit", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    plan_sha256 = sha256_file(args.plan)
    shards, plan_shards_valid = check_plan_shards(plan)
    catalog_sha256 = sha256_file(args.catalog)
    hash_checks = {
        "catalog": plan.get("catalog_sha256") == catalog_sha256,
        "catalog_audit": plan.get("catalog_dual_verification_sha256")
        == sha256_file(args.catalog_audit),
        "producer_source": plan.get("producer_source_sha256")
        == sha256_file(args.producer_source),
        "included_solver_source": plan.get("included_solver_source_sha256")
        == sha256_file(args.included_solver_source),
        "producer_binary": plan.get("producer_binary_sha256")
        == sha256_file(args.solver),
        "independent_parser": plan.get("independent_parser_sha256")
        == sha256_file(args.parser_source),
        "runner": plan.get("runner_source_sha256")
        == sha256_file(args.runner),
        "coverage_checker": plan.get("coverage_checker_sha256")
        == sha256_file(Path(__file__)),
        "python_executable": plan.get("python_executable_sha256")
        == sha256_file(args.python_executable),
        "exhaustive_sat_verifier": plan.get(
            "exhaustive_sat_verifier_sha256"
        )
        == sha256_file(args.exhaustive_verifier),
        "bitset_sat_verifier": plan.get("bitset_sat_verifier_sha256")
        == sha256_file(args.bitset_verifier),
    }

    shard_audits: list[dict[str, object]] = []
    shard_errors: list[dict[str, object]] = []
    unsat_count = 0
    limit_count = 0
    total_records = 0
    total_binary_bytes = 0
    summary_shards = summary.get("shards")
    summary_by_id = (
        {
            int(item["shard"]): item
            for item in summary_shards
            if isinstance(item, dict) and "shard" in item
        }
        if isinstance(summary_shards, list)
        else {}
    )
    for shard in shards:
        shard_id = int(shard["shard"])
        records = args.summary.parent / "shards" / shard_filename(shard)
        result_path = records.with_name(records.stem + ".result.json")
        try:
            audit = validate_file(
                records,
                expected_range=(
                    int(shard["line_start"]),
                    int(shard["line_end"]),
                ),
                expected_catalog_sha256=catalog_sha256,
                node_limit=int(plan["node_limit_per_instance"]),
            )
            result = json.loads(result_path.read_text(encoding="utf-8"))
            result_valid = (
                result.get("status") == "COMPLETE"
                and result.get("shard") == shard_id
                and result.get("line_start") == shard["line_start"]
                and result.get("line_end") == shard["line_end"]
                and result.get("record_count") == audit["record_count"]
                and result.get("unsat_count") == audit["unsat_count"]
                and result.get("limit_count") == audit["limit_count"]
                and result.get("record_bytes") == audit["record_bytes"]
                and result.get("records_sha256") == audit["sha256"]
                and result.get("plan_sha256") == plan_sha256
                and result.get("negative_certified_count") == 0
                and result.get("proof_generated") is False
                and result.get("proof_checked") is False
                and summary_by_id.get(shard_id) == result
            )
            if not result_valid:
                raise ValueError("shard result/summary mismatch")
        except Exception as error:
            shard_errors.append(
                {
                    "shard": shard_id,
                    "error": f"{type(error).__name__}: {error}",
                }
            )
            continue
        shard_audits.append(
            {
                "shard": shard_id,
                "line_start": audit["line_start"],
                "line_end": audit["line_end"],
                "record_count": audit["record_count"],
                "unsat_count": audit["unsat_count"],
                "limit_count": audit["limit_count"],
                "record_bytes": audit["record_bytes"],
                "records_sha256": audit["sha256"],
                "total_nodes": audit["total_nodes"],
                "max_nodes": audit["max_nodes"],
                "max_elapsed_microseconds": audit[
                    "max_elapsed_microseconds"
                ],
                "result": str(result_path.resolve()),
                "result_sha256": sha256_file(result_path),
            }
        )
        total_records += int(audit["record_count"])
        unsat_count += int(audit["unsat_count"])
        limit_count += int(audit["limit_count"])
        total_binary_bytes += int(audit["record_bytes"])

    exact_coverage = (
        plan_shards_valid
        and not shard_errors
        and len(shard_audits) == 4
        and total_records == 282_408
        and unsat_count + limit_count == total_records
        and total_binary_bytes == plan.get("expected_binary_bytes")
    )
    expected_counts = {
        OBSERVED_UNSAT: unsat_count,
        LIMIT: limit_count,
        "DUAL_VERIFIED_SAT_CONSTRUCTION": 0,
        "SAT_MODEL_VERIFICATION_FAILED": 0,
        "ERROR": 0,
    }
    summary_checks = {
        "complete": summary.get("status") == "COMPLETE",
        "plan_sha256": summary.get("plan_sha256") == plan_sha256,
        "catalog_sha256": summary.get("catalog_sha256") == catalog_sha256,
        "limits": (
            summary.get("jobs") == plan.get("jobs")
            and summary.get("seconds_limit_per_instance")
            == plan.get("seconds_limit_per_instance")
            and summary.get("node_limit_per_instance")
            == plan.get("node_limit_per_instance")
            and summary.get("max_wall_seconds")
            == plan.get("max_wall_seconds")
            and float(summary.get("runtime_seconds", float("inf")))
            <= float(plan.get("max_wall_seconds", -1))
        ),
        "coverage": (
            summary.get("expected_pair_count") == 282_408
            and summary.get("actual_pair_count") == total_records
            and summary.get("exact_pair_coverage") is True
        ),
        "binary_bytes": (
            summary.get("expected_binary_bytes")
            == plan.get("expected_binary_bytes")
            and summary.get("actual_binary_bytes") == total_binary_bytes
        ),
        "counts": summary.get("counts") == expected_counts,
        "negative_policy": (
            summary.get("negative_certified_count") == 0
            and summary.get("proof_generation") is False
            and summary.get("proof_replay") is False
        ),
    }
    before_audit_bytes = output_bytes(args.summary.parent, args.output)
    existing_at_launch = int(summary.get("existing_bytes_at_launch", -1))
    required_free_at_launch = int(
        summary.get("required_free_at_launch_bytes", -1)
    )
    expected_required_free = int(plan["free_disk_reserve_bytes"]) + max(
        0, int(plan["output_byte_cap"]) - existing_at_launch
    )
    resource_checks = {
        "output_cap": (
            summary.get("output_byte_cap") == plan.get("output_byte_cap")
            and before_audit_bytes <= int(plan["output_byte_cap"])
        ),
        "disk_preflight": (
            existing_at_launch >= 0
            and required_free_at_launch == expected_required_free
            and int(summary.get("free_disk_before_bytes", -1))
            >= required_free_at_launch
        ),
        "reserve": summary.get("free_disk_reserve_bytes")
        == plan.get("free_disk_reserve_bytes"),
        "worst_case_size": int(plan["worst_case_retained_output_bytes"])
        <= int(plan["output_byte_cap"]),
    }
    valid = (
        exact_coverage
        and all(hash_checks.values())
        and all(summary_checks.values())
        and all(resource_checks.values())
    )
    result = {
        "schema": "ramsey55.core_completion_catalog_k2_full_coverage.v1",
        "checker": CHECKER_ID,
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "valid": valid,
        "evidence_category": "INDEPENDENT EXECUTION AND COVERAGE AUDIT",
        "scope": (
            "exact delete-two/add-three fixed catalog cores only; unchecked "
            "negative statuses are observations, not certificates or a "
            "global Ramsey-bound conclusion"
        ),
        "plan": str(args.plan.resolve()),
        "plan_sha256": plan_sha256,
        "summary": str(args.summary.resolve()),
        "summary_sha256": sha256_file(args.summary),
        "catalog_sha256": catalog_sha256,
        "expected_pair_count": 282_408,
        "actual_pair_count": total_records,
        "exact_pair_coverage": exact_coverage,
        "duplicate_pair_count": 0 if exact_coverage else None,
        "classification_counts": expected_counts,
        "negative_certified_count": 0,
        "proof_generation": False,
        "proof_replay": False,
        "expected_binary_bytes": plan.get("expected_binary_bytes"),
        "actual_binary_bytes": total_binary_bytes,
        "shard_audits": shard_audits,
        "shard_errors": shard_errors,
        "plan_shards_valid": plan_shards_valid,
        "hash_checks": hash_checks,
        "summary_checks": summary_checks,
        "resource_checks": resource_checks,
        "output_bytes_before_audit": before_audit_bytes,
        "output_byte_cap": plan.get("output_byte_cap"),
        "runtime_seconds": time.monotonic() - started,
        "checker_source_sha256": sha256_file(Path(__file__)),
    }
    if args.output:
        if args.output.exists():
            raise SystemExit("coverage output already exists")
        atomic_json(args.output, result)
        if output_bytes(args.summary.parent) > int(plan["output_byte_cap"]):
            raise SystemExit("coverage output caused output-cap breach")
    print(json.dumps(result, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
