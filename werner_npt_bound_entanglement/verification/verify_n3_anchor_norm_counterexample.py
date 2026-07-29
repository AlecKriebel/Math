#!/usr/bin/env python3
"""Exact rational check of the GHZ anchor-norm counterexample."""

from fractions import Fraction


def main() -> None:
    # For GHZ_2 all six proper nontrivial reductions have purity 1/2.
    q3 = (
        Fraction(1)
        - Fraction(1, 2) * 3 * Fraction(1, 2)
        + Fraction(1, 4) * 3 * Fraction(1, 2)
        - Fraction(1, 8)
    )
    assert q3 == Fraction(1, 2)

    # The Rayleigh quotient <w,A_w w> equals Q3(P_w).
    norm_squared_lower_bound = q3 * q3
    proposed_right_side = q3 / 8
    assert norm_squared_lower_bound == Fraction(1, 4)
    assert proposed_right_side == Fraction(1, 16)
    assert norm_squared_lower_bound > proposed_right_side
    print("verified: GHZ anchor violates the norm bound by factor 4")


if __name__ == "__main__":
    main()
