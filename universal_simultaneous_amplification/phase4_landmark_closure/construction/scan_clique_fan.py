#!/usr/bin/env python3
"""Exact quotient-chain reconnaissance for a hub joined to equal cliques.

There are ``modules`` disjoint cliques of ``module_size`` vertices.  Clique
edges have weight one and every hub--clique edge has weight ``spoke_weight``.
The quotient state is the hub type and the histogram of module mutant counts.
The transition formulas below come directly from Bd and dB updating.

Floating-point sparse solves are discovery aids only.  Residuals are checked;
no numerical sign is promoted to a theorem.
"""

from __future__ import annotations

import argparse
import functools
import math

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as spla


def baseline(n: int, r: float, rule: str) -> float:
    if rule == "Bd":
        return (1.0 - 1.0 / r) / (1.0 - r ** (-n))
    return (n - 1.0) / n * (1.0 - 1.0 / r) / (1.0 - r ** (-(n - 1)))


@functools.lru_cache(maxsize=None)
def histograms(modules: int, bins: int) -> tuple[tuple[int, ...], ...]:
    if bins == 1:
        return ((modules,),)
    return tuple(
        (first,) + tail
        for first in range(modules + 1)
        for tail in histograms(modules - first, bins - 1)
    )


def move(histogram: tuple[int, ...], source: int, target: int) -> tuple[int, ...]:
    result = list(histogram)
    result[source] -= 1
    result[target] += 1
    return tuple(result)


def transitions(
    state: tuple[int, tuple[int, ...]],
    modules: int,
    size: int,
    spoke: float,
    fitness: float,
    rule: str,
) -> list[tuple[tuple[int, tuple[int, ...]], float]]:
    hub, counts = state
    leaves = modules * size
    n = leaves + 1
    mutants = sum(k * counts[k] for k in range(size + 1))
    result: list[tuple[tuple[int, tuple[int, ...]], float]] = []
    if rule == "Bd":
        total_fitness = n + (fitness - 1.0) * (hub + mutants)
        leaf_degree = size - 1.0 + spoke
        if not hub and mutants:
            result.append(((1, counts), fitness * mutants * spoke / (total_fitness * leaf_degree)))
        if hub and mutants < leaves:
            result.append(((0, counts), (leaves - mutants) * spoke / (total_fitness * leaf_degree)))
        for k, multiplicity in enumerate(counts):
            if not multiplicity:
                continue
            if k < size:
                rate = multiplicity * (size - k) * fitness / total_fitness * (
                    k / leaf_degree + hub / leaves
                )
                if rate:
                    result.append(((hub, move(counts, k, k + 1)), rate))
            if k:
                rate = multiplicity * k / total_fitness * (
                    (size - k) / leaf_degree + (1 - hub) / leaves
                )
                if rate:
                    result.append(((hub, move(counts, k, k - 1)), rate))
    elif rule == "dB":
        if not hub and mutants:
            result.append(
                ((1, counts), fitness * mutants / (n * (fitness * mutants + leaves - mutants)))
            )
        if hub and mutants < leaves:
            result.append(
                ((0, counts), (leaves - mutants) / (n * (fitness * mutants + leaves - mutants)))
            )
        for k, multiplicity in enumerate(counts):
            if not multiplicity:
                continue
            if k < size:
                mutant_mass = fitness * (k + hub * spoke)
                resident_mass = size - k - 1 + (1 - hub) * spoke
                if mutant_mass:
                    rate = multiplicity * (size - k) / n * mutant_mass / (mutant_mass + resident_mass)
                    result.append(((hub, move(counts, k, k + 1)), rate))
            if k:
                mutant_mass = fitness * (k - 1 + hub * spoke)
                resident_mass = size - k + (1 - hub) * spoke
                if resident_mass:
                    rate = multiplicity * k / n * resident_mass / (mutant_mass + resident_mass)
                    result.append(((hub, move(counts, k, k - 1)), rate))
    else:
        raise ValueError(rule)
    return result


def fixation(modules: int, size: int, spoke: float, fitness: float, rule: str) -> tuple[float, float]:
    empty_counts = (modules,) + (0,) * size
    full_counts = (0,) * size + (modules,)
    empty = (0, empty_counts)
    full = (1, full_counts)
    states = [
        (hub, counts)
        for hub in (0, 1)
        for counts in histograms(modules, size + 1)
        if (hub, counts) not in (empty, full)
    ]
    index = {state: position for position, state in enumerate(states)}
    row_indices: list[int] = []
    column_indices: list[int] = []
    entries: list[float] = []
    rhs = np.zeros(len(states))
    for state, source in index.items():
        changes = transitions(state, modules, size, spoke, fitness, rule)
        total = sum(probability for _, probability in changes)
        if not total > 0:
            raise AssertionError((state, changes))
        row_indices.append(source)
        column_indices.append(source)
        entries.append(1.0)
        for target, probability in changes:
            probability /= total
            if target == full:
                rhs[source] += probability
            elif target != empty:
                row_indices.append(source)
                column_indices.append(index[target])
                entries.append(-probability)
    matrix = sparse.csr_matrix(
        (entries, (row_indices, column_indices)), shape=(len(states),) * 2
    )
    values = spla.spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    hub_singleton = (1, empty_counts)
    leaf_counts = (modules - 1, 1) + (0,) * (size - 1)
    leaf_singleton = (0, leaf_counts)
    n = modules * size + 1
    average = (values[index[hub_singleton]] + modules * size * values[index[leaf_singleton]]) / n
    return float(average), residual


def scan(modules: int, size: int) -> None:
    n = modules * size + 1
    fitnesses = (1.02, 1.1, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 30.0)
    results = []
    for exponent in np.linspace(-4.0, 2.0, 49):
        spoke = modules**exponent
        values = []
        for fitness in fitnesses:
            for rule in ("Bd", "dB"):
                value, residual = fixation(modules, size, spoke, fitness, rule)
                if residual > 5e-9:
                    raise AssertionError((modules, size, spoke, fitness, rule, residual))
                values.append(value - baseline(n, fitness, rule))
        results.append((min(values), exponent, tuple(values)))
    for score, exponent, values in sorted(results, reverse=True)[:20]:
        signs = " ".join("+" if value > 2e-10 else "-" if value < -2e-10 else "0" for value in values)
        magnitudes = " ".join(f"{value:+.3e}" for value in values)
        print(f"M={modules} L={size} e={exponent:+.3f} score={score:+.3e} signs={signs}")
        print("  " + magnitudes)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modules", type=int, required=True)
    parser.add_argument("--size", type=int, required=True)
    args = parser.parse_args()
    scan(args.modules, args.size)


if __name__ == "__main__":
    main()
