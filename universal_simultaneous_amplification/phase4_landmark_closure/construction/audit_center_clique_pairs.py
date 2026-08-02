#!/usr/bin/env python3
"""Exact quotient and separated-module audit for a center clique plus leaf pairs.

The graph has a center clique of size ``c``.  Each center edge has weight
``z/(c-1)``.  There are ``m`` disjoint leaf pairs whose internal edge has
weight one, and every center--leaf edge has weight ``epsilon``.  There are no
edges between distinct leaf pairs.

The quotient state is ``(k, p0, p1, p2)``, where ``k`` is the number of
mutants in the center and ``pj`` is the number of pairs containing ``j``
mutants.  The transition formulas are direct sums of the defining Bd and dB
rules.  Floating-point fixation solves are diagnostics only.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as spla


def pair_histograms(modules: int):
    return tuple(
        (p0, p1, modules - p0 - p1)
        for p0 in range(modules + 1)
        for p1 in range(modules - p0 + 1)
    )


def move(histogram, source, target):
    result = list(histogram)
    result[source] -= 1
    result[target] += 1
    return tuple(result)


def transitions(state, center, modules, z, epsilon, fitness, rule):
    """Return non-self quotient transitions with exact-compatible arithmetic."""
    k, counts = state
    p0, p1, p2 = counts
    x = p1 + 2 * p2
    n = center + 2 * modules
    a = z / (center - 1)
    center_degree = z + 2 * modules * epsilon
    leaf_degree = 1 + center * epsilon
    result = []

    if rule == "Bd":
        total_fitness = n + (fitness - 1) * (k + x)
        if k < center:
            rate = fitness * (center - k) / total_fitness * (
                k * a / center_degree + x * epsilon / leaf_degree
            )
            if rate:
                result.append(((k + 1, counts), rate))
        if k:
            rate = k / total_fitness * (
                (center - k) * a / center_degree
                + (2 * modules - x) * epsilon / leaf_degree
            )
            if rate:
                result.append(((k - 1, counts), rate))
        for occupancy, multiplicity in enumerate(counts):
            if occupancy < 2 and multiplicity:
                rate = multiplicity * (2 - occupancy) * fitness / total_fitness * (
                    occupancy / leaf_degree + k * epsilon / center_degree
                )
                if rate:
                    result.append(((k, move(counts, occupancy, occupancy + 1)), rate))
            if occupancy and multiplicity:
                rate = multiplicity * occupancy / total_fitness * (
                    (2 - occupancy) / leaf_degree
                    + (center - k) * epsilon / center_degree
                )
                if rate:
                    result.append(((k, move(counts, occupancy, occupancy - 1)), rate))
    elif rule == "dB":
        if k < center:
            mutant_mass = k * a + x * epsilon
            resident_mass = (center - k - 1) * a + (2 * modules - x) * epsilon
            if mutant_mass:
                rate = (center - k) * fitness * mutant_mass / (
                    n * (fitness * mutant_mass + resident_mass)
                )
                result.append(((k + 1, counts), rate))
        if k:
            mutant_mass = (k - 1) * a + x * epsilon
            resident_mass = (center - k) * a + (2 * modules - x) * epsilon
            if resident_mass:
                rate = k * resident_mass / (n * (fitness * mutant_mass + resident_mass))
                result.append(((k - 1, counts), rate))
        for occupancy, multiplicity in enumerate(counts):
            if occupancy < 2 and multiplicity:
                mutant_mass = occupancy + k * epsilon
                resident_mass = 1 - occupancy + (center - k) * epsilon
                if mutant_mass:
                    rate = multiplicity * (2 - occupancy) * fitness * mutant_mass / (
                        n * (fitness * mutant_mass + resident_mass)
                    )
                    result.append(((k, move(counts, occupancy, occupancy + 1)), rate))
            if occupancy and multiplicity:
                mutant_mass = occupancy - 1 + k * epsilon
                resident_mass = 2 - occupancy + (center - k) * epsilon
                if resident_mass:
                    rate = multiplicity * occupancy * resident_mass / (
                        n * (fitness * mutant_mass + resident_mass)
                    )
                    result.append(((k, move(counts, occupancy, occupancy - 1)), rate))
    else:
        raise ValueError(rule)
    return result


def fixation(center, modules, z, epsilon, fitness, rule):
    histograms = pair_histograms(modules)
    empty = (0, (modules, 0, 0))
    full = (center, (0, 0, modules))
    states = [
        (k, counts)
        for k in range(center + 1)
        for counts in histograms
        if (k, counts) not in (empty, full)
    ]
    index = {state: position for position, state in enumerate(states)}
    rows, columns, entries = [], [], []
    rhs = np.zeros(len(states))
    for state, source in index.items():
        changes = transitions(state, center, modules, z, epsilon, fitness, rule)
        changing_mass = sum(float(rate) for _, rate in changes)
        if not changing_mass > 0:
            raise AssertionError((state, changes))
        rows.append(source); columns.append(source); entries.append(1.0)
        for target, rate in changes:
            probability = float(rate) / changing_mass
            if target == full:
                rhs[source] += probability
            elif target != empty:
                rows.append(source); columns.append(index[target]); entries.append(-probability)
    matrix = sparse.csr_matrix((entries, (rows, columns)), shape=(len(states),) * 2)
    values = spla.spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    center_singleton = (1, (modules, 0, 0))
    leaf_singleton = (0, (modules - 1, 1, 0))
    n = center + 2 * modules
    average = (
        center * values[index[center_singleton]]
        + 2 * modules * values[index[leaf_singleton]]
    ) / n
    return float(average), residual, float(values[index[center_singleton]]), float(values[index[leaf_singleton]])


def complete_baseline(n, fitness, rule):
    if rule == "Bd":
        return (1 - 1 / fitness) / (1 - fitness ** (-n))
    return (n - 1) / n * (1 - 1 / fitness) / (1 - fitness ** (-(n - 1)))


def db_clique_singleton(center, fitness):
    """Exact K_center dB fixation probability from one mutant."""
    one = fitness * 0 + 1
    denominator = one
    for i in range(1, center):
        denominator += (center - 1 + (fitness - 1) * i) / ((center - 1) * fitness**i)
    return one / denominator


def separated_leaf_limit(center, z, fitness, rule):
    """epsilon->0 leaf-singleton limit, then mutant center is treated as final.

    This retains finite-center within-module fixation probabilities.  It is the
    two-clock value used to audit the proposed macro algebra; center reversal
    is omitted and becomes exponentially unlikely as ``center`` grows.
    """
    if rule == "Bd":
        pair_fix = fitness / (fitness + 1)
        center_up = (1 - 1 / fitness) / (1 - fitness ** (-center))
        seed = fitness * center_up
        erase = 1 / (z * (fitness + 1))
    elif rule == "dB":
        pair_fix = fitness * 0 + Fraction(1, 2) if isinstance(fitness, Fraction) else 0.5
        center_up = db_clique_singleton(center, fitness)
        seed = fitness * center_up / z
        # The resident center competes with the fitness-r internal mate.
        # This 1/r factor is essential.
        erase = 1 / (2 * fitness)
    else:
        raise ValueError(rule)
    return pair_fix * seed / (seed + erase)


def limiting_leaf_formula(z, fitness, rule):
    """The further center->infinity limit of ``separated_leaf_limit``."""
    if rule == "Bd":
        return fitness / (fitness + 1) * z * (fitness**2 - 1) / (
            1 + z * (fitness**2 - 1)
        )
    if rule == "dB":
        return fitness * (fitness - 1) / (z + 2 * fitness * (fitness - 1))
    raise ValueError(rule)


def audit(center, modules, z, epsilon, fitness):
    n = center + 2 * modules
    print(f"c={center} M={modules} z={z:g} eps={epsilon:g} r={fitness:g} n={n}")
    for rule in ("Bd", "dB"):
        value, residual, center_value, leaf_value = fixation(
            center, modules, z, epsilon, fitness, rule
        )
        baseline = complete_baseline(n, fitness, rule)
        finite_macro = separated_leaf_limit(center, z, fitness, rule)
        limiting_macro = limiting_leaf_formula(z, fitness, rule)
        print(
            f"{rule}: rho={value:.12g} excess={value-baseline:+.6g} "
            f"leaf={leaf_value:.12g} center={center_value:.12g} "
            f"res={residual:.2e} finite-macro={float(finite_macro):.12g} "
            f"limit={limiting_macro:.12g}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--center", type=int, default=8)
    parser.add_argument("--modules", type=int, default=20)
    parser.add_argument("--z", type=float, default=1.05)
    parser.add_argument("--epsilon", type=float, default=1e-5)
    parser.add_argument("--fitness", type=float, default=1.2)
    args = parser.parse_args()
    audit(args.center, args.modules, args.z, args.epsilon, args.fitness)


if __name__ == "__main__":
    main()
