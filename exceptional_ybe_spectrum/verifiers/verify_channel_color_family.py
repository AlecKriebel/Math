#!/usr/bin/env python3
"""Exact channel certificate for the symbolic d=4 color/face family.

This imports the independently defined family from
``scripts/verify_color_face_d4_family.py`` and checks its canonical channels.
No numerical specialization of the parameters is used.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
FAMILY_PATH = ROOT / "scripts" / "verify_color_face_d4_family.py"
spec = importlib.util.spec_from_file_location("color_face_family", FAMILY_PATH)
assert spec is not None and spec.loader is not None
family = importlib.util.module_from_spec(spec)
spec.loader.exec_module(family)

h = family.H
s = family.s
t = family.t
relation = family.relation
d = 4
identity = sp.eye(d)
projection = (sp.eye(d * d) - h) / 2


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def partial_trace_second(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda i, k: sum(matrix[d * i + j, d * k + j] for j in range(d)),
    )


def partial_trace_first(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda j, ell: sum(
            matrix[d * i + j, d * i + ell] for i in range(d)
        ),
    )


def vectorize(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [matrix[i, j] for i in range(d) for j in range(d)]
    )


def channel(right: bool) -> sp.Matrix:
    columns = []
    for i in range(d):
        for j in range(d):
            matrix_unit = sp.zeros(d)
            matrix_unit[i, j] = 1
            insertion = (
                tensor(matrix_unit, identity)
                if right
                else tensor(identity, matrix_unit)
            )
            sandwiched = projection * insertion * projection
            image = sp.Rational(1, 2) * (
                partial_trace_second(sandwiched)
                if right
                else partial_trace_first(sandwiched)
            )
            columns.append(vectorize(image))
    return sp.Matrix.hstack(*columns)


channel_r = channel(right=True)
channel_l = channel(right=False)
identity_superoperator = sp.eye(d * d)
identity_vector = vectorize(identity)
omega = identity_vector * identity_vector.T / d

# Commutation is an identity of this ansatz, even before imposing the circle
# relation that makes H an exceptional solution.
assert all(
    sp.simplify(entry) == 0
    for entry in channel_r * channel_l - channel_l * channel_r
)
assert sp.simplify(sp.trace(channel_r) - 8) == 0
assert sp.simplify(sp.trace(channel_l) - 8) == 0
paired_residual = (
    (channel_r + channel_l - sp.Rational(4, 3) * identity_superoperator)
    * (channel_r - sp.Rational(1, 3) * identity_superoperator)
    * (channel_l - sp.Rational(1, 3) * identity_superoperator)
    - sp.Rational(8, 27) * omega
)
for entry in paired_residual:
    entry = sp.expand(entry)
    if entry == 0:
        continue
    quotient = sp.cancel(entry / relation)
    sp.Poly(quotient, s, t, extension=True)
    assert sp.expand(entry - relation * quotient) == 0

variable = sp.symbols("lambda")
expected = (
    (3 * variable - 1) ** 8
    * (-s**2 - 2 * t**2 + 3 * variable - 2) ** 4
    * (s**2 + 2 * t**2 + 3 * variable - 2) ** 4
    / 3**16
)
for canonical_channel in (channel_r, channel_l):
    characteristic = sp.factor(
        canonical_channel.charpoly(variable).as_expr(), extension=True
    )
    assert sp.expand(characteristic - expected) == 0

# On s^2+2t^2=1 this becomes (lambda-1)^4(lambda-1/3)^12.
on_solution = (variable - 1) ** 4 * (
    variable - sp.Rational(1, 3)
) ** 12
reduced_expected = sp.rem(
    sp.Poly(expected - on_solution, s, extension=True),
    sp.Poly(relation, s, extension=True),
).as_expr()
assert sp.expand(reduced_expected) == 0

print("Exact canonical channels for the color/face d=4 family")
print("[ok] [E_L,E_R] = 0 identically in s,t")
print("[ok] the paired joint-channel polynomial holds on the solution circle")
print("[ok] E_L and E_R have the same symbolic characteristic polynomial")
print("[ok] on s^2+2t^2=1: spectrum = {1^4, (1/3)^12}")
