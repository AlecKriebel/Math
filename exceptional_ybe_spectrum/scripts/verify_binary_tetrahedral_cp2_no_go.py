#!/usr/bin/env python3
"""Exact exclusion of the full binary-tetrahedral CP^2 d=6 branch.

This verifier uses three entries of the 72 by 72 shifted cubic residual.  It
does not use the numerical optimizer or its objective implementation.
"""

from __future__ import annotations

import sympy as sp


I = sp.I
SQRT2 = sp.sqrt(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -I], [I, 0]])
Z = sp.diag(1, -1)
EPS = sp.Matrix([[0, 1], [-1, 0]])


def vec_pair(matrix):
    return sp.Matrix(
        [matrix[a, c] for a in range(2) for c in range(2)]
    )


def embed_pair_b(pair_state, b):
    out = sp.zeros(12, 1)
    for a in range(2):
        for c in range(2):
            out[(a * 3 + b) * 2 + c] = pair_state[2 * a + c]
    return out


def invariant_isometries():
    singlet = vec_pair(EPS / SQRT2)
    triplet = [vec_pair(pauli * EPS / SQRT2) for pauli in (X, Y, Z)]
    u0 = sp.Matrix.hstack(
        *(embed_pair_b(singlet, k) for k in range(3))
    )
    anti_columns = []
    sym_columns = []
    for k in range(3):
        anti = sp.zeros(12, 1)
        sym = sp.zeros(12, 1)
        for p in range(3):
            for b in range(3):
                epsilon = sp.LeviCivita(k, p, b)
                if epsilon:
                    anti += epsilon * embed_pair_b(triplet[p], b) / SQRT2
                if k != p and k != b and p != b:
                    sym += embed_pair_b(triplet[p], b) / SQRT2
        anti_columns.append(anti)
        sym_columns.append(sym)
    u1 = sp.Matrix.hstack(*anti_columns)
    u2 = sp.Matrix.hstack(*sym_columns)
    diag = sp.Matrix.hstack(
        *(embed_pair_b(triplet[k], k) for k in range(3))
    )
    full = sp.Matrix.hstack(diag, u0, u1, u2)
    assert sp.simplify(full.conjugate().T * full) == sp.eye(12)
    return diag, (u0, u1, u2)


def sparse_rows(matrix):
    rows = [[] for _ in range(matrix.rows)]
    for (i, j), value in matrix.todok().items():
        rows[i].append((j, value))
    return rows


def triple_entry(left_rows, middle_rows, right, i, j):
    value = 0
    for p, left_value in left_rows[i]:
        for q, middle_value in middle_rows[p]:
            right_value = right[q, j]
            if right_value:
                value += left_value * middle_value * right_value
    return value


def residual_entry(k1, k2, rows1, rows2, i, j):
    return (
        triple_entry(rows1, rows2, k1, i, j)
        - triple_entry(rows2, rows1, k2, i, j)
        - (k1[i, j] - k2[i, j]) / 3
    )


def polynomial_remainder(expression, divisor, variables):
    return sp.Poly(
        expression, *variables, extension=[I, sp.sqrt(2), sp.sqrt(3)]
    ).rem(
        sp.Poly(
            divisor, *variables, extension=[I, sp.sqrt(2), sp.sqrt(3)]
        )
    ).as_expr()


def main():
    diag, copies = invariant_isometries()
    a, b, c, d, e = sp.symbols("a b c d e", real=True)
    variables = (a, b, c, d, e)
    z = (a, b + I * c, d + I * e)
    w = sum(
        (z[j] * copies[j] for j in range(3)), sp.zeros(12, 3)
    )
    p = diag * diag.conjugate().T + w * w.conjugate().T
    k = sp.SparseMatrix(2 * p - sp.eye(12))
    k1 = sp.kronecker_product(k, sp.eye(6))
    k2 = sp.kronecker_product(sp.eye(6), k)
    rows1 = sparse_rows(k1)
    rows2 = sparse_rows(k2)

    f22 = residual_entry(k1, k2, rows1, rows2, 2, 2)
    f55 = residual_entry(k1, k2, rows1, rows2, 5, 5)
    f5720 = residual_entry(k1, k2, rows1, rows2, 57, 20)

    norm_relation = a**2 + b**2 + c**2 + d**2 + e**2 - 1
    expected22 = -sp.Rational(4, 3) * (b * d + c * e)
    expected55 = (
        b**2
        + c**2
        + d**2
        + e**2
        - sp.Rational(2, 3) * (b * d + c * e)
        - sp.Rational(2, 3)
    )
    assert polynomial_remainder(
        f22 - expected22, norm_relation, variables
    ) == 0
    assert polynomial_remainder(
        f55 - expected55, norm_relation, variables
    ) == 0

    # If the residual vanished, these two diagonal entries and normalization
    # would force
    #
    #   bd+ce=0,  b^2+c^2+d^2+e^2=2/3,  a^2=1/3.
    #
    # A projective phase makes a=1/sqrt(3).  Orthogonal real vectors
    # (b,c) and (d,e) can then be written as
    #
    #   (b,c)=r(x,y), (d,e)=epsilon*s(-y,x),
    #
    # where r^2+s^2=2/3, x^2+y^2=1, epsilon=+/-1.
    r, s, x, y = sp.symbols("r s x y", real=True)
    circle_rs = r**2 + s**2 - sp.Rational(2, 3)
    circle_xy = x**2 + y**2 - 1
    for epsilon in (1, -1):
        specialized = sp.expand(
            f5720.subs(
                {
                    a: 1 / sp.sqrt(3),
                    b: r * x,
                    c: r * y,
                    d: -epsilon * s * y,
                    e: epsilon * s * x,
                }
            )
        )
        specialized = sp.rem(specialized, circle_rs, r)
        specialized = sp.rem(specialized, circle_xy, x)
        expected = (
            -2
            * sp.sqrt(6)
            * I
            * (x - I * y)
            / 27
            * (
                r * (6 * s**2 - 1)
                + epsilon * I * s * (6 * s**2 - 3)
            )
        )
        expected = sp.rem(sp.expand(expected), circle_rs, r)
        expected = sp.rem(sp.expand(expected), circle_xy, x)
        assert sp.expand(specialized - expected) == 0

        modulus_squared = sp.expand_complex(
            expected * sp.conjugate(expected)
        )
        modulus_squared = sp.rem(
            sp.expand(modulus_squared), circle_rs, r
        )
        modulus_squared = sp.rem(
            sp.expand(modulus_squared), circle_xy, x
        )
        assert sp.simplify(modulus_squared - sp.Rational(16, 729)) == 0

    print("normalization=|z|^2=1")
    print("F[2,2]=-4*(b*d+c*e)/3")
    print(
        "F[5,5]=|z1|^2+|z2|^2-2*Re(conj(z1)*z2)/3-2/3"
    )
    print("forced_conditions=a^2=1/3,Re(conj(z1)*z2)=0")
    print("under_forced_conditions=|F[57,20]|^2=16/729")
    print("binary_tetrahedral_CP2_branch_has_no_solution=true")


if __name__ == "__main__":
    main()
