#!/usr/bin/env python3
"""Exact replay of the temperature-adjoint scalar-combination obstruction.

This script uses symbolic arithmetic only.  It reconstructs the physical
two-state endpoint tangent, the two reciprocal identities through quadratic
order, the common negative remainder, and the projected Farkas witness.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def coeff(expr: sp.Expr, epsilon: sp.Symbol, order: int) -> sp.Expr:
    """Return an exact Taylor coefficient at epsilon=0."""

    return sp.factor(
        sp.diff(expr, epsilon, order).subs(epsilon, 0) / sp.factorial(order)
    )


def assert_zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.cancel(expr)) == 0


def average(weight: sp.Matrix, value: sp.Matrix) -> sp.Expr:
    return sp.Add(*(weight[i] * value[i] for i in range(value.rows)))


def main() -> None:
    r, lam, epsilon = sp.symbols("r lam epsilon", real=True)
    c = r - 1

    one = sp.ones(2, 1)
    f = sp.Matrix([1, -1])
    pi = sp.Rational(1, 2) * one
    P = sp.Matrix(
        [
            [(1 + lam) / 2, (1 - lam) / 2],
            [(1 - lam) / 2, (1 + lam) / 2],
        ]
    )
    a = one + epsilon * f
    diagonal_a = sp.diag(*a)
    R = diagonal_a.inv() * P * diagonal_a
    t = diagonal_a.inv() * P * a
    p = sp.Matrix([pi[i] * a[i] for i in range(2)])
    p_dagger = sp.Matrix([p[i] * t[i] for i in range(2)])

    # Exact temperature-adjoint normalization and edge reversal.
    assert_zero(sum(p_dagger) - 1)
    assert all(
        assert_zero(p_dagger[i] - pi[i] * (1 + lam * epsilon * f[i])) is None
        for i in range(2)
    )
    P_dagger = sp.diag(*[1 / t[i] for i in range(2)]) * R
    R_dagger = sp.diag(*[1 / t[i] for i in range(2)]) * P
    for i in range(2):
        assert_zero(sum(P_dagger[i, j] for j in range(2)) - 1)
        assert_zero(sum(R_dagger[i, j] for j in range(2)) - 1 / t[i])
        for j in range(2):
            assert_zero(
                p_dagger[i] * P_dagger[i, j]
                - p_dagger[j] * R_dagger[j, i]
            )
    # Lightweight exact replay of the common-edge orientation used for A^dagger.
    x0, x1, y0, y1 = sp.symbols("x0 x1 y0 y1")
    x = sp.Matrix([x0, x1])
    y = sp.Matrix([y0, y1])
    adjoint_left = average(p, y.multiply_elementwise(R * x))
    adjoint_edge = sp.Add(
        *(p[i] * P[i, j] * x[i] * y[j] for i in range(2) for j in range(2))
    )
    assert_zero(adjoint_left - adjoint_edge)

    # Claimed endpoint coefficients.
    q0 = 1 / r
    Q = c * (lam - 1) / (r * (r - lam))
    Q2 = -(lam - 1) * c * (r - lam**2) / (r * (r - lam) ** 2)
    H2 = lam * (lam - 1) * c**2 / (r * (r - lam) ** 2)
    q = q0 * one + epsilon * Q * f + epsilon**2 * Q2 * one
    h = q0 * one - epsilon * Q * f + epsilon**2 * H2 * one
    b = one - q
    s = one - h

    # Replay both endpoint equations through quadratic order.
    bd_residual = sp.Matrix(
        [t[i] * b[i] - r * q[i] * (P * b)[i] for i in range(2)]
    )
    db_residual = sp.Matrix(
        [s[i] - r * h[i] * (R * s)[i] for i in range(2)]
    )
    for residual in (bd_residual, db_residual):
        for i in range(2):
            for order in range(3):
                assert_zero(coeff(residual[i], epsilon, order))

    d = c * q - s
    d_dagger = c * h - b
    for i in range(2):
        assert_zero(d[i] - d_dagger[i] - (r - 2) * (q[i] - h[i]))

    D = (r - 2) * Q
    L = -Q * (1 + lam * (r - 2) / r)
    for i in range(2):
        assert_zero(coeff(d[i], epsilon, 1) - D * f[i])
        assert_zero(coeff(d_dagger[i], epsilon, 1) + D * f[i])

    h1 = sp.Matrix([1 / (1 + r * c * (R * q)[i]) for i in range(2)])
    q1 = sp.Matrix(
        [t[i] / (t[i] + r * c * (P * h)[i]) for i in range(2)]
    )
    for i in range(2):
        assert_zero(coeff(h1[i], epsilon, 0) - q0)
        assert_zero(coeff(q1[i], epsilon, 0) - q0)
        assert_zero(coeff(h1[i], epsilon, 1) - L * f[i])
        assert_zero(coeff(q1[i], epsilon, 1) + L * f[i])
        assert_zero(
            coeff(h[i] - h1[i], epsilon, 1) - lam * D * f[i] / r
        )
        assert_zero(
            coeff(q[i] - q1[i], epsilon, 1) + lam * D * f[i] / r
        )

    # Means and the common physical mean-residual coefficient.
    M = average(p, d)
    M_dagger = average(p_dagger, d_dagger)
    M2 = (lam - 1) ** 2 * c * (r + lam * c) / (r * (r - lam) ** 2)
    assert_zero(coeff(M, epsilon, 2) - (H2 + c * Q2 + D))
    assert_zero(coeff(M_dagger, epsilon, 2) - (Q2 + c * H2 - lam * D))
    assert_zero(coeff(M, epsilon, 2) - M2)
    assert_zero(coeff(M_dagger, epsilon, 2) - M2)

    # Reciprocal gaps, cross terms, and positive squares.
    G = average(p, h - h1)
    G_dagger = average(p_dagger, q - q1)
    U = c * average(p, q) - average(p, one - h1)
    U_dagger = c * average(p_dagger, h) - average(p_dagger, one - q1)

    h1_squared = sp.Matrix([h1[i] ** 2 for i in range(2)])
    q1_squared = sp.Matrix([q1[i] ** 2 for i in range(2)])
    A = average(p, d.multiply_elementwise(P * h1_squared))
    A_dagger = average(p, d_dagger.multiply_elementwise(R * q1_squared))
    square = average(
        p, sp.Matrix([(h[i] - h1[i]) ** 2 / h[i] for i in range(2)])
    )
    square_dagger = average(
        p_dagger,
        sp.Matrix([(q[i] - q1[i]) ** 2 / q[i] for i in range(2)]),
    )

    cross2 = M2 / r**2 + 2 * D * L * lam / r
    square2 = lam**2 * D**2 / r
    assert_zero(coeff(A, epsilon, 2) - cross2)
    assert_zero(coeff(A_dagger, epsilon, 2) - cross2)
    assert_zero(coeff(square, epsilon, 2) - square2)
    assert_zero(coeff(square_dagger, epsilon, 2) - square2)
    assert_zero(coeff(G - r * A - square, epsilon, 2))
    assert_zero(coeff(G_dagger - r * A_dagger - square_dagger, epsilon, 2))

    C = 2 * D * L * lam + square2
    C_factored = (
        -lam
        * (lam - 1) ** 2
        * (r - 2)
        * c**2
        * (2 * r + lam * (r - 2))
        / (r**3 * (r - lam) ** 2)
    )
    assert_zero(C - C_factored)
    assert_zero(coeff(G, epsilon, 2) - (M2 / r + C))
    assert_zero(coeff(G_dagger, epsilon, 2) - (M2 / r + C))
    assert_zero(coeff(U, epsilon, 2) - (c * M2 / r - C))
    assert_zero(coeff(U_dagger, epsilon, 2) - (c * M2 / r - C))

    # Exact interval replay.  Write r=3/2+z/100 with 0<=z<=1 and
    # lambda=-u with 0<u<=1.  Then -lambda=u>0, r-2=-(50-z)/100<0,
    # and the following decomposition proves the remaining bracket positive.
    bracket = 2 * r + lam * (r - 2)
    assert_zero(C_factored - C)
    assert sp.factor(bracket - 2 * r) == lam * (r - 2)
    z, u = sp.symbols("z u", real=True)
    r_strip = sp.Rational(3, 2) + z / 100
    lam_strip = -u
    bracket_strip = sp.factor(bracket.subs({r: r_strip, lam: lam_strip}))
    assert_zero(
        bracket_strip
        - (3 + z / 50 + u * (49 + (1 - z)) / 100)
    )

    # The physical mean coefficient is positive because
    # r+lambda*c = 1+(r-1)(1-u) >= 1 on the same box.
    assert_zero(
        (r + lam * c).subs({r: r_strip, lam: lam_strip})
        - (1 + (r_strip - 1) * (1 - u))
    )

    # The actual physical tangent has positive G2.  Its remaining numerator
    # is concave in lambda, so it suffices to inspect lambda=-1 and lambda=0.
    N = r * (r + lam * c) - lam * (r - 2) * c * bracket
    assert_zero(
        sp.Poly(sp.expand(N), lam).coeff_monomial(lam**2)
        + (r - 2) ** 2 * c
    )
    assert_zero(N.subs(lam, 0) - r**2)
    N_minus_one = r**3 - r**2 - 3 * r + 4
    assert_zero(N.subs(lam, -1) - N_minus_one)
    assert_zero(
        N_minus_one
        - sp.Rational(5, 8)
        - (2 * r - 3) * (4 * r**2 + 2 * r - 9) / 8
    )
    assert_zero(4 * r**2 + 2 * r - 9 - (3 + (2 * r - 3) * (2 * r + 4)))
    G2_positive_form = c * (lam - 1) ** 2 * N / (r**3 * (r - lam) ** 2)
    assert_zero(coeff(G, epsilon, 2) - G2_positive_form)

    # Exact Farkas witness in the projected scalar relaxation.  At m=m*=0,
    # both premise rows equal -C while the target row equals C.
    m_witness = sp.Integer(0)
    m_dagger_witness = sp.Integer(0)
    U_witness = c * m_witness / r - C
    U_dagger_witness = c * m_dagger_witness / r - C
    target_witness = m_witness / r + C
    assert_zero(U_witness + C)
    assert_zero(U_dagger_witness + C)
    assert_zero(target_witness - C)
    assert m_witness == m_dagger_witness

    theorem = HERE / "ENDPOINT_ADJOINT_COMBINATION_OBSTRUCTION.md"
    digest = hashlib.sha256(theorem.read_bytes()).hexdigest()
    print("PASS: exact two-orientation endpoint expansion")
    print("PASS: common reciprocal remainder C is strictly negative on the strip")
    print("PASS: projected Farkas witness; physical tangent has G_2 > 0")
    print(f"theorem_sha256={digest}")


if __name__ == "__main__":
    main()
