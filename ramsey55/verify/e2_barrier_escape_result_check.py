#!/usr/bin/env python3
"""Check bindings and count identities in the retained barrier-scan result."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_ID = "ramsey55_e2_barrier_escape_result_check_v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(path: Path) -> dict[str, object]:
    record = json.loads(path.read_text(encoding="utf-8"))
    implementation = record["implementation"]
    binding = record["input_binding"]
    result = record["result"]
    audit_path = ROOT / binding["independent_cycle_audit"]
    source_path = ROOT / implementation["source"]
    audit = json.loads(audit_path.read_text(encoding="utf-8"))

    checks = {
        "artifact_id": record["artifact"]
        == "ramsey55_e2_barrier_escape_atomic_ceiling15_v1",
        "source_hash": sha256(source_path)
        == implementation["source_sha256"],
        "audit_hash": sha256(audit_path)
        == binding["independent_cycle_audit_sha256"],
        "audit_valid": audit.get("valid") is True,
        "audit_components": audit.get("seed_cycle_count") == 22,
        "audit_states": audit.get("total_distinct_labeled_neutral_states")
        == 1892,
        "pair_coverage_identity": result["pair_checks"]
        == 1892 * 4 * (903 - 1),
        "pair_exact_replay_sum": sum(
            result["pair_raw_retained_distribution"].values()
        )
        == result["pair_exact_replays"],
        "triple_exact_replay_sum": sum(
            result["triple_raw_E_le_4_distribution"].values()
        )
        == result["triple_exact_replays"],
        "fourth_coverage_identity": result["fourth_checks"]
        == sum(result["triple_unique_E_le_4_distribution"].values()) * 903,
        "fourth_exact_replay_sum": sum(
            result["fourth_raw_E_le_4_distribution"].values()
        )
        == result["fourth_exact_replays"],
        "fifth_exact_replay_sum": sum(
            result["fifth_raw_E_le_4_distribution"].values()
        )
        == result["fifth_exact_replays"],
        "closure_complete": result["closure_complete"] is True,
        "closure_below_cap": sum(
            result["closure_state_distribution"].values()
        )
        < result["closure_state_limit"],
        "no_E0": result["E0_found"] is False,
        "no_E1_in_closure": result["closure_E1_hits"] == 0,
        "no_offcycle_E2": result["offcycle_E2_count"] == 0,
        "claim_boundary_present": (
            "not" in record["claim_boundary"].lower()
            or "neither" in record["claim_boundary"].lower()
        )
        and "global nonexistence" in record["claim_boundary"].lower(),
    }
    return {
        "checker": CHECKER_ID,
        "artifact": str(path),
        "artifact_sha256": sha256(path),
        "checks": checks,
        "accepted": all(checks.values()),
        "claim_boundary": (
            "This checker validates retained bindings and internal count "
            "identities; it does not independently replay all search moves "
            "and does not strengthen the artifact's claim boundary."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "artifact",
        type=Path,
        nargs="?",
        default=(
            ROOT
            / "results/verification/e2_barrier_escape_atomic_ceiling15_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check(args.artifact)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        if args.output.exists():
            raise SystemExit("refusing to overwrite output")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
