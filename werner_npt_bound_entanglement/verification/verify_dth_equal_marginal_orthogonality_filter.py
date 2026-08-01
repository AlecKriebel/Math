#!/usr/bin/env python3
"""Exact arithmetic audit of the equal-marginal orthogonality filter."""

from fractions import Fraction as F


def main():
    # L=(1+3p)/108 and the minimum at F=1/2,A=1/4.
    # Represent rational functions (constant + linear*p) where useful.
    # 1/4-L=(26-3p)/108, hence
    # (1/4)^2/[4(1/4-L)] = 27/[16(26-3p)].
    assert F(1, 4) - F(1, 108) == F(13, 54)
    assert F(1, 16) * F(108, 4) == F(27, 16)

    # Cross multiplication of
    # (1+p)/32 > 27/[16(26-3p)] gives
    # (1+p)(26-3p)-54 > 0, i.e. -3p^2+23p-28 > 0.
    # Coefficients are recorded from low to high degree.
    left_coefficients = [F(26), F(23), F(-3)]
    left_coefficients[0] -= F(54)
    assert left_coefficients == [F(-28), F(23), F(-3)]

    # The discriminant and roots of 3p^2-23p+28.
    discriminant = 23 * 23 - 4 * 3 * 28
    assert discriminant == 193
    # The lower root lies strictly between 3/2 and 8/5; the upper exceeds 3.
    polynomial = lambda x: 3 * x * x - 23 * x + 28
    assert polynomial(F(3, 2)) > 0
    assert polynomial(F(8, 5)) < 0
    assert polynomial(F(3)) < 0

    # Uniform range check used in the monotonicity argument.
    max_l = F(1 + 3 * 3, 108)
    assert 2 * max_l == F(5, 27) < F(1, 4)

    print("exact equal-marginal orthogonality filter passed")
    print("threshold polynomial: 3 p^2 - 23 p + 28")
    print("lower root: (23-sqrt(193))/6")


if __name__ == "__main__":
    main()
