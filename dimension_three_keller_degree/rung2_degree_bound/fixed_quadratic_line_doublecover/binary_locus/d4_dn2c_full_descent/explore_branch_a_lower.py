#!/usr/bin/env python3
"""Continue the surviving D4-DN-2C intersection branch A below E4."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import explore_intersection as inter  # noqa: E402

base = inter.base


def solve_selected(equations, variables, rows, columns):
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    free = tuple(
        index for index in range(len(variables)) if index not in columns
    )
    values = matrix.extract(rows, columns).inv() * (
        rhs.extract(rows, (0,))
        - matrix.extract(rows, free)
        * sp.Matrix([variables[index] for index in free])
    )
    substitution = {
        variables[column]: sp.cancel(values[index])
        for index, column in enumerate(columns)
    }
    residuals = tuple(sp.factor(item.subs(substitution)) for item in equations)
    return matrix, substitution, residuals


def build_branch_a():
    data = inter.build()
    substitution_s = {
        base.vc[0]: base.vc[1] - base.vc[2] + base.vc[3]
    }
    substitution_d = {
        base.uc[1]: (
            2 * base.uc[2]
            - 3 * base.uc[3]
            + base.vc[1]
            - 2 * base.vc[2]
            + 3 * base.vc[3]
        )
    }
    substitution_a = {
        base.tc[1]: (
            base.tc[2]
            + sp.Rational(3, 4) * base.uc[2]
            - sp.Rational(9, 8) * base.uc[3]
            - sp.Rational(3, 2) * base.vc[2]
            + sp.Rational(9, 4) * base.vc[3]
        )
    }
    substitution_c = {
        base.ell[8]: base.k
        * (
            -8 * base.tc[2]
            + 6 * base.uc[2]
            - 9 * base.uc[3]
            - 12 * base.vc[1]
            + 12 * base.vc[2]
            - 18 * base.vc[3]
        )
        / 24
    }
    before_e4 = (
        data["contact"],
        data["solve6"],
        data["solve1"],
        data["solve0"],
        substitution_a,
        substitution_s,
        substitution_d,
        substitution_c,
    )

    def descend(expression, extra=()):
        value = expression
        for substitution in before_e4 + extra:
            value = value.subs(substitution)
        return sp.cancel(value)

    e4 = sp.Poly(
        base.full_determinant.coeff_monomial(base.weight**4),
        base.p,
        base.q,
        base.r,
    )
    equations41 = tuple(
        descend(coefficient)
        for monomial, coefficient in e4.terms()
        if monomial[2] == 1 and descend(coefficient) != 0
    )
    variables41 = (base.bc[1], base.bc[3], base.ell[5])
    matrix41, solve41, residual41 = solve_selected(
        equations41, variables41, (0,), (0,)
    )
    assert sp.factor(matrix41[0, 0] + sp.Rational(2, 3) * base.k**2) == 0
    assert all(item == 0 for item in residual41)

    equations40 = tuple(
        descend(coefficient, (solve41,))
        for monomial, coefficient in e4.terms()
        if monomial[2] == 0
        and descend(coefficient, (solve41,)) != 0
    )
    variables40 = (base.ell[0], base.ell[1], base.ell[3], base.ell[4])
    matrix40, solve40, residual40 = solve_selected(
        equations40, variables40, (0, 1), (0, 2)
    )
    assert sp.factor(
        matrix40.extract((0, 1), (0, 2)).det() - 4 * base.k**2
    ) == 0
    assert all(item == 0 for item in residual40)
    return {
        "before_e4": before_e4,
        "solve41": solve41,
        "solve40": solve40,
    }


def main():
    data = build_branch_a()
    substitutions = (
        data["before_e4"]
        + (data["solve41"], data["solve40"])
    )
    for degree in (3, 2, 1):
        coefficient = base.full_determinant.coeff_monomial(
            base.weight**degree
        )
        polynomial = sp.Poly(coefficient, base.p, base.q, base.r)
        print("E", degree, sep="")
        for monomial, value in polynomial.terms():
            for substitution in substitutions:
                value = value.subs(substitution)
            value = sp.cancel(value)
            if value != 0:
                text = str(value)
                print(
                    monomial,
                    "LEN",
                    len(text),
                    "OPS",
                    sp.count_ops(value),
                    "VARS",
                    sorted(map(str, value.free_symbols)),
                    text if len(text) < 2000 else "",
                )
        if degree == 3:
            break
    determinant = base.linear.det()
    for substitution in substitutions:
        determinant = determinant.subs(substitution)
    print("DETL", sp.factor(sp.cancel(determinant)))


if __name__ == "__main__":
    main()
