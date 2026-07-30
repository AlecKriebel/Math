#!/usr/bin/env python3
"""Exact integer audit for the upgraded high-AAA radius."""

from fractions import Fraction as F


eps = F(1, 10**56)
root8_upper = F(1, 10**7)

# r=1/sqrt(6) obeys 2/5 < r < 1/2.  All comparisons below use only
# the rational lower bound r>2/5.
assert 46 * root8_upper < F(1, 10000)
assert F(1, 10000) < F(1, 10)  # in particular eta < r/4

# beta < (8*46+4)/r * eps^(1/8) < 930 eps^(1/8).
assert (8 * 46 + 4) * F(5, 2) == 930

# Feature and concurrence estimates.
q_upper = 7440 * root8_upper
assert q_upper < F(2, 27)
assert 36 * q_upper < F(4, 27)

# The Sylvester smallness condition xi=3r*eta<3r^2/8 follows from
# eta<r/8.  Our rational estimates are much stronger:
# eta<1/10000 and r>2/5 imply eta<r/8.
assert F(1, 10000) < F(1, 20)

# Exact fused depth and its gap below 9/71.
depth = F(648 * 10**56 + 2187, 5112 * 10**56 + 21141)
gap = F(9, 71) - depth
expected_gap = F(
    34992,
    71 * (5112 * 10**56 + 21141),
)
assert gap == expected_gap
assert F(0) < gap

print("verified: O(epsilon^(1/8)) spectral-plane bound constants")
print("verified: high-AAA radius epsilon_0 = 10^-56")
print("verified: exact improved fused-depth rational")
