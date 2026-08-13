#!/usr/bin/env python3
"""Exact replay of portal-uniform BDM for the unweighted three-path."""

from __future__ import annotations

from collections import defaultdict

import sympy as sp


r = sp.symbols("r", positive=True)
WEIGHTS = (
    (sp.Integer(0), sp.Integer(1), sp.Integer(1)),
    (sp.Integer(1), sp.Integer(0), sp.Integer(0)),
    (sp.Integer(1), sp.Integer(0), sp.Integer(0)),
)


def fixation_vector(rule: str, fitness: sp.Expr) -> tuple[sp.Expr, ...]:
    """Rebuild and solve the six transient labelled states."""

    degree = [sum(row) for row in WEIGHTS]
    states = list(range(1, 7))
    index = {state: row for row, state in enumerate(states)}
    matrix = sp.eye(6)
    rhs = sp.zeros(6, 1)

    for state in states:
        mutant = [(state >> vertex) & 1 for vertex in range(3)]
        transition: dict[int, sp.Expr] = defaultdict(lambda: sp.Integer(0))
        if rule == "Bd":
            total_fitness = 3 + (fitness - 1) * sum(mutant)
            for parent in range(3):
                for target in range(3):
                    if not WEIGHTS[parent][target]:
                        continue
                    probability = (
                        (fitness if mutant[parent] else 1)
                        * WEIGHTS[parent][target]
                        / (total_fitness * degree[parent])
                    )
                    next_state = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transition[next_state] += probability
        elif rule == "dB":
            for target in range(3):
                denominator = sum(
                    WEIGHTS[parent][target]
                    * (fitness if mutant[parent] else 1)
                    for parent in range(3)
                )
                for parent in range(3):
                    if not WEIGHTS[parent][target]:
                        continue
                    probability = (
                        WEIGHTS[parent][target]
                        * (fitness if mutant[parent] else 1)
                        / (3 * denominator)
                    )
                    next_state = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transition[next_state] += probability
        else:
            raise ValueError(rule)

        row = index[state]
        for target, probability in transition.items():
            if target == 7:
                rhs[row] += probability
            elif target:
                matrix[row, index[target]] -= probability

    solution = next(iter(sp.linsolve((matrix, rhs))))
    return tuple(sp.factor(sp.cancel(value)) for value in solution)


def labelled_chain_data() -> tuple[sp.Expr, sp.Expr, tuple[sp.Expr, ...], tuple[sp.Expr, ...]]:
    bd = fixation_vector("Bd", r)
    db = fixation_vector("dB", r)
    bd_reciprocal = fixation_vector("Bd", 1 / r)
    db_reciprocal = fixation_vector("dB", 1 / r)

    # Type complementation: a singleton at reciprocal fitness is the
    # complement of the all-but-singleton state at fitness r.
    for vertex in range(3):
        singleton = 1 << vertex
        complement = 7 ^ singleton
        assert sp.factor(bd_reciprocal[singleton - 1] + bd[complement - 1] - 1) == 0
        assert sp.factor(db_reciprocal[singleton - 1] + db[complement - 1] - 1) == 0

    L = 2 * r**2 + r + 2
    expected_u = (
        (2 * r**3 + 5 * r**2 + 4 * r + 4) / ((2 * r + 1) * L**2),
        2 / L,
        2 / L,
    )
    expected_v = (
        (r + 2) / (3 * (r + 1)),
        1 / (2 * (r + 1)),
        1 / (2 * (r + 1)),
    )
    singleton_masks = (1, 2, 4)
    u = tuple(bd_reciprocal[mask - 1] for mask in singleton_masks)
    v = tuple(db_reciprocal[mask - 1] for mask in singleton_masks)
    assert all(sp.factor(x - y) == 0 for x, y in zip(u, expected_u))
    assert all(sp.factor(x - y) == 0 for x, y in zip(v, expected_v))

    b = sp.factor(sum(bd[mask - 1] for mask in singleton_masks) / 3)
    a = sp.factor(sum(db[mask - 1] for mask in singleton_masks) / (3 * (r - 1)))
    expected_b = r**2 * (4 * r**3 + 8 * r**2 + 7 * r + 6) / ((r + 2) * L**2)
    expected_a = (5 * r + 1) / (9 * (r - 1) * (r + 1))
    assert sp.factor(b - expected_b) == 0
    assert sp.factor(a - expected_a) == 0
    return a, b, u, v


def sign_on_isolating_interval(expression: sp.Expr, sign: int) -> None:
    """Prove a rational expression has the requested strict sign at R_hyb."""

    lo = sp.Rational(1502856912, 10**9)
    hi = sp.Rational(1502856913, 10**9)
    numerator, denominator = map(sp.factor, sp.cancel(expression).as_numer_denom())
    assert sp.Poly(numerator, r).count_roots(lo, hi) == 0
    assert sp.Poly(denominator, r).count_roots(lo, hi) == 0
    assert sp.sign(numerator.subs(r, lo)) * sp.sign(denominator.subs(r, lo)) == sign


def portal_quadratic() -> None:
    a, b, u, v = labelled_chain_data()
    e = (sp.Rational(1, 2), sp.Integer(1), sp.Integer(1))
    C = r * (r - 1) ** 2

    polynomial = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    lo = sp.Rational(1502856912, 10**9)
    hi = sp.Rational(1502856913, 10**9)
    assert sp.Poly(polynomial, r).count_roots(lo, hi) == 1

    sign_on_isolating_interval(1 - a, 1)
    sign_on_isolating_interval(1 - b, 1)

    # The two leaf coordinates coincide, leaving three portal-monomial
    # coefficient types.  Negative discriminant and positive endpoints make
    # each quadratic positive for every real gate odds z.
    cases = ((0, 0), (0, 1), (1, 1))
    expected_discriminant_numerators = (
        256*r**14 + 320*r**13 - 892*r**12 - 4524*r**11 - 2231*r**10
        + 8140*r**9 + 13288*r**8 - 5492*r**7 - 18284*r**6 + 3000*r**5
        + 14804*r**4 + 1712*r**3 - 3920*r**2 - 192*r + 576,
        256*r**14 + 320*r**13 - 892*r**12 - 4524*r**11 - 2343*r**10
        + 7688*r**9 + 13086*r**8 - 4282*r**7 - 16803*r**6 + 2390*r**5
        + 13017*r**4 + 1552*r**3 - 3144*r**2 - 160*r + 400,
        64*r**12 + 16*r**11 - 255*r**10 - 880*r**9 + 470*r**8
        + 1872*r**7 + 971*r**6 - 3148*r**5 - 1194*r**4 + 3364*r**3
        + 241*r**2 - 1116*r + 324,
    )

    for (i, j), expected_numerator in zip(cases, expected_discriminant_numerators):
        E = (e[i] + e[j]) / 2
        S = (u[i] * e[j] * v[j] + u[j] * e[i] * v[i]) / 2
        A0 = sp.factor(C * (1 - a) * E)
        A1 = sp.factor(C * (1 - a - b) * E + S)
        A2 = sp.factor((1 - b) * S)
        sign_on_isolating_interval(A0, 1)
        sign_on_isolating_interval(A2, 1)
        discriminant = sp.factor(sp.cancel(A1**2 - 4 * A0 * A2))
        numerator, denominator = discriminant.as_numer_denom()
        assert sp.factor(numerator - expected_numerator) == 0
        assert sp.sign(denominator.subs(r, lo)) == 1
        sign_on_isolating_interval(discriminant, -1)

    # Independent symbolic reconstruction of the complete portal polynomial.
    x0, x1, x2, z = sp.symbols("x0 x1 x2 z", nonnegative=True)
    x = (x0, x1, x2)
    A = sum(x) * sum(x[i] * e[i] for i in range(3))
    Q = sum(x[i] * u[i] for i in range(3)) * sum(
        x[i] * e[i] * v[i] for i in range(3)
    )
    gap = sp.expand(C * ((1 + z) * (1 - a) - b * z) * A + z * (1 + z * (1 - b)) * Q)
    for i in range(3):
        for j in range(i, 3):
            coefficient = sp.expand(gap).coeff(x[i], 1).coeff(x[j], 1)
            if i == j:
                # coeff(x_i,1) misses x_i^2; extract it directly.
                coefficient = sp.Poly(gap, x0, x1, x2).coeff_monomial(x[i] ** 2)
            orbit_i = 0 if i == 0 else 1
            orbit_j = 0 if j == 0 else 1
            E = (e[orbit_i] + e[orbit_j]) / 2
            S = (
                u[orbit_i] * e[orbit_j] * v[orbit_j]
                + u[orbit_j] * e[orbit_i] * v[orbit_i]
            ) / 2
            expected = C * (1 - a) * E + (
                C * (1 - a - b) * E + S
            ) * z + (1 - b) * S * z**2
            multiplicity = 1 if i == j else 2
            assert sp.factor(coefficient - multiplicity * expected) == 0


def main() -> None:
    portal_quadratic()
    print("PASS: independent Bd/dB labelled P3 chains and complementation")
    print("PASS: exact centre/leaf OR-dual data")
    print("PASS: all portal coefficients have positive endpoints and negative discriminant")
    print("PROVED: unweighted P3 satisfies strict BDM at R_hyb for every portal law")


if __name__ == "__main__":
    main()

