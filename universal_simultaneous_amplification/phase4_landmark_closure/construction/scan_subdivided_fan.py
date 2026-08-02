#!/usr/bin/env python3
"""Quotient-chain reconnaissance for a weighted subdivided star.

Each of M exchangeable two-vertex modules is a path H--A_i--B_i.  Edge
H--A_i has weight ``spoke`` and A_i--B_i has weight one.  The quotient records
the hub type and a histogram of the four module types (A_i,B_i).
"""

from __future__ import annotations

import argparse
import functools

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as spla


def baseline(n: int, r: float, rule: str) -> float:
    if rule == "Bd":
        return (1 - 1 / r) / (1 - r ** (-n))
    return (n - 1) / n * (1 - 1 / r) / (1 - r ** (-(n - 1)))


@functools.lru_cache(maxsize=None)
def histograms(total: int, bins: int = 4) -> tuple[tuple[int, ...], ...]:
    if bins == 1:
        return ((total,),)
    return tuple(
        (first,) + tail
        for first in range(total + 1)
        for tail in histograms(total - first, bins - 1)
    )


def module(index: int) -> tuple[int, int]:
    return divmod(index, 2)


def module_index(a: int, b: int) -> int:
    return 2 * a + b


def move(counts: tuple[int, ...], source: int, target: int) -> tuple[int, ...]:
    result = list(counts)
    result[source] -= 1
    result[target] += 1
    return tuple(result)


def transitions(state, modules: int, spoke: float, fitness: float, rule: str):
    hub, counts = state
    n = 2 * modules + 1
    mutant_a = counts[2] + counts[3]
    mutant_b = counts[1] + counts[3]
    mutant_total = hub + mutant_a + mutant_b
    result = []
    if rule == "Bd":
        total_fitness = n + (fitness - 1) * mutant_total
        if not hub and mutant_a:
            result.append(((1, counts), fitness * mutant_a * spoke / (total_fitness * (1 + spoke))))
        if hub and mutant_a < modules:
            result.append(((0, counts), (modules - mutant_a) * spoke / (total_fitness * (1 + spoke))))
        for source, multiplicity in enumerate(counts):
            if not multiplicity:
                continue
            a, b = module(source)
            if not a:
                rate = multiplicity * fitness / total_fitness * (b + hub / modules)
                if rate:
                    result.append(((hub, move(counts, source, module_index(1, b))), rate))
            else:
                rate = multiplicity / total_fitness * ((1 - b) + (1 - hub) / modules)
                if rate:
                    result.append(((hub, move(counts, source, module_index(0, b))), rate))
            if not b and a:
                result.append(
                    ((hub, move(counts, source, module_index(a, 1))), multiplicity * fitness / (total_fitness * (1 + spoke)))
                )
            elif b and not a:
                result.append(
                    ((hub, move(counts, source, module_index(a, 0))), multiplicity / (total_fitness * (1 + spoke)))
                )
    elif rule == "dB":
        if not hub and mutant_a:
            result.append(((1, counts), fitness * mutant_a / (n * (fitness * mutant_a + modules - mutant_a))))
        if hub and mutant_a < modules:
            result.append(((0, counts), (modules - mutant_a) / (n * (fitness * mutant_a + modules - mutant_a))))
        for source, multiplicity in enumerate(counts):
            if not multiplicity:
                continue
            a, b = module(source)
            if not a:
                mutant_mass = fitness * (b + hub * spoke)
                resident_mass = (1 - b) + (1 - hub) * spoke
                if mutant_mass:
                    result.append(
                        ((hub, move(counts, source, module_index(1, b))), multiplicity / n * mutant_mass / (mutant_mass + resident_mass))
                    )
            else:
                mutant_mass = fitness * (b + hub * spoke)
                resident_mass = (1 - b) + (1 - hub) * spoke
                if resident_mass:
                    result.append(
                        ((hub, move(counts, source, module_index(0, b))), multiplicity / n * resident_mass / (mutant_mass + resident_mass))
                    )
            # B has A as its unique neighbor, so a mismatch changes whenever B dies.
            if a != b:
                result.append(
                    ((hub, move(counts, source, module_index(a, a))), multiplicity / n)
                )
    else:
        raise ValueError(rule)
    return result


def fixation(modules: int, spoke: float, fitness: float, rule: str):
    empty = (0, (modules, 0, 0, 0))
    full = (1, (0, 0, 0, modules))
    states = [(h, c) for h in (0, 1) for c in histograms(modules) if (h, c) not in (empty, full)]
    index = {state: i for i, state in enumerate(states)}
    rows, columns, data = [], [], []
    rhs = np.zeros(len(states))
    for state, source in index.items():
        changes = transitions(state, modules, spoke, fitness, rule)
        mass = sum(p for _, p in changes)
        rows.append(source); columns.append(source); data.append(1.0)
        for target, probability in changes:
            probability /= mass
            if target == full:
                rhs[source] += probability
            elif target != empty:
                rows.append(source); columns.append(index[target]); data.append(-probability)
    matrix = sparse.csr_matrix((data, (rows, columns)), shape=(len(states),) * 2)
    values = spla.spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    hub_singleton = (1, (modules, 0, 0, 0))
    a_singleton = (0, (modules - 1, 0, 1, 0))
    b_singleton = (0, (modules - 1, 1, 0, 0))
    n = 2 * modules + 1
    average = (values[index[hub_singleton]] + modules * values[index[a_singleton]] + modules * values[index[b_singleton]]) / n
    return float(average), residual


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modules", type=int, required=True)
    args = parser.parse_args()
    m = args.modules
    n = 2 * m + 1
    fitnesses = (1.001, 1.02, 1.05, 1.1, 1.2, 1.5, 2.0, 3.0)
    best = []
    for exponent in np.linspace(-3, 3, 97):
        spoke = m**exponent
        values = []
        for fitness in fitnesses:
            for rule in ("Bd", "dB"):
                value, residual = fixation(m, spoke, fitness, rule)
                if residual > 1e-8:
                    raise AssertionError(residual)
                values.append(value - baseline(n, fitness, rule))
        best.append((min(values), exponent, values))
    for score, exponent, values in sorted(best, reverse=True)[:20]:
        print(exponent, score, " ".join(f"{value:+.4e}" for value in values))


if __name__ == "__main__":
    main()
