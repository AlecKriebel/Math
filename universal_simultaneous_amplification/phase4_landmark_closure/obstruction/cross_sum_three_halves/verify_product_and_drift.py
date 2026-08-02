#!/usr/bin/env python3
"""Exact certificates for the r=3/2 product route.

The program independently builds both transient triangle chains, proves the
24-atom product certificate, derives the complete dB harmonic recurrence,
and checks the arbitrary-graph drift decomposition over exact rational test
graphs and every nonabsorbing subset.  The finite graph checks audit the
generic algebra stated in the companion note; they are not enumeration
proofs for arbitrary order.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import permutations

import sympy as sp


R = sp.Rational(3, 2)
Q = sp.Rational(2, 3)
a, b, c = sp.symbols("a b c", positive=True)
VARIABLES = (a, b, c)


PRODUCT_CERTIFICATE = (
    ((0, 8, 8), 23961600),
    ((1, 4, 11), 143941632),
    ((1, 5, 10), 304522368),
    ((1, 10, 5), 35376000),
    ((2, 3, 11), 765223790),
    ((2, 4, 10), 2788895530),
    ((2, 6, 8), 217850280),
    ((2, 10, 4), 108379200),
    ((3, 6, 7), 15499192114),
    ((3, 10, 3), 77685696),
    ((4, 5, 7), 35162406304),
    ((4, 9, 3), 2449641334),
    ((5, 5, 6), 2173492555),
    ((5, 6, 5), 296158016),
    ((5, 7, 4), 8036318240),
    ((5, 8, 3), 14235460288),
    ((5, 9, 2), 339267274),
    ((6, 6, 4), 7913106050),
    ((6, 7, 3), 29892232002),
    ((6, 9, 1), 37508384),
    ((6, 10, 0), 4322304),
    ((7, 7, 2), 192937375),
    ((7, 9, 0), 24804608),
    ((8, 8, 0), 14827456),
)


def triangle_fixation(rule: str) -> sp.Expr:
    weights = ((0, a, b), (a, 0, c), (b, c, 0))
    degree = [sum(row) for row in weights]
    states = list(range(1, 7))
    index = {state: row for row, state in enumerate(states)}
    matrix = sp.eye(6)
    rhs = sp.zeros(6, 1)
    for state in states:
        mutant = [(state >> i) & 1 for i in range(3)]
        transitions = defaultdict(lambda: sp.Integer(0))
        if rule == "Bd":
            total_fitness = 3 + (R - 1) * sum(mutant)
            for parent in range(3):
                for target in range(3):
                    if parent == target:
                        continue
                    probability = (
                        (R if mutant[parent] else 1)
                        * weights[parent][target]
                        / (total_fitness * degree[parent])
                    )
                    new_state = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transitions[new_state] += probability
        elif rule == "dB":
            for target in range(3):
                denominator = sum(
                    weights[parent][target] * (R if mutant[parent] else 1)
                    for parent in range(3)
                )
                for parent in range(3):
                    if parent == target:
                        continue
                    probability = (
                        weights[parent][target]
                        * (R if mutant[parent] else 1)
                        / (3 * denominator)
                    )
                    new_state = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transitions[new_state] += probability
        else:
            raise ValueError(rule)
        row = index[state]
        for target, probability in transitions.items():
            if target == 7:
                rhs[row] += probability
            elif target:
                matrix[row, index[target]] -= probability
    solution = next(iter(sp.linsolve((matrix, rhs))))
    return sp.cancel(sum(solution[index[1 << i]] for i in range(3)) / 3)


def certificate_polynomial() -> sp.Expr:
    result = 0
    for (i, j, k), coefficient in PRODUCT_CERTIFICATE:
        assert coefficient > 0
        result += coefficient * sum(
            x**i * y**j * z**k * (x - y) ** 2
            for x, y, z in permutations(VARIABLES)
        )
    return sp.expand(result)


def phi_db(n: int, k: int) -> sp.Rational:
    return sp.cancel(
        (n - (sp.Rational(n) + sp.Rational(k, 2)) * Q**k)
        / (n * (1 - Q ** (n - 1)))
    )


def verify_complete_harmonic() -> None:
    for n in range(2, 21):
        assert phi_db(n, 0) == 0
        assert phi_db(n, n) == 1
        for k in range(1, n):
            up = sp.Rational(n - k) * R * k / (R * k + n - k - 1)
            down = sp.Rational(k * (n - k)) / (R * (k - 1) + n - k)
            drift = up * (phi_db(n, k + 1) - phi_db(n, k))
            drift += down * (phi_db(n, k - 1) - phi_db(n, k))
            assert sp.cancel(drift) == 0
        complete = sp.Rational(n - 1, n) * (1 - 1 / R) / (
            1 - R ** (-(n - 1))
        )
        assert sp.cancel(phi_db(n, 1) - complete) == 0


def verify_drift_decomposition(weights: list[list[int]]) -> int:
    n = len(weights)
    degree = [sum(map(sp.Rational, row)) for row in weights]
    transition = [
        [sp.Rational(weights[i][j], degree[i]) for j in range(n)]
        for i in range(n)
    ]
    temperature = [sum(transition[i][j] for i in range(n)) for j in range(n)]
    checks = 0
    for state in range(1, (1 << n) - 1):
        k = bin(state).count("1")
        mutant = [bool(state & (1 << i)) for i in range(n)]
        x = [
            sum(transition[i][j] for j in range(n) if mutant[j])
            for i in range(n)
        ]
        assert sum(x) == sum(temperature[j] for j in range(n) if mutant[j])
        alpha = sp.Rational(k, n - 1)
        beta = sp.Rational(k - 1, n - 1)
        a_k = sp.Rational(n) + sp.Rational(k, 2) - 1
        a_prev = sp.Rational(n) + sp.Rational(k, 2) - sp.Rational(3, 2)
        c_r = sp.cancel(4 * a_k / (2 + alpha) ** 2)
        c_m = sp.cancel(6 * a_prev / (2 + beta) ** 2)
        direct = a_k * sum(
            x[i] / (1 + x[i] / 2) for i in range(n) if not mutant[i]
        )
        direct -= a_prev * sum(
            (1 - x[i]) / (1 + x[i] / 2) for i in range(n) if mutant[i]
        )
        total_defect = sum(x) - k
        row_cut = sum(x[i] for i in range(n) if not mutant[i])
        complete_cut = sp.Rational(k * (n - k), n - 1)
        dispersion = c_r * sum(
            (x[i] - alpha) ** 2 / (2 + x[i])
            for i in range(n)
            if not mutant[i]
        )
        dispersion += c_m * sum(
            (x[i] - beta) ** 2 / (2 + x[i])
            for i in range(n)
            if mutant[i]
        )
        decomposed = (
            c_m * total_defect
            - (c_m - c_r) * (row_cut - complete_cut)
            - dispersion
        )
        assert sp.cancel(direct - decomposed) == 0
        assert c_m - c_r > 0
        assert dispersion >= 0
        checks += 1
    return checks


def main() -> None:
    rho_bd = triangle_fixation("Bd")
    rho_db = triangle_fixation("dB")
    complete_bd = (1 - 1 / R) / (1 - R**-3)
    complete_db = sp.Rational(2, 3) * (1 - 1 / R) / (1 - R**-2)
    gap = sp.cancel(complete_bd * complete_db - rho_bd * rho_db)
    numerator, denominator = map(sp.expand, sp.fraction(gap))
    assert all(
        coefficient > 0
        for _, coefficient in sp.Poly(denominator, *VARIABLES).terms()
    )
    assert sp.Poly(numerator - certificate_polynomial(), *VARIABLES).is_zero
    first_atom = sum(
        x**0 * y**8 * z**8 * (x - y) ** 2
        for x, y, z in permutations(VARIABLES)
    )
    assert sp.expand(
        first_atom
        - (
            c**8 * (a**8 + b**8) * (a - b) ** 2
            + b**8 * (a**8 + c**8) * (a - c) ** 2
            + a**8 * (b**8 + c**8) * (b - c) ** 2
        )
    ) == 0

    verify_complete_harmonic()
    graphs = (
        [[0, 1, 4], [1, 0, 2], [4, 2, 0]],
        [[0, 2, 0, 5], [2, 0, 3, 1], [0, 3, 0, 4], [5, 1, 4, 0]],
        [
            [0, 1, 0, 0, 7],
            [1, 0, 2, 0, 3],
            [0, 2, 0, 5, 0],
            [0, 0, 5, 0, 4],
            [7, 3, 0, 4, 0],
        ],
    )
    checks = sum(verify_drift_decomposition(graph) for graph in graphs)
    print("PASS: exact Bd and dB triangle absorbing chains constructed")
    print("PASS: product numerator equals 24-atom nonnegative certificate")
    print("PASS: positive triangle equality occurs only at equal weights")
    print("PASS: complete dB harmonic recurrence checked for 2 <= n <= 20")
    print(f"PASS: arbitrary-graph drift decomposition checked on {checks} states")


if __name__ == "__main__":
    main()
