#!/usr/bin/env python3
"""Deterministic exact search for an invertible E4 survivor on the overlap."""

from __future__ import annotations

import itertools
import random
import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, weight = sp.symbols("p q r weight")
coords = (p, q, r)
h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(h * (p - 2 * q))

u0, u1, u2, v0 = sp.symbols("u0 u1 u2 v0")
a0, a1, b0 = sp.symbols("a0 a1 b0")
l0, l1, l3, l4 = sp.symbols("l0 l1 l3 l4")


def coefficient_vector(expression: sp.Expr, degree: int) -> sp.Matrix:
    polynomial = sp.Poly(sp.expand(expression), p, q, r)
    return sp.Matrix(
        [
            polynomial.coeff_monomial(p**i * q ** (degree - k - i) * r**k)
            for k in range(degree + 1)
            for i in range(degree - k, -1, -1)
        ]
    )


def solve_affine(
    equations: sp.Matrix,
    variables: tuple[sp.Symbol, ...],
) -> tuple[dict[sp.Symbol, sp.Expr], int, int]:
    matrix = equations.jacobian(variables)
    constant = equations.subs({variable: 0 for variable in variables})
    assert equations == matrix * sp.Matrix(variables) + constant
    rank = matrix.rank()
    augmented_rank = matrix.row_join(-constant).rank()
    if rank != augmented_rank:
        return {}, rank, augmented_rank
    solution_tuple = tuple(next(iter(sp.linsolve((matrix, -constant), variables))))
    return dict(zip(variables, solution_tuple)), rank, augmented_rank


def trial(values: tuple[int, ...]):
    (
        t1,
        t2,
        u3,
        v1,
        v2,
        v3,
        a2,
        b1,
        b2,
        l2,
        l6,
        l7,
    ) = values
    t0 = t1 - t2
    zed = 6 * v1 - 9 * v2 + 9 * v3
    br0 = sp.Rational(1, 3) * zed
    ell33 = (
        t1
        - 2 * t2
        - sp.Rational(3, 2) * v1
        + 3 * v2
        - sp.Rational(9, 2) * v3
    )
    ar1 = (
        sp.Rational(4, 3) * (t1 - t2)
        - sp.Rational(3, 2) * u3
        + 2 * v2
        - 3 * v3
    )
    ar0 = ar1 + 2 * br0 - 3 * v1 + 4 * v2 - 3 * v3
    br1 = v1 - v2
    vquadratic = v1**2 - 3 * v1 * v2 + 3 * v1 * v3 + 2 * v2**2 - 3 * v2 * v3
    l5 = b1 - 2 * b2 - sp.Rational(1, 2) * vquadratic

    U0 = u0 * p**3 + u1 * p**2 * q + u2 * p * q**2 + u3 * q**3
    V0 = v0 * p**3 + v1 * p**2 * q + v2 * p * q**2 + v3 * q**3
    U = U0 + 2 * r * p * (p + q)
    V = V0 - 2 * r * q * (p + q)
    T = t0 * p**2 + t1 * p * q + t2 * q**2 + 3 * r * (p + q)
    A = (
        a0 * p**2
        + a1 * p * q
        + a2 * q**2
        + r * (ar0 * p + ar1 * q)
        + r**2
    )
    B = (
        b0 * p**2
        + b1 * p * q
        + b2 * q**2
        + r * (br0 * p + br1 * q)
        + r**2
    )
    linear = sp.Matrix(((l0, l1, l2), (l3, l4, l5), (l6, l7, ell33)))
    H2 = sp.Matrix((A, B, T))
    H3 = sp.Matrix((U, V, R))
    H4 = sp.Matrix((P, Q, 0))
    determinant = sp.Poly(
        sp.expand(
            (
                linear
                + weight * H2.jacobian(coords)
                + weight**2 * H3.jacobian(coords)
                + weight**3 * H4.jacobian(coords)
            ).det()
        ),
        weight,
    )

    eq6 = coefficient_vector(determinant.coeff_monomial(weight**6), 6)
    sol6, rank6, aug6 = solve_affine(eq6, (u0, u1, u2, v0))
    if rank6 != 4 or aug6 != 4:
        return None
    eq5 = coefficient_vector(
        determinant.coeff_monomial(weight**5).subs(sol6),
        5,
    )
    sol5, rank5, aug5 = solve_affine(eq5, (a0, a1, b0))
    if rank5 != 3 or aug5 != 3:
        return None
    eq4 = coefficient_vector(
        determinant.coeff_monomial(weight**4).subs(sol6).subs(sol5),
        4,
    )
    sol4, rank4, aug4 = solve_affine(eq4, (l0, l1, l3, l4))
    if rank4 != aug4:
        return None

    linear_solved = sp.simplify(linear.subs(sol4))
    det_linear = sp.factor(linear_solved.det())
    eq3_raw = coefficient_vector(
        determinant.coeff_monomial(weight**3)
        .subs(sol6)
        .subs(sol5)
        .subs(sol4),
        3,
    )
    free_top = tuple(
        sorted(det_linear.free_symbols & {l0, l1, l3, l4}, key=str)
    )
    choices = (0, 1, -1, 2, -2)
    for assignment_values in itertools.product(choices, repeat=len(free_top)):
        assignment = dict(zip(free_top, assignment_values))
        determinant_value = sp.factor(det_linear.subs(assignment))
        if determinant_value == 0:
            continue
        sol4_done = {
            variable: value.subs(assignment) for variable, value in sol4.items()
        }
        sol4_done.update(assignment)
        eq3 = coefficient_vector(
            determinant.coeff_monomial(weight**3)
            .subs(sol6)
            .subs(sol5)
            .subs(sol4_done),
            3,
        )
        nonzero3 = [
            (index, sp.factor(value))
            for index, value in enumerate(eq3)
            if value != 0
        ]
        e3_vector = tuple(sp.factor(value) for value in eq3)
        return {
            "values": values,
            "sol6": sol6,
            "sol5": sol5,
            "rank4": rank4,
            "sol4": sol4_done,
            "sol4_raw": sol4,
            "linear": linear_solved.subs(assignment),
            "det_linear": determinant_value,
            "det_linear_raw": det_linear,
            "nonzero3": nonzero3,
            "e3_vector": e3_vector,
            "e3_vector_raw": tuple(sp.factor(value) for value in eq3_raw),
        }
    return None


rng = random.Random(20260726)
candidate_values = [-1, 0, 1]
found_results = []
for attempt in range(120):
    values = tuple(rng.choice(candidate_values) for _ in range(12))
    result = trial(values)
    if result is not None:
        found_results.append(result)
        if len(found_results) == 1:
            print("ATTEMPT", attempt)
            for key, value in result.items():
                print(key, "=", value)
            print("D4_DN2C_PUNCTURED_REPRESENTATIVE_FOUND")
        if len(found_results) >= 12:
            break
if not found_results:
    print("NO_REPRESENTATIVE_FOUND")
    raise SystemExit(1)

relation_rows = sp.Matrix(
    [
        tuple(result["e3_vector"][:4]) + (-result["det_linear"],)
        for result in found_results
    ]
)
print("E3_RELATION_SAMPLE_COUNT", len(found_results))
print("E3_RELATION_MATRIX_RANK", relation_rows.rank())
print("E3_RELATION_NULLSPACE", relation_rows.nullspace())
print("D4_DN2C_E3_RELATION_SAMPLING_PASS")
