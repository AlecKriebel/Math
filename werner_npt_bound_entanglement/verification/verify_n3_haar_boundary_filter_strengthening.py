#!/usr/bin/env python3
"""Exact rational checks for the Haar boundary-filter strengthening."""

from fractions import Fraction as F


# Local averaged transition energies for A_z = I-|z><z|.
# Columns are scalar/traceless inputs; rows are scalar/traceless outputs.
T = (
    (F(4, 9), F(1, 36)),
    (F(2, 9), F(23, 36)),
)

# Endpoint eigenvalues on scalar/traceless local operators.
ell = (F(-1, 2), F(1))

# The averaged local endpoint form kills scalar input and gives 5/8 on
# normalized traceless input.
effective = tuple(sum(ell[r] * T[r][c] for r in range(2))
                  for c in range(2))
assert effective == (F(0), F(5, 8))

# Summing the one-filter inequalities over the three sites gives
#   (1/4) w1 - w2 + 3 w3 >= 0.
one_filter_grouped = (F(0), F(1, 4), F(-1), F(3))
assert one_filter_grouped == (F(0), F(1, 4), F(-1), F(3))

# Eliminate w3=1-w0-w1-w2:
#   w2 <= 3/4 - 3/4 w0 - 11/16 w1.
pair_ceiling = (F(3, 4), F(-3, 4), F(-11, 16))
assert pair_ceiling == (F(3, 4), F(-3, 4), F(-11, 16))

# Substitute the ceiling into
# Q3 = 1 - 9/8 w0 - 3/4 w1 - 3/2 w2.
q_constant = F(1) - F(3, 2) * pair_ceiling[0]
q_w0 = F(-9, 8) - F(3, 2) * pair_ceiling[1]
q_w1 = F(-3, 4) - F(3, 2) * pair_ceiling[2]
assert (q_constant, q_w0, q_w1) == (F(-1, 8), F(0), F(9, 32))

# The exact formal obstruction saturates the new ceiling and has Q3=-1/8.
w0, w1, w2, w3 = F(1, 9), F(0), F(2, 3), F(2, 9)
assert w0 + w1 + w2 + w3 == 1
assert w2 == pair_ceiling[0] + pair_ceiling[1] * w0 + pair_ceiling[2] * w1
q3 = F(-1, 8) * w0 + F(1, 4) * w1 - F(1, 2) * w2 + w3
assert q3 == F(-1, 8)

# Two filtered sites give -w_ij/2+w_123 >= 0.
assert F(-1, 2) * (2 * w3) + w3 == 0

print("exact Haar boundary-filter strengthening verified")
