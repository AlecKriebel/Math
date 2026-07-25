#!/usr/bin/env python3
"""Verify the orbit-2 quadratic character compression over F_3."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent / "h0_orbit2_lift_audit"
sys.path.insert(0, str(AUDIT))

import search_orbit2_digit2_sat as orbit2  # noqa: E402


EXPECTED_HASHES = {
    "constants": "40f6f49cbe73407bb633f060629361324cf16971c964a88529e7b445ae22a19b",
    "linears": "7d26f6bc846a7347eac8b9a1e8435ee298915532c140a743f268ec664cc990f6",
    "polars": "e5040bf5bfecfc228c7a1c5db86300d3affcb55974fe66645650b24ea99f7e27",
    "parametrization": "6e0032c7e95c3485df28df3c2666e6416cd465ca0f891ad5ca49286edc4093f9",
}

EXCEPTION_REPRESENTATIVES = (
    (1, 1, 2, 2, 1, 2),
    (1, 2, 0, 2, 1, 2),
    (1, 2, 2, 1, 2, 1),
)

EXPECTED_RANK_HISTOGRAM = {
    (19, 20): 4,
    (20, 21): 8,
    (21, 22): 14,
    (22, 23): 20,
    (23, 24): 20,
    (24, 25): 48,
    (25, 26): 52,
    (26, 27): 40,
    (27, 28): 54,
    (28, 29): 104,
    (29, 30): 56,
    (30, 31): 72,
    (31, 32): 64,
    (32, 33): 68,
    (33, 33): 2,
    (33, 34): 58,
    (34, 34): 4,
    (34, 35): 40,
}

EXPECTED_FIBER_HISTOGRAM = {
    205_891_120_934_388: 27,
    205_891_125_717_357: 135,
    205_891_130_500_326: 243,
    205_891_135_283_295: 216,
    205_891_140_066_264: 108,
}

PREFIX_CERTIFICATE = HERE / "EXACT_PREFIX_ZERO_FIBERS.json"


def digest(value: object) -> str:
    payload = json.dumps(
        value, separators=(",", ":"), sort_keys=True
    ).encode()
    return sha256(payload).hexdigest()


def rref_mod3(matrix: np.ndarray) -> tuple[np.ndarray, tuple[int, ...]]:
    work = np.array(matrix, dtype=np.int16) % 3
    rows, columns = work.shape
    pivot_row = 0
    pivots: list[int] = []
    for column in range(columns):
        choices = np.flatnonzero(work[pivot_row:, column])
        if not len(choices):
            continue
        selected = pivot_row + int(choices[0])
        work[[pivot_row, selected]] = work[[selected, pivot_row]]
        if work[pivot_row, column] == 2:
            work[pivot_row] = 2 * work[pivot_row] % 3
        for row in range(rows):
            if row != pivot_row and work[row, column]:
                work[row] = (
                    work[row]
                    - work[row, column] * work[pivot_row]
                ) % 3
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return work, tuple(pivots)


def rank_mod3(matrix: np.ndarray) -> int:
    return len(rref_mod3(matrix)[1])


def nullspace_mod3(matrix: np.ndarray) -> np.ndarray:
    work, pivots = rref_mod3(matrix)
    columns = work.shape[1]
    free = tuple(column for column in range(columns) if column not in pivots)
    basis = []
    for free_column in free:
        vector = np.zeros(columns, dtype=np.int16)
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -work[row, free_column] % 3
        basis.append(vector)
    return np.array(basis, dtype=np.int16)


def canonical_solution(matrix: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    variables = matrix.shape[1]
    work, pivots = rref_mod3(np.column_stack((matrix, rhs)))
    if variables in pivots:
        raise AssertionError("the requested linear system is inconsistent")
    result = np.zeros(variables, dtype=np.int16)
    for row, pivot in enumerate(pivots):
        result[pivot] = work[row, -1]
    assert np.array_equal(matrix @ result % 3, rhs % 3)
    return result


def congruence_diagonal(
    matrix: np.ndarray, linear: np.ndarray
) -> tuple[np.ndarray, np.ndarray, int]:
    """Diagonalize a symmetric matrix and transform its linear term."""

    polar = np.array(matrix, dtype=np.int16) % 3
    term = np.array(linear, dtype=np.int16) % 3
    size = len(term)
    rank = 0

    def apply(change: np.ndarray) -> None:
        nonlocal polar, term
        polar = change.T @ polar @ change % 3
        term = change.T @ term % 3

    while rank < size:
        diagonal = next(
            (
                index
                for index in range(rank, size)
                if polar[index, index]
            ),
            None,
        )
        if diagonal is None:
            pair = next(
                (
                    (left, right)
                    for left in range(rank, size)
                    for right in range(left + 1, size)
                    if polar[left, right]
                ),
                None,
            )
            if pair is None:
                break
            left, right = pair
            change = np.eye(size, dtype=np.int16)
            change[right, left] = 1
            apply(change)
            diagonal = left
        if diagonal != rank:
            change = np.eye(size, dtype=np.int16)
            change[:, [rank, diagonal]] = change[:, [diagonal, rank]]
            apply(change)

        inverse = 1 if polar[rank, rank] == 1 else 2
        for column in range(rank + 1, size):
            if not polar[rank, column]:
                continue
            change = np.eye(size, dtype=np.int16)
            change[rank, column] = (
                -inverse * polar[rank, column]
            ) % 3
            apply(change)
        rank += 1

    assert np.array_equal(polar, np.diag(np.diag(polar)))
    return np.diag(polar) % 3, term % 3, rank


def scalar_value_counts(
    constant: int, linear: np.ndarray, polar: np.ndarray
) -> tuple[tuple[int, int, int], int, bool]:
    """Count the three values of one quadratic without point enumeration."""

    diagonal, transformed_linear, rank = congruence_diagonal(
        polar, linear
    )
    if np.any(transformed_linear[rank:]):
        return (3**35, 3**35, 3**35), rank, True

    counts = [0, 0, 0]
    counts[int(constant) % 3] = 1
    # q(x)=c+l.x+(1/2)x^T Bx and 1/2=2 in F_3.
    for quadratic, affine in zip(
        2 * diagonal[:rank] % 3, transformed_linear[:rank]
    ):
        next_counts = [0, 0, 0]
        for old_value, multiplicity in enumerate(counts):
            for value in range(3):
                image = (
                    old_value
                    + int(quadratic) * value * value
                    + int(affine) * value
                ) % 3
                next_counts[image] += multiplicity
        counts = next_counts
    counts = [value * 3 ** (36 - rank) for value in counts]
    assert sum(counts) == 3**36
    return tuple(counts), rank, False


def fast_scalar_zero_count(
    constant: int, linear: np.ndarray, polar: np.ndarray
) -> int:
    """Return #q^{-1}(0) by symmetric Schur elimination over F_3."""

    matrix = np.array(polar, dtype=np.int16) % 3
    affine = np.array(linear, dtype=np.int16) % 3
    size = len(affine)
    diagonal: list[int] = []
    transformed_affine: list[int] = []
    pivot = 0
    while pivot < size:
        selected = next(
            (
                index
                for index in range(pivot, size)
                if matrix[index, index]
            ),
            None,
        )
        if selected is None:
            pair = next(
                (
                    (left, right)
                    for left in range(pivot, size)
                    for right in range(left + 1, size)
                    if matrix[left, right]
                ),
                None,
            )
            if pair is None:
                break
            left, right = pair
            if left != pivot:
                matrix[[pivot, left], :] = matrix[[left, pivot], :]
                matrix[:, [pivot, left]] = matrix[:, [left, pivot]]
                affine[[pivot, left]] = affine[[left, pivot]]
            old_diagonal = int(matrix[pivot, pivot])
            right_diagonal = int(matrix[right, right])
            cross = int(matrix[pivot, right])
            combined_row = (matrix[pivot] + matrix[right]) % 3
            matrix[pivot] = combined_row
            matrix[:, pivot] = combined_row
            matrix[pivot, pivot] = (
                old_diagonal + right_diagonal + 2 * cross
            ) % 3
            affine[pivot] = (affine[pivot] + affine[right]) % 3
            selected = pivot
        if selected != pivot:
            matrix[[pivot, selected], :] = matrix[[selected, pivot], :]
            matrix[:, [pivot, selected]] = matrix[:, [selected, pivot]]
            affine[[pivot, selected]] = affine[[selected, pivot]]

        value = int(matrix[pivot, pivot])
        inverse = 1 if value == 1 else 2
        cross = matrix[pivot, pivot + 1 :].copy()
        linear_value = int(affine[pivot])
        matrix[pivot + 1 :, pivot + 1 :] = (
            matrix[pivot + 1 :, pivot + 1 :]
            - inverse * np.outer(cross, cross)
        ) % 3
        affine[pivot + 1 :] = (
            affine[pivot + 1 :] - inverse * linear_value * cross
        ) % 3
        matrix[pivot, pivot + 1 :] = 0
        matrix[pivot + 1 :, pivot] = 0
        diagonal.append(value)
        transformed_affine.append(linear_value)
        pivot += 1

    if np.any(affine[pivot:]):
        return 3**35
    counts = [0, 0, 0]
    counts[int(constant) % 3] = 1
    for quadratic, linear_value in zip(diagonal, transformed_affine):
        next_counts = [0, 0, 0]
        for old_value, multiplicity in enumerate(counts):
            for value in range(3):
                image = (
                    old_value
                    + 2 * quadratic * value * value
                    + linear_value * value
                ) % 3
                next_counts[image] += multiplicity
        counts = next_counts
    return counts[0] * 3 ** (36 - pivot)


def exact_prefix_zero_fibers(
    g_constants: np.ndarray,
    g_linears: np.ndarray,
    g_polars: np.ndarray,
    q_constants: np.ndarray,
    q_linears: np.ndarray,
    q_polars: np.ndarray,
) -> dict[int, int]:
    """Count zero fibers for (g_0,...,g_5,q_0,...,q_3)."""

    constants = np.concatenate((g_constants, q_constants[:4]))
    linears = np.concatenate((g_linears, q_linears[:4]), axis=0)
    polars = np.concatenate((g_polars, q_polars[:4]), axis=0)

    # Cross-check the fast Schur implementation against the detached
    # congruence implementation before the full character pass.
    fixtures = [
        tuple(
            (
                0
                if index < first
                else 1
                if index == first
                else (fixture * (index + 1) + index * index) % 3
            )
            for index in range(10)
        )
        for fixture, first in enumerate((0, 1, 2, 3, 4, 5, 6, 7))
    ]
    for coordinates in fixtures:
        coefficient = np.array(coordinates, dtype=np.int16)
        scalar_constant = int(coefficient @ constants % 3)
        scalar_linear = coefficient @ linears % 3
        scalar_polar = np.einsum(
            "e,eij->ij", coefficient, polars
        ) % 3
        slow_counts, _, _ = scalar_value_counts(
            scalar_constant, scalar_linear, scalar_polar
        )
        assert fast_scalar_zero_count(
            scalar_constant, scalar_linear, scalar_polar
        ) == slow_counts[0]

    # One pass over projective F_3^10.  A line whose final nonzero
    # coordinate is d-1 first contributes to the d-equation prefix.
    contribution_by_dimension = [0] * 11
    projective_lines = 0
    for first_nonzero in range(10):
        for tail in itertools.product(
            range(3), repeat=9 - first_nonzero
        ):
            coordinates = (
                (0,) * first_nonzero + (1,) + tuple(tail)
            )
            coefficient = np.array(coordinates, dtype=np.int16)
            scalar_constant = int(coefficient @ constants % 3)
            scalar_linear = coefficient @ linears % 3
            scalar_polar = np.einsum(
                "e,eij->ij", coefficient, polars
            ) % 3
            zero_count = fast_scalar_zero_count(
                scalar_constant, scalar_linear, scalar_polar
            )
            effective_dimension = max(
                index
                for index, value in enumerate(coordinates)
                if value
            ) + 1
            contribution_by_dimension[effective_dimension] += (
                3 * zero_count - 3**36
            )
            projective_lines += 1
    assert projective_lines == (3**10 - 1) // 2 == 29_524

    numerator = 3**36
    result = {}
    for dimension in range(1, 11):
        numerator += contribution_by_dimension[dimension]
        if dimension >= 6:
            assert numerator % 3**dimension == 0
            result[dimension] = numerator // 3**dimension
    return result


def evaluate_vector(
    constants: np.ndarray,
    linears: np.ndarray,
    polars: np.ndarray,
    point: np.ndarray,
) -> np.ndarray:
    return (
        constants
        + linears @ point
        + 2 * np.einsum("i,eij,j->e", point, polars, point)
    ) % 3


def derive_structured_forms() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    _, _, _, constants, linears, polars = orbit2.exact_forms()
    q_constants = np.array(constants, dtype=np.int16) % 3
    q_linears = np.array(linears, dtype=np.int16) % 3
    q_polars = np.array(polars, dtype=np.int16) % 3
    return (
        np.array(
            [
                q_constants[index]
                + q_constants[index + 6]
                + q_constants[index + 12]
                for index in range(6)
            ],
            dtype=np.int16,
        )
        % 3,
        np.array(
            [
                q_linears[index]
                + q_linears[index + 6]
                + q_linears[index + 12]
                for index in range(6)
            ],
            dtype=np.int16,
        )
        % 3,
        np.array(
            [
                q_polars[index]
                + q_polars[index + 6]
                + q_polars[index + 12]
                for index in range(6)
            ],
            dtype=np.int16,
        )
        % 3,
    )


def verify() -> dict[str, object]:
    constants, linears, polars = derive_structured_forms()
    _, _, _, q_constants_raw, q_linears_raw, q_polars_raw = (
        orbit2.exact_forms()
    )
    q_constants = np.array(q_constants_raw, dtype=np.int16) % 3
    q_linears = np.array(q_linears_raw, dtype=np.int16) % 3
    q_polars = np.array(q_polars_raw, dtype=np.int16) % 3
    assert tuple(map(int, constants)) == (2, 0, 1, 2, 1, 0)
    assert digest(tuple(map(int, constants))) == EXPECTED_HASHES["constants"]
    assert digest(tuple(tuple(map(int, row)) for row in linears)) == (
        EXPECTED_HASHES["linears"]
    )
    assert digest(
        tuple(
            tuple(tuple(map(int, row)) for row in matrix)
            for matrix in polars
        )
    ) == EXPECTED_HASHES["polars"]

    rank_histogram: Counter[tuple[int, int]] = Counter()
    exceptions = []
    exception_counts: dict[tuple[int, ...], tuple[int, int, int]] = {}
    for coordinates in itertools.product(range(3), repeat=6):
        if not any(coordinates):
            continue
        coefficient = np.array(coordinates, dtype=np.int16)
        polar = np.einsum("e,eij->ij", coefficient, polars) % 3
        linear = np.einsum("e,ei->i", coefficient, linears) % 3
        polar_rank = rank_mod3(polar)
        augmented_rank = rank_mod3(np.column_stack((polar, linear)))
        rank_histogram[(polar_rank, augmented_rank)] += 1
        if augmented_rank == polar_rank:
            exceptions.append(coordinates)
            value_counts, replayed_rank, balanced = scalar_value_counts(
                int(coefficient @ constants % 3), linear, polar
            )
            assert replayed_rank == polar_rank
            assert not balanced
            exception_counts[coordinates] = value_counts
        else:
            assert augmented_rank == polar_rank + 1

    assert dict(rank_histogram) == EXPECTED_RANK_HISTOGRAM
    expected_exception_vectors = {
        representative
        for base in EXCEPTION_REPRESENTATIVES
        for representative in (
            base,
            tuple(2 * value % 3 for value in base),
        )
    }
    assert set(exceptions) == expected_exception_vectors
    assert all(coordinates[-1] for coordinates in exceptions)

    mean = 3**35
    expected_exception_counts = (
        (mean - 2 * 3**18, mean + 3**18, mean + 3**18),
        (mean - 3**19, mean, mean + 3**19),
        (mean - 2 * 3**18, mean + 3**18, mean + 3**18),
    )
    for representative, expected in zip(
        EXCEPTION_REPRESENTATIVES, expected_exception_counts
    ):
        assert exception_counts[representative] == expected
        negative = tuple(2 * value % 3 for value in representative)
        assert exception_counts[negative] == (
            expected[0],
            expected[2],
            expected[1],
        )

    # Fourier inversion.  A projective exceptional pair contributes
    # 3*N_t-3^36 to the fiber y, where t=<a,y>.
    fiber_sizes = []
    for target in itertools.product(range(3), repeat=6):
        numerator = 3**36
        for representative in EXCEPTION_REPRESENTATIVES:
            residue = sum(
                left * right
                for left, right in zip(representative, target)
            ) % 3
            numerator += (
                3 * exception_counts[representative][residue] - 3**36
            )
        assert numerator % 3**6 == 0
        fiber_sizes.append(numerator // 3**6)
    fiber_histogram = Counter(fiber_sizes)
    assert dict(fiber_histogram) == EXPECTED_FIBER_HISTOGRAM
    assert sum(fiber_sizes) == 3**36
    zero_fiber = fiber_sizes[0]
    assert zero_fiber == 3**30 - 7 * 3**13

    full_common_radical = nullspace_mod3(polars.reshape(-1, 36))
    assert full_common_radical.shape == (2, 36)
    assert rank_mod3(linears @ full_common_radical.T % 3) == 2

    # Construct a translation-equivariant parametrization for g_0,...,g_3.
    common_radical = nullspace_mod3(polars[:4].reshape(-1, 36))
    assert common_radical.shape == (7, 36)
    restriction = linears[:4] @ common_radical.T % 3
    assert rank_mod3(restriction) == 4
    direction_columns = []
    for coordinate in range(4):
        target = np.zeros(4, dtype=np.int16)
        target[coordinate] = 1
        coefficients = canonical_solution(restriction, target)
        direction_columns.append(coefficients @ common_radical % 3)
    directions = np.array(direction_columns, dtype=np.int16).T % 3
    assert digest(
        tuple(tuple(map(int, row)) for row in directions)
    ) == EXPECTED_HASHES["parametrization"]
    assert not np.any(
        np.einsum("eij,jk->eik", polars[:4], directions) % 3
    )
    assert np.array_equal(
        linears[:4] @ directions % 3, np.eye(4, dtype=np.int16)
    )
    _, gauge_coordinates = rref_mod3(directions.T)
    assert gauge_coordinates == (0, 2, 5, 9)

    # Directly replay the quadratic correction on a detached corpus.
    corpus = []
    free_coordinates = tuple(
        index for index in range(36) if index not in gauge_coordinates
    )
    for seed in range(81):
        point = np.array(
            [
                (seed * (index + 1) + index * index + 2 * index) % 3
                for index in range(36)
            ],
            dtype=np.int16,
        )
        point[list(gauge_coordinates)] = 0
        for digit, coordinate in enumerate(free_coordinates[:4]):
            point[coordinate] = seed // (3**digit) % 3
        corpus.append(point)
    assert len({tuple(map(int, point)) for point in corpus}) == 81
    for point in corpus:
        values = evaluate_vector(
            constants[:4], linears[:4], polars[:4], point
        )
        corrected = (point - directions @ values) % 3
        assert not np.any(
            evaluate_vector(
                constants[:4],
                linears[:4],
                polars[:4],
                corrected,
            )
        )

    prefix_zero_fibers = exact_prefix_zero_fibers(
        constants,
        linears,
        polars,
        q_constants,
        q_linears,
        q_polars,
    )
    certificate = json.loads(PREFIX_CERTIFICATE.read_text())
    assert certificate["schema"] == (
        "h668-h0-orbit2-exact-prefix-zero-fibers-v1"
    )
    assert certificate["status"] == "PASS"
    expected_prefixes = {
        int(entry["quadrics"]): int(entry["zero_fiber_size"])
        for entry in certificate["prefixes"]
    }
    assert prefix_zero_fibers == expected_prefixes
    for entry in certificate["prefixes"]:
        dimension = int(entry["quadrics"])
        expectation = 3 ** (36 - dimension)
        assert entry["random_map_expectation"] == expectation
        assert entry["difference"] == (
            int(entry["zero_fiber_size"]) - expectation
        )

    # All nonzero characters supported on the first five coordinates
    # vanished above, so every five-coordinate fiber has this exact size.
    five_coordinate_fiber = 3 ** (36 - 5)
    return {
        "structured_quadrics": 6,
        "nonzero_scalar_combinations": 728,
        "singular_polar_rank_range": [19, 34],
        "balanced_scalar_combinations": 722,
        "exceptional_projective_lines": 3,
        "uniform_first_five_fiber_size": five_coordinate_fiber,
        "six_coordinate_fiber_histogram": dict(
            sorted(EXPECTED_FIBER_HISTOGRAM.items())
        ),
        "zero_fiber_size": zero_fiber,
        "exact_prefix_zero_fibers": prefix_zero_fibers,
        "six_form_common_radical_dimension": 2,
        "first_four_common_radical_dimension": 7,
        "parametrized_zero_set_dimension": 32,
        "status": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
    print("PASS: orbit-2 character compression and parametrization replayed")
