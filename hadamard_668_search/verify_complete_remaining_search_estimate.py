#!/usr/bin/env python3
"""Dependency-free arithmetic replay of the complete LP(333) search estimate."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SHELL_TWO_CERTIFICATE = (
    ROOT
    / "shell_two_exact"
    / "shell_two_exact_orbits_certificate.json"
)


def polynomial_power(
    coefficients: tuple[int, ...], exponent: int
) -> tuple[int, ...]:
    result = (1,)
    for _ in range(exponent):
        product = [0] * (len(result) + len(coefficients) - 1)
        for left, left_value in enumerate(result):
            for right, right_value in enumerate(coefficients):
                product[left + right] += left_value * right_value
        result = tuple(product)
    return result


def bivariate_counts(
    local_by_occupancy: tuple[int, ...], quartets: int
) -> dict[tuple[int, int], int]:
    """Return counts indexed by (total occupancy, nonempty quartets)."""

    states = {(0, 0): 1}
    for _ in range(quartets):
        updated: dict[tuple[int, int], int] = {}
        for (occupancy, nonempty), count in states.items():
            for local_occupancy, multiplicity in enumerate(
                local_by_occupancy
            ):
                if not multiplicity:
                    continue
                key = (
                    occupancy + local_occupancy,
                    nonempty + int(local_occupancy != 0),
                )
                updated[key] = (
                    updated.get(key, 0) + count * multiplicity
                )
        states = updated
    return states


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def audit() -> dict[str, object]:
    # For one opposite quartet, no singleton medium support is legal.
    unsigned_local = (1, 0, 6, 4, 1)
    signed_local = (1, 0, 12, 8, 6)
    unsigned = polynomial_power(unsigned_local, 6)
    signed = polynomial_power(signed_local, 6)
    support_counts = (unsigned[15], unsigned[18])
    signed_counts = (signed[15], signed[18])
    if support_counts != (510_384, 107_476):
        raise AssertionError("the dense-shell support counts changed")
    if signed_counts != (59_743_488, 47_730_304):
        raise AssertionError("the dense-shell signed counts changed")

    by_r = bivariate_counts(signed_local, 6)
    displayed_by_r = {
        "h1_r4": by_r[(15, 4)],
        "h1_r5": by_r[(15, 5)],
        "h1_r6": by_r[(15, 6)],
        "h0_r5": by_r[(18, 5)],
        "h0_r6": by_r[(18, 6)],
    }
    if displayed_by_r != {
        "h1_r4": 103_680,
        "h1_r5": 12_085_248,
        "h1_r6": 47_554_560,
        "h0_r5": 1_296_000,
        "h0_r6": 46_434_304,
    }:
        raise AssertionError("a dense-shell nonempty-quartet count changed")

    h1_medium = (
        displayed_by_r["h1_r4"] * 3**10
        + displayed_by_r["h1_r5"] * 3**9
        + displayed_by_r["h1_r6"] * 3**8
    )
    h0_medium = (
        displayed_by_r["h0_r5"] * 3**12
        + displayed_by_r["h0_r6"] * 3**11
    )
    affine_upper = {
        "h1_medium": h1_medium,
        "h1_high_positions": 9 * h1_medium,
        "h1_high_orientations": 27 * h1_medium,
        "h0_medium": h0_medium,
        "combined": 27 * h1_medium + h0_medium,
    }
    if affine_upper != {
        "h1_medium": 556_001_604_864,
        "h1_high_positions": 5_004_014_443_776,
        "h1_high_orientations": 15_012_043_331_328,
        "h0_medium": 8_914_445_186_688,
        "combined": 23_926_488_518_016,
    }:
        raise AssertionError("a dense-shell affine upper bound changed")

    characters = {
        "maximum_reuse": sum(signed_counts) * 729,
        "unbatched_high_positions": (
            9 * signed_counts[0] + signed_counts[1]
        )
        * 729,
        "support_precomputation": sum(support_counts) * 729,
    }
    if characters != {
        "maximum_reuse": 78_348_394_368,
        "unbatched_high_positions": 426_772_416_384,
        "support_precomputation": 450_419_940,
    }:
        raise AssertionError("a 729-character work count changed")

    stored = json.loads(SHELL_TWO_CERTIFICATE.read_text())
    margin_counts = tuple(
        int(orbit["compatible_row_margin_catalog_rows"])
        for orbit in stored["orbits"]
    )
    if margin_counts != (72, 72, 72, 96, 93):
        raise AssertionError("the shell-two margin counts changed")

    h2_points = 5 * 3**36
    if h2_points != 750_473_176_484_995_605:
        raise AssertionError("the five-profile affine volume changed")
    if not 135**2 < 3**9:
        raise AssertionError("the digit-eight exactness inequality failed")

    result = {
        "schema": "lp333-order3-complete-search-estimate-v1",
        "unsigned_local_polynomial": unsigned_local,
        "signed_local_polynomial": signed_local,
        "support_counts_h1_h0": support_counts,
        "signed_skeleton_counts_h1_h0": signed_counts,
        "signed_counts_by_nonempty_quartets": displayed_by_r,
        "dense_affine_upper_bounds": affine_upper,
        "character_evaluation_counts": characters,
        "shell_two_row_margin_counts": margin_counts,
        "shell_two_row_margin_shards": sum(margin_counts),
        "five_shell_two_affine_points": h2_points,
        "exactness_inequality": {
            "residual_norm_bound": 135**2,
            "lambda_nine_norm": 3**9,
        },
    }
    return {**result, "semantic_sha256": compact_hash(result)}


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
