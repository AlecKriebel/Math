#!/usr/bin/env python3
"""Independent exact verifier for the clique-fan quotient transitions."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction


def quotient(mask: int, modules: int, size: int):
    hub = mask & 1
    occupancies = []
    for module_id in range(modules):
        first = 1 + module_id * size
        occupancies.append(sum((mask >> (first + j)) & 1 for j in range(size)))
    return int(bool(hub)), tuple(occupancies.count(k) for k in range(size + 1))


def weights(modules: int, size: int, spoke: Fraction):
    n = modules * size + 1
    result = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for module_id in range(modules):
        vertices = list(range(1 + module_id * size, 1 + (module_id + 1) * size))
        for i in vertices:
            result[0][i] = result[i][0] = spoke
            for j in vertices:
                if i != j:
                    result[i][j] = Fraction(1)
    return result


def full_changes(mask, matrix, fitness, rule):
    n = len(matrix); full = (1 << n) - 1
    degrees = [sum(row) for row in matrix]
    result = defaultdict(Fraction)
    if mask in (0, full):
        return result
    mutant = [bool(mask >> i & 1) for i in range(n)]
    if rule == "Bd":
        total_fitness = sum(fitness if value else 1 for value in mutant)
        for parent in range(n):
            for target in range(n):
                if not matrix[parent][target]:
                    continue
                probability = (fitness if mutant[parent] else 1) * matrix[parent][target] / (total_fitness * degrees[parent])
                target_mask = mask | (1 << target) if mutant[parent] else mask & ~(1 << target)
                if target_mask != mask:
                    result[target_mask] += probability
    elif rule == "dB":
        for dead in range(n):
            denominator = sum((fitness if mutant[parent] else 1) * matrix[parent][dead] for parent in range(n))
            for parent in range(n):
                if not matrix[parent][dead]:
                    continue
                probability = (fitness if mutant[parent] else 1) * matrix[parent][dead] / (n * denominator)
                target_mask = mask | (1 << dead) if mutant[parent] else mask & ~(1 << dead)
                if target_mask != mask:
                    result[target_mask] += probability
    else:
        raise ValueError(rule)
    return result


def histogram_move(counts, source, target):
    result = list(counts); result[source] -= 1; result[target] += 1
    return tuple(result)


def quotient_changes(state, modules, size, spoke, fitness, rule):
    hub, counts = state
    leaves = modules * size; n = leaves + 1
    mutants = sum(k * counts[k] for k in range(size + 1))
    result = defaultdict(Fraction)
    if rule == "Bd":
        total = n + (fitness - 1) * (hub + mutants); degree = size - 1 + spoke
        if not hub and mutants:
            result[(1, counts)] += fitness * mutants * spoke / (total * degree)
        if hub and mutants < leaves:
            result[(0, counts)] += (leaves - mutants) * spoke / (total * degree)
        for k, multiplicity in enumerate(counts):
            if k < size and multiplicity:
                rate = multiplicity * (size - k) * fitness / total * (Fraction(k, 1) / degree + Fraction(hub, leaves))
                if rate:
                    result[(hub, histogram_move(counts, k, k + 1))] += rate
            if k and multiplicity:
                rate = multiplicity * k / total * (Fraction(size - k, 1) / degree + Fraction(1 - hub, leaves))
                if rate:
                    result[(hub, histogram_move(counts, k, k - 1))] += rate
    elif rule == "dB":
        if not hub and mutants:
            result[(1, counts)] += fitness * mutants / (n * (fitness * mutants + leaves - mutants))
        if hub and mutants < leaves:
            result[(0, counts)] += (leaves - mutants) / (n * (fitness * mutants + leaves - mutants))
        for k, multiplicity in enumerate(counts):
            if k < size and multiplicity:
                mutant_mass = fitness * (k + hub * spoke)
                resident_mass = size - k - 1 + (1 - hub) * spoke
                if mutant_mass:
                    result[(hub, histogram_move(counts, k, k + 1))] += multiplicity * (size - k) * mutant_mass / (n * (mutant_mass + resident_mass))
            if k and multiplicity:
                mutant_mass = fitness * (k - 1 + hub * spoke)
                resident_mass = size - k + (1 - hub) * spoke
                if resident_mass:
                    result[(hub, histogram_move(counts, k, k - 1))] += multiplicity * k * resident_mass / (n * (mutant_mass + resident_mass))
    else:
        raise ValueError(rule)
    return dict(result)


def verify(modules, size, spoke, fitness, rule):
    matrix = weights(modules, size, spoke); n = len(matrix)
    representatives = {}
    for mask in range(1, (1 << n) - 1):
        state = quotient(mask, modules, size)
        aggregate = defaultdict(Fraction)
        for target_mask, probability in full_changes(mask, matrix, fitness, rule).items():
            aggregate[quotient(target_mask, modules, size)] += probability
        aggregate = dict(aggregate)
        if state in representatives and representatives[state] != aggregate:
            raise AssertionError(("not lumpable", state, mask))
        representatives[state] = aggregate
        expected = quotient_changes(state, modules, size, spoke, fitness, rule)
        if aggregate != expected:
            raise AssertionError(("formula mismatch", state, aggregate, expected))
    print(f"PASS M={modules} L={size} spoke={spoke} r={fitness} rule={rule} cells={len(representatives)}")


def main():
    for modules, size, spoke, fitness in (
        (2, 2, Fraction(2, 5), Fraction(3, 2)),
        (2, 3, Fraction(5, 7), Fraction(7, 3)),
    ):
        for rule in ("Bd", "dB"):
            verify(modules, size, spoke, fitness, rule)


if __name__ == "__main__":
    main()
