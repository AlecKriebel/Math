#!/usr/bin/env python3
"""Exhaust every four-space in the six structured forms after margin rank 6.

There are [6 choose 4]_3 = 11,011 four-dimensional subspaces.  This script
represents each as the kernel of a canonical two-dimensional normal space
and uses packed ternary row reduction to find its common polar radical.  A
four-space retracts exactly when its four affine terms have rank four on
that radical.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
SECOND = SEARCH / "phase_second_digit"
sys.path[:0] = [str(HERE), str(SECOND), str(SEARCH)]

import audit_row_margin_retraction as base  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
import verify_phase_second_digit_pencil as pencil  # noqa: E402
from verify_lp333_order3_phase_hensel import canonical_solution  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
)


MODULUS = 3
EXPECTED_SEMANTIC_SHA256 = (
    "1a067c914ea5911136d2b4437d0ffb98fe80601ac545dff7e3dbd34c8216364d"
)


def canonical_two_spaces() -> tuple[
    tuple[tuple[int, ...], tuple[int, ...]], ...
]:
    """Return all 11,011 two-dimensional subspaces of F_3^6."""

    lines = tuple(base.projective_vectors(6))
    spaces = set()
    for left, right in combinations(lines, 2):
        rref, pivots, _ = second.matrix_rref((left, right))
        if len(pivots) == 2:
            spaces.add(tuple(rref))
    result = tuple(sorted(spaces))
    if len(result) != 11011:
        raise AssertionError(
            f"expected 11,011 normal two-spaces, found {len(result)}"
        )
    return result


def trit_add(
    left: tuple[int, int],
    right: tuple[int, int],
    mask: int,
) -> tuple[int, int]:
    """Add two packed F_3 vectors encoded by their one/two bitsets."""

    left_one, left_two = left
    right_one, right_two = right
    left_zero = mask ^ (left_one | left_two)
    right_zero = mask ^ (right_one | right_two)
    one = (
        (left_zero & right_one)
        | (left_one & right_zero)
        | (left_two & right_two)
    )
    two = (
        (left_zero & right_two)
        | (left_two & right_zero)
        | (left_one & right_one)
    )
    return one, two


def trit_negate(vector: tuple[int, int]) -> tuple[int, int]:
    return vector[1], vector[0]


def pack_row(row: Sequence[int]) -> tuple[int, int]:
    one = 0
    two = 0
    for column, value in enumerate(row):
        if int(value) % MODULUS == 1:
            one |= 1 << column
        elif int(value) % MODULUS == 2:
            two |= 1 << column
    return one, two


def packed_rref(
    rows: Sequence[tuple[int, int]],
    columns: int,
) -> tuple[tuple[tuple[int, int], ...], tuple[int, ...]]:
    """Reduced row echelon form over F_3 using packed ternary vectors."""

    work = [row for row in rows if row != (0, 0)]
    mask = (1 << columns) - 1
    pivots = []
    pivot_row = 0
    for column in range(columns):
        bit = 1 << column
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if (work[row][0] | work[row][1]) & bit
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        if work[pivot_row][1] & bit:
            work[pivot_row] = trit_negate(work[pivot_row])
        pivot_vector = work[pivot_row]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            if work[row][0] & bit:
                work[row] = trit_add(
                    work[row], trit_negate(pivot_vector), mask
                )
            elif work[row][1] & bit:
                work[row] = trit_add(work[row], pivot_vector, mask)
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    result = tuple(work[:pivot_row])
    return result, tuple(pivots)


def unpack_value(vector: tuple[int, int], column: int) -> int:
    bit = 1 << column
    if vector[0] & bit:
        return 1
    if vector[1] & bit:
        return 2
    return 0


def packed_nullspace(
    rows: Sequence[tuple[int, int]],
    columns: int,
) -> tuple[tuple[int, ...], ...]:
    rref, pivots = packed_rref(rows, columns)
    pivot_set = set(pivots)
    result = []
    for free in range(columns):
        if free in pivot_set:
            continue
        vector = [0] * columns
        vector[free] = 1
        for row, pivot in zip(rref, pivots):
            vector[pivot] = -unpack_value(row, free) % MODULUS
        result.append(tuple(vector))
    return tuple(result)


def pack_matrices(
    matrices: Sequence[Sequence[Sequence[int]]],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    return tuple(
        tuple(pack_row(row) for row in matrix) for matrix in matrices
    )


def packed_linear_combination_rows(
    coefficients: Sequence[int],
    matrices: Sequence[Sequence[tuple[int, int]]],
    columns: int,
) -> tuple[tuple[int, int], ...]:
    mask = (1 << columns) - 1
    result = []
    for row in range(columns):
        total = (0, 0)
        for coefficient, matrix in zip(coefficients, matrices):
            if int(coefficient) % MODULUS == 1:
                total = trit_add(total, matrix[row], mask)
            elif int(coefficient) % MODULUS == 2:
                total = trit_add(
                    total, trit_negate(matrix[row]), mask
                )
        result.append(total)
    return tuple(result)


def audit_profile(index: int, normal_spaces) -> dict[str, object]:
    candidate = second.CANDIDATES[index]
    label, _, _, identifiers_a, identifiers_b = candidate
    profiles = second.profiles_from_ids(identifiers_a, identifiers_b)
    first_equations = second.first_digit_equations(profiles)
    first_origin, first_basis = second.affine_parameterization(
        first_equations, 54
    )
    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles),
        first_origin,
        first_basis,
    )
    structured = pencil.structured_forms(constants, linears, polars)
    structured_linears = tuple(form[1] for form in structured)
    structured_polars = tuple(form[2] for form in structured)
    margin_rows, base_sums = base.derive_margin_digit_system(
        profiles, first_origin, first_basis
    )
    margin_kernel = second.nullspace_basis(margin_rows)
    row_polars = tuple(
        base.restrict_polar(polar, margin_kernel)
        for polar in structured_polars
    )
    packed_polars = pack_matrices(row_polars)

    # Only a radical of dimension at least four can support a four-form
    # retraction, so discard the generic spaces immediately.
    radical_histogram: Counter[int] = Counter()
    candidates = []
    for normal_basis in normal_spaces:
        coefficient_basis = second.nullspace_basis(normal_basis)
        if len(coefficient_basis) != 4:
            raise AssertionError("a normal two-space lost codimension four")
        packed_rows = []
        for coefficients in coefficient_basis:
            packed_rows.extend(
                packed_linear_combination_rows(
                    coefficients, packed_polars, 30
                )
            )
        radical = packed_nullspace(packed_rows, 30)
        radical_histogram[len(radical)] += 1
        if len(radical) >= 4:
            candidates.append(
                (normal_basis, coefficient_basis, radical)
            )

    catalog = catalog_phase_sum_intersection(identifiers_a, identifiers_b)
    target_records = []
    good_frequency: Counter[
        tuple[tuple[int, ...], tuple[int, ...]]
    ] = Counter()
    good_count_histogram: Counter[int] = Counter()
    coordinate_three_count_histogram: Counter[int] = Counter()
    for target_index, (target, multiplicity) in enumerate(
        catalog["phase_sum_corpus"]
    ):
        constants = base.target_constants(base_sums, target)
        target_origin = canonical_solution(
            tuple(
                tuple(margin_rows[row])
                + ((-constants[row]) % MODULUS,)
                for row in range(6)
            ),
            36,
        )
        if target_origin is None:
            raise AssertionError("a compatible target became inconsistent")
        row_linears = tuple(
            base.shifted_restricted_linear(
                linear, polar, target_origin, margin_kernel
            )
            for linear, polar in zip(
                structured_linears, structured_polars
            )
        )
        good = []
        for normal_basis, coefficient_basis, radical in candidates:
            combined_linears = tuple(
                pencil.combine_vectors(coefficients, row_linears)
                for coefficients in coefficient_basis
            )
            if base.rank_on_radical(combined_linears, radical) == 4:
                good.append(normal_basis)
                good_frequency[normal_basis] += 1
        good_count_histogram[len(good)] += 1
        coordinate_three = 0
        for subset in combinations(range(6), 3):
            radical = second.nullspace_basis(
                tuple(
                    row
                    for form in subset
                    for row in row_polars[form]
                ),
                columns=30,
            )
            if base.rank_on_radical(
                tuple(row_linears[form] for form in subset), radical
            ) == 3:
                coordinate_three += 1
        coordinate_three_count_histogram[coordinate_three] += 1
        target_records.append({
            "target_index": target_index,
            "raw_assignment_multiplicity": int(multiplicity),
            "four_form_retraction_count": len(good),
            "four_form_normal_spaces": tuple(good),
            "coordinate_three_retraction_count": coordinate_three,
        })

    return {
        "candidate_index": index,
        "label": label,
        "normal_four_spaces_tested": len(normal_spaces),
        "radical_dimension_histogram": tuple(
            sorted(radical_histogram.items())
        ),
        "radical_dimension_at_least_four": len(candidates),
        "target_count": len(target_records),
        "four_form_retraction_count_histogram": tuple(
            sorted(good_count_histogram.items())
        ),
        "four_form_normal_space_frequency": tuple(
            sorted(good_frequency.items())
        ),
        "coordinate_three_retraction_count_histogram": tuple(
            sorted(coordinate_three_count_histogram.items())
        ),
        "maximum_retraction_dimension": (
            4 if good_frequency else 3
            if any(coordinate_three_count_histogram)
            and any(
                count
                for coordinate_count, count
                in coordinate_three_count_histogram.items()
                if coordinate_count
            )
            else 2
        ),
        "targets": tuple(target_records),
    }


def verify() -> dict[str, object]:
    normal_spaces = canonical_two_spaces()
    profiles = tuple(
        audit_profile(index, normal_spaces)
        for index in range(len(second.CANDIDATES))
    )
    core = {
        "schema": "lp333-shell-two-row-margin-four-space-audit-v1",
        "scope": (
            "Complete four-subspace retraction audit after the exact "
            "rank-six row-margin digit; no LP(333), Legendre pair, or "
            "H(668) claim."
        ),
        "normal_two_spaces": len(normal_spaces),
        "four_spaces": len(normal_spaces),
        "profiles": profiles,
    }
    semantic_hash = base.compact_hash(core)
    if semantic_hash != EXPECTED_SEMANTIC_SHA256:
        raise AssertionError("the complete four-space audit changed")
    return {**core, "semantic_sha256": semantic_hash}


def main() -> None:
    result = verify()
    summary = {
        "schema": result["schema"],
        "normal_two_spaces": result["normal_two_spaces"],
        "profiles": tuple({
            "label": profile["label"],
            "radical_dimension_histogram": (
                profile["radical_dimension_histogram"]
            ),
            "radical_dimension_at_least_four": (
                profile["radical_dimension_at_least_four"]
            ),
            "target_count": profile["target_count"],
            "four_form_retraction_count_histogram": (
                profile["four_form_retraction_count_histogram"]
            ),
            "four_form_normal_space_frequency": (
                profile["four_form_normal_space_frequency"]
            ),
            "coordinate_three_retraction_count_histogram": (
                profile["coordinate_three_retraction_count_histogram"]
            ),
            "maximum_retraction_dimension": (
                profile["maximum_retraction_dimension"]
            ),
        } for profile in result["profiles"]),
        "semantic_sha256": result["semantic_sha256"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
