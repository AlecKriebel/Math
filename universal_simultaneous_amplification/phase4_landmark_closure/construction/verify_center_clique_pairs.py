#!/usr/bin/env python3
"""Independent exact verifier for the center-clique/pair quotient."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction

from audit_center_clique_pairs import transitions


def graph(center, modules, z, epsilon):
    n = center + 2 * modules
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    internal = z / (center - 1)
    for i in range(center):
        for j in range(i + 1, center):
            matrix[i][j] = matrix[j][i] = internal
    for module in range(modules):
        u = center + 2 * module
        v = u + 1
        matrix[u][v] = matrix[v][u] = Fraction(1)
        for leaf in (u, v):
            for core in range(center):
                matrix[leaf][core] = matrix[core][leaf] = epsilon
    return matrix


def quotient(mask, center, modules):
    k = sum((mask >> i) & 1 for i in range(center))
    occupancies = []
    for module in range(modules):
        u = center + 2 * module
        occupancies.append(((mask >> u) & 1) + ((mask >> (u + 1)) & 1))
    return k, tuple(occupancies.count(j) for j in range(3))


def full_changes(mask, matrix, fitness, rule):
    n = len(matrix)
    degrees = [sum(row) for row in matrix]
    mutant = [bool((mask >> i) & 1) for i in range(n)]
    result = defaultdict(Fraction)
    if rule == "Bd":
        total_fitness = sum(fitness if value else 1 for value in mutant)
        for parent in range(n):
            for target in range(n):
                if not matrix[parent][target] or mutant[parent] == mutant[target]:
                    continue
                probability = (
                    (fitness if mutant[parent] else 1)
                    * matrix[parent][target]
                    / (total_fitness * degrees[parent])
                )
                target_mask = mask | (1 << target) if mutant[parent] else mask & ~(1 << target)
                result[target_mask] += probability
    elif rule == "dB":
        for target in range(n):
            denominator = sum(
                (fitness if mutant[parent] else 1) * matrix[parent][target]
                for parent in range(n)
            )
            for parent in range(n):
                if not matrix[parent][target] or mutant[parent] == mutant[target]:
                    continue
                probability = (
                    (fitness if mutant[parent] else 1)
                    * matrix[parent][target]
                    / (n * denominator)
                )
                target_mask = mask | (1 << target) if mutant[parent] else mask & ~(1 << target)
                result[target_mask] += probability
    else:
        raise ValueError(rule)
    return result


def verify(center, modules, z, epsilon, fitness, rule):
    matrix = graph(center, modules, z, epsilon)
    n = len(matrix)
    representatives = {}
    for mask in range(1, (1 << n) - 1):
        source_cell = quotient(mask, center, modules)
        aggregate = defaultdict(Fraction)
        for target, probability in full_changes(mask, matrix, fitness, rule).items():
            aggregate[quotient(target, center, modules)] += probability
        aggregate = dict(aggregate)
        expected = defaultdict(Fraction)
        for target, probability in transitions(
            source_cell, center, modules, z, epsilon, fitness, rule
        ):
            expected[target] += probability
        expected = dict(expected)
        if source_cell in representatives and representatives[source_cell] != aggregate:
            raise AssertionError(("not lumpable", source_cell, mask))
        representatives[source_cell] = aggregate
        if aggregate != expected:
            raise AssertionError(("formula mismatch", source_cell, aggregate, expected))
    print(
        f"PASS c={center} M={modules} z={z} epsilon={epsilon} "
        f"r={fitness} rule={rule} cells={len(representatives)}"
    )


def main():
    cases = (
        (2, 2, Fraction(7, 5), Fraction(1, 11), Fraction(6, 5)),
        (3, 1, Fraction(13, 10), Fraction(2, 17), Fraction(7, 3)),
    )
    for case in cases:
        for rule in ("Bd", "dB"):
            verify(*case, rule)


if __name__ == "__main__":
    main()
