#!/usr/bin/env python3
"""Exact verifier for the complementary two-channel entrance obstruction."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def labelled_db_fixation(weights: list[list[sp.Rational]], fitness: sp.Rational):
    """Solve the full labelled dB chain exactly from the update definition."""
    n = len(weights)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {mask: row for row, mask in enumerate(states)}
    matrix = sp.zeros(len(states))
    rhs = sp.zeros(len(states), 1)

    for mask, row in index.items():
        moves: dict[int, sp.Expr] = {}
        for target in range(n):
            denominator = sp.Integer(0)
            mutant_mass = sp.Integer(0)
            for parent in range(n):
                if parent == target or not weights[target][parent]:
                    continue
                parent_fitness = fitness if mask & (1 << parent) else 1
                mass = parent_fitness * weights[target][parent]
                denominator += mass
                if mask & (1 << parent):
                    mutant_mass += mass
            assert denominator > 0
            target_mutant = bool(mask & (1 << target))
            mutant_probability = mutant_mass / denominator
            if target_mutant:
                probability = 1 - mutant_probability
                next_mask = mask ^ (1 << target)
            else:
                probability = mutant_probability
                next_mask = mask ^ (1 << target)
            if probability:
                moves[next_mask] = moves.get(next_mask, 0) + probability

        changing_rate = sp.factor(sum(moves.values()))
        assert changing_rate > 0
        matrix[row, row] = changing_rate
        for next_mask, rate in moves.items():
            if next_mask == full:
                rhs[row] += rate
            elif next_mask:
                matrix[row, index[next_mask]] -= rate

    solution = matrix.inv() * rhs
    assert matrix * solution == rhs
    return [sp.factor(solution[index[1 << vertex]]) for vertex in range(n)]


def entrance_data(weights: list[list[sp.Rational]], fitness: sp.Rational):
    """Return exact temperatures, expansion rates, and first-gain bounds."""
    n = len(weights)
    degrees = [sum(row) for row in weights]
    assert all(degree > 0 for degree in degrees)
    temperatures = []
    expansion_rates = []
    first_gain = []
    for vertex in range(n):
        temperature = sum(
            weights[target][vertex] / degrees[target] for target in range(n)
        )
        beta = sum(
            fitness * weights[target][vertex]
            / (degrees[target] + (fitness - 1) * weights[target][vertex])
            for target in range(n)
            if target != vertex and weights[target][vertex]
        )
        temperatures.append(sp.factor(temperature))
        expansion_rates.append(sp.factor(beta))
        first_gain.append(sp.factor(beta / (1 + beta)))
        assert sp.factor(beta - fitness * temperature) <= 0
    assert sp.factor(sum(temperatures) - n) == 0
    return temperatures, expansion_rates, first_gain


def exact_graph_checks() -> None:
    graph_list = [
        # Complete rational graph of order four.
        [
            [0, 1, 2, 3],
            [1, 0, 4, 1],
            [2, 4, 0, 5],
            [3, 1, 5, 0],
        ],
        # Connected incomplete support of order five.
        [
            [0, 2, 0, 0, 7],
            [2, 0, 3, 0, 0],
            [0, 3, 0, 5, 1],
            [0, 0, 5, 0, 4],
            [7, 0, 1, 4, 0],
        ],
    ]
    fitness = sp.Rational(19, 10)
    for raw in graph_list:
        weights = [[sp.Rational(value) for value in row] for row in raw]
        n = len(weights)
        assert weights == [list(row) for row in zip(*weights)]
        fixation = labelled_db_fixation(weights, fitness)
        temperatures, _, first_gain = entrance_data(weights, fitness)
        for value, bound in zip(fixation, first_gain):
            assert sp.factor(bound - value) >= 0

        # Check the finite subset-density inequality for every nonempty B.
        for order in range(1, n + 1):
            delta = sp.Rational(order, n)
            envelope = sp.factor(delta * fitness / (fitness + delta))
            for subset in combinations(range(n), order):
                lhs = sp.factor(sum(fixation[v] for v in subset) / n)
                assert sp.factor(envelope - lhs) >= 0
                # Independent Jensen check at the first-gain relaxation.
                temp_mass = sum(temperatures[v] for v in subset)
                assert temp_mass <= n
                relaxed = sum(
                    fitness * temperatures[v] / (1 + fitness * temperatures[v])
                    for v in subset
                ) / n
                assert sp.factor(envelope - relaxed) >= 0


def symbolic_checks() -> None:
    r, delta = sp.symbols("r delta", positive=True)
    p = (r - 1) / r
    envelope = delta * r / (r + delta)

    # The complementary split has delta <= 1/r; the envelope is increasing.
    assert sp.factor(sp.diff(envelope, delta)) == r**2 / (delta + r) ** 2
    optimized = sp.factor(envelope.subs(delta, 1 / r))
    assert optimized == r / (r**2 + 1)
    cubic = r**3 - 2 * r**2 + r - 1
    assert sp.factor(optimized - p + cubic / (r * (r**2 + 1))) == 0

    equal_split = sp.factor(envelope.subs(delta, sp.Rational(1, 2)))
    assert equal_split == r / (2 * r + 1)
    assert sp.factor(
        equal_split - p + (r**2 - r - 1) / (r * (2 * r + 1))
    ) == 0

    # Sturm/root isolation: the cubic has one real root, in this rational box.
    polynomial = sp.Poly(cubic, r, domain=sp.QQ)
    intervals = sp.polys.polytools.intervals(polynomial, eps=sp.Rational(1, 10**14))
    real_intervals = [(interval, multiplicity) for interval, multiplicity in intervals]
    assert len(real_intervals) == 1
    (left, right), multiplicity = real_intervals[0]
    assert multiplicity == 1
    assert sp.Rational(1754877666246, 10**12) < left
    assert right < sp.Rational(1754877666248, 10**12)
    assert polynomial.count_roots(-sp.oo, sp.oo) == 1


def main() -> None:
    exact_graph_checks()
    symbolic_checks()
    print("PASS exact two-channel entrance and threshold obstruction")


if __name__ == "__main__":
    main()
