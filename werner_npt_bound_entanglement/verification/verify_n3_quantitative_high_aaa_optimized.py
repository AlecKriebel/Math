#!/usr/bin/env python3
"""Dependency-free exact audit of the optimized high-AAA constants."""

from fractions import Fraction as F


eps = F(1, 10**28)
eps_quarter = F(1, 10**7)

# The concentration alternatives are impossible in the stated range.
assert F(4, 3) > F(648) * eps
assert F(4, 3) > F(1928) * eps

# Every high-site Pauli component has weight > 2/5.
assert F(4, 9) - F(656) * eps > F(2, 5)

# The local-gap and purity simplifications used in (7)--(9).
assert F(400, 9) < F(45)
assert F(324) * eps < eps_quarter**2  # 324 h < sqrt(h)

# The Hodge perturbation is inside every spectral-gap regime used.
eta = F(70) * eps_quarter
assert eta < F(1, 16)
assert eta < F(1, 10)  # and hence eta < r/4 because r > 2/5

# Plane-alignment constants:
# 24*eta + 8*sqrt(eps) <= (1680+8)*eps^(1/4).
assert F(24) * F(70) + F(8) == F(1688)
assert F(384, 7) < F(55)

# Feature perturbation and local concurrence thresholds.
q = F(13504) * eps_quarter
assert F(8) * F(1688) == F(13504)
assert q < F(2, 27)
assert F(36) * q == F(486144, 10**7)
assert F(36) * q < F(4, 27)

# Improved face-depth ceiling.
beta = (
    F(648) + F(2187) * eps
) / (
    F(5112) + F(21141) * eps
)
assert beta > F(13, 107)
assert beta < F(9, 71)
assert F(9, 71) - beta == (
    F(34992) * eps
    / (F(71) * (F(5112) + F(21141) * eps))
)

print("optimized quantitative high-AAA constants: exact")
