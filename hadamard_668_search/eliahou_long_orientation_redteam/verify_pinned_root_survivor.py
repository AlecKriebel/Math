#!/usr/bin/env python3
"""Independently replay the sole exact-root point in the parallel sample."""

from __future__ import annotations

import json

import numpy as np

import audit_orientation_redteam as audit


SUPPORT = {
    ("L", 5), ("L", 7), ("L", 8), ("L", 12), ("L", 14),
    ("L", 19), ("L", 20), ("L", 21), ("L", 22), ("L", 24),
    ("L", 25), ("L", 32), ("L", 37), ("L", 39), ("L", 40),
    ("S", 2), ("S", 3), ("S", 4), ("S", 7), ("S", 9),
    ("S", 11), ("S", 12), ("S", 14), ("S", 15), ("S", 19),
    ("S", 20), ("S", 22), ("S", 23), ("S", 24), ("S", 26),
    ("S", 27), ("S", 28), ("S", 33), ("S", 34), ("S", 35),
    ("S", 36), ("S", 37), ("S", 38), ("S", 39),
}

EXPECTED = {
    "case": 5,
    "q_index": 35,
    "profile": 0,
    "support_sha256": (
        "b1ac33262ac93f840ed08870a61b65d6b13c5a1acde4ed803b8ebd8f424a9d20"
    ),
    "mod16_rank": 22,
    "mod16_augmented_rank": 22,
    "mod16_nullity": 17,
    "mod16_exact_root_points": 1094,
    "mod32_points": 131072,
    "mod32_survivors": 1,
    "mod32_exact_root_survivors": 1,
    "mod64_exact_root_survivors": 0,
    "mod32_coefficient_rank": 20,
    "mod32_augmented_coefficient_rank": 20,
    "mod32_quadratic_row_rank": 18,
    "mod32_common_polar_radical_dimension": 0,
    "mod32_polar_rank_histogram": {"0": 2, "2": 7, "4": 7, "6": 5},
}

EXPECTED_SURVIVOR = {
    "coordinate_assignment": 73580,
    "root_values": [-3, -5, 4, -4],
    "root_exact": True,
    "paf": [
        -32, 32, 0, 0, 32, 0, -32, 0, 32, -32, 32,
        -64, 0, 64, -32, -32, 0, 0, 0, 32, 0,
    ],
}


def main() -> None:
    _, keys, *_ = audit.raw_antimod2_space(5)
    support = np.asarray([key in SUPPORT for key in keys], dtype=np.uint8)
    if int(support.sum()) != 39:
        raise AssertionError("pinned support lost weight 39")
    result = audit.audit_fixture(5, 0, 3, support, deep_replay=True)
    observed = {key: result[key] for key in EXPECTED}
    if observed != EXPECTED:
        raise AssertionError(
            json.dumps(
                {"expected": EXPECTED, "observed": observed},
                indent=2,
                sort_keys=True,
            )
        )
    if result["mod32_survivor_examples"] != [EXPECTED_SURVIVOR]:
        raise AssertionError("the pinned physical survivor replay changed")
    print(
        json.dumps(
            {
                "status": (
                    "independent physical replay passed; the point satisfies "
                    "plus mod32 and exact roots but fails plus mod64"
                ),
                "certificate": observed,
                "survivor": EXPECTED_SURVIVOR,
                "scope": (
                    "one bounded support fixture; no long case excluded and "
                    "no base sequence or H(668) constructed"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
