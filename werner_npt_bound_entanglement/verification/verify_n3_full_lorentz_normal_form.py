#!/usr/bin/env python3
"""Dependency-free exact checks for the logical Bell-normal reduction."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations, product

G = tuple[F, F]
ZERO: G = (F(0), F(0))
ONE: G = (F(1), F(0))


def g(real: int | F = 0, imag: int | F = 0) -> G:
    return (F(real), F(imag))


def add(x: G, y: G) -> G:
    return (x[0] + y[0], x[1] + y[1])


def neg(x: G) -> G:
    return (-x[0], -x[1])


def mul(x: G, y: G) -> G:
    return (
        x[0] * y[0] - x[1] * y[1],
        x[0] * y[1] + x[1] * y[0],
    )


def conj(x: G) -> G:
    return (x[0], -x[1])


def sum_g(values) -> G:
    result = ZERO
    for value in values:
        result = add(result, value)
    return result


def product_g(values) -> G:
    result = ONE
    for value in values:
        result = mul(result, value)
    return result


def matrix_add(*matrices: list[list[G]]) -> list[list[G]]:
    return [
        [sum_g(matrix[i][j] for matrix in matrices)
         for j in range(len(matrices[0][0]))]
        for i in range(len(matrices[0]))
    ]


def matrix_scale(value: G, matrix: list[list[G]]) -> list[list[G]]:
    return [[mul(value, entry) for entry in row] for row in matrix]


def matrix_multiply(
    left: list[list[G]], right: list[list[G]]
) -> list[list[G]]:
    return [
        [
            sum_g(
                mul(left[i][k], right[k][j])
                for k in range(len(right))
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def dagger(matrix: list[list[G]]) -> list[list[G]]:
    return [
        [conj(matrix[j][i]) for j in range(len(matrix))]
        for i in range(len(matrix[0]))
    ]


def kronecker(
    left: list[list[G]], right: list[list[G]]
) -> list[list[G]]:
    return [
        [
            mul(
                left[i // len(right)][j // len(right[0])],
                right[i % len(right)][j % len(right[0])],
            )
            for j in range(len(left[0]) * len(right[0]))
        ]
        for i in range(len(left) * len(right))
    ]


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix: list[list[G]]) -> G:
    size = len(matrix)
    terms = []
    for permutation in permutations(range(size)):
        term = product_g(
            matrix[i][permutation[i]] for i in range(size)
        )
        terms.append(term if permutation_sign(permutation) == 1 else neg(term))
    return sum_g(terms)


def partial_transpose_second(matrix: list[list[G]]) -> list[list[G]]:
    """Partial transpose in the second factor of a 2 x 2 system."""
    result = [[ZERO for _ in range(4)] for _ in range(4)]
    for a, b, c, d in product(range(2), repeat=4):
        result[2 * a + d][2 * c + b] = matrix[2 * a + b][2 * c + d]
    return result


def bell_operator(t1: F, t2: F, t3: F) -> list[list[G]]:
    identity = [[ONE, ZERO], [ZERO, ONE]]
    pauli_x = [[ZERO, ONE], [ONE, ZERO]]
    pauli_y = [[ZERO, g(0, -1)], [g(0, 1), ZERO]]
    pauli_z = [[ONE, ZERO], [ZERO, neg(ONE)]]
    return matrix_scale(
        g(F(1, 4)),
        matrix_add(
            kronecker(identity, identity),
            matrix_scale(g(t1), kronecker(pauli_x, pauli_x)),
            matrix_scale(g(t2), kronecker(pauli_y, pauli_y)),
            matrix_scale(g(t3), kronecker(pauli_z, pauli_z)),
        ),
    )


def sign_values(t1: F, t2: F, t3: F, sign_product: int) -> list[F]:
    return [
        F(1) + e1 * t1 + e2 * t2 + e3 * t3
        for e1, e2, e3 in product((-1, 1), repeat=3)
        if e1 * e2 * e3 == sign_product
    ]


# A strict rational PPT point checks every determinant formula.
t1, t2, t3 = F(1, 5), F(-1, 4), F(1, 6)
k = bell_operator(t1, t2, t3)
k_partial_transpose = partial_transpose_second(k)
ordinary_factors = sign_values(t1, t2, t3, -1)
partial_transpose_factors = sign_values(t1, t2, t3, 1)
assert determinant(k) == mul(
    g(F(1, 4**4)), product_g(g(value) for value in ordinary_factors)
)
assert determinant(k_partial_transpose) == g(
    product_g(g(value) for value in partial_transpose_factors)[0] / 4**4
)
det_transfer = -t1 * t2 * t3 / 16
assert determinant(k_partial_transpose) == add(
    determinant(k), g(-det_transfer)
)

# The eight Bell inequalities are exactly the trace-norm octahedron.
all_factors = ordinary_factors + partial_transpose_factors
assert min(all_factors) == F(1) - abs(t1) - abs(t2) - abs(t3)
spatial_nuclear_norm = (abs(t1) + abs(t2) + abs(t3)) / 2
assert spatial_nuclear_norm <= F(1, 2)

# Positivity of K alone is strictly weaker: this Bell-diagonal point is NPT.
u1, u2, u3 = F(1, 2), F(-1, 2), F(1, 2)
assert min(sign_values(u1, u2, u3, -1)) > 0
assert min(sign_values(u1, u2, u3, 1)) < 0
assert (abs(u1) + abs(u2) + abs(u3)) / 2 > F(1, 2)

# Local determinant scaling is audited on non-unit diagonal filters.
r = [[g(2), ZERO], [ZERO, g(3)]]
s = [[g(5), ZERO], [ZERO, g(7)]]
local_filter = kronecker(r, s)
filtered = matrix_multiply(
    local_filter, matrix_multiply(k, dagger(local_filter))
)
filtered_partial_transpose = partial_transpose_second(filtered)
scale = F(2 * 3) ** 4 * F(5 * 7) ** 4
assert determinant(filtered) == g(scale * determinant(k)[0])
assert determinant(filtered_partial_transpose) == g(
    scale * determinant(k_partial_transpose)[0]
)

print(
    "verified exact Bell eigenvalues, partial-transpose determinant, "
    "octahedral trace-norm frontier, and local-filter scaling"
)
