#!/usr/bin/env python3
"""Exact replay for the natural endpoint Fenchel--Bregman obstruction."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def assert_zero(expr: sp.Expr) -> None:
    expanded = sp.expand_log(expr, force=True)
    assert sp.factor(sp.cancel(sp.simplify(expanded))) == 0


def coeff(expr: sp.Expr, epsilon: sp.Symbol, order: int) -> sp.Expr:
    return sp.factor(
        sp.diff(expr, epsilon, order).subs(epsilon, 0) / sp.factorial(order)
    )


def average(weight: sp.Matrix, value: sp.Matrix) -> sp.Expr:
    return sp.Add(*(weight[i] * value[i] for i in range(value.rows)))


def main() -> None:
    # Scalar Fenchel and Bregman identities.
    x, y = sp.symbols("x y", positive=True)
    phi = lambda z: -z - sp.log(1 - z)
    phi_prime = lambda z: z / (1 - z)
    assert_zero(sp.diff(phi(x), x) - phi_prime(x))
    assert_zero(sp.diff(phi(x), x, 2) - 1 / (1 - x) ** 2)

    dual_point = y / (1 + y)
    phi_star = y - sp.log(1 + y)
    assert_zero(y * dual_point - phi(dual_point) - phi_star)

    bregman = phi(x) - phi(y) - phi_prime(y) * (x - y)
    complement_form = (1 - x) / (1 - y) - 1 - sp.log((1 - x) / (1 - y))
    assert_zero(bregman - complement_form)
    fenchel_bregman = (
        phi(x)
        + (phi_prime(y) - sp.log(1 + phi_prime(y)))
        - x * phi_prime(y)
        - bregman
    )
    # Substitute y=odds/(1+odds), which records the endpoint domain 0<y<1
    # and removes branch ambiguity in the logarithm simplifier.
    assert_zero(fenchel_bregman.subs(y, dual_point))

    # Exact two-node ground-state/Picone identity.  Self-loop conductances
    # cancel, so one symbolic off-diagonal conductance proves the edge formula.
    k, g0, g1, u0, u1 = sp.symbols("k g0 g1 u0 u1", nonzero=True)
    picone_left = k * g1 / g0 * u0**2 + k * g0 / g1 * u1**2 - 2 * k * u0 * u1
    picone_right = k * g0 * g1 * (u0 / g0 - u1 / g1) ** 2
    assert_zero(picone_left - picone_right)

    r, lam, epsilon = sp.symbols("r lam epsilon", real=True)
    c = r - 1
    q_symbol = sp.symbols("q_symbol", nonzero=True)
    b_symbol = 1 - q_symbol
    assert_zero(1 / (r * q_symbol**2) - 1 / (r * q_symbol)
                - b_symbol / (r * q_symbol**2))
    h_symbol = sp.symbols("h_symbol", nonzero=True)
    s_symbol = 1 - h_symbol
    assert_zero(1 / (r * h_symbol**2) - 1 / (r * h_symbol)
                - s_symbol / (r * h_symbol**2))

    # Homogeneous one-state nonconvexity and active curvature.
    z = sp.symbols("z")
    j_second = 1 / (r * (1 - z) ** 2) - 1
    assert_zero(j_second.subs(z, 0) - (1 / r - 1))
    assert_zero(j_second.subs(z, c / r) - c)
    # At homogeneous active data, each P-eigenmode curvature is r-lambda.
    # Natural Legendre duality would require its square to be one.
    assert_zero((r - lam) * (r - lam) - (r - lam) ** 2)
    assert sp.factor((r - 1) ** 2 - 1) == r * (r - 2)

    # Physical reversible two-state endpoint tangent.
    one = sp.ones(2, 1)
    f = sp.Matrix([1, -1])
    pi = sp.Rational(1, 2) * one
    P = sp.Matrix(
        [
            [(1 + lam) / 2, (1 - lam) / 2],
            [(1 - lam) / 2, (1 + lam) / 2],
        ]
    )

    # Exact IFT Jacobians at the homogeneous active point.  In the variables
    # q and h they are both P-rI; the s-variable reverses the dB sign.
    qv0, qv1, hv0, hv1 = sp.symbols("qv0 qv1 hv0 hv1")
    q_variable = sp.Matrix([qv0, qv1])
    h_variable = sp.Matrix([hv0, hv1])
    b_variable = one - q_variable
    s_variable = one - h_variable
    bd_at_zero = sp.Matrix(
        [
            b_variable[i] - r * q_variable[i] * (P * b_variable)[i]
            for i in range(2)
        ]
    )
    db_at_zero = sp.Matrix(
        [
            s_variable[i] - r * h_variable[i] * (P * s_variable)[i]
            for i in range(2)
        ]
    )
    active_substitution = {qv0: 1 / r, qv1: 1 / r, hv0: 1 / r, hv1: 1 / r}
    expected_jacobian = P - r * sp.eye(2)
    jacobian_q = bd_at_zero.jacobian(q_variable).subs(active_substitution)
    jacobian_h = db_at_zero.jacobian(h_variable).subs(active_substitution)
    for i in range(2):
        for j in range(2):
            assert_zero(jacobian_q[i, j] - expected_jacobian[i, j])
            assert_zero(jacobian_h[i, j] - expected_jacobian[i, j])

    a = one + epsilon * f
    diagonal_a = sp.diag(*a)
    R = diagonal_a.inv() * P * diagonal_a
    t = diagonal_a.inv() * P * a
    p = sp.Matrix([pi[i] * a[i] for i in range(2)])

    q0 = 1 / r
    Q = c * (lam - 1) / (r * (r - lam))
    Q2 = -(lam - 1) * c * (r - lam**2) / (r * (r - lam) ** 2)
    H2 = lam * (lam - 1) * c**2 / (r * (r - lam) ** 2)
    q = q0 * one + epsilon * Q * f + epsilon**2 * Q2 * one
    h = q0 * one - epsilon * Q * f + epsilon**2 * H2 * one
    b = one - q
    s = one - h

    # Verify both endpoint equations through the order used below.
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

    support = average(p, c * q - s)
    T2 = (lam - 1) ** 2 * c * (r + lam * c) / (r * (r - lam) ** 2)
    assert_zero(coeff(support, epsilon, 2) - T2)

    def dphi(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        ratio = (1 - left) / (1 - right)
        return ratio - 1 - sp.log(ratio)

    B_B = sum(pi[i] * t[i] * dphi(s[i], b[i]) for i in range(2)) / r
    B_D = sum(pi[i] * a[i] ** 2 * dphi(b[i], s[i]) for i in range(2)) / r
    difference = s - b
    kinetic_B = average(pi, difference.multiply_elementwise(P * difference)) / 2
    weighted_difference = a.multiply_elementwise(b - s)
    kinetic_D = average(
        pi, weighted_difference.multiply_elementwise(P * weighted_difference)
    ) / 2
    Delta_B = B_B - kinetic_B
    Delta_D = B_D - kinetic_D

    def action_B(label: sp.Matrix) -> sp.Expr:
        node = sum(pi[i] * t[i] * phi(label[i]) for i in range(2)) / r
        kinetic = average(pi, label.multiply_elementwise(P * label)) / 2
        return node - kinetic

    def action_D(label: sp.Matrix) -> sp.Expr:
        node = sum(pi[i] * a[i] ** 2 * phi(label[i]) for i in range(2)) / r
        weighted = a.multiply_elementwise(label)
        kinetic = average(pi, weighted.multiply_elementwise(P * weighted)) / 2
        return node - kinetic

    for order in range(3):
        assert_zero(
            coeff(action_B(s) - action_B(b) - Delta_B, epsilon, order)
        )
        assert_zero(
            coeff(action_D(b) - action_D(s) - Delta_D, epsilon, order)
        )

    B2 = 2 * r * Q**2
    Delta2 = 2 * (r - lam) * Q**2
    assert_zero(coeff(B_B, epsilon, 2) - B2)
    assert_zero(coeff(B_D, epsilon, 2) - B2)
    assert_zero(coeff(Delta_B, epsilon, 2) - Delta2)
    assert_zero(coeff(Delta_D, epsilon, 2) - Delta2)

    ratio_B = (r + lam * c) / (2 * c)
    ratio_Delta = r * (r + lam * c) / (2 * c * (r - lam))
    assert_zero(T2 / B2 - ratio_B)
    assert_zero(T2 / Delta2 - ratio_Delta)
    assert_zero(sp.diff(ratio_B, lam) - sp.Rational(1, 2))
    assert_zero(
        sp.diff(ratio_Delta, lam) - r**3 / (2 * c * (r - lam) ** 2)
    )

    # Exact unit crossings for the individual node gaps.
    assert_zero(ratio_B.subs(lam, -1) - 1 / (2 * c))
    assert_zero(ratio_B.subs(lam, 0) - r / (2 * c))
    assert_zero(ratio_B.subs(lam, -1) - 1 - (3 - 2 * r) / (2 * c))
    assert_zero(ratio_B.subs(lam, 0) - 1 - (2 - r) / (2 * c))

    # Exact unit crossings for each full stationary remainder.
    assert_zero(ratio_Delta.subs(lam, -1) - r / (2 * c * (r + 1)))
    assert_zero(ratio_Delta.subs(lam, 0) - r / (2 * c))
    below_numerator = 2 * c * (r + 1) - r
    assert_zero(below_numerator - (2 * r**2 - r - 2))
    strip_z = sp.symbols("strip_z", real=True)
    r_strip = sp.Rational(3, 2) + strip_z / 100
    assert_zero(
        below_numerator.subs(r, r_strip)
        - (strip_z**2 + 250 * strip_z + 5000) / 5000
    )

    # The symmetric full remainder crosses T.  At lambda=1/2 the exact
    # positivity polynomial has positive Bernstein coefficients on the strip.
    symmetric_difference = sp.factor(
        r * (r + c / 2) - 4 * c * (r - sp.Rational(1, 2))
    )
    assert_zero(symmetric_difference + (5 * r**2 - 11 * r + 4) / 2)
    strip_polynomial = sp.factor(symmetric_difference.subs(r, r_strip))
    assert_zero(
        strip_polynomial
        - (sp.Rational(5, 8) - strip_z / 50 - strip_z**2 / 4000)
    )
    bernstein = (
        sp.Rational(5, 8),
        sp.Rational(123, 200),
        sp.Rational(2419, 4000),
    )
    assert all(value > 0 for value in bernstein)
    bernstein_reconstruction = (
        bernstein[0] * (1 - strip_z) ** 2
        + 2 * bernstein[1] * strip_z * (1 - strip_z)
        + bernstein[2] * strip_z**2
    )
    assert_zero(strip_polynomial - bernstein_reconstruction)

    theorem = HERE / "ENDPOINT_FENCHEL_BREGMAN_OBSTRUCTION.md"
    digest = hashlib.sha256(theorem.read_bytes()).hexdigest()
    print("PASS: exact stationary and ground-state Hessian identities")
    print("PASS: natural Fenchel/Bregman tangent ratios and unit crossings")
    print("PASS: symmetric variational remainder crosses the support target")
    print(f"theorem_sha256={digest}")


if __name__ == "__main__":
    main()
