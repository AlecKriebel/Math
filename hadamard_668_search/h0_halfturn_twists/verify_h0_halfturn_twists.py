#!/usr/bin/env python3
"""Exact half-turn algebra and global fiber-twist census for the h=0 profile.

The pinned exact profile repeats after six cyclotomic classes.  On its
54 placement trits, the class half-turn therefore acts linearly.  This
verifier:

* splits the first placement affine space into its +1 and -1 eigenspaces;
* derives the equivariant shape of the second placement digit;
* counts the six anti-output equations exactly; and
* exhausts all 36 ways to pair opposite classes by one global permutation
  of the three quotient positions in each channel.

This is a fixed-profile placement theorem, not an LP(333) or H(668).
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product
from pathlib import Path
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
PHASE_ROOT = SEARCH_ROOT / "phase_second_digit"
sys.path.insert(0, str(PHASE_ROOT))
sys.path.insert(0, str(SEARCH_ROOT))

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
    quotient_support,
)


TARGET = (2, -2, -4, -2)
PROFILE_IDS_A = (1, 1, 2, 4, 4, 5, 1, 1, 2, 4, 4, 5)
PROFILE_IDS_B = (5, 5, 1, 7, 4, 1, 5, 5, 1, 7, 4, 1)
FIBER_PERMUTATIONS = tuple(permutations(range(3)))
ACTIVE_SECOND_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))


def permutation_affine_action(
    count: int,
    permutation: Sequence[int],
) -> tuple[int, int]:
    """Return ``u -> slope*u+offset`` for one profile count."""

    if count not in (1, 2):
        raise ValueError("only active profile counts carry a trit")
    images = []
    for trit in range(3):
        old_support = set(quotient_support(count, trit))
        new_support = tuple(
            quotient
            for quotient in range(3)
            if int(permutation[quotient]) in old_support
        )
        images.append(
            next(
                candidate
                for candidate in range(3)
                if quotient_support(count, candidate) == new_support
            )
        )
    offset = images[0]
    slope = (images[1] - offset) % 3
    if images[2] != (offset + 2 * slope) % 3:
        raise AssertionError("an S3 action on a trit was not affine")
    return slope, offset


def paired_affine_system(
    permutation_a: Sequence[int],
    permutation_b: Sequence[int],
) -> tuple[
    tuple[tuple[tuple[int, int, int], ...], ...],
    tuple[tuple[int, ...], ...],
    tuple[int, ...] | None,
    tuple[tuple[int, ...], ...] | None,
]:
    """Add one global quotient-position pairing in each channel."""

    profiles = profiles_from_ids(PROFILE_IDS_A, PROFILE_IDS_B)
    coordinates = active_trit_coordinates(profiles)
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    rows = list(augmented_system(first_digit_equations(profiles)))
    for channel, permutation in enumerate((permutation_a, permutation_b)):
        for class_index in range(6):
            opposite = class_index + 6
            if profiles[channel][class_index] != profiles[channel][opposite]:
                raise AssertionError("the h=0 profile lost its half-turn")
            for residue, count in enumerate(profiles[channel][class_index]):
                if count not in (1, 2):
                    continue
                slope, offset = permutation_affine_action(
                    count, permutation
                )
                row = [0] * 55
                row[
                    coordinate_index[(channel, opposite, residue)]
                ] = 1
                row[
                    coordinate_index[(channel, class_index, residue)]
                ] = -slope % 3
                row[-1] = offset
                rows.append(tuple(row))
    normalized_rows = tuple(rows)
    origin = canonical_solution(normalized_rows, 54)
    if origin is None:
        return profiles, normalized_rows, None, None
    basis = second.nullspace_basis(
        tuple(row[:-1] for row in normalized_rows),
        columns=54,
    )
    return profiles, normalized_rows, origin, basis


def reduced_quadratic(
    constant: int,
    linear: Sequence[int],
    polar: Sequence[Sequence[int]],
) -> tuple[int, tuple[tuple[int, int, int], ...]]:
    """Convert the audited polar convention to ordinary monomials."""

    variables = len(linear)
    terms = [
        (index, -1, int(linear[index]) % 3)
        for index in range(variables)
        if int(linear[index]) % 3
    ]
    # q=c+l.x+(1/2)x^T Bx.  In F3 this gives 2*B_ii*x_i^2
    # on the diagonal and B_ij*x_i*x_j off the diagonal.
    terms.extend(
        (index, index, 2 * int(polar[index][index]) % 3)
        for index in range(variables)
        if int(polar[index][index]) % 3
    )
    terms.extend(
        (left, right, int(polar[left][right]) % 3)
        for left in range(variables)
        for right in range(left + 1, variables)
        if int(polar[left][right]) % 3
    )
    return int(constant) % 3, tuple(terms)


def evaluate_reduced_quadratic(
    polynomial: tuple[int, Sequence[tuple[int, int, int]]],
    point: Sequence[int],
) -> int:
    value = int(polynomial[0])
    for left, right, coefficient in polynomial[1]:
        if right < 0:
            value += coefficient * int(point[left])
        else:
            value += coefficient * int(point[left]) * int(point[right])
    return value % 3


def exhaust_dimension_nine_second_digit(
    profiles: Sequence[Sequence[Sequence[int]]],
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
) -> int:
    """Count every full second-digit solution in one 3^9 family."""

    if len(basis) != 9:
        raise ValueError("this exhaustive kernel is specific to dimension nine")
    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles),
        origin,
        basis,
    )
    polynomials = tuple(
        reduced_quadratic(
            constants[equation],
            linears[equation],
            polars[equation],
        )
        for equation in ACTIVE_SECOND_ROWS
    )

    # Cross-check the compact evaluator against the general audited one.
    fixtures = (
        (0,) * 9,
        tuple(index % 3 for index in range(9)),
        tuple((index * index + 2 * index + 1) % 3 for index in range(9)),
    )
    for point in fixtures:
        expected = second.evaluate_interpolation(
            constants, linears, polars, point
        )
        actual = tuple(
            evaluate_reduced_quadratic(polynomial, point)
            for polynomial in polynomials
        )
        if actual != tuple(expected[index] for index in ACTIVE_SECOND_ROWS):
            raise AssertionError("the reduced quadratic evaluator changed")

    survivors = 0
    for point in product(range(3), repeat=9):
        if all(
            evaluate_reduced_quadratic(polynomial, point) == 0
            for polynomial in polynomials
        ):
            placement = second.lift_affine_point(origin, basis, point)
            direct = second.symbolic_second_digits(
                second.second_digit_term_data(profiles),
                placement,
            )
            if direct != (0,) * 20:
                raise AssertionError("a reduced survivor failed direct replay")
            survivors += 1
    return survivors


def classify_global_fiber_twists() -> dict[str, object]:
    records = []
    dimension_histogram: Counter[str] = Counter()
    enumerated_points = 0
    for index_a, permutation_a in enumerate(FIBER_PERMUTATIONS):
        for index_b, permutation_b in enumerate(FIBER_PERMUTATIONS):
            profiles, rows, origin, basis = paired_affine_system(
                permutation_a,
                permutation_b,
            )
            coefficient_rank = matrix_rank(
                tuple(row[:-1] for row in rows)
            )
            augmented_rank = matrix_rank(rows)
            if origin is None:
                if augmented_rank != coefficient_rank + 1:
                    raise AssertionError("an inconsistent family lost rank one")
                dimension = None
                second_digit_survivors = None
                dimension_histogram["inconsistent"] += 1
            else:
                if augmented_rank != coefficient_rank or basis is None:
                    raise AssertionError("a consistent family lost its basis")
                dimension = len(basis)
                dimension_histogram[str(dimension)] += 1
                if dimension == 9:
                    second_digit_survivors = (
                        exhaust_dimension_nine_second_digit(
                            profiles, origin, basis
                        )
                    )
                    enumerated_points += 3**9
                    if second_digit_survivors:
                        raise AssertionError(
                            "a nonidentity global twist survived digit two"
                        )
                elif dimension == 21:
                    second_digit_survivors = None
                    if (
                        index_a,
                        index_b,
                    ) != (0, 0):
                        raise AssertionError(
                            "a nonidentity family retained dimension 21"
                        )
                else:
                    raise AssertionError(
                        f"unexpected twist dimension {dimension}"
                    )
            records.append({
                "permutation_indices": (index_a, index_b),
                "permutation_a": tuple(permutation_a),
                "permutation_b": tuple(permutation_b),
                "coefficient_rank": coefficient_rank,
                "augmented_rank": augmented_rank,
                "dimension": dimension,
                "second_digit_survivors": second_digit_survivors,
            })
    expected_histogram = {"inconsistent": 17, "9": 18, "21": 1}
    if dict(dimension_histogram) != expected_histogram:
        raise AssertionError(
            f"twist histogram changed: {dict(dimension_histogram)}"
        )
    if enumerated_points != 18 * 3**9:
        raise AssertionError("the dimension-nine census lost a family")
    return {
        "families": len(records),
        "dimension_histogram": expected_histogram,
        "dimension_nine_families": 18,
        "points_exhausted_per_dimension_nine_family": 3**9,
        "points_exhausted_total": enumerated_points,
        "dimension_nine_second_digit_survivors": 0,
        "records": tuple(records),
    }


def combine_quadratics(
    constants: Sequence[int],
    linears: Sequence[Sequence[int]],
    polars: Sequence[Sequence[Sequence[int]]],
    indices: Sequence[int],
    coefficients: Sequence[int],
) -> tuple[int, tuple[int, ...], tuple[tuple[int, ...], ...]]:
    variables = len(linears[0])
    constant = sum(
        int(coefficient) * int(constants[index])
        for coefficient, index in zip(coefficients, indices)
    ) % 3
    linear = tuple(
        sum(
            int(coefficient) * int(linears[index][column])
            for coefficient, index in zip(coefficients, indices)
        )
        % 3
        for column in range(variables)
    )
    polar = tuple(
        tuple(
            sum(
                int(coefficient) * int(polars[index][row][column])
                for coefficient, index in zip(coefficients, indices)
            )
            % 3
            for column in range(variables)
        )
        for row in range(variables)
    )
    return constant, linear, polar


def halfturn_decomposition() -> dict[str, object]:
    profiles = profiles_from_ids(PROFILE_IDS_A, PROFILE_IDS_B)
    coordinates = active_trit_coordinates(profiles)
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    halfturn = tuple(
        coordinate_index[(channel, (class_index + 6) % 12, residue)]
        for channel, class_index, residue in coordinates
    )
    if any(halfturn[halfturn[index]] != index for index in range(54)):
        raise AssertionError("the profile half-turn is not an involution")

    first_rows = augmented_system(first_digit_equations(profiles))
    coefficient_rows = tuple(row[:-1] for row in first_rows)
    fixed_rows = tuple(
        tuple(
            (
                1
                if column == index
                else -1
                if column == halfturn[index]
                else 0
            )
            % 3
            for column in range(54)
        )
        for index in range(54)
    )
    anti_rows = tuple(
        tuple(
            (
                1
                if column == index
                else 1
                if column == halfturn[index]
                else 0
            )
            % 3
            for column in range(54)
        )
        for index in range(54)
    )
    fixed_basis = second.nullspace_basis(
        coefficient_rows + fixed_rows,
        columns=54,
    )
    anti_basis = second.nullspace_basis(
        coefficient_rows + anti_rows,
        columns=54,
    )
    if (len(fixed_basis), len(anti_basis)) != (21, 15):
        raise AssertionError("the half-turn eigenspace dimensions changed")
    eigenbasis = fixed_basis + anti_basis
    if matrix_rank(eigenbasis) != 36:
        raise AssertionError("the two eigenspaces do not span the first lift")

    origin = canonical_solution(first_rows, 54)
    if origin is None:
        raise AssertionError("the first placement digit became inconsistent")
    fixed_origin = tuple(
        2 * (int(origin[index]) + int(origin[halfturn[index]])) % 3
        for index in range(54)
    )
    if any(
        (
            sum(row[index] * fixed_origin[index] for index in range(54))
            - row[-1]
        )
        % 3
        for row in first_rows
    ):
        raise AssertionError("the symmetrized origin left the affine space")

    term_data = second.second_digit_term_data(profiles)
    constants, linears, polars = second.derive_quadratics(
        term_data,
        fixed_origin,
        eigenbasis,
    )

    # The output action fixes the first eight rows and swaps the final
    # two blocks of six.
    for fixture in range(6):
        point = tuple(
            (fixture * (index + 1) + index * index + 2 * index) % 3
            for index in range(36)
        )
        placement = second.lift_affine_point(
            fixed_origin, eigenbasis, point
        )
        transformed = tuple(
            placement[halfturn[index]] for index in range(54)
        )
        value = second.symbolic_second_digits(term_data, placement)
        transformed_value = second.symbolic_second_digits(
            term_data, transformed
        )
        expected = value[:8] + value[14:20] + value[8:14]
        if transformed_value != expected:
            raise AssertionError("the second-digit output action changed")

    plus_forms = [
        combine_quadratics(
            constants, linears, polars, (index,), (1,)
        )
        for index in range(8)
    ]
    plus_forms.extend(
        combine_quadratics(
            constants,
            linears,
            polars,
            (8 + index, 14 + index),
            (1, 1),
        )
        for index in range(6)
    )
    minus_forms = tuple(
        combine_quadratics(
            constants,
            linears,
            polars,
            (8 + index, 14 + index),
            (1, 2),
        )
        for index in range(6)
    )

    active_plus = 0
    for constant, linear, polar in plus_forms:
        plus_plus = any(
            polar[left][right]
            for left in range(21)
            for right in range(21)
        )
        minus_minus = any(
            polar[left][right]
            for left in range(21, 36)
            for right in range(21, 36)
        )
        cross = any(
            polar[left][right]
            for left in range(21)
            for right in range(21, 36)
        )
        if cross or any(linear[21:]):
            raise AssertionError("a plus equation mixed the eigenspaces")
        if constant or any(linear) or plus_plus or minus_minus:
            active_plus += 1
    if active_plus != 12:
        raise AssertionError("the plus output should have 12 active rows")

    bilinear_blocks = []
    minus_linears = []
    for constant, linear, polar in minus_forms:
        if (
            constant
            or any(linear[:21])
            or any(
                polar[left][right]
                for left in range(21)
                for right in range(21)
            )
            or any(
                polar[left][right]
                for left in range(21, 36)
                for right in range(21, 36)
            )
        ):
            raise AssertionError("a minus equation was not odd bilinear")
        block = tuple(
            tuple(polar[left][21 + right] for right in range(15))
            for left in range(21)
        )
        if matrix_rank(block) != 15:
            raise AssertionError("an anti-output bilinear block lost rank")
        bilinear_blocks.append(block)
        minus_linears.append(tuple(linear[21:]))

    projective_rank_histogram: Counter[int] = Counter()
    exceptional = []
    exceptional_kernels: list[tuple[tuple[int, ...], ...]] = []
    for coefficients in product(range(3), repeat=6):
        if not any(coefficients):
            continue
        if next(value for value in coefficients if value) != 1:
            continue
        combination = tuple(
            tuple(
                sum(
                    coefficients[index]
                    * bilinear_blocks[index][row][column]
                    for index in range(6)
                )
                % 3
                for column in range(15)
            )
            for row in range(21)
        )
        rank = matrix_rank(combination)
        projective_rank_histogram[rank] += 1
        if rank < 15:
            kernel = second.nullspace_basis(combination, columns=15)
            exceptional.append((tuple(coefficients), rank, len(kernel)))
            exceptional_kernels.append(kernel)
    expected_projective_histogram = {11: 1, 12: 1, 14: 1, 15: 361}
    if dict(sorted(projective_rank_histogram.items())) != (
        expected_projective_histogram
    ):
        raise AssertionError("the anti-pencil rank histogram changed")

    special_y = {(0,) * 15}
    for kernel in exceptional_kernels:
        special_y.update(
            tuple(
                sum(
                    coordinate * kernel[index][column]
                    for index, coordinate in enumerate(point)
                )
                % 3
                for column in range(15)
            )
            for point in product(range(3), repeat=len(kernel))
        )
    if len(special_y) != 109:
        raise AssertionError("the exceptional anti-direction union changed")

    special_histogram: Counter[tuple[int, int, bool]] = Counter()
    special_solutions = 0
    for y in special_y:
        coefficient_matrix = tuple(
            tuple(
                sum(
                    bilinear_blocks[equation][column][right] * y[right]
                    for right in range(15)
                )
                % 3
                for column in range(21)
            )
            for equation in range(6)
        )
        rhs = tuple(
            -sum(
                minus_linears[equation][right] * y[right]
                for right in range(15)
            )
            % 3
            for equation in range(6)
        )
        coefficient_rank = matrix_rank(coefficient_matrix)
        augmented_rank = matrix_rank(
            tuple(
                coefficient_matrix[equation] + (rhs[equation],)
                for equation in range(6)
            )
        )
        consistent = coefficient_rank == augmented_rank
        special_histogram[
            (coefficient_rank, augmented_rank, consistent)
        ] += 1
        if consistent:
            special_solutions += 3 ** (21 - coefficient_rank)

    expected_special_histogram = {
        (0, 0, True): 1,
        (5, 5, True): 34,
        (5, 6, False): 74,
    }
    if dict(special_histogram) != expected_special_histogram:
        raise AssertionError("the exceptional anti-fiber census changed")
    ordinary_y = 3**15 - len(special_y)
    anti_zero_count = ordinary_y * 3**15 + special_solutions
    if anti_zero_count != 205_901_492_005_503:
        raise AssertionError("the anti-output zero count changed")

    return {
        "first_affine_dimension": 36,
        "fixed_eigenspace_dimension": len(fixed_basis),
        "anti_eigenspace_dimension": len(anti_basis),
        "active_plus_quadrics": active_plus,
        "anti_bilinear_equations": len(minus_forms),
        "anti_block_ranks": tuple(
            matrix_rank(block) for block in bilinear_blocks
        ),
        "anti_pencil_projective_rank_histogram": (
            expected_projective_histogram
        ),
        "anti_pencil_exceptions": tuple(exceptional),
        "exceptional_anti_directions": len(special_y),
        "exceptional_fiber_histogram": expected_special_histogram,
        "anti_equation_zero_count": anti_zero_count,
    }


def main() -> None:
    decomposition = halfturn_decomposition()
    twists = classify_global_fiber_twists()
    print(f"target={TARGET}")
    print(f"profile_ids_a={PROFILE_IDS_A}")
    print(f"profile_ids_b={PROFILE_IDS_B}")
    print(
        "first_eigenspaces="
        f"{decomposition['fixed_eigenspace_dimension']}+"
        f"{decomposition['anti_eigenspace_dimension']}"
    )
    print(
        "second_digit_split="
        f"{decomposition['active_plus_quadrics']} plus quadrics + "
        f"{decomposition['anti_bilinear_equations']} anti bilinear rows"
    )
    print(
        "anti_pencil_projective_rank_histogram="
        f"{decomposition['anti_pencil_projective_rank_histogram']}"
    )
    print(
        "anti_equation_zero_count="
        f"{decomposition['anti_equation_zero_count']}"
    )
    print(f"global_fiber_twists={twists['families']}")
    print(f"twist_dimension_histogram={twists['dimension_histogram']}")
    print(
        "dimension_nine_points_exhausted="
        f"{twists['points_exhausted_total']}"
    )
    print(
        "dimension_nine_second_digit_survivors="
        f"{twists['dimension_nine_second_digit_survivors']}"
    )
    print("PASS: h=0 half-turn decomposition and global twist census")
    print("STATUS: fixed-profile theorem only; no LP(333) or H(668)")


if __name__ == "__main__":
    main()
