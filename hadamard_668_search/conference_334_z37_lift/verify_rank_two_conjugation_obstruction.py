#!/usr/bin/env python3
"""Exclude every constant symmetric rank-two formal conjugator.

This is a companion verifier for the trace-corrected family

    exp(-zA) (N0 + eta*z^18*J + 19*y^36*J) exp(zA)

over F_37[y]/(y^37).  It proves an obstruction only within this
constant-generator family; it does not exclude general C37 lifts.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from math import comb
from typing import Iterable, Sequence


P = 37
DEGREES = [18, 20, 18, 20, 18, 20, 18, 20, 10]
ZERO = [0] * P
ONE = [1] + [0] * (P - 1)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def polynomial_add(
    left: Sequence[int], right: Sequence[int]
) -> list[int]:
    return [(a + b) % P for a, b in zip(left, right)]


def polynomial_scale(poly: Sequence[int], scalar: int) -> list[int]:
    return [scalar * value % P for value in poly]


def polynomial_multiply(
    left: Sequence[int], right: Sequence[int]
) -> list[int]:
    result = [0] * P
    for i, first in enumerate(left):
        if not first:
            continue
        for j, second in enumerate(right[: P - i]):
            result[i + j] = (result[i + j] + first * second) % P
    return result


def polynomial_power(poly: Sequence[int], exponent: int) -> list[int]:
    result = ONE[:]
    for _ in range(exponent):
        result = polynomial_multiply(result, poly)
    return result


LOGARITHM = [0] * P
for degree in range(1, P):
    LOGARITHM[degree] = (
        (1 if degree % 2 else -1) * pow(degree, -1, P)
    ) % P
HALF_POWER = polynomial_power(LOGARITHM, 18)


def y_to_x_coefficients(poly: Sequence[int]) -> list[int]:
    """Convert from y=x-1 to the cyclic basis 1,x,...,x^36."""

    result = [0] * P
    for degree in range(P - 1, -1, -1):
        result[degree] = (
            poly[degree]
            - sum(
                result[index] * comb(index, degree)
                for index in range(degree + 1, P)
            )
        ) % P
    return result


def numeric_matrix_multiply(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]
) -> list[list[int]]:
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(middle)) % P
            for j in range(columns)
        ]
        for i in range(rows)
    ]


def exponential_matrix(
    matrix: Sequence[Sequence[int]], sign: int
) -> list[list[list[int]]]:
    """Return exp(sign*z*matrix), with polynomial entries in the y basis."""

    order = len(matrix)
    result = [
        [[0] * P for _ in range(order)]
        for _ in range(order)
    ]
    matrix_power = [
        [int(i == j) for j in range(order)]
        for i in range(order)
    ]
    z_power = ONE[:]
    factorial = 1
    for i in range(order):
        result[i][i] = ONE[:]

    signed_matrix = [
        [sign * entry % P for entry in row]
        for row in matrix
    ]
    for degree in range(1, P):
        matrix_power = numeric_matrix_multiply(
            matrix_power, signed_matrix
        )
        z_power = polynomial_multiply(z_power, LOGARITHM)
        factorial = factorial * degree % P
        inverse_factorial = pow(factorial, -1, P)
        for i in range(order):
            for j in range(order):
                coefficient = (
                    matrix_power[i][j] * inverse_factorial
                ) % P
                if coefficient:
                    result[i][j] = polynomial_add(
                        result[i][j],
                        polynomial_scale(z_power, coefficient),
                    )
    return result


def reduced_row_basis(
    vectors: Iterable[Sequence[int]],
) -> tuple[list[list[int]], list[int]]:
    """Return an RREF row basis and its information coordinates."""

    basis: list[list[int]] = []
    pivots: list[int] = []
    for vector in vectors:
        work = [value % P for value in vector]
        for row, pivot in zip(basis, pivots):
            if work[pivot]:
                factor = work[pivot]
                work = [
                    (left - factor * right) % P
                    for left, right in zip(work, row)
                ]
        if not any(work):
            continue
        pivot = next(index for index, value in enumerate(work) if value)
        inverse = pow(work[pivot], -1, P)
        work = polynomial_scale(work, inverse)
        for index, row in enumerate(basis):
            if row[pivot]:
                factor = row[pivot]
                basis[index] = [
                    (left - factor * right) % P
                    for left, right in zip(row, work)
                ]
        insertion = sum(old_pivot < pivot for old_pivot in pivots)
        basis.insert(insertion, work)
        pivots.insert(insertion, pivot)

    require(
        all(
            basis[i][pivot] == int(i == j)
            for i in range(len(basis))
            for j, pivot in enumerate(pivots)
        ),
        "row basis is not reduced on its information coordinates",
    )
    return basis, pivots


def universal_diagonal_code(
    canonical_matrix: Sequence[Sequence[int]],
) -> tuple[list[list[int]], list[int]]:
    """Construct W(A)=V(A)+z^18 V(A) in cyclic coefficients.

    V(A) is the span of all products of an entry of exp(-zA) with an
    entry of exp(zA).  It contains every diagonal entry of
    exp(-zA) M exp(zA), for every constant matrix M.
    """

    negative = exponential_matrix(canonical_matrix, -1)
    positive = exponential_matrix(canonical_matrix, 1)
    negative_entries = [entry for row in negative for entry in row]
    positive_entries = [entry for row in positive for entry in row]

    generators: list[list[int]] = []
    for left in negative_entries:
        for right in positive_entries:
            value = polynomial_multiply(left, right)
            generators.append(y_to_x_coefficients(value))
            generators.append(
                y_to_x_coefficients(
                    polynomial_multiply(HALF_POWER, value)
                )
            )
    return reduced_row_basis(generators)


def compatible_binary_words(
    basis: Sequence[Sequence[int]], pivots: Sequence[int]
) -> list[tuple[int, ...]]:
    """Enumerate W intersect ({0} x {18,19}^36) exactly."""

    choices = [
        (0,) if pivot == 0 else (18, 19)
        for pivot in pivots
    ]
    require(
        2 ** sum(pivot != 0 for pivot in pivots) <= 8192,
        "unexpectedly large information-set enumeration",
    )

    result: list[tuple[int, ...]] = []
    for values in product(*choices):
        word = [0] * P
        for coefficient, row in zip(values, basis):
            if coefficient:
                word = [
                    (left + coefficient * right) % P
                    for left, right in zip(word, row)
                ]
        if (
            word[0] == 0
            and all(value in (18, 19) for value in word[1:])
        ):
            result.append(
                tuple(value - 18 for value in word[1:])
            )
    return result


def quadratic_character(value: int) -> int:
    value %= P
    if value == 0:
        return 0
    return 1 if pow(value, 18, P) == 1 else -1


def verify_split_semisimple_types() -> dict[str, object]:
    """Exclude the split diagonalizable rank-two types pointwise."""

    surviving_distinct: dict[int, list[tuple[int, int, int]]] = {}
    minimum_nonexceptional_lags = P
    for ratio in range(2, P):
        exceptional = {
            0,
            1,
            -1 % P,
            ratio,
            -ratio % P,
            (ratio - 1) % P,
            (1 - ratio) % P,
        }
        tested_lags = [
            value for value in range(P)
            if value not in exceptional
        ]
        minimum_nonexceptional_lags = min(
            minimum_nonexceptional_lags, len(tested_lags)
        )
        survivors: list[tuple[int, int, int]] = []
        for first in range(P):
            for second in range(P):
                third = (1 - first - second) % P
                diagonal = (
                    first * first
                    + second * second
                    + third * third
                ) % P
                pair01 = first * second % P
                pair02 = first * third % P
                pair12 = second * third % P
                feasible = True
                for lag in tested_lags:
                    value = (
                        quadratic_character(lag) * diagonal
                        + (
                            quadratic_character(lag - 1)
                            + quadratic_character(lag + 1)
                        )
                        * pair01
                        + (
                            quadratic_character(lag - ratio)
                            + quadratic_character(lag + ratio)
                        )
                        * pair02
                        + (
                            quadratic_character(lag - (ratio - 1))
                            + quadratic_character(lag + (ratio - 1))
                        )
                        * pair12
                    ) % P
                    if value not in (3, P - 3):
                        feasible = False
                        break
                if feasible:
                    survivors.append((first, second, third))
        if survivors:
            surviving_distinct[ratio] = survivors

    repeated_survivors: list[tuple[int, int]] = []
    for first in range(P):
        second = (1 - first) % P
        diagonal = (first * first + second * second) % P
        pair = first * second % P
        if all(
            (
                quadratic_character(lag) * diagonal
                + (
                    quadratic_character(lag - 1)
                    + quadratic_character(lag + 1)
                )
                * pair
            )
            % P
            in (3, P - 3)
            for lag in range(P)
            if lag not in (0, 1, P - 1)
        ):
            repeated_survivors.append((first, second))

    require(
        not surviving_distinct,
        "a distinct split semisimple local profile survived",
    )
    require(
        not repeated_survivors,
        "a repeated split semisimple local profile survived",
    )
    return {
        "distinct_projective_ratios_checked": P - 2,
        "coordinate_triples_checked_per_ratio": P * P,
        "minimum_nonexceptional_lags_per_ratio": (
            minimum_nonexceptional_lags
        ),
        "distinct_type_survivors": 0,
        "repeated_type_coordinate_pairs_checked": P,
        "repeated_type_survivors": 0,
    }


def companion_matrix(trace: int, determinant: int) -> list[list[int]]:
    """Return 0 direct-summed with X^2-trace*X+determinant."""

    return [
        [0, 0, 0],
        [0, 0, -determinant % P],
        [0, 1, trace % P],
    ]


def code_record(
    name: str, matrix: Sequence[Sequence[int]]
) -> dict[str, object]:
    basis, pivots = universal_diagonal_code(matrix)
    words = compatible_binary_words(basis, pivots)
    weights = Counter(sum(word) for word in words)
    residue_word = tuple(
        int(quadratic_character(value) == 1)
        for value in range(1, P)
    )
    paley_pair = {residue_word, tuple(1 - bit for bit in residue_word)}
    return {
        "name": name,
        "dimension": len(basis),
        "information_coordinates": pivots,
        "compatible_word_count": len(words),
        "weight_distribution": dict(sorted(weights.items())),
        "paley_pair_only": set(words) == paley_pair,
    }


def verify_remaining_rational_types() -> dict[str, object]:
    """Enumerate the universal-code intersection for every other type."""

    trace_zero_determinant = next(
        value for value in range(1, P)
        if quadratic_character(value) == -1
    )
    require(
        trace_zero_determinant == 2,
        "trace-zero irreducible representative changed",
    )
    normalized_irreducible_determinants = [
        value
        for value in range(1, P)
        if quadratic_character(1 - 4 * value) == -1
    ]
    require(
        normalized_irreducible_determinants
        == [4, 5, 6, 8, 9, 10, 11, 13, 14,
            15, 20, 22, 23, 26, 30, 33, 34, 36],
        "trace-one irreducible projective classes changed",
    )

    irreducible_records = [
        code_record(
            "irreducible_trace_zero",
            companion_matrix(0, trace_zero_determinant),
        )
    ] + [
        code_record(
            f"irreducible_trace_one_det_{determinant}",
            companion_matrix(1, determinant),
        )
        for determinant in normalized_irreducible_determinants
    ]
    require(
        all(
            record["compatible_word_count"] == 2
            and record["weight_distribution"] == {18: 2}
            and record["paley_pair_only"]
            for record in irreducible_records
        ),
        "an irreducible quadratic class gained a non-Paley weight",
    )

    nonzero_jordan = code_record(
        "nonzero_J2",
        [
            [0, 0, 0],
            [0, 1, 1],
            [0, 0, 1],
        ],
    )
    mixed_zero_jordan = code_record(
        "nonzero_eigenline_plus_J2_zero",
        [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
        ],
    )
    expected_jordan_weights = {16: 1, 17: 6, 18: 10, 19: 6, 20: 1}
    for record in (nonzero_jordan, mixed_zero_jordan):
        require(
            record["dimension"] == 14
            and record["compatible_word_count"] == 24
            and record["weight_distribution"] == expected_jordan_weights,
            f"the universal intersection changed for {record['name']}",
        )

    nilpotent_j3 = code_record(
        "J3_zero",
        [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
        ],
    )
    nilpotent_j2_j2 = code_record(
        "J2_zero_plus_J2_zero",
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
        ],
    )
    for record, expected_dimension in (
        (nilpotent_j3, 10),
        (nilpotent_j2_j2, 6),
    ):
        require(
            record["dimension"] == expected_dimension
            and record["compatible_word_count"] == 2
            and record["weight_distribution"] == {18: 2}
            and bool(record["paley_pair_only"]),
            f"the nilpotent universal intersection changed for "
            f"{record['name']}",
        )

    all_records = (
        irreducible_records
        + [
            nonzero_jordan,
            mixed_zero_jordan,
            nilpotent_j3,
            nilpotent_j2_j2,
        ]
    )
    require(10 in DEGREES, "the quotient lost its degree-10 diagonal block")
    require(
        all(
            10 not in record["weight_distribution"]
            for record in all_records
        ),
        "a remaining rank-two type now permits diagonal degree 10",
    )
    return {
        "quotient_diagonal_degrees": DEGREES,
        "irreducible_projective_class_count": len(irreducible_records),
        "irreducible_records": irreducible_records,
        "nonzero_jordan_record": nonzero_jordan,
        "mixed_zero_jordan_record": mixed_zero_jordan,
        "nilpotent_records": [nilpotent_j3, nilpotent_j2_j2],
        "degree_ten_permitted_by_any_type": False,
    }


def verify_rank_two_conjugation_obstruction() -> dict[str, object]:
    """Return a compact certificate after replaying every exact check."""

    require(
        y_to_x_coefficients(HALF_POWER)
        == [0]
        + [
            6 if quadratic_character(value) == 1 else P - 6
            for value in range(1, P)
        ],
        "z^18 no longer has the quadratic-character coefficient law",
    )
    split = verify_split_semisimple_types()
    remaining = verify_remaining_rational_types()
    return {
        "status": "impossible",
        "family_scope": (
            "single constant symmetric rank-two generator in the "
            "trace-corrected exponential family"
        ),
        "split_semisimple": split,
        "irreducible_projective_classes_checked": (
            remaining["irreducible_projective_class_count"]
        ),
        "irreducible_and_pure_nilpotent_binary_intersection": (
            "exactly_the_QR_and_NQR_words_of_weight_18"
        ),
        "nonzero_jordan_compatible_weight_distribution": {
            "16": 1,
            "17": 6,
            "18": 10,
            "19": 6,
            "20": 1,
        },
        "required_diagonal_degrees": DEGREES,
        "required_degree_ten_permitted": False,
        "higher_y_conjugators": "open",
        "general_z37_block_lift": "open",
    }


def main() -> None:
    report = verify_rank_two_conjugation_obstruction()
    split = report["split_semisimple"]
    print(
        "split_distinct=IMPOSSIBLE "
        "split_repeated=IMPOSSIBLE "
        f"other_projective_types="
        f"{report['irreducible_projective_classes_checked'] + 4} "
        "degree10=IMPOSSIBLE "
        "rank_two_constant_A=IMPOSSIBLE"
    )
    print(
        f"ratios={split['distinct_projective_ratios_checked']} "
        f"local_triples_per_ratio="
        f"{split['coordinate_triples_checked_per_ratio']} "
        "max_information_enumeration=8192"
    )
    print("PASS")


if __name__ == "__main__":
    main()
