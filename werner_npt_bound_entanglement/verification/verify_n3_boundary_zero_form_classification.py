#!/usr/bin/env python3
"""Exact checks for the boundary zero-form classification constants."""

from fractions import Fraction as F


# On the scalar and traceless sectors of M_3, the one-copy endpoint
# superoperator has eigenvalues -1/2 and 1.
endpoint_eigenvalues = (F(-1, 2),) + (F(1),) * 8
assert sum(endpoint_eigenvalues) == F(15, 2)

# Q_1 on rank-two and rank-one coordinate projections.
def q1(rank: int) -> F:
    return F(rank) - F(1, 2) * F(rank * rank)


assert q1(2) == 0
assert q1(1) == F(1, 2)
assert q1(3) == F(-3, 2)

# At the formal negative Haar-equality point, Q_3=-1/8 and therefore
# gamma=-2 Q_3/3=1/12.
w0, w1, w2, w3 = F(1, 9), F(0), F(2, 3), F(2, 9)
q3 = F(-1, 8) * w0 + F(1, 4) * w1 - F(1, 2) * w2 + w3
gamma = -F(2, 3) * q3
assert q3 == F(-1, 8)
assert gamma == F(1, 12)
assert gamma * q1(3) == q3

# The supertrace of each local form gamma L is -5 Q_3.
assert gamma * sum(endpoint_eigenvalues) == -5 * q3

print("exact boundary zero-form classification constants verified")
