#!/usr/bin/env python3
"""Exact algebra certificate for the dilute pair--leaf hybrid threshold."""

from __future__ import annotations

import sys

import sympy as sp


r, sigma = sp.symbols("r sigma", positive=True)
p = r**6 - 8*r**5 + 22*r**4 - 30*r**3 + 21*r**2 - 6*r + 1


def require(condition: object, message: str) -> None:
    if not bool(condition):
        raise RuntimeError(message)


def reject_optimized_python() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("optimized Python is not permitted for certificate replay")


def main() -> None:
    reject_optimized_python()
    polynomial = sp.Poly(p, r, domain=sp.QQ)
    require(
        polynomial.count_roots(sp.Rational(1), sp.Rational(3, 2)) == 0,
        "sextic unexpectedly has a root below 3/2",
    )
    require(
        polynomial.count_roots(sp.Rational(3, 2), sp.Rational(151, 100)) == 1,
        "sextic root count on (3/2,151/100) is not one",
    )
    require(
        p.subs(r, sp.Rational(3, 2)) == sp.Rational(1, 64),
        "sextic value at 3/2 is incorrect",
    )
    require(
        p.subs(r, sp.Rational(151, 100))
        == -sp.Rational(39866792399, 10**12),
        "sextic value at 151/100 is incorrect",
    )
    root = sp.CRootOf(polynomial, 0)
    require(
        sp.Rational(3, 2) < root < sp.Rational(151, 100),
        "isolated sextic root lies outside the claimed interval",
    )

    lower = 2 * (1 - sigma) * (r - 1) / (1 + sigma * (r**2 - 1))
    upper = 2 * (r * (2 - r) - sigma) / (sigma + 2 * r * (r - 1))
    gap_numerator = sp.factor(sp.together(upper - lower).as_numer_denom()[0])
    expected = -2 * r * (
        (r - 1) * sigma**2
        + (r**3 - 4 * r**2 + 3 * r + 1) * sigma
        + r * (2 * r - 3)
    )
    require(
        sp.expand(gap_numerator - expected) == 0,
        "response-gap numerator identity failed",
    )

    minimizing_sigma = sp.factor(
        -(r**3 - 4 * r**2 + 3 * r + 1) / (2 * (r - 1))
    )
    quadratic = -gap_numerator / (2 * r)
    minimum = sp.factor(quadratic.subs(sigma, minimizing_sigma))
    require(
        sp.simplify(minimum + p / (4 * (r - 1))) == 0,
        "quadratic minimum identity failed",
    )

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
        require(
            sp.Poly(numerator, r).count_roots(interval_left, interval_right) == 0,
            f"parameter-positivity numerator has an interval root: {numerator}",
        )
        require(
            numerator.subs(r, interval_left) > 0,
            f"parameter-positivity numerator is nonpositive at 3/2: {numerator}",
        )

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
    require(
        sp.simplify(derivative_lower - expected_lower_derivative) == 0,
        "lower-response derivative identity failed",
    )
    require(
        sp.simplify(derivative_upper - expected_upper_derivative) == 0,
        "upper-response derivative identity failed",
    )

    print(f"R_hyb~{sp.N(root, 18)}")
    print(f"sigma_*~{sp.N(sigma_star, 18)}")
    print(f"lambda_*~{sp.N(lambda_star, 18)}")
    print("PASS exact sextic threshold, tangency, and monotonicity algebra")


if __name__ == "__main__":
    main()
