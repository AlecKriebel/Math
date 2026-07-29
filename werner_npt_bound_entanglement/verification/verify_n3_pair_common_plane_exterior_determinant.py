#!/usr/bin/env python3
"""Exact checks for the exterior determinant common-plane reduction."""

from fractions import Fraction as F
from itertools import combinations


def determinant(a):
    a = [row[:] for row in a]
    out = F(1)
    n = len(a)
    for col in range(n):
        pivot = next((row for row in range(col, n) if a[row][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            out = -out
        value = a[col][col]
        out *= value
        for j in range(col, n):
            a[col][j] /= value
        for row in range(col + 1, n):
            value = a[row][col]
            for j in range(col, n):
                a[row][j] -= value * a[col][j]
    return out


# First four columns of the Sylvester Hadamard matrix, divided by sqrt(8).
# We retain the integer signs and insert the normalization algebraically.
hadamard = [[F(1)]]
for _ in range(3):
    old = hadamard
    hadamard = (
        [row + row for row in old]
        + [row + [-x for x in row] for row in old]
    )
w = [row[:4] for row in hadamard]
assert all(
    sum((w[row][i] * w[row][j] for row in range(8)), F(0))
    == (8 if i == j else 0)
    for i in range(4) for j in range(4)
)

# Two basis directions in each of the four physical sectors.
sector = [0, 0, 1, 1, 2, 2, 3, 3]
d = [F(1), F(-1), F(0), F(4)]

# Sector traces r_k=Tr(W^*P_kW), where normalized W is w/sqrt(8).
r = [
    sum(
        (w[row][col] ** 2 for row in range(8) if sector[row] == k
         for col in range(4)),
        F(0),
    ) / 8
    for k in range(4)
]
s = (r[1] - r[2] + 3 * r[3]) / 2

# Exterior occupation masses from squared four-by-four row minors.
masses = {}
for rows in combinations(range(8), 4):
    nu = tuple(sum(sector[row] == k for row in rows) for k in range(4))
    minor = determinant([[w[row][col] for col in range(4)] for row in rows])
    masses[nu] = masses.get(nu, F(0)) + minor * minor / (8 ** 4)

assert sum(masses.values(), F(0)) == 1
for k in range(4):
    assert sum((nu[k] * mass for nu, mass in masses.items()), F(0)) == r[k]
assert s == sum(
    ((nu[1] - nu[2] + 3 * nu[3]) * mass / 2
     for nu, mass in masses.items()),
    F(0),
)

# Direct four-by-four compression W^*(D+sI)W.
compressed = [
    [
        sum(
            (w[row][i] * (d[sector[row]] + s) * w[row][j]
             for row in range(8)),
            F(0),
        ) / 8
        for j in range(4)
    ]
    for i in range(4)
]
direct_det = determinant(compressed)
exterior_det = sum(
    (
        mass
        * (1 + s) ** nu[0]
        * (s - 1) ** nu[1]
        * s ** nu[2]
        * (s + 4) ** nu[3]
        for nu, mass in masses.items()
    ),
    F(0),
)
assert direct_det == exterior_det

# Exact block-positive relaxed obstruction.
s_relaxed = F(1, 2)
eigenvalues = [s_relaxed - 1] + [s_relaxed + 1] * 3
assert eigenvalues == [F(-1, 2), F(3, 2), F(3, 2), F(3, 2)]
assert determinant([[eigenvalues[i] if i == j else F(0)
                     for j in range(4)] for i in range(4)]) == F(-27, 16)

# Product-vector block positivity of I-2|Phi><Phi| reduces to
# |x_0 y_0+x_1 y_1|^2 <= ||x||^2 ||y||^2.
tests = [
    ((F(1), F(0)), (F(1), F(0))),
    ((F(1), F(1)), (F(1), F(-1))),
    ((F(2), F(-3)), (F(4), F(5))),
]
for x, y in tests:
    overlap = x[0] * y[0] + x[1] * y[1]
    assert overlap * overlap <= sum(a * a for a in x) * sum(b * b for b in y)

print("all exact exterior-determinant checks passed")
