#!/usr/bin/env python3
"""Complete-support modular graphs with one exceptional module.

There are M modules of common size L.  One module is exceptional; the other
M-1 modules are exchangeable.  Orbit weights are:

* exceptional internal: ``exceptional_internal``;
* ordinary internal: one;
* between distinct ordinary modules: ``ordinary_cross``;
* exceptional--ordinary: ``exceptional_cross``.

The quotient state is the exceptional occupancy and the histogram of ordinary
module occupancies.  All cross weights are required positive, so every graph
has complete support.
"""

from __future__ import annotations

import functools

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as spla


def baseline(n: int, r: float, rule: str) -> float:
    if rule == "Bd":
        return (1 - 1 / r) / (1 - r ** (-n))
    return (n - 1) / n * (1 - 1 / r) / (1 - r ** (-(n - 1)))


@functools.lru_cache(maxsize=None)
def histograms(total: int, bins: int):
    if bins == 1:
        return ((total,),)
    return tuple(
        (first,) + tail
        for first in range(total + 1)
        for tail in histograms(total - first, bins - 1)
    )


def move(counts, source, target):
    result = list(counts); result[source] -= 1; result[target] += 1
    return tuple(result)


def degrees(modules, size, exceptional_internal, ordinary_cross, exceptional_cross):
    exceptional = (size - 1) * exceptional_internal + (modules - 1) * size * exceptional_cross
    ordinary = (size - 1) + (modules - 2) * size * ordinary_cross + size * exceptional_cross
    return exceptional, ordinary


def transitions(state, modules, size, parameters, fitness, rule):
    exceptional_internal, ordinary_cross, exceptional_cross = parameters
    exceptional_mutants, counts = state
    ordinary_mutants = sum(k * counts[k] for k in range(size + 1))
    n = modules * size
    total_mutants = exceptional_mutants + ordinary_mutants
    degree_e, degree_o = degrees(modules, size, *parameters)
    result = []
    if rule == "Bd":
        total_fitness = n + (fitness - 1) * total_mutants
        if exceptional_mutants < size:
            parent_mass = (
                exceptional_mutants * exceptional_internal / degree_e
                + ordinary_mutants * exceptional_cross / degree_o
            )
            rate = (size - exceptional_mutants) * fitness / total_fitness * parent_mass
            if rate:
                result.append(((exceptional_mutants + 1, counts), rate))
        if exceptional_mutants:
            parent_mass = (
                (size - exceptional_mutants) * exceptional_internal / degree_e
                + ((modules - 1) * size - ordinary_mutants) * exceptional_cross / degree_o
            )
            rate = exceptional_mutants / total_fitness * parent_mass
            if rate:
                result.append(((exceptional_mutants - 1, counts), rate))
        for k, multiplicity in enumerate(counts):
            if not multiplicity:
                continue
            other_mutants = ordinary_mutants - k
            other_residents = (modules - 2) * size - other_mutants
            if k < size:
                parent_mass = (
                    k / degree_o
                    + other_mutants * ordinary_cross / degree_o
                    + exceptional_mutants * exceptional_cross / degree_e
                )
                rate = multiplicity * (size - k) * fitness / total_fitness * parent_mass
                if rate:
                    result.append(((exceptional_mutants, move(counts, k, k + 1)), rate))
            if k:
                parent_mass = (
                    (size - k) / degree_o
                    + other_residents * ordinary_cross / degree_o
                    + (size - exceptional_mutants) * exceptional_cross / degree_e
                )
                rate = multiplicity * k / total_fitness * parent_mass
                if rate:
                    result.append(((exceptional_mutants, move(counts, k, k - 1)), rate))
    elif rule == "dB":
        if exceptional_mutants < size:
            mutant_mass = exceptional_mutants * exceptional_internal + ordinary_mutants * exceptional_cross
            resident_mass = (size - exceptional_mutants - 1) * exceptional_internal + ((modules - 1) * size - ordinary_mutants) * exceptional_cross
            if mutant_mass:
                rate = (size - exceptional_mutants) / n * fitness * mutant_mass / (fitness * mutant_mass + resident_mass)
                result.append(((exceptional_mutants + 1, counts), rate))
        if exceptional_mutants:
            mutant_mass = (exceptional_mutants - 1) * exceptional_internal + ordinary_mutants * exceptional_cross
            resident_mass = (size - exceptional_mutants) * exceptional_internal + ((modules - 1) * size - ordinary_mutants) * exceptional_cross
            if resident_mass:
                rate = exceptional_mutants / n * resident_mass / (fitness * mutant_mass + resident_mass)
                result.append(((exceptional_mutants - 1, counts), rate))
        for k, multiplicity in enumerate(counts):
            if not multiplicity:
                continue
            other_mutants = ordinary_mutants - k
            other_residents = (modules - 2) * size - other_mutants
            if k < size:
                mutant_mass = k + other_mutants * ordinary_cross + exceptional_mutants * exceptional_cross
                resident_mass = size - k - 1 + other_residents * ordinary_cross + (size - exceptional_mutants) * exceptional_cross
                if mutant_mass:
                    rate = multiplicity * (size - k) / n * fitness * mutant_mass / (fitness * mutant_mass + resident_mass)
                    result.append(((exceptional_mutants, move(counts, k, k + 1)), rate))
            if k:
                mutant_mass = k - 1 + other_mutants * ordinary_cross + exceptional_mutants * exceptional_cross
                resident_mass = size - k + other_residents * ordinary_cross + (size - exceptional_mutants) * exceptional_cross
                if resident_mass:
                    rate = multiplicity * k / n * resident_mass / (fitness * mutant_mass + resident_mass)
                    result.append(((exceptional_mutants, move(counts, k, k - 1)), rate))
    else:
        raise ValueError(rule)
    return result


def fixation(modules, size, parameters, fitness, rule):
    ordinary_modules = modules - 1
    empty_counts = (ordinary_modules,) + (0,) * size
    full_counts = (0,) * size + (ordinary_modules,)
    empty = (0, empty_counts); full = (size, full_counts)
    states = [
        (exceptional, counts)
        for exceptional in range(size + 1)
        for counts in histograms(ordinary_modules, size + 1)
        if (exceptional, counts) not in (empty, full)
    ]
    index = {state: i for i, state in enumerate(states)}
    rows, columns, data = [], [], []
    rhs = np.zeros(len(states))
    for state, source in index.items():
        changes = transitions(state, modules, size, parameters, fitness, rule)
        mass = sum(probability for _, probability in changes)
        if not mass > 0: raise AssertionError((state, changes))
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
    singleton_e = (1, empty_counts)
    singleton_counts = (ordinary_modules - 1, 1) + (0,) * (size - 1)
    singleton_o = (0, singleton_counts)
    n = modules * size
    average = (size * values[index[singleton_e]] + ordinary_modules * size * values[index[singleton_o]]) / n
    return float(average), residual

