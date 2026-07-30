#!/usr/bin/env python3
"""Exact rational checker for the stationary one-body obstruction."""

from fractions import Fraction as F


# One exact member of the open family 0 < delta < 1/8.
delta = F(1, 16)

# Schur-normalized sector reconstruction identities.
u = F(2, 3) - F(16, 3) * delta
a_normalized = F(0)
c_normalized = (1 + delta) / 3
norm_normalized = (
    4 * delta + F(3, 4) * u + F(9, 4) * a_normalized
)
x_normalized = (
    F(32, 9) * delta
    - F(4, 9)
    + F(2, 3) * u
    + F(4, 3) * a_normalized
)
d_normalized = (
    (1 + delta) / 9 + u / 12 - a_normalized / 12
)
assert norm_normalized == F(1, 2)
assert x_normalized == 0
assert c_normalized == (1 + delta) / 3
assert d_normalized == (1 - 2 * delta) / 6

# Summed local-filter trace identities in the sigma=1 normalization.
trace_h = F(15, 8) * (x_normalized - a_normalized) + F(15, 2) * d_normalized
trace_k = F(16, 3) * a_normalized + F(17, 3) * c_normalized + d_normalized
trace_depth = 2 * (1 + delta) * trace_h + 3 * delta * trace_k
trace_depth_reconstructed = (
    21 * delta * (1 + delta)
    + (F(15, 4) + 4 * delta) * u
    + F(63, 4) * delta * a_normalized
)
assert trace_depth == trace_depth_reconstructed
assert trace_depth > 0

# Unscaled isotropic obstruction: N=1, sigma=2.
x = F(0)
a = F(0)
c = 2 * (1 + delta) / 3
d = (1 - 2 * delta) / 3
N = x + a + c + d
Q = -delta
sigma = 2 * Q + 3 * c
Delta = F(0)
assert N == 1
assert sigma == 2
assert Q == -delta
assert a < F(2, 3) * delta * sigma + F(4, 9) * Delta

# Complete isotropic local endpoint form.
t = 5 * (1 - 8 * delta) / 48
h_scalar = -delta / 3
h_traceless = 2 * delta / 3 + t
n_eigenvalue = F(1, 3)
assert h_scalar + delta * n_eigenvalue == 0
assert h_traceless + delta * n_eigenvalue > 0

# Complete isotropic pair-sector form.
k_scalar = 2 * (1 + delta) / 9
k_traceless = (31 + 22 * delta) / 216
f = c / N
assert 3 * k_scalar == c
assert f * n_eigenvalue - k_scalar == 0
assert f * n_eigenvalue - k_traceless > 0

# Complete negative-depth local Hessian.
m_scalar = 2 * (1 + delta) * h_scalar + 3 * delta * k_scalar
m_traceless = (
    2 * (1 + delta) * h_traceless + 3 * delta * k_traceless
)
assert m_scalar == 0
assert m_traceless > 0

# The local traces agree with the global sector contractions.
local_trace_h = h_scalar + 8 * h_traceless
local_trace_k = k_scalar + 8 * k_traceless
assert 3 * local_trace_h == F(5, 2) * (1 - 2 * delta)
assert 3 * local_trace_k == (37 + 28 * delta) / 9

print(
    "verified: exact a=Delta=0 data violate the proposed one-body "
    "bound while satisfying all isotropic one-site Euler equations, "
    "endpoint/pair/depth Hessians, and global trace identities"
)
