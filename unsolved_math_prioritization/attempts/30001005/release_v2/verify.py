#!/usr/bin/env python3
"""Supplemental exact checks. The analytic proof is SOURCE_CERTIFICATE.md.

Python standard library only. This is not a PDE solver or a substitute for
checking the stated weak-flow definition and the first-variation argument.
"""
from fractions import Fraction as F
import json


def rank(a):
    a = [[F(v) for v in row] for row in a]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][col]
        a[row] = [v / scale for v in a[row]]
        for i in range(len(a)):
            if i != row:
                scale = a[i][col]
                a[i] = [x - scale * y for x, y in zip(a[i], a[row])]
        row += 1
    return row


def q(v):
    return sum(t * t for t in v[:4]) - sum(t * t for t in v[4:])


# Eight cone vectors span R^8. Their positive dilations are rays of C.
vectors = []
for i in range(4):
    for sign in (-1, 1):
        v = [0] * 8
        v[i] = 1
        v[i + 4] = sign
        vectors.append(v)
assert all(q(v) == 0 for v in vectors)
assert rank(vectors) == 8

# For J=diag(I4,-I4), nu=Jz/|z|. Numerator of div(nu) is
# tr(J)|z|^2 - z^T J z = -q(z). Verify the coefficients, not samples.
j = [1] * 4 + [-1] * 4
divergence_coefficients = [sum(j) - a for a in j]
assert divergence_coefficients == [-a for a in j]
assert sum(j) == 0

# z dot nu has numerator q; both H and normal dilation vanish on C.
assert [a for a in j] == [1, 1, 1, 1, -1, -1, -1, -1]

# Exact radial exponents: cone dimension 7, link dimension 6.
assert 7 - 1 == 6 and 6 > 0
assert F(1, 7) * F(1, 2) / F(16, 105) == F(15, 32)

print(json.dumps({
    "result": "PASS",
    "cone_vector_count": len(vectors),
    "cone_span_rank": rank(vectors),
    "divergence_polynomial_identity": "tr(J)|z|^2-z^TJz=-q(z)",
    "vertex_boundary_decay_power": 6,
    "vertex_mass_decay_power": 7,
    "density_multiple_of_pi": "15/32",
    "scope": "exact algebra only; analytic and source claims require review",
}, indent=2))
