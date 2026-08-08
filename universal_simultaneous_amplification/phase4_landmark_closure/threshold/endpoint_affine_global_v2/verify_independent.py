#!/usr/bin/env python3
"""Independent exact labelled-event audit of the endpoint counterexample.

This implementation uses actual discrete-time update probabilities and
SymPy's DomainMatrix solver.  It shares neither the time-changed rates nor
the FLINT solve used by ``verify_exact_counterexample.py``.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction as F

from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix


R = F(3, 2)
A, B = 2, 20
N = A + B
U, V, E = F(137), F(1), F(1, 500)
EXPECTED = {
    "Bd": "5fa981402c7ce25a405d14241422655c691080d6debefc4314628e25642e3b3c",
    "dB": "71e0c343623729ad9a56088f810e630dc32836eada55a730582cbe117362bdd2",
    "excess": "33f2d8a055fec42b665cafbccfda9e17190cad636cbb0b2119fea9767f500146",
}


def digest(value: F) -> str:
    return hashlib.sha256(f"{value.numerator}/{value.denominator}".encode()).hexdigest()


def pair(value: F):
    return value.numerator, value.denominator


def state_space():
    return tuple(
        (i, j)
        for i in range(A + 1)
        for j in range(B + 1)
        if (i, j) not in ((0, 0), (A, B))
    )


def event_probabilities(state, rule):
    """Sum labelled source-target or death-parent event probabilities."""
    i, j = state
    d_a = (A - 1) * U + B * E
    d_b = (B - 1) * V + A * E
    moves = {}

    def add(target, probability):
        if probability:
            moves[target] = moves.get(target, F(0)) + probability

    if rule == "Bd":
        fitness_mass = R * (i + j) + (N - i - j)
        # Each summand is: number of labelled reproducers, probability of
        # choosing one, number of opposite-type targets, and edge/degree.
        add((i + 1, j), R / fitness_mass * (i * (A - i) * U / d_a + j * (A - i) * E / d_b))
        add((i - 1, j), 1 / fitness_mass * ((A - i) * i * U / d_a + (B - j) * i * E / d_b))
        add((i, j + 1), R / fitness_mass * (j * (B - j) * V / d_b + i * (B - j) * E / d_a))
        add((i, j - 1), 1 / fitness_mass * ((B - j) * j * V / d_b + (A - i) * j * E / d_a))
    elif rule == "dB":
        if i < A:
            mutant = i * U + j * E
            resident = d_a - mutant
            add((i + 1, j), F(A - i, N) * R * mutant / (R * mutant + resident))
        if i:
            mutant = (i - 1) * U + j * E
            resident = d_a - mutant
            add((i - 1, j), F(i, N) * resident / (R * mutant + resident))
        if j < B:
            mutant = j * V + i * E
            resident = d_b - mutant
            add((i, j + 1), F(B - j, N) * R * mutant / (R * mutant + resident))
        if j:
            mutant = (j - 1) * V + i * E
            resident = d_b - mutant
            add((i, j - 1), F(j, N) * resident / (R * mutant + resident))
    else:
        raise ValueError(rule)
    # Boundary-formula calls with a nonexistent target contribute zero.
    return {target: value for target, value in moves.items() if 0 <= target[0] <= A and 0 <= target[1] <= B}


def solve(rule):
    transient = state_space()
    index = {state: row for row, state in enumerate(transient)}
    rows = [[F(0) for _ in transient] for _ in transient]
    rhs = [[F(0)] for _ in transient]
    for state, row in index.items():
        probabilities = event_probabilities(state, rule)
        rows[row][row] = sum(probabilities.values(), F(0))
        for target, probability in probabilities.items():
            if target == (A, B):
                rhs[row][0] += probability
            elif target != (0, 0):
                rows[row][index[target]] -= probability
    matrix = DomainMatrix.from_list([[pair(value) for value in row] for row in rows], QQ)
    vector = DomainMatrix.from_list([[pair(value) for value in row] for row in rhs], QQ)
    result = matrix.lu_solve(vector).to_list_flat()
    h = [F(int(value.numerator), int(value.denominator)) for value in result]
    return F(A, N) * h[index[(1, 0)]] + F(B, N) * h[index[(0, 1)]]


def baseline(rule):
    if rule == "Bd":
        return F(3 ** (N - 1), 3**N - 2**N)
    return F((N - 1) * 3 ** (N - 2), N * (3 ** (N - 1) - 2 ** (N - 1)))


def main():
    rho = {rule: solve(rule) for rule in ("Bd", "dB")}
    assert digest(rho["Bd"]) == EXPECTED["Bd"]
    assert digest(rho["dB"]) == EXPECTED["dB"]
    x = rho["Bd"] / baseline("Bd")
    y = rho["dB"] / baseline("dB")
    excess = (x + 2 * y) / 3 - 1
    crossing = (y - 1) / (y - x)
    assert digest(excess) == EXPECTED["excess"]
    assert excess > 0
    assert crossing > F(1, 3)
    print("PASS independent discrete-time labelled-event SymPy-QQ solve")
    print(f"theta_0~{float(crossing):.15g} > 1/3 exactly")


if __name__ == "__main__":
    main()
