#!/usr/bin/env python3
"""Exact algebra replay for the paired BDM trace-cone reduction."""

import sympy as sp


r, z, K = sp.symbols("r z K", positive=True)
c = r - 1
a, b, s = sp.symbols("a b s", positive=True)

# Exact bounded-module support formula.
B = s * (r * b / c * z / (1 + z) - 1)
D = s * (r * a * K / (K + z) - 1)
support = sp.factor(D + c * B)
target = s * (r * a * K / (K + z) + r * b * z / (1 + z) - r)
assert sp.factor(support - target) == 0

# The one-charge identity for distinct rule-specific marginal weights.
B0, D0, wB, wD = sp.symbols("B0 D0 wB wD")
slack = -(D0 + c * B0)
assembled = c * wB * B0 + wD * D0
charge_form = -wD * slack + c * (wB - wD) * B0
assert sp.expand(assembled - charge_form) == 0

# Exact physical marginal-cone obstruction: leaf versus the z -> 0 K2 ray.
# On K2, rho_dB=1/2, hence a=1/(2(r-1)).
K2_B = sp.simplify(B.subs({s: 2, b: r / (r + 1), z: 0}))
K2_D = sp.simplify(D.subs({s: 2, a: 1 / (2 * c), z: 0}))
K2_support = sp.factor(K2_D + c * K2_B)
assert K2_B == -2
assert K2_D == (2 - r) / c
assert sp.factor(K2_support - r * (3 - 2 * r) / c) == 0

leaf_B = 1 / c
leaf_D = -1
assert sp.factor(leaf_D + c * leaf_B) == 0
assert sp.factor(leaf_B) == 1 / c
assert sp.factor(K2_D - (2 - r) / c) == 0

# The strict trivial-BDM branch follows just by replacing both gate
# fractions by one; this records the cleared difference exactly.
gamma = sp.symbols("gamma", positive=True)
upper_at_boundary = sp.factor(s * r * ((1 - gamma) - 1))
assert upper_at_boundary == -s * r * gamma

print("PASS exact paired support identity")
print("PASS exact one-charge marginal synchronization identity")
print("PASS leaf/K2 marginal-cone obstruction for 3/2 < r < 2")
print("K2 support factor:", K2_support)
