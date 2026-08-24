#!/usr/bin/env python3
"""Hostile exact audit of the weighted-triangle dB classification.

This file deliberately imports neither the phase-two derivation nor the
project Markov solver.  It constructs the six transient subset equations from
dead-target/parent loops, then checks the manuscript polynomials independently.
All tests are exact over SymPy rationals or rational-function fields.
"""

from __future__ import annotations

import random
from itertools import permutations

import sympy as sp


class CertificateFailure(RuntimeError):
    """Raised when an explicit certificate check fails."""


def require(condition, detail="certificate check failed"):
    """Raise a failure that remains active under optimized Python."""
    if not condition:
        raise CertificateFailure(str(detail))


r = sp.symbols("r", positive=True)
a, b, c = sp.symbols("a b c", positive=True)
x, y = sp.symbols("x y", positive=True)


def direct_state_system(weights, fitness):
    """Return 3*(state-change Laplacian) and fixation rhs for masks 1..6."""

    n = 3
    full = (1 << n) - 1
    states = tuple(range(1, full))
    index = {mask: position for position, mask in enumerate(states)}
    matrix = sp.zeros(len(states))
    rhs = sp.zeros(len(states), 1)

    for mask in states:
        row = index[mask]
        for target in range(n):
            denominator = sum(
                (fitness if mask & (1 << source) else 1)
                * weights[source][target]
                for source in range(n)
            )
            for source in range(n):
                weight = weights[source][target]
                if weight == 0:
                    continue
                scaled_probability = (
                    (fitness if mask & (1 << source) else 1)
                    * weight
                    / denominator
                )
                if mask & (1 << source):
                    next_mask = mask | (1 << target)
                else:
                    next_mask = mask & ~(1 << target)
                if next_mask == mask:
                    continue
                matrix[row, row] += scaled_probability
                if next_mask == full:
                    rhs[row, 0] += scaled_probability
                elif next_mask != 0:
                    matrix[row, index[next_mask]] -= scaled_probability

    return matrix.applyfunc(sp.cancel), rhs.applyfunc(sp.cancel), states


def claimed_polynomials(edge_a, edge_b, edge_c):
    s1 = edge_a + edge_b + edge_c
    s2 = edge_a * edge_b + edge_a * edge_c + edge_b * edge_c
    s3 = edge_a * edge_b * edge_c
    B5 = 12 * s1 * s2 * s3 - 36 * s3**2
    B4 = (
        12 * s1**3 * s3
        - 56 * s1 * s2 * s3
        + 12 * s2**3
        + 72 * s3**2
    )
    B3 = (
        -24 * s1**3 * s3
        + 12 * s1**2 * s2**2
        + 80 * s1 * s2 * s3
        - 24 * s2**3
        - 90 * s3**2
    )
    P = sp.expand(
        9 * s3**2 * (r**6 + 1)
        + B5 * (r**5 + r)
        + B4 * (r**4 + r**2)
        + B3 * r**3
    )
    A = sp.expand(3 * s3 * (s1 * s2 - 9 * s3))
    D = sp.expand(
        12 * s1**3 * s3
        - 45 * s1 * s2 * s3
        + 4 * s2**3
        - 27 * s3**2
    )
    E = sp.expand(4 * s2 * (3 * s1**2 * s2 - 3 * s1 * s3 - 8 * s2**2))
    H = sp.expand(A * (r - 1) ** 4 + D * r * (r - 1) ** 2 + E * r**2)
    return {
        "s1": s1,
        "s2": s2,
        "s3": s3,
        "B5": sp.expand(B5),
        "B4": sp.expand(B4),
        "B3": sp.expand(B3),
        "P": P,
        "A": A,
        "D": D,
        "E": E,
        "H": H,
    }


def claimed_difference(edge_a, edge_b, edge_c):
    data = claimed_polynomials(edge_a, edge_b, edge_c)
    return sp.cancel(-r * (r - 1) * data["H"] / (3 * (r + 1) * data["P"]))


def exact_average(weights, fitness):
    matrix, rhs, states = direct_state_system(weights, fitness)
    values = matrix.inv(method="DM") * rhs
    return sp.cancel(sum(values[states.index(1 << vertex), 0] for vertex in range(3)) / 3)


def verify_symmetric_coefficients_and_determinant():
    weights = ((0, a, b), (a, 0, c), (b, c, 0))
    matrix, _, _ = direct_state_system(weights, r)
    row_gaps = matrix * sp.ones(6, 1) - sp.ones(6, 1)
    require(all(sp.cancel(entry) == 0 for entry in row_gaps))

    data = claimed_polynomials(a, b, c)
    local_product = sp.prod(r * u + v for u, v in permutations((a, b, c), 2))
    cleared_determinant = sp.cancel(matrix.det(method="domain-ge") * local_product / 3)
    require(sp.denom(cleared_determinant) == 1)
    require(sp.expand(cleared_determinant - data["P"]) == 0)

    polynomial = sp.Poly(cleared_determinant, r)
    expected = {
        6: 9 * data["s3"] ** 2,
        5: data["B5"],
        4: data["B4"],
        3: data["B3"],
        2: data["B4"],
        1: data["B5"],
        0: 9 * data["s3"] ** 2,
    }
    for degree, coefficient in expected.items():
        require(sp.expand(polynomial.coeff_monomial(r**degree) - coefficient) == 0)

    for expression in (data["B5"], data["B4"], data["B3"], data["A"], data["D"], data["E"]):
        for permuted in permutations((a, b, c)):
            replacement = {a: permuted[0], b: permuted[1], c: permuted[2]}
            require(sp.expand(expression.xreplace(replacement) - expression) == 0)


def verify_direct_symbolic_difference():
    weights = ((0, 1, x), (1, 0, y), (x, y, 0))
    rho = exact_average(weights, r)
    baseline = 2 * r / (3 * (r + 1))
    require(sp.cancel(rho - baseline - claimed_difference(1, x, y)) == 0)


def verify_sos_identities():
    data = claimed_polynomials(a, b, c)
    s1, s2, s3 = data["s1"], data["s2"], data["s3"]
    X, Y, Z0 = a * b, a * c, b * c
    U = s1**2 - 3 * s2
    V = s2**2 - 3 * s1 * s3
    W = s1 * s2 - 9 * s3
    Z = s2**3 - 27 * s3**2

    U_squares = ((a - b) ** 2 + (a - c) ** 2 + (b - c) ** 2) / 2
    V_squares = ((X - Y) ** 2 + (X - Z0) ** 2 + (Y - Z0) ** 2) / 2
    W_squares = c * (a - b) ** 2 + b * (a - c) ** 2 + a * (b - c) ** 2
    Z_squares = s2 * V + 3 * (
        Z0 * (X - Y) ** 2 + Y * (X - Z0) ** 2 + X * (Y - Z0) ** 2
    )
    require(sp.expand(U - U_squares) == 0)
    require(sp.expand(V - V_squares) == 0)
    require(sp.expand(W - W_squares) == 0)
    require(sp.expand(Z - Z_squares) == 0)
    require(sp.expand(data["A"] - 3 * s3 * W) == 0)
    require(sp.expand(data["D"] - (12 * s1 * s3 * U + 3 * s2 * V + Z)) == 0)
    require(sp.expand(data["E"] - 4 * s2 * (3 * s2 * U + V)) == 0)
    require(sp.expand(
        data["H"]
        - (data["A"] * (r - 1) ** 4 + data["D"] * r * (r - 1) ** 2 + data["E"] * r**2)
    ) == 0)


def verify_edge_limits():
    data = claimed_polynomials(a, b, c)
    P_at_zero = sp.factor(data["P"].subs(a, 0))
    H_at_zero = sp.factor(data["H"].subs(a, 0))
    require(P_at_zero == 12 * b**2 * c**2 * r**2 * (b + c * r) * (b * r + c))
    require(sp.expand(
        H_at_zero
        - 4
        * b**2
        * c**2
        * r
        * (b * c * (r - 1) ** 2 + r * (3 * b**2 - 2 * b * c + 3 * c**2))
    ) == 0)

    t = sp.symbols("t", positive=True)
    paths = (
        ((1, t, 1), -(r - 1) / (9 * (r + 1)), -(r - 1) / (3 * (r + 1))),
        ((1, t, t), -(r - 1) / (3 * (r + 1)), -(r - 1) / (9 * (r + 1))),
        ((1, t, 1 / t), -(r - 1) / (3 * (r + 1)), -(r - 1) / (3 * (r + 1))),
    )
    for weights, expected_zero, expected_infinity in paths:
        difference = claimed_difference(*weights)
        require(sp.factor(sp.limit(difference, t, 0, dir="+") - expected_zero) == 0)
        require(sp.factor(sp.limit(difference, t, sp.oo) - expected_infinity) == 0)

    epsilon = sp.symbols("epsilon", positive=True)
    near_uniform = claimed_difference(1, 1 + epsilon, 1)
    expected_quadratic = -2 * r * (r - 1) / (
        9 * (r + 1) * (r**2 + 3 * r + 1)
    )
    require(sp.factor(sp.limit(near_uniform / epsilon**2, epsilon, 0) - expected_quadratic) == 0)


def verify_random_and_extreme_cases():
    generator = random.Random(20260801)
    checked = 0
    for _ in range(120):
        weights = tuple(
            sp.Rational(generator.randint(1, 19), generator.randint(1, 11))
            for _ in range(3)
        )
        if weights[0] == weights[1] == weights[2]:
            continue
        fitness = sp.Rational(
            generator.randint(2, 30) + generator.randint(1, 12),
            generator.randint(2, 30),
        )
        if fitness <= 1:
            fitness = 1 + fitness
        edge_a, edge_b, edge_c = weights
        matrix_weights = (
            (0, edge_a, edge_b),
            (edge_a, 0, edge_c),
            (edge_b, edge_c, 0),
        )
        rho = exact_average(matrix_weights, fitness)
        baseline = 2 * fitness / (3 * (fitness + 1))
        direct_difference = sp.cancel(rho - baseline)
        formula = sp.cancel(claimed_difference(*weights).subs(r, fitness))
        require(direct_difference == formula)
        require(direct_difference < 0)
        data = claimed_polynomials(*weights)
        require(data["P"].subs(r, fitness) > 0)
        require(data["H"].subs(r, fitness) > 0)
        checked += 1

    extremes = (
        ((sp.Rational(1), sp.Rational(1, 10**9), sp.Rational(10**9)), sp.Rational(1000001, 1000000)),
        ((sp.Rational(1), sp.Rational(1, 10**12), sp.Rational(10**12)), sp.Rational(10**6)),
        ((sp.Rational(10**15), sp.Rational(10**15 + 1), sp.Rational(10**15 - 1)), sp.Rational(2)),
    )
    for weights, fitness in extremes:
        edge_a, edge_b, edge_c = weights
        matrix_weights = (
            (0, edge_a, edge_b),
            (edge_a, 0, edge_c),
            (edge_b, edge_c, 0),
        )
        direct_difference = sp.cancel(
            exact_average(matrix_weights, fitness) - 2 * fitness / (3 * (fitness + 1))
        )
        formula = sp.cancel(claimed_difference(*weights).subs(r, fitness))
        require(direct_difference == formula)
        require(direct_difference < 0)

    for common in (sp.Rational(1), sp.Rational(7, 13), sp.Rational(10**8)):
        matrix_weights = ((0, common, common), (common, 0, common), (common, common, 0))
        for fitness in (sp.Rational(11, 10), sp.Rational(2), sp.Rational(10**5)):
            require(sp.cancel(
                exact_average(matrix_weights, fitness)
                - 2 * fitness / (3 * (fitness + 1))
            ) == 0)
    return checked, len(extremes)


def main():
    verify_symmetric_coefficients_and_determinant()
    print("[PASS] all seven reciprocal coefficients of P match the direct determinant")
    verify_direct_symbolic_difference()
    print("[PASS] direct subset-state solution matches the homogeneous H/P formula")
    verify_sos_identities()
    print("[PASS] all gap and numerator SOS identities expand to zero")
    verify_edge_limits()
    print("[PASS] one-edge, extreme-ratio, and near-uniform symbolic limits match")
    random_count, extreme_count = verify_random_and_extreme_cases()
    print(f"[PASS] {random_count} deterministic random and {extreme_count} extreme exact cases")
    print("[VERDICT] no counterexample; classification and equality condition are exact")


if __name__ == "__main__":
    main()
