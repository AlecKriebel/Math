#!/usr/bin/env python3
"""Exact verifier for the diffuse growing-portal limit and obstruction."""

from __future__ import annotations

import sympy as sp


def checked_zero(expression, label):
    value = sp.factor(sp.cancel(expression))
    if value != 0:
        raise AssertionError(f"{label}: {value}")
    print("PASS", label)


def main():
    Q, k = sp.symbols("Q k", positive=True, integer=True)
    r, B, H = sp.symbols("r B H", positive=True)
    d = B + H
    edge = H / (Q - 1)

    # Exact complete-portal count-chain rates.
    loss_b = k * (B + (Q - k) * edge / d)
    gain_b = (Q - k) * r * k * edge / d
    loss_d = k * (B + (Q - k) * edge) / (
        B + (Q - k) * edge + r * (k - 1) * edge
    )
    gain_d = (Q - k) * r * k * edge / (
        B + (Q - k - 1) * edge + r * k * edge
    )

    delta_b = B + H / d
    delta_d = sp.Integer(1)
    birth = r * H / d
    checked_zero(sp.limit(loss_b, Q, sp.oo) - k * delta_b,
                 "Bd finite-Q loss limit")
    checked_zero(sp.limit(gain_b, Q, sp.oo) - k * birth,
                 "Bd finite-Q gain limit")
    checked_zero(sp.limit(loss_d, Q, sp.oo) - k * delta_d,
                 "dB finite-Q loss limit")
    checked_zero(sp.limit(gain_d, Q, sp.oo) - k * birth,
                 "dB finite-Q gain limit")

    # Parent clean-blade seed/death ratios.  Lambda=B/2 per portal.
    parent_seed_b = r * Q * B
    parent_death_b = Q * B / ((r + 1) * d)
    parent_seed_d = r * Q * B / d
    parent_death_d = Q * B / (2 * r)
    checked_zero(parent_seed_b / parent_death_b - r * (r + 1) * d,
                 "Bd parent episode ratio")
    checked_zero(parent_seed_d / parent_death_d - 2 * r**2 / d,
                 "dB parent episode ratio")

    # At the two complete-graph establishment test points, the retained-child
    # rates simplify before solving the portal quadratic.
    beta_b = r**2 * B / ((r + 1) * d)
    beta_d = r * B / 2
    q0_b = 1 / r**2
    q0_d = (2 - r) / r
    mark_b = sp.factor(beta_b * (1 - q0_b))
    mark_d = sp.factor(beta_d * (1 - q0_d))
    checked_zero(mark_b - (r - 1) * B / d,
                 "Bd retained-child rate")
    checked_zero(mark_d - (r - 1) * B,
                 "dB retained-child rate")

    # If X=1-F, the branching episode equation is
    # u X^2 + (delta+mark-u) X - mark = 0.
    X = sp.symbols("X")
    phi_b = birth * X**2 + (delta_b + mark_b - birth) * X - mark_b
    phi_d = birth * X**2 + (delta_d + mark_d - birth) * X - mark_d
    threshold_b = (r - 1) / (r * d)
    threshold_d = d * (r - 1) / (r**2 * (2 - r))
    bd_factor = -(
        (r - 1)**2 * (d - 1) * (B**2 + B * H + H)
        / (r * d**3)
    )
    checked_zero(phi_b.subs(X, threshold_b) - bd_factor,
                 "Bd degree-one threshold factor")

    # The dB sign polynomial and its affine endpoint certificate.
    dB_value = sp.factor(phi_d.subs(X, threshold_d))
    numerator, denominator = sp.together(dB_value).as_numer_denom()
    N = (
        B**2 * r**2 - 2 * B**2 * r
        + B * H * r**2 - 2 * B * H * r - B * H
        + B * r**4 - 3 * B * r**3 + B * r**2 + 2 * B * r
        - H**2 - H * r**2 + 2 * H * r
    )
    checked_zero(
        dB_value + (r - 1)**2 * N / (r**3 * (r - 2)**2),
        "dB threshold rational factor",
    )
    if denominator == 0 or numerator == 0:
        raise AssertionError("dB test rational function collapsed")

    x = sp.symbols("x", nonnegative=True)
    P = sp.factor(-N.subs(B, 1 + x - H))
    endpoint_zero = r * (2 - r) * (1 + x) * (r**2 - r + x)
    endpoint_full = (1 + x) * ((r - 1)**2 + x)
    checked_zero(P.subs(H, 0) - endpoint_zero,
                 "dB affine endpoint H=0")
    checked_zero(P.subs(H, 1 + x) - endpoint_full,
                 "dB affine endpoint H=1+x")
    checked_zero(sp.diff(P, H, 2), "dB sign polynomial affine in H")
    interpolation = (
        (1 - H / (1 + x)) * endpoint_zero
        + H / (1 + x) * endpoint_full
    )
    checked_zero(P - interpolation, "dB positive affine interpolation")

    # Displayed reconnaissance values are exact specializations, not sampled
    # numerical evidence.
    special_bd_3_2 = sp.factor(bd_factor.subs(r, sp.Rational(3, 2)))
    special_bd_31_20 = sp.factor(bd_factor.subs(r, sp.Rational(31, 20)))
    if special_bd_3_2 == 0 or special_bd_31_20 == 0:
        raise AssertionError("endpoint Bd factors vanished identically")
    print("PASS exact r=3/2 and r=31/20 specializations")
    print("ALL DIFFUSE GROWING-PORTAL CHECKS PASS")


if __name__ == "__main__":
    main()
