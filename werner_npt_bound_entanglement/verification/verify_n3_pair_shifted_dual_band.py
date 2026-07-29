#!/usr/bin/env python3
"""Dependency-free exact arithmetic for the shifted dual-band reduction."""

from fractions import Fraction as F


def dual_value(d1: F, d2: F) -> F:
    """The squared dual gauge from Lemma 1."""

    if d1 >= 2 * d2:
        return d1 * d1
    return F(4, 3) * (d1 * d1 - d1 * d2 + d2 * d2)


# Boundary agreement.
for d2 in (F(1), F(3, 7), F(11, 13)):
    d1 = 2 * d2
    assert d1 * d1 == F(4, 3) * (
        d1 * d1 - d1 * d2 + d2 * d2
    )

# Direct substitution of the maximizing rays in both branches.
tests = [
    (F(5), F(1)),
    (F(2), F(1)),
    (F(3, 2), F(1)),
    (F(1), F(1)),
]
for d1, d2 in tests:
    value = dual_value(d1, d2)
    if d1 >= 2 * d2:
        s1, s2 = F(1), F(0)
    else:
        s1 = d1 - d2 / 2
        s2 = d2 - d1 / 2
    quotient = (d1 * s1 + d2 * s2) ** 2 / (
        s1 * s1 + s2 * s2 + s1 * s2
    )
    assert quotient == value

# In the balanced branch, the strengthened bound implies the ordinary
# top-two Ky--Fan bound by the exact square in equation (17).
for d1, d2 in (
    (F(2), F(1)),
    (F(3, 2), F(1)),
    (F(5, 4), F(1)),
    (F(1), F(1)),
):
    strengthened_rhs = 3 * (d1 * d1 - d1 * d2 + d2 * d2)
    kyfan_rhs = F(3, 2) * (d1 * d1 + d2 * d2)
    assert strengthened_rhs - kyfan_rhs == F(3, 2) * (d1 - d2) ** 2
    assert strengthened_rhs >= kyfan_rhs

# Tail form is algebraically identical to the balanced dual inequality.
for d1, d2 in (
    (F(2), F(1)),
    (F(3, 2), F(1)),
    (F(1), F(1)),
):
    required_norm = 3 * (d1 * d1 - d1 * d2 + d2 * d2)
    required_tail = required_norm - d1 * d1 - d2 * d2
    assert required_tail == 2 * d1 * d1 + 2 * d2 * d2 - 3 * d1 * d2
    assert required_tail > 0

print(
    "verified exact shifted dual gauge, imbalanced rank-one branch, "
    "balanced tail reduction, and Ky-Fan implication"
)
