#!/usr/bin/env python3
"""Exact symbolic verifier for clique--pendant affine sharpness."""

from __future__ import annotations

import sympy as sp


def main():
    alpha = sp.symbols("alpha", positive=True)
    q = (3 + 10 * alpha - sp.sqrt(9 + 60 * alpha - 44 * alpha**2)) / (
        18 * alpha
    )
    ell = 1 - q
    lam = sp.Rational(9, 4) * alpha
    mu = alpha
    kappa = sp.Rational(3, 4) * (1 - alpha)

    branching_polynomial = sp.factor(
        lam * q**2 - (lam + mu + kappa) * q + mu
    )
    assert branching_polynomial == 0
    assert sp.limit(q / alpha, alpha, 0, dir="+") == sp.Rational(4, 3)
    assert sp.limit(ell, alpha, 0, dir="+") == 1

    x = sp.factor(1 - alpha + 3 * alpha * ell)
    y = 1 - alpha
    crossing = sp.factor((1 - y) / (x - y))
    slack = sp.factor(1 - (x + 2 * y) / 3)
    assert sp.simplify(crossing - 1 / (3 * ell)) == 0
    assert sp.simplify(slack - alpha * (1 - ell)) == 0
    assert sp.limit(crossing, alpha, 0, dir="+") == sp.Rational(1, 3)
    assert sp.limit((x - 1) / alpha, alpha, 0, dir="+") == 2
    assert sp.limit((1 - y) / alpha, alpha, 0, dir="+") == 1

    # Exact algebraic spot checks.  Positivity is decided symbolically, not
    # by the decimal values printed for readability.
    for value in (sp.Rational(1, 100), sp.Rational(1, 20), sp.Rational(1, 9)):
        ell_value = sp.simplify(ell.subs(alpha, value))
        crossing_value = sp.simplify(crossing.subs(alpha, value))
        slack_value = sp.simplify(slack.subs(alpha, value))
        assert 0 < ell_value < 1
        assert crossing_value > sp.Rational(1, 3)
        assert slack_value > 0
        print(
            f"alpha={value}: ell~{sp.N(ell_value, 14)}, "
            f"crossing~{sp.N(crossing_value, 14)}, "
            f"one_third_slack~{sp.N(slack_value, 14)}"
        )

    # The previously audited a=8 ray is alpha=1/9.
    assert sp.simplify(ell.subs(alpha, sp.Rational(1, 9))) == sp.Rational(8, 9)
    assert sp.simplify(x.subs(alpha, sp.Rational(1, 9))) == sp.Rational(32, 27)
    assert sp.simplify(y.subs(alpha, sp.Rational(1, 9))) == sp.Rational(8, 9)

    print("PASS exact branching polynomial and limiting ratios")
    print("PASS exact affine-sharpness algebra")
    print("CONDITIONAL theorem: coefficient <=1/3 pending mesoscopic-core audit")


if __name__ == "__main__":
    main()
