#!/usr/bin/env python3
"""Discovery-only exact elimination on one generic-ell squarefree chart.

This fixes q=q0=xy(x-y), s=1, ell=x+c*y and substitutes the already
proved binary E5/E4 restrictions.  It is not a certificate: its purpose is
to expose the next linear pivots and residual factors for a uniform proof.
"""

from __future__ import annotations

import sympy as sp


x, y, z = sp.symbols("x y z")
c, w, k = sp.symbols("c w k")
r20, r11, r02, r10, r01 = sp.symbols("r20 r11 r02 r10 r01")
a = sp.symbols("a0:6")
b3, b4, b5 = sp.symbols("b3 b4 b5")
v4, v5, v6, v7, v8 = sp.symbols("v4 v5 v6 v7 v8")
l = sp.symbols("l0:9")

q = (
    x * y * (x - y)
    + z * (r20 * x**2 + r11 * x * y + r02 * y**2)
    + z**2 * (r10 * x + r01 * y)
)
quadratics = (x**2, x * y, y**2, x * z, y * z, z**2)
A = sum(coefficient * monomial for coefficient, monomial in zip(a, quadratics))
B = (
    k * (a[0] * x**2 + a[1] * x * y + a[2] * y**2)
    + b3 * x * z
    + b4 * y * z
    + b5 * z**2
)
W = z * (x + c * y + w * z)
V = (
    k * x * y * (x - y)
    + z * (v4 * x**2 + v5 * x * y + v6 * y**2)
    + z**2 * (v7 * x + v8 * y)
)
L = sp.Matrix(((l[0], l[1], l[2]), (l[3], l[4], l[5]), (0, 0, l[8])))

H2 = sp.Matrix((A, B, W))
H3 = sp.Matrix((sp.Rational(4, 3) * z * W + q, V, z**3))
H4 = sp.Matrix((z**4, z * q, 0))
determinant = sp.Poly(
    sp.expand(
        (L + H2.jacobian((x, y, z)) + H3.jacobian((x, y, z))
         + H4.jacobian((x, y, z))).det()
    ),
    x,
    y,
    z,
)


def equations(degree: int, substitutions: dict[sp.Symbol, sp.Expr] | None = None):
    substitutions = substitutions or {}
    return [
        sp.factor(coefficient.subs(substitutions))
        for monomial, coefficient in determinant.terms()
        if sum(monomial) == degree and coefficient.subs(substitutions) != 0
    ]


e6_unknowns = (v4, v5, v6, v7, v8)
e6 = equations(6)
m6, r6 = sp.linear_eq_to_matrix(e6, e6_unknowns)
print("E6", m6.shape, "rank", m6.rank(), "augmented", m6.row_join(r6).rank())
solution6 = sp.solve(e6, e6_unknowns, dict=True, simplify=False)
print("E6 solutions", len(solution6))
if not solution6:
    for monomial, coefficient in determinant.terms():
        if sum(monomial) == 6 and coefficient != 0:
            print("E6 residual", monomial, sp.factor(coefficient))
    expanded_unknowns = e6_unknowns + a
    expanded_matrix, expanded_rhs = sp.linear_eq_to_matrix(e6, expanded_unknowns)
    print(
        "E6 expanded",
        expanded_matrix.shape,
        "rank",
        expanded_matrix.rank(),
        "augmented",
        expanded_matrix.row_join(expanded_rhs).rank(),
    )
    expanded_solutions = sp.linsolve(
        (expanded_matrix, expanded_rhs), expanded_unknowns
    )
    print("E6 expanded solution", expanded_solutions)
    raise SystemExit(0)
for variable in e6_unknowns:
    print(variable, "=", sp.factor(solution6[0].get(variable, variable)))

e5 = equations(5, solution6[0])
e5_unknowns = (b3, b4, b5, l[3], l[4])
m5, r5 = sp.linear_eq_to_matrix(e5, e5_unknowns)
print("E5", m5.shape, "rank", m5.rank(), "augmented", m5.row_join(r5).rank())
solution5 = sp.solve(e5, e5_unknowns, dict=True, simplify=False)
print("E5 solutions", len(solution5))
if not solution5:
    for equation in e5:
        print("E5 residual", sp.factor(equation))
    raise SystemExit(0)
combined = {**solution6[0], **solution5[0]}
for variable in e5_unknowns:
    print(variable, "=", sp.factor(solution5[0].get(variable, variable)))

for degree in (4, 3, 2, 1, 0):
    residuals = equations(degree, combined)
    print(f"E{degree} residuals", len(residuals))
    for residual in residuals:
        print(sp.factor(residual))
