#!/usr/bin/env python3
"""Exact integral primitive-nine sieve for labelled order-three lifts.

The six-digit jet modulo three is only the first congruence shadow of the
primitive ninth-root equation.  For an integer correlation polynomial

    C(x) = c_0 + ... + c_8 x^8,

exact vanishing at a primitive ninth root is equivalent to divisibility by

    Phi_9(x) = x^6 + x^3 + 1.

Because the degree is at most eight, this says exactly

    c_s = c_(s+3) = c_(s+6),    s=0,1,2.

This module reconstructs the labelled plus supports, evaluates all exact
integer correlations, and audits that stronger equidistribution law.
"""

from __future__ import annotations

from functools import reduce
from hashlib import sha256
import json
from math import gcd
from typing import Sequence

from verify_lp333_order3_labeled_jet import (
    CLASS_COUNT,
    LABELLED_SURVIVOR_AGGREGATE,
    LABELLED_SURVIVOR_MASKS_A,
    LABELLED_SURVIVOR_MASKS_B,
    P,
    ROWS,
    ZERO_A_PLUS,
    ZERO_B_PLUS,
    actual_word,
    validate_labelled_certificate,
)
from verify_lp333_order3_primitive9_jet import CLASSES
from verify_lp333_order3_quotient import PARTS
from verify_lp333_order3_trit_lift import (
    TRIT_SURVIVOR_MASKS_A,
    TRIT_SURVIVOR_MASKS_B,
)


EXPECTED_PINNED_TABLE_SHA256 = (
    "4f9d704942b8105fda93ee4672a388fff0b830ec2fbcc9ef85685893bbc19244"
)
EXPECTED_TRIT_TABLE_SHA256 = (
    "063254151ec2c77b0ee806cb1e485963182ecece696f34f8bc175d115b478ab7"
)

CLASS_OF = {
    value: class_index
    for class_index, part in enumerate(CLASSES)
    for value in part
}


def divide_by_phi9(
    coefficients: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Divide an integer polynomial by x^6+x^3+1."""

    work = [int(value) for value in coefficients]
    if not work:
        work = [0]
    quotient = [0] * max(1, len(work) - 6)
    for degree in range(len(work) - 1, 5, -1):
        factor = work[degree]
        quotient[degree - 6] = factor
        work[degree] -= factor
        work[degree - 3] -= factor
        work[degree - 6] -= factor
    while len(quotient) > 1 and quotient[-1] == 0:
        quotient.pop()
    remainder = work[:6]
    while len(remainder) > 1 and remainder[-1] == 0:
        remainder.pop()
    return tuple(quotient), tuple(remainder)


def primitive9_remainder(correlations: Sequence[int]) -> tuple[int, ...]:
    if len(correlations) != ROWS:
        raise ValueError("a row-correlation vector must have length nine")
    _, remainder = divide_by_phi9(correlations)
    return tuple(
        remainder[index] if index < len(remainder) else 0
        for index in range(6)
    )


def equidistribution_remainder(
    correlations: Sequence[int],
) -> tuple[int, ...]:
    if len(correlations) != ROWS:
        raise ValueError("a row-correlation vector must have length nine")
    return tuple(
        value
        for residue in range(3)
        for value in (
            correlations[residue] - correlations[residue + 6],
            correlations[residue + 3] - correlations[residue + 6],
        )
    )


def verify_divisibility_criterion() -> dict[str, object]:
    """Check the exact remainder formula on a spanning integer family."""

    test_vectors = []
    test_vectors.extend(
        tuple(int(index == basis) for index in range(ROWS))
        for basis in range(ROWS)
    )
    test_vectors.extend(
        (
            first,
            second,
            third,
            first,
            second,
            third,
            first,
            second,
            third,
        )
        for first in (-2, 0, 3)
        for second in (-1, 1)
        for third in (0, 4)
    )
    for vector in test_vectors:
        polynomial = primitive9_remainder(vector)
        equidistribution = equidistribution_remainder(vector)
        # Polynomial-basis order is (s=0,1,2) followed by (s+3).
        reordered = (
            equidistribution[0],
            equidistribution[2],
            equidistribution[4],
            equidistribution[1],
            equidistribution[3],
            equidistribution[5],
        )
        if polynomial != reordered:
            raise AssertionError("the Phi_9 remainder formula changed")
    return {
        "cyclotomic_polynomial": (1, 0, 0, 1, 0, 0, 1),
        "test_vectors": len(test_vectors),
        "equidistribution_groups": 3,
        "integer_equations_per_column_class": 6,
    }


def expand_columns(
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    if len(masks_a) != CLASS_COUNT or len(masks_b) != CLASS_COUNT:
        raise ValueError("each channel needs twelve normalized masks")
    result = []
    for channel, masks in enumerate((masks_a, masks_b)):
        class_words = tuple(
            actual_word(channel, class_index, masks[class_index])
            for class_index in range(CLASS_COUNT)
        )
        zero = (ZERO_A_PLUS, ZERO_B_PLUS)[channel]
        result.append(
            tuple(
                zero if column == 0 else class_words[CLASS_OF[column]]
                for column in range(P)
            )
        )
    return tuple(result)  # type: ignore[return-value]


def full_correlation_table(
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    """Return the exact residual row polynomial at every physical column lag."""

    columns = expand_columns(masks_a, masks_b)
    result = []
    for column_lag in range(P):
        row_values = []
        for row_lag in range(ROWS):
            value = sum(
                channel[(column + column_lag) % P][
                    (row + row_lag) % ROWS
                ]
                * channel[column][row]
                for channel in columns
                for column in range(P)
                for row in range(ROWS)
            )
            if column_lag == 0 and row_lag == 0:
                value -= 167
            row_values.append(value)
        result.append(tuple(row_values))
    return tuple(result)


def invariant_correlation_table(
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    physical = full_correlation_table(masks_a, masks_b)
    result = []
    for part in PARTS:
        representative = physical[part[0]]
        if any(physical[column] != representative for column in part):
            raise AssertionError("the exact correlations lost class invariance")
        result.append(representative)
    return tuple(result)


def table_hash(table: object) -> str:
    payload = json.dumps(table, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def audit_integral_primitive9(
    aggregate: Sequence[int],
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> dict[str, object]:
    """Replay the mod-three certificate and audit exact Phi_9 divisibility."""

    modular = validate_labelled_certificate(aggregate, masks_a, masks_b)
    table = invariant_correlation_table(masks_a, masks_b)
    remainders = tuple(
        equidistribution_remainder(row) for row in table
    )
    flat = tuple(value for row in remainders for value in row)
    bad_groups = sum(
        len(
            {
                row[residue],
                row[residue + 3],
                row[residue + 6],
            }
        )
        > 1
        for row in table
        for residue in range(3)
    )
    nonzero_equations = sum(value != 0 for value in flat)
    common_divisor = reduce(gcd, flat, 0)
    return {
        "invariant_column_classes": len(table),
        "displayed_integer_equations": len(flat),
        "nonzero_integer_equations": nonzero_equations,
        "bad_equidistribution_groups": bad_groups,
        "maximum_absolute_defect": max(abs(value) for value in flat),
        "defect_gcd": abs(common_divisor),
        "all_defects_divisible_by_three": all(
            value % 3 == 0 for value in flat
        ),
        "exact_integral_survivor": not any(flat),
        "correlation_table_sha256": table_hash(table),
        "modular_jet_equations": modular["jet_equations"],
    }


def validate_integral_primitive9(
    aggregate: Sequence[int],
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> dict[str, object]:
    result = audit_integral_primitive9(aggregate, masks_a, masks_b)
    if not result["exact_integral_survivor"]:
        raise ValueError("exact primitive-nine equidistribution failed")
    return result


def audit_known_modular_survivors() -> dict[str, object]:
    pinned = audit_integral_primitive9(
        LABELLED_SURVIVOR_AGGREGATE,
        LABELLED_SURVIVOR_MASKS_A,
        LABELLED_SURVIVOR_MASKS_B,
    )
    trit = audit_integral_primitive9(
        LABELLED_SURVIVOR_AGGREGATE,
        TRIT_SURVIVOR_MASKS_A,
        TRIT_SURVIVOR_MASKS_B,
    )
    if pinned["correlation_table_sha256"] != EXPECTED_PINNED_TABLE_SHA256:
        raise AssertionError("the pinned exact-correlation table changed")
    if trit["correlation_table_sha256"] != EXPECTED_TRIT_TABLE_SHA256:
        raise AssertionError("the trit exact-correlation table changed")
    return {"pinned": pinned, "trit": trit}


def main() -> None:
    criterion = verify_divisibility_criterion()
    audits = audit_known_modular_survivors()
    print(f"phi9={criterion['cyclotomic_polynomial']}")
    print(
        "integer_equations_per_column_class="
        f"{criterion['integer_equations_per_column_class']}"
    )
    for label in ("pinned", "trit"):
        result = audits[label]
        print(
            f"{label}_bad_groups={result['bad_equidistribution_groups']} "
            f"{label}_nonzero_equations="
            f"{result['nonzero_integer_equations']} "
            f"{label}_max_defect={result['maximum_absolute_defect']}"
        )
    print("PASS: exact primitive-nine integer criterion reconstructed")
    print("STATUS: both known mod-three survivors fail the exact criterion")


if __name__ == "__main__":
    main()
