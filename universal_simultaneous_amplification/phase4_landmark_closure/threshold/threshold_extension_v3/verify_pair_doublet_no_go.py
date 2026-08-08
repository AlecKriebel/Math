#!/usr/bin/env python3
"""Exact certificate for the symmetric correlated-pair tangent obstruction."""

from __future__ import annotations

import sympy as sp


def sign_without_roots(poly: sp.Expr, variable: sp.Symbol, left: sp.Rational, right: sp.Rational, sign: int) -> None:
    polynomial = sp.Poly(poly, variable, domain=sp.QQ)
    assert sp.count_roots(polynomial, left, right) == 0
    value = sp.sign(polynomial.eval(left))
    assert value == sign, (polynomial, value, sign)


def main() -> None:
    r, sigma, u = sp.symbols("r sigma u", positive=True)
    left, right = sp.Rational(3, 2), sp.Rational(151, 100)

    # Solve the exact three-state trace (one mutant pair, two mutant pairs,
    # and successful center establishment) independently.
    A, D, m, q, h1, h2 = sp.symbols("A D m q h1 h2", positive=True)
    solution = sp.solve(
        [
            (A + D + q + m) * h1 - A - m * h2,
            (A + D) * h2 - A - D * h1,
        ],
        [h1, h2],
        dict=True,
    )[0]
    generic_h = A * (A + D + m) / ((A + D) * (A + D + q) + m * A)
    assert sp.factor(solution[h1] - generic_h) == 0

    def H(z: sp.Expr, theta: sp.Expr) -> sp.Expr:
        return z * (z + 1 + r**2 * theta) / (
            (z + 1) ** 2 + theta * (1 + (1 + r**2) * z)
        )

    # Direct Bd/dB event sums give m/q=r^2.  With u=2 times the
    # inter-pair/core weak-load ratio, the two center-hit odds and conflict
    # intensities are as displayed below.
    z_bd = sigma * (r**2 - 1)
    z_db = 2 * r * (r - 1) / sigma
    h_bd = H(z_bd, sigma * u)
    h_db = H(z_db, u)

    # Full singleton-normalized separator per pair vertex, including the
    # far-field subtraction -r.
    separator = sp.together(
        r * h_db / (2 * (r - 1)) + r**2 * h_bd / (r + 1) - r
    )
    numerator, denominator = separator.as_numer_denom()
    Q = sp.factor(-numerator / r)
    assert sp.factor(numerator + r * Q) == 0
    assert sp.degree(Q, u) == 2

    q0 = sp.factor(sp.Poly(Q, u).coeff_monomial(1))
    q1 = sp.factor(sp.Poly(Q, u).coeff_monomial(u))
    q2 = sp.factor(sp.Poly(Q, u).coeff_monomial(u**2))

    F = (
        (r - 1) * sigma**2
        + (r**3 - 4 * r**2 + 3 * r + 1) * sigma
        + r * (2 * r - 3)
    )
    assert sp.factor(
        q0
        - (r + 1)
        * (2 * r**2 - 2 * r + sigma)
        * (1 + (r**2 - 1) * sigma)
        * F
    ) == 0

    P = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    assert sp.count_roots(P, left, right) == 1
    linear = r**3 - 4 * r**2 + 3 * r + 1
    assert sp.factor(
        4 * (r - 1) * F - (2 * (r - 1) * sigma + linear) ** 2 + P
    ) == 0
    sign_without_roots(linear, r, left, right, -1)

    # q1=sigma*P1(sigma).  Its cubic and the quadratic part are positive:
    # the quadratic has positive leading/constant terms and negative
    # discriminant throughout the isolating interval.
    P1 = sp.factor(q1 / sigma)
    c10 = sp.Poly(P1, sigma).coeff_monomial(1)
    c11 = sp.Poly(P1, sigma).coeff_monomial(sigma)
    c12 = sp.Poly(P1, sigma).coeff_monomial(sigma**2)
    c13 = sp.Poly(P1, sigma).coeff_monomial(sigma**3)
    assert sp.factor(c13 - r * (r - 1) * (r + 1) * (2 * r + 1)) == 0
    g10 = 6 * r**3 - 13 * r**2 + 8 * r - 2
    g12 = r**7 - 4 * r**6 + 7 * r**5 - 4 * r**4 - 3 * r**3 + r**2 + 4 * r - 1
    assert sp.factor(c10 - r * (r + 1) * g10) == 0
    assert sp.factor(c12 - (r + 1) * g12) == 0
    delta1 = sp.factor(c11**2 - 4 * c10 * c12)
    sign_without_roots(g10, r, left, right, 1)
    sign_without_roots(g12, r, left, right, 1)
    sign_without_roots(delta1, r, left, right, -1)

    # q2=sigma^2*P2(sigma), and P2 is a positive quadratic by the same
    # exact discriminant certificate.
    P2 = sp.factor(q2 / sigma**2)
    c20 = sp.Poly(P2, sigma).coeff_monomial(1)
    c21 = sp.Poly(P2, sigma).coeff_monomial(sigma)
    c22 = sp.Poly(P2, sigma).coeff_monomial(sigma**2)
    g20 = 2 * r**3 - 3 * r**2 + 2 * r - 2
    assert sp.factor(c20 - r * (r + 1) * g20) == 0
    assert sp.factor(c22 - (r - 1) * (r + 1) * (r**2 + r + 1)) == 0
    delta2 = sp.factor(c21**2 - 4 * c20 * c22)
    sign_without_roots(g20, r, left, right, 1)
    sign_without_roots(delta2, r, left, right, -1)

    # Denominator positivity is transparent in the unreduced H expressions;
    # this identity ensures the cleared expression used above is the same one.
    rebuilt = sp.together(
        r * H(z_db, u) / (2 * (r - 1))
        + r**2 * H(z_bd, sigma * u) / (r + 1)
        - r
    )
    assert sp.factor(rebuilt - separator) == 0

    print("PASS: exact symmetric correlated-pair trace solved")
    print("PASS: separator numerator is -r*(Q0+u*Q1+u^2*Q2)")
    print("PASS: Q0 is a positive factor times the tangency square at P(r)=0")
    print("PASS: Q1,Q2 are positive by exact Sturm/discriminant certificates")
    print("PASS: equality only at u=0 and sigma=sigma_*")


if __name__ == "__main__":
    main()
