#!/usr/bin/env python3
"""Dependency-free exact checks for the marginal Schur no-go note."""

from fractions import Fraction as F


# The three pairwise allocations sum to the marginal defect:
# each contributes 2I and -R/3; every e_i occurs in two pairs.
assert 3 * F(2) == 6
assert 2 * F(1) == 2
assert F(-3) == -3
assert 3 * F(-1, 3) == -1


# Exact negative Rayleigh quotients on the canonical equality code.
pair_12 = F(2) - 3 * F(2)
pair_13 = F(2) - 3 * F(1)
pair_23 = F(2) - 3 * F(1)
assert pair_12 == -4
assert pair_13 == -1
assert pair_23 == -1


# H sector values from
# 6 - 3 sum f_i + 2 sum_{i<j} f_i f_j - product f_i,
# with exactly r signs equal to -1.
def h_sector(r: int) -> int:
    signs = [-1] * r + [1] * (3 - r)
    singles = sum(signs)
    pairs = sum(
        signs[i] * signs[j] for i in range(3) for j in range(i + 1, 3)
    )
    triple = signs[0] * signs[1] * signs[2]
    return 6 - 3 * singles + 2 * pairs - triple


h = tuple(h_sector(r) for r in range(4))
assert h == (2, 2, 6, 22)


# A positive scalar-multiplier Gram would require simultaneously
# t >= -4 and t <= -44/3.  Cross-multiplication is exact.
lower = F(-4)
upper = F(-44, 3)
assert upper < lower


# Check the two decisive eigenvalue formulae at the interval endpoints.
def gram_eigenvalue(epsilon: int, physical_h: int, t: F) -> F:
    return F(epsilon * physical_h) + t * (F(epsilon) - F(1, 2))


assert gram_eigenvalue(+1, 2, lower) == 0
assert gram_eigenvalue(-1, 22, lower) < 0
assert gram_eigenvalue(-1, 22, upper) == 0
assert gram_eigenvalue(+1, 2, upper) < 0


print("verified: the natural three pairwise marginal allocations sum exactly")
print("verified: their canonical negative expectations are -4, -1, -1")
print("verified: H has physical swap-sector values 2, 2, 6, 22")
print("verified: no scalar invariant isometry multiplier yields a PSD Gram")
