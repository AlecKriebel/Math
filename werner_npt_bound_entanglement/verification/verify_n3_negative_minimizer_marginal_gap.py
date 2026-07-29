#!/usr/bin/env python3
"""Dependency-free exact checks for the marginal-gap arithmetic."""

from fractions import Fraction


def check(delta: Fraction, r: Fraction) -> None:
    m = delta / (1 + 2 * delta)
    # (1+delta)r-delta(1-r)=(1+2delta)(r-m).
    assert (1 + delta) * r - delta * (1 - r) == (
        1 + 2 * delta
    ) * (r - m)
    # The trace-two determinant floor.
    assert m * m * (2 - 2 * m) == 2 * m * m * (1 - m)


for d0, r0 in [
    (Fraction(1, 8), Fraction(1, 10)),
    (Fraction(1, 17), Fraction(3, 11)),
    (Fraction(2, 9), Fraction(7, 20)),
]:
    check(d0, r0)

# The endpoint Haar floor delta <= 1/8 gives m <= 1/10 exactly,
# with equality at delta=1/8.
d0 = Fraction(1, 8)
m0 = d0 / (1 + 2 * d0)
assert m0 == Fraction(1, 10)
assert d0 * (1 - m0) == (1 + d0) * m0

print("verified: negative-minimizer marginal gap identities")
