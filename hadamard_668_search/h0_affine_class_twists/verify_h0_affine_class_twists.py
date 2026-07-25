#!/usr/bin/env python3
"""Exact affine-in-class half-turn census for the pinned h=0 profile.

For each channel choose ``(epsilon,a,b)`` in

    F_3^* x F_3 x F_3.

On the opposite cyclotomic-class pair ``j,j+6``, impose

    W_(j+6)(s,q) = W_j(s, epsilon*q + a*j + b).

The slope ``a`` makes this a class-dependent row shear.  When ``a=0`` this
is exactly the previously audited global S3 fiber-permutation family,
because every permutation of F_3 is affine.  At least one nonzero slope is
therefore the genuinely new part of the census.

The verifier reconstructs every affine system from the exact phase
equations.  Every consistent nonidentity family has dimension nine, so its
complete second placement digit is exhausted without a solver or timeout.
This is a fixed-profile structured-family obstruction, not an LP(333) or
H(668).
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
HALFTURN_ROOT = SEARCH_ROOT / "h0_halfturn_twists"
PHASE_ROOT = SEARCH_ROOT / "phase_second_digit"
sys.path.insert(0, str(HALFTURN_ROOT))
sys.path.insert(0, str(PHASE_ROOT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_h0_halfturn_twists as halfturn  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    canonical_solution,
    first_digit_equations,
    matrix_rank,
    profiles_from_ids,
)
from verify_lp333_order3_trit_lift import (  # noqa: E402
    active_trit_coordinates,
)


MODULUS = 3
PARAMETERS = tuple(product((1, 2), range(3), range(3)))
IDENTITY = (1, 0, 0)
EXPECTED_RECORDS_SHA256 = (
    "4ed1c0043d04d5b45bf9cb08b1a975a1c455b9b00202df639a937bd87eb9dbc4"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return sha256(payload).hexdigest()


def class_permutation(
    parameters: Sequence[int], class_index: int
) -> tuple[int, int, int]:
    """Return ``q -> epsilon*q+a*j+b`` on F_3."""

    if (
        len(parameters) != 3
        or int(parameters[0]) % MODULUS not in (1, 2)
        or not 0 <= class_index < 6
    ):
        raise ValueError("invalid affine-in-class parameters")
    epsilon, slope, offset = (
        int(value) % MODULUS for value in parameters
    )
    permutation = tuple(
        (epsilon * quotient + slope * class_index + offset) % MODULUS
        for quotient in range(MODULUS)
    )
    if set(permutation) != set(range(MODULUS)):
        raise AssertionError("an affine class rule is not a permutation")
    return permutation  # type: ignore[return-value]


def affine_class_system(
    parameters_a: Sequence[int],
    parameters_b: Sequence[int],
) -> tuple[
    tuple[tuple[tuple[int, int, int], ...], ...],
    tuple[tuple[int, ...], ...],
    tuple[int, ...] | None,
    tuple[tuple[int, ...], ...] | None,
]:
    """Add the two channel-specific affine-in-class pairings."""

    profiles = profiles_from_ids(
        halfturn.PROFILE_IDS_A,
        halfturn.PROFILE_IDS_B,
    )
    coordinates = active_trit_coordinates(profiles)
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    rows = list(augmented_system(first_digit_equations(profiles)))
    for channel, parameters in enumerate((parameters_a, parameters_b)):
        for class_index in range(6):
            opposite = class_index + 6
            if profiles[channel][class_index] != profiles[channel][opposite]:
                raise AssertionError("the pinned profile lost its half-turn")
            permutation = class_permutation(parameters, class_index)
            for residue, count in enumerate(
                profiles[channel][class_index]
            ):
                if count not in (1, 2):
                    continue
                trit_slope, trit_offset = (
                    halfturn.permutation_affine_action(count, permutation)
                )
                row = [0] * (len(coordinates) + 1)
                row[
                    coordinate_index[(channel, opposite, residue)]
                ] = 1
                row[
                    coordinate_index[(channel, class_index, residue)]
                ] = -trit_slope % MODULUS
                row[-1] = trit_offset
                rows.append(tuple(row))

    normalized_rows = tuple(rows)
    origin = canonical_solution(normalized_rows, len(coordinates))
    if origin is None:
        return profiles, normalized_rows, None, None
    basis = second.nullspace_basis(
        tuple(row[:-1] for row in normalized_rows),
        columns=len(coordinates),
    )
    return profiles, normalized_rows, origin, basis


def verify_global_subfamily(
    records: Sequence[dict[str, object]],
) -> None:
    """Check that the zero-slope slice is the prior 36-family theorem."""

    old = halfturn.classify_global_fiber_twists()
    expected = Counter()
    for record in old["records"]:
        dimension = record["dimension"]
        label = "inconsistent" if dimension is None else f"dimension_{dimension}"
        expected[label] += 1

    actual = Counter()
    for record in records:
        parameters_a = tuple(record["parameters_a"])  # type: ignore[arg-type]
        parameters_b = tuple(record["parameters_b"])  # type: ignore[arg-type]
        if parameters_a[1] or parameters_b[1]:
            continue
        dimension = record["dimension"]
        label = "inconsistent" if dimension is None else f"dimension_{dimension}"
        actual[label] += 1
    if actual != expected:
        raise AssertionError(
            f"the zero-slope slice changed: {actual} != {expected}"
        )


def classify_affine_class_twists() -> dict[str, object]:
    """Classify all 18^2 families through the complete second digit."""

    records = []
    outcome_histogram: Counter[str] = Counter()
    slope_histogram: Counter[str] = Counter()
    enumerated_points = 0

    for parameters_a in PARAMETERS:
        for parameters_b in PARAMETERS:
            profiles, rows, origin, basis = affine_class_system(
                parameters_a,
                parameters_b,
            )
            coefficient_rank = matrix_rank(
                tuple(row[:-1] for row in rows)
            )
            augmented_rank = matrix_rank(rows)
            new_family = bool(parameters_a[1] or parameters_b[1])

            if origin is None:
                if augmented_rank != coefficient_rank + 1:
                    raise AssertionError(
                        "an inconsistent family did not gain one rank"
                    )
                dimension = None
                second_digit_survivors = None
                outcome = "inconsistent"
            else:
                if basis is None or coefficient_rank != augmented_rank:
                    raise AssertionError("a consistent system lost its basis")
                dimension = len(basis)
                if dimension == 9:
                    second_digit_survivors = (
                        halfturn.exhaust_dimension_nine_second_digit(
                            profiles,
                            origin,
                            basis,
                        )
                    )
                    enumerated_points += MODULUS**dimension
                    if second_digit_survivors:
                        raise AssertionError(
                            "an affine class twist survived digit two"
                        )
                    outcome = "dimension_9"
                elif dimension == 21:
                    second_digit_survivors = None
                    if (
                        tuple(parameters_a),
                        tuple(parameters_b),
                    ) != (IDENTITY, IDENTITY):
                        raise AssertionError(
                            "a nonidentity family retained dimension 21"
                        )
                    outcome = "dimension_21"
                else:
                    raise AssertionError(
                        f"unexpected affine dimension {dimension}"
                    )

            outcome_histogram[outcome] += 1
            slope_histogram[
                ("new_" if new_family else "global_") + outcome
            ] += 1
            records.append({
                "parameters_a": tuple(parameters_a),
                "parameters_b": tuple(parameters_b),
                "coefficient_rank": coefficient_rank,
                "augmented_rank": augmented_rank,
                "dimension": dimension,
                "second_digit_survivors": second_digit_survivors,
                "new_nonzero_slope_family": new_family,
            })

    expected_outcomes = {
        "inconsistent": 161,
        "dimension_9": 162,
        "dimension_21": 1,
    }
    expected_slopes = {
        "global_inconsistent": 17,
        "global_dimension_9": 18,
        "global_dimension_21": 1,
        "new_inconsistent": 144,
        "new_dimension_9": 144,
    }
    if dict(outcome_histogram) != expected_outcomes:
        raise AssertionError(
            f"outcome histogram changed: {dict(outcome_histogram)}"
        )
    if dict(slope_histogram) != expected_slopes:
        raise AssertionError(
            f"slope histogram changed: {dict(slope_histogram)}"
        )
    if enumerated_points != 162 * MODULUS**9:
        raise AssertionError("the dimension-nine point census changed")

    verify_global_subfamily(records)
    records_hash = compact_hash(records)
    if EXPECTED_RECORDS_SHA256 and records_hash != EXPECTED_RECORDS_SHA256:
        raise AssertionError(
            "affine-class record hash changed: "
            f"{records_hash} != {EXPECTED_RECORDS_SHA256}"
        )
    return {
        "families": len(records),
        "new_nonzero_slope_families": sum(
            bool(record["new_nonzero_slope_family"]) for record in records
        ),
        "outcome_histogram": expected_outcomes,
        "slope_histogram": expected_slopes,
        "dimension_nine_points_exhausted": enumerated_points,
        "nonidentity_second_digit_survivors": 0,
        "records_sha256": records_hash,
        "status": "PASS",
    }


def main() -> None:
    result = classify_affine_class_twists()
    for key, value in result.items():
        print(f"{key}={value}")
    print("PASS: all affine-in-class half-turn twists classified")
    print("STATUS: structured h=0 obstruction only; no LP(333) or H(668)")


if __name__ == "__main__":
    main()
