#!/usr/bin/env python3
"""Replay all saved digit-2 census hits and their row-margin joins."""

from __future__ import annotations

import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SECOND_DIGIT = HERE.parent
SEARCH_ROOT = SECOND_DIGIT.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_phase_second_digit as second  # noqa: E402
from verify_full_second_digit_witness import compact_hash  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
    phase_sums_from_masks,
)


CENSUS = HERE / "digit2_row7_census"


def replay_file(path: Path, candidate_index: int) -> dict[str, object]:
    stored = json.loads(path.read_text())
    semantic_hash = stored.pop("semantic_sha256")
    if compact_hash(stored) != semantic_hash:
        raise AssertionError("a census semantic hash changed")
    if stored["schema"] != "lp333-order3-digit2-row7-bounded-census-v1":
        raise AssertionError("a census schema changed")
    if int(stored["candidate_index"]) != candidate_index:
        raise AssertionError("a census candidate index changed")
    candidate = second.CANDIDATES[candidate_index]
    if stored["label"] != candidate[0]:
        raise AssertionError("a census profile label changed")
    if stored["status"] != "BOUNDED_COMPLETE":
        raise AssertionError("a census status was overstated")
    profiles = second.profiles_from_ids(candidate[3], candidate[4])
    equations = second.first_digit_equations(profiles)
    origin, basis = second.affine_parameterization(equations, 54)
    catalog = catalog_phase_sum_intersection(candidate[3], candidate[4])
    corpus = {sums for sums, _ in catalog["phase_sum_corpus"]}
    hashes = set()
    row7_zero = 0
    row_margin = 0
    for hit in stored["hits"]:
        affine = tuple(map(int, hit["affine_coordinates"]))
        if compact_hash(affine) != hit["affine_coordinates_sha256"]:
            raise AssertionError("a census affine hash changed")
        placement = second.lift_affine_point(origin, basis, affine)
        placement_hash = compact_hash(placement)
        if placement_hash != hit["placement_trits_sha256"]:
            raise AssertionError("a census placement hash changed")
        if placement_hash in hashes:
            raise AssertionError("a census contains a duplicate hit")
        hashes.add(placement_hash)
        digits = tuple(
            second.lambda_digits(value, 10)
            for value in second.displayed_values(profiles, placement)
        )
        if any(row[:3] != (0, 0, 0) for row in digits):
            raise AssertionError("a census hit lost digit 2")
        if digits[7][3] != int(hit["delayed_e1_origin_digit3"]):
            raise AssertionError("a census delayed-row value changed")
        if sum(row[3] != 0 for row in digits) != int(
            hit["digit3_nonzero_rows"]
        ):
            raise AssertionError("a census digit-3 count changed")
        row7_zero += int(digits[7][3] == 0)
        masks = second.masks_from_trits(profiles, placement)
        sums = phase_sums_from_masks(*masks)
        row_margin += int(sums in corpus)
    if len(hashes) != int(stored["distinct_digit2_hits"]):
        raise AssertionError("a census hit total changed")
    if row7_zero != int(stored["row7_zero_hits"]):
        raise AssertionError("a census stage-2.5 total changed")
    return {
        "candidate_index": candidate_index,
        "label": candidate[0],
        "digit_2_hits": len(hashes),
        "stage_2_5_hits": row7_zero,
        "row_margin_compatible_hits": row_margin,
        "source_semantic_sha256": semantic_hash,
    }


def audit() -> dict[str, object]:
    profiles = tuple(
        replay_file(CENSUS / f"candidate_{index}.json", index)
        for index in range(5)
    )
    result = {
        "schema": "lp333-order3-digit2-row7-census-replay-v1",
        "profiles": profiles,
        "total_digit_2_hits": sum(
            profile["digit_2_hits"] for profile in profiles
        ),
        "total_stage_2_5_hits": sum(
            profile["stage_2_5_hits"] for profile in profiles
        ),
        "total_row_margin_compatible_hits": sum(
            profile["row_margin_compatible_hits"] for profile in profiles
        ),
    }
    if result["total_digit_2_hits"] != 9:
        raise AssertionError("the five-profile census hit count changed")
    if result["total_stage_2_5_hits"] != 2:
        raise AssertionError("the five-profile stage-2.5 count changed")
    if result["total_row_margin_compatible_hits"] != 0:
        raise AssertionError("a saved census hit entered the margin corpus")
    return result


def main() -> None:
    result = audit()
    print(json.dumps(result, indent=2))
    print(f"semantic_sha256={compact_hash(result)}")


if __name__ == "__main__":
    main()
