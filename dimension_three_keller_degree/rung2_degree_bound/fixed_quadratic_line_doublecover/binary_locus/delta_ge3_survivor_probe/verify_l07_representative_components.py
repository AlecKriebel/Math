#!/usr/bin/env python3
"""Exact checks for the two explicit L07 representatives studied here.

The scope is deliberately narrow: these assertions certify equations and
component descents for the displayed representatives.  They do not certify
that the representatives exhaust L07 or any orbit space.
"""

from __future__ import annotations

import os
import sys

import sympy as sp

import complete_lower_component as base

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, wt = base.p, base.q, base.r, base.wt


def jac2(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p))


def representative_data(R):
    h = (p + q) ** 2
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    alpha = jac2(Q, R)
    beta = -jac2(P, R)
    gamma = jac2(P, Q)
    gcd = sp.gcd(
        sp.gcd(sp.Poly(alpha, p, q), sp.Poly(beta, p, q)),
        sp.Poly(gamma, p, q),
    )
    coefficient_matrix = sp.Matrix(
        [
            [sp.Poly(alpha, p, q).coeff_monomial(p ** (5 - j) * q**j) for j in range(6)],
            [sp.Poly(beta, p, q).coeff_monomial(p ** (5 - j) * q**j) for j in range(6)],
        ]
    )
    assert coefficient_matrix.rank() == 2
    assert gcd.total_degree() == 4
    return P, Q, alpha, beta, gamma, sp.factor(gcd.as_expr())


def e4_after_e6(case_name):
    data = base.build(case_name)
    e4 = base.exponent_coefficients(
        data["determinant"].coeff_monomial(wt**4), 4
    )
    return data, {
        exponent: sp.factor(value.subs(data["substitution6"]))
        for exponent, value in e4.items()
    }


def weighted_determinant(P, Q, R, U, V, T, A, B, L):
    H2 = sp.Matrix([A, B, T])
    H3 = sp.Matrix([U, V, R])
    H4 = sp.Matrix([P, Q, 0])
    return sp.Poly(
        sp.expand(
            (
                L
                + wt * H2.jacobian((p, q, r))
                + wt**2 * H3.jacobian((p, q, r))
                + wt**3 * H4.jacobian((p, q, r))
            ).det()
        ),
        wt,
    )


def check_representatives():
    power_R = (p + q) ** 3
    mixed_R = (p + q) * (2 * p**2 + p * q + 2 * q**2)
    _, _, _, _, _, power_gcd = representative_data(power_R)
    _, _, _, _, _, mixed_gcd = representative_data(mixed_R)
    assert sp.cancel(power_gcd / (p + q) ** 4).free_symbols == set()
    assert sp.cancel(mixed_gcd / (p * q * (p + q) ** 2)).free_symbols == set()
    print("L07_REPRESENTATIVE_GCD_PASS")


def check_mixed_components():
    data_line, e4_line = e4_after_e6("mixed_line")
    assert data_line["rank6"] == 6
    expected = sp.Rational(16, 135) * base.k**4
    assert sp.factor(e4_line[(1, 0, 3)] - expected) == 0
    assert sp.factor(e4_line[(0, 1, 3)] - expected) == 0

    data_zero, e4_zero = e4_after_e6("mixed_zero")
    assert data_zero["rank6"] == 5
    b4, l8 = base.b[4], base.ell[8]
    assert sp.factor(
        e4_zero[(3, 0, 1)]
        - sp.Rational(2, 135) * (15 * b4 + 2 * l8) ** 2
    ) == 0
    assert sp.factor(
        e4_zero[(0, 3, 1)]
        - sp.Rational(10, 27) * (3 * b4 - 2 * l8) ** 2
    ) == 0
    zero_substitution = {b4: 0, l8: 0}
    for variable in (base.a[2], base.a[4], base.a[5], base.b[2], base.b[4], base.b[5]):
        assert sp.factor(
            data_zero["substitution6"][variable].subs(zero_substitution)
        ) == 0
    print("MIXED_COMPONENTS_EXACT_PASS")


def check_power_zero_component():
    data_zero, e4_zero = e4_after_e6("power_zero")
    if os.environ.get("D4_DN3_MUTATE_ORIGIN_SQUARE") == "1":
        e4_zero[(3, 0, 1)] += 1
    assert data_zero["rank6"] == 5
    b4, l8 = base.b[4], base.ell[8]
    assert sp.factor(e4_zero[(3, 0, 1)] - 3 * b4**2) == 0
    assert sp.factor(
        e4_zero[(0, 3, 1)] - sp.Rational(1, 3) * (3 * b4 - 4 * l8) ** 2
    ) == 0
    zero_substitution = {b4: 0, l8: 0}
    for variable in (base.a[2], base.a[4], base.a[5], base.b[2], base.b[4], base.b[5]):
        assert sp.factor(
            data_zero["substitution6"][variable].subs(zero_substitution)
        ) == 0
    print("POWER_ZERO_COMPONENT_EXACT_PASS")


def check_e6_e5_survivor_witnesses():
    h = (p + q) ** 2
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)

    power_R = (p + q) ** 3
    power_U = -p * (p + q) * r
    power_V = q * (p + q) * r
    power_T = 0
    power_A = -4 * p**2 - 2 * p * q - q**2 + sp.Rational(1, 4) * r**2
    power_B = p**2 - 2 * q**2 + sp.Rational(1, 4) * r**2
    power_L = sp.Matrix([[2, 1, 0], [1, -1, -1], [-1, 2, 0]])
    power_det = weighted_determinant(
        P, Q, power_R, power_U, power_V, power_T, power_A, power_B, power_L
    )
    assert power_L.det() == 5
    assert all(power_det.coeff_monomial(wt**degree) == 0 for degree in range(9, 4, -1))
    assert power_det.coeff_monomial(wt**4) != 0

    mixed_R = (p + q) * (2 * p**2 + p * q + 2 * q**2)
    mixed_U = -sp.Rational(2, 3) * p * (p + q) * r
    mixed_V = sp.Rational(2, 3) * q * (p + q) * r
    mixed_T = (-p + q) * r
    mixed_A = (
        -sp.Rational(167, 90) * p**2
        - sp.Rational(34, 9) * p * q
        + sp.Rational(4, 15) * p * r
        - q**2
        + sp.Rational(4, 15) * q * r
        + sp.Rational(1, 45) * r**2
    )
    mixed_B = (
        sp.Rational(83, 90) * p**2
        + 2 * p * q
        + sp.Rational(4, 15) * p * r
        + 2 * q**2
        + sp.Rational(4, 15) * q * r
        + sp.Rational(1, 45) * r**2
    )
    mixed_L = sp.Matrix([[1, 2, 2], [0, 1, -1], [2, 0, 1]])
    mixed_det = weighted_determinant(
        P, Q, mixed_R, mixed_U, mixed_V, mixed_T, mixed_A, mixed_B, mixed_L
    )
    assert mixed_L.det() == -7
    assert all(mixed_det.coeff_monomial(wt**degree) == 0 for degree in range(9, 4, -1))
    mixed_e4 = sp.Poly(mixed_det.coeff_monomial(wt**4), p, q, r)
    assert mixed_e4.coeff_monomial(p * r**3) == sp.Rational(16, 135)
    assert mixed_e4.coeff_monomial(q * r**3) == sp.Rational(16, 135)
    print("E6_E5_INVERTIBLE_SURVIVORS_PASS")


def main():
    check_representatives()
    check_mixed_components()
    check_power_zero_component()
    check_e6_e5_survivor_witnesses()
    print("L07_REPRESENTATIVE_COMPONENTS_ALL_PASS")


if __name__ == "__main__":
    main()
