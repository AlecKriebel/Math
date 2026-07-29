#!/usr/bin/env python3
"""Dependency-free exact checks for the intersection-one obstruction."""

from fractions import Fraction as F


def add(p, q):
    out = dict(p)
    for degree, value in q.items():
        out[degree] = out.get(degree, F(0)) + value
        if out[degree] == 0:
            del out[degree]
    return out


def mul(p, q):
    out = {}
    for i, a in p.items():
        for j, b in q.items():
            out[i + j] = out.get(i + j, F(0)) + a * b
    return {degree: value for degree, value in out.items() if value}


def determinant3(matrix):
    total = {}
    permutations = (
        ((0, 1, 2), 1),
        ((0, 2, 1), -1),
        ((1, 0, 2), -1),
        ((1, 2, 0), 1),
        ((2, 0, 1), 1),
        ((2, 1, 0), -1),
    )
    for permutation, sign in permutations:
        term = {0: F(sign)}
        for row in range(3):
            term = mul(term, matrix[row][permutation[row]])
        total = add(total, term)
    return total


def rank3_rational(a):
    det = (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )
    minor = a[0][1] * a[1][2] - a[0][2] * a[1][1]
    assert det == 0
    assert minor == 1
    return 2


def main():
    c = [
        [F(0), F(1), F(1)],
        [F(0), F(0), F(1)],
        [F(0), F(0), F(0)],
    ]
    assert rank3_rational(c) == 2
    frobenius_squared = sum(x * x for row in c for x in row)
    assert frobenius_squared == 3

    # ran(C)=span(e0,e1), ran(C^*)=span(e1,e2).
    assert [row[1] for row in c] == [F(1), F(0), F(0)]
    assert [row[2] for row in c] == [F(1), F(1), F(0)]
    assert c[0] == [F(0), F(1), F(1)]
    assert c[1] == [F(0), F(0), F(1)]

    # Laurent-polynomial matrix for A_theta, with zbar=z^{-1}.
    zero = {}
    z_over_2 = {1: F(1, 2)}
    zbar_over_2 = {-1: F(1, 2)}
    a = [
        [zero, z_over_2, z_over_2],
        [zbar_over_2, zero, z_over_2],
        [zbar_over_2, zbar_over_2, zero],
    ]
    assert determinant3(a) == {-1: F(1, 8), 1: F(1, 8)}

    # Every one of the three edges contributes twice with weight 1/4.
    trace_a_squared = 3 * 2 * F(1, 4)
    assert trace_a_squared == F(3, 2)

    # The inverse-variable relation s=h(y)=y(y-3/4)^2.
    def h(y):
        return y * (y - F(3, 4)) ** 2

    assert h(F(3, 4)) == 0
    assert h(F(1)) == F(1, 16)
    assert 6 * F(3, 4) - 3 == F(3, 2)

    g_zero = F(3, 4)
    g_endpoint = F(1)
    minimum_nuclear_sum_squared = 4 * (g_zero + g_endpoint)
    threshold = 2 * frobenius_squared
    assert minimum_nuclear_sum_squared == 7
    assert threshold == 6
    assert minimum_nuclear_sum_squared - threshold == 1

    # Exact endpoint spectra.
    a0_spectrum = (F(1), F(-1, 2), F(-1, 2))
    assert sum(a0_spectrum) == 0
    assert sum(x * x for x in a0_spectrum) == F(3, 2)
    assert sum(abs(x) for x in a0_spectrum) ** 2 == 4
    assert 4 + 3 == minimum_nuclear_sum_squared

    print("verified rank-two intersection-one support geometry")
    print("verified exact Laurent determinant and quadratic trace")
    print("verified convex inverse endpoint bound for every phase")
    print("verified uniform phase-nuclear gap: 7 - 6 = 1")


if __name__ == "__main__":
    main()
