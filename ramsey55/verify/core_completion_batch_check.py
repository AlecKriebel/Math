#!/usr/bin/env python3
"""Check every explicit DPLL tree in a core-completion batch."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from extension_sat_check import (  # noqa: E402
    TreeChecker,
    read_cnf,
    read_proof,
)


CHECKER_ID = "core_completion_batch_tree_checker_v1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--expect-all-42",
        action="store_true",
        help="require exactly deletion labels 0 through 41",
    )
    args = parser.parse_args()
    started = time.monotonic()

    cnf_paths = sorted(args.input_dir.glob("core_completion_delete_*.cnf"))
    if not cnf_paths:
        raise SystemExit("no core-completion CNFs found")
    deletion_labels = [
        int(path.stem.rsplit("_", 1)[1]) for path in cnf_paths
    ]
    expected_labels = list(range(42)) if args.expect_all_42 else deletion_labels
    if (
        len(deletion_labels) != len(set(deletion_labels))
        or deletion_labels != expected_labels
    ):
        raise SystemExit(
            "deletion-label coverage mismatch: "
            f"found={deletion_labels}, expected={expected_labels}"
        )
    results: list[dict[str, object]] = []
    for cnf_path in cnf_paths:
        proof_path = cnf_path.with_suffix(".tree")
        if not proof_path.is_file():
            raise SystemExit(f"missing proof for {cnf_path.name}")
        cnf_sha256 = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
        proof_sha256 = hashlib.sha256(proof_path.read_bytes()).hexdigest()
        variables, clauses = read_cnf(cnf_path)
        records = read_proof(proof_path, variables, cnf_sha256)
        stats = TreeChecker(variables, clauses, records).check()
        result = {
            "cnf": cnf_path.name,
            "proof": proof_path.name,
            "variable_count": variables,
            "clause_count": len(clauses),
            "cnf_sha256": cnf_sha256,
            "proof_sha256": proof_sha256,
            "valid": True,
            **vars(stats),
        }
        results.append(result)
        print(json.dumps(result, sort_keys=True), flush=True)

    coverage_conclusion = (
        "ALL_42_LABELED_FIXED_CORE_INSTANCES_UNSAT"
        if args.expect_all_42
        else "ALL_LISTED_FIXED_CORE_INSTANCES_UNSAT"
    )
    summary = {
        "checker": CHECKER_ID,
        "valid": True,
        "conclusion": coverage_conclusion,
        "deletion_labels": deletion_labels,
        "expected_all_42": args.expect_all_42,
        "instance_count": len(results),
        "total_records_checked": sum(
            int(item["records_checked"]) for item in results
        ),
        "total_branch_records": sum(
            int(item["branch_records"]) for item in results
        ),
        "total_unit_records": sum(
            int(item["unit_records"]) for item in results
        ),
        "total_conflict_records": sum(
            int(item["conflict_records"]) for item in results
        ),
        "runtime_seconds": time.monotonic() - started,
        "instances": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {key: value for key, value in summary.items() if key != "instances"},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
