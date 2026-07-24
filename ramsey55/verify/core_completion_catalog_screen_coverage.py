#!/usr/bin/env python3
"""Enforce exact pair/status coverage for the non-certifying catalog screen."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path


CHECKER_ID = "ramsey55_core_completion_catalog_screen_coverage_v1"
OBSERVED_UNSAT = "OBSERVED_UNSAT_UNCHECKED"
VERIFIED_SAT = "DUAL_VERIFIED_SAT_CONSTRUCTION"
FAILED_SAT = "SAT_MODEL_VERIFICATION_FAILED"
LIMIT = "LIMIT_NO_CONCLUSION"
ERROR = "SCREEN_ERROR"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def pair(record: dict[str, object]) -> tuple[int, int]:
    return int(record["catalog_line"]), int(record["deleted_vertex"])


def check_record(
    record: dict[str, object],
    *,
    catalog_sha256: str,
    solver_sha256: str,
    catalog_lines: int,
) -> dict[str, object]:
    line, deleted = pair(record)
    classification = record.get("classification")
    solver = record.get("solver_result")
    returncode = record.get(
        "solver_returncode", record.get("solver_returncode_semantics")
    )
    record_artifact = Path(str(record.get("record_path")))
    artifact_valid = (
        record_artifact.is_file()
        and sha256_file(record_artifact) == record.get("record_sha256")
    )
    artifact_matches_summary = False
    if artifact_valid:
        artifact_record = json.loads(
            record_artifact.read_text(encoding="utf-8")
        )
        summary_record = {
            key: value
            for key, value in record.items()
            if key not in ("record_path", "record_sha256", "resumed")
        }
        artifact_matches_summary = artifact_record == summary_record
    solver_shape = (
        isinstance(solver, dict)
        and solver.get("catalog_line") == line
        and solver.get("deleted_vertex") == deleted
        and solver.get("input_n") == 42
        and solver.get("core_n") == 41
        and solver.get("variables") == 83
        and solver.get("core_k5") == 0
        and solver.get("core_i5") == 0
        and solver.get("clauses")
        == solver.get("negative_clauses", -1)
        + solver.get("positive_clauses", -1)
    )
    common = {
        "catalog_hash": record.get("catalog_sha256") == catalog_sha256,
        "solver_hash": record.get("solver_sha256") == solver_sha256,
        "pair_range": 1 <= line <= catalog_lines and 0 <= deleted < 42,
        "negative_not_certified": record.get("negative_certified") is False,
        "record_artifact_hash": artifact_valid,
        "record_artifact_matches_summary": artifact_matches_summary,
        "solver_shape": solver_shape,
    }
    if classification == OBSERVED_UNSAT:
        checks = {
            **common,
            "solver_result_present": isinstance(solver, dict),
            "solver_status_unsat": (
                isinstance(solver, dict) and solver.get("status") == "UNSAT"
            ),
            "solver_pair": (
                isinstance(solver, dict)
                and solver.get("catalog_line") == line
                and solver.get("deleted_vertex") == deleted
            ),
            "returncode": returncode == 20,
            "evidence_label": (
                record.get("evidence_category")
                == "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
            ),
            "no_proof_generated": record.get("proof_generated") is False,
            "no_proof_checked": record.get("proof_checked") is False,
        }
        executed = True
        precise = True
    elif classification == LIMIT:
        checks = {
            **common,
            "solver_result_present": isinstance(solver, dict),
            "solver_status_limit": (
                isinstance(solver, dict) and solver.get("status") == "LIMIT"
            ),
            "solver_pair": (
                isinstance(solver, dict)
                and solver.get("catalog_line") == line
                and solver.get("deleted_vertex") == deleted
            ),
            "returncode": returncode == 2,
            "evidence_label": (
                record.get("evidence_category")
                == "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
            ),
            "no_proof_generated": record.get("proof_generated") is False,
            "no_proof_checked": record.get("proof_checked") is False,
        }
        executed = True
        precise = True
    elif classification == VERIFIED_SAT:
        checks = {
            **common,
            "solver_result_present": isinstance(solver, dict),
            "solver_status_sat": (
                isinstance(solver, dict) and solver.get("status") == "SAT"
            ),
            "solver_pair": (
                isinstance(solver, dict)
                and solver.get("catalog_line") == line
                and solver.get("deleted_vertex") == deleted
            ),
            "returncode": returncode == 10,
            "dual_verified": record.get("dual_verified") is True,
            "certified_label": record.get("evidence_category") == "CERTIFIED",
        }
        for path_key, hash_key in (
            ("model_path", "model_sha256"),
            ("candidate_graph6_path", "candidate_graph6_sha256"),
            ("candidate_canonical_path", "candidate_canonical_sha256"),
            ("verification_path", "verification_sha256"),
        ):
            artifact = Path(str(record.get(path_key)))
            checks[f"{path_key}_hash"] = (
                artifact.is_file()
                and sha256_file(artifact) == record.get(hash_key)
            )
        executed = True
        precise = True
    elif classification == FAILED_SAT:
        checks = {**common, "failed_sat_is_not_acceptable": False}
        executed = True
        precise = False
    elif classification == ERROR:
        checks = {**common, "screen_error_is_not_acceptable": False}
        executed = False
        precise = False
    else:
        checks = {**common, "recognized_classification": False}
        executed = False
        precise = False
    return {
        "catalog_line": line,
        "deleted_vertex": deleted,
        "classification": classification,
        "valid": all(checks.values()),
        "executed": executed,
        "precise_status": precise,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--catalog-lines", type=int, default=328)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    if args.catalog_lines <= 0:
        raise SystemExit("--catalog-lines must be positive")

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    instances = summary.get("instances")
    if not isinstance(instances, list):
        raise SystemExit("summary has no instances list")
    expected = [
        (line, deleted)
        for line in range(1, args.catalog_lines + 1)
        for deleted in range(42)
    ]
    actual = [pair(record) for record in instances]
    duplicate_count = len(actual) - len(set(actual))
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    coverage_valid = (
        duplicate_count == 0
        and not missing
        and not extra
        and len(actual) == len(expected)
    )

    catalog_sha256 = sha256_file(args.catalog)
    solver_sha256 = sha256_file(args.solver)
    checked = [
        check_record(
            record,
            catalog_sha256=catalog_sha256,
            solver_sha256=solver_sha256,
            catalog_lines=args.catalog_lines,
        )
        for record in instances
    ]
    classification_counts = {
        classification: sum(
            item["classification"] == classification for item in checked
        )
        for classification in (
            OBSERVED_UNSAT,
            VERIFIED_SAT,
            FAILED_SAT,
            LIMIT,
            ERROR,
        )
    }
    summary_checks = {
        "expected_pair_count": summary.get("expected_pair_count")
        == len(expected),
        "actual_record_count": summary.get("actual_record_count")
        == len(actual),
        "catalog_sha256": summary.get("catalog_sha256") == catalog_sha256,
        "solver_sha256": summary.get("solver_sha256") == solver_sha256,
        "catalog_data_line_count": summary.get("catalog_data_line_count")
        == args.catalog_lines,
        "deletion_labels": summary.get("deletion_labels") == list(range(42)),
        "counts": summary.get("counts") == classification_counts,
        "worker_errors": not summary.get("worker_errors"),
        "unsat_proof_replay": summary.get("unsat_proof_replay") is False,
    }
    records_valid = (
        all(item["valid"] for item in checked)
        and all(summary_checks.values())
    )
    all_pairs_executed = all(item["executed"] for item in checked)
    all_statuses_precise = all(item["precise_status"] for item in checked)
    valid = coverage_valid and records_valid
    negative_certified_count = sum(
        record.get("negative_certified") is True
        for record in instances
        if record.get("classification") in (OBSERVED_UNSAT, LIMIT)
    )
    result = {
        "checker": CHECKER_ID,
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "valid": valid,
        "coverage_valid": coverage_valid,
        "records_valid": records_valid,
        "all_pairs_executed": all_pairs_executed,
        "all_statuses_precise": all_statuses_precise,
        "negative_certified_count": negative_certified_count,
        "negative_evidence_category": (
            "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        ),
        "scope": (
            "exact execution/status coverage of fixed catalog cores only; "
            "negative statuses were not proof-checked and are not global "
            "order-43 nonexistence"
        ),
        "summary": str(args.summary.resolve()),
        "summary_sha256": sha256_file(args.summary),
        "catalog": str(args.catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "solver": str(args.solver.resolve()),
        "solver_sha256": solver_sha256,
        "catalog_lines": args.catalog_lines,
        "deletion_labels": list(range(42)),
        "expected_pair_count": len(expected),
        "actual_pair_count": len(actual),
        "duplicate_pair_count": duplicate_count,
        "missing_pair_count": len(missing),
        "extra_pair_count": len(extra),
        "missing_pairs_first_20": [
            {"catalog_line": line, "deleted_vertex": deleted}
            for line, deleted in missing[:20]
        ],
        "extra_pairs_first_20": [
            {"catalog_line": line, "deleted_vertex": deleted}
            for line, deleted in extra[:20]
        ],
        "classification_counts": classification_counts,
        "summary_checks": summary_checks,
        "runtime_seconds": time.monotonic() - started,
        "checker_source_sha256": sha256_file(Path(__file__)),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
