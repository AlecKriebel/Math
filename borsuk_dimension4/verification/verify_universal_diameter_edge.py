#!/usr/bin/env python3
"""Exact constants for universal_diameter_edge_elimination.md.

The geometric proof is symbolic.  This checker independently replays every
rational endpoint identity and the strict auxiliary inequalities at c=1/3.
"""

from fractions import Fraction as Q


def verify_universal_edge_reduction() -> None:
    # Residual points have squared radius 3/4.  Scaling to the unit sphere
    # turns the original squared-distance bound 1 into inner product >= 1/3.
    residual_radius_sq = Q(3, 4)
    threshold = 1 - Q(1, 2) / residual_radius_sq
    assert threshold == Q(1, 3)


def verify_cap_and_sector_constants() -> None:
    c = Q(1, 3)

    # A closest point supported on at most three cap contacts has this
    # squared norm lower bound.
    cap_cosine_sq = c + (1 - c) / 3
    assert cap_cosine_sq == Q(5, 9)

    cap_sine_sq = 1 - cap_cosine_sq
    assert cap_sine_sq == Q(4, 9)

    # At the simultaneous radial and 120-degree endpoint, the inner product
    # is exactly c.  Half-open sectors make the angular comparison strict.
    sector_endpoint = cap_cosine_sq - Q(1, 2) * cap_sine_sq
    assert sector_endpoint == c

    # In the sharp cap case, an outer-cap point on a sector boundary is
    # antipodal in longitude to one regular support point and violates the
    # global threshold by an exact positive margin.
    opposite_longitude_inner = 2 * cap_cosine_sq - 1
    assert opposite_longitude_inner == Q(1, 9)
    assert c - opposite_longitude_inner == Q(2, 9)

    # A polar point has inner product sqrt(5)/3 > 1/3.  Squaring is valid
    # because both sides are positive.
    assert cap_cosine_sq > c * c
    assert cap_cosine_sq - c * c == Q(4, 9)


def verify_symbolic_range() -> None:
    # The key polar inequality works symbolically for every rational c in
    # (0,1): (1+2c)/3 - c^2 = (1-c)(1+3c)/3 > 0.
    for c in (Q(1, 100), Q(1, 3), Q(1, 2), Q(99, 100)):
        lhs = (1 + 2 * c) / 3 - c * c
        rhs = (1 - c) * (1 + 3 * c) / 3
        assert lhs == rhs and lhs > 0


if __name__ == "__main__":
    verify_universal_edge_reduction()
    verify_cap_and_sector_constants()
    verify_symbolic_range()
    print("universal diameter edge elimination: exact checks passed")
