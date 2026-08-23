#!/usr/bin/env python3
"""Exact certificates and hostile screens for complete-refresh forests.

The symbolic triangle calculation is a proof certificate at order three.
The rational order-four/five screens are finite evidence only.
"""

from __future__ import annotations

from itertools import combinations
from math import comb
from random import Random

import sympy as sp
from flint import fmpq as Q, fmpq_mat


class CertificateFailure(RuntimeError):
    """Raised when an explicit certificate check fails."""


def require(condition, detail="certificate check failed"):
    """Raise a failure that remains active under optimized Python."""
    if not condition:
        raise CertificateFailure(str(detail))


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
        for i in range(n):
            if P[v][i]:
                kernel[source, index[B | (1 << i), v]] += P[v][i] / 2
        for w in range(n):
            if B >> w & 1:
                C = B & ~(1 << w)
                for i in range(n):
                    if P[w][i]:
                        kernel[source, index[C | (1 << i), w]] += P[w][i] / (2 * k)
        require(sp.factor(sum(kernel[source, j] for j in range(len(states)))) == 1)
    return states, kernel


def bernstein_from_power(coefficients):
    degree = len(coefficients) - 1
    return [
        sp.factor(sum(
            coefficients[j] * sp.binomial(k, j) / sp.binomial(degree, j)
            for j in range(k + 1)
        ))
        for k in range(degree + 1)
    ]


def triangle_certificate():
    a, b, c, alpha = sp.symbols("a b c alpha", positive=True)
    weights = ((0, a, b), (a, 0, c), (b, c, 0))
    P = [
        [sp.Integer(0) if i == j else weights[i][j] / sum(weights[i])
         for j in range(3)]
        for i in range(3)
    ]
    P0 = [
        [sp.Integer(0) if i == j else sp.Rational(1, 2) for j in range(3)]
        for i in range(3)
    ]
    states, kernel = sympy_active(P)
    complete_states, complete = sympy_active(P0)
    require(states == complete_states and len(states) == 9)
    interpolated = (1 - alpha) * complete + alpha * kernel
    laplacian = sp.eye(len(states)) - interpolated
    q = sp.Matrix([
        sp.Rational(1, B.bit_count()) - sp.Rational(3, 4) for B, _ in states
    ])
    nu0 = sp.Matrix([[
        sp.Rational(B.bit_count(), 12) for B, _ in states
    ]])
    numerator, denominator = sp.cancel(
        (laplacian + q * nu0).det(method="domain-ge")
    ).as_numer_denom()
    require(sp.factor(denominator) == (
        65536 * (a + b) ** 2 * (a + c) ** 2 * (b + c) ** 2
    ))
    polynomial = sp.Poly(numerator, alpha)
    require(polynomial.degree() == 6)
    power = [polynomial.coeff_monomial(alpha**j) for j in range(7)]
    bernstein = bernstein_from_power(power)
    require(bernstein[0] == bernstein[1] == 0)

    x, y, z = sp.symbols("x y z")
    table = {
        2: (0, sp.Rational(396, 5), sp.Rational(913, 15),
            sp.Rational(55, 3), sp.Rational(913, 15)),
        3: (0, sp.Rational(1332, 5), sp.Rational(913, 5),
            sp.Rational(131, 5), sp.Rational(913, 5)),
        4: (0, sp.Integer(588), sp.Rational(5468, 15),
            sp.Rational(8, 3), sp.Rational(5324, 15)),
        5: (sp.Rational(196, 3), sp.Rational(3008, 3),
            sp.Rational(1816, 3), 0, sp.Integer(492)),
        6: (sp.Integer(192), sp.Integer(1536), sp.Integer(912),
            0, sp.Integer(576)),
    }

    def qpoly(j, first, second, third):
        A, B, C, D, E = table[j]
        return (
            A * first**2 * second**2
            + B * first * second * (first + second) * third
            + C * first * second * third**2
            + D * (first + second) * third**3
            + E * third**4
        )

    for j in range(2, 7):
        certificate = sp.expand(
            (a - b) ** 2 * qpoly(j, a, b, c)
            + (b - c) ** 2 * qpoly(j, b, c, a)
            + (c - a) ** 2 * qpoly(j, c, a, b)
        )
        require(sp.expand(bernstein[j] - certificate) == 0)
        require(all(value >= 0 for value in table[j]))
    print("PASS: symbolic triangle complete-refresh determinant")
    print("PASS: every nonzero Bernstein coefficient has a centered positive certificate")


def flint_active(weights):
    n = len(weights)
    degrees = [sum(row) for row in weights]
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
        require(sum((kernel[source, j] for j in range(len(states))), Q(0)) == 1)
    return states, kernel


def exact_polynomial_values(weights):
    n = len(weights)
    complete_weights = [
        [0 if i == j else 1 for j in range(n)] for i in range(n)
    ]
    states, kernel = flint_active(weights)
    complete_states, complete = flint_active(complete_weights)
    require(states == complete_states)
    size = len(states)
    identity = fmpq_mat(size, size, [
        int(i == j) for i in range(size) for j in range(size)
    ])
    base = identity - complete
    direction = complete - kernel
    c0 = Q(2 ** (n - 1) - 1, (n - 1) * 2 ** (n - 2))
    nu_denominator = n * (n - 1) * 2 ** (n - 2)
    for i, (B, _) in enumerate(states):
        q = Q(1, B.bit_count()) - c0
        for j, (C, _) in enumerate(states):
            base[i, j] += q * Q(C.bit_count(), nu_denominator)
    return [(base + value * direction).det() for value in range(size)]


def exact_bernstein(weights):
    values = exact_polynomial_values(weights)
    differences = []
    row = values
    while row:
        differences.append(row[0])
        row = [row[i + 1] - row[i] for i in range(len(row) - 1)]
    degree = max((i for i, value in enumerate(differences) if value), default=-1)
    if degree < 0:
        return []

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

    bernstein = [
        sum(
            (power[j] * Q(comb(k, j), comb(degree, j)) for j in range(k + 1)),
            Q(0),
        )
        for k in range(degree + 1)
    ]
    require(bernstein[-1] == values[1])
    return bernstein


def symmetric_weights(n, values):
    weights = [[0 for _ in range(n)] for _ in range(n)]
    for value, (i, j) in zip(values, combinations(range(n), 2)):
        weights[i][j] = weights[j][i] = value
    return weights


def connected(weights):
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for u, value in enumerate(weights[v]):
            if value and u not in seen:
                seen.add(u)
                stack.append(u)
    return len(seen) == len(weights)


def finite_screen():
    rng = Random(26080841)
    alphabet = (0, 0, 1, 2, 7, 100, 10000)
    counts = {}
    for n, target in ((4, 12), (5, 12)):
        tested = 0
        while tested < target:
            values = [rng.choice(alphabet) for _ in range(n * (n - 1) // 2)]
            weights = symmetric_weights(n, values)
            if not connected(weights):
                continue
            coefficients = exact_bernstein(weights)
            require(coefficients[0] == coefficients[1] == 0)
            require(all(value >= 0 for value in coefficients))
            require(coefficients[-1] > 0)
            tested += 1
        counts[f"reversible-n{n}"] = tested

    # Directed kernels are outside the graph theorem, but are a useful
    # diagnostic of whether reversibility is already needed by this route.
    for n, target in ((4, 6), (5, 6)):
        for _ in range(target):
            weights = [
                [0 if i == j else rng.choice((1, 2, 7, 100, 10000))
                 for j in range(n)]
                for i in range(n)
            ]
            coefficients = exact_bernstein(weights)
            require(coefficients[0] == coefficients[1] == 0)
            require(all(value >= 0 for value in coefficients))
        counts[f"directed-n{n}"] = target
    print("PASS: exact finite Bernstein screen", counts)
    print("OPEN: arbitrary-order positivity of all complete-refresh forest coefficients")


def main():
    triangle_certificate()
    finite_screen()


if __name__ == "__main__":
    main()
