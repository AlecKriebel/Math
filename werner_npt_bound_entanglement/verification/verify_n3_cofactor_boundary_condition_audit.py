#!/usr/bin/env python3
"""Exact audit of the missing condition in the two-site cofactor lemma.

Only the Python standard library is used.  All matrix entries are
fractions, so the rank, marginal, kernel, and determinant-factor checks
are exact.
"""

from fractions import Fraction as F


def zeros(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def identity(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def add(a, b):
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def scale(c, a):
    return [[c * value for value in row] for row in a]


def matvec(a, x):
    return [
        sum((a[i][j] * x[j] for j in range(len(x))), F(0))
        for i in range(len(a))
    ]


def rank(a):
    work = [row[:] for row in a]
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (i for i in range(pivot_row, rows) if work[i][col] != 0),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][col]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for i in range(rows):
            if i == pivot_row:
                continue
            value = work[i][col]
            if value:
                work[i] = [
                    work[i][j] - value * work[pivot_row][j]
                    for j in range(cols)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def idx(k, a, b):
    return 9 * k + 3 * a + b


def partial_trace_physical(r, site):
    """Trace site 1 or 2, retaining K and the other qutrit."""
    out = zeros(6, 6)
    if site == 1:
        for k in range(2):
            for b in range(3):
                for ell in range(2):
                    for d in range(3):
                        out[3 * k + b][3 * ell + d] = sum(
                            (
                                r[idx(k, a, b)][idx(ell, a, d)]
                                for a in range(3)
                            ),
                            F(0),
                        )
    else:
        for k in range(2):
            for a in range(3):
                for ell in range(2):
                    for c in range(3):
                        out[3 * k + a][3 * ell + c] = sum(
                            (
                                r[idx(k, a, b)][idx(ell, c, b)]
                                for b in range(3)
                            ),
                            F(0),
                        )
    return out


def embed_after_trace(x, site):
    """Insert the identity on the site traced by partial_trace_physical."""
    out = zeros(18, 18)
    if site == 1:
        for k in range(2):
            for a in range(3):
                for b in range(3):
                    for ell in range(2):
                        for c in range(3):
                            for d in range(3):
                                if a == c:
                                    out[idx(k, a, b)][idx(ell, c, d)] = (
                                        x[3 * k + b][3 * ell + d]
                                    )
    else:
        for k in range(2):
            for a in range(3):
                for b in range(3):
                    for ell in range(2):
                        for c in range(3):
                            for d in range(3):
                                if b == d:
                                    out[idx(k, a, b)][idx(ell, c, d)] = (
                                        x[3 * k + a][3 * ell + c]
                                    )
    return out


def physical_marginal(r, site):
    out = zeros(3, 3)
    if site == 1:
        for a in range(3):
            for c in range(3):
                out[a][c] = sum(
                    (
                        r[idx(k, a, b)][idx(k, c, b)]
                        for k in range(2)
                        for b in range(3)
                    ),
                    F(0),
                )
    else:
        for b in range(3):
            for d in range(3):
                out[b][d] = sum(
                    (
                        r[idx(k, a, b)][idx(k, a, d)]
                        for k in range(2)
                        for a in range(3)
                    ),
                    F(0),
                )
    return out


def auxiliary_marginal(r):
    out = zeros(2, 2)
    for k in range(2):
        for ell in range(2):
            out[k][ell] = sum(
                (
                    r[idx(k, a, b)][idx(ell, a, b)]
                    for a in range(3)
                    for b in range(3)
                ),
                F(0),
            )
    return out


# P is the sum of the projectors onto the two shifted Bell vectors.  Their
# outer products have entries 1/3, so no square roots are needed.
p = zeros(9, 9)
supports = (
    ((0, 0), (1, 1), (2, 2)),
    ((0, 1), (1, 2), (2, 0)),
)
for support in supports:
    for a, b in support:
        for c, d in support:
            p[3 * a + b][3 * c + d] += F(1, 3)

r = zeros(18, 18)
for i in range(9):
    for j in range(9):
        r[i][j] = p[i][j]  # the K=0 block

assert rank(p) == 2
assert rank(r) == 2
assert sum((r[i][i] for i in range(18)), F(0)) == 2

rho1 = physical_marginal(r, 1)
rho2 = physical_marginal(r, 2)
assert rho1 == scale(F(2, 3), identity(3))
assert rho2 == scale(F(2, 3), identity(3))
assert F(8, 27) * F(8, 27) == F(64, 729)

e1 = embed_after_trace(partial_trace_physical(r, 1), 1)
e2 = embed_after_trace(partial_trace_physical(r, 2), 2)

# E1 E2(R) is I_1 I_2 tensor Tr_12(R).
rho_k = auxiliary_marginal(r)
e12 = zeros(18, 18)
for k in range(2):
    for a in range(3):
        for b in range(3):
            for ell in range(2):
                for c in range(3):
                    for d in range(3):
                        if a == c and b == d:
                            e12[idx(k, a, b)][idx(ell, c, d)] = rho_k[k][ell]

m = add(add(scale(4, e12), scale(-2, e1)), add(scale(-2, e2), r))

for a in range(3):
    for b in range(3):
        x = [F(0) for _ in range(18)]
        x[idx(1, a, b)] = F(1)
        assert matvec(m, x) == [F(0) for _ in range(18)]

assert rho_k == [[F(2), F(0)], [F(0), F(0)]]
assert rho_k != identity(2)

print("exact cofactor-boundary condition audit passed")
