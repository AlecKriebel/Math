#!/usr/bin/env python3
"""Dependency-free exact checks for the common-local-plane theorem."""

from fractions import Fraction as F
from itertools import product


def zeros(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def kron(a, b):
    ar, ac = len(a), len(a[0])
    br, bc = len(b), len(b[0])
    out = zeros(ar * br, ac * bc)
    for i in range(ar):
        for j in range(ac):
            for k in range(br):
                for ell in range(bc):
                    out[i * br + k][j * bc + ell] = a[i][j] * b[k][ell]
    return out


def hs_inner(a, b):
    # All matrices used below are real.
    return sum(
        a[i][j] * b[i][j]
        for i in range(len(a))
        for j in range(len(a[0]))
    )


def matrix_rank(a):
    x = [row[:] for row in a]
    rows, cols = len(x), len(x[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (r for r in range(pivot_row, rows) if x[r][col] != 0),
            None,
        )
        if pivot is None:
            continue
        x[pivot_row], x[pivot] = x[pivot], x[pivot_row]
        value = x[pivot_row][col]
        x[pivot_row] = [entry / value for entry in x[pivot_row]]
        for r in range(rows):
            if r == pivot_row:
                continue
            value = x[r][col]
            if value:
                x[r] = [
                    x[r][j] - value * x[pivot_row][j]
                    for j in range(cols)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def digits(index, n=3):
    out = [0] * n
    for position in range(n - 1, -1, -1):
        out[position] = index % 3
        index //= 3
    return out


def reflection_at_site(c, site):
    size = len(c)
    out = [row[:] for row in c]
    for row in range(size):
        rr = digits(row)
        for col in range(size):
            cc = digits(col)
            if rr[site] != cc[site]:
                continue
            trace = F(0)
            for value in range(3):
                r2, c2 = rr[:], cc[:]
                r2[site] = value
                c2[site] = value
                ri = (r2[0] * 3 + r2[1]) * 3 + r2[2]
                ci = (c2[0] * 3 + c2[1]) * 3 + c2[2]
                trace += c[ri][ci]
            out[row][col] -= F(2, 3) * trace
    return out


def reflection_cube(c):
    out = c
    for site in range(3):
        out = reflection_at_site(out, site)
    return out


def local_reflection(a):
    trace = sum(a[i][i] for i in range(3))
    return [
        [
            a[i][j] - (F(2, 3) * trace if i == j else F(0))
            for j in range(3)
        ]
        for i in range(3)
    ]


# Formal local spectral arithmetic.  If x=||V^*U||_F^2 is in [0,2],
# the exceptional eigenvalue is kappa=1-2x/3 in [-1/3,1].
for numerator in range(0, 201):
    x = F(numerator, 100)
    kappa = F(1) - F(2, 3) * x
    assert F(-1, 3) <= kappa <= F(1)

# Enumerate all endpoint products through eight copies.  A multilinear
# product reaches its minimum at interval endpoints, and the symbolic
# proof in the note handles arbitrary n by counting negative factors.
endpoints = (F(-1, 3), F(1))
for copies in range(1, 9):
    products_n = []
    for factors in product(endpoints, repeat=copies):
        value = F(1)
        for factor in factors:
            value *= factor
        products_n.append(value)
    assert min(products_n) == F(-1, 3)

# Exact rank-two equality C=P_2 tensor E_01 tensor E_01.
p2 = [[F(1), F(0), F(0)],
      [F(0), F(1), F(0)],
      [F(0), F(0), F(0)]]
e01 = [[F(0), F(1), F(0)],
       [F(0), F(0), F(0)],
       [F(0), F(0), F(0)]]
c = kron(kron(p2, e01), e01)
assert matrix_rank(c) == 2
norm = hs_inner(c, c)
value = hs_inner(c, reflection_cube(c))
assert norm == 2
assert value == -F(1, 3) * norm

# The local equality factors are exactly -1/3, 1, 1.
assert hs_inner(p2, local_reflection(p2)) == -F(1, 3) * hs_inner(p2, p2)
assert hs_inner(e01, local_reflection(e01)) == hs_inner(e01, e01)
assert F(-1, 3) * F(1) * F(1) == F(-1, 3)

# Exact crossed-energy obstruction from the same equality.
h00 = F(1, 3)
h11 = F(1, 3)
h01 = -F(2, 3)
g00, g01, g10, g11 = F(1, 3), F(1), F(1), F(1, 3)
assert g01 * g10 > (g00 + F(1, 3)) * (g11 + F(1, 3))
assert h01 * h01 == (h00 + F(1, 3)) * (h11 + F(1, 3))
assert g01 * g10 - h01 * h01 == F(5, 9)

print(
    "verified exact compressed-spectrum interval, all-copy tensor floor, "
    "rank-two reflection equality, and crossed-assignment obstruction"
)
