#!/usr/bin/env python3
"""Exact audit of the full Choi-transfer and exterior determinant identities."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, permutations

G = tuple[F, F]
Z: G = (F(0), F(0))
O: G = (F(1), F(0))
I: G = (F(0), F(1))


def g(re: int | F = 0, im: int | F = 0) -> G:
    return (F(re), F(im))


def add(x: G, y: G) -> G:
    return (x[0] + y[0], x[1] + y[1])


def neg(x: G) -> G:
    return (-x[0], -x[1])


def sub(x: G, y: G) -> G:
    return add(x, neg(y))


def mul(x: G, y: G) -> G:
    return (
        x[0] * y[0] - x[1] * y[1],
        x[0] * y[1] + x[1] * y[0],
    )


def conj(x: G) -> G:
    return (x[0], -x[1])


def sum_g(values) -> G:
    out = Z
    for value in values:
        out = add(out, value)
    return out


def product(values) -> G:
    out = O
    for value in values:
        out = mul(out, value)
    return out


def dagger(a: list[list[G]]) -> list[list[G]]:
    return [
        [conj(a[j][i]) for j in range(len(a))]
        for i in range(len(a[0]))
    ]


def matmul(a: list[list[G]], b: list[list[G]]) -> list[list[G]]:
    return [
        [
            sum_g(mul(a[i][k], b[k][j]) for k in range(len(b)))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def trace(a: list[list[G]]) -> G:
    return sum_g(a[i][i] for i in range(len(a)))


def sign(p: tuple[int, ...]) -> int:
    inversions = sum(
        p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))
    )
    return -1 if inversions % 2 else 1


def determinant(a: list[list[G]]) -> G:
    n = len(a)
    terms = []
    for p in permutations(range(n)):
        value = product(a[i][p[i]] for i in range(n))
        terms.append(value if sign(p) == 1 else neg(value))
    return sum_g(terms)


def adjugate2(a: list[list[G]]) -> list[list[G]]:
    return [
        [a[1][1], neg(a[0][1])],
        [neg(a[1][0]), a[0][0]],
    ]


def block(a, b, c, d):
    return [
        a[0] + b[0],
        a[1] + b[1],
        c[0] + d[0],
        c[1] + d[1],
    ]


def coefficients(r: list[list[G]]) -> list[G]:
    """Coefficients in R = r0 I + r1 X + r2 Y + r3 Z."""
    return [
        mul(g(F(1, 2)), add(r[0][0], r[1][1])),
        mul(g(F(1, 2)), add(r[0][1], r[1][0])),
        mul(g(0, F(-1, 2)), sub(r[1][0], r[0][1])),
        mul(g(F(1, 2)), sub(r[0][0], r[1][1])),
    ]


def minor(a: list[list[G]], rows: tuple[int, ...]) -> G:
    return determinant([[a[row][column] for column in range(4)] for row in rows])


# Section 1: Choi-transfer identity for a genuinely complex exact K.
a = [[g(4), g(F(1, 3), F(1, 5))],
     [g(F(1, 3), F(-1, 5)), g(5)]]
d = [[g(3), g(F(-1, 4), F(1, 6))],
     [g(F(-1, 4), F(-1, 6)), g(6)]]
b = [[g(F(1, 7), F(1, 8)), g(F(1, 9), F(-1, 10))],
     [g(F(-1, 11), F(1, 12)), g(F(1, 13), F(1, 14))]]

k = block(a, b, dagger(b), d)
kgamma = block(a, dagger(b), b, d)
h = [[mul(g(F(1, 2)), add(b[i][j], dagger(b)[i][j]))
      for j in range(2)] for i in range(2)]
q = [[mul(g(0, F(-1, 2)), sub(b[i][j], dagger(b)[i][j]))
      for j in range(2)] for i in range(2)]
assert b == [[add(h[i][j], mul(I, q[i][j])) for j in range(2)]
             for i in range(2)]

# Transfer columns are coefficients of Lambda(I), Lambda(X),
# Lambda(Y), Lambda(Z).
outputs = [
    [[add(a[i][j], d[i][j]) for j in range(2)] for i in range(2)],
    [[mul(g(2), h[i][j]) for j in range(2)] for i in range(2)],
    [[mul(g(2), q[i][j]) for j in range(2)] for i in range(2)],
    [[sub(a[i][j], d[i][j]) for j in range(2)] for i in range(2)],
]
transfer_columns = [coefficients(output) for output in outputs]
transfer = [
    [transfer_columns[column][row] for column in range(4)]
    for row in range(4)
]
assert determinant(kgamma) == sub(determinant(k), determinant(transfer))

# The Pauli-row orientation form gives det(T) = -8 Delta.
orientation_rows = [coefficients(matrix) for matrix in (a, d, h, q)]
assert determinant(transfer) == mul(g(-8), determinant(orientation_rows))
oriented_trace = trace(
    matmul(adjugate2(d), matmul(q, matmul(adjugate2(a), h)))
)
assert oriented_trace[1] == mul(g(2), determinant(orientation_rows))[0]
assert sub(determinant(kgamma), determinant(k)) == g(4 * oriented_trace[1])


# Section 2: exact Cauchy--Binet / fourth-exterior pairing.
# These rational 6x4 matrices stand in for two code embeddings, and
# the diagonal entries stand in for physical superoperator eigenvalues.
left = [
    [g(1), g(0), g(1), g(-1)],
    [g(0), g(1), g(1), g(2)],
    [g(1), g(1), g(0), g(1)],
    [g(2), g(-1), g(1), g(0)],
    [g(1), g(2), g(-1), g(1)],
    [g(-1), g(1), g(2), g(1)],
]
right = [
    [g(1), g(1), g(0), g(2)],
    [g(2), g(0), g(1), g(-1)],
    [g(0), g(1), g(2), g(1)],
    [g(1), g(-1), g(1), g(1)],
    [g(2), g(1), g(-1), g(0)],
    [g(1), g(2), g(1), g(-1)],
]
eigenvalues = [g(2), g(-3), g(5), g(1), g(-2), g(4)]
weighted_left = [
    [mul(eigenvalues[row], value) for value in left[row]]
    for row in range(6)
]
compressed = matmul(dagger(right), weighted_left)
exterior_pairing = sum_g(
    mul(
        product(eigenvalues[row] for row in rows),
        mul(conj(minor(right, rows)), minor(left, rows)),
    )
    for rows in combinations(range(6), 4)
)
assert determinant(compressed) == exterior_pairing


# Section 3: Gram determinant equals a sum of squared four-minors.
phi = [
    [g(1), g(0), g(2), g(-1)],
    [g(0), g(1), g(1), g(1)],
    [g(1), g(-1), g(0), g(2)],
    [g(2), g(1), g(-1), g(0)],
    [g(-1), g(2), g(1), g(1)],
    [g(1), g(1), g(2), g(-2)],
]
gram = matmul(dagger(phi), phi)
minor_square_sum = sum_g(
    mul(conj(minor(phi, rows)), minor(phi, rows))
    for rows in combinations(range(6), 4)
)
assert determinant(gram) == minor_square_sum

print(
    "verified Choi-transfer determinant, Pauli orientation, paired "
    "fourth-exterior Cauchy--Binet, and Gram-volume identities"
)
