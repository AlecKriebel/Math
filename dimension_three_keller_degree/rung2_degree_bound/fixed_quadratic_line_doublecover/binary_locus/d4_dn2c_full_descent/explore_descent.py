#!/usr/bin/env python3
"""Exploratory lower descent for the frozen D4-DN-2C atlas."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

REBUILD = Path(__file__).resolve().parent.parent / "d4_dn2c_full_rebuild"
sys.path.insert(0, str(REBUILD))
import verify_full_e6_elimination as base  # noqa: E402


def solve_chart(substitution, rows, columns):
    equations = tuple(
        sp.expand(item.subs(substitution)) for item in base.e6_equations
    )
    matrix, rhs = sp.linear_eq_to_matrix(equations, base.lower18)
    free_columns = tuple(
        index for index in range(len(base.lower18)) if index not in columns
    )
    selected = matrix.extract(rows, columns)
    free_matrix = matrix.extract(rows, free_columns)
    free_vector = sp.Matrix([base.lower18[index] for index in free_columns])
    values = selected.inv() * (
        rhs.extract(rows, (0,)) - free_matrix * free_vector
    )
    solved = {
        base.lower18[column]: sp.cancel(values[index])
        for index, column in enumerate(columns)
    }
    assert all(sp.cancel(item.subs(solved)) == 0 for item in equations)
    return solved


def report_degree(label, polynomial, remaining_symbols):
    print(label, "MONOMIALS", polynomial.monoms())
    for monomial, coefficient in polynomial.terms():
        coefficient = sp.cancel(coefficient)
        if not (coefficient.free_symbols & remaining_symbols):
            numerator, denominator = sp.together(coefficient).as_numer_denom()
            print(
                label,
                "PURE",
                monomial,
                "NUM",
                sp.factor(numerator, extension=base.eta),
                "DEN",
                sp.factor(denominator, extension=base.eta),
            )


def main():
    all_lower = (
        set(base.uc)
        | set(base.vc)
        | set(base.tc)
        | set(base.ac)
        | set(base.bc)
        | set(base.ell)
    )
    for label, contact in (
        ("PLUS", base.plane_plus),
        ("MINUS", base.plane_minus),
    ):
        solved = solve_chart(contact, base.rows7, base.cols7)
        remaining = all_lower - set(solved)
        e5 = sp.Poly(
            sp.cancel(
                base.full_determinant.coeff_monomial(base.weight**5)
                .subs({base.d: 0, base.z: 0})
                .subs(contact)
                .subs(solved)
            ),
            base.p,
            base.q,
            base.r,
        )
        print(label, "FREE", len(remaining), sorted(map(str, remaining)))
        report_degree(label + "_E5", e5, remaining)


if __name__ == "__main__":
    main()
