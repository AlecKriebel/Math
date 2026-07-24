#!/usr/bin/env python3
"""Dependency-free exact replay of the two stage-2.5 witnesses."""

from __future__ import annotations

import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SECOND_DIGIT = HERE.parent
SEARCH_ROOT = SECOND_DIGIT.parent
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_phase_second_digit as second  # noqa: E402
from verify_full_second_digit_witness import compact_hash  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
    phase_sums_from_masks,
)


CERTIFICATE = HERE / "stage_2_5_witnesses.json"


def replay_witness(stored: dict[str, object]) -> dict[str, object]:
    candidate_index = int(stored["candidate_index"])
    candidate = second.CANDIDATES[candidate_index]
    if stored["label"] != candidate[0]:
        raise AssertionError("the stage-2.5 profile label changed")
    profiles = second.profiles_from_ids(candidate[3], candidate[4])
    equations = second.first_digit_equations(profiles)
    origin, basis = second.affine_parameterization(equations, 54)
    affine = tuple(map(int, stored["affine_coordinates"]))
    if len(affine) != 36 or any(value not in (0, 1, 2) for value in affine):
        raise AssertionError("invalid stage-2.5 affine coordinates")
    if compact_hash(affine) != stored["affine_coordinates_sha256"]:
        raise AssertionError("a stage-2.5 affine hash changed")
    placement = second.lift_affine_point(origin, basis, affine)
    if compact_hash(placement) != stored["placement_trits_sha256"]:
        raise AssertionError("a stage-2.5 placement hash changed")
    if second.symbolic_first_digits(equations, placement) != (0,) * 20:
        raise AssertionError("a stage-2.5 point left the first-digit space")
    term_data = second.second_digit_term_data(profiles)
    if second.symbolic_second_digits(term_data, placement) != (0,) * 20:
        raise AssertionError("a stage-2.5 point failed symbolic digit 2")
    values = second.displayed_values(profiles, placement)
    digits = tuple(second.lambda_digits(value, 10) for value in values)
    if any(row[:3] != (0, 0, 0) for row in digits):
        raise AssertionError("a stage-2.5 point lost a lower exact digit")
    if digits[7][3] != 0:
        raise AssertionError("the delayed E1-origin digit 3 is nonzero")
    counts = tuple(
        sum(row[digit] != 0 for row in digits) for digit in range(9)
    )
    if counts != tuple(stored["digit_nonzero_rows_through_8"]):
        raise AssertionError("the stage-2.5 digit counts changed")
    if counts[3] == 0:
        raise AssertionError("a certificate was overstated as only stage 2.5")
    if values[7] != tuple(stored["delayed_e1_origin_exact_value"]):
        raise AssertionError("the delayed exact coefficient changed")
    if digits[7][:9] != tuple(
        stored["delayed_e1_origin_digits_through_8"]
    ):
        raise AssertionError("the delayed exact digits changed")
    exact_zero_rows = tuple(
        row for row, value in enumerate(values) if value == (0, 0)
    )
    if exact_zero_rows != tuple(stored["exact_zero_displayed_rows"]):
        raise AssertionError("the exact-zero row list changed")
    masks = second.masks_from_trits(profiles, placement)
    phase_sums = phase_sums_from_masks(*masks)
    expected_sums = tuple(
        tuple(tuple(value) for value in channel)
        for channel in stored["phase_sums"]
    )
    if phase_sums != expected_sums:
        raise AssertionError("the stage-2.5 phase sums changed")
    catalog = catalog_phase_sum_intersection(candidate[3], candidate[4])
    row_margin_join = phase_sums in {
        sums for sums, _ in catalog["phase_sum_corpus"]
    }
    if row_margin_join != bool(stored["row_margin_join_holds"]):
        raise AssertionError("the stage-2.5 row-margin join changed")
    if row_margin_join:
        raise AssertionError("a nonviable stage-2.5 seed became viable")
    return {
        "candidate_index": candidate_index,
        "label": candidate[0],
        "placement_trits_sha256": stored["placement_trits_sha256"],
        "digit_3_nonzero_rows": counts[3],
        "delayed_e1_origin_digit_3": digits[7][3],
        "row_margin_join_holds": row_margin_join,
    }


def audit() -> dict[str, object]:
    stored = json.loads(CERTIFICATE.read_text())
    if stored["schema"] != "lp333-order3-stage-2-5-witnesses-v1":
        raise AssertionError("the stage-2.5 schema changed")
    census = stored["bounded_census"]
    if tuple(record["candidate_index"] for record in census) != tuple(
        range(5)
    ):
        raise AssertionError("the stage-2.5 census lost a profile")
    if any(record["status"] != "BOUNDED_COMPLETE" for record in census):
        raise AssertionError("a bounded census status changed")
    if sum(record["distinct_digit2_hits"] for record in census) != 9:
        raise AssertionError("the bounded digit-2 hit count changed")
    if sum(record["row7_zero_hits"] for record in census) != 2:
        raise AssertionError("the bounded stage-2.5 hit count changed")
    witnesses = tuple(replay_witness(point) for point in stored["witnesses"])
    if tuple(point["candidate_index"] for point in witnesses) != (0, 2):
        raise AssertionError("the stage-2.5 witness profiles changed")
    return {
        "schema": stored["schema"],
        "bounded_digit_2_hits": 9,
        "bounded_stage_2_5_hits": 2,
        "viable_stage_2_5_hits": sum(
            point["row_margin_join_holds"] for point in witnesses
        ),
        "witnesses": witnesses,
    }


def main() -> None:
    result = audit()
    print(json.dumps(result, indent=2))
    print(f"semantic_sha256={compact_hash(result)}")


if __name__ == "__main__":
    main()
