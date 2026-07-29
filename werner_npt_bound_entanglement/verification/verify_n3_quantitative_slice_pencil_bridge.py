#!/usr/bin/env python3
"""Exact constant checks for the quantitative slice-pencil bridge."""

from fractions import Fraction as F


def main() -> None:
    # Robust rank-one exclusion:
    # s1^2 >= r^2/2 and s2 < s1/10 imply Q > s1^2/20.
    assert F(1, 2) * F(1, 20) == F(1, 40)
    assert F(1, 40) > F(1, 64)
    # The rational comparison replacing 1/(10 sqrt(2)) > 1/15.
    assert 15 * 15 > 2 * 10 * 10

    # Initial conditioning:
    # r0^2=gamma/24, kappa0^2=gamma/5400.
    assert 24 * 15 * 15 == 5400

    # Two propagation rounds.  The stricter threshold is
    # kappa0^2*m^2/(225*64).
    assert 5400 * 225 * 64 == 77_760_000
    assert 30 * 15 * 15 == 6750
    assert 6750 * 6750 * 6 == 273_375_000

    # Minor-to-factor calculation for mu <= 1/2.
    # 4 mu^3 / 3 <= mu/3, so |qr| <= 5 mu/6.
    assert F(4, 3) * F(1, 2) ** 2 == F(1, 3)
    assert F(1, 3) + F(1, 2) == F(5, 6)
    # b^2 + |s|^2 + min(q^2,r^2)
    # <= mu^2/2 + 4mu^2/3 + 5mu/6 <= 7mu/4.
    assert F(1, 2) + F(4, 3) == F(11, 6)
    assert F(5, 6) + F(11, 6) * F(1, 2) == F(7, 4)
    assert F(7, 4) < 4

    # Full-H second-kernel and min-max constants.
    assert 20 * 2 == 40
    assert F(40, 4) == 10

    print(
        "verified: robust-rank, propagation, projection, "
        "and factor-distance constants"
    )


if __name__ == "__main__":
    main()
