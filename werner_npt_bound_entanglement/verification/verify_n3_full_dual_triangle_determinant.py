#!/usr/bin/env python3
"""Dependency-free exact checks for the full-dual triangle determinant."""

from fractions import Fraction as F
from itertools import permutations


def z(real=0, imag=0):
    return (F(real), F(imag))


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[0], -x[1])


def mul(x, y):
    return (x[0] * y[0] - x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


def conj(x):
    return (x[0], -x[1])


def scale(a, x):
    return (a * x[0], a * x[1])


def abs2(x):
    return x[0] * x[0] + x[1] * x[1]


def determinant(matrix):
    answer = z()
    for p in permutations(range(3)):
        inversions = sum(
            p[i] > p[j] for i in range(3) for j in range(i + 1, 3)
        )
        term = z(1)
        for i in range(3):
            term = mul(term, matrix[i][p[i]])
        answer = add(answer, neg(term) if inversions % 2 else term)
    return answer


d1, d2, d3 = F(5, 3), F(7, 4), F(11, 6)
c12 = z(F(1, 3), F(2, 5))
c13 = z(F(-2, 7), F(1, 4))
c23 = z(F(3, 8), F(-1, 6))

G = [
    [z(d1), neg(c12), neg(c13)],
    [neg(conj(c12)), z(d2), neg(c23)],
    [neg(conj(c13)), neg(conj(c23)), z(d3)],
]

cycle = mul(mul(c12, c23), conj(c13))
closed = (
    d1 * d2 * d3
    - d1 * abs2(c23)
    - d2 * abs2(c13)
    - d3 * abs2(c12)
    - 2 * cycle[0]
)
assert determinant(G) == z(closed)

# Check the denominator-cleared Schur/Bargmann identity:
# d1 det(G) =
# (d1*d2-|c12|^2)(d1*d3-|c13|^2)
# - |d1*c23+conj(c12)*c13|^2.
schur_left = d1 * closed
schur_right = (
    (d1 * d2 - abs2(c12)) * (d1 * d3 - abs2(c13))
    - abs2(add(scale(d1, c23), mul(conj(c12), c13)))
)
assert schur_left == schur_right

# Audit the residualized-face coefficients in (29)--(30).
lam = scale(F(1, 1) / d1, c12)
pair_defect = (
    abs2(lam) * d1 + d2
    - 2 * mul(conj(lam), c12)[0]
)
A = d2 - abs2(c12) / d1
m = add(c23, scale(F(1, 1) / d1, mul(conj(c12), c13)))
assert pair_defect == A
assert schur_right == d1**2 * (
    A * (d3 - abs2(c13) / d1) - abs2(m)
)

# Audit exact saturated-face phase transport without square roots.
# Take d1=1, d2=4, c12=2i.  Kernel transport requires
# c23=-c13*conj(c12)/d1.
d1s, d2s, d3s = F(1), F(4), F(9)
c12s = z(0, 2)
c13s = z(F(3, 2), F(-1, 2))
c23s = neg(mul(c13s, conj(c12s)))
Gs = [
    [z(d1s), neg(c12s), neg(c13s)],
    [neg(conj(c12s)), z(d2s), neg(c23s)],
    [neg(conj(c13s)), neg(conj(c23s)), z(d3s)],
]
assert d1s * d2s == abs2(c12s)
assert determinant(Gs) == z()

# The principal minors remain nonnegative in this rational example.
assert d1s * d3s >= abs2(c13s)
assert d2s * d3s >= abs2(c23s)

# Check the scalar complete-square identity in an exact toy frame.
# S, T, and b are real here; the identity is purely algebraic and has
# the same coefficients as the operator identity.
S = F(5, 2)
T = [F(2, 3), F(-4, 5)]
b = [F(7, 6), F(-3, 8)]
y = sum(T[i] * b[i] for i in range(2))
zz = y / S
lhs = 2 * sum(x * x for x in b) - y * zz
Tnorm2 = sum(x * x for x in T)
rhs = (
    2 * sum((b[i] - T[i] * zz / 2) ** 2 for i in range(2))
    + zz * zz * (S - Tnorm2 / 2)
)
assert lhs == rhs

print("exact full-dual triangle determinant checks passed")
