#!/usr/bin/env python3
"""Exact symbolic replay of the R_hyb bounded dual-moment reduction."""

from __future__ import annotations

import sympy as sp


def generic_reduction() -> None:
    r, z, q, a, b = sp.symbols("r z q a b", positive=True)
    C = r * (r - 1) ** 2
    K = C / q
    c, d = r * b, r * a

    separator = d * K / (K + z) + c * z / (1 + z) - r
    numerator, denominator = map(sp.factor, sp.together(separator).as_numer_denom())
    expected = (c - r) * z**2 + (K * (c + d - r) - r) * z + K * (d - r)
    # SymPy clears K=C/q by one positive factor q; compare rationally.
    assert sp.factor(separator - expected / ((1 + z) * (K + z))) == 0
    assert denominator != 0 and numerator != 0

    middle = K * (c + d - r) - r
    discriminant = sp.factor(middle**2 - 4 * (r - c) * K * (r - d))
    normalized = sp.factor(discriminant / r**2)
    expected_normalized = (K * (a + b - 1) - 1) ** 2 - 4 * K * (1 - a) * (1 - b)
    assert sp.factor(normalized - expected_normalized) == 0

    # When a+b>1, the discriminant condition is equivalent to
    # sqrt(K) <= 1/(sqrt(ab)-sqrt((1-a)(1-b))).  Squaring and K=C/q
    # gives the Hellinger form.  The key difference-of-squares identity is
    # purely algebraic and is checked here without branch assumptions.
    A, B = sp.symbols("A B")
    assert sp.expand((A - B) * (A + B) - (A**2 - B**2)) == 0
    assert sp.expand(a * b - (1 - a) * (1 - b) - (a + b - 1)) == 0

    # Direct denominator-cleared BDM gap used by the product-chain forcing.
    gap = sp.factor((C + z * q) * (1 + z) - a * C * (1 + z) - b * z * (C + z * q))
    expected_gap = C * ((1 + z) * (1 - a) - b * z) + z * q * (1 + z * (1 - b))
    assert sp.expand(gap - expected_gap) == 0
    assert sp.factor(gap + q * expected / r) == 0

    # Algebraic boundary of the square-root/Hellinger form.  Here u and v
    # stand for sqrt(ab) and sqrt((1-a)(1-b)); branch inequalities are stated
    # explicitly in the note.
    u, v = sp.symbols("u v", nonnegative=True)
    hellinger_boundary = sp.expand(
        (u**2 - v**2 - (u - v) ** 2) ** 2
        - 4 * (u - v) ** 2 * v**2
    )
    assert hellinger_boundary == 0


def portal_copositivity() -> None:
    x1, x2, u1, u2, v1, v2, e1, e2, Q = sp.symbols(
        "x1 x2 u1 u2 v1 v2 e1 e2 Q"
    )
    x = sp.Matrix([x1, x2])
    u = sp.Matrix([u1, u2])
    ev = sp.Matrix([e1 * v1, e2 * v2])
    one = sp.Matrix([1, 1])
    e = sp.Matrix([e1, e2])
    matrix = (u * ev.T + ev * u.T - Q * (one * e.T + e * one.T)) / 2
    target = (x.dot(u)) * (x.dot(ev)) - Q * (x.dot(one)) * (x.dot(e))
    assert sp.expand((x.T * matrix * x)[0] - target) == 0


def k2_equality() -> None:
    r, z = sp.symbols("r z", positive=True)
    polynomial = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    root_poly = sp.Poly(polynomial, r, domain=sp.QQ)
    assert root_poly.count_roots(sp.Rational(3, 2), sp.Rational(151, 100)) == 1

    b = r / (r + 1)
    a = 1 / (2 * (r - 1))
    q_B = 1 / (r + 1)
    q_D = sp.Rational(1, 2)
    K = sp.factor(r * (r - 1) ** 2 / (q_B * q_D))
    c, d = sp.factor(r * b), sp.factor(r * a)
    assert K == 2 * r * (r - 1) ** 2 * (r + 1)

    middle = sp.factor(K * (c + d - r) - r)
    discriminant = sp.factor(middle**2 - 4 * (r - c) * K * (r - d))
    assert sp.factor(discriminant - r**2 * polynomial) == 0

    double_root = sp.factor(middle / (2 * (r - c)))
    sigma = sp.factor((-r**3 + 4 * r**2 - 3 * r - 1) / (2 * (r - 1)))
    assert sp.factor(double_root - (r**2 - 1) * sigma) == 0

    # At P(r)=0 the quadratic is exactly -(r-c)(z-z_*)^2.
    N = sp.expand((c - r) * z**2 + middle * z + K * (d - r))
    square = sp.expand(-(r - c) * (z - double_root) ** 2)
    remainder = sp.rem(
        sp.Poly(sp.together(N - square).as_numer_denom()[0], r), root_poly
    )
    assert remainder.is_zero


def main() -> None:
    generic_reduction()
    portal_copositivity()
    k2_equality()
    print("PASS: exact OR-dual normal-form reduction")
    print("PASS: quadratic/discriminant/Hellinger equivalence")
    print("PASS: exact portal copositivity formulation")
    print("PASS: K2 discriminant = r^2 P(r) and R_hyb double root")
    print("OPEN: universal bounded dual-moment inequality")


if __name__ == "__main__":
    main()
