#!/usr/bin/env python3
"""Exact symbolic certificates for the symmetric two-portal tradeoff."""

from __future__ import annotations

import sympy as sp


def checked_zero(expr: sp.Expr, label: str) -> None:
    value = sp.factor(sp.cancel(expr))
    if value != 0:
        raise AssertionError(f"{label}: {value}")
    print(f"PASS {label}")


def main() -> None:
    r, c, g, q, y, x = sp.symbols("r c g q y x", positive=True)
    one_minus_g = 1 - g

    # Bd episode PGF on portal counts 1,2.
    beta_b = r**2 * one_minus_g / (r + 1)
    a0 = 2 * c + g
    a1 = r * g
    u = 1 - q
    f2_b = 4 * c / (4 * c + 2 * beta_b * u)  # multiplier of F1
    f1_b = sp.factor(a0 / (a0 + a1 + beta_b * u - a1 * f2_b))
    F_b = sp.factor(
        a0 * (4 * c + 2 * beta_b * u)
        / ((a0 + a1 + beta_b * u) * (4 * c + 2 * beta_b * u) - 4 * c * a1)
    )
    checked_zero(f1_b - F_b, "Bd two-state episode PGF")
    checked_zero(F_b.subs(q, 1) - 1, "Bd PGF normalization")

    kappa_b = 2 * r * (r + 1) * c / one_minus_g
    D_b = sp.factor(1 / (1 + kappa_b * (1 - F_b)))
    q0_b = 1 / r**2
    bd_test = sp.factor(sp.together(q0_b - D_b.subs(q, q0_b)))
    bd_expected_numerator = (
        (r - 1) ** 2
        * (r + 1)
        * (2 * c + g - 1)
        * (2 * c + 2 * g + r - 1)
    )
    bd_numerator, _ = bd_test.as_numer_denom()
    checked_zero(bd_numerator - bd_expected_numerator, "Bd amplification-test numerator")

    # dB episode PGF on portal counts 1,2.
    h = 1 + (r - 1) * g
    a = r * g / h
    b0 = one_minus_g / h
    beta_d = r * c
    f2_d = b0 / (b0 + beta_d * u)  # multiplier of F1
    f1_d = sp.factor(1 / (1 + a + beta_d * u - a * f2_d))
    F_d = sp.factor(
        (b0 + beta_d * u)
        / ((1 + a + beta_d * u) * (b0 + beta_d * u) - a * b0)
    )
    checked_zero(f1_d - F_d, "dB two-state episode PGF")
    checked_zero(F_d.subs(q, 1) - 1, "dB PGF normalization")

    D_d = sp.factor(c / (c + r**2 * one_minus_g * (1 - F_d)))
    q0_d = (2 - r) / r
    # q0-D(q0) has the sign of this cross-multiplied expression, whose
    # denominator is manifestly positive in the probabilistic formula.
    H0_d = sp.factor(1 - F_d.subs(q, q0_d))
    cross_d = sp.factor(q0_d * (c + r**2 * one_minus_g * H0_d) - c)
    raw_num, raw_den = sp.together(cross_d).as_numer_denom()
    # Remove the known positive prefactor 2*c*(r-1)^2/r and retain E.
    E = sp.factor(raw_num / (2 * c * (r - 1) ** 2))
    checked_zero(raw_num - 2 * c * (r - 1) ** 2 * E, "dB test extraction")

    shift = (1 - g) / 2
    B = r * ((r - 1) ** 2 + 1)
    E_shifted = -(
        (1 - g)
        * (r - 1)
        * (r**2 + g**2 + r * (r - 1) ** 2 * g * (1 - g))
        + 2 * h * (B * (1 - g) + 2 * g) * x
        + 4 * (r - 1) * h * x**2
    )
    checked_zero(E.subs(c, shift + x) - E_shifted, "manifestly negative shifted dB certificate")

    # Special exact r=8/5 certificate used in reconnaissance.
    special = sp.factor(E_shifted.subs(r, sp.Rational(8, 5)))
    special_expected = (
        -12 * (3 * g + 5) * x**2 / 25
        + 4 * (3 * g + 5) * (11 * g - 136) * x / 625
        + 3 * (g - 1) * (53 * g**2 + 72 * g + 320) / 625
    )
    checked_zero(special - special_expected, "r=8/5 signed quadratic")

    # Post-establishment portal stationary odds and blade drift ratios.
    u0_b = 4 * r * c * y
    d1_b = 2 * c * (1 - y) + g
    u1_b = 2 * r * c * y + r * g
    d2_b = 4 * c * (1 - y)
    ratio10_b = u0_b / d1_b
    ratio21_b = u1_b / d2_b
    portal_odds_b = sp.factor(
        (ratio10_b + 2 * ratio10_b * ratio21_b)
        / (2 + ratio10_b)
    )
    drift_b = sp.factor(r**2 * (1 - y) * portal_odds_b / y)
    drift_b_expected = sp.factor(
        r**3
        * (2 * c * (1 + (r - 1) * y) + g * r)
        / (2 * c * (1 + (r - 1) * y) + g)
    )
    checked_zero(drift_b - drift_b_expected, "Bd post-establishment drift ratio")

    theta = g / (1 - g)
    u0_d = 2 * r * y / (r * y + 1 - y + theta)
    d1_d = (1 - y + theta) / (r * y + 1 - y + theta)
    u1_d = r * (y + theta) / (r * (y + theta) + 1 - y)
    d2_d = 2 * (1 - y) / (r * (y + theta) + 1 - y)
    ratio10_d = u0_d / d1_d
    ratio21_d = u1_d / d2_d
    portal_odds_d = sp.factor(
        (ratio10_d + 2 * ratio10_d * ratio21_d)
        / (2 + ratio10_d)
    )
    drift_d = sp.factor(r**2 * (1 - y) * portal_odds_d / y)
    drift_d_expected = sp.factor(
        r**3
        * (1 + (r - 1) * (y + g * (1 - y)))
        / (1 + (r - 1) * y * (1 - g))
    )
    checked_zero(drift_d - drift_d_expected, "dB post-establishment drift ratio")

    # raw_den is recorded only to make accidental cancellation visible.  Its
    # positivity follows directly from the positive-rate PGF representation.
    if raw_den == 0:
        raise AssertionError("dB test denominator vanished identically")
    print("PASS dB probabilistic denominator retained")
    print("ALL TWO-PORTAL CERTIFICATES PASS")


if __name__ == "__main__":
    main()
