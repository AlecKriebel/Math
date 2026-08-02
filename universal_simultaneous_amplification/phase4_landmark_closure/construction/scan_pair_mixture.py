#!/usr/bin/env python3
"""Complete-support mixture of exchangeable weighted pairs.

Every non-pair edge has weight one.  Category A contains m_A disjoint pairs
whose within-pair edge has weight A; category B is analogous with weight B.
The quotient records the numbers of mixed and fully mutant pairs in each
category.  This tests diffuse near-complete perturbations when A,B=o(n).
"""

from __future__ import annotations

import itertools

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as spla


def baseline(n, fitness, rule):
    if rule == "Bd": return (1 - 1 / fitness) / (1 - fitness ** (-n))
    return (n - 1) / n * (1 - 1 / fitness) / (1 - fitness ** (-(n - 1)))


def category_counts(modules, mixed, full):
    return (modules - mixed - full, mixed, full)


def transition_state(state, category, source_k, target_k):
    result = list(state); mixed_index = 2 * category; full_index = mixed_index + 1
    if source_k == 1: result[mixed_index] -= 1
    elif source_k == 2: result[full_index] -= 1
    if target_k == 1: result[mixed_index] += 1
    elif target_k == 2: result[full_index] += 1
    return tuple(result)


def transitions(state, modules, pair_weights, fitness, rule):
    mixed_a, full_a, mixed_b, full_b = state
    category_state = ((mixed_a, full_a), (mixed_b, full_b))
    mutant_counts = (mixed_a + 2 * full_a, mixed_b + 2 * full_b)
    vertex_counts = (2 * modules[0], 2 * modules[1])
    n = sum(vertex_counts); total_mutants = sum(mutant_counts)
    degrees = tuple(pair_weights[t] + n - 2 for t in (0, 1))
    result = []
    if rule == "Bd":
        total_fitness = n + (fitness - 1) * total_mutants
        mutant_parent_base = sum(mutant_counts[t] / degrees[t] for t in (0, 1))
        resident_parent_base = sum((vertex_counts[t] - mutant_counts[t]) / degrees[t] for t in (0, 1))
        for category in (0, 1):
            counts = category_counts(modules[category], *category_state[category])
            pair_weight = pair_weights[category]; degree = degrees[category]
            for k, multiplicity in enumerate(counts):
                if not multiplicity: continue
                if k < 2:
                    parent_mass = mutant_parent_base + k * (pair_weight - 1) / degree
                    rate = multiplicity * (2 - k) * fitness / total_fitness * parent_mass
                    if rate: result.append((transition_state(state, category, k, k + 1), rate))
                if k:
                    parent_mass = resident_parent_base + (2 - k) * (pair_weight - 1) / degree
                    rate = multiplicity * k / total_fitness * parent_mass
                    if rate: result.append((transition_state(state, category, k, k - 1), rate))
    elif rule == "dB":
        for category in (0, 1):
            counts = category_counts(modules[category], *category_state[category])
            pair_weight = pair_weights[category]
            for k, multiplicity in enumerate(counts):
                if not multiplicity: continue
                if k < 2:
                    mutant_mass = total_mutants + k * (pair_weight - 1)
                    resident_mass = n - total_mutants - 1 + (1 - k) * (pair_weight - 1)
                    if mutant_mass:
                        rate = multiplicity * (2 - k) / n * fitness * mutant_mass / (fitness * mutant_mass + resident_mass)
                        result.append((transition_state(state, category, k, k + 1), rate))
                if k:
                    mutant_mass = total_mutants - 1 + (k - 1) * (pair_weight - 1)
                    resident_mass = n - total_mutants + (2 - k) * (pair_weight - 1)
                    if resident_mass:
                        rate = multiplicity * k / n * resident_mass / (fitness * mutant_mass + resident_mass)
                        result.append((transition_state(state, category, k, k - 1), rate))
    else:
        raise ValueError(rule)
    return result


def fixation(modules, pair_weights, fitness, rule):
    states = [
        (ma, fa, mb, fb)
        for ma in range(modules[0] + 1)
        for fa in range(modules[0] - ma + 1)
        for mb in range(modules[1] + 1)
        for fb in range(modules[1] - mb + 1)
    ]
    empty = (0, 0, 0, 0); full = (0, modules[0], 0, modules[1])
    states.remove(empty); states.remove(full); index = {state: i for i, state in enumerate(states)}
    rows, columns, data = [], [], []; rhs = np.zeros(len(states))
    for state, source in index.items():
        changes = transitions(state, modules, pair_weights, fitness, rule)
        mass = sum(probability for _, probability in changes)
        rows.append(source); columns.append(source); data.append(1.0)
        for target, probability in changes:
            probability /= mass
            if target == full: rhs[source] += probability
            elif target != empty:
                rows.append(source); columns.append(index[target]); data.append(-probability)
    matrix = sparse.csr_matrix((data, (rows, columns)), shape=(len(states),) * 2)
    values = spla.spsolve(matrix, rhs); residual = float(np.max(np.abs(matrix @ values - rhs)))
    n = 2 * sum(modules)
    initial_a = (1, 0, 0, 0); initial_b = (0, 0, 1, 0)
    average = (2 * modules[0] * values[index[initial_a]] + 2 * modules[1] * values[index[initial_b]]) / n
    return float(average), residual

