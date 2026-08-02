#!/usr/bin/env python3
"""Exact quotient chain for a clique center joined to weak triangles.

The quotient is the mutant count in the center and the histogram of the eight
labelled mutant masks of an exchangeable triangle module.  Sparse numerical
solutions are verification diagnostics; theorem signs come from the
asymptotic proof, not these values.
"""

from __future__ import annotations

import argparse
import functools

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as spla


@functools.lru_cache(maxsize=None)
def histograms(total: int, bins: int = 8):
    if bins == 1:
        return ((total,),)
    return tuple(
        (first,) + tail
        for first in range(total + 1)
        for tail in histograms(total - first, bins - 1)
    )


def move(counts, source, target):
    result = list(counts)
    result[source] -= 1
    result[target] += 1
    return tuple(result)


def triangle_weights(delta):
    zero = delta * 0
    one = zero + 1
    return ((zero, delta, one), (delta, zero, delta), (one, delta, zero))


def transitions(state, center, modules, delta, z, epsilon, fitness, rule):
    k, counts = state
    local = triangle_weights(delta)
    local_degrees = tuple(sum(row) for row in local)
    center_degree = (center - 1) * z + 3 * modules * epsilon
    module_degrees = tuple(degree + center * epsilon for degree in local_degrees)
    # ``int.bit_count`` is unavailable in the Python 3.9 runtime used by the
    # independent certificate runner.
    local_mutants = sum(counts[mask] * bin(mask).count("1") for mask in range(8))
    n = center + 3 * modules
    result = []

    if rule == "Bd":
        total_fitness = n + (fitness - 1) * (k + local_mutants)
        inverse_degree_mutants = sum(
            counts[mask]
            * sum(1 / module_degrees[v] for v in range(3) if (mask >> v) & 1)
            for mask in range(8)
        )
        inverse_degree_residents = sum(
            counts[mask]
            * sum(1 / module_degrees[v] for v in range(3) if not ((mask >> v) & 1))
            for mask in range(8)
        )
        if k < center:
            rate = fitness * (center - k) / total_fitness * (
                k * z / center_degree + epsilon * inverse_degree_mutants
            )
            if rate:
                result.append(((k + 1, counts), rate))
        if k:
            rate = k / total_fitness * (
                (center - k) * z / center_degree + epsilon * inverse_degree_residents
            )
            if rate:
                result.append(((k - 1, counts), rate))
        for mask, multiplicity in enumerate(counts):
            if not multiplicity:
                continue
            for target in range(3):
                if not ((mask >> target) & 1):
                    internal = sum(
                        local[parent][target] / module_degrees[parent]
                        for parent in range(3)
                        if (mask >> parent) & 1
                    )
                    rate = multiplicity * fitness / total_fitness * (
                        internal + k * epsilon / center_degree
                    )
                    if rate:
                        result.append(((k, move(counts, mask, mask | (1 << target))), rate))
                else:
                    internal = sum(
                        local[parent][target] / module_degrees[parent]
                        for parent in range(3)
                        if not ((mask >> parent) & 1)
                    )
                    rate = multiplicity / total_fitness * (
                        internal + (center - k) * epsilon / center_degree
                    )
                    if rate:
                        result.append(((k, move(counts, mask, mask & ~(1 << target))), rate))
    elif rule == "dB":
        if k < center:
            mutant_mass = k * z + local_mutants * epsilon
            resident_mass = (center - k - 1) * z + (3 * modules - local_mutants) * epsilon
            if mutant_mass:
                rate = (center - k) * fitness * mutant_mass / (
                    n * (fitness * mutant_mass + resident_mass)
                )
                result.append(((k + 1, counts), rate))
        if k:
            mutant_mass = (k - 1) * z + local_mutants * epsilon
            resident_mass = (center - k) * z + (3 * modules - local_mutants) * epsilon
            if resident_mass:
                rate = k * resident_mass / (n * (fitness * mutant_mass + resident_mass))
                result.append(((k - 1, counts), rate))
        for mask, multiplicity in enumerate(counts):
            if not multiplicity:
                continue
            for target in range(3):
                internal_mutant = sum(
                    local[parent][target]
                    for parent in range(3)
                    if (mask >> parent) & 1
                )
                internal_resident = sum(
                    local[parent][target]
                    for parent in range(3)
                    if not ((mask >> parent) & 1)
                )
                if not ((mask >> target) & 1):
                    mutant_mass = internal_mutant + k * epsilon
                    resident_mass = internal_resident + (center - k) * epsilon
                    if mutant_mass:
                        rate = multiplicity * fitness * mutant_mass / (
                            n * (fitness * mutant_mass + resident_mass)
                        )
                        result.append(((k, move(counts, mask, mask | (1 << target))), rate))
                else:
                    mutant_mass = internal_mutant + k * epsilon
                    resident_mass = internal_resident + (center - k) * epsilon
                    if resident_mass:
                        rate = multiplicity * resident_mass / (
                            n * (fitness * mutant_mass + resident_mass)
                        )
                        result.append(((k, move(counts, mask, mask & ~(1 << target))), rate))
    else:
        raise ValueError(rule)
    return result


def fixation(center, modules, delta, z, epsilon, fitness, rule):
    empty_counts = (modules,) + (0,) * 7
    full_counts = (0,) * 7 + (modules,)
    empty = (0, empty_counts)
    full = (center, full_counts)
    states = [
        (k, counts)
        for k in range(center + 1)
        for counts in histograms(modules)
        if (k, counts) not in (empty, full)
    ]
    index = {state: position for position, state in enumerate(states)}
    rows, columns, entries = [], [], []
    rhs = np.zeros(len(states))
    for state, source in index.items():
        changes = transitions(state, center, modules, delta, z, epsilon, fitness, rule)
        changing_mass = sum(float(rate) for _, rate in changes)
        if not changing_mass > 0:
            raise AssertionError((state, rule))
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
    center_singleton = (1, empty_counts)
    total = center * values[index[center_singleton]]
    for vertex in range(3):
        counts = list(empty_counts)
        counts[0] -= 1
        counts[1 << vertex] += 1
        total += modules * values[index[(0, tuple(counts))]]
    n = center + 3 * modules
    return float(total / n), residual, len(states)


def baseline(n, fitness, rule):
    if rule == "Bd":
        return (1 - 1 / fitness) / (1 - fitness ** (-n))
    return (n - 1) / n * (1 - 1 / fitness) / (1 - fitness ** (-(n - 1)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--center", type=int, default=2)
    parser.add_argument("--modules", type=int, default=4)
    parser.add_argument("--delta", type=float, default=1 / 16)
    parser.add_argument("--z", type=float, default=1 / 8)
    parser.add_argument("--epsilon", type=float, default=1e-5)
    parser.add_argument("--fitness", type=float, default=1.2)
    args = parser.parse_args()
    n = args.center + 3 * args.modules
    for rule in ("Bd", "dB"):
        value, residual, states = fixation(
            args.center,
            args.modules,
            args.delta,
            args.z,
            args.epsilon,
            args.fitness,
            rule,
        )
        print(
            f"{rule} rho={value:.12g} excess={value-baseline(n,args.fitness,rule):+.6g} "
            f"residual={residual:.2e} states={states}"
        )


if __name__ == "__main__":
    main()
