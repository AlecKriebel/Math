#!/usr/bin/env python3
"""Exact certificate for the minimal portal product on every triangle.

The script derives the two forward three-vertex chains through their exact
singleton/doubleton Schur recurrences.  It then uses type complementation for
the reciprocal singleton atoms and proves the portal matrix entrywise
positive at the isolated hybrid root.  All sign tests use rational tensor
Bernstein coefficients; no floating-point sign is used.
"""

from __future__ import annotations

from math import comb

import sympy as sp


r, p, q = sp.symbols("r p q", positive=True)
S = sp.symbols("S0:3")

# After sorting and scaling the three triangle edges, every positive triangle
# has this form with 0 < p,q <= 1.
WEIGHTS = ((0, p * q, q), (p * q, 0, 1), (q, 1, 0))
DEGREES = (q * (p + 1), p * q + 1, q + 1)

HYBRID_EXPR = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
COEFFICIENT_RING = sp.QQ[p, q]
HYBRID = sp.Poly(HYBRID_EXPR, r, domain=COEFFICIENT_RING)

# A much narrower interval than the original 10^-9 enclosure is useful
# after reducing high-degree numerators modulo the sextic.
ROOT_LO = sp.Rational(150285691279056962670, 10**20)
ROOT_HI = ROOT_LO + sp.Rational(1, 10**20)
SMALL_EDGE = sp.Rational(1, 2000)


def schur_chain(
    rule: str, fitness: sp.Expr
) -> tuple[tuple[sp.Expr, ...], dict[tuple[int, int], sp.Expr]]:
    """Solve the exact three singleton equations after eliminating pairs."""

    pair: dict[tuple[int, int], sp.Expr] = {}
    for k in range(3):
        i, j = [vertex for vertex in range(3) if vertex != k]
        if rule == "Bd":
            incoming = (
                WEIGHTS[i][k] / DEGREES[i]
                + WEIGHTS[j][k] / DEGREES[j]
            )
            pair[i, j] = (
                fitness * incoming
                + WEIGHTS[k][i] / DEGREES[k] * S[j]
                + WEIGHTS[k][j] / DEGREES[k] * S[i]
            ) / (fitness * incoming + 1)
        elif rule == "dB":
            h_ki = WEIGHTS[k][i] / (
                WEIGHTS[k][i] + fitness * WEIGHTS[j][i]
            )
            h_kj = WEIGHTS[k][j] / (
                WEIGHTS[k][j] + fitness * WEIGHTS[i][j]
            )
            pair[i, j] = (
                1 + h_ki * S[j] + h_kj * S[i]
            ) / (1 + h_ki + h_kj)
        else:
            raise ValueError(rule)

    equations = []
    for i in range(3):
        others = [vertex for vertex in range(3) if vertex != i]
        if rule == "Bd":
            numerator = fitness * sum(
                WEIGHTS[i][j] / DEGREES[i] * pair[tuple(sorted((i, j)))]
                for j in others
            )
            denominator = fitness + sum(
                WEIGHTS[j][i] / DEGREES[j] for j in others
            )
        else:
            h = {}
            for j in others:
                k = next(vertex for vertex in range(3) if vertex not in (i, j))
                h[j] = fitness * WEIGHTS[i][j] / (
                    fitness * WEIGHTS[i][j] + WEIGHTS[k][j]
                )
            numerator = sum(
                h[j] * pair[tuple(sorted((i, j)))] for j in others
            )
            denominator = 1 + sum(h.values())
        equations.append(
            sp.Poly(
                sp.together(S[i] - numerator / denominator).as_numer_denom()[0],
                *S,
            )
        )

    matrix = sp.Matrix(
        [[equation.coeff_monomial(S[j]) for j in range(3)] for equation in equations]
    )
    rhs = sp.Matrix([-equation.coeff_monomial(1) for equation in equations])
    determinant = matrix.det()
    singleton = []
    for i in range(3):
        replaced = matrix.copy()
        replaced[:, i] = rhs
        singleton.append(sp.cancel(replaced.det() / determinant))

    substitution = dict(zip(S, singleton))
    solved_pair = {
        indices: sp.cancel(value.subs(substitution, simultaneous=True))
        for indices, value in pair.items()
    }
    return tuple(singleton), solved_pair


def positive_denominator(expression: sp.Expr) -> None:
    """Check the displayed rational denominator coefficientwise."""

    denominator = sp.Poly(expression.as_numer_denom()[1], r, p, q)
    assert denominator.terms()
    assert all(coefficient > 0 for _, coefficient in denominator.terms())


def reduce_at_hybrid(expression: sp.Expr) -> sp.Poly:
    return sp.rem(sp.Poly(expression, r, domain=COEFFICIENT_RING), HYBRID)


def modular_product(*factors: sp.Expr) -> sp.Poly:
    answer = sp.Poly(1, r, domain=COEFFICIENT_RING)
    for factor in factors:
        answer = sp.rem(answer * reduce_at_hybrid(factor), HYBRID)
    return answer


def affine_power(
    coefficients: dict[tuple[int, int, int], sp.Expr],
    axis: int,
    degree: int,
    lower: sp.Rational,
    upper: sp.Rational,
) -> dict[tuple[int, int, int], sp.Expr]:
    """Change one power coordinate from x to lower+(upper-lower)y."""

    other_axes = [candidate for candidate in range(3) if candidate != axis]
    groups: dict[tuple[int, int], dict[int, sp.Expr]] = {}
    for monomial, coefficient in coefficients.items():
        key = tuple(monomial[candidate] for candidate in other_axes)
        groups.setdefault(key, {})[monomial[axis]] = coefficient

    answer: dict[tuple[int, int, int], sp.Expr] = {}
    scale = upper - lower
    for key, powers in groups.items():
        for k in range(degree + 1):
            value = sum(
                powers.get(j, 0)
                * comb(j, k)
                * lower ** (j - k)
                * scale**k
                for j in range(k, degree + 1)
            )
            monomial = [0, 0, 0]
            monomial[axis] = k
            for candidate, exponent in zip(other_axes, key):
                monomial[candidate] = exponent
            if value:
                answer[tuple(monomial)] = value
    return answer


def power_to_bernstein(
    coefficients: dict[tuple[int, int, int], sp.Expr],
    axis: int,
    degree: int,
) -> dict[tuple[int, int, int], sp.Expr]:
    """Convert one unit-interval power coordinate to Bernstein form."""

    other_axes = [candidate for candidate in range(3) if candidate != axis]
    groups: dict[tuple[int, int], dict[int, sp.Expr]] = {}
    for monomial, coefficient in coefficients.items():
        key = tuple(monomial[candidate] for candidate in other_axes)
        groups.setdefault(key, {})[monomial[axis]] = coefficient

    answer: dict[tuple[int, int, int], sp.Expr] = {}
    for key, powers in groups.items():
        for k in range(degree + 1):
            value = sum(
                powers.get(i, 0)
                * sp.Rational(comb(k, i), comb(degree, i))
                for i in range(k + 1)
            )
            monomial = [0, 0, 0]
            monomial[axis] = k
            for candidate, exponent in zip(other_axes, key):
                monomial[candidate] = exponent
            if value:
                answer[tuple(monomial)] = value
    return answer


def tensor_bernstein(
    expression: sp.Expr,
    intervals: tuple[tuple[sp.Rational, sp.Rational], ...],
) -> tuple[tuple[int, int, int], list[sp.Expr]]:
    """Return exact tensor-Bernstein coefficients in (r,p,q) order."""

    polynomial = sp.Poly(expression, r, p, q)
    degree = tuple(polynomial.degree(variable) for variable in (r, p, q))
    coefficients = {monomial: value for monomial, value in polynomial.terms()}

    # Transform the long edge coordinates first, retaining small integer
    # coefficient polynomials in r until the last step.
    for axis in (2, 1, 0):
        lower, upper = intervals[axis]
        coefficients = affine_power(
            coefficients, axis, degree[axis], lower, upper
        )
        coefficients = power_to_bernstein(
            coefficients, axis, degree[axis]
        )
    return degree, list(coefficients.values())


def product_entry_numerators(
    u: tuple[sp.Expr, ...],
    v: tuple[sp.Expr, ...],
    b: sp.Expr,
    d: sp.Expr,
) -> dict[tuple[int, int], sp.Expr]:
    """Clear positive denominators and reduce six raw product gaps mod P."""

    numerator_b, denominator_b = b.as_numer_denom()
    numerator_d, denominator_d = d.as_numer_denom()
    excess_b = r * numerator_b - (r - 1) * denominator_b
    excess_d = r * numerator_d - (r - 1) * denominator_d
    excess_denominator_b = r * denominator_b
    excess_denominator_d = r * denominator_d
    inverse_degrees = DEGREES  # e_i=1/DEGREES[i]

    answer: dict[tuple[int, int], sp.Expr] = {}
    for i in range(3):
        numerator_u, denominator_u = u[i].as_numer_denom()
        numerator_v, denominator_v = v[i].as_numer_denom()
        left = modular_product(
            numerator_u,
            numerator_v,
            excess_denominator_b,
            excess_denominator_d,
        )
        right = modular_product(
            r**3,
            excess_b,
            excess_d,
            denominator_u,
            denominator_v,
        )
        answer[i, i] = (left - right).as_expr()

    for i, j in ((0, 1), (0, 2), (1, 2)):
        numerator_ui, denominator_ui = u[i].as_numer_denom()
        numerator_uj, denominator_uj = u[j].as_numer_denom()
        numerator_vi, denominator_vi = v[i].as_numer_denom()
        numerator_vj, denominator_vj = v[j].as_numer_denom()
        degree_i, degree_j = inverse_degrees[i], inverse_degrees[j]

        # First summand: u_i e_j v_j.
        numerator_1 = (numerator_ui, numerator_vj)
        denominator_1 = (denominator_ui, degree_j, denominator_vj)
        # Second summand: u_j e_i v_i.
        numerator_2 = (numerator_uj, numerator_vi)
        denominator_2 = (denominator_uj, degree_i, denominator_vi)

        inverse_degree_denominator = degree_i * degree_j
        inverse_degree_numerator = degree_i + degree_j
        left_1 = modular_product(
            *numerator_1,
            *denominator_2,
            inverse_degree_denominator,
            excess_denominator_b,
            excess_denominator_d,
        )
        left_2 = modular_product(
            *numerator_2,
            *denominator_1,
            inverse_degree_denominator,
            excess_denominator_b,
            excess_denominator_d,
        )
        right = modular_product(
            r**3,
            excess_b,
            excess_d,
            *denominator_1,
            *denominator_2,
            inverse_degree_numerator,
        )
        answer[i, j] = (left_1 + left_2 - right).as_expr()
    return answer


def main() -> None:
    bd_singleton, bd_pair = schur_chain("Bd", r)
    db_singleton, db_pair = schur_chain("dB", r)
    b = sp.cancel(sum(bd_singleton) / 3)
    d = sp.cancel(sum(db_singleton) / 3)

    # Type complementation: reciprocal singleton fixation equals one minus
    # forward fixation from its complementary doubleton.
    u = tuple(
        sp.cancel(1 - bd_pair[pair])
        for pair in ((1, 2), (0, 2), (0, 1))
    )
    v = tuple(
        sp.cancel(1 - db_pair[pair])
        for pair in ((1, 2), (0, 2), (0, 1))
    )

    for expression in (*bd_singleton, *db_singleton, *u, *v, b, d):
        positive_denominator(expression)

    # Isolate R_hyb exactly.
    assert sp.Poly(HYBRID_EXPR, r).count_roots(ROOT_LO, ROOT_HI) == 1
    assert HYBRID_EXPR.subs(r, ROOT_LO) > 0
    assert HYBRID_EXPR.subs(r, ROOT_HI) < 0

    # On q <= 1/2000 the dB excess is negative, so the positive-part target
    # vanishes for every portal vector.
    numerator_d, denominator_d = d.as_numer_denom()
    excess_d = r * numerator_d - (r - 1) * denominator_d
    small_numerator = -reduce_at_hybrid(excess_d).as_expr()
    small_degree, small_coefficients = tensor_bernstein(
        small_numerator,
        ((ROOT_LO, ROOT_HI), (sp.Rational(0), sp.Rational(1)),
         (sp.Rational(0), SMALL_EDGE)),
    )
    assert small_degree == (5, 4, 4)
    assert len(small_coefficients) == 150
    assert all(coefficient > 0 for coefficient in small_coefficients)

    # On the remaining chamber, prove the stronger raw (no positive parts)
    # product entrywise.  Positive parts are then immediate: if either excess
    # is nonpositive the desired target is zero, while q_B q_D is positive.
    entries = product_entry_numerators(u, v, b, d)
    expected = {
        (0, 0): ((5, 24, 24), 3750),
        (1, 1): ((5, 24, 24), 3750),
        (2, 2): ((5, 24, 24), 3750),
        (0, 1): ((5, 39, 39), 9600),
        (0, 2): ((5, 38, 39), 9360),
        (1, 2): ((5, 38, 39), 9360),
    }
    for indices, numerator in entries.items():
        degree, coefficients = tensor_bernstein(
            numerator,
            ((ROOT_LO, ROOT_HI), (sp.Rational(0), sp.Rational(1)),
             (SMALL_EDGE, sp.Rational(1))),
        )
        assert (degree, len(coefficients)) == expected[indices]
        assert all(coefficient > 0 for coefficient in coefficients), indices

    print("PASS exact Bd and dB singleton/doubleton Schur chains")
    print("PASS all rational denominators have positive coefficients")
    print("PASS 150 coefficients force zero target on q <= 1/2000")
    print("PASS 39,570 coefficients prove all six portal entries on q >= 1/2000")
    print("PROVED minimal portal product for every positive weighted triangle")


if __name__ == "__main__":
    main()
