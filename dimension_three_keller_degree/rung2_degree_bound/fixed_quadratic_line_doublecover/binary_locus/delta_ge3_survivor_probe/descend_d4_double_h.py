#!/usr/bin/env python3
"""Exact descent for promising doubled-root delta=4 representatives.

The fixed top data are

    h=(p+q)^2, R=(p+q)^3,
    U=-p(p+q)r, V=q(p+q)r, T=0.

The E6 and E5 equations are solved as one affine-linear system in the first
two quadratic components and the linear part.  The remaining E4--E1 ideal
and det(L) on that affine space are then exposed for exact elimination.
"""

from __future__ import annotations

import argparse
import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, wt = sp.symbols("p q r wt")
tau = sp.symbols("tau")
sigma = sp.symbols("sigma")
coords = (p, q, r)
mon2 = (p**2, p * q, p * r, q**2, q * r, r**2)
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
ell = sp.symbols("l0:9")
lower = a + b + ell
A = sum(value * monomial for value, monomial in zip(a, mon2))
B = sum(value * monomial for value, monomial in zip(b, mon2))
L = sp.Matrix(3, 3, ell)

CASES = {
    "power_zero": {
        "h": (p + q) ** 2,
        "R": (p + q) ** 3,
        "U": 0,
        "V": 0,
        "T": 0,
    },
    "power_tangent": {
        "h": (p + q) ** 2,
        "R": (p + q) ** 3,
        "U": -p * (p + q) * r,
        "V": q * (p + q) * r,
        "T": 0,
    },
    "power_intersection_family": {
        "h": (p + q) ** 2,
        "R": (p + q) ** 3,
        "U": -tau * p * (p + q) * r,
        "V": tau * q * (p + q) * r,
        "T": 0,
    },
    "power_conic_plus": {
        "h": (p + q) ** 2,
        "R": (p + q) ** 3,
        "U": r * p * ((8 - 2 * sp.sqrt(2)) * p + 4 * q) / 3,
        "V": r * p * q * (-4 + 2 * sp.sqrt(2)) / 3,
        "T": r * (p + q),
    },
    "power_conic_minus": {
        "h": (p + q) ** 2,
        "R": (p + q) ** 3,
        "U": r * p * ((8 + 2 * sp.sqrt(2)) * p + 4 * q) / 3,
        "V": r * p * q * (-4 - 2 * sp.sqrt(2)) / 3,
        "T": r * (p + q),
    },
    "mixed_tangent": {
        "h": (p + q) ** 2,
        "R": (p + q) * (2 * p**2 + p * q + 2 * q**2),
        "U": -sp.Rational(2, 3) * p * (p + q) * r,
        "V": sp.Rational(2, 3) * q * (p + q) * r,
        "T": (-p + q) * r,
    },
    "mixed_tangent_family": {
        "h": (p + q) ** 2,
        "R": (p + q) * (2 * p**2 + p * q + 2 * q**2),
        "U": -sp.Rational(2, 3) * tau * p * (p + q) * r,
        "V": sp.Rational(2, 3) * tau * q * (p + q) * r,
        "T": tau * (-p + q) * r,
    },
    "mixed_zero": {
        "h": (p + q) ** 2,
        "R": (p + q) * (2 * p**2 + p * q + 2 * q**2),
        "U": 0,
        "V": 0,
        "T": 0,
    },
}


def homogeneous_coefficients(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q, r)
    return [
        pp.coeff_monomial(p**i * q**j * r ** (degree - i - j))
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    ]


def primitive_unique(polynomials):
    result = []
    for polynomial in polynomials:
        value = sp.factor(polynomial)
        if value == 0:
            continue
        if not value.free_symbols:
            value = sp.S.One
            if value not in result:
                result.append(value)
            continue
        pp = sp.Poly(value)
        _, primitive = pp.primitive()
        value = sp.factor(primitive.as_expr())
        if sp.Poly(value).LC() < 0:
            value = -value
        if value not in result:
            result.append(value)
    return tuple(result)


def build(case_name):
    case = CASES[case_name]
    h, R, U, V, T = (case[key] for key in ("h", "R", "U", "V", "T"))
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
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
    assert all(determinant.coeff_monomial(wt**degree) == 0 for degree in (9, 8, 7))
    high_equations = []
    for degree in (6, 5):
        high_equations.extend(homogeneous_coefficients(determinant.coeff_monomial(wt**degree), degree))
    matrix, rhs = sp.linear_eq_to_matrix(high_equations, lower)
    expected_rank = {
        "power_zero": 7,
        "power_tangent": 10,
        "power_intersection_family": 10,
        "power_conic_plus": 9,
        "power_conic_minus": 9,
        "mixed_tangent": 9,
        "mixed_tangent_family": 9,
        "mixed_zero": 7,
    }[case_name]
    matrix_rank = matrix.rank()
    augmented_rank = matrix.row_join(rhs).rank()
    assert matrix_rank == augmented_rank == expected_rank, (
        case_name,
        matrix_rank,
        augmented_rank,
        expected_rank,
    )
    solution = tuple(next(iter(sp.linsolve((matrix, rhs), lower))))
    substitution = dict(zip(lower, solution))
    assert all(sp.expand(equation.subs(substitution)) == 0 for equation in high_equations)
    free = tuple(
        variable
        for variable in lower
        if any(variable in expression.free_symbols for expression in solution)
    )
    lower_equations_by_weight = {}
    for degree in (4, 3, 2, 1):
        lower_equations_by_weight[degree] = primitive_unique(
            value.subs(substitution)
            for value in homogeneous_coefficients(determinant.coeff_monomial(wt**degree), degree)
        )
    all_lower = primitive_unique(
        polynomial
        for degree in (4, 3, 2, 1)
        for polynomial in lower_equations_by_weight[degree]
    )
    determinant_linear = sp.factor(L.det().subs(substitution))
    return {
        "determinant": determinant,
        "matrix": matrix,
        "rhs": rhs,
        "solution": solution,
        "substitution": substitution,
        "free": free,
        "lower_by_weight": lower_equations_by_weight,
        "lower": all_lower,
        "detL": determinant_linear,
        "case": case_name,
    }


def report(data):
    print(f"case={data['case']} high rank={data['matrix'].rank()} free={data['free']}")
    for variable, expression in zip(lower, data["solution"]):
        print(f"  {variable} = {sp.factor(expression)}")
    print(f"detL={data['detL']}")
    for degree in (4, 3, 2, 1):
        print(f"E{degree} ({len(data['lower_by_weight'][degree])}):")
        for equation in data["lower_by_weight"][degree]:
            print(f"  {sp.factor(equation)}")


def groebner_report(data):
    free = data["free"]
    print(f"computing Groebner basis in {len(free)} variables / {len(data['lower'])} equations")
    basis = sp.groebner(data["lower"], *free, order="grevlex")
    print(f"Groebner basis length={len(basis.polys)}")
    for polynomial in basis.polys:
        print(sp.factor(polynomial.as_expr()))
    remainder = sp.factor(basis.reduce(data["detL"])[1])
    print(f"detL remainder={remainder}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(CASES), default="power_tangent")
    parser.add_argument("--groebner", action="store_true")
    args = parser.parse_args()
    data = build(args.case)
    report(data)
    if args.groebner:
        groebner_report(data)


if __name__ == "__main__":
    main()
