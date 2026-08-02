#!/usr/bin/env python3
"""Independent exact checks for DENSE_PROTECTED_STATE_NO_GO.md.

The verifier rebuilds the complete 2^k-1 dB colony system from the local
update rates, differentiates it exactly at epsilon=0, solves the consistency
equation, and compares the uniform second coefficient with formula (19).
It also checks the partner Bd series symbolically.
"""

from __future__ import annotations

import sympy as sp


def exact_db_instance(weights, fitness):
    k = len(weights); r = sp.Rational(*fitness); e = sp.symbols("epsilon")
    Q1, Q2 = sp.symbols("Q1 Q2"); q0 = 1 / r
    A = sp.Matrix(weights)
    Z = e * A
    degree = [sum(Z[i, j] for j in range(k)) for i in range(k)]
    inv = [1 / (1 + degree[i]) for i in range(k)]
    H = sum(inv) / k
    Q = q0 + Q1 * e + Q2 * e**2
    states = list(range(1, 1 << k)); index = {mask: i for i, mask in enumerate(states)}
    matrix = sp.zeros(len(states)); rhs = sp.zeros(len(states), 1)

    for mask in states:
        row = index[mask]
        mutant = [(mask >> i) & 1 for i in range(k)]
        rates = {}
        for v in range(k):
            mutant_mass = sum(Z[u, v] for u in range(k) if mutant[u] and u != v)
            resident_mass = 1 + sum(Z[u, v] for u in range(k) if not mutant[u] and u != v)
            denominator = r * mutant_mass + resident_mass
            if not mutant[v] and mutant_mass:
                rates[mask | (1 << v)] = r * mutant_mass / denominator
            elif mutant[v] and resident_mass:
                rates[mask & ~(1 << v)] = resident_mass / denominator
        external = sum(mutant) * r * H
        matrix[row, row] = sum(rates.values()) + external * (1 - Q)
        for target, rate in rates.items():
            if target == 0:
                rhs[row] += rate
            else:
                matrix[row, index[target]] -= rate

    coefficient = lambda value, order: sp.diff(value, e, order).subs(e, 0) / sp.factorial(order)
    matrices = [matrix.applyfunc(lambda value, j=j: sp.cancel(coefficient(value, j))) for j in range(3)]
    vectors = [rhs.applyfunc(lambda value, j=j: sp.cancel(coefficient(value, j))) for j in range(3)]
    v0 = sp.Matrix([r ** (-bin(mask).count("1")) for mask in states])
    assert matrices[0] * v0 == vectors[0]

    v1 = matrices[0].inv() * (vectors[1] - matrices[1] * v0)
    singles = [index[1 << i] for i in range(k)]
    child_numerator = sum(inv[i] * (v0[singles[i]] + e * v1[singles[i]]) for i in range(k))
    first_equation = coefficient(child_numerator / sum(inv) - Q, 1)
    first_solution = sp.solve(first_equation, Q1)[0]
    assert first_solution == 0
    v1 = sp.simplify(v1.subs(Q1, first_solution))

    v2 = matrices[0].inv() * (
        vectors[2]
        - matrices[1].subs(Q1, first_solution) * v1
        - matrices[2].subs(Q1, first_solution) * v0
    )
    child_numerator = sum(
        inv[i] * (v0[singles[i]] + e * v1[singles[i]] + e**2 * v2[singles[i]])
        for i in range(k)
    )
    second_equation = coefficient(child_numerator / sum(inv) - Q, 2)
    second_solution = sp.solve(second_equation, Q2)[0]
    v2 = sp.simplify(v2.subs(Q2, second_solution))
    observed = sp.factor(sum(v2[singles[i]] for i in range(k)) / k)

    unscaled_degree = [sum(A[i, j] for j in range(k)) for i in range(k)]
    mean_degree = sum(unscaled_degree) / k
    variance = sum((value - mean_degree) ** 2 for value in unscaled_degree) / k
    edge_square = sum(A[i, j] ** 2 for i in range(k) for j in range(i + 1, k))
    predicted = sp.factor((r - 1) / r**2 * (variance + 2 * (r - 1) * edge_square / k))
    assert sp.simplify(observed - predicted) == 0
    return observed


def verify_partner_bd():
    e, a, mu, nu, kappa, r = sp.symbols("e a mu nu kappa r", positive=True)
    p = (r - 1) / r
    H = 1 - mu * e + nu * e**2 - kappa * e**3
    T1, T2, T3 = sp.symbols("T1 T2 T3")
    T = p + T1 * e + T2 * e**2 + T3 * e**3
    x = 1 / (1 + e * a); h = 1 - x
    ratio = H / (H + r * x * T)
    q1 = (H + h) / (H + h + r * h + r * x * T - r * h * ratio)
    series = sp.series(q1, e, 0, 4).removeO().expand()

    moments = {0: 1, 1: mu, 2: nu, 3: kappa}
    polynomial = sp.Poly(series, a)
    average_q = sum(coefficient * moments[power[0]] for power, coefficient in polynomial.terms())
    residual = sp.expand(1 - average_q - T)
    solutions = {}
    for order, unknown in enumerate((T1, T2, T3), 1):
        equation = sp.expand(residual.subs(solutions)).coeff(e, order)
        solutions[unknown] = sp.factor(sp.solve(equation, unknown)[0])
    assert solutions[T1] == 0
    assert solutions[T2] == 0
    expected = -(r - 1) * (mu**3 - 3 * mu * nu + 2 * kappa) / r**3
    assert sp.simplify(solutions[T3] - expected) == 0
    return expected


def main():
    instances = [
        ([[0, 2], [2, 0]], (3, 2)),
        ([[0, 1, 2], [1, 0, 3], [2, 3, 0]], (7, 5)),
        ([[0, 1, 2, 1], [1, 0, 3, 1], [2, 3, 0, 2], [1, 1, 2, 0]], (3, 2)),
    ]
    for weights, fitness in instances:
        value = exact_db_instance(weights, fitness)
        print(f"exact dB k={len(weights)} r={fitness[0]}/{fitness[1]} coefficient={value}")
    print("partner Bd cubic:", verify_partner_bd())
    print("all dense protected-state certificates passed")


if __name__ == "__main__":
    main()
