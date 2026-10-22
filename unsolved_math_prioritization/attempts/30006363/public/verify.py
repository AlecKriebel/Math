#!/usr/bin/env python3
"""Exact checks for PROOF.md; no network, source downloads, or search.

Requires Python 3.11+ and SymPy 1.14.0. The checks are examples and algebra,
not a machine proof of helicity invariance under arbitrary homeomorphisms.
Run: python verify.py
"""

import json
from pathlib import Path

import sympy as s

x, y, z = s.symbols("x y z", real=True)
n = s.symbols("n", integer=True, positive=True)
k = s.symbols("k", integer=True, positive=True)
q = 2 * s.pi
coords = (x, y, z)
checks = {}


def simplified(value):
    if isinstance(value, s.MatrixBase):
        return value.applyfunc(s.simplify)
    return s.simplify(value)


def equal(name, lhs, rhs):
    delta = simplified(lhs - rhs)
    if isinstance(delta, s.MatrixBase):
        passed = delta == s.zeros(*delta.shape)
    else:
        passed = delta == 0
    assert passed, (name, delta)
    checks[name] = {"passed": True, "value": str(simplified(lhs))}


def curl(v):
    return s.Matrix([
        s.diff(v[2], y) - s.diff(v[1], z),
        s.diff(v[0], z) - s.diff(v[2], x),
        s.diff(v[1], x) - s.diff(v[0], y),
    ])


def div(v):
    return sum(s.diff(v[j], coords[j]) for j in range(3))


def integral(value):
    for variable in coords:
        value = s.integrate(value, (variable, 0, 1))
    return s.simplify(value)


# Section 1: orientation reversal is outside the question's hypotheses.
B = s.Matrix([s.sin(q * z), s.cos(q * z), 0])
R = s.diag(-1, 1, 1)
C = R * B
equal("reflection_determinant", R.det(), s.Integer(-1))
equal("positive_beltrami_curl", curl(B), q * B)
equal("negative_beltrami_curl", curl(C), -q * C)
equal("positive_helicity", integral((B / q).dot(B)), 1 / q)
equal("negative_helicity", integral((-C / q).dot(C)), -1 / q)

# Section 3: n is an arbitrary positive integer, not a sampled range.
hn = s.Matrix([x, y + s.sin(q * n * x) / n, z])
J = hn.jacobian(coords)
U = s.Matrix([s.sin(q * z), 0, 0])
Un = s.Matrix([s.sin(q * z), q * s.cos(q * n * x) * s.sin(q * z), 0])
AU = s.Matrix([0, s.cos(q * z) / q, 0])
AUn = s.Matrix([-s.cos(q * z) * s.cos(q * n * x), s.cos(q * z) / q, 0])
equal("shear_jacobian", J.det(), s.Integer(1))
equal("shear_pushforward", J * U, Un)
equal("original_shear_primitive", curl(AU), U)
equal("pushed_shear_primitive", curl(AUn), Un)
equal("shear_divergence", div(Un), s.Integer(0))
equal("shear_squared_L2_error", integral((Un - U).dot(Un - U)), s.pi ** 2)
equal("shear_helicity_density", AUn.dot(Un), s.Integer(0))

# Section 4: exactness, eight nondegenerate zeroes, and indices.
X = s.Matrix([s.sin(q * y), s.sin(q * z), s.sin(q * x)])
A = -s.Matrix([s.cos(q * z), s.cos(q * x), s.cos(q * y)]) / q
equal("indexed_field_divergence", div(X), s.Integer(0))
equal("indexed_field_primitive", curl(A), X)
equal("indexed_field_helicity", integral(A.dot(X)), s.Integer(0))
DX = X.jacobian(coords)
indices = []
for i in range(2):
    for j in range(2):
        for ell in range(2):
            point = (s.Rational(i, 2), s.Rational(j, 2), s.Rational(ell, 2))
            subs = dict(zip(coords, point))
            equal(f"zero_{i}{j}{ell}", X.subs(subs), s.zeros(3, 1))
            index = (-1) ** (i + j + ell)
            equal(f"index_{i}{j}{ell}", DX.subs(subs).det() / q ** 3, s.Integer(index))
            indices.append(index)
equal("total_index", s.Integer(sum(indices)), s.Integer(0))
equal("boundary_radius_lower_bound", 4 * s.Rational(1, 8), s.Rational(1, 2))

# Section 6: exact commuting field and divergent variation lower bound.
V = s.Matrix([0, s.sin(q * z), 0])
AV = s.Matrix([-s.cos(q * z) / q, 0, 0])
equal("rough_shear_field_primitive", curl(AV), V)
equal("rough_shear_field_divergence", div(V), s.Integer(0))
equal("rough_shear_field_helicity", integral(AV.dot(V)), s.Integer(0))
equal("oscillatory_extremal_values", s.sin(s.pi / 2 + k * s.pi), (-1) ** k)
N = s.symbols("N", positive=True)
K = s.symbols("K", positive=True)
variation_lower_bound = 2 * (N - K) / s.sqrt(s.pi / 2 + N * s.pi)
assert s.limit(variation_lower_bound, N, s.oo) == s.oo
checks["variation_lower_bound_diverges"] = {"passed": True, "value": "oo for every fixed K"}

result = {
    "problem_id": 30006363,
    "sympy_version": s.__version__,
    "all_checks_passed": True,
    "number_of_checks": len(checks),
    "scope": "Exact example identities only; no verification of the unrestricted conjecture.",
    "checks": checks,
}
out = Path(__file__).with_name("verification.json")
out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({key: result[key] for key in ("problem_id", "all_checks_passed", "number_of_checks", "scope")}, indent=2))
