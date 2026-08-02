#!/usr/bin/env python3
"""Independent exact full-state check of the center/triangle quotient."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction

from scan_center_triangle import transitions, triangle_weights


def graph(center, modules, delta, z, epsilon):
    n = center + 3 * modules
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(center):
        for j in range(i + 1, center):
            matrix[i][j] = matrix[j][i] = z
    local = triangle_weights(delta)
    for module in range(modules):
        vertices = [center + 3 * module + v for v in range(3)]
        for u in range(3):
            for v in range(u + 1, 3):
                matrix[vertices[u]][vertices[v]] = matrix[vertices[v]][vertices[u]] = local[u][v]
        for vertex in vertices:
            for core in range(center):
                matrix[vertex][core] = matrix[core][vertex] = epsilon
    return matrix


def quotient(mask, center, modules):
    k = sum((mask >> v) & 1 for v in range(center))
    local_masks = []
    for module in range(modules):
        local_mask = 0
        for v in range(3):
            local_mask |= ((mask >> (center + 3 * module + v)) & 1) << v
        local_masks.append(local_mask)
    return k, tuple(local_masks.count(local_mask) for local_mask in range(8))


def full_changes(mask, matrix, fitness, rule):
    n = len(matrix)
    mutant = [bool((mask >> v) & 1) for v in range(n)]
    degrees = [sum(row) for row in matrix]
    result = defaultdict(Fraction)
    if rule == "Bd":
        total = sum(fitness if value else 1 for value in mutant)
        for parent in range(n):
            for target in range(n):
                if not matrix[parent][target] or mutant[parent] == mutant[target]:
                    continue
                rate = (
                    (fitness if mutant[parent] else 1)
                    * matrix[parent][target]
                    / (total * degrees[parent])
                )
                target_mask = mask | (1 << target) if mutant[parent] else mask & ~(1 << target)
                result[target_mask] += rate
    elif rule == "dB":
        for target in range(n):
            denominator = sum(
                (fitness if mutant[parent] else 1) * matrix[parent][target]
                for parent in range(n)
            )
            for parent in range(n):
                if not matrix[parent][target] or mutant[parent] == mutant[target]:
                    continue
                rate = (
                    (fitness if mutant[parent] else 1)
                    * matrix[parent][target]
                    / (n * denominator)
                )
                target_mask = mask | (1 << target) if mutant[parent] else mask & ~(1 << target)
                result[target_mask] += rate
    else:
        raise ValueError(rule)
    return result


def verify(center, modules, delta, z, epsilon, fitness, rule):
    matrix = graph(center, modules, delta, z, epsilon)
    n = len(matrix)
    representatives = {}
    for mask in range(1, (1 << n) - 1):
        source = quotient(mask, center, modules)
        aggregate = defaultdict(Fraction)
        for target, rate in full_changes(mask, matrix, fitness, rule).items():
            aggregate[quotient(target, center, modules)] += rate
        aggregate = dict(aggregate)
        expected = defaultdict(Fraction)
        for target, rate in transitions(
            source, center, modules, delta, z, epsilon, fitness, rule
        ):
            expected[target] += rate
        expected = dict(expected)
        if source in representatives and representatives[source] != aggregate:
            raise AssertionError(("not lumpable", source, mask))
        representatives[source] = aggregate
        if aggregate != expected:
            raise AssertionError(("formula mismatch", source, aggregate, expected))
    print(
        f"PASS c={center} M={modules} delta={delta} z={z} epsilon={epsilon} "
        f"r={fitness} rule={rule} cells={len(representatives)}"
    )


def main():
    cases = (
        (2, 1, Fraction(1, 5), Fraction(2, 7), Fraction(1, 13), Fraction(6, 5)),
        (2, 2, Fraction(2, 9), Fraction(3, 8), Fraction(1, 17), Fraction(7, 3)),
    )
    for case in cases:
        for rule in ("Bd", "dB"):
            verify(*case, rule)


if __name__ == "__main__":
    main()
