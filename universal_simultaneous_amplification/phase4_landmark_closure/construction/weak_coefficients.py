#!/usr/bin/env python3
"""Numerical neutral-pair calculation of exact weak-selection criteria.

The equations are the first-principles remeeting identities derived in the
inherited weak-selection note.  Floating-point output is reconnaissance; a
candidate must later be checked in exact rational arithmetic.
"""

from __future__ import annotations

import itertools

import numpy as np
import scipy.linalg


def effective_size(weights: np.ndarray, rule: str) -> tuple[float, float]:
    weights = np.asarray(weights, dtype=float)
    n = len(weights)
    degrees = weights.sum(axis=1)
    if np.any(degrees <= 0) or not np.allclose(weights, weights.T) or np.any(np.diag(weights)):
        raise ValueError("invalid weight matrix")
    if rule == "Bd":
        rates = weights / degrees[None, :]
        inverse_degree_sum = np.sum(1 / degrees)
        stationary = (1 / degrees) / inverse_degree_sum
    elif rule == "dB":
        rates = weights / degrees[:, None]
        stationary = degrees / degrees.sum()
    else:
        raise ValueError(rule)
    exit_rates = rates.sum(axis=1)
    pairs = list(itertools.combinations(range(n), 2))
    index = {pair: p for p, pair in enumerate(pairs)}
    matrix = np.zeros((len(pairs), len(pairs)))
    rhs = np.ones(len(pairs))

    def pair_index(i: int, j: int):
        if i == j:
            return None
        return index[(i, j) if i < j else (j, i)]

    for (i, j), row in index.items():
        matrix[row, row] = exit_rates[i] + exit_rates[j]
        for k in range(n):
            target = pair_index(k, j)
            if target is not None:
                matrix[row, target] -= rates[i, k]
            target = pair_index(i, k)
            if target is not None:
                matrix[row, target] -= rates[j, k]
    meeting = scipy.linalg.solve(matrix, rhs, assume_a="gen", check_finite=False)
    residual = float(np.max(np.abs(matrix @ meeting - rhs)))
    remeeting = np.empty(n)
    for i in range(n):
        remeeting[i] = 1 / (2 * exit_rates[i]) + sum(
            rates[i, j] / exit_rates[i] * (0 if i == j else meeting[pair_index(i, j)])
            for j in range(n)
        )
    effective = 2 * np.sum(stationary * exit_rates * remeeting)
    return float(effective), residual


def weak_excesses(weights: np.ndarray) -> tuple[float, float]:
    n = len(weights)
    return tuple((effective_size(weights, rule)[0] - n) / (2 * n) for rule in ("Bd", "dB"))

