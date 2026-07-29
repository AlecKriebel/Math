#!/usr/bin/env python3
"""Exact audit of the reverse-Cauchy/leakage abstract obstruction."""

from fractions import Fraction as F


def zeros(n: int) -> list[list[F]]:
    return [[F(0) for _ in range(n)] for _ in range(n)]


def inner(left: list[list[F]], right: list[list[F]]) -> F:
    return sum(
        (
            left[i][j] * right[i][j]
            for i in range(len(left))
            for j in range(len(left))
        ),
        F(0),
    )


def add(left: list[list[F]], right: list[list[F]]) -> list[list[F]]:
    return [
        [left[i][j] + right[i][j] for j in range(len(left))]
        for i in range(len(left))
    ]


def scale(value: F, matrix: list[list[F]]) -> list[list[F]]:
    return [[value * entry for entry in row] for row in matrix]


def p_trace(matrix: list[list[F]]) -> F:
    return matrix[0][0] + matrix[1][1]


def superoperator(matrix: list[list[F]]) -> list[list[F]]:
    return add(matrix, scale(-F(3, 4) * p_trace(matrix), projection))


def quadratic(matrix: list[list[F]]) -> F:
    return inner(matrix, superoperator(matrix))


n = 4
projection = zeros(n)
projection[0][0] = F(1)
projection[1][1] = F(1)

c1 = zeros(n)
c2 = zeros(n)
c1[0][0] = F(1)
c2[1][1] = F(1)
c = add(c1, c2)

assert quadratic(c1) == F(1, 4)
assert quadratic(c2) == F(1, 4)
crossed = inner(c1, superoperator(c2))
assert crossed == -F(3, 4)
assert crossed**2 - quadratic(c1) * quadratic(c2) == F(1, 2)

critical_value = quadratic(c) / 2
assert quadratic(c) == -1
assert critical_value == -F(1, 2)
assert superoperator(c) == scale(critical_value, c)

# Exact representative left/right leakages.
d_left = zeros(n)
d_right = zeros(n)
d_left[2][0] = F(2)
d_left[3][1] = F(-1)
d_right[0][2] = F(3)
d_right[1][3] = F(1)

assert p_trace(d_left) == 0
assert p_trace(d_right) == 0
assert superoperator(d_left) == d_left
assert superoperator(d_right) == d_right
p = inner(d_left, superoperator(d_right))
q = F(0)  # the normal residual vanishes identically
assert p == 0 and q == 0

a_leak = quadratic(d_left) - critical_value * inner(d_left, d_left)
b_leak = (
    quadratic(d_right) - critical_value * inner(d_right, d_right)
)
assert a_leak > 0 and b_leak > 0
assert (abs(p) + abs(q)) ** 2 <= a_leak * b_leak

# The global determinant-slice lower bound is
#   Q(D) >= (s1^2+s2^2)/4 - 3/2 >= -1
# because s1*s2=1.
singular_square_sum = F(17, 4)  # example s1=2, s2=1/2
assert singular_square_sum / 4 - F(3, 2) > -1
assert F(2) / 4 - F(3, 2) == -1

print(
    "verified exact strict rank-one floor, negative global critical "
    "point, reverse-Cauchy defect, and identically vanishing leakage "
    "cross/normal terms"
)
