#!/usr/bin/env python3
"""Exact checks for the pair-critical local spectral floor."""

import sympy as sp


f, m = sp.symbols("f m", positive=True)
kappa = sp.Rational(2, 3) - f

# The truncation estimate and its two equivalent rearrangements.
truncation_upper = sp.expand(kappa * (1 - m) + sp.Rational(2, 3) * m)
assert sp.simplify(
    truncation_upper
    - (1 - m) * (sp.Rational(2, 3) / (1 - m) - f)
) == 0
assert sp.simplify(
    (1 - sp.Rational(2, 3) / f)
    - (3 * f - 2) / (3 * f)
) == 0

# Exact sharp abstract model:
# rho=(1/2,1/4,1/4), e=vec(sqrt(rho)),
# H=2/3 I-(8/9)|e><e|.
rho_values = [sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 4)]
e = sp.zeros(9, 1)
for j, value in enumerate(rho_values):
    e[3 * j + j] = sp.sqrt(value)
assert (e.T * e)[0] == 1

H = sp.Rational(2, 3) * sp.eye(9) - sp.Rational(8, 9) * (e * e.T)
assert H * e == -sp.Rational(2, 9) * e

# The best rank-two truncation deletes one 1/4 Schmidt weight.
psi = sp.zeros(9, 1)
psi[0] = sp.sqrt(sp.Rational(2, 3))
psi[4] = sp.sqrt(sp.Rational(1, 3))
assert (psi.T * psi)[0] == 1
assert sp.simplify((e.T * psi)[0] ** 2) == sp.Rational(3, 4)
assert sp.simplify((psi.T * H * psi)[0]) == 0

# Spectrum: one eigenvalue -2/9 and eight eigenvalues 2/3.
assert H.eigenvals() == {
    -sp.Rational(2, 9): 1,
    sp.Rational(2, 3): 8,
}

# Determinant floor at the sharp model.
mu = sp.Rational(1, 4)
assert sp.prod(rho_values) == mu**2 * (1 - 2 * mu)

print(
    "verified the exact critical local spectral floor, determinant "
    "floor, and the sharp abstract two-block-positive model"
)
