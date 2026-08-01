#!/usr/bin/env python3
"""Dependency-free exact matrix checks for a rational DTH certificate.

The final constrained five-replica certificate is block diagonal after the
local Schur--Weyl reduction.  Its nonzero holomorphic blocks have size at
most 16 and its mixed product-face coordinate blocks have size at most 53.
This module supplies the small exact-linear-algebra primitives needed by the
final verifier.  It intentionally uses only Python integers and
``fractions.Fraction``.

The key positivity test is fraction-free symmetric elimination.  After one
positive common denominator is cleared, the successive Bareiss pivots are
the leading principal minors.  Sylvester's criterion therefore gives a
short exact positive-definiteness certificate without symbolic eigenvalues.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from random import Random


def lcm(a: int, b: int) -> int:
    """Return the nonnegative least common multiple of two integers."""
    if not a or not b:
        return 0
    return abs(a // gcd(a, b) * b)


def as_rows(matrix):
    """Convert a matrix-like object to nested rows without importing it."""
    if hasattr(matrix, "tolist"):
        matrix = matrix.tolist()
    return [list(row) for row in matrix]


def check_square_symmetric(matrix) -> int:
    """Check that ``matrix`` is square and symmetric; return its size."""
    matrix = as_rows(matrix)
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("matrix is not square")
    for i in range(n):
        for j in range(i):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError(f"matrix is not symmetric at ({i},{j})")
    return n


def clear_denominators(matrix):
    """Return ``(integer_matrix, positive_denominator)`` exactly."""
    matrix = as_rows(matrix)
    n = check_square_symmetric(matrix)
    denominator = 1
    rational = []
    for row in matrix:
        rational_row = []
        for value in row:
            value = Fraction(value)
            denominator = lcm(denominator, value.denominator)
            rational_row.append(value)
        rational.append(rational_row)
    integer = [
        [value.numerator * (denominator // value.denominator)
         for value in row]
        for row in rational
    ]
    assert denominator > 0
    assert len(integer) == n
    return integer, denominator


def bareiss_leading_minors(integer_matrix):
    """Return all leading principal minors using exact Bareiss elimination.

    No pivoting is performed: positive definiteness is equivalent to every
    leading principal minor being positive, so a zero or negative pivot is a
    valid failure rather than a reason to exchange rows.  Exact divisibility
    of every update is checked explicitly.
    """
    integer_matrix = as_rows(integer_matrix)
    n = check_square_symmetric(integer_matrix)
    if n == 0:
        return []
    work = [[int(value) for value in row] for row in integer_matrix]
    previous = 1
    minors = []
    for k in range(n - 1):
        pivot = work[k][k]
        minors.append(pivot)
        if pivot == 0:
            # Subsequent fraction-free updates would divide by zero.  The
            # recorded zero already disproves strict positive definiteness.
            return minors
        for i in range(k + 1, n):
            for j in range(i, n):
                numerator = pivot * work[i][j] - work[i][k] * work[k][j]
                quotient, remainder = divmod(numerator, previous)
                if remainder:
                    raise ArithmeticError(
                        f"non-exact Bareiss division at ({i},{j}), step {k}")
                work[i][j] = quotient
                work[j][i] = quotient
        previous = pivot
    minors.append(work[n - 1][n - 1])
    return minors


def assert_positive_definite(matrix):
    """Prove positive definiteness exactly and return diagnostic metadata."""
    integer, denominator = clear_denominators(matrix)
    minors = bareiss_leading_minors(integer)
    if len(minors) != len(integer) or any(value <= 0 for value in minors):
        first = next((i for i, value in enumerate(minors) if value <= 0),
                     len(minors))
        raise AssertionError(
            f"matrix is not certified positive definite; first bad "
            f"leading minor index {first}")
    return {
        "dimension": len(integer),
        "denominator": denominator,
        "minor_signs": tuple(1 for _ in minors),
        "last_minor": minors[-1] if minors else 1,
    }


def assert_pd_by_diagonal_dominance(matrix, transform, triangular=False):
    """Prove ``matrix`` positive definite by an exact rational congruence.

    A certificate generator may round an inverse Cholesky factor to a small
    rational matrix ``transform``.  This verifier computes

    ``transform^T * matrix * transform``

    exactly and requires it to be strictly row-diagonally dominant with
    positive diagonal.  Symmetric Gershgorin then makes the congruent matrix
    positive definite.  Invertibility of the transform is checked either
    from its triangular diagonal or by exact elimination.
    """
    matrix = as_rows(matrix)
    transform = as_rows(transform)
    n = check_square_symmetric(matrix)
    if len(transform) != n or any(len(row) != n for row in transform):
        raise ValueError("congruence transform has the wrong shape")
    rational_transform = [[Fraction(value) for value in row]
                          for row in transform]
    if triangular:
        upper = all(rational_transform[i][j] == 0
                    for i in range(n) for j in range(i))
        lower = all(rational_transform[i][j] == 0
                    for i in range(n) for j in range(i + 1, n))
        if not (upper or lower):
            raise AssertionError("claimed transform is not triangular")
        if any(rational_transform[i][i] == 0 for i in range(n)):
            raise AssertionError("triangular transform is singular")
    else:
        # Exact inversion is only a nonsingularity audit; the inverse itself
        # is not used in the positivity argument.
        inverse(rational_transform)
    transformed = matmul(
        transpose(rational_transform),
        matmul([[Fraction(value) for value in row] for row in matrix],
               rational_transform),
    )
    margins = []
    for i, row in enumerate(transformed):
        if row[i] <= 0:
            raise AssertionError(f"nonpositive congruent diagonal at row {i}")
        radius = sum(abs(value) for j, value in enumerate(row) if j != i)
        margin = row[i] - radius
        if margin <= 0:
            raise AssertionError(
                f"congruent matrix is not strictly diagonally dominant at "
                f"row {i}")
        margins.append(margin)
    transform_norm_squared = sum(
        abs(value) ** 2 for row in rational_transform for value in row
    )
    lower_bound = min(margins, default=Fraction(1)) / transform_norm_squared
    return {
        "dimension": n,
        "minimum_margin": min(margins, default=Fraction(1)),
        # If B=R^T A R has B >= margin*I, then
        # A >= margin/||R||_2^2 I >= margin/||R||_F^2 I.
        "matrix_lower_bound": lower_bound,
    }


def assert_pd_near_reference(candidate, reference, transform,
                             triangular=False):
    """Prove PD by an exact Frobenius perturbation from a reference.

    This is useful when ``candidate`` has determinant-sized rational
    denominators from the 334-dimensional exact correction.  The small-
    denominator dyadic ``reference`` is certified once by congruence, and
    Weyl's inequality transfers positivity using only quadratic-many exact
    operations on the large candidate entries.
    """
    candidate = as_rows(candidate)
    reference = as_rows(reference)
    if len(candidate) != len(reference) or any(
            len(a) != len(b) for a, b in zip(candidate, reference)):
        raise ValueError("candidate and reference shapes differ")
    result = assert_pd_by_diagonal_dominance(
        reference, transform, triangular=triangular
    )
    difference_squared = sum(
        (Fraction(a) - Fraction(b)) ** 2
        for candidate_row, reference_row in zip(candidate, reference)
        for a, b in zip(candidate_row, reference_row)
    )
    lower = result["matrix_lower_bound"]
    if difference_squared >= lower ** 2:
        raise AssertionError(
            "candidate perturbation is not smaller than the certified "
            "reference spectral gap"
        )
    result = dict(result)
    result["difference_frobenius_squared"] = difference_squared
    return result


def transpose(matrix):
    return [list(row) for row in zip(*as_rows(matrix))]


def matmul(left, right):
    left = as_rows(left)
    right = as_rows(right)
    if not left:
        return []
    if len(left[0]) != len(right):
        raise ValueError("incompatible matrix dimensions")
    columns = transpose(right)
    return [[sum(a * b for a, b in zip(row, column))
             for column in columns] for row in left]


def congruence(basis, coordinate):
    """Compute ``basis * coordinate * basis^T`` exactly."""
    return matmul(matmul(basis, coordinate), transpose(basis))


def assert_equal_matrix(left, right):
    left = as_rows(left)
    right = as_rows(right)
    if len(left) != len(right) or any(
            len(a) != len(b) for a, b in zip(left, right)):
        raise AssertionError("matrix shapes differ")
    for i, (a, b) in enumerate(zip(left, right)):
        for j, (x, y) in enumerate(zip(a, b)):
            if x != y:
                raise AssertionError(f"matrix mismatch at ({i},{j})")


def inverse(matrix):
    """Invert a small rational square matrix by exact Gauss--Jordan."""
    matrix = as_rows(matrix)
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("matrix is not square")
    augmented = [
        [Fraction(value) for value in row]
        + [Fraction(int(i == j)) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot = next((row for row in range(column, n)
                      if augmented[row][column]), None)
        if pivot is None:
            raise ValueError("matrix is singular")
        augmented[column], augmented[pivot] = (
            augmented[pivot], augmented[column])
        scale = augmented[column][column]
        augmented[column] = [value / scale
                             for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    value - scale * pivot_value
                    for value, pivot_value in zip(
                        augmented[row], augmented[column])
                ]
    return [row[n:] for row in augmented]


def recover_coordinate(full_matrix, basis, pivot_rows):
    """Recover ``A`` from ``full_matrix = basis A basis^T`` exactly.

    ``pivot_rows`` selects a square nonsingular row submatrix of ``basis``.
    The caller should subsequently use :func:`assert_equal_matrix` on the
    full congruence, so the pivot recovery itself is not trusted as a support
    check.
    """
    full_matrix = as_rows(full_matrix)
    basis = as_rows(basis)
    rank = len(basis[0]) if basis else 0
    if len(pivot_rows) != rank or len(set(pivot_rows)) != rank:
        raise ValueError("pivot row list has the wrong size")
    pivot_basis = [[Fraction(basis[i][j]) for j in range(rank)]
                   for i in pivot_rows]
    pivot_matrix = [[Fraction(full_matrix[i][j]) for j in pivot_rows]
                    for i in pivot_rows]
    inv = inverse(pivot_basis)
    return matmul(matmul(inv, pivot_matrix), transpose(inv))


def _self_test():
    rng = Random(20260801)
    for n in range(1, 9):
        lower = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1):
                lower[i][j] = rng.randrange(-5, 6)
            lower[i][i] += 9
        matrix = matmul(lower, transpose(lower))
        result = assert_positive_definite(matrix)
        assert result["dimension"] == n
        diagonal_result = assert_pd_by_diagonal_dominance(
            matrix, inverse(transpose(lower)), triangular=True)
        assert diagonal_result["minimum_margin"] > 0
        perturbed = [row[:] for row in matrix]
        perturbed[0][0] += Fraction(1, 10**6)
        near_result = assert_pd_near_reference(
            perturbed, matrix, inverse(transpose(lower)), triangular=True
        )
        assert near_result["difference_frobenius_squared"] > 0

        # Exercise rational range recovery in a tall, nonorthogonal basis.
        basis = [[Fraction(rng.randrange(-4, 5), rng.randrange(1, 5))
                  for _ in range(n)] for _ in range(n + 3)]
        for i in range(n):
            basis[i][i] += 7
        full = congruence(basis, matrix)
        recovered = recover_coordinate(full, basis, list(range(n)))
        assert_equal_matrix(recovered, matrix)
        assert_equal_matrix(congruence(basis, recovered), full)

    indefinite = [[1, 2], [2, 1]]
    try:
        assert_positive_definite(indefinite)
    except AssertionError:
        pass
    else:
        raise AssertionError("indefinite self-test matrix was accepted")
    print("exact DTH matrix primitives passed")


if __name__ == "__main__":
    _self_test()
