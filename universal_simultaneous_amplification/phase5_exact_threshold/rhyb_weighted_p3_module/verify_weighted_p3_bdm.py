#!/usr/bin/env python3
"""Exact replay of BDM for every weighted three-vertex path.

The script derives the labelled fixation chains rather than taking the dual
moments as inputs.  All endpoint and Bernstein calculations use exact SymPy
rationals.  No floating-point sign is used.
"""

from __future__ import annotations

from collections import defaultdict
from math import comb

import sympy as sp


r, t = sp.symbols("r t", positive=True)
ROOT_LO = sp.Rational(1502856912, 10**9)
ROOT_HI = sp.Rational(1502856913, 10**9)
SMALL_INTERVAL = (sp.Rational(0), sp.Rational(1, 250))
LARGE_INTERVALS = (
    (sp.Rational(1, 250), sp.Rational(1, 100)),
    (sp.Rational(1, 100), sp.Rational(1, 20)),
    (sp.Rational(1, 20), sp.Rational(1, 10)),
    (sp.Rational(1, 10), sp.Rational(1, 4)),
    (sp.Rational(1, 4), sp.Rational(1, 2)),
    (sp.Rational(1, 2), sp.Rational(3, 4)),
    (sp.Rational(3, 4), sp.Rational(1)),
)

WEIGHTS = (
    (sp.Integer(0), sp.Integer(1), sp.Integer(0)),
    (sp.Integer(1), sp.Integer(0), t),
    (sp.Integer(0), t, sp.Integer(0)),
)


def fixation_vector(rule: str, fitness: sp.Expr) -> tuple[sp.Expr, ...]:
    """Solve the six labelled transient states of the original process."""

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


def displayed_data() -> tuple[
    sp.Expr, sp.Expr, tuple[sp.Expr, ...], tuple[sp.Expr, ...]
]:
    """Return and independently check the displayed a,b,u,v formulas."""

    bd = fixation_vector("Bd", r)
    db = fixation_vector("dB", r)
    bd_reciprocal = fixation_vector("Bd", 1 / r)
    db_reciprocal = fixation_vector("dB", 1 / r)

    # Type complementation at reciprocal fitness.
    for vertex in range(3):
        singleton = 1 << vertex
        complement = 7 ^ singleton
        assert sp.factor(
            bd_reciprocal[singleton - 1] + bd[complement - 1] - 1
        ) == 0
        assert sp.factor(
            db_reciprocal[singleton - 1] + db[complement - 1] - 1
        ) == 0

    A = r**2 * (t + 1) + r * t + t * (t + 1)
    B = r**2 * t * (t + 1) + r * t + t + 1
    N_center = (
        2 * r**3 * t
        + r**2 * t**2
        + 3 * r**2 * t
        + r**2
        + r * t**2
        + 2 * r * t
        + r
        + t**2
        + 2 * t
        + 1
    )
    expected_u = (
        t * (t + 1) / A,
        t * N_center / ((2 * r + 1) * A * B),
        (t + 1) / B,
    )
    expected_v = (
        1 / (2 * (r * t + 1)),
        (2 * r**2 * t + 3 * r * t**2 + 3 * r + 4 * t)
        / (6 * (r + t) * (r * t + 1)),
        t / (2 * (r + t)),
    )
    singleton_masks = (1, 2, 4)
    u = tuple(bd_reciprocal[mask - 1] for mask in singleton_masks)
    v = tuple(db_reciprocal[mask - 1] for mask in singleton_masks)
    assert all(sp.factor(x - y) == 0 for x, y in zip(u, expected_u))
    assert all(sp.factor(x - y) == 0 for x, y in zip(v, expected_v))

    b = sp.factor(sum(bd[mask - 1] for mask in singleton_masks) / 3)
    a = sp.factor(
        sum(db[mask - 1] for mask in singleton_masks) / (3 * (r - 1))
    )
    N_b = (
        3 * r**3 * t**3
        + 6 * r**3 * t**2
        + 3 * r**3 * t
        + 6 * r**2 * t**3
        + 12 * r**2 * t**2
        + 6 * r**2 * t
        + r * t**4
        + 5 * r * t**3
        + 9 * r * t**2
        + 5 * r * t
        + r
        + 2 * t**4
        + 4 * t**3
        + 6 * t**2
        + 4 * t
        + 2
    )
    expected_a = (5 * r**2 * t + 3 * r * t**2 + 3 * r + t) / (
        9 * (r - 1) * (r + t) * (r * t + 1)
    )
    expected_b = r**2 * N_b / (3 * (r + 2) * A * B)
    assert sp.factor(a - expected_a) == 0
    assert sp.factor(b - expected_b) == 0
    return a, b, u, v


def reflection_checks(
    a: sp.Expr,
    b: sp.Expr,
    u: tuple[sp.Expr, ...],
    v: tuple[sp.Expr, ...],
) -> None:
    """Check that reflection reduces every t>0 to 0<t<=1."""

    assert sp.factor(a - a.subs(t, 1 / t)) == 0
    assert sp.factor(b - b.subs(t, 1 / t)) == 0
    for left, right in ((0, 2), (1, 1), (2, 0)):
        assert sp.factor(u[left] - u[right].subs(t, 1 / t)) == 0
        assert sp.factor(v[left] - v[right].subs(t, 1 / t)) == 0

    e = (sp.Integer(1), 1 / (1 + t), 1 / t)
    reflected_e = tuple(value.subs(t, 1 / t) for value in e)
    assert all(
        sp.factor(reflected_e[i] - t * e[2 - i]) == 0 for i in range(3)
    )

    # Check the complete portal quotient, including the degree reweighting.
    x_l, x_c, x_r = sp.symbols("x_l x_c x_r", nonnegative=True)
    x = (x_l, x_c, x_r)
    reflected_x = (x_r, x_c, x_l)

    def quotient(
        loads: tuple[sp.Expr, ...],
        uu: tuple[sp.Expr, ...],
        vv: tuple[sp.Expr, ...],
        ee: tuple[sp.Expr, ...],
    ) -> sp.Expr:
        return sp.cancel(
            sum(loads[i] * uu[i] for i in range(3))
            * sum(loads[i] * ee[i] * vv[i] for i in range(3))
            / (
                sum(loads)
                * sum(loads[i] * ee[i] for i in range(3))
            )
        )

    reflected_u = tuple(value.subs(t, 1 / t) for value in u)
    reflected_v = tuple(value.subs(t, 1 / t) for value in v)
    assert sp.factor(
        quotient(x, u, v, e)
        - quotient(reflected_x, reflected_u, reflected_v, reflected_e)
    ) == 0


def power_to_bernstein(poly: sp.Expr, variable: sp.Symbol) -> list[sp.Expr]:
    """Return exact Bernstein coefficients on [0,1]."""

    polynomial = sp.Poly(sp.expand(poly), variable)
    degree = polynomial.degree()
    power = [polynomial.coeff_monomial(variable**i) for i in range(degree + 1)]
    return [
        sp.factor(
            sum(
                power[i] * sp.Rational(comb(k, i), comb(degree, i))
                for i in range(k + 1)
            )
        )
        for k in range(degree + 1)
    ]


def positive_for_r_at_least_three_halves(expression: sp.Expr) -> None:
    """Certify positivity by nonnegative powers of y=r-3/2."""

    y = sp.symbols("y", nonnegative=True)
    shifted = sp.Poly(sp.expand(expression.subs(r, sp.Rational(3, 2) + y)), y)
    coefficients = [coefficient for _, coefficient in shifted.terms()]
    assert coefficients
    assert all(coefficient >= 0 for coefficient in coefficients)
    assert shifted.eval(0) > 0


def portal_extremal_check(
    u: tuple[sp.Expr, ...], v: tuple[sp.Expr, ...]
) -> sp.Expr:
    """Reconstruct all portal-matrix entries and prove q(x)>=u_L v_L."""

    A = r**2 * (t + 1) + r * t + t * (t + 1)
    B = r**2 * t * (t + 1) + r * t + t + 1
    e = (sp.Integer(1), 1 / (1 + t), 1 / t)
    k_zero = sp.factor(u[0] * v[0])
    assert sp.factor(
        k_zero - t * (t + 1) / (2 * (r * t + 1) * A)
    ) == 0

    delta = {
        (i, j): sp.factor(
            u[i] * e[j] * v[j]
            + u[j] * e[i] * v[i]
            - k_zero * (e[i] + e[j])
        )
        for i in range(3)
        for j in range(i, 3)
    }
    assert delta[(0, 0)] == 0

    F_lc = (
        4 * r**4 * t**3
        + 4 * r**4 * t**2
        + 6 * r**3 * t**4
        + 6 * r**3 * t**3
        - 2 * r**3 * t**2
        + 3 * r**2 * t**4
        + 2 * r**2 * t**3
        - 3 * r**2 * t**2
        + 4 * r**2 * t
        + 3 * r**2
        + 3 * r * t**3
        + 2 * r * t**2
        - t**2
        - t
    )
    F_cc = (
        4 * r**4 * t**2
        + 2 * r**3 * t**3
        - 2 * r**3 * t**2
        + 2 * r**3 * t
        - 3 * r**2 * t**4
        - 2 * r**2 * t**3
        - 2 * r**2 * t**2
        + 4 * r**2 * t
        + 3 * r**2
        - 3 * r * t**4
        - 2 * r * t**3
        + 2 * r * t**2
        + r * t
        - t**3
        - 2 * t**2
        - t
    )
    F_cr = (
        4 * r**4 * t**2
        + 4 * r**4 * t
        - 2 * r**3 * t**2
        + 6 * r**3 * t
        + 6 * r**3
        - 9 * r**2 * t**4
        - 2 * r**2 * t**3
        - 3 * r**2 * t**2
        + 14 * r**2 * t
        + 9 * r**2
        - 6 * r * t**4
        - 3 * r * t**3
        + 2 * r * t**2
        + 9 * r * t
        + 3 * r
        - t**3
        - t**2
    )

    expected_delta = {
        (0, 1): t * (r - 1) * F_lc
        / (6 * (r + t) * (2 * r + 1) * (r * t + 1) * A * B),
        (0, 2): r
        * (r - 1)
        * (t - 1)
        * (t + 1)
        * (r * (t + 1) ** 2 * (t - 1) - 2 * t - 1)
        / (2 * (r + t) * (r * t + 1) * A * B),
        (1, 1): t * (r - 1) * F_cc
        / (3 * (r + t) * (2 * r + 1) * (t + 1) * (r * t + 1) * A * B),
        (1, 2): (r - 1) * F_cr
        / (6 * (r + t) * (2 * r + 1) * (r * t + 1) * A * B),
        (2, 2): -r
        * (r - 1)
        * (t - 1)
        * (t + 1)
        * (t**2 + t + 1)
        / ((r + t) * (r * t + 1) * A * B),
    }
    for key, expected in expected_delta.items():
        assert sp.factor(delta[key] - expected) == 0

    expected_bernstein = {
        "LC": (
            3 * r**2,
            (4 * r - 1) * (4 * r + 1) / 4,
            (4 * r**4 - 2 * r**3 + 27 * r**2 + 2 * r - 4) / 6,
            (12 * r**4 + 2 * r**3 + 20 * r**2 + 7 * r - 5) / 4,
            (r + 1) * (4 * r - 1) * (2 * r**2 + r + 2),
        ),
        "CC": (
            3 * r**2,
            (2 * r**3 + 16 * r**2 + r - 1) / 4,
            (4 * r**4 + 4 * r**3 + 28 * r**2 + 5 * r - 5) / 6,
            (2 * r - 1) * (4 * r**3 + 4 * r**2 + 11 * r + 8) / 4,
            2 * (r - 1) * (r + 1) * (2 * r**2 + r + 2),
        ),
        "CR": (
            3 * r * (r + 1) * (2 * r + 1),
            r * (2 * r + 3) * (2 * r**2 + 12 * r + 7) / 4,
            (16 * r**4 + 52 * r**3 + 93 * r**2 + 47 * r - 1) / 6,
            (20 * r**4 + 38 * r**3 + 70 * r**2 + 40 * r - 3) / 4,
            (r + 1) * (4 * r - 1) * (2 * r**2 + r + 2),
        ),
    }
    for name, polynomial in (("LC", F_lc), ("CC", F_cc), ("CR", F_cr)):
        coefficients = tuple(power_to_bernstein(polynomial, t))
        assert all(
            sp.factor(x - y) == 0
            for x, y in zip(coefficients, expected_bernstein[name])
        )
        for coefficient in coefficients:
            positive_for_r_at_least_three_halves(coefficient)

    # Reconstruct the complete quadratic form abstractly, avoiding a costly
    # re-expansion of the already checked rational entries.  delta_ii is
    # twice the actual diagonal coefficient by definition.
    abstract_u = sp.symbols("abstract_u0:3")
    abstract_v = sp.symbols("abstract_v0:3")
    abstract_e = sp.symbols("abstract_e0:3")
    abstract_x = sp.symbols("abstract_x0:3")
    abstract_k = sp.symbols("abstract_k")
    abstract_delta = {
        (i, j): abstract_u[i] * abstract_e[j] * abstract_v[j]
        + abstract_u[j] * abstract_e[i] * abstract_v[i]
        - abstract_k * (abstract_e[i] + abstract_e[j])
        for i in range(3)
        for j in range(i, 3)
    }
    abstract_gap = (
        sum(abstract_x[i] * abstract_u[i] for i in range(3))
        * sum(
            abstract_x[i] * abstract_e[i] * abstract_v[i]
            for i in range(3)
        )
        - abstract_k
        * sum(abstract_x)
        * sum(abstract_x[i] * abstract_e[i] for i in range(3))
    )
    abstract_reconstruction = (
        sum(
            abstract_delta[(i, i)] * abstract_x[i] ** 2 / 2
            for i in range(3)
        )
        + sum(
            abstract_delta[(i, j)] * abstract_x[i] * abstract_x[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
    )
    assert sp.expand(abstract_gap - abstract_reconstruction) == 0
    return k_zero


def tensor_bernstein_coefficients(
    polynomial: sp.Expr,
    r_interval: tuple[sp.Rational, sp.Rational],
    t_interval: tuple[sp.Rational, sp.Rational],
) -> tuple[int, int, list[sp.Rational]]:
    """Map a bivariate polynomial to a rectangle and return exact coefficients."""

    y, z = sp.symbols("y z")
    r_lo, r_hi = r_interval
    t_lo, t_hi = t_interval
    mapped = sp.Poly(
        sp.expand(
            polynomial.subs(
                {r: r_lo + (r_hi - r_lo) * y, t: t_lo + (t_hi - t_lo) * z},
                simultaneous=True,
            )
        ),
        y,
        z,
    )
    r_degree = mapped.degree(y)
    t_degree = mapped.degree(z)
    power = {
        (i, j): mapped.coeff_monomial(y**i * z**j)
        for i in range(r_degree + 1)
        for j in range(t_degree + 1)
    }
    coefficients = [
        sp.factor(
            sum(
                power[(i, j)]
                * sp.Rational(comb(big_i, i), comb(r_degree, i))
                * sp.Rational(comb(big_j, j), comb(t_degree, j))
                for i in range(big_i + 1)
                for j in range(big_j + 1)
            )
        )
        for big_i in range(r_degree + 1)
        for big_j in range(t_degree + 1)
    ]
    assert len(coefficients) == (r_degree + 1) * (t_degree + 1)
    return r_degree, t_degree, coefficients


def scalar_endpoint_check(a: sp.Expr, b: sp.Expr, k_zero: sp.Expr) -> None:
    """Check a,b<1 and both exact endpoint Bernstein regimes."""

    polynomial = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    assert sp.Poly(polynomial, r).count_roots(ROOT_LO, ROOT_HI) == 1

    # Exact one-variable Bernstein lists for the two endpoint coefficients.
    one_minus_a_num, one_minus_a_den = map(
        sp.factor, sp.together(1 - a).as_numer_denom()
    )
    expected_a_bernstein = (
        3 * r * (3 * r - 4),
        (r + 1) * (9 * r**2 - 5 * r - 10) / 2,
        (r + 1) * (9 * r**2 - 5 * r - 10),
    )
    assert all(
        sp.factor(x - y) == 0
        for x, y in zip(power_to_bernstein(one_minus_a_num, t), expected_a_bernstein)
    )
    assert sp.factor(
        one_minus_a_den - 9 * (r - 1) * (r + t) * (r * t + 1)
    ) == 0

    one_minus_b_num, one_minus_b_den = map(
        sp.factor, sp.together(1 - b).as_numer_denom()
    )
    expected_b_bernstein = (
        2 * r**2 * (r + 2),
        3 * (r**4 + 5 * r**3 + 9 * r**2 + 3 * r + 2) / 4,
        5 * (r**4 + 3 * r**3 + 5 * r**2 + 3 * r + 2) / 2,
        3 * (r**2 + 2 * r + 2) * (2 * r**2 + r + 2),
        6 * (r**2 + 2 * r + 2) * (2 * r**2 + r + 2),
    )
    assert all(
        sp.factor(x - y) == 0
        for x, y in zip(power_to_bernstein(one_minus_b_num, t), expected_b_bernstein)
    )
    A = r**2 * (t + 1) + r * t + t * (t + 1)
    B = r**2 * t * (t + 1) + r * t + t + 1
    assert sp.factor(one_minus_b_den - 3 * (r + 2) * A * B) == 0
    for coefficient in expected_a_bernstein + expected_b_bernstein:
        positive_for_r_at_least_three_halves(coefficient)

    C = r * (r - 1) ** 2
    s = a + b - 1
    K_zero = C / k_zero

    small = sp.factor(1 - K_zero * s)
    small_num, small_den = map(sp.factor, sp.together(small).as_numer_denom())
    assert sp.factor(
        small_den - 9 * t * (r + 2) * (r + t) * (t + 1) * B
    ) == 0
    r_degree, t_degree, small_coefficients = tensor_bernstein_coefficients(
        small_num, (ROOT_LO, ROOT_HI), SMALL_INTERVAL
    )
    assert (r_degree, t_degree, len(small_coefficients)) == (9, 6, 70)
    assert all(coefficient > 0 for coefficient in small_coefficients)

    strong = sp.factor(4 * k_zero * (1 - a) * (1 - b) - C * s**2)
    strong_num, strong_den = map(
        sp.factor, sp.together(strong).as_numer_denom()
    )
    assert sp.factor(strong_den - (
        81
        * (r - 1)
        * (r + 2) ** 2
        * (r + t) ** 2
        * (r * t + 1) ** 2
        * A**2
        * B**2
    )) == 0
    large_certificate_sizes = []
    for interval in LARGE_INTERVALS:
        r_degree, t_degree, coefficients = tensor_bernstein_coefficients(
            strong_num, (ROOT_LO, ROOT_HI), interval
        )
        assert (r_degree, t_degree, len(coefficients)) == (16, 12, 221)
        assert all(coefficient > 0 for coefficient in coefficients)
        large_certificate_sizes.append(len(coefficients))
    assert large_certificate_sizes == [221] * len(LARGE_INTERVALS)

    # Replay the rationalization used to pass from the strong scalar bound to
    # the square-root/Hellinger target.  With U=sqrt(ab), V=sqrt((1-a)(1-b))
    # and U>V, s=(U-V)(U+V).
    U, V = sp.symbols("U V", positive=True)
    hellinger_remainder = sp.factor(
        (U**2 - V**2) ** 2 - 4 * V**2 * (U - V) ** 2
    )
    assert hellinger_remainder == (U - V) ** 3 * (U + 3 * V)
    assert sp.expand((U - V) * (U + V) - (U**2 - V**2)) == 0

    # Check the normalized portal gap and its monotonicity in q.  Once q is
    # above the Hellinger target, this is the parent quadratic equivalence.
    q, z = sp.symbols("q z", positive=True)
    normalized_gap = sp.expand(
        C * ((1 + z) * (1 - a) - b * z)
        + z * q * (1 + z * (1 - b))
    )
    assert sp.factor(sp.diff(normalized_gap, q) - z * (1 + z * (1 - b))) == 0


def main() -> None:
    a, b, u, v = displayed_data()
    reflection_checks(a, b, u, v)
    k_zero = portal_extremal_check(u, v)
    scalar_endpoint_check(a, b, k_zero)
    print("PASS: four exact labelled chains, complementation, and displayed moments")
    print("PASS: reflection t <-> 1/t, including arbitrary portal laws")
    print("PASS: every portal-matrix entry and all explicit Bernstein lists")
    print("PASS: 70 small-regime tensor-Bernstein coefficients")
    print("PASS: 7 x 221 remaining-regime tensor-Bernstein coefficients")
    print("PASS: exact rationalized Hellinger implication")
    print("PROVED: every weighted P3 satisfies strict BDM at R_hyb")


if __name__ == "__main__":
    main()
