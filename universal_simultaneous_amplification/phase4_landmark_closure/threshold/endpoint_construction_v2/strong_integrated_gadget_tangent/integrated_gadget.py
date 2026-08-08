#!/usr/bin/env python3
"""Strong integrated finite-gadget tangent coefficients.

A gadget vertex ``i`` has portal edge weight ``x_i`` to every large-clique
vertex and internal edge ``C*a_ij`` to gadget vertex ``j``.  The routines
below solve the exact limiting local chain and include the ordinary-singleton
Poisson correction.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TangentResult:
    Bd: float
    dB: float
    separator: float
    balanced: float
    leaf_ratio: float
    local_Bd: np.ndarray
    local_dB: np.ndarray


def local_fixation(
    internal: np.ndarray, portal: np.ndarray, fitness: float, rule: str
) -> np.ndarray:
    """Fixation-through-core probability from every gadget singleton."""
    internal = np.asarray(internal, dtype=float)
    portal = np.asarray(portal, dtype=float)
    order = len(portal)
    assert internal.shape == (order, order)
    assert np.allclose(internal, internal.T)
    assert np.all(internal >= 0.0) and np.all(portal >= 0.0)
    degrees = portal + internal.sum(axis=1)
    if np.any(degrees <= 0.0) or not np.any(portal > 0.0):
        raise ValueError("every gadget degree and at least one portal must be positive")

    full = (1 << order) - 1
    states = list(range(1, full + 1))
    index = {mask: row for row, mask in enumerate(states)}
    matrix = np.zeros((len(states), len(states)))
    rhs = np.zeros(len(states))
    p = 1.0 - 1.0 / fitness

    for mask, row in index.items():
        mutant = np.array([(mask >> vertex) & 1 for vertex in range(order)])
        changes: dict[int, float] = {}
        if rule == "Bd":
            for parent in range(order):
                parent_fitness = fitness if mutant[parent] else 1.0
                for target in np.flatnonzero(internal[parent]):
                    if mutant[parent] != mutant[target]:
                        next_mask = mask ^ (1 << int(target))
                        changes[next_mask] = changes.get(next_mask, 0.0) + (
                            parent_fitness
                            * internal[parent, target]
                            / degrees[parent]
                        )
            # Resident core parents recover mutant gadget vertices.
            for target in np.flatnonzero(mutant):
                next_mask = mask ^ (1 << int(target))
                changes[next_mask] = changes.get(next_mask, 0.0) + portal[target]
            mark_rate = fitness * p * float(np.sum(portal[mutant == 1] / degrees[mutant == 1]))
        elif rule == "dB":
            vertex_fitness = np.where(mutant, fitness, 1.0)
            for target in range(order):
                denominator = portal[target] + float(internal[target] @ vertex_fitness)
                if mutant[target]:
                    recovery = portal[target] + float(
                        np.sum(internal[target, mutant == 0])
                    )
                    if recovery:
                        changes[mask ^ (1 << target)] = recovery / denominator
                else:
                    invasion = fitness * float(np.sum(internal[target, mutant == 1]))
                    if invasion:
                        changes[mask ^ (1 << target)] = invasion / denominator
            mark_rate = fitness * p * float(np.sum(portal[mutant == 1]))
        else:
            raise ValueError(rule)

        exit_rate = mark_rate + sum(changes.values())
        if not exit_rate > 0.0:
            raise np.linalg.LinAlgError("nonabsorbing local class")
        matrix[row, row] = exit_rate
        rhs[row] = mark_rate
        for target, rate in changes.items():
            if target:
                matrix[row, index[target]] -= rate

    solution = np.linalg.solve(matrix, rhs)
    residual = np.max(np.abs(matrix @ solution - rhs))
    if residual > 2e-8 or np.any(solution < -1e-8) or np.any(solution > 1 + 1e-8):
        raise np.linalg.LinAlgError(f"bad local solve residual={residual}")
    return np.array([solution[index[1 << vertex]] for vertex in range(order)])


def tangent_coefficients(
    internal: np.ndarray, portal: np.ndarray, fitness: float
) -> TangentResult:
    """Return the full Bd/dB dilute defect correction vector."""
    internal = np.asarray(internal, dtype=float)
    portal = np.asarray(portal, dtype=float)
    order = len(portal)
    degrees = portal + internal.sum(axis=1)
    p = 1.0 - 1.0 / fitness
    local_bd = local_fixation(internal, portal, fitness, "Bd")
    local_db = local_fixation(internal, portal, fitness, "dB")

    source_bd = fitness * float(portal @ local_bd) - (fitness - 1.0) * float(
        np.sum(portal / degrees)
    )
    source_db = (
        fitness * float((portal / degrees) @ local_db)
        - (fitness - 1.0) * (float(np.sum(portal)) + fitness - 1.0)
    )
    bd = float(np.sum(local_bd)) / p - order + source_bd / (fitness - 1.0) ** 2
    db = (
        float(np.sum(local_db)) / p
        - order
        + 1.0
        + source_db / (fitness - 1.0) ** 2
    )
    separator = db + (fitness - 1.0) * bd
    leaf_ratio = max(0.0, (fitness - 1.0) / fitness * (db - bd))
    balanced = min(bd + leaf_ratio / (fitness - 1.0), db - leaf_ratio)
    return TangentResult(bd, db, separator, balanced, leaf_ratio, local_bd, local_db)


def decode_complete(order: int, parameters: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Decode logarithmic complete-support internal and portal weights."""
    parameters = np.asarray(parameters, dtype=float)
    edge_count = order * (order - 1) // 2
    if len(parameters) != edge_count + order:
        raise ValueError((len(parameters), edge_count + order))
    internal = np.zeros((order, order))
    cursor = 0
    for left in range(order):
        for right in range(left + 1, order):
            value = np.exp(parameters[cursor])
            cursor += 1
            internal[left, right] = internal[right, left] = value
    portal = np.exp(parameters[cursor:])
    return internal, portal
