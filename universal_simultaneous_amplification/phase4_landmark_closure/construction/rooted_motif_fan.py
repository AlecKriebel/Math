#!/usr/bin/env python3
"""Exact histogram quotient for exchangeable rooted weighted motifs.

M identical k-vertex motifs are disjoint except for a common hub.  ``internal``
is the symmetric k by k internal weight matrix and ``spokes[v]`` is the
hub--v weight.  The quotient records the hub type and the histogram of the
2^k motif mutant masks.  This is practical for k=3,4 and moderate M.
"""

from __future__ import annotations

import functools

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as spla


def baseline(n, fitness, rule):
    if rule == "Bd": return (1 - 1 / fitness) / (1 - fitness ** (-n))
    return (n - 1) / n * (1 - 1 / fitness) / (1 - fitness ** (-(n - 1)))


@functools.lru_cache(maxsize=None)
def histograms(total, bins):
    if bins == 1: return ((total,),)
    return tuple((first,) + tail for first in range(total + 1) for tail in histograms(total - first, bins - 1))


def move(counts, source, target):
    result = list(counts); result[source] -= 1; result[target] += 1
    return tuple(result)


def transitions(state, modules, internal, spokes, fitness, rule):
    hub, counts = state
    internal = np.asarray(internal, dtype=float); spokes = np.asarray(spokes, dtype=float)
    size = len(spokes); bins = 1 << size; n = modules * size + 1
    local_degrees = internal.sum(axis=1) + spokes
    hub_degree = modules * spokes.sum()
    mutants_by_vertex = np.array([
        sum(counts[mask] * ((mask >> vertex) & 1) for mask in range(bins))
        for vertex in range(size)
    ], dtype=float)
    mutant_total = int(hub + mutants_by_vertex.sum())
    result = []
    if rule == "Bd":
        total_fitness = n + (fitness - 1) * mutant_total
        if not hub:
            rate = fitness / total_fitness * float(np.sum(mutants_by_vertex * spokes / local_degrees))
            if rate: result.append(((1, counts), rate))
        else:
            rate = 1 / total_fitness * float(np.sum((modules - mutants_by_vertex) * spokes / local_degrees))
            if rate: result.append(((0, counts), rate))
        for mask, multiplicity in enumerate(counts):
            if not multiplicity: continue
            types = np.array([(mask >> vertex) & 1 for vertex in range(size)], dtype=float)
            for target in range(size):
                current = int(types[target])
                if not current:
                    parent_mass = float(np.sum(types * internal[:, target] / local_degrees))
                    parent_mass += hub * spokes[target] / hub_degree
                    rate = multiplicity * fitness / total_fitness * parent_mass
                    target_mask = mask | (1 << target)
                else:
                    parent_mass = float(np.sum((1 - types) * internal[:, target] / local_degrees))
                    parent_mass += (1 - hub) * spokes[target] / hub_degree
                    rate = multiplicity / total_fitness * parent_mass
                    target_mask = mask & ~(1 << target)
                if rate: result.append(((hub, move(counts, mask, target_mask)), rate))
    elif rule == "dB":
        mutant_hub_mass = fitness * float(np.sum(mutants_by_vertex * spokes))
        resident_hub_mass = float(np.sum((modules - mutants_by_vertex) * spokes))
        if not hub and mutant_hub_mass:
            result.append(((1, counts), mutant_hub_mass / (n * (mutant_hub_mass + resident_hub_mass))))
        if hub and resident_hub_mass:
            result.append(((0, counts), resident_hub_mass / (n * (mutant_hub_mass + resident_hub_mass))))
        for mask, multiplicity in enumerate(counts):
            if not multiplicity: continue
            types = np.array([(mask >> vertex) & 1 for vertex in range(size)], dtype=float)
            for target in range(size):
                current = int(types[target])
                mutant_mass = fitness * (float(np.sum(types * internal[:, target])) + hub * spokes[target])
                resident_mass = float(np.sum((1 - types) * internal[:, target])) + (1 - hub) * spokes[target]
                if not current and mutant_mass:
                    rate = multiplicity / n * mutant_mass / (mutant_mass + resident_mass)
                    target_mask = mask | (1 << target)
                elif current and resident_mass:
                    rate = multiplicity / n * resident_mass / (mutant_mass + resident_mass)
                    target_mask = mask & ~(1 << target)
                else:
                    continue
                result.append(((hub, move(counts, mask, target_mask)), rate))
    else:
        raise ValueError(rule)
    return result


def fixation(modules, internal, spokes, fitness, rule):
    size = len(spokes); bins = 1 << size
    empty_counts = (modules,) + (0,) * (bins - 1)
    full_counts = (0,) * (bins - 1) + (modules,)
    empty = (0, empty_counts); full = (1, full_counts)
    states = [(hub, counts) for hub in (0, 1) for counts in histograms(modules, bins) if (hub, counts) not in (empty, full)]
    index = {state: i for i, state in enumerate(states)}
    rows, columns, data = [], [], []; rhs = np.zeros(len(states))
    for state, source in index.items():
        changes = transitions(state, modules, internal, spokes, fitness, rule)
        mass = sum(probability for _, probability in changes)
        if not mass > 0: raise AssertionError((state, changes))
        rows.append(source); columns.append(source); data.append(1.0)
        for target, probability in changes:
            probability /= mass
            if target == full: rhs[source] += probability
            elif target != empty:
                rows.append(source); columns.append(index[target]); data.append(-probability)
    matrix = sparse.csr_matrix((data, (rows, columns)), shape=(len(states),) * 2)
    values = spla.spsolve(matrix, rhs); residual = float(np.max(np.abs(matrix @ values - rhs)))
    n = modules * size + 1
    average = values[index[(1, empty_counts)]] / n
    for vertex in range(size):
        singleton_counts = [0] * bins; singleton_counts[0] = modules - 1; singleton_counts[1 << vertex] = 1
        average += modules * values[index[(0, tuple(singleton_counts))]] / n
    return float(average), residual

