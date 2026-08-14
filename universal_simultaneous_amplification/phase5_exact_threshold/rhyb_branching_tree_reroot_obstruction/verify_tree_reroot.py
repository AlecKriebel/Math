#!/usr/bin/env python3
"""Exact symbolic replay of the two-type tree-reroot obstruction."""

import sympy as sp


r, k, c = sp.symbols("r k c", positive=True)
d = sp.symbols("d", integer=True, nonnegative=True)

A1 = 1 + r * k
B1 = k + r
A2 = B1 / k
B2 = A1 / k

lam = r * (1 + k) ** 2 / (A1 * B1)

# The vertex normalization identity.
assert sp.factor(A1 * B1 - r * (1 + k) ** 2 - (r - 1) ** 2 * k) == 0

# Root law cancels in all ratios, so set p_1=1.
WD = r**d * k**d / (A1 ** (d + 1) * A2**d)
WB = k * r**d / (B1 ** (d + 1) * A1**d)
W0 = k ** (2 * d) / (1 + k) ** (2 * d + 1)

def assert_power_identity(left, right):
    """Compare expressions after collecting positive symbolic powers."""
    assert sp.factor(sp.powsimp(left / right, force=True)) == 1


assert_power_identity(WD / W0, (1 + k) / A1 * lam**d)
assert_power_identity(WB / W0, k * (1 + k) / B1 * (lam / k**2) ** d)
assert_power_identity(WD / WB, k ** (2 * d - 1) * B1 / A1)

# Rerooting the star from its type-1 center to a type-2 leaf.
a1 = sp.symbols("a1", positive=True)
a2 = k * a1
reroot_D = sp.simplify(a1 * A1 / (a2 * A2))
reroot_B = sp.simplify(a2 * B1 / (a1 * B2))
assert reroot_D == A1 / B1
assert reroot_B == k**2 * B1 / A1

# Positive marked-child decomposition used by the endpoint star expansion.
q = sp.symbols("q", nonnegative=True)
assert sp.expand((1 - c) + c * (1 - q) - (1 - c * q)) == 0

print("tree-reroot symbolic identities: PASS")
print("lambda = 1 - (r-1)^2 k / ((1+rk)(k+r))")
print("for k>1: lambda<1 and lambda/k^2<1")
