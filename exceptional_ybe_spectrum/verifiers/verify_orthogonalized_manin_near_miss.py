#!/usr/bin/env python3
"""Exact d=6 check of the orthogonalized Manin Grassmann starting point.

This is a verifier for a numerical-search calibration, not an exceptional
Yang--Baxter witness.  It constructs the orthogonal projection onto the
(-1)-eigenspace of the balanced standard GL(3|3) Manin operator and checks
the resulting Hermitian involution exactly.
"""

from __future__ import annotations

import platform
import sys

import sympy as sp


def exact_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix.todok().values())


d = 6
n = d * d
t = (sp.sqrt(3) + sp.I) / 2

projector = sp.MutableSparseMatrix(n, n, {})

# Odd diagonal vectors are (-1)-eigenvectors of the Manin operator.
for odd in range(3, 6):
    projector[odd * d + odd, odd * d + odd] = 1

# For every unordered pair, the normalized vector
# (|ij> - t |ji>)/sqrt(2) is a (-1)-eigenvector.  The supports of all
# eighteen vectors are disjoint, so this is already an orthonormal frame.
for first in range(d):
    for second in range(first + 1, d):
        left = first * d + second
        right = second * d + first
        projector[left, left] = sp.Rational(1, 2)
        projector[right, right] = sp.Rational(1, 2)
        projector[left, right] = -sp.conjugate(t) / 2
        projector[right, left] = -t / 2

projector = sp.SparseMatrix(projector)
identity_pair = sp.eye(n)
assert exact_zero(projector.conjugate().T - projector)
assert exact_zero(projector * projector - projector)
assert projector.rank() == 18

h = sp.SparseMatrix(identity_pair - 2 * projector)
assert exact_zero(h.conjugate().T - h)
assert exact_zero(h * h - identity_pair)
assert sp.trace(h) == 0

identity_local = sp.eye(d)
h1 = sp.kronecker_product(h, identity_local)
h2 = sp.kronecker_product(identity_local, h)
residual = h1 * h2 * h1 - h2 * h1 * h2 - (h1 - h2) / 3
nonzero = [
    sp.simplify(value)
    for value in residual.todok().values()
    if sp.simplify(value) != 0
]
residual_norm_squared = sp.simplify(
    sum(sp.conjugate(value) * value for value in nonzero)
)
assert residual_norm_squared == sp.Rational(140, 3)

h_tensor = sp.MutableDenseNDimArray(h, (d, d, d, d))
partial_second = sp.zeros(d)
partial_first = sp.zeros(d)
for i in range(d):
    for k in range(d):
        partial_second[i, k] = sum(
            h_tensor[i, j, k, j] for j in range(d)
        )
for j in range(d):
    for ell in range(d):
        partial_first[j, ell] = sum(
            h_tensor[i, j, i, ell] for i in range(d)
        )

def scalar_deviation_norm_squared(matrix: sp.MatrixBase) -> sp.Expr:
    scalar = sp.trace(matrix) / d
    deviation = matrix - scalar * sp.eye(d)
    return sp.simplify(
        sum(
            sp.conjugate(deviation[row, column])
            * deviation[row, column]
            for row in range(d)
            for column in range(d)
        )
    )


left_deviation = scalar_deviation_norm_squared(partial_first)
right_deviation = scalar_deviation_norm_squared(partial_second)
assert left_deviation == 6
assert right_deviation == 6

print("PASS exact orthogonalized Manin d=6 near-miss")
print("  rank(P) = 18")
print("  H is a trace-zero Hermitian involution")
print(f"  cubic residual Frobenius norm squared = {residual_norm_squared}")
print(f"  left partial-trace scalar-deviation norm squared = {left_deviation}")
print(f"  right partial-trace scalar-deviation norm squared = {right_deviation}")
print("  conclusion: this Grassmann starting point is not a YB solution")
print("  scope: calibration/failed-construction certificate only")
print(f"  Python {sys.version.split()[0]}")
print(f"  SymPy {sp.__version__}")
print(f"  platform {platform.platform()}")
