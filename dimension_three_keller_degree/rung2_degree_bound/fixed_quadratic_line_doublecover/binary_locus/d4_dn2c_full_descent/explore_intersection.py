#!/usr/bin/env python3
"""Exploratory E5/E4 descent on the punctured D4-DN-2C intersection."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import explore_descent as common  # noqa: E402

base = common.base


def build():
    contact = {base.d: 0, base.z: 0} | base.intersection_line
    solve6 = common.solve_chart(
        base.intersection_line, base.rows6, base.cols6
    )
    e5 = sp.Poly(
        base.full_determinant.coeff_monomial(base.weight**5),
        base.p,
        base.q,
        base.r,
    )

    def descend(expression, substitutions=()):
        value = expression.subs(contact).subs(solve6)
        for substitution in substitutions:
            value = value.subs(substitution)
        return sp.cancel(value)

    r1 = tuple(
        descend(coefficient)
        for monomial, coefficient in e5.terms()
        if monomial[2] == 1 and descend(coefficient) != 0
    )
    variables1 = (
        base.bc[4],
        base.tc[0],
        base.tc[1],
        base.tc[2],
        base.uc[1],
        base.uc[2],
        base.uc[3],
        base.vc[1],
        base.vc[2],
        base.vc[3],
    )
    matrix1, rhs1 = sp.linear_eq_to_matrix(r1, variables1)
    rows1 = (0, 1)
    columns1 = (0, 1)
    free1 = tuple(
        index for index in range(len(variables1)) if index not in columns1
    )
    values1 = matrix1.extract(rows1, columns1).inv() * (
        rhs1.extract(rows1, (0,))
        - matrix1.extract(rows1, free1)
        * sp.Matrix([variables1[index] for index in free1])
    )
    solve1 = {
        variables1[column]: sp.cancel(values1[index])
        for index, column in enumerate(columns1)
    }
    assert all(sp.cancel(item.subs(solve1)) == 0 for item in r1)

    r0 = tuple(
        descend(coefficient, (solve1,))
        for monomial, coefficient in e5.terms()
        if monomial[2] == 0
        and descend(coefficient, (solve1,)) != 0
    )
    variables0 = (
        base.ac[0],
        base.ac[1],
        base.ac[3],
        base.bc[0],
        base.bc[1],
        base.bc[3],
        base.ell[2],
        base.ell[5],
        base.ell[6],
        base.ell[7],
    )
    matrix0, rhs0 = sp.linear_eq_to_matrix(r0, variables0)
    rows0 = (0, 1, 2)
    columns0 = (0, 1, 3)
    free0 = tuple(
        index for index in range(len(variables0)) if index not in columns0
    )
    values0 = matrix0.extract(rows0, columns0).inv() * (
        rhs0.extract(rows0, (0,))
        - matrix0.extract(rows0, free0)
        * sp.Matrix([variables0[index] for index in free0])
    )
    solve0 = {
        variables0[column]: sp.cancel(values0[index])
        for index, column in enumerate(columns0)
    }
    residual0 = tuple(sp.factor(item.subs(solve0)) for item in r0)

    factor_a = (
        8 * base.tc[1]
        - 8 * base.tc[2]
        - 6 * base.uc[2]
        + 9 * base.uc[3]
        + 12 * base.vc[2]
        - 18 * base.vc[3]
    )
    factor_b = (
        -6 * base.ell[8]
        + 2 * base.k * base.tc[1]
        - 4 * base.k * base.tc[2]
        - 3 * base.k * base.vc[1]
        + 6 * base.k * base.vc[2]
        - 9 * base.k * base.vc[3]
    )
    quadratic = (
        base.uc[1] ** 2
        - 4 * base.uc[1] * base.uc[2]
        + 6 * base.uc[1] * base.uc[3]
        - 6 * base.uc[1] * base.vc[0]
        + 4 * base.uc[1] * base.vc[1]
        - 2 * base.uc[1] * base.vc[2]
        + 4 * base.uc[2] ** 2
        - 12 * base.uc[2] * base.uc[3]
        + 12 * base.uc[2] * base.vc[0]
        - 8 * base.uc[2] * base.vc[1]
        + 4 * base.uc[2] * base.vc[2]
        + 9 * base.uc[3] ** 2
        - 18 * base.uc[3] * base.vc[0]
        + 12 * base.uc[3] * base.vc[1]
        - 6 * base.uc[3] * base.vc[2]
        + 18 * base.vc[0] ** 2
        - 30 * base.vc[0] * base.vc[1]
        + 24 * base.vc[0] * base.vc[2]
        - 18 * base.vc[0] * base.vc[3]
        + 13 * base.vc[1] ** 2
        - 22 * base.vc[1] * base.vc[2]
        + 18 * base.vc[1] * base.vc[3]
        + 10 * base.vc[2] ** 2
        - 18 * base.vc[2] * base.vc[3]
        + 9 * base.vc[3] ** 2
    )
    ideal = sp.groebner(
        (factor_a * factor_b, quadratic),
        base.ell[8],
        base.tc[1],
        base.tc[2],
        base.uc[1],
        base.uc[2],
        base.uc[3],
        base.vc[0],
        base.vc[1],
        base.vc[2],
        base.vc[3],
        order="grevlex",
        domain=sp.QQ.frac_field(base.k),
    )
    assert all(
        ideal.reduce(sp.together(value).as_numer_denom()[0])[1] == 0
        for value in residual0
    )
    return {
        "contact": contact,
        "solve6": solve6,
        "solve1": solve1,
        "solve0": solve0,
        "factor_a": factor_a,
        "factor_b": factor_b,
        "quadratic": quadratic,
    }


def main():
    data = build()
    e4 = sp.Poly(
        base.full_determinant.coeff_monomial(base.weight**4),
        base.p,
        base.q,
        base.r,
    )
    common_substitutions = (
        data["contact"],
        data["solve6"],
        data["solve1"],
        data["solve0"],
    )
    branch_a = {
        base.tc[1]: (
            base.tc[2]
            + sp.Rational(3, 4) * base.uc[2]
            - sp.Rational(9, 8) * base.uc[3]
            - sp.Rational(3, 2) * base.vc[2]
            + sp.Rational(9, 4) * base.vc[3]
        )
    }
    branch_b = {
        base.ell[8]: (
            2 * base.k * base.tc[1]
            - 4 * base.k * base.tc[2]
            - 3 * base.k * base.vc[1]
            + 6 * base.k * base.vc[2]
            - 9 * base.k * base.vc[3]
        )
        / 6
    }
    for label, branch in (("A", branch_a), ("B", branch_b)):
        print("BRANCH", label)
        for monomial, coefficient in e4.terms():
            if monomial[2] == 0:
                continue
            value = coefficient
            for substitution in common_substitutions + (branch,):
                value = value.subs(substitution)
            value = sp.cancel(value)
            if value != 0:
                text = str(value)
                print(
                    monomial,
                    "LEN",
                    len(text),
                    "VARS",
                    len(value.free_symbols),
                    text if len(text) < 3000 else "",
                )
        determinant = base.linear.det()
        for substitution in common_substitutions + (branch,):
            determinant = determinant.subs(substitution)
        determinant = sp.factor(sp.cancel(determinant))
        print("DETL", label, len(str(determinant)), determinant)


if __name__ == "__main__":
    main()
