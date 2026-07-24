#!/usr/bin/env python3
"""Discovery-only SOS search for the five-point C5 core inequality.

This script searches for a degree-four certificate of

    3/2 - sum_{i<j} h(g_ij) >= 0,
    h(t) = t^2 (t^2 - 1/4),

on the Gram spectrahedron with the five cycle entries in [-1,-1/2] and
the five chord entries in [-1/2,1/2].  It deliberately uses redundant
principal-minor inequalities.  Solver output is numerical evidence only;
an exact rational reconstruction and a separate checker would be required
before any resulting certificate could enter a proof.

The optional dependencies were installed only in a temporary discovery
directory during the initial run:

    PYTHONPATH=/tmp/c5deps /usr/local/bin/python \
        experiments/c5_core_sos_search.py
"""

from __future__ import annotations

import itertools
import os
from collections import defaultdict

import cvxpy as cp
import sympy as sp


NVAR = 10
ZERO = (0,) * NVAR


def exponent_vectors(max_degree: int):
    ans = []
    for degree in range(max_degree + 1):
        for support in itertools.combinations_with_replacement(
            range(NVAR), degree
        ):
            exponent = [0] * NVAR
            for index in support:
                exponent[index] += 1
            ans.append(tuple(exponent))
    return ans


def add_exp(left, right):
    return tuple(a + b for a, b in zip(left, right))


def sympy_poly(expression, variables):
    polynomial = sp.Poly(sp.expand(expression), *variables)
    return {
        tuple(monomial): float(coefficient)
        for monomial, coefficient in polynomial.terms()
    }


def add_product(accumulator, left, right, scale=1.0):
    for left_exp, left_coefficient in left.items():
        for right_exp, right_coefficient in right.items():
            accumulator[add_exp(left_exp, right_exp)] += (
                scale * left_coefficient * right_coefficient
            )


def add_sos_times(accumulator, factor, monomials, matrix):
    """Add factor * m^T matrix m to a polynomial accumulator."""
    for i, left_exp in enumerate(monomials):
        for j in range(i, len(monomials)):
            right_exp = monomials[j]
            scale = 1.0 if i == j else 2.0
            base_exp = add_exp(left_exp, right_exp)
            for factor_exp, factor_coefficient in factor.items():
                accumulator[add_exp(base_exp, factor_exp)] += (
                    scale * factor_coefficient * matrix[i, j]
                )


def main():
    variables = sp.symbols("x0:10")
    gram = sp.eye(5)
    pairs = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 0),
        (0, 2),
        (1, 3),
        (2, 4),
        (3, 0),
        (4, 1),
    ]
    for variable, (i, j) in zip(variables, pairs):
        gram[i, j] = variable
        gram[j, i] = variable

    target = sp.Rational(3, 2) - sum(
        variable**4 - sp.Rational(1, 4) * variable**2
        for variable in variables
    )
    target_poly = sympy_poly(target, variables)

    # The twenty affine box factors, all nonnegative on the domain.
    box_expressions = []
    for variable in variables[:5]:
        box_expressions.extend(
            [variable + 1, -sp.Rational(1, 2) - variable]
        )
    for variable in variables[5:]:
        box_expressions.extend(
            [variable + sp.Rational(1, 2),
             sp.Rational(1, 2) - variable]
        )
    box_polys = [
        sympy_poly(expression, variables) for expression in box_expressions
    ]

    minors = {}
    for size in (2, 3, 4):
        minors[size] = [
            sympy_poly(
                gram.extract(indices, indices).det(), variables
            )
            for indices in itertools.combinations(range(5), size)
        ]

    degree_two = exponent_vectors(2)
    degree_one = exponent_vectors(1)
    coefficient_sum = defaultdict(lambda: 0.0)
    psd_variables = []

    free_sos = cp.Variable(
        (len(degree_two), len(degree_two)), PSD=True, name="free_sos"
    )
    psd_variables.append(free_sos)
    add_sos_times(coefficient_sum, {ZERO: 1.0}, degree_two, free_sos)

    for index, box_poly in enumerate(box_polys):
        multiplier = cp.Variable(
            (len(degree_one), len(degree_one)),
            PSD=True,
            name=f"box_sos_{index}",
        )
        psd_variables.append(multiplier)
        add_sos_times(coefficient_sum, box_poly, degree_one, multiplier)

    # A 2x2 principal minor is quadratic, so it may carry an affine SOS.
    for index, minor in enumerate(minors[2]):
        multiplier = cp.Variable(
            (len(degree_one), len(degree_one)),
            PSD=True,
            name=f"minor2_sos_{index}",
        )
        psd_variables.append(multiplier)
        add_sos_times(coefficient_sum, minor, degree_one, multiplier)

    # Constant nonnegative multipliers for cubic and quartic minors.
    minor3_coefficients = cp.Variable(len(minors[3]), nonneg=True)
    minor4_coefficients = cp.Variable(len(minors[4]), nonneg=True)
    for coefficient, minor in zip(minor3_coefficients, minors[3]):
        add_product(coefficient_sum, minor, {ZERO: coefficient})
    for coefficient, minor in zip(minor4_coefficients, minors[4]):
        add_product(coefficient_sum, minor, {ZERO: coefficient})

    all_exponents = set(target_poly) | set(coefficient_sum)
    constraints = [
        coefficient_sum[exponent] == target_poly.get(exponent, 0.0)
        for exponent in all_exponents
    ]
    regularizer = sum(cp.trace(matrix) for matrix in psd_variables)
    regularizer += cp.sum(minor3_coefficients) + cp.sum(minor4_coefficients)
    problem = cp.Problem(cp.Minimize(regularizer), constraints)
    solver = os.environ.get("C5_SOS_SOLVER", "SCS").upper()
    if solver == "SCS":
        value = problem.solve(
            solver="SCS",
            verbose=True,
            eps=1e-6,
            max_iters=100_000,
        )
    else:
        value = problem.solve(
            solver="CLARABEL",
            verbose=True,
            tol_gap_abs=1e-9,
            tol_feas=1e-9,
            tol_gap_rel=1e-9,
            max_iter=500,
        )
    print("status", problem.status)
    print("regularizer", value)
    if problem.status in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE):
        residual = max(
            abs(constraint.violation())
            for constraint in constraints
        )
        minimum_eigenvalue = min(
            float(min(__import__("numpy").linalg.eigvalsh(matrix.value)))
            for matrix in psd_variables
        )
        print("maximum coefficient residual", residual)
        print("minimum SOS eigenvalue", minimum_eigenvalue)
        print("minor3 coefficients", minor3_coefficients.value)
        print("minor4 coefficients", minor4_coefficients.value)


if __name__ == "__main__":
    main()
