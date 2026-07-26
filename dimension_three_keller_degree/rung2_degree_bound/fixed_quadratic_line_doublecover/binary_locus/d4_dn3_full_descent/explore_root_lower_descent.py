#!/usr/bin/env python3
"""Root-side probe of the D4-DN-3 plus-plane E5 system.

Exploratory only: solve the certified all-lower E6 seven-pivot on the
entire k != 0 plus plane and report any E5 coefficient independent of the
remaining free lower variables.  No generic formula is used on k=0.
"""

from __future__ import annotations

import pathlib
import sys

import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "d4_dn3_full_rebuild"))
import verify_full_e6_elimination as base  # noqa: E402


def solve_chart(matrix, rhs, rows, columns):
    free_columns = tuple(
        index
        for index in range(len(base.lower18))
        if index not in columns
    )
    pivot = matrix.extract(rows, columns)
    free_matrix = matrix.extract(rows, free_columns)
    free_vector = sp.Matrix(
        [base.lower18[index] for index in free_columns]
    )
    values = pivot.inv() * (
        rhs.extract(rows, (0,)) - free_matrix * free_vector
    )
    substitution = {
        base.lower18[column]: sp.cancel(values[index])
        for index, column in enumerate(columns)
    }
    return free_columns, substitution


def pure_coefficients(polynomial, free_columns):
    free_variables = {
        base.lower18[index] for index in free_columns
    }
    pure = []
    support = []
    for exponent, coefficient in polynomial.terms():
        coefficient = sp.cancel(coefficient)
        active_free = tuple(
            variable
            for variable in free_variables
            if variable in coefficient.free_symbols
        )
        support.append((exponent, len(active_free)))
        if not active_free and coefficient != 0:
            pure.append(
                (
                    exponent,
                    sp.factor(coefficient, extension=base.sqrt2),
                )
            )
    return tuple(sorted(map(str, free_variables))), tuple(support), tuple(pure)


def main():
    free_columns, substitution = solve_chart(
        base.full_matrix,
        base.full_rhs,
        base.rows7,
        base.cols7,
    )
    assert all(
        sp.cancel(equation.subs(substitution)) == 0
        for equation in base.full_e6.coeffs()
    )
    e5 = sp.Poly(
        base.full_det.coeff_monomial(base.weight**5).subs(substitution),
        base.p,
        base.q,
        base.r,
    )
    free_variables, support, pure = pure_coefficients(e5, free_columns)
    print("D4_DN3_PLUS_E5_FREE_VARIABLES", free_variables)
    print("D4_DN3_PLUS_E5_SUPPORT_FREE_COUNTS", support)
    print("D4_DN3_PLUS_E5_PURE_COEFFICIENTS", pure)
    p3 = dict(pure)[(3, 0, 2)]
    q3 = dict(pure)[(0, 3, 2)]
    cplus = (-4 + 2 * base.sqrt2) / 3
    assert sp.factor(
        p3
        - base.k
        * (-6 + 3 * base.sqrt2)
        * (base.s + cplus * base.k) ** 2,
        extension=base.sqrt2,
    ) == 0
    assert sp.factor(
        q3
        - base.k
        * (-6 + 3 * base.sqrt2)
        * (base.s - sp.Rational(4, 3) * base.k) ** 2,
        extension=base.sqrt2,
    ) == 0
    assert sp.factor(
        -cplus - sp.Rational(4, 3),
        extension=base.sqrt2,
    ) != 0
    print("D4_DN3_PLUS_INTERIOR_E5_EXCLUDED")

    intersection_matrix = base.full_matrix.subs(base.k, 0)
    intersection_rhs = base.full_rhs.subs(base.k, 0)
    intersection_free, intersection_substitution = solve_chart(
        intersection_matrix,
        intersection_rhs,
        base.rows6,
        base.cols6,
    )
    intersection_e6 = sp.Poly(
        base.full_det.coeff_monomial(base.weight**6).subs(base.k, 0),
        base.p,
        base.q,
        base.r,
    )
    assert all(
        sp.cancel(equation.subs(intersection_substitution)) == 0
        for equation in intersection_e6.coeffs()
    )
    intersection_e5 = sp.Poly(
        base.full_det.coeff_monomial(base.weight**5)
        .subs(base.k, 0)
        .subs(intersection_substitution),
        base.p,
        base.q,
        base.r,
    )
    i_free, i_support, i_pure = pure_coefficients(
        intersection_e5,
        intersection_free,
    )
    print("D4_DN3_INTERSECTION_E5_FREE_VARIABLES", i_free)
    print("D4_DN3_INTERSECTION_E5_SUPPORT_FREE_COUNTS", i_support)
    print("D4_DN3_INTERSECTION_E5_PURE_COEFFICIENTS", i_pure)
    print("D4_DN3_PLUS_E5_ROOT_PROBE_PASS")


if __name__ == "__main__":
    main()
