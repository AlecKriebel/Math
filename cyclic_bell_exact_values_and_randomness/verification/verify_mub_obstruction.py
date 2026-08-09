#!/usr/bin/env python3
"""Independent finite hostile check of the computational-MUB proposition.

For each ``d=2,...,20`` and every computational vector ``e_r``, this script
constructs the real operator system

    F diag(x) F^* + R F diag(y) F^* R^*,   x,y in R^d,

directly from the Fourier matrices.  It solves, by standard-library Gaussian
elimination, the real nullspace imposing that ``e_r`` is an eigenvector.  It
then samples that nullspace with a fixed pseudorandom seed.

For every nonscalar admissible sample, a nonzero two-coordinate principal
compression of ``K-kappa I`` supplies explicit positive and negative Rayleigh
quotients.  Hence the spectrum of ``K`` lies on both sides of the stated
eigenvalue ``kappa``.  Endpoint nullspaces, for which the proposition predicts
only scalar operators, are checked separately.

This is finite floating-point regression evidence for the narrowly scoped
proposition.  It is not an all-dimensional proof and says nothing about joint
SOS certificates, different MUBs, different self-tests, or arbitrary
``(2,3,d,d)`` Bell functionals.
"""

from __future__ import annotations

import cmath
import math
import random


MAX_D = 20
SAMPLES_PER_INDEX = 8
SEED = 20260808
RREF_TOL = 2.0e-11
CHECK_TOL = 3.0e-8


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def fourier_operator_basis(d: int) -> list[list[list[complex]]]:
    """Return the ``2d`` Hermitian basis matrices for the displayed system."""
    omega = cmath.exp(2j * math.pi / d)
    rho = cmath.exp(1j * math.pi / d)
    basis: list[list[list[complex]]] = []

    for frequency in range(d):
        basis.append(
            [
                [omega ** ((j - k) * frequency) / d for k in range(d)]
                for j in range(d)
            ]
        )
    for frequency in range(d):
        basis.append(
            [
                [
                    rho ** (j - k) * omega ** ((j - k) * frequency) / d
                    for k in range(d)
                ]
                for j in range(d)
            ]
        )
    return basis


def eigenvector_constraint_matrix(
    basis: list[list[list[complex]]], r: int
) -> list[list[float]]:
    """Real linear constraints forcing every off-diagonal entry in column r to vanish."""
    d = len(basis[0])
    rows: list[list[float]] = []
    for j in range(d):
        if j == r:
            continue
        column = [matrix[j][r] for matrix in basis]
        rows.append([value.real for value in column])
        rows.append([value.imag for value in column])
    return rows


def real_nullspace(matrix: list[list[float]]) -> list[list[float]]:
    """Compute an RREF nullspace basis without third-party linear algebra."""
    rows = len(matrix)
    columns = len(matrix[0])
    work = [row[:] for row in matrix]
    pivot_columns: list[int] = []
    pivot_row = 0

    for column in range(columns):
        candidate = max(range(pivot_row, rows), key=lambda row: abs(work[row][column]))
        pivot = abs(work[candidate][column])
        if pivot <= RREF_TOL:
            continue
        work[pivot_row], work[candidate] = work[candidate], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [value / divisor for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            multiplier = work[row][column]
            if abs(multiplier) <= RREF_TOL:
                work[row][column] = 0.0
                continue
            work[row] = [
                left - multiplier * right
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break

    free_columns = [column for column in range(columns) if column not in pivot_columns]
    basis: list[list[float]] = []
    for free in free_columns:
        vector = [0.0] * columns
        vector[free] = 1.0
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -work[row][free]
        basis.append(vector)
    return basis


def constraint_residual(matrix: list[list[float]], vector: list[float]) -> float:
    return max(
        abs(sum(value * coefficient for value, coefficient in zip(row, vector)))
        for row in matrix
    )


def combine_nullspace(
    nullspace: list[list[float]], coefficients: list[float]
) -> list[float]:
    return [
        sum(weight * vector[column] for weight, vector in zip(coefficients, nullspace))
        for column in range(len(nullspace[0]))
    ]


def operator_from_parameters(
    basis: list[list[list[complex]]], parameters: list[float]
) -> list[list[complex]]:
    d = len(basis[0])
    return [
        [
            sum(parameters[index] * basis[index][j][k] for index in range(len(basis)))
            for k in range(d)
        ]
        for j in range(d)
    ]


def rayleigh(matrix: list[list[complex]], vector: list[complex]) -> complex:
    return sum(
        vector[j].conjugate() * matrix[j][k] * vector[k]
        for j in range(len(vector))
        for k in range(len(vector))
    )


def audit_sample(
    matrix: list[list[complex]], d: int, r: int
) -> tuple[bool, float, float]:
    """Return ``(is_scalar, positive_witness, negative_witness)``."""
    scale = max(1.0, max(abs(entry) for row in matrix for entry in row))
    tolerance = CHECK_TOL * scale

    hermitian_error = max(
        abs(matrix[j][k] - matrix[k][j].conjugate())
        for j in range(d)
        for k in range(d)
    )
    require(hermitian_error <= tolerance, f"non-Hermitian sample at d={d}, r={r}")

    kappa = matrix[r][r].real
    require(
        abs(matrix[r][r].imag) <= tolerance,
        f"nonreal stated eigenvalue at d={d}, r={r}",
    )
    column_error = max(abs(matrix[j][r]) for j in range(d) if j != r)
    require(column_error <= tolerance, f"e_r is not an eigenvector at d={d}, r={r}")

    shifted = [
        [matrix[j][k] - (kappa if j == k else 0.0) for k in range(d)]
        for j in range(d)
    ]
    diagonal_error = max(abs(shifted[j][j]) for j in range(d))
    require(
        diagonal_error <= tolerance,
        f"operator-system diagonal is not constant at d={d}, r={r}",
    )

    s = min(r, d - 1 - r)
    corner_error = 0.0
    for j in range(d):
        for k in range(d):
            in_corner = (j < s and k >= d - s) or (k < s and j >= d - s)
            if j != k and not in_corner:
                corner_error = max(corner_error, abs(shifted[j][k]))
    require(
        corner_error <= tolerance,
        f"admissible nullspace sample leaks outside corner blocks at d={d}, r={r}",
    )

    off_diagonal = [
        (abs(shifted[j][k]), j, k)
        for j in range(d)
        for k in range(j + 1, d)
    ]
    magnitude, j, k = max(off_diagonal)
    if magnitude <= tolerance:
        scalar_error = max(abs(entry) for row in shifted for entry in row)
        require(scalar_error <= tolerance, f"undetected nonscalar sample at d={d}, r={r}")
        return True, 0.0, 0.0

    z = shifted[j][k]
    phase = z.conjugate() / abs(z)
    normalization = 1.0 / math.sqrt(2.0)
    positive_vector = [0j] * d
    negative_vector = [0j] * d
    positive_vector[j] = normalization
    positive_vector[k] = phase * normalization
    negative_vector[j] = normalization
    negative_vector[k] = -phase * normalization
    positive = rayleigh(shifted, positive_vector)
    negative = rayleigh(shifted, negative_vector)
    require(abs(positive.imag) <= tolerance, f"complex positive Rayleigh value at d={d}, r={r}")
    require(abs(negative.imag) <= tolerance, f"complex negative Rayleigh value at d={d}, r={r}")
    require(
        positive.real > tolerance and negative.real < -tolerance,
        f"spectrum not witnessed on both sides of kappa at d={d}, r={r}",
    )
    require(
        abs(positive.real - magnitude) <= 3.0 * tolerance
        and abs(negative.real + magnitude) <= 3.0 * tolerance,
        f"incorrect two-coordinate Rayleigh witnesses at d={d}, r={r}",
    )
    return False, positive.real, negative.real


def main() -> None:
    rng = random.Random(SEED)
    indices_checked = 0
    samples_checked = 0
    nonscalar_samples = 0
    smallest_positive = math.inf
    largest_negative = -math.inf

    for d in range(2, MAX_D + 1):
        operator_basis = fourier_operator_basis(d)
        for r in range(d):
            constraints = eigenvector_constraint_matrix(operator_basis, r)
            nullspace = real_nullspace(constraints)
            s = min(r, d - 1 - r)
            expected_nullity = 2 + 2 * s
            require(
                len(nullspace) == expected_nullity,
                f"unexpected nullity at d={d}, r={r}: "
                f"got {len(nullspace)}, expected {expected_nullity}",
            )
            for vector in nullspace:
                require(
                    constraint_residual(constraints, vector) <= 5.0e-9,
                    f"RREF nullspace residual at d={d}, r={r}",
                )

            accepted = 0
            attempts = 0
            while accepted < SAMPLES_PER_INDEX and attempts < 8 * SAMPLES_PER_INDEX:
                attempts += 1
                weights = [rng.uniform(-1.0, 1.0) for _ in nullspace]
                parameters = combine_nullspace(nullspace, weights)
                matrix = operator_from_parameters(operator_basis, parameters)
                is_scalar, positive, negative = audit_sample(matrix, d, r)

                if s == 0:
                    require(is_scalar, f"endpoint admits a nonscalar sample at d={d}, r={r}")
                elif is_scalar:
                    # A chance cancellation is admissible but gives no hostile
                    # spectral test, so draw another deterministic sample.
                    continue
                else:
                    nonscalar_samples += 1
                    smallest_positive = min(smallest_positive, positive)
                    largest_negative = max(largest_negative, negative)
                accepted += 1
                samples_checked += 1

            require(
                accepted == SAMPLES_PER_INDEX,
                f"could not obtain enough admissible samples at d={d}, r={r}",
            )
            indices_checked += 1

    require(nonscalar_samples > 0, "no nonscalar samples were exercised")
    require(smallest_positive > 0.0, "no positive Rayleigh witness")
    require(largest_negative < 0.0, "no negative Rayleigh witness")
    print("PASS: narrowly scoped computational-MUB obstruction hostile check")
    print(f"  dimensions: d=2,...,{MAX_D}")
    print(f"  computational indices checked: {indices_checked}")
    print(f"  random admissible nullspace samples: {samples_checked}")
    print(f"  nonscalar samples with two-sided spectral witnesses: {nonscalar_samples}")
    print(f"  deterministic random seed: {SEED}")


if __name__ == "__main__":
    main()
