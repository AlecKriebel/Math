#!/usr/bin/env python3
"""Exclude the two rank-two Jordan types left by the diagonal over-code.

The earlier universal code W(A) forgot that the coefficient of the
trace-correcting z^18 J term is fixed to eta in {+1,-1}.  For each of the
two surviving Jordan types, symmetry puts every diagonal word in the same
small affine code eta*h+U.  This verifier computes its exact intersection
with the binary diagonal alphabet.

Scope: constant symmetric rank-two generators in the trace-corrected
formal exponential family over F_37[y]/(y^37).  This does not address
higher-y conjugators or arbitrary semiregular C37 lifts.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product
import json
from math import comb
from pathlib import Path
from typing import Iterable, Sequence


P = 37
ORDER = 9
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "RANK_TWO_JORDAN_OBSTRUCTION.json"

EXCEPTIONAL_T = [
    [-4, -11, -7, 1, 1, 3, 5, 5, 7],
    [-11, 0, 11, 1, 1, -5, 3, 3, -3],
    [-7, 11, -4, -3, -3, 5, -3, -3, 7],
    [1, 1, -3, 4, 1, 5, -9, 9, -9],
    [1, 1, -3, 1, 4, 5, 9, -9, -9],
    [3, -5, 5, 5, 5, 0, -9, -9, 5],
    [5, 3, -3, -9, 9, -9, 0, 3, 1],
    [5, 3, -3, 9, -9, -9, 3, 0, 1],
    [7, -3, 7, -9, -9, 5, 1, 1, 0],
]

ZERO = [0] * P
ONE = [1] + [0] * (P - 1)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def matrix_multiply(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]
) -> list[list[int]]:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def rank_mod(matrix: Sequence[Sequence[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [
            entry * inverse % prime for entry in work[rank]
        ]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % prime
                for left, right in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def verify_exceptional_quotient() -> dict[str, object]:
    """Validate the class-607 representative from the complete census."""

    matrix = EXCEPTIONAL_T
    require(
        all(matrix[i][j] == matrix[j][i] for i in range(ORDER)
            for j in range(ORDER)),
        "exceptional quotient is not symmetric",
    )
    require(
        all(sum(row) == 0 for row in matrix),
        "exceptional quotient does not annihilate one",
    )
    square = matrix_multiply(matrix, matrix)
    require(
        square
        == [
            [296 if i == j else -37 for j in range(ORDER)]
            for i in range(ORDER)
        ],
        "exceptional quotient has the wrong square",
    )
    require(
        all(matrix[i][i] % 2 == 0 for i in range(ORDER))
        and all(
            matrix[i][j] % 2
            for i in range(ORDER)
            for j in range(ORDER)
            if i != j
        ),
        "exceptional quotient has the wrong parity pattern",
    )

    diagonal_profile = sorted(matrix[i][i] for i in range(ORDER))
    diagonal_degrees = [
        (36 - matrix[i][i]) // 2 for i in range(ORDER)
    ]
    require(
        diagonal_profile == [-4, -4, 0, 0, 0, 0, 0, 4, 4],
        "exceptional diagonal profile changed",
    )
    require(
        sorted(diagonal_degrees)
        == [16, 16, 18, 18, 18, 18, 18, 20, 20],
        "exceptional diagonal degrees changed",
    )

    quotient = [
        [
            (37 - int(i == j) - matrix[i][j]) // 2
            for j in range(ORDER)
        ]
        for i in range(ORDER)
    ]
    require(
        all(sum(row) == 166 for row in quotient),
        "exceptional adjacency quotient is not 166-regular",
    )
    quotient_square_plus = matrix_multiply(quotient, quotient)
    for i in range(ORDER):
        for j in range(ORDER):
            quotient_square_plus[i][j] += quotient[i][j]
    require(
        quotient_square_plus
        == [
            [
                83 + 83 * 37 if i == j else 83 * 37
                for j in range(ORDER)
            ]
            for i in range(ORDER)
        ],
        "exceptional adjacency quotient fails B^2+B=83I+83*37J",
    )

    inverse_two = pow(2, -1, P)
    n0 = [
        [(-matrix[i][j] * inverse_two) % P for j in range(ORDER)]
        for i in range(ORDER)
    ]
    require(
        [
            [entry % P for entry in row]
            for row in matrix_multiply(n0, n0)
        ]
        == [[0] * ORDER for _ in range(ORDER)],
        "the exceptional N0 is not square-zero modulo 37",
    )
    require(
        all(sum(row) % P == 0 for row in n0),
        "the exceptional N0 does not annihilate J",
    )

    automorphisms = 0
    for permutation in permutations(range(ORDER)):
        if all(
            matrix[permutation[i]][permutation[j]] == matrix[i][j]
            for i in range(ORDER)
            for j in range(i, ORDER)
        ):
            automorphisms += 1
    require(
        automorphisms == 2,
        "exceptional quotient automorphism order changed",
    )
    require(
        all(
            matrix[[0, 1, 2, 4, 3, 5, 7, 6, 8][i]]
                  [[0, 1, 2, 4, 3, 5, 7, 6, 8][j]]
            == matrix[i][j]
            for i in range(ORDER)
            for j in range(ORDER)
        ),
        "the named exceptional quotient involution disappeared",
    )

    return {
        "source_census_permutation_class": 607,
        "paired_negative_permutation_class": 622,
        "representative": matrix,
        "diagonal_profile": diagonal_profile,
        "diagonal_degrees_in_representative_order": diagonal_degrees,
        "automorphism_order": automorphisms,
        "automorphism_generator_one_based": "(4 5)(7 8)",
        "rank_mod_3": rank_mod(matrix, 3),
        "rank_mod_37": rank_mod(matrix, 37),
        "maximum_absolute_entry": max(
            abs(entry) for row in matrix for entry in row
        ),
    }


def polynomial_add(
    left: Sequence[int], right: Sequence[int]
) -> list[int]:
    return [(first + second) % P for first, second in zip(left, right)]


def polynomial_subtract(
    left: Sequence[int], right: Sequence[int]
) -> list[int]:
    return [(first - second) % P for first, second in zip(left, right)]


def polynomial_scale(
    polynomial: Sequence[int], scalar: int
) -> list[int]:
    return [scalar * value % P for value in polynomial]


def polynomial_multiply(
    left: Sequence[int], right: Sequence[int]
) -> list[int]:
    result = [0] * P
    for i, first in enumerate(left):
        if not first:
            continue
        for j, second in enumerate(right[: P - i]):
            result[i + j] = (
                result[i + j] + first * second
            ) % P
    return result


def polynomial_power(
    polynomial: Sequence[int], exponent: int
) -> list[int]:
    result = ONE[:]
    factor = list(polynomial)
    while exponent:
        if exponent & 1:
            result = polynomial_multiply(result, factor)
        factor = polynomial_multiply(factor, factor)
        exponent //= 2
    return result


def y_to_x_coefficients(polynomial: Sequence[int]) -> list[int]:
    """Convert y=x-1 coefficients to the cyclic x^0,...,x^36 basis."""

    result = [0] * P
    for degree in range(P - 1, -1, -1):
        result[degree] = (
            polynomial[degree]
            - sum(
                result[index] * comb(index, degree)
                for index in range(degree + 1, P)
            )
        ) % P
    return result


def reduced_row_basis(
    vectors: Iterable[Sequence[int]],
) -> tuple[list[list[int]], list[int]]:
    """Return an RREF row basis and its information coordinates."""

    basis: list[list[int]] = []
    pivots: list[int] = []
    for vector in vectors:
        work = [entry % P for entry in vector]
        for row, pivot in zip(basis, pivots):
            if work[pivot]:
                factor = work[pivot]
                work = [
                    (left - factor * right) % P
                    for left, right in zip(work, row)
                ]
        if not any(work):
            continue
        pivot = next(i for i, entry in enumerate(work) if entry)
        inverse = pow(work[pivot], -1, P)
        work = polynomial_scale(work, inverse)
        for index, row in enumerate(basis):
            if row[pivot]:
                factor = row[pivot]
                basis[index] = [
                    (left - factor * right) % P
                    for left, right in zip(row, work)
                ]
        insertion = sum(old < pivot for old in pivots)
        basis.insert(insertion, work)
        pivots.insert(insertion, pivot)
    require(
        all(
            basis[row][pivot] == int(row == column)
            for row in range(len(basis))
            for column, pivot in enumerate(pivots)
        ),
        "row basis is not systematic on the information set",
    )
    return basis, pivots


def algebra_multiply(
    left: Sequence[Sequence[int]],
    right: Sequence[Sequence[int]],
    jordan_type: str,
) -> list[list[int]]:
    """Multiply coefficients of I,P,N in the two normalized algebras."""

    first_i, first_p, first_n = left
    second_i, second_p, second_n = right
    result_i = polynomial_multiply(first_i, second_i)
    result_p = polynomial_add(
        polynomial_add(
            polynomial_multiply(first_i, second_p),
            polynomial_multiply(first_p, second_i),
        ),
        polynomial_multiply(first_p, second_p),
    )
    result_n = polynomial_add(
        polynomial_multiply(first_i, second_n),
        polynomial_multiply(first_n, second_i),
    )
    if jordan_type == "nonzero_J2":
        result_n = polynomial_add(
            result_n,
            polynomial_add(
                polynomial_multiply(first_p, second_n),
                polynomial_multiply(first_n, second_p),
            ),
        )
    elif jordan_type != "nonzero_eigenline_plus_J2_zero":
        raise ValueError("unknown normalized Jordan algebra")
    return [result_i, result_p, result_n]


def verify_normalized_exponentials(
    z: Sequence[int],
    x: Sequence[int],
    x_inverse: Sequence[int],
) -> dict[str, bool]:
    """Check the closed exponential formulas for both Jordan types."""

    a = polynomial_subtract(x, ONE)
    b = polynomial_subtract(x_inverse, ONE)
    formulas: dict[str, tuple[list[list[int]], list[list[int]]]] = {
        "nonzero_J2": (
            [ONE, a, polynomial_multiply(x, z)],
            [
                ONE,
                b,
                polynomial_scale(
                    polynomial_multiply(x_inverse, z), -1
                ),
            ],
        ),
        "nonzero_eigenline_plus_J2_zero": (
            [ONE, a, list(z)],
            [ONE, b, polynomial_scale(z, -1)],
        ),
    }
    result: dict[str, bool] = {}
    f1 = polynomial_add(a, b)
    f2 = polynomial_multiply(a, b)
    common_f3 = polynomial_multiply(
        z, polynomial_subtract(b, a)
    )
    f4 = polynomial_scale(polynomial_multiply(z, z), -1)
    for name, (positive, negative) in formulas.items():
        inverse_product = algebra_multiply(negative, positive, name)
        require(
            inverse_product == [ONE, ZERO, ZERO],
            f"normalized exponential formula failed for {name}",
        )

        # For symmetric M, reversal of a word in the symmetric letters
        # P,M,N has the same diagonal.  Group the nine terms of
        # E_- M E_+ into the six reversal classes
        # M, MP/PM, PMP, MN/NM, PMN/NMP, NMN.
        left_i, left_p, left_n = negative
        right_i, right_p, right_n = positive
        reversal_coefficients = [
            polynomial_multiply(left_i, right_i),
            polynomial_add(
                polynomial_multiply(left_i, right_p),
                polynomial_multiply(left_p, right_i),
            ),
            polynomial_multiply(left_p, right_p),
            polynomial_add(
                polynomial_multiply(left_i, right_n),
                polynomial_multiply(left_n, right_i),
            ),
            polynomial_add(
                polynomial_multiply(left_p, right_n),
                polynomial_multiply(left_n, right_p),
            ),
            polynomial_multiply(left_n, right_n),
        ]
        expected_reversal_coefficients = (
            [ONE, f1, f2, ZERO, common_f3, f4]
            if name == "nonzero_eigenline_plus_J2_zero"
            else [
                ONE,
                f1,
                f2,
                polynomial_scale(common_f3, -1),
                common_f3,
                f4,
            ]
        )
        require(
            reversal_coefficients == expected_reversal_coefficients,
            f"the symmetric diagonal span failed for {name}",
        )
        result[name] = True
    return result


def binary_words_in_coset(
    eta: int,
    h: Sequence[int],
    basis: Sequence[Sequence[int]],
    pivots: Sequence[int],
) -> tuple[list[tuple[int, ...]], int]:
    """Enumerate (eta*h+U) intersect ({0} x {18,19}^36)."""

    choices = [
        (0,) if pivot == 0 else (18, 19)
        for pivot in pivots
    ]
    words: list[tuple[int, ...]] = []
    assignments = 0
    for desired_values in product(*choices):
        assignments += 1
        coefficients = [
            (desired - eta * h[pivot]) % P
            for desired, pivot in zip(desired_values, pivots)
        ]
        word = [eta * value % P for value in h]
        for coefficient, row in zip(coefficients, basis):
            word = [
                (left + coefficient * right) % P
                for left, right in zip(word, row)
            ]
        if (
            word[0] == 0
            and all(value in (18, 19) for value in word[1:])
        ):
            words.append(
                tuple(
                    lag
                    for lag in range(1, P)
                    if word[lag] == 19
                )
            )
    return words, assignments


def verify_affine_diagonal_obstruction() -> dict[str, object]:
    """Build and exhaust the common affine diagonal over-code."""

    y = [0, 1] + [0] * (P - 2)
    x = polynomial_add(ONE, y)
    x_inverse = [
        1 if degree == 0 else (-1) ** degree % P
        for degree in range(P)
    ]
    require(
        polynomial_multiply(x, x_inverse) == ONE,
        "the truncated x inverse changed",
    )

    z = [0] * P
    for degree in range(1, P):
        z[degree] = (
            (1 if degree % 2 else -1) * pow(degree, -1, P)
        ) % P
    h = polynomial_power(z, 18)
    h_x = y_to_x_coefficients(h)
    require(
        h_x
        == [0]
        + [
            6 if pow(lag, 18, P) == 1 else P - 6
            for lag in range(1, P)
        ],
        "the z^18 quadratic-character identity changed",
    )
    require(
        polynomial_multiply(h, h) == [0] * (P - 1) + [1],
        "z^36 is no longer y^36",
    )

    exponential_checks = verify_normalized_exponentials(
        z, x, x_inverse
    )

    a = polynomial_subtract(x, ONE)
    b = polynomial_subtract(x_inverse, ONE)
    f1 = polynomial_add(a, b)
    f2 = polynomial_multiply(a, b)
    # The mixed-zero-Jordan type has this sign.  The nonzero-J2 type has
    # its negative, which spans the identical affine code.
    f3 = polynomial_multiply(z, polynomial_subtract(b, a))
    f4 = polynomial_scale(polynomial_multiply(z, z), -1)
    functions = [f1, f2, f3, f4]

    # For either surviving type and every symmetric constant M, the
    # diagonal of exp(-zA) M exp(zA) lies in span(1,f1,...,f4).
    # Taking M=N0 and then M=J therefore puts the formal diagonal in
    #
    #   eta*h + span(1,f1,...,f4,h*f1,...,h*f4).
    #
    # Treating all nine scalar coefficients as independent is a safe
    # over-approximation of the actual projector/nilpotent relations.
    generators_y = (
        [ONE] + functions
        + [polynomial_multiply(h, function) for function in functions]
    )
    generators_x = [
        y_to_x_coefficients(function)
        for function in generators_y
    ]
    basis, pivots = reduced_row_basis(generators_x)
    require(
        len(basis) == 7 and pivots == [0, 1, 2, 3, 4, 5, 6],
        "the common diagonal over-code changed",
    )
    require(
        len(reduced_row_basis(generators_x + [h_x])[0]) == 8,
        "h unexpectedly entered the homogeneous diagonal over-code",
    )

    spectrum: dict[str, dict[str, object]] = {}
    for eta in range(P):
        words, assignments = binary_words_in_coset(
            eta, h_x, basis, pivots
        )
        require(
            assignments == 64,
            "the information-set enumeration size changed",
        )
        if words:
            spectrum[str(eta)] = {
                "word_count": len(words),
                "weight_distribution": {
                    str(weight): count
                    for weight, count in sorted(
                        Counter(map(len, words)).items()
                    )
                },
                "supports": [list(word) for word in words],
            }

    expected_spectrum = {
        "3": {
            "word_count": 2,
            "weight_distribution": {"18": 1, "20": 1},
            "supports": [
                [2, 5, 6, 8, 13, 14, 15, 17, 18, 19, 20, 22, 23,
                 24, 29, 31, 32, 35],
                [1, 2, 5, 6, 8, 13, 14, 15, 17, 18, 19, 20, 22,
                 23, 24, 29, 31, 32, 35, 36],
            ],
        },
        "34": {
            "word_count": 2,
            "weight_distribution": {"16": 1, "18": 1},
            "supports": [
                [3, 4, 7, 9, 10, 11, 12, 16, 21, 25, 26, 27, 28,
                 30, 33, 34],
                [1, 3, 4, 7, 9, 10, 11, 12, 16, 21, 25, 26, 27,
                 28, 30, 33, 34, 36],
            ],
        },
    }
    require(
        spectrum == expected_spectrum,
        "the affine binary-coset spectrum changed",
    )
    require(
        "1" not in spectrum and str(P - 1) not in spectrum,
        "an actual trace orientation gained a binary diagonal word",
    )

    # The two integral trace orientations really are eta=+/-1:
    # 9 diagonal J entries times 19*y^36, plus 9*eta*z^18.
    trace_pairs = []
    for eta in (1, P - 1):
        trace_pairs.append(
            sorted({
                (9 * 19 + 9 * eta * character_coefficient) % P
                for character_coefficient in (6, P - 6)
            })
        )
    require(
        trace_pairs == [[3, 6], [3, 6]],
        "the 3/6 trace orientations changed",
    )

    return {
        "coefficient_ring": "F_37[y]/(y^37)",
        "formal_trace_orientations": [1, 36],
        "normalized_jordan_exponential_checks": exponential_checks,
        "homogeneous_affine_code_dimension": len(basis),
        "information_coordinates": pivots,
        "information_assignments_per_eta": 64,
        "h_outside_homogeneous_code": True,
        "nonempty_binary_cosets_by_eta": spectrum,
        "actual_orientation_binary_word_counts": {"1": 0, "36": 0},
        "excluded_normalized_jordan_types": [
            "nonzero_J2",
            "nonzero_eigenline_plus_J2_zero",
        ],
        "scale_normalization": (
            "x->x^(lambda^-1) sends the nonzero eigenvalue to 1 "
            "and eta to chi(lambda^-1)*eta, still in {+1,-1}"
        ),
    }


def verify() -> dict[str, object]:
    quotient = verify_exceptional_quotient()
    obstruction = verify_affine_diagonal_obstruction()
    report = {
        "status": "impossible",
        "claim": (
            "The two constant symmetric rank-two Jordan types left by "
            "the universal diagonal weight code cannot realize even one "
            "binary diagonal block after the fixed z^18 J coefficient "
            "is restored."
        ),
        "family_scope": (
            "constant symmetric rank-two A in the trace-corrected "
            "formal exponential family"
        ),
        "exceptional_sign_class": quotient,
        "affine_diagonal_obstruction": obstruction,
        "uses_specific_N0_entries": False,
        "uses_N0_symmetry": True,
        "uses_fixed_J_coefficient": True,
        "off_diagonal_binary_conditions_needed": False,
        "higher_y_conjugators": "open",
        "general_semiregular_C37_lift": "open",
    }
    with CERTIFICATE.open() as stream:
        expected = json.load(stream)
    require(report == expected, "certificate record changed")
    return report


def main() -> None:
    report = verify()
    affine = report["affine_diagonal_obstruction"]
    print(
        "exceptional_class=607/622 "
        "types=nonzero_J2,mixed_zero_J2 "
        "eta=+1:0 eta=-1:0 "
        f"homogeneous_dimension="
        f"{affine['homogeneous_affine_code_dimension']} "
        "status=IMPOSSIBLE"
    )
    print("PASS")


if __name__ == "__main__":
    main()
