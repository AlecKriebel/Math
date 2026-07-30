#!/usr/bin/env python3
"""Exact rational audit of the n=3 triple-Hodge/face fusion."""

from fractions import Fraction as F


def verify_fusion() -> None:
    # Choose independent nonnegative data and solve the exact
    # triple-Hodge identity for R.
    T = F(5, 13)
    c = F(7, 11)
    a = F(2, 17)
    Delta = F(3, 19)
    tau = F(4, 23)
    R = (468 * c + 405 * a + 144 * Delta + 864 * tau - 28 * T) / 320

    G = T / 3
    k = R / 3 + 2 * T / 3
    q = (2 * R + 4 * T - 9 * c) / 36
    sigma = 2 * q + 3 * c
    Xi = Delta + 6 * tau

    rhs = (
        F(13, 71) * sigma
        + F(255, 142) * G
        + F(225, 568) * a
        + F(10, 71) * Xi
    )
    assert k == rhs
    assert 5112 * k == (
        936 * sigma
        + 9180 * G
        + 2025 * a
        + 720 * Delta
        + 4320 * tau
    )

    # Equivalent coefficient-matrix fusion.
    q_shifted = q + F(27, 160) * c
    primal_rhs = (
        F(51, 160) * G
        + F(9, 128) * a
        + F(1, 40) * Xi
    )
    assert q_shifted == primal_rhs


def verify_operator_constants() -> None:
    assert F(1, 2) - F(13, 71) == F(45, 142)
    assert (F(13, 71) - F(1, 2)) * F(2, 5) == -F(9, 71)

    # Multiplying the remaining inequality by 568 and dividing by 5.
    assert F(255, 142) * F(568, 5) == 204
    assert F(225, 568) * F(568, 5) == 45
    assert F(10, 71) * F(568, 5) == 16
    assert F(45, 142) * F(568, 5) == 36
    assert F(27, 160) * 640 == 108


if __name__ == "__main__":
    verify_fusion()
    verify_operator_constants()
    print("n=3 triple-Hodge/face fusion: exact checks passed")
