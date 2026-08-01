#!/usr/bin/env python3
"""Exact rational audit of the degenerate DTH product-corner cluster."""

from fractions import Fraction as F
from itertools import permutations, product


N = 27
K = [9 * i + 3 * j + k for i, j, k in product((1, 2), repeat=3)]


def eps(p, a, i):
    positive = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    negative = ((0, 2, 1), (2, 1, 0), (1, 0, 2))
    return int((p, a, i) in positive) - int((p, a, i) in negative)


def zeros(n=N, m=N):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def add(*matrices):
    return [[sum(m[i][j] for m in matrices)
             for j in range(len(matrices[0][0]))]
            for i in range(len(matrices[0]))]


def scale(c, a):
    return [[c * x for x in row] for row in a]


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


def rank(a):
    matrix = [row[:] for row in a]
    rows, columns = len(matrix), len(matrix[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((r for r in range(pivot_row, rows)
                      if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [x / value for x in matrix[pivot_row]]
        for r in range(rows):
            if r != pivot_row and matrix[r][column]:
                value = matrix[r][column]
                matrix[r] = [x - value * y
                             for x, y in zip(matrix[r], matrix[pivot_row])]
        pivot_row += 1
    return pivot_row


def eye(n=8):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def effective(delta):
    z0 = [F(0)] * N
    z0[0] = F(1)
    d0 = hodge_hat(z0)
    e = hodge_hat(delta)
    n = sum(x * x for x in delta)
    s1 = scale(F(1, 8), add(matmul(transpose(d0), e),
                              matmul(transpose(e), d0)))
    outside = [i for i in range(N) if i not in K]
    et_e = matmul(transpose(e), e)
    out = zeros(8, 8)
    for a, ia in enumerate(K):
        for b, ib in enumerate(K):
            value = et_e[ia][ib] / 8 - F(a == b) * n / 8
            value += 8 * sum(s1[ia][q] * s1[q][ib] for q in outside)
            out[a][b] = value
    return out


def tangent(entries):
    out = [F(0)] * N
    for index, value in entries.items():
        out[9 * index[0] + 3 * index[1] + index[2]] = F(value)
    return out


def matrix_polynomial_zero(h, n, d):
    i8 = eye()
    shifted = add(h, scale(n / 8, i8))
    quadratic = add(matmul(h, h), scale(-(d * d) / 16, i8))
    return matmul(shifted, quadratic) == zeros(8, 8)


# Bivariate polynomials in (lambda,t), represented by {(l_degree,t_degree):c}.
def padd(*polys):
    out = {}
    for p in polys:
        for key, value in p.items():
            out[key] = out.get(key, F(0)) + value
            if not out[key]:
                del out[key]
    return out


def pscale(c, p):
    return {key: c * value for key, value in p.items() if c * value}


def pmul(*polys):
    out = {(0, 0): F(1)}
    for b in polys:
        product_out = {}
        for (la, ta), x in out.items():
            for (lb, tb), y in b.items():
                key = (la + lb, ta + tb)
                product_out[key] = product_out.get(key, F(0)) + x * y
        out = {key: value for key, value in product_out.items() if value}
    return out


ONE = {(0, 0): F(1)}
LAM = {(1, 0): F(1)}
TVAR = {(0, 1): F(1)}


def ppower(a, n):
    out = ONE
    for _ in range(n):
        out = pmul(out, a)
    return out


def parity(perm):
    return -1 if sum(perm[i] > perm[j] for i in range(len(perm))
                     for j in range(i + 1, len(perm))) % 2 else 1


def determinant(matrix):
    n = len(matrix)
    out = {}
    for perm in permutations(range(n)):
        term = ONE
        for i, j in enumerate(perm):
            term = pmul(term, matrix[i][j])
        out = padd(out, pscale(parity(perm), term))
    return out


def characteristic_quartic_path():
    z0 = tangent({(0, 0, 0): 1})
    delta = tangent({(1, 1, 0): 1, (2, 2, 0): 1,
                     (1, 0, 1): 1, (2, 0, 2): 1})
    d0, de = hodge_hat(z0), hodge_hat(delta)
    g0 = matmul(transpose(d0), d0)
    g1 = add(matmul(transpose(d0), de), matmul(transpose(de), d0))
    g2 = matmul(transpose(de), de)
    matrix = [[padd(pscale(F(g0[i][j]), ONE),
                    pscale(F(g1[i][j]), TVAR),
                    pscale(F(g2[i][j]), ppower(TVAR, 2)))
               for j in range(N)] for i in range(N)]

    # Connected components of the polynomial Gram matrix.
    graph = {i: set() for i in range(N)}
    for i in range(N):
        for j in range(N):
            if i != j and matrix[i][j]:
                graph[i].add(j)
                graph[j].add(i)
    seen, components = set(), []
    for start in range(N):
        if start in seen:
            continue
        stack, component = [start], []
        seen.add(start)
        while stack:
            i = stack.pop()
            component.append(i)
            for j in graph[i]:
                if j not in seen:
                    seen.add(j)
                    stack.append(j)
        components.append(sorted(component))
    assert sorted(map(len, components)) == [1] * 9 + [2] * 4 + [5] * 2

    characteristic = ONE
    for component in components:
        block = []
        for i in component:
            row = []
            for j in component:
                row.append(padd(LAM if i == j else {}, pscale(-1, matrix[i][j])))
            block.append(row)
        characteristic = pmul(characteristic, determinant(block))

    t2 = ppower(TVAR, 2)
    t4 = ppower(TVAR, 4)
    q6 = padd(ppower(LAM, 2),
              pscale(-1, LAM), pscale(-6, pmul(LAM, t2)),
              pscale(9, t4))
    q2 = padd(ppower(LAM, 2),
              pscale(-1, LAM), pscale(-2, pmul(LAM, t2)),
              t4)
    expected = pmul(
        ppower(LAM, 7),
        ppower(padd(LAM, pscale(-2, t2)), 8),
        ppower(padd(LAM, pscale(-1, ONE)), 4),
        ppower(q6, 2),
        ppower(q2, 2),
    )
    assert characteristic == expected


def main():
    # Weight-one block vanishes.
    h1 = effective(tangent({(1, 0, 0): 2, (2, 0, 0): -3}))
    assert h1 == zeros(8, 8)

    # Generic weight-two spectrum certificate.
    z = [[F(1), F(2)], [F(3), F(5)]]
    h2 = effective(tangent({(1, 1, 0): z[0][0], (1, 2, 0): z[0][1],
                            (2, 1, 0): z[1][0], (2, 2, 0): z[1][1]}))
    n2 = sum(x * x for row in z for x in row)
    d2 = abs(z[0][0] * z[1][1] - z[0][1] * z[1][0])
    assert matrix_polynomial_zero(h2, n2, d2)
    assert rank(add(h2, scale(n2 / 8, eye()))) == 4
    assert rank(add(matmul(h2, h2), scale(-(d2 * d2) / 16, eye()))) == 4

    # Generic weight-three spectrum certificate.
    entries = {(i, j, k): 1 + i + 2 * j + 3 * k
               for i, j, k in product((1, 2), repeat=3)}
    delta3 = tangent(entries)
    n3 = sum(x * x for x in delta3)
    h3 = effective(delta3)
    assert matmul(h3, add(h3, scale(n3 / 8, eye()))) == zeros(8, 8)
    assert rank(h3) == 6

    # Orthogonal support splitting.
    pieces = [
        tangent({(1, 0, 0): 2, (2, 0, 0): -3}),
        tangent({(1, 1, 0): 1, (2, 2, 0): 2}),
        tangent({(1, 0, 1): -2, (2, 0, 2): 1}),
        delta3,
    ]
    total = [sum(piece[i] for piece in pieces) for i in range(N)]
    assert effective(total) == add(*(effective(piece) for piece in pieces))

    # Explicit nonintegrable zero-Hessian direction.
    star = tangent({(1, 1, 0): 1, (2, 2, 0): 1,
                    (1, 0, 1): 1, (2, 0, 2): 1})
    hstar = effective(star)
    assert rank(add(hstar, scale(F(1, 2), eye()))) == 4
    assert rank(add(hstar, scale(F(-1, 4), eye()))) == 6
    assert rank(add(hstar, scale(F(1, 4), eye()))) == 6

    characteristic_quartic_path()
    print("exact product-corner cluster certificate passed")
    print("support-orthogonal Hessian splitting passed")
    print("nonintegrable zero-Hessian quartic path passed")


if __name__ == "__main__":
    main()
