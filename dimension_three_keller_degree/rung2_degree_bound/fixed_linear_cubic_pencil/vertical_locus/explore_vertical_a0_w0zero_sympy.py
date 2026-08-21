#!/usr/bin/env python3
"""Discovery-only E6/E5 exploration of the a=0, W0=0 vertical branch."""

from __future__ import annotations

import sympy as sp


x, y, z = sp.symbols("x y z")
u, vlin, w, alpha = sp.symbols("u vlin w alpha")
r20, r11, r02, r10, r01 = sp.symbols("r20 r11 r02 r10 r01")
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
t = sp.symbols("t0:9")
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
V = sum(coefficient * monomial for coefficient, monomial in zip(t, cubics))
L = sp.Matrix(3, 3, l)
charts = {
    "squarefree": (
        x * y * (x - y)
        + z * (r20 * x**2 + r11 * x * y + r02 * y**2)
        + z**2 * (r10 * x + r01 * y)
    ),
    "double": (
        x**2 * y
        + z * (r20 * x**2 + r11 * x * y + r02 * y**2)
        + z**2 * (r10 * x + r01 * y)
    ),
    "triple_C": x**3 + y**2 * z + alpha * x * z**2,
    "triple_B": x**3 + x * y * z,
    "triple_E": x**3 + y * z**2,
}


def equations(poly: sp.Poly, degree: int):
    return [
        sp.expand(coefficient)
        for monomial, coefficient in poly.terms()
        if sum(monomial) == degree and coefficient != 0
    ]


for chart, q in charts.items():
    W = z * (u * x + vlin * y + w * z)
    H2 = sp.Matrix((A, B, W))
    H3 = sp.Matrix((sp.Rational(4, 3) * z * W, V, z**3))
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
    print(chart, "max degree", max(map(sum, determinant.monoms())))
    for degree in (6,):
        eqs = equations(determinant, degree)
        unknowns = a[:3] + (l[6], l[7])
        matrix, rhs = sp.linear_eq_to_matrix(eqs, unknowns)
        print(
            chart,
            f"E{degree}",
            matrix.shape,
            "ranks",
            matrix.rank(),
            matrix.row_join(rhs).rank(),
        )
        if degree == 6:
            solution = sp.solve(eqs, unknowns, dict=True, simplify=False)
            print(chart, "E6 solutions", len(solution))
            if solution:
                for variable in unknowns:
                    if variable in solution[0]:
                        print(variable, "=", sp.factor(solution[0][variable]))
                for equation in eqs:
                    residual = sp.factor(equation.subs(solution[0]))
                    if residual != 0:
                        print("E6 residual", residual)
                reduced = sp.Poly(
                    sp.expand(determinant.as_expr().subs(solution[0])),
                    x,
                    y,
                    z,
                )
                e5 = equations(reduced, 5)
                e5_unknowns = t + b + l[:6]
                try:
                    matrix5, rhs5 = sp.linear_eq_to_matrix(e5, e5_unknowns)
                except Exception as error:
                    print(chart, "E5 nonlinear", error)
                else:
                    print(
                        chart,
                        "E5",
                        matrix5.shape,
                        "ranks",
                        matrix5.rank(),
                        matrix5.row_join(rhs5).rank(),
                    )
                    e5_monomials = [
                        monomial
                        for monomial, coefficient in reduced.terms()
                        if sum(monomial) == 5 and coefficient != 0
                    ]
                    for index, relation in enumerate(matrix5.T.nullspace()):
                        obstruction = sp.factor((relation.T * rhs5)[0])
                        if obstruction != 0:
                            support = [
                                (
                                    position,
                                    e5_monomials[position],
                                    sp.factor(value),
                                )
                                for position, value in enumerate(relation)
                                if value != 0
                            ]
                            print(
                                chart,
                                "E5 compatibility",
                                index,
                                support,
                                obstruction,
                            )
                    zero_ell = {u: 0, vlin: 0}
                    e5_zero = [
                        sp.factor(equation.subs(zero_ell))
                        for equation in e5
                        if equation.subs(zero_ell) != 0
                    ]
                    matrix_zero, rhs_zero = sp.linear_eq_to_matrix(
                        e5_zero,
                        e5_unknowns,
                    )
                    print(
                        chart,
                        "E5 ell0",
                        matrix_zero.shape,
                        "rank",
                        matrix_zero.rank(),
                        "pivots",
                        matrix_zero.rref()[1],
                    )
                    solution_zero = sp.solve(
                        e5_zero,
                        e5_unknowns,
                        dict=True,
                        simplify=False,
                    )
                    print(chart, "E5 ell0 solutions", len(solution_zero))
                    if solution_zero:
                        for variable in e5_unknowns:
                            if variable in solution_zero[0]:
                                print(
                                    variable,
                                    "=",
                                    sp.factor(solution_zero[0][variable]),
                                )
                        combined_zero = {
                            **solution[0],
                            **zero_ell,
                            **solution_zero[0],
                        }
                        e4_zero = [
                            (monomial, sp.factor(coefficient.subs(combined_zero)))
                            for monomial, coefficient in determinant.terms()
                            if sum(monomial) == 4
                            and coefficient.subs(combined_zero) != 0
                        ]
                        print(chart, "E4 ell0 equations", len(e4_zero))
                        for monomial, equation in e4_zero:
                            print(chart, "E4", monomial, equation)
                    if chart == "triple_E":
                        exceptional = {
                            vlin: 0,
                            a[3]: sp.Rational(8, 9) * u * w,
                            a[4]: 0,
                        }
                        e5_exceptional = [
                            sp.factor(equation.subs(exceptional))
                            for equation in e5
                            if equation.subs(exceptional) != 0
                        ]
                        matrix_exceptional, rhs_exceptional = (
                            sp.linear_eq_to_matrix(
                                e5_exceptional,
                                e5_unknowns,
                            )
                        )
                        print(
                            chart,
                            "E5 exceptional",
                            matrix_exceptional.shape,
                            "rank",
                            matrix_exceptional.rank(),
                        )
                        solve_exceptional = sp.solve(
                            e5_exceptional,
                            e5_unknowns,
                            dict=True,
                            simplify=False,
                        )
                        print(
                            chart,
                            "E5 exceptional solutions",
                            len(solve_exceptional),
                        )
                        if solve_exceptional:
                            for variable in e5_unknowns:
                                if variable in solve_exceptional[0]:
                                    print(
                                        "exceptional",
                                        variable,
                                        "=",
                                        sp.factor(
                                            solve_exceptional[0][variable]
                                        ),
                                    )
                            e4_exceptional = [
                                (
                                    monomial,
                                    sp.factor(
                                        coefficient
                                        .subs(solution[0])
                                        .subs(exceptional)
                                        .subs(solve_exceptional[0])
                                    ),
                                )
                                for monomial, coefficient
                                in determinant.terms()
                                if sum(monomial) == 4
                                and coefficient
                                .subs(solution[0])
                                .subs(exceptional)
                                .subs(solve_exceptional[0]) != 0
                            ]
                            for monomial, equation in e4_exceptional:
                                print(
                                    chart,
                                    "E4 exceptional",
                                    monomial,
                                    equation,
                                )
