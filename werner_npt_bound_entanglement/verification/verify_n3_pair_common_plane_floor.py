#!/usr/bin/env python3
"""Dependency-free exact checks for the common-plane floor note."""

from fractions import Fraction as F


def add(*matrices):
    return [
        [sum((a[i][j] for a in matrices), F(0))
         for j in range(len(matrices[0][0]))]
        for i in range(len(matrices[0]))
    ]


def scale(c, a):
    return [[F(c) * x for x in row] for row in a]


def matvec(a, x):
    return [
        sum((a[i][j] * x[j] for j in range(len(x))), F(0))
        for i in range(len(a))
    ]


def assert_eigenbasis(a, vectors, values):
    assert len(vectors) == len(values) == len(a)
    for vector, value in zip(vectors, values):
        assert matvec(a, vector) == [value * x for x in vector]


def partial_transpose_second(a):
    """Logical partial transpose in basis 00,01,10,11."""
    out = [[F(0) for _ in range(4)] for _ in range(4)]
    for x in range(2):
        for y in range(2):
            for u in range(2):
                for v in range(2):
                    out[2 * x + v][2 * u + y] = a[2 * x + y][2 * u + v]
    return out


I = [[F(i == j) for j in range(4)] for i in range(4)]
e00 = [F(1), F(0), F(0), F(0)]
e01 = [F(0), F(1), F(0), F(0)]
e10 = [F(0), F(0), F(1), F(0)]
e11 = [F(0), F(0), F(0), F(1)]


def plus(x, y, sign=1):
    return [a + sign * b for a, b in zip(x, y)]


# Sector eigenvalue table from Y=(I-3P)/2.
s2 = []
s3 = []
for k in range(4):
    ys = [F(-1)] * k + [F(1, 2)] * (3 - k)
    s2.append(F(4, 9) * sum(
        (ys[i] * ys[j] for i in range(3) for j in range(i + 1, 3)),
        F(0),
    ))
    s3.append(F(8, 9) * ys[0] * ys[1] * ys[2])

assert s2 == [F(1, 3), F(-1, 3), F(0), F(4, 3)]
assert s3 == [F(1, 9), F(-2, 9), F(4, 9), F(-8, 9)]

# The scalar correction in the common-plane sector formula.
r1, r2, r3 = F(7, 10), F(9, 10), F(3, 5)
r0 = 4 - r1 - r2 - r3
tr_q3 = sum((r * s for r, s in zip((r0, r1, r2, r3), s3)), F(0))
assert 3 * (F(2, 9) - tr_q3 / 2) == (r1 - r2 + 3 * r3) / 2


def common_factor_matrices(eta1, eta2, eta12):
    """Matrices in equation (16), using the logical singlet projector."""
    singlet = scale(
        F(1, 2),
        [
            [0, 0, 0, 0],
            [0, 1, -1, 0],
            [0, -1, 1, 0],
            [0, 0, 0, 0],
        ],
    )
    q3 = scale(F(8, 9) * eta12, singlet)
    q2 = scale(F(4, 9), add(scale(eta12, I), scale(eta1 + eta2, singlet)))
    return q2, q3


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def floor_matrix(q2, q3):
    return add(
        partial_transpose_second(q2),
        scale(F(2, 9) - trace(q3) / 2, I),
    )


# Canonical sharp code: eta1=eta2=1/2, eta12=1/4.
q2_can, q3_can = common_factor_matrices(F(1, 2), F(1, 2), F(1, 4))
h_can = floor_matrix(q2_can, q3_can)
assert trace(q3_can) == F(2, 9)
assert_eigenbasis(
    partial_transpose_second(q2_can),
    [plus(e00, e11), plus(e00, e11, -1), e01, e10],
    [F(-1, 9), F(1, 3), F(1, 3), F(1, 3)],
)
assert_eigenbasis(
    h_can,
    [plus(e00, e11), plus(e00, e11, -1), e01, e10],
    [F(0), F(4, 9), F(4, 9), F(4, 9)],
)

# Exact 8/27 three-exterior code: all eta values are 1/3.
q2_phi, q3_phi = common_factor_matrices(F(1, 3), F(1, 3), F(1, 3))
h_phi = floor_matrix(q2_phi, q3_phi)
assert trace(q3_phi) == F(8, 27)
assert_eigenbasis(
    partial_transpose_second(q2_phi),
    [plus(e00, e11), plus(e00, e11, -1), e01, e10],
    [F(0), F(8, 27), F(8, 27), F(8, 27)],
)
assert_eigenbasis(
    h_phi,
    [plus(e00, e11), plus(e00, e11, -1), e01, e10],
    [F(2, 27), F(10, 27), F(10, 27), F(10, 27)],
)

# The chart floor is exactly (2/9)(1-eta1-eta2).
for eta1, eta2, eta12 in [
    (F(0), F(0), F(0)),
    (F(1, 7), F(2, 9), F(1, 8)),
    (F(1, 2), F(1, 2), F(1, 4)),
]:
    q2, q3 = common_factor_matrices(eta1, eta2, eta12)
    h = floor_matrix(q2, q3)
    expected_min = F(2, 9) * (1 - eta1 - eta2)
    assert_eigenbasis(
        h,
        [plus(e00, e11), plus(e00, e11, -1), e01, e10],
        [
            expected_min,
            expected_min + F(4, 9) * (eta1 + eta2),
            expected_min + F(4, 9) * (eta1 + eta2),
            expected_min + F(4, 9) * (eta1 + eta2),
        ],
    )

# Computational trace maximizer.
q2_trace = scale(F(1, 3), I)
q3_trace = scale(F(1, 9), I)
assert trace(q3_trace) == F(4, 9)
assert floor_matrix(q2_trace, q3_trace) == q2_trace

# Pure-state partial-transpose floor reduces to (a-b)^2 >= 0.
for a, b in [(F(0), F(1)), (F(2, 7), F(3, 5)), (F(1), F(1))]:
    assert (a - b) ** 2 >= 0
    assert a * b <= (a * a + b * b) / 2

print("all exact common-plane floor checks passed")
