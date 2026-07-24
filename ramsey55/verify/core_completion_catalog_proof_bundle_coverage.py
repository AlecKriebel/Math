#!/usr/bin/env python3
"""Audit exact certified coverage from replayed fixed-core proof bundles."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "src"))

from core_completion_catalog_batch import atomic_json, sha256_file  # noqa: E402
from core_completion_catalog_proof_bundle_run import (  # noqa: E402
    parse_json_lines,
    parse_pairs,
)


CHECKER_ID = "ramsey55_core_completion_catalog_proof_bundle_coverage_v1"
VERIFIED_STATUS = (
    "VERIFIED_UNSAT_FIXED_41_CORE_TWO_VERTEX_COMPLETION"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--producer", required=True, type=Path)
    parser.add_argument("--checker", required=True, type=Path)
    parser.add_argument("--pairs", required=True, type=Path, nargs="+")
    parser.add_argument("--results", required=True, type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    if len(args.pairs) != len(args.results):
        raise SystemExit("--pairs and --results must have equal lengths")

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    catalog_sha256 = sha256_file(args.catalog)
    producer_sha256 = sha256_file(args.producer)
    checker_sha256 = sha256_file(args.checker)
    expected: list[tuple[int, int]] = []
    pair_hashes: list[str] = []
    for path in args.pairs:
        expected.extend(parse_pairs(path))
        pair_hashes.append(sha256_file(path))
    expected_unique = len(expected) == len(set(expected))

    producer_records: list[dict[str, object]] = []
    checker_records: list[dict[str, object]] = []
    artifact_checks: list[dict[str, object]] = []
    result_checks: list[dict[str, object]] = []
    for pairs_path, result_path in zip(args.pairs, args.results):
        shard_pairs = parse_pairs(pairs_path)
        result = json.loads(result_path.read_text(encoding="utf-8"))
        checks = {
            "status": result.get("status")
            == "CERTIFIED_UNSAT_FIXED_CORE_BUNDLE",
            "catalog_sha256": result.get("catalog_sha256")
            == catalog_sha256,
            "pairs_sha256": result.get("pairs_sha256")
            == sha256_file(pairs_path),
            "expected_pair_count": result.get("expected_pair_count")
            == len(shard_pairs),
            "producer_pair_count": result.get("producer_pair_count")
            == len(shard_pairs),
            "producer_returncode": result.get("producer_returncode") == 0,
            "producer_sha256": result.get("producer_sha256")
            == producer_sha256,
            "checker_sha256": result.get("checker_sha256")
            == checker_sha256,
            "no_sat_verification": result.get("sat_verifications") == [],
        }
        shard_producer = result.get("producer_records")
        if not isinstance(shard_producer, list):
            shard_producer = []
        producer_records.extend(shard_producer)
        artifacts = result.get("artifacts")
        if not isinstance(artifacts, dict):
            artifacts = {}
        shard_artifact_checks: dict[str, object] = {}
        for label in (
            "bundle",
            "producer_transcript",
            "checker_transcript",
        ):
            path = Path(str(artifacts.get(label)))
            shard_artifact_checks[label] = (
                path.is_file()
                and sha256_file(path) == artifacts.get(f"{label}_sha256")
                and path.stat().st_size == artifacts.get(f"{label}_bytes")
            )
        bundle_limit = plan.get("bundle_byte_limit_per_shard")
        checks["bundle_byte_limit"] = (
            bundle_limit is None
            or (
                isinstance(bundle_limit, int)
                and int(artifacts.get("bundle_bytes", -1))
                <= bundle_limit
            )
        )
        checks["resource_limits"] = (
            result.get("seconds_limit_per_instance")
            == plan.get("seconds_limit_per_instance")
            and result.get("node_limit_per_instance")
            == plan.get("node_limit_per_instance")
            and (
                bundle_limit is None
                or result.get("bundle_byte_limit") == bundle_limit
            )
            and (
                plan.get("max_wall_seconds") is None
                or result.get("max_wall_seconds")
                == plan.get("max_wall_seconds")
            )
        )
        transcript = Path(str(artifacts.get("checker_transcript")))
        shard_checker = (
            parse_json_lines(
                transcript.read_text(encoding="utf-8"),
                "checker transcript",
            )
            if transcript.is_file()
            else []
        )
        checker_records.extend(shard_checker)
        checks["checker_transcript_count"] = (
            len(shard_checker) == len(shard_pairs)
        )
        checker_summary = result.get("checker_result")
        checks["checker_summary"] = (
            isinstance(checker_summary, dict)
            and checker_summary.get("status")
            == "VERIFIED_UNSAT_FIXED_CORE_BUNDLE"
            and checker_summary.get("pair_count") == len(shard_pairs)
            and checker_summary.get("tree_nodes_total")
            == sum(
                int(record.get("tree_nodes", -1))
                for record in shard_checker
            )
            and checker_summary.get("tree_leaves_total")
            == sum(
                int(record.get("tree_leaves", -1))
                for record in shard_checker
            )
            and checker_summary.get("proof_bytes_total")
            == sum(
                int(record.get("proof_bytes", -1))
                for record in shard_checker
            )
        )
        result_checks.append(
            {
                "result": str(result_path.resolve()),
                "result_sha256": sha256_file(result_path),
                "valid": all(checks.values()),
                "checks": checks,
            }
        )
        artifact_checks.append(
            {
                "result": str(result_path.resolve()),
                "valid": all(shard_artifact_checks.values()),
                "checks": shard_artifact_checks,
            }
        )

    producer_pairs = [
        (int(record["catalog_line"]), int(record["deleted_vertex"]))
        for record in producer_records
    ]
    checker_pairs = [
        (int(record["catalog_line"]), int(record["deleted_vertex"]))
        for record in checker_records
    ]
    pairwise_agreement = (
        len(producer_records) == len(checker_records)
        and all(
            (
                int(produced["catalog_line"]),
                int(produced["deleted_vertex"]),
                int(produced["proof_bytes"]),
                int(produced["clauses"]),
                int(produced["nodes"]),
                int(produced["branches"]),
                int(produced["leaves"]),
            )
            == (
                int(checked["catalog_line"]),
                int(checked["deleted_vertex"]),
                int(checked["proof_bytes"]),
                int(checked["clauses"]),
                int(checked["tree_nodes"]),
                int(checked["tree_branches"]),
                int(checked["tree_leaves"]),
            )
            for produced, checked in zip(
                producer_records, checker_records
            )
        )
    )
    exact_coverage = (
        expected_unique
        and producer_pairs == expected
        and checker_pairs == expected
    )
    statuses_valid = (
        all(record.get("status") == "UNSAT" for record in producer_records)
        and all(
            record.get("status") == VERIFIED_STATUS
            for record in checker_records
        )
    )
    plan_hashes = {
        str(value)
        for value in (
            plan.get("pairs_sha256"),
            plan.get("sample_pairs_sha256"),
        )
        if value is not None
    }
    plan_hashes.update(
        str(shard.get("pairs_sha256"))
        for shard in plan.get("shards", [])
        if isinstance(shard, dict) and shard.get("pairs_sha256")
    )
    plan_checks = {
        "catalog_sha256": plan.get("catalog_sha256") == catalog_sha256,
        "producer_binary_sha256": plan.get("producer_binary_sha256")
        == producer_sha256,
        "checker_binary_sha256": plan.get("checker_binary_sha256")
        == checker_sha256,
        "pair_hashes": all(value in plan_hashes for value in pair_hashes),
    }
    full_catalog = [
        (line, deleted)
        for line in range(1, 329)
        for deleted in range(42)
    ]
    valid = (
        all(item["valid"] for item in result_checks)
        and all(item["valid"] for item in artifact_checks)
        and all(plan_checks.values())
        and exact_coverage
        and statuses_valid
        and pairwise_agreement
    )
    result = {
        "checker": CHECKER_ID,
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "valid": valid,
        "evidence_category": "CERTIFIED",
        "scope": (
            "exact independently replayed fixed-core pair set only; this is "
            "not global order-43 nonexistence and changes no Ramsey bound"
        ),
        "catalog": str(args.catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "plan": str(args.plan.resolve()),
        "plan_sha256": sha256_file(args.plan),
        "expected_pair_count": len(expected),
        "producer_pair_count": len(producer_pairs),
        "checker_pair_count": len(checker_pairs),
        "certified_pair_count": (
            len(checker_pairs) if valid else 0
        ),
        "expected_pairs_unique": expected_unique,
        "exact_coverage": exact_coverage,
        "statuses_valid": statuses_valid,
        "producer_checker_pairwise_agreement": pairwise_agreement,
        "full_catalog_coverage": expected == full_catalog,
        "missing_from_full_catalog_count": len(
            set(full_catalog) - set(expected)
        ),
        "extra_outside_full_catalog_count": len(
            set(expected) - set(full_catalog)
        ),
        "plan_checks": plan_checks,
        "result_checks": result_checks,
        "artifact_checks": artifact_checks,
        "proof_bytes_total": sum(
            int(record["proof_bytes"]) for record in checker_records
        ),
        "tree_nodes_total": sum(
            int(record["tree_nodes"]) for record in checker_records
        ),
        "tree_leaves_total": sum(
            int(record["tree_leaves"]) for record in checker_records
        ),
        "runtime_seconds": time.monotonic() - started,
        "checker_source_sha256": sha256_file(Path(__file__)),
    }
    if args.output:
        if args.output.exists():
            raise SystemExit("coverage output already exists")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        atomic_json(args.output, result)
    print(json.dumps(result, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
