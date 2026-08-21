#!/usr/bin/env python3
"""Descend E6/E5 for explicit nonzero E7-tangent survivors.

Binary cubic/quadratic summands are set to zero in this construction probe.
For each displayed tangent, E6 is solved completely.  Its one- or
two-dimensional affine solution is then searched exactly for an E5 solution
whose linear part is invertible.  Any such point is tested against all lower
weighted identities.
"""

from __future__ import annotations

from itertools import product
import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, wt = sp.symbols("p q r wt")
coords = (p, q, r)
ell = sp.symbols("l0:9")
avars = sp.symbols("a0:3")
bvars = sp.symbols("b0:3")
nonbinary_lower = avars + bvars
L = sp.Matrix(3, 3, ell)


def homogeneous_coefficients(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q, r)
    return [
        pp.coeff_monomial(p**i * q**j * r ** (degree - i - j))
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    ]


def solve_linear(equations, variables):
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    augmented = matrix.row_join(rhs)
    if matrix.rank() != augmented.rank():
        return None, matrix, rhs
    solution_set = sp.linsolve((matrix, rhs), variables)
    assert solution_set is not sp.EmptySet
    solution = tuple(next(iter(solution_set)))
    return solution, matrix, rhs


def determinant_witness(affine_matrix, parameters):
    determinant = sp.factor(affine_matrix.det())
    if determinant == 0:
        return None, determinant
    for values in product((-2, -1, 0, 1, 2), repeat=len(parameters)):
        substitution = dict(zip(parameters, values))
        value = sp.factor(determinant.subs(substitution))
        if value != 0:
            return substitution, determinant
    raise AssertionError("nonzero determinant polynomial had no small witness")


def analyze(label, h, R, U, V, T):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    A = avars[0] * p * r + avars[1] * q * r + avars[2] * r**2
    B = bvars[0] * p * r + bvars[1] * q * r + bvars[2] * r**2
    H2 = sp.Matrix([A, B, T])
    H3 = sp.Matrix([U, V, R])
    H4 = sp.Matrix([P, Q, 0])
    determinant = sp.Poly(
        sp.expand(
            (
                L
                + wt * H2.jacobian(coords)
                + wt**2 * H3.jacobian(coords)
                + wt**3 * H4.jacobian(coords)
            ).det()
        ),
        wt,
    )
    for degree in (9, 8, 7):
        assert determinant.coeff_monomial(wt**degree) == 0

    e6_equations = homogeneous_coefficients(determinant.coeff_monomial(wt**6), 6)
    e6_variables = nonbinary_lower + (ell[8],)
    solution6, matrix6, rhs6 = solve_linear(e6_equations, e6_variables)
    assert solution6 is not None
    free6 = tuple(
        symbol
        for symbol in e6_variables
        if any(symbol in expression.free_symbols for expression in solution6)
    )
    substitution6 = dict(zip(e6_variables, solution6))
    assert all(sp.expand(equation.subs(substitution6)) == 0 for equation in e6_equations)

    e5_equations = [
        sp.factor(value.subs(substitution6))
        for value in homogeneous_coefficients(determinant.coeff_monomial(wt**5), 5)
    ]
    remaining_linear = ell[:8]
    print(f"{label}: E6 rank={matrix6.rank()}, free={free6}, solution={solution6}")
    found = None
    tested = 0
    for values in product((-3, -2, -1, 0, 1, 2, 3), repeat=len(free6)):
        free_substitution = dict(zip(free6, values))
        specialized5 = [sp.factor(eq.subs(free_substitution)) for eq in e5_equations]
        solution5, matrix5, rhs5 = solve_linear(specialized5, remaining_linear)
        tested += 1
        if solution5 is None:
            continue
        free5 = tuple(
            symbol
            for symbol in remaining_linear
            if any(symbol in expression.free_symbols for expression in solution5)
        )
        substitution5 = dict(zip(remaining_linear, solution5))
        lmatrix = L.subs(substitution6).subs(free_substitution).subs(substitution5)
        witness_parameters, det_polynomial = determinant_witness(lmatrix, free5)
        if witness_parameters is None:
            continue
        full_substitution = substitution6 | free_substitution | substitution5 | witness_parameters
        concrete_l = sp.simplify(L.subs(full_substitution))
        concrete_h2 = sp.simplify(H2.subs(full_substitution))
        assert concrete_l.det() != 0
        residuals = {}
        for degree in (5, 4, 3, 2, 1):
            polynomial = sp.expand(determinant.coeff_monomial(wt**degree).subs(full_substitution))
            residuals[degree] = tuple(
                value
                for value in homogeneous_coefficients(polynomial, degree)
                if value != 0
            )
        assert residuals[5] == ()
        found = {
            "free6": free_substitution,
            "L": concrete_l,
            "H2": concrete_h2,
            "detL": sp.factor(concrete_l.det()),
            "residuals": residuals,
            "e5_rank": matrix5.rank(),
            "e5_nullity": len(free5),
            "det_polynomial": det_polynomial,
        }
        break
    print(f"  searched {tested} E6 parameter points")
    print(f"  E5 invertible survivor={found}")
    return found


def main():
    cases = (
        (
            "D3_P2_Y2",
            p**2,
            p**2 * (p + q),
            4 * r * p**2,
            -6 * r * p * q,
            r * q,
        ),
        (
            "D3_P2_Y1",
            p**2,
            p**2 * (p + q),
            0,
            2 * r * p * q,
            r * p,
        ),
        (
            "D4_DOUBLE_H_Y01",
            (p + q) ** 2,
            (p + q) ** 3,
            -r * p * (p + q),
            r * q * (p + q),
            0,
        ),
    )
    selected = set(sys.argv[1:])
    for case in cases:
        if not selected or case[0] in selected:
            analyze(*case)


if __name__ == "__main__":
    main()
