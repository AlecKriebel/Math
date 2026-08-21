#!/usr/bin/env python3
"""Complete high-to-low solve for selected E6-contact components.

Unlike the quick construction probes, this script retains arbitrary binary
parts U0,V0,T0,A0,B0 and all nine entries of L.  It first solves E6 as a
linear system in every nonbinary coefficient together with the binary top
coefficients, then exposes E5 by powers of r.  Claims remain tied to the
explicit (h,R) and contact component selected on the command line.
"""

from __future__ import annotations

import argparse
import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, wt = sp.symbols("p q r wt")
coords = (p, q, r)
k = sp.symbols("k")
s = sp.symbols("s")

mon3_binary = (p**3, p**2 * q, p * q**2, q**3)
mon2 = (p**2, p * q, p * r, q**2, q * r, r**2)
mon2_binary = (p**2, p * q, q**2)

u = sp.symbols("u0:4")
v = sp.symbols("v0:4")
t0 = sp.symbols("t0:3")
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
ell = sp.symbols("l0:9")

U0 = sum(value * monomial for value, monomial in zip(u, mon3_binary))
V0 = sum(value * monomial for value, monomial in zip(v, mon3_binary))
T0 = sum(value * monomial for value, monomial in zip(t0, mon2_binary))
A = sum(value * monomial for value, monomial in zip(a, mon2))
B = sum(value * monomial for value, monomial in zip(b, mon2))
L = sp.Matrix(3, 3, ell)

CASES = {
    "mixed_zero": {
        "h": (p + q) ** 2,
        "R": (p + q) * (2 * p**2 + p * q + 2 * q**2),
        "U1": 0,
        "V1": 0,
        "T1": 0,
    },
    "mixed_line": {
        "h": (p + q) ** 2,
        "R": (p + q) * (2 * p**2 + p * q + 2 * q**2),
        "U1": -sp.Rational(2, 3) * k * p * (p + q),
        "V1": sp.Rational(2, 3) * k * q * (p + q),
        "T1": k * (-p + q),
    },
    "power_intersection": {
        "h": (p + q) ** 2,
        "R": (p + q) ** 3,
        "U1": -k * p * (p + q),
        "V1": k * q * (p + q),
        "T1": 0,
    },
    "power_conic_plus": {
        "h": (p + q) ** 2,
        "R": (p + q) ** 3,
        "U1": (
            -s * p * (p + q)
            + k * p * ((8 - 2 * sp.sqrt(2)) * p + 4 * q) / 3
        ),
        "V1": s * q * (p + q) + k * p * q * (-4 + 2 * sp.sqrt(2)) / 3,
        "T1": k * (p + q),
    },
    "power_conic_minus": {
        "h": (p + q) ** 2,
        "R": (p + q) ** 3,
        "U1": (
            -s * p * (p + q)
            + k * p * ((8 + 2 * sp.sqrt(2)) * p + 4 * q) / 3
        ),
        "V1": s * q * (p + q) + k * p * q * (-4 - 2 * sp.sqrt(2)) / 3,
        "T1": k * (p + q),
    },
    "power_zero": {
        "h": (p + q) ** 2,
        "R": (p + q) ** 3,
        "U1": 0,
        "V1": 0,
        "T1": 0,
    },
}


def exponent_coefficients(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q, r)
    return {
        (i, j, degree - i - j): pp.coeff_monomial(p**i * q**j * r ** (degree - i - j))
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    }


def solve_linear(equations, variables):
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    augmented = matrix.row_join(rhs)
    rank, augmented_rank = matrix.rank(), augmented.rank()
    if rank != augmented_rank:
        return None, matrix, rhs, rank, augmented_rank
    solution = tuple(next(iter(sp.linsolve((matrix, rhs), variables))))
    substitution = dict(zip(variables, solution))
    assert all(sp.cancel(eq.subs(substitution)) == 0 for eq in equations)
    return solution, matrix, rhs, rank, augmented_rank


def build(case_name):
    case = CASES[case_name]
    h, R = case["h"], case["R"]
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    U = U0 + r * case["U1"]
    V = V0 + r * case["V1"]
    T = T0 + r * case["T1"]
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

    e6_dict = exponent_coefficients(determinant.coeff_monomial(wt**6), 6)
    e6_equations = tuple(e6_dict.values())
    e6_variables = (a[2], a[4], a[5], b[2], b[4], b[5], ell[8]) + u + v + t0
    result = solve_linear(e6_equations, e6_variables)
    solution6, matrix6, _, rank6, augmented_rank6 = result
    if solution6 is None:
        raise AssertionError(("E6 inconsistent", rank6, augmented_rank6))
    substitution6 = dict(zip(e6_variables, solution6))
    free6 = tuple(
        variable
        for variable in e6_variables
        if any(variable in expression.free_symbols for expression in solution6)
    )

    e5_dict = {
        exponent: sp.factor(value.subs(substitution6))
        for exponent, value in exponent_coefficients(determinant.coeff_monomial(wt**5), 5).items()
    }
    return {
        "case": case_name,
        "determinant": determinant,
        "e6_variables": e6_variables,
        "solution6": solution6,
        "substitution6": substitution6,
        "free6": free6,
        "rank6": rank6,
        "e5": e5_dict,
    }


def report(data):
    print(f"case={data['case']} E6 rank={data['rank6']} free={data['free6']}")
    for variable, expression in zip(data["e6_variables"], data["solution6"]):
        print(f"  {variable} = {sp.factor(expression)}")
    by_r = {}
    for exponent, value in data["e5"].items():
        if value != 0:
            by_r.setdefault(exponent[2], []).append((exponent, value))
    for r_degree in sorted(by_r, reverse=True):
        print(f"E5 r-degree {r_degree}:")
        for exponent, value in by_r[r_degree]:
            print(f"  {exponent}: {sp.factor(value)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(CASES), default="mixed_line")
    args = parser.parse_args()
    report(build(args.case))


if __name__ == "__main__":
    main()
