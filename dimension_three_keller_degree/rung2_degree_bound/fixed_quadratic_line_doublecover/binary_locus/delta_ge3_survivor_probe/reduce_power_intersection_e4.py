#!/usr/bin/env python3
"""Reduce the complete E4 system on the nonzero power-intersection line.

This is an elimination aid for the complete arbitrary-binary descent.  It
uses only constant-coefficient linear solves at each stage and prints every
remaining compatibility polynomial rather than silently selecting a generic
pivot.
"""

from __future__ import annotations

import os

import sympy as sp

import complete_lower_component as base
from descend_power_intersection_complete import independent_rows, nonzero_by_r, solve_linear


def unique_associates(values):
    result = []
    for value in values:
        value = sp.factor(value)
        if value == 0:
            continue
        polynomial = sp.Poly(value)
        _, primitive = polynomial.primitive()
        value = sp.factor(primitive.as_expr())
        if sp.Poly(value).LC() < 0:
            value = -value
        if not any(
            sp.cancel(value / existing).free_symbols == set()
            for existing in result
        ):
            result.append(value)
    return tuple(result)


def linear_stage(equations, variables):
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    rank = matrix.rank()
    compatibility = unique_associates(
        (left.T * rhs)[0] for left in matrix.T.nullspace()
    )
    rows = independent_rows(matrix)
    selected = tuple(equations[index] for index in rows)
    _, solution, substitution = solve_linear(selected, variables)
    residuals = unique_associates(
        equation.subs(substitution) for equation in equations
    )
    assert all(
        any(sp.cancel(residual / item).free_symbols == set() for item in compatibility)
        for residual in residuals
    ) if residuals else not compatibility
    return {
        "matrix": matrix,
        "rank": rank,
        "compatibility": compatibility,
        "rows": rows,
        "solution": solution,
        "substitution": substitution,
    }


def main():
    data = base.build("power_intersection")

    stage51 = linear_stage(nonzero_by_r(data["e5"], 1), data["free6"])
    assert stage51["rank"] == 3 and not stage51["compatibility"]
    e50 = tuple(
        sp.factor(value.subs(stage51["substitution"]))
        for value in nonzero_by_r(data["e5"], 0)
    )
    variables50 = (
        base.a[0],
        base.a[1],
        base.a[3],
        base.b[0],
        base.b[1],
        base.b[3],
        base.ell[2],
        base.ell[5],
        base.ell[6],
        base.ell[7],
    )
    stage50 = linear_stage(e50, variables50)
    assert stage50["rank"] == 3 and len(stage50["compatibility"]) == 1

    substitutions = (
        data["substitution6"],
        stage51["substitution"],
        stage50["substitution"],
    )

    def descend(expression):
        value = expression
        for substitution in substitutions:
            value = value.subs(substitution)
        return sp.factor(value)

    e4 = {
        exponent: descend(value)
        for exponent, value in base.exponent_coefficients(
            data["determinant"].coeff_monomial(base.wt**4), 4
        ).items()
    }
    if os.environ.get("D4_DN3_MUTATE_S_FORCING") == "1":
        e4[(2, 0, 2)] += 1
    compatibility5 = stage50["compatibility"][0]
    s_condition = base.v[0] - base.v[1] + base.v[2] - base.v[3]
    d_condition = (
        base.u[1]
        - 2 * base.u[2]
        + 3 * base.u[3]
        - base.v[1]
        + 2 * base.v[2]
        - 3 * base.v[3]
    )
    # These are the equations which force S=0 on the punctured contact
    # line.  Keep the identities literal and check that no other
    # coefficient of r-degree at least two survives.  Without these
    # assertions the later S-substitution would not be fail-closed.
    s_forcing = {
        (2, 0, 2): -sp.Rational(9, 4) * base.k**3 * s_condition,
        (1, 1, 2): -sp.Rational(9, 2) * base.k**3 * s_condition,
        (0, 2, 2): -sp.Rational(9, 4) * base.k**3 * s_condition,
    }
    assert all(
        sp.factor(e4[exponent] - expected) == 0
        for exponent, expected in s_forcing.items()
    )
    assert all(
        value == 0 or exponent in s_forcing
        for exponent, value in e4.items()
        if exponent[2] >= 2
    )
    sd_substitution = {
        base.v[0]: base.v[1] - base.v[2] + base.v[3],
        base.u[1]: (
            2 * base.u[2]
            - 3 * base.u[3]
            + base.v[1]
            - 2 * base.v[2]
            + 3 * base.v[3]
        ),
    }
    compatibility_after_s = sp.factor(
        compatibility5.subs({base.v[0]: base.v[1] - base.v[2] + base.v[3]})
    )
    assert sp.cancel(compatibility_after_s / d_condition**2).free_symbols <= {base.k}, (
        compatibility_after_s,
        d_condition,
        sp.factor(compatibility_after_s / d_condition**2),
    )
    e4_sd = {
        exponent: sp.factor(value.subs(sd_substitution))
        for exponent, value in e4.items()
    }
    assert all(
        value == 0
        for exponent, value in e4_sd.items()
        if exponent[2] >= 2
    )

    equations41 = tuple(
        value for exponent, value in e4_sd.items() if exponent[2] == 1 and value != 0
    )
    variables41 = (
        base.b[1],
        base.b[3],
        base.ell[5],
        base.ell[6],
        base.ell[7],
    )
    stage41 = linear_stage(equations41, variables41)
    assert stage41["rank"] == 2 and not stage41["compatibility"]

    e4_after41 = {
        exponent: sp.factor(value.subs(stage41["substitution"]))
        for exponent, value in e4_sd.items()
    }
    equations40 = tuple(
        value for exponent, value in e4_after41.items() if exponent[2] == 0 and value != 0
    )
    variables40 = (base.ell[0], base.ell[1], base.ell[3], base.ell[4])
    stage40 = linear_stage(equations40, variables40)
    assert stage40["rank"] == 2 and not stage40["compatibility"]

    e4_final = {
        exponent: sp.factor(value.subs(stage41["substitution"]).subs(stage40["substitution"]))
        for exponent, value in e4_sd.items()
    }
    assert all(value == 0 for value in e4_final.values())

    det_l = descend(base.L.det())
    det_reduced = sp.factor(
        det_l.subs(sd_substitution)
        .subs(stage41["substitution"])
        .subs(stage40["substitution"])
    )

    print(f"E5 r1 rank={stage51['rank']}")
    print(f"E5 r0 rank={stage50['rank']} compatibility={stage50['compatibility']}")
    print(f"E4 gives S={s_condition}; with E5 this gives D={d_condition}")
    print(
        f"E4 r1 rank={stage41['rank']} rows={stage41['rows']} "
        f"compatibility={stage41['compatibility']}"
    )
    for variable, expression in zip(variables41, stage41["solution"]):
        print(f"  {variable} = {sp.factor(expression)}")
    print(
        f"E4 r0 rank={stage40['rank']} rows={stage40['rows']} "
        f"compatibility={stage40['compatibility']}"
    )
    for variable, expression in zip(variables40, stage40["solution"]):
        print(f"  {variable} = {sp.factor(expression)}")
    print(f"detL reduced={det_reduced}")
    assert det_reduced == 0
    print("POWER_INTERSECTION_COMPLETE_PASS_DETL_ZERO")


if __name__ == "__main__":
    main()
