#!/usr/bin/env python3
"""Fail-closed post-pilot launch audit for the 128 lifted C7 shards.

This script does not solve a pair cube and cannot certify the order-7 branch.
It binds the exact-cover certificate, the frozen design, the full-size pilot,
and the independently replayed pilot.  It then evaluates the preregistered
storage envelope and a conservative empirical runtime envelope.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDIT_ID = "ramsey55_automorphism7_pair_lifted_launch_audit_v1"
OLD_GATE_REQUIRED_BYTES = 20_317_547_392


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_path(record: dict[str, Any]) -> Path:
    path = Path(str(record["path"]))
    return path if path.is_absolute() else ROOT / path


def validate_pin(record: object, path: Path, label: str) -> None:
    if (
        not isinstance(record, dict)
        or resolve_path(record).resolve() != path.resolve()
        or record.get("sha256") != sha256_file(path)
    ):
        raise ValueError(f"pin mismatch: {label}")


def all_true(record: object) -> bool:
    return (
        isinstance(record, dict)
        and bool(record)
        and all(value is True for value in record.values())
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing to overwrite output")
    started = time.monotonic()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if (
        plan.get("schema")
        != "ramsey55.automorphism7_pair_lifted_launch_audit_plan.v1"
        or plan.get("status") != "FROZEN_POST_PILOT_AUDIT"
        or plan.get("full_run_authorized") is not False
    ):
        raise SystemExit("wrong audit plan schema/status")

    validate_pin(plan["audit"], Path(__file__).resolve(), "audit")
    paths = {
        label: resolve_path(record)
        for label, record in plan["pins"].items()
    }
    for label, path in paths.items():
        validate_pin(plan["pins"][label], path, label)

    design = json.loads(paths["full_design"].read_text(encoding="utf-8"))
    design_audit = json.loads(
        paths["full_design_audit"].read_text(encoding="utf-8")
    )
    side_bundle = json.loads(
        paths["side_exhaustion_bundle"].read_text(encoding="utf-8")
    )
    pilot_plan = json.loads(
        paths["pilot_plan"].read_text(encoding="utf-8")
    )
    pilot = json.loads(paths["pilot_result"].read_text(encoding="utf-8"))
    pilot_check = json.loads(
        paths["pilot_check"].read_text(encoding="utf-8")
    )

    old_design_gate = design["existing_conservative_gate"]
    old_audit_gate = design_audit["existing_conservative_gate"]
    old_plan_gate = pilot_plan["existing_conservative_gate"]
    old_gate_unchanged = all(
        gate.get("status") == "UNCHANGED_AND_FROZEN"
        and int(gate["required_prelaunch_free_bytes"])
        == OLD_GATE_REQUIRED_BYTES
        for gate in (old_design_gate, old_audit_gate, old_plan_gate)
    )
    if not old_gate_unchanged:
        raise AssertionError("existing conservative gate changed")

    storage = design["hard_storage_gate"]
    retained_cap = (
        int(storage["pair_drat_zstd_total_cap_bytes"])
        + int(storage["exact_cover_total_cap_bytes"])
    )
    required_prelaunch = (
        retained_cap
        + int(storage["maximum_transient_bytes"])
        + int(storage["minimum_free_bytes_after_completion"])
    )
    if (
        required_prelaunch
        != int(storage["required_prelaunch_free_bytes"])
        or required_prelaunch != 9_126_805_504
    ):
        raise AssertionError("new hard storage envelope changed")

    side_exact = (
        side_bundle.get("valid") is True
        and side_bundle.get("model_count") == 191394
        and side_bundle.get("drat_trim_valid") is True
        and side_bundle.get("lrat_check_valid") is True
        and side_bundle.get("regenerated_lrat_exact") is True
        and side_bundle.get("cap_passed") is True
        and int(side_bundle["retained_bundle_bytes"])
        <= int(storage["exact_cover_total_cap_bytes"])
    )
    pilot_exact = (
        pilot.get("status") == "CERTIFIED_UNSAT_SHARD"
        and pilot.get("shard_index") == 73
        and pilot.get("shard_count") == 128
        and pilot.get("pair_count") == 291
        and pilot.get("first_pair_index") == 73
        and pilot.get("last_pair_index") == 37193
        and pilot.get("all_pairs_unsat_within_budget") is True
        and pilot.get("all_blockers_derived") is True
        and pilot.get("drat_trim_valid") is True
        and pilot.get("lrat_check_valid") is True
        and int(pilot["measurements"]["maximum_conflicts"])
        <= int(pilot_plan["conflict_budget_per_pair"])
    )
    pilot_replay_exact = (
        pilot_check.get("valid") is True
        and pilot_check.get("certified_schedule_reconstruction") is True
        and pilot_check.get("wrapper_exact") is True
        and pilot_check.get("all_segments_exact") is True
        and pilot_check.get("drat_trim_valid") is True
        and pilot_check.get("lrat_check_valid") is True
        and pilot_check.get("regenerated_lrat_exact") is True
        and all_true(pilot_check.get("compressed_checks"))
        and all_true(pilot_check.get("cap_checks"))
        and pilot_check.get("shard_result_sha256")
        == sha256_file(paths["pilot_result"])
    )

    shard_count = int(design["sharding"]["shard_count"])
    if shard_count != 128:
        raise AssertionError("shard count changed")
    projections = {
        "raw_drat_bytes_128x": int(pilot["lifted_drat"]["bytes"])
        * shard_count,
        "zstd_drat_bytes_128x": int(pilot["lifted_drat"]["zstd_bytes"])
        * shard_count,
        "raw_lrat_bytes_128x_informational_only": int(
            pilot["lifted_lrat"]["bytes"]
        )
        * shard_count,
        "zstd_lrat_bytes_128x_informational_only": int(
            pilot["lifted_lrat"]["zstd_bytes"]
        )
        * shard_count,
        "wrapper_bytes_128x_informational_only": int(
            pilot["wrapper"]["bytes"]
        )
        * shard_count,
    }
    retained_projection = (
        projections["zstd_drat_bytes_128x"]
        + int(side_bundle["retained_bundle_bytes"])
    )
    retained_projection_passed = (
        projections["zstd_drat_bytes_128x"]
        <= int(storage["pair_drat_zstd_total_cap_bytes"])
        and int(side_bundle["retained_bundle_bytes"])
        <= int(storage["exact_cover_total_cap_bytes"])
        and retained_projection <= retained_cap
    )
    per_shard_caps_passed = (
        int(pilot["wrapper"]["bytes"])
        <= int(storage["per_shard_wrapper_cap_bytes"])
        and int(pilot["lifted_drat"]["bytes"])
        <= int(storage["per_shard_raw_drat_cap_bytes"])
        and int(pilot["lifted_lrat"]["bytes"])
        <= int(storage["per_shard_raw_lrat_cap_bytes"])
    )

    runtime_gate = plan["runtime_gate"]
    production_scaled_seconds = (
        float(pilot["run_seconds"]) * shard_count
    )
    verification_scaled_seconds = (
        float(pilot_check["runtime_seconds"]) * shard_count
    )
    combined_scaled_seconds = (
        production_scaled_seconds + verification_scaled_seconds
    )
    contingency_factor = float(runtime_gate["contingency_factor"])
    contingency_seconds = math.ceil(
        combined_scaled_seconds * contingency_factor
    )
    runtime_projection_passed = (
        float(pilot["run_seconds"])
        <= int(runtime_gate["per_shard_runner_cap_seconds"])
        and float(pilot_check["runtime_seconds"])
        <= int(runtime_gate["per_shard_checker_cap_seconds"])
        and contingency_seconds
        <= int(runtime_gate["full_serial_cap_seconds"])
    )

    available = shutil.disk_usage(ROOT).free
    dynamic_storage_gate_passed = available >= required_prelaunch
    tooling_gate_passed = (
        side_exact
        and pilot_exact
        and pilot_replay_exact
        and per_shard_caps_passed
        and retained_projection_passed
        and old_gate_unchanged
    )
    every_gate_passed = (
        tooling_gate_passed
        and runtime_projection_passed
        and dynamic_storage_gate_passed
    )
    launch_recommended = every_gate_passed and bool(
        plan["recommend_if_every_gate_passes"]
    )

    blockers = []
    if not dynamic_storage_gate_passed:
        blockers.append(
            "available storage is below the 9,126,805,504-byte "
            "prelaunch requirement"
        )
    if not tooling_gate_passed:
        blockers.append("one or more exact-certificate/tooling gates failed")
    if not runtime_projection_passed:
        blockers.append("the conservative empirical runtime gate failed")
    if plan.get("full_run_authorized") is not True:
        blockers.append(
            "the frozen audit plan explicitly withholds full-run "
            "authorization"
        )

    result: dict[str, Any] = {
        "audit": AUDIT_ID,
        "valid": True,
        "status": (
            "RECOMMEND_FULL_LAUNCH_PENDING_AUTHORIZATION"
            if launch_recommended
            else "DO_NOT_LAUNCH"
        ),
        "claim_boundary": (
            "This is a launch-readiness audit based on one certified "
            "full-size shard. It does not certify any of the other 127 "
            "shards or the complete order-7 branch."
        ),
        "exact_evidence": {
            "side_model_exhaustion": side_exact,
            "pilot_shard": pilot_exact,
            "independent_pilot_replay": pilot_replay_exact,
            "pilot_result_sha256": sha256_file(paths["pilot_result"]),
            "pilot_check_sha256": sha256_file(paths["pilot_check"]),
        },
        "pilot_measurements": {
            "shard_index": pilot["shard_index"],
            "pair_count": pilot["pair_count"],
            "maximum_conflicts": pilot["measurements"]["maximum_conflicts"],
            "conflict_cap_per_pair": pilot["conflict_budget_per_pair"],
            "run_seconds": pilot["run_seconds"],
            "independent_check_seconds": pilot_check["runtime_seconds"],
            "wrapper_bytes": pilot["wrapper"]["bytes"],
            "raw_drat_bytes": pilot["lifted_drat"]["bytes"],
            "zstd_drat_bytes": pilot["lifted_drat"]["zstd_bytes"],
            "raw_lrat_bytes": pilot["lifted_lrat"]["bytes"],
            "zstd_lrat_bytes": pilot["lifted_lrat"]["zstd_bytes"],
        },
        "storage_audit": {
            "per_shard_caps_passed": per_shard_caps_passed,
            "projection": projections,
            "retained_projection_bytes": retained_projection,
            "retained_projection_passed": retained_projection_passed,
            "retained_cap_bytes": retained_cap,
            "available_bytes_at_audit": available,
            "required_prelaunch_free_bytes": required_prelaunch,
            "dynamic_storage_gate_passed": dynamic_storage_gate_passed,
            "retention_semantics": design["sharding"]["retention"],
        },
        "runtime_audit": {
            "basis": (
                "Scale the certified maximum-size shard and its independent "
                "replay by all 128 shards, then apply the frozen contingency "
                "factor. This is an empirical planning bound, not a proof "
                "that every shard will finish below it."
            ),
            "production_128x_seconds": production_scaled_seconds,
            "independent_verification_128x_seconds": (
                verification_scaled_seconds
            ),
            "combined_128x_seconds": combined_scaled_seconds,
            "contingency_factor": contingency_factor,
            "contingency_seconds": contingency_seconds,
            "full_serial_cap_seconds": int(
                runtime_gate["full_serial_cap_seconds"]
            ),
            "runtime_projection_passed": runtime_projection_passed,
        },
        "gates": {
            "tooling_and_exact_evidence": tooling_gate_passed,
            "runtime_projection": runtime_projection_passed,
            "dynamic_storage": dynamic_storage_gate_passed,
            "every_gate_passed": every_gate_passed,
        },
        "existing_conservative_gate": {
            "status": "UNCHANGED_AND_FROZEN",
            "required_prelaunch_free_bytes": OLD_GATE_REQUIRED_BYTES,
        },
        "launch_recommended": launch_recommended,
        "full_run_authorized": False,
        "blockers": blockers,
        "plan_sha256": sha256_file(args.plan),
        "runtime_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
