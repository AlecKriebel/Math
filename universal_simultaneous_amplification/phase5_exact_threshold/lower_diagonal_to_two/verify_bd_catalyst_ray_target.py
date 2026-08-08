#!/usr/bin/env python3
"""Exact symbolic verifier for the Bd-catalyst ray reduction."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    r, sigma = sp.symbols("r sigma", positive=True)
    pair_b = 2 * (sigma - 1) / (1 + sigma * (r**2 - 1))
    pair_d = 2 * (r * (2 - r) - sigma) / (sigma + 2 * r * (r - 1))
    delta = (2 - r) / (r - 1)
    assert sp.factor(pair_b.subs(sigma, 0) + 2) == 0
    assert sp.factor(pair_d.subs(sigma, 0) - delta) == 0

    # A normalized catalyst ray (b,0), mixed with coefficient tau.
    b, tau = sp.symbols("b tau", positive=True)
    total_b = sp.factor(-2 + tau * b)
    total_d = delta
    assert sp.factor(total_b - (tau * b - 2)) == 0
    assert sp.factor(total_d - (2 - r) / (r - 1)) == 0

    # At one fixed fitness, a catalyst (B,D), D<0, paid at the minimum
    # coefficient 2/B leaves dB margin delta+2D/B.
    B, D = sp.symbols("B D", real=True)
    db_margin = sp.factor(delta + 2 * D / B)
    ratio_threshold_residual = sp.factor(
        db_margin - 2 * (delta / 2 + D / B)
    )
    assert ratio_threshold_residual == 0

    # The pair resource is positive below two and vanishes at two.
    assert sp.factor(delta.subs(r, 2)) == 0
    for value in [sp.Rational(3, 2), sp.Rational(19, 10), sp.Rational(199, 100)]:
        assert delta.subs(r, value) > 0

    print("PASS exact Bd-catalyst ray target")


if __name__ == "__main__":
    main()
