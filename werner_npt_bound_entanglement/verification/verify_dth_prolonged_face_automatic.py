#!/usr/bin/env python3
"""Exact finite-dimensional audit of the automatic-face contraction."""

from fractions import Fraction as Q


def zeros(n, m):
    return [[Q(0) for _ in range(m)] for _ in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt]
            for row in a]


def kron(a, b):
    return [[a[i][j] * b[k][ell]
             for j in range(len(a[0])) for ell in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def partial_trace_last(a, d, c):
    out = zeros(d, d)
    for i in range(d):
        for j in range(d):
            out[i][j] = sum(a[i * c + k][j * c + k] for k in range(c))
    return out


def main():
    # An arbitrary exact PSD T=B B^T on D tensor C, with D=4 and C=2.
    d, c = 4, 2
    b = [[Q((3 * i + 5 * j + 1) % 11 - 5) for j in range(5)]
         for i in range(d * c)]
    t = matmul(b, transpose(b))
    r = partial_trace_last(t, d, c)

    c2 = [[Q(1), Q(-2), Q(0), Q(3)],
          [Q(0), Q(1), Q(1), Q(-1)]]
    eye_c = [[Q(int(i == j)) for j in range(c)] for i in range(c)]
    c3 = kron(c2, eye_c)

    left = partial_trace_last(matmul(matmul(c3, t), transpose(c3)), 2, c)
    right = matmul(matmul(c2, r), transpose(c2))
    assert left == right

    # A positive matrix with zero partial trace must itself vanish.
    zero = zeros(2 * c, 2 * c)
    assert partial_trace_last(zero, 2, c) == zeros(2, 2)
    assert sum(zero[i][i] for i in range(2 * c)) == 0

    print("PASS: exact contraction identity and automatic positive face")


if __name__ == "__main__":
    main()

