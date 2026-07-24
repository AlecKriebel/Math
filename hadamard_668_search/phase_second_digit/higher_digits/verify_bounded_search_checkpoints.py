#!/usr/bin/env python3
"""Dependency-free replay of every bounded higher-digit checkpoint."""

from __future__ import annotations

import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SECOND_DIGIT = HERE.parent
SEARCH_ROOT = SECOND_DIGIT.parent
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_phase_second_digit as second  # noqa: E402
from verify_full_second_digit_witness import compact_hash  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
    phase_sums_from_masks,
)


CHECKPOINTS = HERE / "bounded_search_checkpoints.json"


def replay_point(stored: dict[str, object], maximum_digit: int):
    candidate_index = int(stored["candidate_index"])
    candidate = second.CANDIDATES[candidate_index]
    if stored["label"] != candidate[0]:
        raise AssertionError("a checkpoint label changed")
    profiles = second.profiles_from_ids(candidate[3], candidate[4])
    equations = second.first_digit_equations(profiles)
    origin, basis = second.affine_parameterization(equations, 54)
    affine = tuple(map(int, stored["affine_coordinates"]))
    if compact_hash(affine) != stored["affine_coordinates_sha256"]:
        raise AssertionError("a checkpoint affine hash changed")
    placement = second.lift_affine_point(origin, basis, affine)
    if compact_hash(placement) != stored["placement_trits_sha256"]:
        raise AssertionError("a checkpoint placement hash changed")
    digits = tuple(
        second.lambda_digits(value, 10)
        for value in second.displayed_values(profiles, placement)
    )
    objective = sum(
        int(row[digit] != 0)
        for row in digits
        for digit in range(2, maximum_digit + 1)
    )
    if objective != int(stored["best_objective"]):
        raise AssertionError("a checkpoint objective changed")
    if stored["status"] != "UNKNOWN":
        raise AssertionError("a bounded checkpoint status was overstated")
    return {
        "candidate_index": candidate_index,
        "maximum_digit": maximum_digit,
        "objective": objective,
        "placement_trits_sha256": stored["placement_trits_sha256"],
    }


def audit() -> dict[str, object]:
    stored = json.loads(CHECKPOINTS.read_text())
    digit_three = tuple(
        replay_point(point, 3)
        for point in stored["digit_3_tabu"]
    )
    digit_four = replay_point(stored["digit_4_tabu"], 4)
    if tuple(point["candidate_index"] for point in digit_three) != tuple(
        range(5)
    ):
        raise AssertionError("the five-profile checkpoint order changed")
    if stored["digit_3_cp_sat"]["status"] != "UNKNOWN":
        raise AssertionError("the CP-SAT status was overstated")
    if stored["random_codimension_12_slices"]["status"] != "UNKNOWN":
        raise AssertionError("the slice status was overstated")
    localized = replay_point(
        stored["stage_2_5_localized_tabu"], 3
    )
    if not stored["stage_2_5_localized_tabu"][
        "delayed_e1_origin_enforced"
    ]:
        raise AssertionError("the localized hyperplane flag changed")
    row_margin = stored["row_margin_digit_2_cp_sat"]
    if row_margin["union"]["status"] != "UNKNOWN":
        raise AssertionError("the row-margin union status was overstated")
    shards = row_margin["fixed_target_shards"]
    if tuple(shard["target_index"] for shard in shards) != (
        0,
        9,
        18,
        27,
        36,
        45,
        54,
        63,
    ):
        raise AssertionError("the row-margin shard sample changed")
    if any(shard["status"] != "UNKNOWN" for shard in shards):
        raise AssertionError("a row-margin shard status was overstated")
    permutation = stored["row_margin_permutation_tabu"]
    candidate_index = int(permutation["candidate_index"])
    candidate = second.CANDIDATES[candidate_index]
    if permutation["label"] != candidate[0]:
        raise AssertionError("the permutation profile label changed")
    profiles = second.profiles_from_ids(candidate[3], candidate[4])
    placement = tuple(map(int, permutation["placement_trits"]))
    if compact_hash(placement) != permutation["placement_trits_sha256"]:
        raise AssertionError("the permutation placement hash changed")
    first_count = sum(
        value != 0
        for value in second.symbolic_first_digits(
            second.first_digit_equations(profiles), placement
        )
    )
    second_count = sum(
        value != 0
        for value in second.symbolic_second_digits(
            second.second_digit_term_data(profiles), placement
        )
    )
    if (
        first_count,
        second_count,
    ) != (
        int(permutation["best_first_digit_nonzero_rows"]),
        int(permutation["best_second_digit_nonzero_rows"]),
    ):
        raise AssertionError("the permutation objective changed")
    masks = second.masks_from_trits(profiles, placement)
    phase_sums = phase_sums_from_masks(*masks)
    stored_sums = tuple(
        tuple(tuple(value) for value in channel)
        for channel in permutation["phase_sums"]
    )
    if phase_sums != stored_sums:
        raise AssertionError("the permutation phase sums changed")
    catalog = catalog_phase_sum_intersection(candidate[3], candidate[4])
    target_index = int(permutation["target_index"])
    if phase_sums != catalog["phase_sum_corpus"][target_index][0]:
        raise AssertionError("the permutation point left its target")
    if permutation["status"] != "UNKNOWN":
        raise AssertionError("the permutation status was overstated")
    result = {
        "schema": stored["schema"],
        "digit_3_objectives": tuple(
            point["objective"] for point in digit_three
        ),
        "digit_4_objective": digit_four["objective"],
        "localized_stage_2_5_objective": localized["objective"],
        "row_margin_digit_2_union": "UNKNOWN",
        "row_margin_digit_2_shards": len(shards),
        "row_margin_permutation_objective": (
            first_count,
            second_count,
        ),
        "all_statuses": "UNKNOWN",
    }
    return result


def main() -> None:
    result = audit()
    print(json.dumps(result, indent=2))
    print(f"semantic_sha256={compact_hash(result)}")


if __name__ == "__main__":
    main()
