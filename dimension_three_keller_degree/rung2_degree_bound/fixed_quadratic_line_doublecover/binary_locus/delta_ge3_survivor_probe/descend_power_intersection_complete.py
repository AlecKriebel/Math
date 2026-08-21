#!/usr/bin/env python3
"""Complete E6/E5 descent on the nonzero power-intersection contact line.

This retains arbitrary binary U0,V0,T0,A0,B0 and all entries of L.  The
contact scale k is treated over Q(k), so every division by k is explicit;
the k=0 boundary is handled by the fresh zero-contact calculation in the
companion verifier.
"""

from __future__ import annotations

import sys

import sympy as sp

import complete_lower_component as base

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)


def solve_linear(equations, variables):
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    assert matrix.rank() == matrix.row_join(rhs).rank()
    solution = tuple(next(iter(sp.linsolve((matrix, rhs), variables))))
    substitution = dict(zip(variables, solution))
    assert all(sp.cancel(equation.subs(substitution)) == 0 for equation in equations)
    return matrix, solution, substitution


def nonzero_by_r(coefficient_dict, r_degree):
    return tuple(
        value
        for exponent, value in coefficient_dict.items()
        if exponent[2] == r_degree and value != 0
    )


def independent_rows(matrix):
    chosen = []
    rank = 0
    for index in range(matrix.rows):
        candidate = chosen + [index]
        new_rank = matrix.extract(candidate, range(matrix.cols)).rank()
        if new_rank > rank:
            chosen.append(index)
            rank = new_rank
        if rank == matrix.rank():
            break
    return tuple(chosen)


def main():
    data = base.build("power_intersection")
    assert data["rank6"] == 6

    e5_r1 = nonzero_by_r(data["e5"], 1)
    variables_r1 = data["free6"]
    matrix51, solution51, substitution51 = solve_linear(e5_r1, variables_r1)
    assert matrix51.rank() == 3, matrix51.rank()
    free51 = tuple(
        variable
        for variable in variables_r1
        if any(variable in expression.free_symbols for expression in solution51)
    )

    e5_r0 = tuple(sp.factor(value.subs(substitution51)) for value in nonzero_by_r(data["e5"], 0))
    variables_r0 = (
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
    matrix50, rhs50 = sp.linear_eq_to_matrix(e5_r0, variables_r0)
    assert matrix50.rank() == 3
    compatibility_values = tuple(
        sp.factor((left.T * rhs50)[0])
        for left in matrix50.T.nullspace()
        if sp.factor((left.T * rhs50)[0]) != 0
    )
    compatibility = sp.factor(compatibility_values[0])
    assert all(sp.cancel(value / compatibility).free_symbols == set() for value in compatibility_values)
    rows50 = independent_rows(matrix50)
    selected50 = tuple(e5_r0[index] for index in rows50)
    _, solution50, substitution50 = solve_linear(selected50, variables_r0)
    assert all(
        sp.cancel(sp.factor(equation.subs(substitution50)) / compatibility).free_symbols == set()
        for equation in e5_r0
        if sp.factor(equation.subs(substitution50)) != 0
    )

    substitutions = (data["substitution6"], substitution51, substitution50)

    def descend(expression):
        value = expression
        for substitution_step in substitutions:
            value = value.subs(substitution_step)
        return sp.factor(value)

    determinant = data["determinant"]
    for degree in (6,):
        coefficient_dict = base.exponent_coefficients(
            determinant.coeff_monomial(base.wt**degree), degree
        )
        assert all(sp.cancel(descend(value)) == 0 for value in coefficient_dict.values())
    e5_after = base.exponent_coefficients(determinant.coeff_monomial(base.wt**5), 5)
    assert all(
        sp.cancel(descend(value) / compatibility).free_symbols == set()
        for value in e5_after.values()
        if descend(value) != 0
    )

    e4 = {
        exponent: descend(value)
        for exponent, value in base.exponent_coefficients(
            determinant.coeff_monomial(base.wt**4), 4
        ).items()
    }
    det_l = descend(base.L.det())

    s_condition = base.v[0] - base.v[1] + base.v[2] - base.v[3]
    d_condition = (
        base.u[1]
        - 2 * base.u[2]
        + 3 * base.u[3]
        - base.v[1]
        + 2 * base.v[2]
        - 3 * base.v[3]
    )
    boundary_substitution = {
        base.v[0]: base.v[1] - base.v[2] + base.v[3],
        base.u[1]: (
            2 * base.u[2]
            - 3 * base.u[3]
            + base.v[1]
            - 2 * base.v[2]
            + 3 * base.v[3]
        ),
    }
    assert sp.factor(compatibility.subs({base.v[0]: base.v[1] - base.v[2] + base.v[3]})) == (
        sp.Rational(3, 4) * base.k * d_condition**2
    )
    e4_reduced = {
        exponent: sp.factor(value.subs(boundary_substitution))
        for exponent, value in e4.items()
    }
    det_l_reduced = sp.factor(det_l.subs(boundary_substitution))

    print(f"E6 rank={data['rank6']}")
    print(f"E5 r1 rank={matrix51.rank()} free={free51}")
    for variable, expression in zip(variables_r1, solution51):
        print(f"  {variable} = {sp.factor(expression)}")
    print(f"E5 r0 rank={matrix50.rank()} compatibility={compatibility}")
    for variable, expression in zip(variables_r0, solution50):
        print(f"  {variable} = {sp.factor(expression)}")
    print(f"detL={det_l}")
    print(f"E4 forces S={s_condition}; E5 compatibility then forces D={d_condition}")
    print(f"detL after S=D=0: {det_l_reduced}")
    print("E4 after S=D=0:")
    for exponent, value in e4_reduced.items():
        if value != 0:
            print(f"  {exponent}: {value}")
    print("E4:")
    for exponent, value in e4.items():
        if value != 0:
            print(f"  {exponent}: {value}")


if __name__ == "__main__":
    main()
