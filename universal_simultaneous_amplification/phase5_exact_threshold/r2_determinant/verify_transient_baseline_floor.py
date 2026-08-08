#!/usr/bin/env python3
"""Exact finite certificates for the transient r=2 baseline-floor route.

The directed-triangle identities and negative path packets are proofs.  The
higher-order Bernstein and boundary checks are finite evidence only.
"""

from __future__ import annotations

from itertools import combinations, product
from math import comb, factorial
from random import Random

import sympy as sp
from flint import fmpq as Q, fmpq_mat


def sympy_active(P):
    n = len(P)
    states = [
        (B, v) for v in range(n) for B in range(1, 1 << n)
        if not B >> v & 1
    ]
    index = {state: i for i, state in enumerate(states)}
    kernel = sp.zeros(len(states))
    for source, (B, v) in enumerate(states):
        k = B.bit_count()
        for i, probability in enumerate(P[v]):
            if probability:
                kernel[source, index[B | (1 << i), v]] += probability / 2
        for w in range(n):
            if B >> w & 1:
                C = B & ~(1 << w)
                for i, probability in enumerate(P[w]):
                    if probability:
                        kernel[source, index[C | (1 << i), w]] += probability / (2 * k)
        assert sp.factor(sum(kernel[source, target] for target in range(len(states)))) == 1
    return states, kernel


def triangle_certificates():
    x, y, z = sp.symbols("x y z", real=True)
    P = (
        (0, x, 1 - x),
        (y, 0, 1 - y),
        (z, 1 - z, 0),
    )
    states, kernel = sympy_active(P)
    assert len(states) == 9
    nu = sp.Matrix([[sp.Rational(B.bit_count(), 12) for B, _ in states]])
    H = sp.Matrix([sp.Rational(1, B.bit_count()) for B, _ in states])
    values = [sp.factor((nu * H)[0])]
    observable = H
    for _ in range(3):
        observable = kernel * observable
        values.append(sp.factor((nu * observable)[0]))
    X, Y, Z = x - sp.Rational(1, 2), y - sp.Rational(1, 2), z - sp.Rational(1, 2)
    assert values[0] == values[1] == sp.Rational(3, 4)
    assert sp.expand(values[2] - values[0] - (X**2 + Y**2 + Z**2) / 12) == 0
    third_increment = (
        (y + z) * X**2
        + (1 + x - z) * Y**2
        + (2 - x - y) * Z**2
    ) / 16
    assert sp.expand(values[3] - values[2] - third_increment) == 0
    alpha = sp.symbols("alpha", real=True)
    Ssq = X**2 + Y**2 + Z**2
    cubic = (X + Y) * (X - Z) * (Y + Z)
    interpolated = [
        [0 if i == j else sp.Rational(1, 2) + alpha * (P[i][j] - sp.Rational(1, 2))
         for j in range(3)]
        for i in range(3)
    ]
    _, ray_kernel = sympy_active(interpolated)
    ray_observable = H
    for _ in range(3):
        ray_observable = ray_kernel * ray_observable
    ray_gap = sp.factor((nu * ray_observable)[0] - sp.Rational(3, 4))
    assert sp.expand(ray_gap - alpha**2 * (7 * Ssq + 3 * alpha * cubic) / 48) == 0

    weights = ((0, 1, 10), (1, 0, 10), (10, 10, 0))
    weighted_P = [
        [sp.Rational(weights[i][j], sum(weights[i])) for j in range(3)]
        for i in range(3)
    ]
    states, weighted = sympy_active(weighted_P)
    size = len(states)
    S = sp.zeros(size)
    rank_counts = {
        rank: sum(B.bit_count() == rank for B, _ in states)
        for rank in (1, 2)
    }
    for source, (B, _) in enumerate(states):
        rank = B.bit_count()
        for target, (C, _) in enumerate(states):
            if C.bit_count() == rank:
                S[source, target] = sp.Rational(1, rank_counts[rank])
    T = sp.eye(size) - S
    R = S * weighted * S
    Bblock = S * weighted * T
    Cblock = T * weighted * S
    Dblock = T * weighted * T
    nu = sp.Matrix([[sp.Rational(B.bit_count(), 12) for B, _ in states]])
    H = sp.Matrix([sp.Rational(1, B.bit_count()) for B, _ in states])
    packets = [
        sp.factor((nu * R * Bblock * Cblock * H)[0]),
        sp.factor((nu * Bblock * Cblock * R * H)[0]),
        sp.factor((nu * Bblock * Dblock * Cblock * H)[0]),
    ]
    assert packets == [sp.Rational(27, 968), sp.Rational(27, 1936), -sp.Rational(135, 85184)]
    assert sum(packets) == sp.Rational(3429, 85184)

    weights = ((0, 1, 2), (1, 0, 2), (2, 2, 0))
    P12 = [
        [sp.Rational(weights[i][j], sum(weights[i])) for j in range(3)]
        for i in range(3)
    ]
    _, actual = sympy_active(P12)
    P0 = [[0 if i == j else sp.Rational(1, 2) for j in range(3)] for i in range(3)]
    _, complete = sympy_active(P0)
    Delta = actual - complete
    packet = sp.factor((nu * Delta * complete**2 * Delta * H)[0])
    assert packet == -sp.Rational(1, 6912)
    print("PASS: exact directed-triangle a2 and a3 certificates")
    print("PASS: exact negative transverse packet and positive grouped t=3 sum")
    print("PASS: exact negative individual two-colour word")


def raw_sympy_active(P):
    """Formal active matrix without assuming the symbolic row sums yet."""
    n = len(P)
    states = [
        (B, v) for v in range(n) for B in range(1, 1 << n)
        if not B >> v & 1
    ]
    index = {state: i for i, state in enumerate(states)}
    kernel = sp.zeros(len(states))
    for source, (B, v) in enumerate(states):
        k = B.bit_count()
        for i, probability in enumerate(P[v]):
            if probability:
                kernel[source, index[B | (1 << i), v]] += probability / 2
        for w in range(n):
            if B >> w & 1:
                C = B & ~(1 << w)
                for i, probability in enumerate(P[w]):
                    if probability:
                        kernel[source, index[C | (1 << i), w]] += probability / (2 * k)
    return states, kernel


def multinomial(exponents):
    degree = sum(exponents)
    answer = factorial(degree)
    for exponent in exponents:
        answer //= factorial(exponent)
    return answer


def elevated_product_simplex_coefficient(polynomial, row_variables, target, degree=3):
    """Coefficient after separate homogeneous elevation on every row."""
    variables = [variable for row in row_variables for variable in row]
    poly = sp.Poly(sp.expand(polynomial), *variables)
    positions = {variable: i for i, variable in enumerate(variables)}
    monomial_coefficient = sp.Integer(0)
    for exponents, coefficient in poly.terms():
        factor = coefficient
        possible = True
        for row, alpha in zip(row_variables, target):
            old = tuple(exponents[positions[variable]] for variable in row)
            missing = degree - sum(old)
            increment = tuple(alpha[i] - old[i] for i in range(len(row)))
            if min(increment) < 0 or sum(increment) != missing:
                possible = False
                break
            factor *= multinomial(increment)
        if possible:
            monomial_coefficient += factor
    denominator = 1
    for alpha in target:
        denominator *= multinomial(alpha)
    return sp.factor(monomial_coefficient / denominator)


def product_simplex_obstruction():
    n = 4
    row_variables = []
    P = []
    for i in range(n):
        row = []
        matrix_row = []
        for j in range(n):
            if i == j:
                matrix_row.append(0)
            else:
                variable = sp.symbols(f"p{i}{j}")
                row.append(variable)
                matrix_row.append(variable)
        row_variables.append(tuple(row))
        P.append(matrix_row)
    states, kernel = raw_sympy_active(P)
    nu = sp.Matrix([[sp.Rational(B.bit_count(), 48) for B, _ in states]])
    H = sp.Matrix([sp.Rational(1, B.bit_count()) for B, _ in states])
    observable = H
    for _ in range(3):
        observable = kernel * observable
    raw_reward = sp.expand((nu * observable)[0])
    row_sums = [sum(row) for row in row_variables]
    # Elevation is performed term by term below.  Represent the baseline as
    # a constant polynomial; the helper supplies all missing row degrees.
    polynomial = raw_reward - sp.Rational(7, 12)
    negative_index = ((0, 0, 3), (0, 1, 2), (1, 1, 1), (1, 1, 1))
    symmetric_index = ((1, 1, 1),) * 4
    # The raw transition polynomial is evaluated on row sums one.  To make
    # the constant subtraction compatible with the same elevation, no
    # explicit product of row_sums is needed in this representation.
    assert all(len(row) == 3 for row in row_variables) and len(row_sums) == 4
    first = elevated_product_simplex_coefficient(polynomial, row_variables, negative_index)
    second = elevated_product_simplex_coefficient(polynomial, row_variables, symmetric_index)
    assert first == -sp.Rational(11, 5184)
    assert second == -sp.Rational(187, 3456)
    print("PASS: exact negative raw product-simplex Bernstein coefficients")


def flint_active(weights):
    n = len(weights)
    degrees = [sum(row) for row in weights]
    if any(degree <= 0 for degree in degrees):
        raise ValueError("zero row")
    P = [[Q(weights[i][j], degrees[i]) for j in range(n)] for i in range(n)]
    states = [
        (B, v) for v in range(n) for B in range(1, 1 << n)
        if not B >> v & 1
    ]
    index = {state: i for i, state in enumerate(states)}
    kernel = fmpq_mat(len(states), len(states))
    for source, (B, v) in enumerate(states):
        k = B.bit_count()
        for i, probability in enumerate(P[v]):
            if probability:
                kernel[source, index[B | (1 << i), v]] += probability / 2
        for w in range(n):
            if B >> w & 1:
                C = B & ~(1 << w)
                for i, probability in enumerate(P[w]):
                    if probability:
                        kernel[source, index[C | (1 << i), w]] += probability / (2 * k)
        assert sum((kernel[source, target] for target in range(len(states))), Q(0)) == 1
    return states, kernel


def reference_vectors(states, n):
    denominator = n * (n - 1) * 2 ** (n - 2)
    nu = fmpq_mat(1, len(states), [
        Q(B.bit_count(), denominator) for B, _ in states
    ])
    H = fmpq_mat(len(states), 1, [Q(1, B.bit_count()) for B, _ in states])
    return nu, H, (nu * H)[0, 0]


def bernstein_from_values(values):
    degree = len(values) - 1
    differences = []
    row = values
    while row:
        differences.append(row[0])
        row = [row[i + 1] - row[i] for i in range(len(row) - 1)]
    power = [Q(0) for _ in range(degree + 1)]
    binomial_basis = [Q(1)]
    for j in range(degree + 1):
        for k, value in enumerate(binomial_basis):
            power[k] += differences[j] * value
        next_basis = [Q(0) for _ in range(len(binomial_basis) + 1)]
        for k, value in enumerate(binomial_basis):
            next_basis[k] -= Q(j, j + 1) * value
            next_basis[k + 1] += Q(1, j + 1) * value
        binomial_basis = next_basis
    return [
        sum(
            (power[j] * Q(comb(k, j), comb(degree, j)) for j in range(k + 1)),
            Q(0),
        )
        for k in range(degree + 1)
    ]


def complete_ray_bernstein(weights, time):
    n = len(weights)
    complete_weights = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
    states, actual = flint_active(weights)
    complete_states, complete = flint_active(complete_weights)
    assert states == complete_states
    nu, H, baseline = reference_vectors(states, n)
    direction = actual - complete
    values = []
    for alpha in range(time + 1):
        observable = H
        interpolated = complete + alpha * direction
        for _ in range(time):
            observable = interpolated * observable
        values.append((nu * observable)[0, 0] - baseline)
    return bernstein_from_values(values)


def complete_ray_bernstein_recurrence(weights, final_time):
    n = len(weights)
    complete_weights = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
    states, actual = flint_active(weights)
    complete_states, complete = flint_active(complete_weights)
    assert states == complete_states
    nu, H, baseline = reference_vectors(states, n)
    controls = [H]
    answer = [[Q(0)]]
    for step in range(final_time):
        degree = step + 1
        next_controls = []
        for j in range(degree + 1):
            vector = fmpq_mat(len(states), 1)
            if j <= step:
                vector += Q(degree - j, degree) * complete * controls[j]
            if j:
                vector += Q(j, degree) * actual * controls[j - 1]
            next_controls.append(vector)
        controls = next_controls
        answer.append([(nu * vector)[0, 0] - baseline for vector in controls])
    return answer


def symmetric_weights(n, values):
    weights = [[0 for _ in range(n)] for _ in range(n)]
    for value, (i, j) in zip(values, combinations(range(n), 2)):
        weights[i][j] = weights[j][i] = value
    return weights


def direct_floor_check(weights, final_time=50):
    states, kernel = flint_active(weights)
    nu, H, baseline = reference_vectors(states, len(weights))
    law = nu
    for time in range(final_time + 1):
        gap = (law * H)[0, 0] - baseline
        assert gap == 0 if time in (0, 1) else gap > 0
        law = law * kernel


def exact_finite_screens():
    boundary_counts = {}
    for n in (3, 4):
        choices = [[j for j in range(n) if j != i] for i in range(n)]
        tested = 0
        for targets in product(*choices):
            weights = [[0 for _ in range(n)] for _ in range(n)]
            for i, target in enumerate(targets):
                weights[i][target] = 1
            direct_floor_check(weights)
            tested += 1
        boundary_counts[f"deterministic-n{n}"] = tested

    n = 4
    supports = [list(combinations([j for j in range(n) if j != i], 2)) for i in range(n)]
    tested = 0
    for rows in product(*supports):
        weights = [[0 for _ in range(n)] for _ in range(n)]
        for i, support in enumerate(rows):
            for target in support:
                weights[i][target] = 1
        direct_floor_check(weights)
        tested += 1
    boundary_counts["two-support-n4"] = tested

    rng = Random(26080813)
    bernstein_counts = {}
    for n, count in ((4, 8), (5, 5)):
        for kind in ("reversible", "directed"):
            tested = 0
            for _ in range(count):
                if kind == "reversible":
                    values = [rng.choice((1, 2, 7, 100)) for _ in combinations(range(n), 2)]
                    weights = symmetric_weights(n, values)
                else:
                    weights = [
                        [0 if i == j else rng.choice((1, 2, 7, 100)) for j in range(n)]
                        for i in range(n)
                    ]
                controls = complete_ray_bernstein_recurrence(weights, 30)
                for time in range(2, 31):
                    coefficients = controls[time]
                    assert coefficients[0] == coefficients[1] == 0
                    assert all(value >= 0 for value in coefficients[2:])
                # Independent polynomial interpolation agrees at a
                # representative nontrivial degree.
                assert controls[12] == complete_ray_bernstein(weights, 12)
                tested += 1
            bernstein_counts[f"{kind}-n{n}"] = tested
    print("PASS: exact transient boundary floor screen", boundary_counts)
    print("PASS: exact complete-ray Bernstein screen", bernstein_counts, "times 2..30")
    print("OPEN: universal transient baseline floor and Bernstein positivity")


def convexity_obstruction():
    weights = symmetric_weights(
        5,
        (2, 1233002, 865, 13228210, 1106078, 12, 1130, 56225120, 385413, 2),
    )
    complete_weights = [[0 if i == j else 1 for j in range(5)] for i in range(5)]
    states, actual = flint_active(weights)
    _, complete = flint_active(complete_weights)
    nu, H, _ = reference_vectors(states, 5)
    direction = actual - complete
    value = H
    first = fmpq_mat(len(states), 1)
    second = fmpq_mat(len(states), 1)
    for _ in range(18):
        second = actual * second + 2 * direction * first
        first = actual * first + direction * value
        value = actual * value
    curvature = (nu * second)[0, 0]
    assert curvature < 0
    controls = complete_ray_bernstein_recurrence(weights, 18)
    coefficients = controls[18]
    assert coefficients == complete_ray_bernstein(weights, 18)
    assert coefficients[0] == coefficients[1] == 0
    assert all(value > 0 for value in coefficients[2:])
    print("PASS: exact reversible n=5 complete-ray convexity counterexample")
    print("PASS: same degree-18 ray polynomial has nonnegative Bernstein coefficients")


def colour_count_monotonicity_obstruction():
    """Exact positive ray whose final two controls decrease."""

    targets = (1, 0, 0, 4, 3)
    weights = [[0 for _ in targets] for _ in targets]
    for source, target in enumerate(targets):
        weights[source][target] = 1
    coefficients = complete_ray_bernstein_recurrence(weights, 28)[28]
    assert all(value > 0 for value in coefficients[2:])
    assert coefficients[27] == Q(
        5419433765256640517224634078697766406321,
        41300141969359454129500389108526885109760,
    )
    assert coefficients[28] == Q(
        128473916356718592969158918814619542013,
        983336713556177479273818788298259169280,
    )
    assert coefficients[28] - coefficients[27] == -Q(
        4705855654891922503991897696749128355,
        8260028393871890825900077821705377021952,
    )
    print("PASS: exact positive n=5 ray with nonmonotone colour-count controls")


def main():
    triangle_certificates()
    product_simplex_obstruction()
    convexity_obstruction()
    colour_count_monotonicity_obstruction()
    exact_finite_screens()


if __name__ == "__main__":
    main()
