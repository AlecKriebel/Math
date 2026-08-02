#!/usr/bin/env python3
"""Sparse fixation solver for finite equitable weighted vertex classes.

Class ``a`` has ``sizes[a]`` vertices.  Distinct vertices in classes ``a,b``
are joined with common symmetric weight ``weights[a,b]``.  Mutant counts by
class form a strongly lumpable chain because the raw transition rates below
depend only on those counts.  The formulas are direct sums of the update rules.
"""

from __future__ import annotations

import itertools

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as spla


def baseline(n: int, r: float, rule: str) -> float:
    if rule == "Bd":
        return (1 - 1 / r) / (1 - r ** (-n))
    return (n - 1) / n * (1 - 1 / r) / (1 - r ** (-(n - 1)))


def transitions(state, sizes, weights, fitness, rule):
    state = np.asarray(state, dtype=int)
    sizes = np.asarray(sizes, dtype=int)
    weights = np.asarray(weights, dtype=float)
    classes = len(sizes)
    n = int(sizes.sum())
    degrees = (weights * sizes[None, :]).sum(axis=1) - np.diag(weights)
    result = []
    if rule == "Bd":
        total_fitness = n + (fitness - 1) * int(state.sum())
        for target_class in range(classes):
            if state[target_class] < sizes[target_class]:
                rate = fitness * (sizes[target_class] - state[target_class]) / total_fitness * sum(
                    state[parent_class] * weights[parent_class, target_class] / degrees[parent_class]
                    for parent_class in range(classes)
                )
                if rate:
                    target = state.copy(); target[target_class] += 1
                    result.append((tuple(target), float(rate)))
            if state[target_class]:
                rate = state[target_class] / total_fitness * sum(
                    (sizes[parent_class] - state[parent_class])
                    * weights[parent_class, target_class]
                    / degrees[parent_class]
                    for parent_class in range(classes)
                )
                if rate:
                    target = state.copy(); target[target_class] -= 1
                    result.append((tuple(target), float(rate)))
    elif rule == "dB":
        for target_class in range(classes):
            if state[target_class] < sizes[target_class]:
                mutant_mass = sum(state[b] * weights[b, target_class] for b in range(classes))
                resident_mass = sum(
                    (sizes[b] - state[b] - (1 if b == target_class else 0)) * weights[b, target_class]
                    for b in range(classes)
                )
                if mutant_mass:
                    rate = (sizes[target_class] - state[target_class]) / n * fitness * mutant_mass / (fitness * mutant_mass + resident_mass)
                    target = state.copy(); target[target_class] += 1
                    result.append((tuple(target), float(rate)))
            if state[target_class]:
                mutant_mass = sum(
                    (state[b] - (1 if b == target_class else 0)) * weights[b, target_class]
                    for b in range(classes)
                )
                resident_mass = sum((sizes[b] - state[b]) * weights[b, target_class] for b in range(classes))
                if resident_mass:
                    rate = state[target_class] / n * resident_mass / (fitness * mutant_mass + resident_mass)
                    target = state.copy(); target[target_class] -= 1
                    result.append((tuple(target), float(rate)))
    else:
        raise ValueError(rule)
    return result


def fixation(sizes, weights, fitness, rule):
    sizes = tuple(sizes); empty = (0,) * len(sizes); full = sizes
    states = [state for state in itertools.product(*(range(size + 1) for size in sizes)) if state not in (empty, full)]
    index = {state: i for i, state in enumerate(states)}
    rows, columns, data = [], [], []
    rhs = np.zeros(len(states))
    for state, source in index.items():
        changes = transitions(state, sizes, weights, fitness, rule)
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
    n = sum(sizes)
    average = 0.0
    for vertex_class, size in enumerate(sizes):
        singleton = tuple(1 if a == vertex_class else 0 for a in range(len(sizes)))
        average += size * values[index[singleton]] / n
    return float(average), residual

