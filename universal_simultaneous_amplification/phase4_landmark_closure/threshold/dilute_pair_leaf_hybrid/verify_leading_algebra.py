#!/usr/bin/env python3
"""Exact algebra certificate for the dilute pair--leaf hybrid threshold."""

from __future__ import annotations

import sympy as sp


r, sigma = sp.symbols("r sigma", positive=True)
p = r**6 - 8*r**5 + 22*r**4 - 30*r**3 + 21*r**2 - 6*r + 1


def main() -> None:
    polynomial = sp.Poly(p, r, domain=sp.QQ)
    assert polynomial.count_roots(sp.Rational(1), sp.Rational(3, 2)) == 0
    assert polynomial.count_roots(sp.Rational(3, 2), sp.Rational(151, 100)) == 1
    assert p.subs(r, sp.Rational(3, 2)) == sp.Rational(1, 64)
    assert p.subs(r, sp.Rational(151, 100)) < 0
    root = sp.CRootOf(polynomial, 0)
    assert sp.Rational(3, 2) < root < sp.Rational(151, 100)

    lower = 2 * (1 - sigma) * (r - 1) / (1 + sigma * (r**2 - 1))
    upper = 2 * (r * (2 - r) - sigma) / (sigma + 2 * r * (r - 1))
    gap_numerator = sp.factor(sp.together(upper - lower).as_numer_denom()[0])
    expected = -2 * r * (
        (r - 1) * sigma**2
        + (r**3 - 4 * r**2 + 3 * r + 1) * sigma
        + r * (2 * r - 3)
    )
    assert sp.expand(gap_numerator - expected) == 0

    minimizing_sigma = sp.factor(
        -(r**3 - 4 * r**2 + 3 * r + 1) / (2 * (r - 1))
    )
    quadratic = -gap_numerator / (2 * r)
    minimum = sp.factor(quadratic.subs(sigma, minimizing_sigma))
    assert sp.simplify(minimum + p / (4 * (r - 1))) == 0

    sigma_star = sp.cancel(minimizing_sigma.subs(r, root))
    lambda_star = sp.cancel(lower.subs({r: root, sigma: sigma_star}))
    # The exact minimum identity above and p(root)=0 prove L=U at this
    # algebraic pair.  Positivity follows throughout the isolating interval:
    # neither the numerator of sigma_* nor that of 1-sigma_* has a root
    # there, and both are positive at 3/2.
    sigma_numerator = -r**3 + 4 * r**2 - 3 * r - 1
    one_minus_numerator = 2 * (r - 1) - sigma_numerator
    interval_left, interval_right = sp.Rational(3, 2), sp.Rational(151, 100)
    for numerator in (sigma_numerator, one_minus_numerator):
        assert sp.Poly(numerator, r).count_roots(interval_left, interval_right) == 0
        assert numerator.subs(r, interval_left) > 0

    # For fixed sigma_star, L is increasing and U decreasing throughout the
    # relevant interval.  The factored derivatives make both signs exact.
    derivative_lower = sp.factor(sp.diff(lower, r))
    derivative_upper = sp.factor(sp.diff(upper, r))
    expected_lower_derivative = (
        2
        * (sigma - 1)
        * (r**2 * sigma - 2 * r * sigma + sigma - 1)
        / (r**2 * sigma - sigma + 1) ** 2
    )
    expected_upper_derivative = 4 * r * (-r + sigma) / (2 * r**2 - 2 * r + sigma) ** 2
    assert sp.simplify(derivative_lower - expected_lower_derivative) == 0
    assert sp.simplify(derivative_upper - expected_upper_derivative) == 0

    print(f"R_hyb~{sp.N(root, 18)}")
    print(f"sigma_*~{sp.N(sigma_star, 18)}")
    print(f"lambda_*~{sp.N(lambda_star, 18)}")
    print("PASS exact sextic threshold, tangency, and monotonicity algebra")


if __name__ == "__main__":
    main()
