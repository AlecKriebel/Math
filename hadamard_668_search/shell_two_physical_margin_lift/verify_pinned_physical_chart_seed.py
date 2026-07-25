#!/usr/bin/env python3
"""Replay the pinned physical-chart digit-two seed and tangent-sheet audit."""

from __future__ import annotations

import json

from search_physical_digit2 import search


EXPECTED_PLACEMENT_SHA256 = (
    "941b2029c2d0df0935f91bb213bb53b3ee23117f21c7cee1f9fc245eaddb8abc"
)


def verify() -> dict[str, object]:
    # One CPU second is enough to construct the deterministic exhaustive
    # 3^7 tangent sheet.  Stochastic points found after it are not trusted.
    result = search(
        candidate_index=4,
        target_index=65,
        cpu_seconds=1.0,
        seed=668_333_4,
        samples=128,
        random_samples=0,
    )
    record = result["best_record"]
    if not isinstance(record, dict):
        raise AssertionError("the pinned seed failed direct replay")
    expected = {
        "placement_sha256": EXPECTED_PLACEMENT_SHA256,
        "row_margin_exact": False,
        "margin_digit4_defect": 1,
        "margin_digit4_residuals": (0, 0, 0, 1, 0, 0),
        "active_digit_three_defect": 12,
        "active_digit_four_defect": 11,
        "digit2_jacobian_rank": 18,
        "digit2_tangent_dimension": 12,
        "margin_digit4_tangent_rank": 5,
        "margin_digit4_linearized_correction_consistent": True,
    }
    for key, value in expected.items():
        actual = record[key]
        if isinstance(value, tuple):
            actual = tuple(actual)
        if actual != value:
            raise AssertionError(
                f"pinned seed field {key} changed: {actual!r}"
            )
    sheet = result["search"]["first_targeted_tangent_sheet"]
    if not isinstance(sheet, dict):
        raise AssertionError("the exact tangent sheet was not audited")
    sheet_expected = {
        "sheet_size": 2187,
        "tangent_dimension": 12,
        "linearized_solution_dimension": 7,
        "digit2_defect_minimum": 4,
        "margin_digit4_defect_minimum": 0,
        "joint_exact_points": 0,
    }
    for key, value in sheet_expected.items():
        if sheet[key] != value:
            raise AssertionError(
                f"tangent-sheet field {key} changed: {sheet[key]!r}"
            )
    return {
        "candidate_index": result["candidate_index"],
        "target_index": result["target_index"],
        "placement_sha256": record["placement_sha256"],
        "margin_digit4_residuals": record[
            "margin_digit4_residuals"
        ],
        "active_digit_three_defect": record[
            "active_digit_three_defect"
        ],
        "active_digit_four_defect": record[
            "active_digit_four_defect"
        ],
        "tangent_sheet": {
            key: sheet[key] for key in sheet_expected
        },
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))
    print("PASS")


if __name__ == "__main__":
    main()
