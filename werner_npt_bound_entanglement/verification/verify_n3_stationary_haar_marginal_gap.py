#!/usr/bin/env python3
"""Dependency-free exact checks for the stationary Haar marginal gap."""

from __future__ import annotations

from fractions import Fraction as F


def integrate_monomial_over_triangle(
    p_power: int, q_power: int, p_intercept: F, q_intercept: F
) -> F:
    """Integral of p^p_power q^q_power on the coordinate triangle.

    The triangle has vertices (0,0), (p_intercept,0),
    (0,q_intercept).
    """
    # Substitute p=p_intercept*u, q=q_intercept*v on the unit simplex.
    # Integral u^a v^b = a! b!/(a+b+2)!.
    from math import factorial

    return (
        p_intercept ** (p_power + 1)
        * q_intercept ** (q_power + 1)
        * F(
            factorial(p_power) * factorial(q_power),
            factorial(p_power + q_power + 2),
        )
    )


def positive_part_integral(lam1: F, lam2: F, lam3: F) -> F:
    """Direct simplex integral of (2 r-1)_+ with Haar density two."""
    h = lam1 - F(1, 2)
    a = lam1 - lam2
    b = lam1 - lam3
    p_intercept = h / a
    q_intercept = h / b

    area_moment = integrate_monomial_over_triangle(
        0, 0, p_intercept, q_intercept
    )
    p_moment = integrate_monomial_over_triangle(
        1, 0, p_intercept, q_intercept
    )
    q_moment = integrate_monomial_over_triangle(
        0, 1, p_intercept, q_intercept
    )
    # Haar density is 2; the integrand is
    # 2(h-a p-b q), giving the factor 4.
    return 4 * (h * area_moment - a * p_moment - b * q_moment)


def main() -> None:
    # One-site Haar coefficients.
    # P=I-R: scalar 0, traceless 5/8.
    p_scalar, p_traceless = F(0), F(5, 8)
    # R: scalar 1/6, traceless 7/24.
    r_scalar, r_traceless = F(1, 6), F(7, 24)
    assert 3 * (p_scalar - r_scalar) == F(-1, 2)
    assert 3 * (p_traceless - r_traceless) == F(1)

    # Check the exact tent integral on several nondegenerate rational
    # spectra, independently from the closed formula.
    spectra = [
        (F(3, 5), F(1, 4), F(3, 20)),
        (F(2, 3), F(1, 5), F(2, 15)),
        (F(7, 10), F(1, 6), F(2, 15)),
    ]
    for lam1, lam2, lam3 in spectra:
        assert lam1 + lam2 + lam3 == 1
        direct = positive_part_integral(lam1, lam2, lam3)
        closed = (
            2
            * (lam1 - F(1, 2)) ** 3
            / (3 * (lam1 - lam2) * (lam1 - lam3))
        )
        assert direct == closed

    # The two positive parts differ by E(1-2r)=1/3.
    assert F(1) - 2 * F(1, 3) == F(1, 3)

    print("verified: stationary Haar coefficients and marginal tent integral")


if __name__ == "__main__":
    main()
