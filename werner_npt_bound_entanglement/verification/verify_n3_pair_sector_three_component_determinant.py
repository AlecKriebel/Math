#!/usr/bin/env python3
"""Exact checks for the three-component determinant reduction.

Only Python's standard library is used.  The script checks:

1. the coefficient identity
       (2/3)||C||^2 - w1 = (2/3)Q2(C) + (1/2)w0;
2. the sharp tensor-product example;
3. the exact formal determinant of the Hermitian deficit matrix;
4. the old cyclic-budget obstruction against the new 2x2 theorem.
"""

from fractions import Fraction as F
from itertools import permutations


def add_poly(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, F(0)) + coefficient
        if out[monomial] == 0:
            del out[monomial]
    return out


def mul_poly(left, right):
    out = {}
    for m1, a in left.items():
        for m2, b in right.items():
            monomial = tuple(x + y for x, y in zip(m1, m2))
            out[monomial] = out.get(monomial, F(0)) + a * b
    return {m: a for m, a in out.items() if a}


def scale_poly(value, scalar):
    return {m: scalar * a for m, a in value.items() if scalar * a}


NVAR = 9


def variable(index):
    exponent = [0] * NVAR
    exponent[index] = 1
    return {tuple(exponent): F(1)}


def parity_of_permutation(p):
    inversions = sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
    return -1 if inversions % 2 else 1


def determinant3(matrix):
    out = {}
    for p in permutations(range(3)):
        term = {(0,) * NVAR: F(parity_of_permutation(p))}
        for row in range(3):
            term = mul_poly(term, matrix[row][p[row]])
        out = add_poly(out, term)
    return out


def main():
    # Sector order is w0,w1,w2.
    lhs = (F(2, 3), F(-1, 3), F(2, 3))
    q2 = (F(1, 4), F(-1, 2), F(1))
    rhs = (
        F(2, 3) * q2[0] + F(1, 2),
        F(2, 3) * q2[1],
        F(2, 3) * q2[2],
    )
    assert lhs == rhs

    # Sharp example E_01 tensor diag(1,1,0).
    norm_e_squared = F(1)
    norm_r_squared = F(2)
    trace_r = F(2)
    scalar_r_squared = trace_r * trace_r / F(3)
    total_squared = norm_e_squared * norm_r_squared
    degree_one_squared = norm_e_squared * scalar_r_squared
    assert total_squared == F(2)
    assert degree_one_squared == F(4, 3)
    assert degree_one_squared == F(2, 3) * total_squared

    # Formal Hermitian determinant.  Variables are
    # d1,d2,d3,c12,c12bar,c13,c13bar,c23,c23bar.
    d1, d2, d3, c12, c12b, c13, c13b, c23, c23b = [
        variable(i) for i in range(NVAR)
    ]
    matrix = [
        [d1, scale_poly(c12, -1), scale_poly(c13, -1)],
        [scale_poly(c12b, -1), d2, scale_poly(c23, -1)],
        [scale_poly(c13b, -1), scale_poly(c23b, -1), d3],
    ]
    computed = determinant3(matrix)

    expected = mul_poly(mul_poly(d1, d2), d3)
    expected = add_poly(expected, scale_poly(mul_poly(d1, mul_poly(c23, c23b)), -1))
    expected = add_poly(expected, scale_poly(mul_poly(d2, mul_poly(c13, c13b)), -1))
    expected = add_poly(expected, scale_poly(mul_poly(d3, mul_poly(c12, c12b)), -1))
    expected = add_poly(
        expected,
        scale_poly(mul_poly(mul_poly(c12, c23), c13b), -1),
    )
    expected = add_poly(
        expected,
        scale_poly(mul_poly(mul_poly(c12b, c23b), c13), -1),
    )
    assert computed == expected

    # Previous exact obstruction: the 2x2 deficit matrix is PSD even
    # though the symmetric half-budget edge form was negative.
    d_1, d_3, c_13 = F(10), F(16), F(8)
    assert d_1 >= 0 and d_3 >= 0
    assert d_1 * d_3 - c_13 * c_13 == F(96) > 0
    half_budget = (d_1 + d_3) / 2 - 2 * c_13
    assert half_budget == F(-3)

    print("three-component determinant reduction: exact checks passed")


if __name__ == "__main__":
    main()
