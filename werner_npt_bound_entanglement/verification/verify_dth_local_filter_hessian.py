#!/usr/bin/env python3
"""Exact audit of the summed one-site DTH filter-Hessian inequality."""

from fractions import Fraction as F
from itertools import product


N = 27


def eps(p, a, i):
    pos = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    neg = ((0, 2, 1), (2, 1, 0), (1, 0, 2))
    return int((p, a, i) in pos) - int((p, a, i) in neg)


def zeros(n=N, m=N):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(r, s)] for r, s in zip(a, b)]


def hodge_hat(z):
    out = zeros()
    for p, q, r in product(range(3), repeat=3):
        coefficient = z[9 * p + 3 * q + r]
        if not coefficient:
            continue
        for a, b, c in product(range(3), repeat=3):
            row = 9 * a + 3 * b + c
            for i, j, k in product(range(3), repeat=3):
                value = coefficient * eps(p, a, i) * eps(q, b, j) * eps(r, c, k)
                if value:
                    out[row][9 * i + 3 * j + k] += value
    return out


def partial_trace(a, site):
    others = [j for j in range(3) if j != site]
    out = zeros(9, 9)
    for rr, cc in product(product(range(3), repeat=2), repeat=2):
        total = F(0)
        for x in range(3):
            row = [0, 0, 0]
            col = [0, 0, 0]
            row[site] = col[site] = x
            for j, value in zip(others, rr):
                row[j] = value
            for j, value in zip(others, cc):
                col[j] = value
            total += a[9 * row[0] + 3 * row[1] + row[2]][
                9 * col[0] + 3 * col[1] + col[2]]
        out[3 * rr[0] + rr[1]][3 * cc[0] + cc[1]] = total
    return out


def hs_norm_squared(a):
    return sum(x * x for row in a for x in row)


def trace_product(a, b):
    return sum(a[i][j] * b[j][i]
               for i in range(len(a)) for j in range(len(a)))


def main():
    # Basis-independent completeness tensor for traceless M_3.
    for i, j, k, l in product(range(3), repeat=4):
        contraction = F(i == l) * F(j == k) - F(i == j) * F(k == l) / 3
        expected = F(i == l and j == k) - F(i == j and k == l, 3)
        assert contraction == expected

    # Smooth equality z=e0 tensor (3E00+4E11)/5.
    z = [F(0)] * N
    z[0], z[4] = F(3, 5), F(4, 5)
    dh = hodge_hat(z)
    s = scale(F(1, 8), matmul(transpose(dh), dh))

    q = [F(0)] * 9
    q[0], q[4] = F(4, 5), F(3, 5)
    r = [F(0)] * 9
    r[8] = F(1)
    prest = [[q[i] * q[j] + r[i] * r[j] for j in range(9)] for i in range(9)]
    ptop = zeros()
    for local in (1, 2):
        for i, j in product(range(9), repeat=2):
            ptop[9 * local + i][9 * local + j] = prest[i][j]

    m = matmul(ptop, s)
    f_value = sum(m[i][i] for i in range(N))
    assert f_value == F(1, 2)

    # Chat=2sqrt(2) C=P Dhat^T, so ||Tr C||^2=||Tr Chat||^2/8.
    chat = matmul(ptop, transpose(dh))
    lhs = []
    for site in range(3):
        c_hat = partial_trace(chat, site)
        p_hat = partial_trace(ptop, site)
        m_hat = partial_trace(m, site)
        value = hs_norm_squared(c_hat) / 8 + trace_product(p_hat, m_hat)
        assert value <= 2 * f_value
        lhs.append(value)

    assert lhs[0] == 2 * f_value
    assert lhs[1] == lhs[2] == F(481, 1250)

    print("exact summed local-filter Hessian audit passed")
    print("factor equality values:", *lhs)


if __name__ == "__main__":
    main()
