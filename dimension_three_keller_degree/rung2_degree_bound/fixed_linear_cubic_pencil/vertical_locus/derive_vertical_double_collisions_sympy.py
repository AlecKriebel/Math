#!/usr/bin/env python3
"""Discovery-only exact equations on the two double-root/ell collisions."""

from __future__ import annotations

import sympy as sp


x, y, z = sp.symbols("x y z")
s, w, k, h = sp.symbols("s w k h")
r20, r11, r02, r10, r01 = sp.symbols("r20 r11 r02 r10 r01")
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
t = sp.symbols("t4:9")
l = sp.symbols("l0:9")

quadratics = (x**2, x * y, y**2, x * z, y * z, z**2)
A = sum(coefficient * monomial for coefficient, monomial in zip(a, quadratics))
B = sum(coefficient * monomial for coefficient, monomial in zip(b, quadratics))
q0 = x**2 * y
q = (
    q0
    + z * (r20 * x**2 + r11 * x * y + r02 * y**2)
    + z**2 * (r10 * x + r01 * y)
)

collisions = {
    "ell_x": (
        x,
        k * q0 + sp.Rational(2, 3) * h * x * y**2,
        (0, h),
    ),
    "ell_y": (
        y,
        k * q0 + sp.Rational(1, 3) * h * x**3,
        (h, 0),
    ),
}

for label, (ell_form, v0, third_row) in collisions.items():
    W = z * (ell_form + w * z)
    V = (
        v0
        + z * (t[0] * x**2 + t[1] * x * y + t[2] * y**2)
        + z**2 * (t[3] * x + t[4] * y)
    )
    L = sp.Matrix(
        (
            (l[0], l[1], l[2]),
            (l[3], l[4], l[5]),
            (third_row[0], third_row[1], l[8]),
        )
    )
    H2 = sp.Matrix((A, B, W))
    H3 = sp.Matrix((sp.Rational(4, 3) * z * W + s * q, V, z**3))
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
    print(label)
    for degree in (6, 5, 4):
        selected = [
            (monomial, sp.factor(coefficient))
            for monomial, coefficient in determinant.terms()
            if sum(monomial) == degree and coefficient != 0
        ]
        print("degree", degree, "equations", len(selected))
        if degree == 6:
            for monomial, coefficient in selected:
                if monomial[2] <= 2:
                    print(monomial, coefficient)

    e6 = [
        sp.expand(coefficient)
        for monomial, coefficient in determinant.terms()
        if sum(monomial) == 6 and coefficient != 0
    ]
    e6_unknowns = t + b[:3]
    matrix, rhs = sp.linear_eq_to_matrix(e6, e6_unknowns)
    print(
        "E6 linear",
        matrix.shape,
        "rank",
        matrix.rank(),
        "augmented",
        matrix.row_join(rhs).rank(),
    )
    solution = sp.solve(e6, e6_unknowns, dict=True, simplify=False)
    print("E6 solutions", len(solution))
    if solution:
        for variable in e6_unknowns:
            if variable in solution[0]:
                print(variable, "=", sp.factor(solution[0][variable]))
