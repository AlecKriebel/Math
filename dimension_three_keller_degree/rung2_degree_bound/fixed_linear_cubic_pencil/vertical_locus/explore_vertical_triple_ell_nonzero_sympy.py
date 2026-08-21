#!/usr/bin/env python3
"""Discovery-only E6/E5 ranks for triple-root charts with gamma=0, ell!=0."""

from __future__ import annotations

import sympy as sp


x, y, z = sp.symbols("x y z")
w, alpha = sp.symbols("w alpha")
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
v = sp.symbols("v0:9")
l = sp.symbols("l0:9")
quadratics = (x**2, x * y, y**2, x * z, y * z, z**2)
cubics = (
    x**3,
    x**2 * y,
    x * y**2,
    y**3,
    x**2 * z,
    x * y * z,
    y**2 * z,
    x * z**2,
    y * z**2,
)
A = sum(coefficient * monomial for coefficient, monomial in zip(a, quadratics))
B = sum(coefficient * monomial for coefficient, monomial in zip(b, quadratics))
V = sum(coefficient * monomial for coefficient, monomial in zip(v, cubics))
L = sp.Matrix(3, 3, l)
charts = {
    "C": x**3 + y**2 * z + alpha * x * z**2,
    "B": x**3 + x * y * z,
    "E": x**3 + y * z**2,
}


def equations(poly: sp.Poly, degree: int):
    return [
        sp.expand(coefficient)
        for monomial, coefficient in poly.terms()
        if sum(monomial) == degree and coefficient != 0
    ]


for chart, q in charts.items():
    for ell_label, ell_form in (("x", x), ("y", y)):
        W = z * (ell_form + w * z)
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
        e6 = equations(determinant, 6)
        e6_monomials = [
            monomial
            for monomial, coefficient in determinant.terms()
            if sum(monomial) == 6 and coefficient != 0
        ]
        unknowns = v + (l[6], l[7])
        matrix, rhs = sp.linear_eq_to_matrix(e6, unknowns)
        print(
            chart,
            ell_label,
            "E6",
            matrix.shape,
            "ranks",
            matrix.rank(),
            matrix.row_join(rhs).rank(),
        )
        unknown_set = set(unknowns)
        for monomial, coefficient in determinant.terms():
            if (
                sum(monomial) == 6
                and coefficient != 0
                and not (coefficient.free_symbols & unknown_set)
            ):
                print("independent", monomial, sp.factor(coefficient))
        for index, relation in enumerate(matrix.T.nullspace()):
            obstruction = sp.factor((relation.T * rhs)[0])
            if obstruction != 0:
                support = [
                    (position, e6_monomials[position], sp.factor(value))
                    for position, value in enumerate(relation)
                    if value != 0
                ]
                print("compatibility", index, "support", support, "rhs", obstruction)
        solution = sp.linsolve((matrix, rhs), unknowns)
        print("solution", solution)
