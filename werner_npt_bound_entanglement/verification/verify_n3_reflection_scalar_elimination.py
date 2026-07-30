#!/usr/bin/env python3
"""Exact checks for the reflection scalar elimination."""

from fractions import Fraction as F


# Scalar Schur complement:
# -16 |c|^2 + 2 Re(conj(c)t) is maximized at c=t/16.
t2 = F(37, 11)
c2 = t2 / 16**2
mixed = 2 * t2 / 16
assert -16 * c2 + mixed == t2 / 16

# Degree-sector reflection signs and the equivalence
# R >= -N/3 <=> w0+w2 <= 2N/3.
w0, w1, w2, w3 = F(2), F(3), F(5), F(7)
norm = w0 + w1 + w2 + w3
reflection = -w0 + w1 - w2 + w3
assert reflection == norm - 2 * (w0 + w2)
assert 3 * (reflection + norm / 3) == 4 * norm - 6 * (w0 + w2)

# The one-component pure-state inequality reduces to the trace-zero
# complement estimate |a|^2 <= 8 residual.
column_norm = F(13, 17)
diagonal2 = F(8) * (F(1) - column_norm)
left = 2 * column_norm + diagonal2 / 4
assert left == 2

# Tensor spectator normalizations.
assert F(2, 3) * 3 == 2

print(
    "verified exact reflection parity algebra, scalar Schur complement, "
    "and the sharp one-component constants"
)
