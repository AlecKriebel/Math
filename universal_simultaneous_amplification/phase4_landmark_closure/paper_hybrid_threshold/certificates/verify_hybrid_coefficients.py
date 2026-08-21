#!/usr/bin/env python3
"""Exact symbolic audit of the dilute hybrid correction coefficients."""

from __future__ import annotations

import sympy as sp


def sturm_count(poly, variable, left, right):
    sequence = sp.sturm(poly, variable)

    def variations(point):
        signs = []
        for entry in sequence:
            value = sp.sign(entry.subs(variable, point))
            assert value in (-1, 0, 1)
            if value:
                signs.append(int(value))
        return sum(a != b for a, b in zip(signs, signs[1:]))

    return variations(left) - variations(right)


def main():
    r, sigma, lam = sp.symbols("r sigma lam", positive=True)
    p = (r - 1) / r

    # Direct rare-invasion rates after the common positive factors are
    # removed.  The K2-local establishment probabilities are r/(r+1) for Bd
    # and 1/2 for dB.
    A_b, D_b = 2 * sigma * (r - 1), 2 / (r + 1)
    pi_b = sp.factor(A_b / (A_b + D_b))
    A_d, D_d = 2 * (r - 1), sigma / r
    pi_d = sp.factor(A_d / (A_d + D_d))

    F_b = sp.factor(-2 + 2 * (r / (r + 1)) * pi_b / p)
    F_d = sp.factor(-2 + pi_d / p)
    expected_b = 2 * (sigma - 1) / (1 + sigma * (r**2 - 1))
    expected_d = 2 * (r * (2 - r) - sigma) / (
        sigma + 2 * r * (r - 1)
    )
    assert sp.factor(F_b - expected_b) == 0
    assert sp.factor(F_d - expected_d) == 0

    G_b = sp.factor(F_b + lam / (r - 1))
    G_d = sp.factor(F_d - lam)
    lower = sp.factor(-(r - 1) * F_b)
    upper = sp.factor(F_d)
    assert sp.factor(G_b - (lam - lower) / (r - 1)) == 0
    assert sp.factor(G_d - (upper - lam)) == 0

    # A family with entirely rational edge weights already crosses 3/2.
    rational_sigma, rational_lam = sp.Rational(19, 137), sp.Rational(20, 27)
    endpoint_b = sp.factor(G_b.subs({r: sp.Rational(3, 2), sigma: rational_sigma, lam: rational_lam}))
    endpoint_d = sp.factor(G_d.subs({r: sp.Rational(3, 2), sigma: rational_sigma, lam: rational_lam}))
    assert endpoint_b == sp.Rational(232, 17361)
    assert endpoint_d == sp.Rational(65, 12123)
    rational_b = sp.factor(G_b.subs({sigma: rational_sigma, lam: rational_lam}))
    rational_d = sp.factor(G_d.subs({sigma: rational_sigma, lam: rational_lam}))
    assert sp.factor(rational_b - 4 * (95 * r**2 - 1593 * r + 2183) / (
        27 * (r - 1) * (19 * r**2 + 118)
    )) == 0
    assert sp.factor(rational_d + 2 * (6439 * r**2 - 10138 * r + 703) / (
        27 * (274 * r**2 - 274 * r + 19)
    )) == 0
    rational_threshold = (sp.Integer(5069) + 12 * sp.sqrt(147001)) / 6439
    assert sp.factor(6439 * rational_threshold**2 - 10138 * rational_threshold + 703) == 0
    assert sp.Rational(3, 2) < rational_threshold < sp.Rational(151, 100)
    assert rational_b.subs(r, rational_threshold) > 0

    # Optimize the two-parameter leading family.  Equality of the lower and
    # upper admissible lambda bounds is quadratic in sigma.  Its discriminant
    # is the displayed degree-six phase polynomial.
    phase = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    equality_numerator = sp.factor(sp.together(lower - upper).as_numer_denom()[0])
    assert sp.factor(sp.discriminant(equality_numerator, sigma) - 4 * r**2 * phase) == 0
    assert sturm_count(phase, r, sp.Rational(3, 2), sp.Rational(151, 100)) == 1
    # There are only two real roots; the smaller is the desired one.
    assert sturm_count(phase, r, -100, 100) == 2

    real_roots = [root for root in sp.nroots(phase, n=50) if abs(sp.im(root)) < sp.Rational(1, 10) ** 40]
    small = min(real_roots, key=lambda value: abs(sp.re(value) - sp.Rational(3, 2)))
    assert sp.Rational(3, 2) < sp.re(small) < sp.Rational(151, 100)
    R_decimal = sp.re(small)
    sigma_decimal = (-R_decimal**3 + 4 * R_decimal**2 - 3 * R_decimal - 1) / (2 * (R_decimal - 1))
    lambda_decimal = lower.subs({r: R_decimal, sigma: sigma_decimal})
    assert abs(float(R_decimal) - 1.5028569127905696) < 1e-15
    assert abs(float(sigma_decimal) - 0.13067728228704838) < 1e-15
    assert abs(float(lambda_decimal) - 0.7508064830318805) < 1e-15

    # The exact algebraic definitions use the unique root in the rational
    # isolating interval.  Substitution modulo the phase polynomial verifies
    # the double-root sigma identity without relying on decimals.
    sigma_star = (-r**3 + 4 * r**2 - 3 * r - 1) / (2 * (r - 1))
    remainder = sp.rem(
        sp.together(equality_numerator.subs(sigma, sigma_star)).as_numer_denom()[0],
        phase,
        domain=sp.QQ,
    )
    assert remainder == 0
    derivative_remainder = sp.rem(
        sp.together(sp.diff(equality_numerator, sigma).subs(sigma, sigma_star)).as_numer_denom()[0],
        phase,
        domain=sp.QQ,
    )
    assert derivative_remainder == 0

    print(f"rational endpoint margins: Bd={endpoint_b}, dB={endpoint_d}")
    print(f"rational-edge-family threshold ~{float(rational_threshold):.15g}")
    print(f"optimized phase root ~{float(R_decimal):.15g}")
    print(f"optimized sigma ~{float(sigma_decimal):.15g}, lambda ~{float(lambda_decimal):.15g}")
    print("PASS exact hybrid coefficient and phase-polynomial audit")


if __name__ == "__main__":
    main()
