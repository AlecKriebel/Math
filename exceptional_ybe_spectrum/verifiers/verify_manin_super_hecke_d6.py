#!/usr/bin/env python3
"""Exact d=6 audit of the balanced Manin super-Hecke candidate.

The verifier uses ordinary Kronecker placements throughout.  It checks
the braid and Hecke identities directly over Q(sqrt(3), i), determines
the two eigenspace dimensions, and replays the local-metric obstruction.
"""

from __future__ import annotations

import platform
import sys

import sympy as sp


def exact_zero(matrix: sp.MatrixBase) -> bool:
    """Test a sparse algebraic matrix after simplifying every stored entry."""

    return all(sp.simplify(value) == 0 for value in matrix.todok().values())


def basis_vector(dimension: int, index: int) -> sp.SparseMatrix:
    return sp.SparseMatrix(dimension, 1, {(index, 0): sp.Integer(1)})


half = sp.Rational(1, 2)
sqrt3 = sp.sqrt(3)
t = half * (sqrt3 + sp.I)
q = sp.expand(t**2)

assert sp.simplify(q - (1 + sp.I * sqrt3) / 2) == 0
assert sp.simplify(sp.conjugate(t) - t + sp.I) == 0

s = 3
d = 2 * s
parity = (0,) * s + (1,) * s

candidate_mutable = sp.MutableSparseMatrix(d * d, d * d, {})
for i in range(d):
    for j in range(d):
        column = i * d + j
        if i == j:
            candidate_mutable[column, column] = q if parity[i] == 0 else -1
        elif i < j:
            candidate_mutable[column, column] = q - 1
            candidate_mutable[j * d + i, column] = (
                (-1) ** (parity[i] * parity[j]) * t
            )
        else:
            candidate_mutable[j * d + i, column] = (
                (-1) ** (parity[i] * parity[j]) * t
            )

candidate = sp.SparseMatrix(candidate_mutable)
identity_d = sp.eye(d)
identity_d2 = sp.eye(d * d)

# The exact Hecke polynomial in the exceptional normalization.
hecke_residual = (candidate + identity_d2) * (candidate - q * identity_d2)
assert exact_zero(hecke_residual)

# Ordinary, not graded, tensor placements.
candidate_1 = sp.kronecker_product(candidate, identity_d)
candidate_2 = sp.kronecker_product(identity_d, candidate)
braid_residual = (
    candidate_1 * candidate_2 * candidate_1
    - candidate_2 * candidate_1 * candidate_2
)
assert exact_zero(braid_residual)

# Direct eigenspace dimensions; the square-free polynomial then gives the
# algebraic multiplicities as well.
q_eigenspace_dimension = d * d - (candidate - q * identity_d2).rank()
minus_eigenspace_dimension = d * d - (candidate + identity_d2).rank()
assert q_eigenspace_dimension == 18
assert minus_eigenspace_dimension == 18
assert sp.simplify(sp.trace(candidate) - 18 * (q - 1)) == 0

# The matrix is not unitary in the standard product metric.
standard_unitarity_defect = candidate.conjugate().T * candidate - identity_d2
defect_values = [
    sp.simplify(value)
    for value in standard_unitarity_defect.todok().values()
    if sp.simplify(value) != 0
]
defect_frobenius_squared = sp.simplify(
    sum(sp.conjugate(value) * value for value in defect_values)
)
assert defect_frobenius_squared == 45

# Replay the two eigenvector identities used in the arbitrary-local-metric
# no-go.  Every even i and odd a gives the same contradiction.
for i in range(s):
    for a in range(s, d):
        even_diagonal = basis_vector(d * d, i * d + i)
        odd_diagonal = basis_vector(d * d, a * d + a)
        assert exact_zero(candidate * even_diagonal - q * even_diagonal)
        assert exact_zero(candidate * odd_diagonal + odd_diagonal)

        x = basis_vector(d * d, i * d + a)
        y = basis_vector(d * d, a * d + i)
        q_vector = t * x + y
        minus_vector = x - t * y
        assert exact_zero(candidate * q_vector - q * q_vector)
        assert exact_zero(candidate * minus_vector + minus_vector)

# If G_ia=0, x and y are orthogonal and have the same squared norm c>0.
# Their q/-1 eigenvectors then have inner product (conj(t)-t)c=-i c.
c = sp.Symbol("c", positive=True, real=True)
mixed_eigenvector_inner_product = sp.simplify((sp.conjugate(t) - t) * c)
assert mixed_eigenvector_inner_product == -sp.I * c
assert mixed_eigenvector_inner_product != 0

print("PASS exact d=6 balanced Manin super-Hecke audit")
print(f"  q = {q}")
print(f"  t = {t}")
print("  ordinary braid residual = 0 on dimension 216")
print("  Hecke residual = 0 on dimension 36")
print(
    "  eigenspace multiplicities (q, -1) = "
    f"({q_eigenspace_dimension}, {minus_eigenspace_dimension})"
)
print(f"  trace = {sp.simplify(sp.trace(candidate))}")
print(
    "  standard-metric unitarity-defect Frobenius norm squared = "
    f"{defect_frobenius_squared}"
)
print("  local-metric obstruction coefficient = (conj(t)-t)c = -I*c")
print("  conclusion: no positive tensor-square local metric can unitarize T")
print("  scope: standard one-parameter Manin ansatz only")
print(f"  Python {sys.version.split()[0]}")
print(f"  SymPy {sp.__version__}")
print(f"  platform {platform.platform()}")
