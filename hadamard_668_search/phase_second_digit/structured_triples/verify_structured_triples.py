#!/usr/bin/env python3
"""Audit the six structured low-rank second-digit combinations.

For a nonzero column lag ``b``, put

    T_b = E0(b) + E1(b) + E1(27*b).

The multiplier 27 lies in the cyclotomic class of -1.  The exact adjoint
identity ``E2=omega^2 E1^*`` shows that, at the second lambda digit after
the lower two digits vanish, this is the digit of ``E0+E1+E2`` at b.
Equivalently it is the row-collapsed norm obtained by setting zeta_9=1.

This verifier:

* proves the resulting polar factorization through the 12-class
  cyclotomic algebra, plus the fixed-zero-column boundary term;
* reconstructs that cyclotomic algebra as F_27 x F_27;
* checks all six structured triples on all five exact h=2 profiles;
* evaluates all 3^6 character sums, without enumerating a phase point;
* proves exact scalar balance and counts every joint six-coordinate fiber.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
SECOND_DIGIT = HERE.parent
SEARCH_ROOT = SECOND_DIGIT.parent
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_phase_second_digit as base  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    coefficient_terms,
    first_digit_equations,
    matrix_rank,
    phase_entries,
    profiles_from_ids,
)
from verify_lp333_order3_quotient import (  # noqa: E402
    CLASS_OF,
    CLASSES,
    PARTS,
)


P = 3
CLASS_COUNT = 12
TRIPLE_COUNT = 6
AMBIENT_DIMENSION = 54
AFFINE_DIMENSION = 36
EXPECTED_SEMANTIC_SHA256 = (
    "aa6dbb0c3272e8695e3c8beff8381702a9f7f5a2505716138086d8074aa20d5c"
)

Vector = tuple[int, ...]
Matrix = tuple[tuple[int, ...], ...]
Eisenstein = tuple[int, int]


def mod3(value: int) -> int:
    return value % P


def zero_matrix(rows: int, columns: int | None = None) -> Matrix:
    if columns is None:
        columns = rows
    return ((0,) * columns,) * rows


def identity(size: int) -> Matrix:
    return tuple(
        tuple(int(row == column) for column in range(size))
        for row in range(size)
    )


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple((a + b) % P for a, b in zip(left_row, right_row))
        for left_row, right_row in zip(left, right)
    )


def matrix_scale(scalar: int, matrix: Matrix) -> Matrix:
    return tuple(
        tuple(scalar * value % P for value in row)
        for row in matrix
    )


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    if not left or not right:
        return ()
    inner = len(right)
    if len(left[0]) != inner:
        raise ValueError("matrix dimensions do not match")
    columns = len(right[0])
    return tuple(
        tuple(
            sum(
                left[row][middle] * right[middle][column]
                for middle in range(inner)
            )
            % P
            for column in range(columns)
        )
        for row in range(len(left))
    )


def transpose(matrix: Sequence[Sequence[int]]) -> Matrix:
    if not matrix:
        return ()
    return tuple(
        tuple(int(matrix[row][column]) % P for row in range(len(matrix)))
        for column in range(len(matrix[0]))
    )


def combine_vectors(
    coefficients: Sequence[int],
    rows: Sequence[Sequence[int]],
) -> Vector:
    return tuple(
        sum(
            int(coefficient) * int(row[column])
            for coefficient, row in zip(coefficients, rows)
        )
        % P
        for column in range(len(rows[0]))
    )


def combine_matrices(
    coefficients: Sequence[int],
    matrices: Sequence[Matrix],
) -> Matrix:
    size = len(matrices[0])
    return tuple(
        tuple(
            sum(
                int(coefficient) * matrix[row][column]
                for coefficient, matrix in zip(coefficients, matrices)
            )
            % P
            for column in range(size)
        )
        for row in range(size)
    )


def projective_vectors(dimension: int) -> tuple[Vector, ...]:
    result = []
    for vector in product(range(P), repeat=dimension):
        if not any(vector):
            continue
        if next(value for value in vector if value) == 1:
            result.append(vector)
    expected = (P**dimension - 1) // (P - 1)
    if len(result) != expected:
        raise AssertionError("projective-vector count changed")
    return tuple(result)


def rref(
    rows: Sequence[Sequence[int]],
) -> tuple[Matrix, tuple[int, ...]]:
    if not rows:
        return (), ()
    work = [list(map(mod3, row)) for row in rows]
    width = len(work[0])
    if any(len(row) != width for row in work):
        raise ValueError("matrix is not rectangular")
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        if work[pivot_row][column] == 2:
            work[pivot_row] = [
                2 * value % P for value in work[pivot_row]
            ]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % P
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def solve_linear(matrix: Matrix, target: Sequence[int]) -> Vector | None:
    """Return one solution of matrix*x=target, or None."""

    if len(matrix) != len(target):
        raise ValueError("linear target has wrong length")
    augmented = tuple(
        tuple(row) + (int(value) % P,)
        for row, value in zip(matrix, target)
    )
    reduced, pivots = rref(augmented)
    variables = len(matrix[0])
    if any(
        not any(row[:variables]) and row[variables]
        for row in reduced
    ):
        return None
    solution = [0] * variables
    for row, pivot in enumerate(pivots):
        if pivot == variables:
            return None
        solution[pivot] = reduced[row][variables]
    return tuple(solution)


def diagonal_values(matrix: Matrix) -> tuple[int, ...]:
    """Diagonalize a symmetric form by congruence over F_3."""

    size = len(matrix)
    work = [list(row) for row in matrix]
    rank = 0
    diagonal = []
    while rank < size:
        pivot = next(
            (index for index in range(rank, size) if work[index][index]),
            None,
        )
        if pivot is None:
            off_diagonal = next(
                (
                    (left, right)
                    for left in range(rank, size)
                    for right in range(left + 1, size)
                    if work[left][right]
                ),
                None,
            )
            if off_diagonal is None:
                break
            left, right = off_diagonal
            # Replace e_left by e_left+e_right.  Since all remaining
            # diagonal values are zero, its norm is 2*B(left,right).
            old_row = work[left][:]
            for column in range(size):
                work[left][column] = (
                    old_row[column] + work[right][column]
                ) % P
            old_column = [work[row][left] for row in range(size)]
            for row in range(size):
                work[row][left] = (
                    old_column[row] + work[row][right]
                ) % P
            pivot = left
        if pivot != rank:
            work[rank], work[pivot] = work[pivot], work[rank]
            for row in range(size):
                work[row][rank], work[row][pivot] = (
                    work[row][pivot],
                    work[row][rank],
                )
        value = work[rank][rank]
        if not value:
            raise AssertionError("symmetric pivot creation failed")
        inverse = pow(value, -1, P)
        for column in range(rank + 1, size):
            if not work[rank][column]:
                continue
            factor = work[rank][column] * inverse % P
            # Congruence operation e_column <- e_column-factor*e_rank.
            old_column = [work[row][column] for row in range(size)]
            for row in range(size):
                work[row][column] = (
                    old_column[row] - factor * work[row][rank]
                ) % P
            old_row = work[column][:]
            for row_column in range(size):
                work[column][row_column] = (
                    old_row[row_column]
                    - factor * work[rank][row_column]
                ) % P
        diagonal.append(value)
        rank += 1
    if any(
        work[row][column]
        for row in range(rank, size)
        for column in range(rank, size)
    ):
        raise AssertionError("symmetric diagonalization left a tail")
    if len(diagonal) != matrix_rank(matrix):
        raise AssertionError("symmetric diagonalization rank changed")
    return tuple(diagonal)


OMEGA_POWERS: tuple[Eisenstein, ...] = (
    (1, 0),
    (0, 1),
    (-1, -1),
)


def e_add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] + right[0], left[1] + right[1]


def e_scale(scalar: int, value: Eisenstein) -> Eisenstein:
    return scalar * value[0], scalar * value[1]


def e_multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_conjugate(value: Eisenstein) -> Eisenstein:
    return value[0] - value[1], -value[1]


def character_sum(
    constant: int,
    linear: Vector,
    polar: Matrix,
) -> Eisenstein:
    """Return sum_y omega^q(y) exactly in Z[omega]."""

    dimension = len(linear)
    solution = solve_linear(polar, linear)
    if solution is None:
        return (0, 0)
    rank = matrix_rank(polar)
    shifted_constant = (
        constant
        - 2
        * sum(
            solution[left]
            * polar[left][right]
            * solution[right]
            for left in range(dimension)
            for right in range(dimension)
        )
    ) % P
    value = OMEGA_POWERS[shifted_constant]
    for diagonal in diagonal_values(polar):
        # The quadratic coefficient is diagonal/2=2*diagonal.
        factor = e_add(
            (1, 0),
            e_scale(2, OMEGA_POWERS[2 * diagonal % P]),
        )
        value = e_multiply(value, factor)
    return e_scale(P ** (dimension - rank), value)


def scalar_fiber_counts(
    constant: int,
    linear: Vector,
    polar: Matrix,
) -> tuple[int, int, int]:
    """Count q(y)=0,1,2 by an exact one-dimensional Fourier transform."""

    dimension = len(linear)
    total = P**dimension
    first = character_sum(constant, linear, polar)
    second = e_conjugate(first)
    result = []
    for target in range(P):
        correction = e_add(
            e_multiply(OMEGA_POWERS[-target % P], first),
            e_multiply(OMEGA_POWERS[-2 * target % P], second),
        )
        if correction[1]:
            raise AssertionError("a scalar fiber correction is not rational")
        if (total + correction[0]) % P:
            raise AssertionError("a scalar fiber count is not integral")
        result.append((total + correction[0]) // P)
    if sum(result) != total:
        raise AssertionError("scalar fibers do not partition the domain")
    return tuple(result)  # type: ignore[return-value]


def audit_character_sum_primitive() -> int:
    """Exhaustively compare the exact Gauss sum on every binary form."""

    checks = 0
    points = tuple(product(range(P), repeat=2))
    for diagonal_left, cross, diagonal_right in product(
        range(P), repeat=3
    ):
        polar = (
            (diagonal_left, cross),
            (cross, diagonal_right),
        )
        for linear in product(range(P), repeat=2):
            for constant in range(P):
                expected = [0, 0, 0]
                for point in points:
                    value = constant
                    value += sum(
                        linear[index] * point[index] for index in range(2)
                    )
                    value += 2 * sum(
                        point[left]
                        * polar[left][right]
                        * point[right]
                        for left in range(2)
                        for right in range(2)
                    )
                    expected[value % P] += 1
                if scalar_fiber_counts(
                    constant, tuple(linear), polar
                ) != tuple(expected):
                    raise AssertionError("quadratic Gauss sum failed replay")
                checks += 1
    if checks != 729:
        raise AssertionError("quadratic primitive check count changed")
    return checks


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def cyclotomic_polar_matrices() -> tuple[Matrix, ...]:
    result = []
    for lag_class in range(TRIPLE_COUNT):
        transition = [[0] * CLASS_COUNT for _ in range(CLASS_COUNT)]
        lag = CLASSES[lag_class][0]
        for source in range(1, 37):
            target = (source + lag) % 37
            if target:
                transition[CLASS_OF[source]][CLASS_OF[target]] += 1
        result.append(
            tuple(
                tuple(
                    (
                        transition[left][right]
                        + transition[right][left]
                    )
                    % P
                    for right in range(CLASS_COUNT)
                )
                for left in range(CLASS_COUNT)
            )
        )
    return tuple(result)


CYCLOTOMIC_POLAR = cyclotomic_polar_matrices()


def coordinates_in_cyclotomic_basis(matrix: Matrix) -> Vector:
    columns = tuple(
        tuple(
            CYCLOTOMIC_POLAR[basis][row][column]
            for basis in range(TRIPLE_COUNT)
        )
        for row in range(CLASS_COUNT)
        for column in range(CLASS_COUNT)
    )
    augmented = tuple(
        row + (matrix[index // CLASS_COUNT][index % CLASS_COUNT],)
        for index, row in enumerate(columns)
    )
    reduced, pivots = rref(augmented)
    if len(tuple(pivot for pivot in pivots if pivot < TRIPLE_COUNT)) != 6:
        raise AssertionError("cyclotomic matrices lost independence")
    if any(
        not any(row[:TRIPLE_COUNT]) and row[TRIPLE_COUNT]
        for row in reduced
    ):
        raise AssertionError("matrix left the cyclotomic span")
    result = [0] * TRIPLE_COUNT
    for row, pivot in enumerate(pivots):
        if pivot < TRIPLE_COUNT:
            result[pivot] = reduced[row][TRIPLE_COUNT]
    if combine_matrices(result, CYCLOTOMIC_POLAR) != matrix:
        raise AssertionError("cyclotomic coordinate recovery failed")
    return tuple(result)


def audit_cyclotomic_algebra() -> dict[str, object]:
    if combine_matrices((1,) * 6, CYCLOTOMIC_POLAR) != matrix_scale(
        2, identity(CLASS_COUNT)
    ):
        raise AssertionError("cyclotomic sum is not 2I")
    for left in CYCLOTOMIC_POLAR:
        for right in CYCLOTOMIC_POLAR:
            if matrix_multiply(left, right) != matrix_multiply(right, left):
                raise AssertionError("cyclotomic pencil is not commutative")
            coordinates_in_cyclotomic_basis(
                matrix_multiply(left, right)
            )
    rank_histogram = Counter(
        matrix_rank(combine_matrices(vector, CYCLOTOMIC_POLAR))
        for vector in projective_vectors(6)
    )
    expected = {6: 26, 12: 338}
    if dict(rank_histogram) != expected:
        raise AssertionError("cyclotomic projective ranks changed")
    idempotents = []
    for vector in product(range(P), repeat=6):
        matrix = combine_matrices(vector, CYCLOTOMIC_POLAR)
        if matrix_multiply(matrix, matrix) == matrix:
            idempotents.append(vector)
    expected_idempotents = {
        (0, 0, 0, 0, 0, 0),
        (2, 0, 2, 0, 2, 0),
        (0, 2, 0, 2, 0, 2),
        (2, 2, 2, 2, 2, 2),
    }
    if set(idempotents) != expected_idempotents:
        raise AssertionError("cyclotomic idempotents changed")
    return {
        "algebra": "F_27 x F_27",
        "full_bulk_translation_algebra": (
            "F_27[epsilon]/(epsilon^3) x "
            "F_27[epsilon]/(epsilon^3)"
        ),
        "row_algebra": "F_3[epsilon]/(epsilon^3)",
        "row_collapse": "epsilon -> 0",
        "identity_coordinates": (2,) * 6,
        "projective_rank_histogram": dict(sorted(rank_histogram.items())),
        "idempotents": tuple(sorted(idempotents)),
    }


def ambient_row_polar(terms: Iterable[object]) -> Matrix:
    result = [[0] * AMBIENT_DIMENSION for _ in range(AMBIENT_DIMENSION)]
    for term in terms:
        slope = dict(term.coefficients)
        for left, left_value in slope.items():
            for right, right_value in slope.items():
                result[left][right] = (
                    result[left][right]
                    + term.sign * left_value * right_value
                ) % P
    return tuple(tuple(row) for row in result)


def restrict_polar(matrix: Matrix, basis: Sequence[Sequence[int]]) -> Matrix:
    # Basis vectors are stored basis-coordinate first, ambient-coordinate
    # second.  The restricted matrix is K^T B K.
    return tuple(
        tuple(
            sum(
                basis[left][ambient_left]
                * matrix[ambient_left][ambient_right]
                * basis[right][ambient_right]
                for ambient_left in range(AMBIENT_DIMENSION)
                for ambient_right in range(AMBIENT_DIMENSION)
            )
            % P
            for right in range(len(basis))
        )
        for left in range(len(basis))
    )


def factorized_ambient_polar(
    profiles: Sequence[Sequence[Sequence[int]]],
    lag_class: int,
) -> tuple[Matrix, tuple[int, int], tuple[int, int]]:
    """Build the row-collapse factorization for one structured triple.

    For one channel and nonzero physical column c, let

        g_c = sum_s sign(c,s) slope(c,s),
        H_c = sum_s sign(c,s) slope(c,s)slope(c,s)^T.

    The profile entries sum to weight three, hence their signed active count
    is zero modulo three.  The fixed zero column has signed count -1.
    Consequently

        B_b = -G^T M_b G - H_b - H_-b.
    """

    entries = phase_entries(profiles)
    result = [[0] * AMBIENT_DIMENSION for _ in range(AMBIENT_DIMENSION)]
    bulk_ranks = []
    boundary_ranks = []
    for channel in range(2):
        zero_signed_count = sum(
            entry.sign for entry in entries[channel][0] if entry is not None
        ) % P
        if zero_signed_count != 2:
            raise AssertionError("zero-column signed count changed")

        g_rows = []
        h_diagonals = []
        for class_index in range(CLASS_COUNT):
            representative = CLASSES[class_index][0]
            signed_count = sum(
                entry.sign
                for entry in entries[channel][representative]
                if entry is not None
            ) % P
            if signed_count:
                raise AssertionError("a weight-three profile sum is nonzero")
            g = [0] * AMBIENT_DIMENSION
            h = [0] * AMBIENT_DIMENSION
            for entry in entries[channel][representative]:
                if entry is None or entry.variable is None:
                    continue
                g[entry.variable] = (
                    g[entry.variable] + entry.sign * entry.slope
                ) % P
                h[entry.variable] = (
                    h[entry.variable]
                    + entry.sign * entry.slope * entry.slope
                ) % P
            g_rows.append(tuple(g))
            h_diagonals.append(tuple(h))
        g_matrix = tuple(g_rows)
        bulk = matrix_multiply(
            transpose(g_matrix),
            matrix_multiply(CYCLOTOMIC_POLAR[lag_class], g_matrix),
        )
        opposite = (lag_class + 6) % CLASS_COUNT
        boundary_diagonal = tuple(
            (
                h_diagonals[lag_class][index]
                + h_diagonals[opposite][index]
            )
            % P
            for index in range(AMBIENT_DIMENSION)
        )
        boundary = tuple(
            tuple(
                boundary_diagonal[row] if row == column else 0
                for column in range(AMBIENT_DIMENSION)
            )
            for row in range(AMBIENT_DIMENSION)
        )
        channel_result = matrix_scale(
            2, matrix_add(bulk, boundary)
        )
        for row in range(AMBIENT_DIMENSION):
            for column in range(AMBIENT_DIMENSION):
                result[row][column] = (
                    result[row][column] + channel_result[row][column]
                ) % P
        bulk_ranks.append(matrix_rank(bulk))
        boundary_ranks.append(matrix_rank(boundary))
    return (
        tuple(tuple(row) for row in result),
        tuple(bulk_ranks),  # type: ignore[arg-type]
        tuple(boundary_ranks),  # type: ignore[arg-type]
    )


def combine_triples(
    constants: Sequence[int],
    linears: Sequence[Vector],
    polars: Sequence[Matrix],
) -> tuple[Vector, tuple[Vector, ...], tuple[Matrix, ...]]:
    indices = tuple(
        (1 + lag, 8 + lag, 14 + lag)
        for lag in range(TRIPLE_COUNT)
    )
    return (
        tuple(
            sum(constants[index] for index in triple) % P
            for triple in indices
        ),
        tuple(
            combine_vectors((1, 1, 1), tuple(linears[index] for index in triple))
            for triple in indices
        ),
        tuple(
            combine_matrices((1, 1, 1), tuple(polars[index] for index in triple))
            for triple in indices
        ),
    )


def joint_fiber_distribution(
    constants: Vector,
    linears: Sequence[Vector],
    polars: Sequence[Matrix],
) -> tuple[int, ...]:
    characters: dict[Vector, Eisenstein] = {}
    for coefficients in product(range(P), repeat=TRIPLE_COUNT):
        if not any(coefficients):
            characters[coefficients] = (P**AFFINE_DIMENSION, 0)
            continue
        characters[coefficients] = character_sum(
            sum(
                coefficient * constant
                for coefficient, constant in zip(coefficients, constants)
            )
            % P,
            combine_vectors(coefficients, linears),
            combine_matrices(coefficients, polars),
        )
    counts = []
    for target in product(range(P), repeat=TRIPLE_COUNT):
        total: Eisenstein = (0, 0)
        for coefficients, value in characters.items():
            exponent = -sum(
                coefficient * target_value
                for coefficient, target_value in zip(coefficients, target)
            )
            total = e_add(
                total,
                e_multiply(OMEGA_POWERS[exponent % P], value),
            )
        if total[1] or total[0] % (P**TRIPLE_COUNT):
            raise AssertionError("joint Fourier inversion was not integral")
        counts.append(total[0] // (P**TRIPLE_COUNT))
    if sum(counts) != P**AFFINE_DIMENSION:
        raise AssertionError("joint fibers do not partition the domain")
    return tuple(counts)


def audit_profile(index: int) -> dict[str, object]:
    label, partition, target, identifiers_a, identifiers_b = (
        base.CANDIDATES[index]
    )
    profiles = profiles_from_ids(identifiers_a, identifiers_b)
    equations = first_digit_equations(profiles)
    origin, basis = base.affine_parameterization(
        equations, AMBIENT_DIMENSION
    )
    term_data = base.second_digit_term_data(profiles)
    constants, linears, polars = base.derive_quadratics(
        term_data, origin, basis
    )
    triple_constants, triple_linears, triple_polars = combine_triples(
        constants, linears, polars
    )

    factor_records = []
    for lag_class, triple in enumerate(
        (1 + lag, 8 + lag, 14 + lag)
        for lag in range(TRIPLE_COUNT)
    ):
        ambient = combine_matrices(
            (1, 1, 1),
            tuple(
                ambient_row_polar(term_data[index_in_triple][0])
                for index_in_triple in triple
            ),
        )
        factorized, bulk_ranks, boundary_ranks = factorized_ambient_polar(
            profiles, lag_class
        )
        if ambient != factorized:
            raise AssertionError("row-collapse polar factorization failed")
        if restrict_polar(ambient, basis) != triple_polars[lag_class]:
            raise AssertionError("ambient/restricted structured polar changed")
        polar_rank = matrix_rank(triple_polars[lag_class])
        augmented_rank = matrix_rank(
            triple_polars[lag_class]
            + (triple_linears[lag_class],)
        )
        if augmented_rank != polar_rank + 1:
            raise AssertionError("a structured triple lost scalar balance")
        radical_witness = solve_linear(
            triple_polars[lag_class] + (triple_linears[lag_class],),
            (0,) * AFFINE_DIMENSION + (1,),
        )
        if radical_witness is None:
            raise AssertionError("a scalar-balance witness disappeared")
        if any(
            sum(
                triple_polars[lag_class][row][column]
                * radical_witness[column]
                for column in range(AFFINE_DIMENSION)
            )
            % P
            for row in range(AFFINE_DIMENSION)
        ):
            raise AssertionError("balance witness left the polar radical")
        if sum(
            left * right
            for left, right in zip(
                triple_linears[lag_class], radical_witness
            )
        ) % P != 1:
            raise AssertionError("balance witness has wrong linear response")
        scalar_counts = scalar_fiber_counts(
            triple_constants[lag_class],
            triple_linears[lag_class],
            triple_polars[lag_class],
        )
        if scalar_counts != (P**35,) * P:
            raise AssertionError("a structured triple is not exactly balanced")
        factor_records.append({
            "lag_class": lag_class,
            "physical_lag": CLASSES[lag_class][0],
            "opposite_lag": CLASSES[lag_class + 6][0],
            "restricted_rank": polar_rank,
            "radical_dimension": AFFINE_DIMENSION - polar_rank,
            "linear_augmented_rank": augmented_rank,
            "ambient_rank": matrix_rank(ambient),
            "bulk_rank_by_channel": bulk_ranks,
            "boundary_rank_by_channel": boundary_ranks,
            "each_scalar_fiber": P**35,
            "radical_translation_response": 1,
            "radical_witness_weight": sum(
                value != 0 for value in radical_witness
            ),
            "radical_witness_sha256": compact_hash(radical_witness),
        })

    pencil_rank_histogram: Counter[int] = Counter()
    balanced_pencils = 0
    minimum_scalar_fiber = P**AFFINE_DIMENSION
    minimum_record = None
    for coefficients in projective_vectors(TRIPLE_COUNT):
        constant = sum(
            coefficient * value
            for coefficient, value in zip(coefficients, triple_constants)
        ) % P
        linear = combine_vectors(coefficients, triple_linears)
        polar = combine_matrices(coefficients, triple_polars)
        rank = matrix_rank(polar)
        pencil_rank_histogram[rank] += 1
        if matrix_rank(polar + (linear,)) == rank + 1:
            balanced_pencils += 1
        counts = scalar_fiber_counts(constant, linear, polar)
        local_minimum = min(counts)
        if local_minimum < minimum_scalar_fiber:
            minimum_scalar_fiber = local_minimum
            minimum_record = {
                "coefficients": coefficients,
                "rank": rank,
                "counts": counts,
            }
    if minimum_scalar_fiber <= 0:
        raise AssertionError("a structured-pencil scalar obstruction appeared")

    joint_counts = joint_fiber_distribution(
        triple_constants, triple_linears, triple_polars
    )
    if min(joint_counts) <= 0:
        raise AssertionError("the six-coordinate structured map is not onto")
    joint_average = P ** (AFFINE_DIMENSION - TRIPLE_COUNT)
    deviation_unit = P**13
    deviations = tuple(
        (count - joint_average) // deviation_unit
        for count in joint_counts
    )
    if any(
        count - joint_average != multiplier * deviation_unit
        for count, multiplier in zip(joint_counts, deviations)
    ):
        raise AssertionError("a joint fiber lost its 3^13 congruence")
    return {
        "label": label,
        "partition": partition,
        "target": target,
        "structured_triples": tuple(factor_records),
        "pencil": {
            "projective_members": len(projective_vectors(TRIPLE_COUNT)),
            "rank_histogram": dict(sorted(pencil_rank_histogram.items())),
            "balanced_members": balanced_pencils,
            "minimum_scalar_fiber": minimum_scalar_fiber,
            "minimum_record": minimum_record,
        },
        "joint_map": {
            "domain_dimension": AFFINE_DIMENSION,
            "codomain_dimension": TRIPLE_COUNT,
            "fibers": len(joint_counts),
            "surjective": True,
            "zero_fiber": joint_counts[0],
            "minimum_fiber": min(joint_counts),
            "maximum_fiber": max(joint_counts),
            "distinct_fiber_sizes": len(set(joint_counts)),
            "average_fiber": joint_average,
            "deviation_unit": deviation_unit,
            "minimum_deviation_multiplier": min(deviations),
            "maximum_deviation_multiplier": max(deviations),
            "distribution_sha256": compact_hash(joint_counts),
        },
    }


def build_certificate() -> dict[str, object]:
    primitive_checks = audit_character_sum_primitive()
    algebra = audit_cyclotomic_algebra()
    profiles = tuple(
        audit_profile(index) for index in range(len(base.CANDIDATES))
    )
    return {
        "schema": "lp333-h2-structured-second-digit-triples-v1",
        "scope": (
            "Six row-collapsed quadratic combinations on the five exact "
            "h=2 profiles; character sums only, no phase enumeration."
        ),
        "cyclotomic_algebra": algebra,
        "quadratic_primitive_checks": primitive_checks,
        "profiles": profiles,
    }


def main() -> None:
    certificate = build_certificate()
    semantic_sha256 = compact_hash(certificate)
    if EXPECTED_SEMANTIC_SHA256 and (
        semantic_sha256 != EXPECTED_SEMANTIC_SHA256
    ):
        raise AssertionError("structured-triple semantic certificate changed")
    print(
        "cyclotomic_algebra="
        f"{certificate['cyclotomic_algebra']['algebra']}"
    )
    for profile in certificate["profiles"]:
        factors = profile["structured_triples"]
        pencil = profile["pencil"]
        joint = profile["joint_map"]
        print(profile["label"])
        print(
            "  structured_ranks="
            f"{tuple(record['restricted_rank'] for record in factors)}"
        )
        print(
            "  ambient_ranks="
            f"{tuple(record['ambient_rank'] for record in factors)}"
        )
        print(
            "  pencil_rank_histogram="
            f"{pencil['rank_histogram']}"
        )
        print(
            "  balanced_projective_members="
            f"{pencil['balanced_members']}/"
            f"{pencil['projective_members']}"
        )
        print(
            "  minimum_scalar_fiber="
            f"{pencil['minimum_scalar_fiber']}"
        )
        print(
            "  joint_zero_min_max="
            f"{joint['zero_fiber']},"
            f"{joint['minimum_fiber']},"
            f"{joint['maximum_fiber']}"
        )
        print(
            "  joint_distribution_sha256="
            f"{joint['distribution_sha256']}"
        )
    print(f"semantic_sha256={semantic_sha256}")


if __name__ == "__main__":
    main()
