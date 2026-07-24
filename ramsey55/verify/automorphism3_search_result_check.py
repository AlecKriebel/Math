#!/usr/bin/env python3
"""Independent structural checker for an order-3 constructive-search summary."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import Counter
from pathlib import Path


CHECKER_ID = "ramsey55_order3_search_result_checker_v1"
SEARCH_ID = "ramsey55_order3_maxcycle_search_v1"
FORMULA_SHA256 = (
    "2cb249c2d09d00bd199be27711fc344873785b9e9756dc1cafad8f756084a5e5"
)
RAW_SOLVERS = ("Cadical195", "Glucose4", "MapleChrono")
ALLOWED_NEGATIVE_STATUSES = {
    "BUDGET_EXHAUSTED",
    "OBSERVED_UNSAT_UNCHECKED",
}


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def schedule(left_count: int, right_count: int, seed: int) -> list[tuple[int, int]]:
    pairs = list(itertools.product(range(left_count), range(right_count)))
    random.Random(seed).shuffle(pairs)
    return pairs


def check(result_path: Path, formula_audit_path: Path, candidate: Path) -> dict[str, object]:
    result = json.loads(result_path.read_text(encoding="utf-8"))
    formula_audit = json.loads(formula_audit_path.read_text(encoding="utf-8"))
    configuration = result.get("configuration")
    formula = result.get("formula")
    normalization = result.get("normalization")
    raw_records = result.get("raw_records")
    gluing_records = result.get("gluing_records")
    side_pools = result.get("side_pools")
    if not all(
        isinstance(value, dict)
        for value in (configuration, formula, normalization, side_pools)
    ) or not isinstance(raw_records, list) or not isinstance(gluing_records, list):
        raise ValueError("result has malformed top-level fields")

    formula_valid = (
        formula_audit.get("valid") is True
        and formula_audit.get("dimacs_sha256_without_materialization")
        == FORMULA_SHA256
        and formula.get("dimacs_sha256_without_materialization") == FORMULA_SHA256
        and formula.get("variable_count") == 301
        and formula.get("unique_signature_count") == 320_593
        and formula.get("clause_count") == 641_186
    )
    normalization_valid = (
        normalization.get("possible_fixed_degrees") == [18, 21, 24]
        and normalization.get("possible_neighbor_cycle_counts") == [6, 7, 8]
        and normalization.get("complement_pair") == [6, 8]
        and normalization.get("searched_cases") == [6, 7]
    )

    raw_attempts = configuration.get("raw_attempts")
    raw_budget = configuration.get("raw_budget")
    raw_solvers = configuration.get("raw_solvers")
    expected_raw_keys = {
        (solver, attempt, t_case)
        for solver in RAW_SOLVERS
        for attempt in range(2)
        for t_case in (6, 7)
    }
    actual_raw_keys = {
        (record.get("solver"), record.get("attempt"), record.get("t_case"))
        for record in raw_records
    }
    raw_valid = (
        raw_attempts == 2
        and raw_budget == 100_000
        and raw_solvers == list(RAW_SOLVERS)
        and len(raw_records) == 12
        and actual_raw_keys == expected_raw_keys
        and all(
            record.get("status") in ALLOWED_NEGATIVE_STATUSES
            and record.get("negative_certified") is False
            and record.get("conflict_budget") == raw_budget
            and type(record.get("conflicts")) is int
            and record["conflicts"] > 0
            for record in raw_records
        )
    )

    pool_counts_raw = configuration.get("side_pool_counts")
    if not isinstance(pool_counts_raw, dict):
        raise ValueError("side-pool counts missing")
    pool_counts = {
        cycle_count: pool_counts_raw.get(str(cycle_count))
        for cycle_count in (6, 7, 8)
    }
    expected_side_shapes = {
        6: (51, 3_831),
        7: (70, 8_715),
        8: (92, 17_626),
    }
    side_valid = True
    for cycle_count, count in pool_counts.items():
        record = side_pools.get(str(cycle_count))
        if not isinstance(record, dict):
            side_valid = False
            continue
        expected_variables, expected_clauses = expected_side_shapes[cycle_count]
        side_valid &= (
            type(count) is int
            and count > 0
            and record.get("requested_count") == count
            and record.get("variable_count") == expected_variables
            and record.get("clause_count") == expected_clauses
            and record.get("base_model_count") == 16
            and isinstance(record.get("model_pool_sha256"), str)
            and len(record["model_pool_sha256"]) == 64
        )

    stages = configuration.get("stages")
    seed = configuration.get("seed")
    if not isinstance(stages, list) or type(seed) is not int:
        raise ValueError("stages or seed missing")
    schedules = {
        t_case: schedule(
            pool_counts[t_case], pool_counts[14 - t_case], seed + t_case
        )
        for t_case in (6, 7)
    }
    offsets = {6: 0, 7: 0}
    expected_identities = []
    for stage_index, raw_stage in enumerate(stages):
        if (
            not isinstance(raw_stage, list)
            or len(raw_stage) != 3
            or raw_stage[0] not in RAW_SOLVERS
            or type(raw_stage[1]) is not int
            or type(raw_stage[2]) is not int
        ):
            raise ValueError("malformed stage")
        solver, budget, pair_count = raw_stage
        for t_case in (7, 6):
            start = offsets[t_case]
            stop = start + pair_count
            selected = schedules[t_case][start:stop]
            if len(selected) != pair_count:
                raise ValueError("stage requests more pairs than its schedule")
            expected_identities.extend(
                (
                    stage_index,
                    solver,
                    budget,
                    t_case,
                    schedule_index,
                    left,
                    right,
                )
                for schedule_index, (left, right) in enumerate(
                    selected, start=start
                )
            )
            offsets[t_case] = stop
    actual_identities = [
        (
            record.get("stage_index"),
            record.get("solver"),
            record.get("conflict_budget"),
            record.get("t_case"),
            record.get("schedule_index"),
            record.get("left_model_index"),
            record.get("right_model_index"),
        )
        for record in gluing_records
    ]
    gluing_valid = (
        actual_identities == expected_identities
        and len(actual_identities) == len(set(actual_identities))
        and all(
            record.get("status") in ALLOWED_NEGATIVE_STATUSES
            and record.get("negative_certified") is False
            and record.get("fixed_variable_count")
            == (157 if record.get("t_case") == 6 else 154)
            and record.get("free_variable_count")
            == (144 if record.get("t_case") == 6 else 147)
            and type(record.get("conflicts")) is int
            and record["conflicts"] > 0
            for record in gluing_records
        )
    )
    status_counts = Counter(record["status"] for record in gluing_records)
    recorded_counts = result.get("gluing_status_counts")
    status_counts_valid = recorded_counts == dict(sorted(status_counts.items()))
    claim_boundary_valid = (
        result.get("construction") is None
        and result.get("evidence_label")
        == "REPRODUCIBLE_COMPUTATIONAL_OBSERVATION"
        and not candidate.exists()
        and isinstance(result.get("claim_boundary"), str)
        and "do not exclude" in result["claim_boundary"]
    )
    valid = (
        result.get("search") == SEARCH_ID
        and formula_valid
        and normalization_valid
        and raw_valid
        and side_valid
        and gluing_valid
        and status_counts_valid
        and claim_boundary_valid
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "formula_valid": formula_valid,
        "normalization_valid": normalization_valid,
        "raw_schedule_valid": raw_valid,
        "side_metadata_valid": side_valid,
        "gluing_schedule_valid": gluing_valid,
        "status_counts_valid": status_counts_valid,
        "claim_boundary_valid": claim_boundary_valid,
        "raw_record_count": len(raw_records),
        "gluing_record_count": len(gluing_records),
        "gluing_unique_identity_count": len(set(actual_identities)),
        "gluing_status_counts": dict(sorted(status_counts.items())),
        "distinct_pairs_by_t": {
            str(t_case): len(
                {
                    (record["left_model_index"], record["right_model_index"])
                    for record in gluing_records
                    if record["t_case"] == t_case
                }
            )
            for t_case in (6, 7)
        },
        "result_path": str(result_path.resolve()),
        "result_sha256": sha256_file(result_path),
        "formula_audit_path": str(formula_audit_path.resolve()),
        "formula_audit_sha256": sha256_file(formula_audit_path),
        "candidate_absent": not candidate.exists(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--formula-audit", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    checked = check(args.result, args.formula_audit, args.candidate)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite {args.output}")
    args.output.write_text(
        json.dumps(checked, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(checked, sort_keys=True))
    return 0 if checked["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
