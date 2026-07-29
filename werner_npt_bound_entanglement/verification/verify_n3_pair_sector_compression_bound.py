#!/usr/bin/env python3
"""Exact coefficient check for the one-site compression bound."""

from fractions import Fraction as F


def main():
    # Local identity/traceless output masses after A=I-|z><z|.
    total_identity = F(2, 3)
    total_traceless = F(2, 3)
    p_identity = F(4, 9)
    p_traceless = F(1, 36)
    q_identity = total_identity - p_identity
    q_traceless = total_traceless - p_traceless
    assert q_identity == F(2, 9)
    assert q_traceless == F(23, 36)

    # Sum over the three possible filtered sites.
    coefficient_degree_one = 2 * q_identity
    coefficient_degree_two = p_identity + 2 * q_traceless
    coefficient_degree_three = 3 * p_traceless
    assert coefficient_degree_one == F(4, 9)
    assert coefficient_degree_two == F(31, 18)
    assert coefficient_degree_three == F(1, 12)

    summed_right_side = 3 * F(2, 3) * F(2, 3)
    assert summed_right_side == F(4, 3)

    scale = 36
    assert scale * coefficient_degree_one == 16
    assert scale * coefficient_degree_two == 62
    assert scale * coefficient_degree_three == 3
    assert scale * summed_right_side == 48
    assert F(48, 62) == F(24, 31)

    print("verified: one-site Haar compression gives w2 <= 24/31")


if __name__ == "__main__":
    main()
