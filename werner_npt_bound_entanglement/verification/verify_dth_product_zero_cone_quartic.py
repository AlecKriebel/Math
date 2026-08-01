#!/usr/bin/env python3
"""Exact algebra audit of the product-corner zero cone and quartic block."""

from fractions import Fraction as F
from itertools import permutations, product


# Sparse polynomials in (lambda,u,a,b,c).
ZERO_EXPONENT = (0, 0, 0, 0, 0)


def add(*polys):
    out = {}
    for poly in polys:
        for key, value in poly.items():
            out[key] = out.get(key, F(0)) + value
            if not out[key]:
                del out[key]
    return out


def scale(value, poly):
    return {key: value * coefficient for key, coefficient in poly.items()
            if value * coefficient}


def multiply(*polys):
    out = {ZERO_EXPONENT: F(1)}
    for poly in polys:
        product_out = {}
        for left, x in out.items():
            for right, y in poly.items():
                key = tuple(a + b for a, b in zip(left, right))
                product_out[key] = product_out.get(key, F(0)) + x * y
        out = {key: value for key, value in product_out.items() if value}
    return out


def power(poly, exponent):
    return multiply(*(poly for _ in range(exponent))) if exponent else {
        ZERO_EXPONENT: F(1)
    }


ONE = {ZERO_EXPONENT: F(1)}
LAM = {(1, 0, 0, 0, 0): F(1)}
U = {(0, 1, 0, 0, 0): F(1)}
A = {(0, 0, 1, 0, 0): F(1)}
B = {(0, 0, 0, 1, 0): F(1)}
C = {(0, 0, 0, 0, 1): F(1)}


def parity(perm):
    return -1 if sum(perm[i] > perm[j] for i in range(len(perm))
                     for j in range(i + 1, len(perm))) % 2 else 1


def determinant(matrix):
    out = {}
    for perm in permutations(range(len(matrix))):
        term = ONE
        for i, j in enumerate(perm):
            term = multiply(term, matrix[i][j])
        out = add(out, scale(parity(perm), term))
    return out


def eps(p, i, j):
    positive = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    negative = ((0, 2, 1), (2, 1, 0), (1, 0, 2))
    return int((p, i, j) in positive) - int((p, i, j) in negative)


def hodge_basis(index):
    out = [[F(0) for _ in range(27)] for _ in range(27)]
    p, q, r = index
    for a0, a1, a2, i0, i1, i2 in product(range(3), repeat=6):
        value = eps(p, a0, i0) * eps(q, a1, i1) * eps(r, a2, i2)
        if value:
            out[9 * a0 + 3 * a1 + a2][9 * i0 + 3 * i1 + i2] = F(value)
    return out


def polynomial_gram_block():
    # Dhat=D000+t[a(D110+D220)+b(D101+D202)+c(D012-D021)].
    d0 = hodge_basis((0, 0, 0))
    da = [[x + y for x, y in zip(r, s)] for r, s in zip(
        hodge_basis((1, 1, 0)), hodge_basis((2, 2, 0)))]
    db = [[x + y for x, y in zip(r, s)] for r, s in zip(
        hodge_basis((1, 0, 1)), hodge_basis((2, 0, 2)))]
    dc = [[x - y for x, y in zip(r, s)] for r, s in zip(
        hodge_basis((0, 1, 2)), hodge_basis((0, 2, 1)))]

    coefficient = [[None for _ in range(27)] for _ in range(27)]
    ua = multiply(U, A)
    ub = multiply(U, B)
    uc = multiply(U, C)
    for i, j in product(range(27), repeat=2):
        coefficient[i][j] = add(
            scale(d0[i][j], ONE), scale(da[i][j], ua),
            scale(db[i][j], ub), scale(dc[i][j], uc))

    gram = [[{} for _ in range(27)] for _ in range(27)]
    for i, j in product(range(27), repeat=2):
        gram[i][j] = add(*(multiply(coefficient[k][i], coefficient[k][j])
                           for k in range(27)))

    component = [1, 3, 13, 18, 23, 25]
    block = []
    for i in component:
        row = []
        for j in component:
            row.append(add(LAM if i == j else {}, scale(-1, gram[i][j])))
        block.append(row)
    actual = determinant(block)

    a2, b2, c2 = power(A, 2), power(B, 2), power(C, 2)
    s = add(a2, b2, c2)
    p = add(multiply(a2, b2), multiply(a2, c2), multiply(b2, c2))
    u2 = power(U, 2)
    q = add(
        multiply(power(LAM, 2), power(add(LAM, scale(-1, ONE)), 2)),
        scale(4, multiply(s, u2, power(LAM, 2), add(ONE, scale(-1, LAM)))),
        multiply(power(u2, 2), add(
            multiply(add(scale(4, power(s, 2)), scale(6, p)), power(LAM, 2)),
            scale(-1, multiply(add(scale(4, power(s, 2)), scale(-6, p)), LAM)),
        )),
        scale(-12, multiply(s, p, power(u2, 3), LAM)),
        scale(9, multiply(power(p, 2), power(u2, 4))),
    )
    expected = multiply(LAM, add(LAM, scale(-1, ONE)), q)
    assert actual == expected


def rank(vectors):
    if not vectors:
        return 0
    matrix = [[F(x) for x in vector] for vector in vectors]
    rows, columns = len(matrix), len(matrix[0])
    pivot = 0
    for column in range(columns):
        row = next((i for i in range(pivot, rows) if matrix[i][column]), None)
        if row is None:
            continue
        matrix[pivot], matrix[row] = matrix[row], matrix[pivot]
        value = matrix[pivot][column]
        matrix[pivot] = [x / value for x in matrix[pivot]]
        for i in range(rows):
            if i != pivot and matrix[i][column]:
                value = matrix[i][column]
                matrix[i] = [x - value * y for x, y in zip(matrix[i], matrix[pivot])]
        pivot += 1
    return pivot


def vector(entries):
    out = [F(0)] * 8
    for bits, value in entries.items():
        out[4 * bits[0] + 2 * bits[1] + bits[2]] = F(value)
    return out


def incidence_check():
    a12 = [vector({(0, 0, 0): 1, (1, 1, 0): 1}),
           vector({(0, 0, 1): 1, (1, 1, 1): 1})]
    a13 = [vector({(0, 0, 0): 1, (1, 0, 1): 1}),
           vector({(0, 1, 0): 1, (1, 1, 1): 1})]
    a23_skew = [vector({(0, 0, 1): 1, (0, 1, 0): -1}),
                vector({(1, 0, 1): 1, (1, 1, 0): -1})]
    a23_symmetric = [vector({(0, 0, 0): 1, (0, 1, 1): 1}),
                     vector({(1, 0, 0): 1, (1, 1, 1): 1})]
    assert rank(a12 + a13) == 4
    assert rank(a12 + a13 + a23_skew) == 4
    assert rank(a12 + a13 + a23_symmetric) == 6


def quartic_vieta_check():
    # B_++B_-=-4s^2+6p and normalization give
    # q4=(-4s^2+6p)/4=-sum alpha^4-p/2.
    for values in ((F(1), F(1), F(0)),
                   (F(2), F(1), F(0)),
                   (F(3), F(2), F(1))):
        squares = [x * x for x in values]
        s = sum(squares)
        p = sum(squares[i] * squares[j]
                for i in range(3) for j in range(i + 1, 3))
        left = (-4 * s * s + 6 * p) / 4
        right = -sum(x * x for x in squares) - p / 2
        assert left == right < 0


def main():
    incidence_check()
    polynomial_gram_block()
    quartic_vieta_check()
    print("exact product zero-cone incidence certificate passed")
    print("universal compatible-Bell quartic block passed")
    print("quartic coefficient is strictly negative off the rank-one branch")


if __name__ == "__main__":
    main()
