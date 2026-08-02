#!/usr/bin/env python3
"""Reproducible exact-rational finite-r search on weighted K4.

Search output is explicitly observational.  The family theorems are proved by
``derive_lumped_certificates.py`` and do not depend on this sampling script.
"""

from __future__ import annotations

import argparse
import random
from fractions import Fraction
from itertools import combinations, product


Q = Fraction


def solve_fraction_system(matrix, rhs):
    n = len(rhs)
    augmented = [matrix[row][:] + [rhs[row]] for row in range(n)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        for entry in range(column, n + 1):
            augmented[column][entry] /= divisor
        for row in range(n):
            if row == column:
                continue
            multiplier = augmented[row][column]
            if multiplier:
                for entry in range(column, n + 1):
                    augmented[row][entry] -= multiplier * augmented[column][entry]
    return [row[-1] for row in augmented]


def rho_db_k4(weights, fitness):
    full = 0b1111
    states = tuple(range(1, full))
    index = {state: location for location, state in enumerate(states)}
    degree = [sum(row) for row in weights]
    matrix = [[Q(0) for _ in states] for _ in states]
    rhs = [Q(0) for _ in states]
    for state in states:
        moves = []
        for dead in range(4):
            mutant_mass = sum(
                weights[parent][dead]
                for parent in range(4)
                if state & (1 << parent)
            )
            resident_mass = degree[dead] - mutant_mass
            denominator = fitness * mutant_mass + resident_mass
            if state & (1 << dead):
                probability = Q(1, 4) * resident_mass / denominator
                target = state & ~(1 << dead)
            else:
                probability = Q(1, 4) * fitness * mutant_mass / denominator
                target = state | (1 << dead)
            if probability:
                moves.append((target, probability))
        row = index[state]
        matrix[row][row] = sum(probability for _, probability in moves)
        for target, probability in moves:
            if target == full:
                rhs[row] += probability
            elif target:
                matrix[row][index[target]] -= probability
    solution = solve_fraction_system(matrix, rhs)
    return sum(solution[index[1 << vertex]] for vertex in range(4)) / 4


def baseline(fitness):
    return Q(3) * fitness**2 / (4 * (fitness**2 + fitness + 1))


def weights_22(internal_a, internal_b):
    return (
        (Q(0), internal_a, Q(1), Q(1)),
        (internal_a, Q(0), Q(1), Q(1)),
        (Q(1), Q(1), Q(0), internal_b),
        (Q(1), Q(1), internal_b, Q(0)),
    )


def arbitrary_weights(edge_values):
    matrix = [[Q(0) for _ in range(4)] for _ in range(4)]
    for value, (left, right) in zip(edge_values, combinations(range(4), 2)):
        matrix[left][right] = matrix[right][left] = value
    return tuple(tuple(row) for row in matrix)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=5000)
    args = parser.parse_args()

    weight_grid = tuple(
        Q(value)
        for value in (
            Q(1, 32),
            Q(1, 16),
            Q(1, 8),
            Q(1, 4),
            Q(1, 2),
            Q(3, 4),
            Q(1),
            Q(4, 3),
            Q(2),
            Q(4),
            Q(8),
            Q(16),
            Q(32),
        )
    )
    fitness_grid = (
        Q(1001, 1000),
        Q(101, 100),
        Q(11, 10),
        Q(3, 2),
        Q(2),
        Q(3),
        Q(10),
        Q(100),
    )

    family_positive = []
    for internal_a, internal_b in product(weight_grid, repeat=2):
        weights = weights_22(internal_a, internal_b)
        for fitness in fitness_grid:
            difference = rho_db_k4(weights, fitness) - baseline(fitness)
            if difference > 0:
                family_positive.append((internal_a, internal_b, fitness, difference))

    rng = random.Random(20260801)
    unrestricted_grid = (
        Q(1, 32),
        Q(1, 16),
        Q(1, 8),
        Q(1, 4),
        Q(1, 2),
        Q(1),
        Q(2),
        Q(4),
        Q(8),
        Q(16),
        Q(32),
    )
    unrestricted_fitness = fitness_grid + (Q(5, 4), Q(5))
    unrestricted_positive = []
    for _ in range(args.trials):
        edge_values = [rng.choice(unrestricted_grid) for _ in range(6)]
        scale = edge_values[0]
        edge_values = [value / scale for value in edge_values]
        fitness = rng.choice(unrestricted_fitness)
        difference = rho_db_k4(arbitrary_weights(edge_values), fitness) - baseline(fitness)
        if difference > 0:
            unrestricted_positive.append((edge_values, fitness, difference))
            break

    print(
        "[EXACT GRID OBSERVATION, NOT PROOF] 2+2 comparisons checked:",
        len(weight_grid) ** 2 * len(fitness_grid),
    )
    print(
        "[EXACT GRID OBSERVATION, NOT PROOF] positive 2+2 samples:",
        len(family_positive),
    )
    print(
        "[EXACT RANDOM OBSERVATION, NOT PROOF] unrestricted K4 trials:",
        args.trials,
    )
    print(
        "[EXACT RANDOM OBSERVATION, NOT PROOF] first positive unrestricted sample:",
        unrestricted_positive[:1],
    )


if __name__ == "__main__":
    main()
