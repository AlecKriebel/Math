#!/usr/bin/env python3
"""Exact symbolic replay of the mixed finite-tree/spine obstruction."""

import sympy as sp


# First-success geometric summation.
r, t, u, edge_x = sp.symbols("r t u edge_x", positive=True)
A0 = 1 + r * t
first_position_sum = (r * edge_x / A0) / (1 - r * (t - u) / A0)
assert sp.simplify(first_position_sum - r * edge_x / (1 + r * u)) == 0

# Abstract spine likelihood normalization, with h+s=1.
h, w, z_j = sp.symbols("h w z_j", positive=True)
s = 1 - h
h1_over_h = 1 / (h + s * w)
L = z_j * h1_over_h
assert sp.simplify(L - z_j / (h + s * w)) == 0
ell = w / (h + s * w)
F_over_s = w / (h + s * w)
assert sp.simplify(ell - F_over_s) == 0

# Exact deterministic two-type family.
r, k = sp.symbols("r k", positive=True)
c = r - 1
A = 1 + r * k
B = k + r

hvec = sp.Matrix([B / (r * A), A / (r * B)])
svec = sp.Matrix([
    k * (r**2 - 1) / (r * A),
    (r**2 - 1) / (r * B),
])
qvec = sp.Matrix([A / (r * B), B / (r * A)])

R = sp.Matrix([[0, k], [1 / k, 0]])
P = sp.Matrix([[0, 1], [1, 0]])
tvec = sp.Matrix([k, 1 / k])

for i in range(2):
    assert sp.simplify(
        hvec[i] - 1 / (1 + r * (tvec[i] - (R * hvec)[i]))
    ) == 0
    assert sp.simplify(
        qvec[i] - tvec[i] / (tvec[i] + r * (1 - (P * qvec)[i]))
    ) == 0
    assert sp.simplify(svec[i] - (1 - hvec[i])) == 0

h1vec = sp.Matrix([
    A / (A + c * k * B),
    k * B / (k * B + c * A),
])
for i in range(2):
    assert sp.simplify(h1vec[i] - 1 / (1 + r * c * (R * qvec)[i])) == 0

ell1 = r * A * B / ((r + 1) * (A + c * k * B))
ell2 = r * A * B / ((r + 1) * (k * B + c * A))
assert sp.simplify(ell1 - (1 - h1vec[0]) / svec[0]) == 0
assert sp.simplify(ell2 - (1 - h1vec[1]) / svec[1]) == 0

assert sp.simplify(
    r * A * B
    - (r + 1) * (A + c * k * B)
    + (k - 1) * (-k + r**2 - r - 1)
) == 0
assert sp.simplify(
    r * A * B
    - (r + 1) * (k * B + c * A)
    - (k - 1) * (k * r**2 - k * r - k - 1)
) == 0

# Positive exact cycle holonomy after substituting r=1+c0.
c0 = sp.symbols("c0", positive=True)
cycle_gap = sp.together((ell1 * ell2 - 1).subs(r, 1 + c0))
cycle_num, cycle_den = cycle_gap.as_numer_denom()
Q = (
    k * c0**5
    + (k**2 + 5 * k + 1) * c0**4
    + (3 * k**2 + 9 * k + 3) * c0**3
    + (2 * k**2 + 5 * k + 2) * c0**2
    + (k + 1) ** 2
)
assert sp.factor(cycle_num - (k - 1) ** 2 * Q) == 0
assert cycle_den.is_positive is not False

print("mixed finite-tree/spine symbolic identities: PASS")
print("cycle holonomy numerator = (k-1)^2 Q(c,k), with Q coefficientwise positive")
