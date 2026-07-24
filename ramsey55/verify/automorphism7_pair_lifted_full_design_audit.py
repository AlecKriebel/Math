#!/usr/bin/env python3
"""Audit the frozen sharded design for a full lifted order-7 certificate.

This does not solve any unsampled cube.  It reconstructs the exact prospective
wrapper sizes, checks the sample evidence, checks the new hard storage caps,
and records the missing logical prerequisites that keep the full run frozen.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
for directory in (ROOT / "src", ROOT / "verify"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import automorphism7_side_orbit_cover as one_side  # noqa: E402
import automorphism7_side_pair_orbit_sweep as sweep  # noqa: E402


AUDIT_ID = "ramsey55_automorphism7_pair_lifted_full_design_audit_v1"
BASE_VARIABLE_COUNT = 129


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_pin(record: object, path: Path, label: str) -> None:
    if (
        not isinstance(record, dict)
        or Path(str(record.get("path", ""))).resolve() != path.resolve()
        or record.get("sha256") != sha256_file(path)
    ):
        raise ValueError(f"pin mismatch: {label}")


def fixed_and_side_maps(
    metadata: dict[str, object],
    edge_orbits: tuple[tuple[tuple[int, int], ...], ...],
) -> tuple[list[int], list[int], list[int]]:
    edge_table = one_side.global_edge_table(metadata)
    map_a = [edge_table[orbit[0]] for orbit in edge_orbits]
    map_b = [
        edge_table[(orbit[0][0] + 21, orbit[0][1] + 21)]
        for orbit in edge_orbits
    ]
    fixed_variables = sorted(
        {
            variable
            for (left, right), variable in edge_table.items()
            if right == 42
        },
        key=lambda variable: min(
            left
            for (left, right), observed in edge_table.items()
            if right == 42 and observed == variable
        ),
    )
    fixed_units = fixed_variables[:3] + [
        -variable for variable in fixed_variables[3:]
    ]
    return fixed_units, map_a, map_b


def side_units(
    left_model: int,
    right_model: int,
    map_a: list[int],
    map_b: list[int],
) -> tuple[int, ...]:
    units = [
        variable if left_model >> index & 1 else -variable
        for index, variable in enumerate(map_a)
    ]
    units.extend(
        -variable if right_model >> index & 1 else variable
        for index, variable in enumerate(map_b)
    )
    return tuple(units)


def line_bytes(clause: tuple[int, ...]) -> bytes:
    return (" ".join(map(str, clause)) + " 0\n").encode("ascii")


def prospective_wrapper(
    base_body: bytes,
    base_clause_count: int,
    fixed_units: list[int],
    pair_indices: list[int],
    pair_schedule: list[tuple[int, int]],
    representatives: list[int],
    map_a: list[int],
    map_b: list[int],
    declared_variables: int,
) -> dict[str, object]:
    clause_count = base_clause_count + len(fixed_units) + 61 * len(pair_indices) + 1
    digest = hashlib.sha256()
    byte_count = 0

    def update(payload: bytes) -> None:
        nonlocal byte_count
        digest.update(payload)
        byte_count += len(payload)

    update(f"p cnf {declared_variables} {clause_count}\n".encode("ascii"))
    update(base_body)
    for unit in fixed_units:
        update(line_bytes((unit,)))
    selectors: list[int] = []
    for pair_index in pair_indices:
        selector = BASE_VARIABLE_COUNT + pair_index + 1
        selectors.append(selector)
        left_class, right_class = pair_schedule[pair_index]
        cube = side_units(
            representatives[left_class],
            representatives[right_class],
            map_a,
            map_b,
        )
        for literal in cube:
            update(line_bytes((-selector, literal)))
        update(line_bytes((selector, *(-literal for literal in cube))))
    update(line_bytes(tuple(selectors)))
    return {
        "pair_count": len(pair_indices),
        "variable_count": declared_variables,
        "clause_count": clause_count,
        "bytes": byte_count,
        "sha256": digest.hexdigest(),
        "first_pair_index": pair_indices[0],
        "last_pair_index": pair_indices[-1],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing to overwrite output")
    started = time.monotonic()
    design = json.loads(args.design.read_text(encoding="utf-8"))
    if (
        design.get("schema")
        != "ramsey55.automorphism7_pair_lifted_full_design.v1"
        or design.get("status") != "FROZEN_DESIGN"
    ):
        raise SystemExit("wrong design schema/status")

    paths = {
        label: (Path(record["path"]) if Path(record["path"]).is_absolute() else ROOT / record["path"])
        for label, record in design["pins"].items()
    }
    for label, path in paths.items():
        validate_pin(design["pins"][label], path, label)
    validate_pin(
        design["design_audit"],
        Path(__file__).resolve(),
        "design_audit",
    )

    sample = json.loads(paths["lifted_sample_result"].read_text(encoding="utf-8"))
    sample_check = json.loads(
        paths["lifted_sample_check"].read_text(encoding="utf-8")
    )
    old_plan = json.loads(paths["existing_concat_plan"].read_text(encoding="utf-8"))
    pair_audit = json.loads(paths["pair_audit"].read_text(encoding="utf-8"))
    if (
        sample.get("drat_trim_valid") is not True
        or sample.get("lrat_check_valid") is not True
        or sample_check.get("valid") is not True
        or pair_audit.get("coverage_valid") is not True
    ):
        raise AssertionError("required sample/action audit is not valid")
    old_required = (
        int(old_plan["full_bundle_working_reserve_bytes"])
        + 16022580096
    )
    if old_required != 20317547392:
        raise AssertionError("existing conservative gate changed")

    edge_orbits, representatives, pair_schedule = sweep.build_pair_schedule()
    variable_count, base_clauses = one_side.parse_dimacs(paths["cnf"])
    metadata = json.loads(paths["metadata"].read_text(encoding="utf-8"))
    fixed_units, map_a, map_b = fixed_and_side_maps(metadata, edge_orbits)
    if variable_count != BASE_VARIABLE_COUNT or len(pair_schedule) != 37194:
        raise AssertionError("unexpected base/schedule")
    raw_cnf = paths["cnf"].read_bytes()
    _, base_body = raw_cnf.split(b"\n", 1)

    shard_count = int(design["sharding"]["shard_count"])
    shard_indices = [
        [
            pair_index
            for pair_index in range(len(pair_schedule))
            if pair_index % shard_count == shard
        ]
        for shard in range(shard_count)
    ]
    declared_variables = BASE_VARIABLE_COUNT + len(pair_schedule)
    shard_wrappers = [
        prospective_wrapper(
            base_body,
            len(base_clauses),
            fixed_units,
            indices,
            pair_schedule,
            representatives,
            map_a,
            map_b,
            declared_variables,
        )
        for indices in shard_indices
    ]
    monolithic = prospective_wrapper(
        base_body,
        len(base_clauses),
        fixed_units,
        list(range(len(pair_schedule))),
        pair_schedule,
        representatives,
        map_a,
        map_b,
        declared_variables,
    )

    target = len(pair_schedule)
    sample_count = int(sample["sample_count"])
    projections = {
        "lifted_drat_raw_average_scaled_bytes": math.ceil(
            int(sample["lifted_drat"]["bytes"]) * target / sample_count
        ),
        "lifted_drat_zstd_average_scaled_bytes": math.ceil(
            int(sample["lifted_drat"]["zstd_bytes"]) * target / sample_count
        ),
        "lifted_lrat_raw_average_scaled_bytes": math.ceil(
            int(sample["lifted_lrat"]["bytes"]) * target / sample_count
        ),
        "lifted_lrat_zstd_average_scaled_bytes": math.ceil(
            int(sample["lifted_lrat"]["zstd_bytes"]) * target / sample_count
        ),
        "raw_segment_sample_max_scaled_bytes": (
            int(sample["measurements"]["segment_bytes_maximum"]) * target
        ),
    }

    gate = design["hard_storage_gate"]
    retained_cap = (
        int(gate["pair_drat_zstd_total_cap_bytes"])
        + int(gate["exact_cover_total_cap_bytes"])
    )
    required = (
        retained_cap
        + int(gate["maximum_transient_bytes"])
        + int(gate["minimum_free_bytes_after_completion"])
    )
    if required != int(gate["required_prelaunch_free_bytes"]):
        raise AssertionError("hard storage gate arithmetic mismatch")
    available = shutil.disk_usage(ROOT).free
    storage_subgate_passed = available >= required

    prerequisites = {
        "selector_lifting_sample": "PASS",
        "independent_sample_replay": "PASS",
        "pair_action_and_schedule_audit": "PASS_RELATIVE_TO_MODEL_LIST",
        "side_model_exhaustion_lrat": "MISSING",
        "full_sharded_runner_hash_pin": "MISSING",
        "full_sharded_independent_checker": "MISSING",
        "one_full_size_shard_pilot": "MISSING",
    }
    launch_ready = storage_subgate_passed and all(
        status == "PASS" for status in prerequisites.values()
    )
    if launch_ready:
        raise AssertionError("design unexpectedly became launch-ready")

    result: dict[str, Any] = {
        "audit": AUDIT_ID,
        "valid": True,
        "status": "FROZEN_NOT_LAUNCH_READY",
        "claim_boundary": (
            "This is a checked design and storage audit, not a certificate "
            "for an unsampled pair or for the complete order-7 branch."
        ),
        "target_pair_count": target,
        "pair_schedule_sha256": sweep.EXPECTED_PAIR_SCHEDULE_SHA256,
        "sample_evidence": {
            "result_sha256": sha256_file(paths["lifted_sample_result"]),
            "check_sha256": sha256_file(paths["lifted_sample_check"]),
            "all_blockers_derived": sample["all_blockers_derived"],
            "drat_trim_valid": sample["drat_trim_valid"],
            "lrat_check_valid": sample["lrat_check_valid"],
        },
        "prospective_monolithic_wrapper": monolithic,
        "sharding": {
            "rule": f"pair_index modulo {shard_count}",
            "shard_count": shard_count,
            "pair_count_minimum": min(
                int(record["pair_count"]) for record in shard_wrappers
            ),
            "pair_count_maximum": max(
                int(record["pair_count"]) for record in shard_wrappers
            ),
            "wrapper_bytes_minimum": min(
                int(record["bytes"]) for record in shard_wrappers
            ),
            "wrapper_bytes_maximum": max(
                int(record["bytes"]) for record in shard_wrappers
            ),
            "wrapper_clause_count_minimum": min(
                int(record["clause_count"]) for record in shard_wrappers
            ),
            "wrapper_clause_count_maximum": max(
                int(record["clause_count"]) for record in shard_wrappers
            ),
            "shard_wrapper_records": shard_wrappers,
        },
        "sample_scaled_projections": projections,
        "hard_storage_gate": {
            **gate,
            "retained_cap_bytes": retained_cap,
            "available_bytes_at_audit": available,
            "storage_subgate_passed": storage_subgate_passed,
            "semantics": (
                "A future runner must abort before any hard cap is exceeded. "
                "Passing this storage subgate does not predict that every "
                "proof will fit and does not authorize launch."
            ),
        },
        "existing_conservative_gate": {
            "status": "UNCHANGED_AND_FROZEN",
            "required_prelaunch_free_bytes": old_required,
        },
        "exact_cover_design": {
            "side_model_completeness": (
                "Retain the 191,394 side assignments, directly replay each "
                "as a side-formula model, and certify S plus all corresponding "
                "30-literal model blockers UNSAT with DRAT-to-LRAT."
            ),
            "finite_quotient": (
                "Partition the certified model list under the 294 H actions, "
                "then partition ordered class pairs under independent H "
                "actions, common multipliers, and color-complementing swap."
            ),
            "global_link": (
                "Independently verify every group generator preserves the "
                "normalized global CNF and maps pair units with the audited "
                "sign convention. Thus every normalized global model has a "
                "symmetry image in exactly one scheduled representative "
                "orbit."
            ),
            "shard_cover": (
                "Each shard wrapper asserts a selector cover over its exact "
                "schedule subset. Certified UNSAT of all shards eliminates "
                "all representatives; the exact finite quotient then lifts "
                "that conclusion to the normalized order-7 branch."
            ),
        },
        "prerequisites": prerequisites,
        "storage_subgate_passed": storage_subgate_passed,
        "launch_ready": launch_ready,
        "full_run_authorized": False,
        "design_sha256": sha256_file(args.design),
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
