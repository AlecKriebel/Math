#!/usr/bin/env python3
"""Seeded exact search for an invertible E6/E5 survivor.

For each representative and chosen nonbinary E7 tangent, small binary
summands of U,V,T are sampled.  With those fixed, E6 and E5 are a single
affine-linear system in all twelve coefficients of the first two quadratic
components and all nine entries of the linear part.  The search checks
whether the full affine solution space has a nonzero determinant, rather
than testing one arbitrarily selected solution.
"""

from __future__ import annotations

import argparse
import random
import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, wt = sp.symbols("p q r wt")
coords = (p, q, r)
mon2 = (p**2, p * q, p * r, q**2, q * r, r**2)
mon2_binary = (p**2, p * q, q**2)
mon3_binary = (p**3, p**2 * q, p * q**2, q**3)
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
ell = sp.symbols("l0:9")
lower = a + b + ell
L = sp.Matrix(3, 3, ell)
A = sum(value * monomial for value, monomial in zip(a, mon2))
B = sum(value * monomial for value, monomial in zip(b, mon2))


def homogeneous_coefficients(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q, r)
    return [
        pp.coeff_monomial(p**i * q**j * r ** (degree - i - j))
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    ]


def affine_solution(equations):
    matrix, rhs = sp.linear_eq_to_matrix(equations, lower)
    augmented = matrix.row_join(rhs)
    rank = matrix.rank()
    if rank != augmented.rank():
        return None, rank
    solution = tuple(next(iter(sp.linsolve((matrix, rhs), lower))))
    return solution, rank


def determinant_point(solution):
    substitution = dict(zip(lower, solution))
    affine_l = sp.simplify(L.subs(substitution))
    determinant = sp.factor(affine_l.det())
    if determinant == 0:
        return None
    free = sorted(
        set().union(*(expression.free_symbols for expression in solution)) & set(lower),
        key=str,
    )
    rng_values = (-2, -1, 0, 1, 2)
    # Determinant has degree three, so a nonzero polynomial cannot vanish on
    # the entire five-point grid in each variable.  A deterministic sparse
    # walk is tried before random grid points.
    substitutions = [{symbol: 0 for symbol in free}]
    for symbol in free:
        for value in (-2, -1, 1, 2):
            substitutions.append({candidate: (value if candidate == symbol else 0) for candidate in free})
    trial_rng = random.Random(917_331 + len(free))
    for _ in range(400):
        substitutions.append({symbol: trial_rng.choice(rng_values) for symbol in free})
    for free_values in substitutions:
        concrete = sp.simplify(affine_l.subs(free_values))
        if concrete.det() != 0:
            return {
                "solution": solution,
                "free_values": free_values,
                "L": concrete,
                "detL": sp.factor(concrete.det()),
                "full_substitution": substitution | free_values,
            }
    raise AssertionError("nonzero cubic determinant vanished on five-point grid")


def coefficient_tuple(poly, monomials):
    pp = sp.Poly(poly, p, q, r)
    return tuple(pp.coeff_monomial(monomial) for monomial in monomials)


CASES = {
    "D3_P2_ZERO": (p**2, p**2 * (p + q), 0, 0, 0),
    "D3_P2_Y2": (p**2, p**2 * (p + q), 4 * r * p**2, -6 * r * p * q, r * q),
    "D3_P2_Y1": (p**2, p**2 * (p + q), 0, 2 * r * p * q, r * p),
    "D3_PQ_ZERO": (p * q, p**3, 0, 0, 0),
    "D4_DOUBLE_H_ZERO": ((p + q) ** 2, (p + q) ** 3, 0, 0, 0),
    "D4_DOUBLE_H_Y01": (
        (p + q) ** 2,
        (p + q) ** 3,
        -r * p * (p + q),
        r * q * (p + q),
        0,
    ),
    "D4_DOUBLE_H_CONIC_PLUS": (
        (p + q) ** 2,
        (p + q) ** 3,
        r * p * ((8 - 2 * sp.sqrt(2)) * p + 4 * q) / 3,
        r * p * q * (-4 + 2 * sp.sqrt(2)) / 3,
        r * (p + q),
    ),
    "D4_DOUBLE_MIX_ZERO": (
        (p + q) ** 2,
        (p + q) * (2 * p**2 + p * q + 2 * q**2),
        0,
        0,
        0,
    ),
    "D4_DOUBLE_MIX_TANGENT": (
        (p + q) ** 2,
        (p + q) * (2 * p**2 + p * q + 2 * q**2),
        -sp.Rational(2, 3) * r * p * (p + q),
        sp.Rational(2, 3) * r * q * (p + q),
        r * (-p + q),
    ),
}


def analyze(label, trials, seed):
    h, R, U_nonbinary, V_nonbinary, T_nonbinary = CASES[label]
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    rng = random.Random(seed)
    assignments = [(0,) * 11]
    # Coordinate directions and then a reproducible random portfolio.
    for index in range(11):
        for value in (-1, 1):
            point = [0] * 11
            point[index] = value
            assignments.append(tuple(point))
    while len(assignments) < trials:
        point = tuple(rng.choice((-2, -1, 0, 1, 2)) for _ in range(11))
        assignments.append(point)

    consistent = 0
    invertible = None
    for index, values in enumerate(assignments, 1):
        U0 = sum(value * monomial for value, monomial in zip(values[:4], mon3_binary))
        V0 = sum(value * monomial for value, monomial in zip(values[4:8], mon3_binary))
        T0 = sum(value * monomial for value, monomial in zip(values[8:], mon2_binary))
        U, V, T = U_nonbinary + U0, V_nonbinary + V0, T_nonbinary + T0
        H2, H3, H4 = sp.Matrix([A, B, T]), sp.Matrix([U, V, R]), sp.Matrix([P, Q, 0])
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
        equations = []
        for degree in (6, 5):
            equations.extend(homogeneous_coefficients(determinant.coeff_monomial(wt**degree), degree))
        solution, rank = affine_solution(equations)
        if solution is None:
            continue
        consistent += 1
        point = determinant_point(solution)
        if point is None:
            continue
        full_substitution = point["full_substitution"]
        residuals = {
            degree: tuple(
                value
                for value in homogeneous_coefficients(
                    determinant.coeff_monomial(wt**degree).subs(full_substitution),
                    degree,
                )
                if value != 0
            )
            for degree in (4, 3, 2, 1)
        }
        invertible = {
            "trial": index,
            "binary_coefficients": values,
            "rank": rank,
            "U": U,
            "V": V,
            "T": T,
            "A": sp.expand(A.subs(full_substitution)),
            "B": sp.expand(B.subs(full_substitution)),
            "L": point["L"],
            "detL": point["detL"],
            "residuals": residuals,
        }
        break
    print(
        f"{label}: tested={len(assignments) if invertible is None else invertible['trial']} "
        f"consistent={consistent} invertible_E6_E5={invertible}"
    )
    return invertible


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("labels", nargs="*", choices=tuple(CASES))
    parser.add_argument("--trials", type=int, default=150)
    parser.add_argument("--seed", type=int, default=20260726)
    args = parser.parse_args()
    labels = args.labels or tuple(CASES)
    for offset, label in enumerate(labels):
        analyze(label, args.trials, args.seed + offset)


if __name__ == "__main__":
    main()
