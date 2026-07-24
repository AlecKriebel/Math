#!/usr/bin/env python3
"""Independently enforce pair coverage for catalog k=1 classifications."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path


CHECKER_ID = "ramsey55_core_completion_catalog_coverage_checker_v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def pair(record: dict[str, object]) -> tuple[int, int]:
    return int(record["catalog_line"]), int(record["deleted_vertex"])


def expected_from_plan(path: Path) -> tuple[list[tuple[int, int]], str]:
    plan = json.loads(path.read_text(encoding="utf-8"))
    raw_pairs = plan.get("pairs")
    if not isinstance(raw_pairs, list) or not raw_pairs:
        raise ValueError("plan has no nonempty pairs list")
    expected = [pair(item) for item in raw_pairs]
    if len(expected) != len(set(expected)):
        raise ValueError("plan contains duplicate pairs")
    return expected, sha256_file(path)


def check_instance(record: dict[str, object]) -> dict[str, object]:
    line, deleted = pair(record)
    solver = record.get("solver_result")
    if not isinstance(solver, dict):
        raise ValueError(f"{(line, deleted)} has no solver result")
    common = {
        "solver_selected_pair": (
            solver.get("catalog_line") == line
            and solver.get("deleted_vertex") == deleted
        ),
        "fixed_core_scope_recorded": bool(record.get("fixed_core_scope")),
    }
    classification = record.get("classification")
    if classification == "CHECKED_UNSAT_FIXED_CORE":
        proof = Path(str(record["proof_path"]))
        checked = record.get("checker_result")
        if not isinstance(checked, dict):
            raise ValueError(f"{(line, deleted)} has no checker result")
        checks = {
            **common,
            "solver_status_unsat": solver.get("status") == "UNSAT",
            "proof_exists": proof.is_file(),
            "proof_hash": (
                proof.is_file()
                and sha256_file(proof) == record.get("proof_sha256")
            ),
            "checker_status": (
                checked.get("status")
                == "VERIFIED_UNSAT_FIXED_41_CORE_TWO_VERTEX_COMPLETION"
            ),
            "checker_pair": (
                checked.get("catalog_line") == line
                and checked.get("deleted_original_vertex") == deleted
            ),
            "checker_proof_hash": (
                checked.get("proof_sha256") == record.get("proof_sha256")
            ),
            "checker_format": checked.get("proof_format") == "CORE2DP2",
        }
        conclusive = True
    elif classification == "DUAL_VERIFIED_SAT_CONSTRUCTION":
        model = Path(str(record["model_path"]))
        candidate = Path(str(record["candidate_graph6_path"]))
        canonical = Path(str(record["candidate_canonical_path"]))
        checks = {
            **common,
            "solver_status_sat": solver.get("status") == "SAT",
            "dual_verified": record.get("dual_verified") is True,
            "model_hash": (
                model.is_file()
                and sha256_file(model) == record.get("model_sha256")
            ),
            "candidate_graph6_hash": (
                candidate.is_file()
                and sha256_file(candidate)
                == record.get("candidate_graph6_sha256")
            ),
            "candidate_canonical_hash": (
                canonical.is_file()
                and sha256_file(canonical)
                == record.get("candidate_canonical_sha256")
            ),
        }
        conclusive = True
    elif classification == "LIMIT_NO_CONCLUSION":
        checks = {
            **common,
            "solver_status_limit": solver.get("status") == "LIMIT",
        }
        conclusive = False
    else:
        checks = {**common, "recognized_classification": False}
        conclusive = False
    return {
        "catalog_line": line,
        "deleted_vertex": deleted,
        "classification": classification,
        "valid": all(checks.values()),
        "conclusive": conclusive,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, required=True)
    expected_group = parser.add_mutually_exclusive_group(required=True)
    expected_group.add_argument("--pairs-plan", type=Path)
    expected_group.add_argument("--expect-all", action="store_true")
    parser.add_argument("--catalog-lines", type=int, default=328)
    parser.add_argument("--require-conclusive", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    raw_instances = summary.get("instances")
    if not isinstance(raw_instances, list):
        raise SystemExit("summary has no instances list")
    actual_pairs = [pair(item) for item in raw_instances]
    if len(actual_pairs) != len(set(actual_pairs)):
        raise SystemExit("summary contains duplicate fixed-core pairs")
    if args.expect_all:
        expected_pairs = [
            (line, deleted)
            for line in range(1, args.catalog_lines + 1)
            for deleted in range(42)
        ]
        plan_sha256 = None
    else:
        assert args.pairs_plan is not None
        expected_pairs, plan_sha256 = expected_from_plan(args.pairs_plan)
    missing = sorted(set(expected_pairs) - set(actual_pairs))
    extra = sorted(set(actual_pairs) - set(expected_pairs))
    if missing or extra or len(actual_pairs) != len(expected_pairs):
        raise SystemExit(
            "fixed-core pair coverage mismatch: "
            f"missing={missing[:20]} extra={extra[:20]} "
            f"actual={len(actual_pairs)} expected={len(expected_pairs)}"
        )

    checked = [check_instance(record) for record in raw_instances]
    artifact_valid = all(item["valid"] for item in checked)
    conclusive = all(item["conclusive"] for item in checked)
    valid = artifact_valid and (conclusive or not args.require_conclusive)
    result = {
        "checker": CHECKER_ID,
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "valid": valid,
        "artifact_valid": artifact_valid,
        "complete_checked_classification": conclusive,
        "scope": (
            "coverage of explicitly selected fixed 41-vertex cores only; "
            "not global order-43 nonexistence"
        ),
        "summary": str(args.summary),
        "summary_sha256": sha256_file(args.summary),
        "pairs_plan": str(args.pairs_plan) if args.pairs_plan else None,
        "pairs_plan_sha256": plan_sha256,
        "expected_all": args.expect_all,
        "catalog_lines": args.catalog_lines,
        "expected_pair_count": len(expected_pairs),
        "actual_pair_count": len(actual_pairs),
        "missing_pair_count": len(missing),
        "extra_pair_count": len(extra),
        "classification_counts": {
            classification: sum(
                item["classification"] == classification for item in checked
            )
            for classification in sorted(
                {str(item["classification"]) for item in checked}
            )
        },
        "instances": checked,
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
