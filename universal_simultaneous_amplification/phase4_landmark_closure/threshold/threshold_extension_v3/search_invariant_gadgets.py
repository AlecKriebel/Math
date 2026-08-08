#!/usr/bin/env python3
"""Hostile random/local search for a bounded-gadget threshold extension.

This is discovery code.  It derives every isolated fixation vector from the
full subset chain and evaluates the complete first-order separator, including
the uniform-singleton subtraction.  A reported numerical lead is not a
theorem until reconstructed exactly.
"""

from __future__ import annotations

import argparse
import itertools
import math

import networkx as nx
import numpy as np
from scipy.optimize import differential_evolution, minimize_scalar


def fixation_vector(weights: np.ndarray, fitness: float, rule: str) -> np.ndarray:
    """Fixation from every singleton, using only type-changing rates."""
    n = len(weights)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {mask: row for row, mask in enumerate(states)}
    matrix = np.zeros((len(states), len(states)))
    rhs = np.zeros(len(states))
    degrees = weights.sum(axis=1)
    for mask, row in index.items():
        mutant = np.array([(mask >> vertex) & 1 for vertex in range(n)])
        rates: dict[int, float] = {}
        if rule == "Bd":
            for parent in range(n):
                parent_fitness = fitness if mutant[parent] else 1.0
                for target in np.flatnonzero(weights[parent]):
                    if mutant[parent] != mutant[target]:
                        next_mask = mask ^ (1 << int(target))
                        rates[next_mask] = rates.get(next_mask, 0.0) + (
                            parent_fitness * weights[parent, target] / degrees[parent]
                        )
        elif rule == "dB":
            vertex_fitness = np.where(mutant, fitness, 1.0)
            for target in range(n):
                denominator = float(weights[target] @ vertex_fitness)
                for parent in np.flatnonzero(weights[target]):
                    if mutant[parent] != mutant[target]:
                        next_mask = mask ^ (1 << int(target))
                        rates[next_mask] = rates.get(next_mask, 0.0) + (
                            vertex_fitness[parent]
                            * weights[target, parent]
                            / denominator
                        )
        else:
            raise ValueError(rule)
        exit_rate = sum(rates.values())
        matrix[row, row] = exit_rate
        for target, rate in rates.items():
            if target == full:
                rhs[row] += rate
            elif target:
                matrix[row, index[target]] -= rate
    solution = np.linalg.solve(matrix, rhs)
    return np.array([solution[index[1 << vertex]] for vertex in range(n)])


def max_separator(a_bd: float, a_db: float, product: float, fitness: float) -> tuple[float, float]:
    """Return max separator per vertex and its Z_B scale."""
    def separator(log_z: float) -> float:
        z = math.exp(log_z)
        return (
            a_db * product / (product + z)
            + (fitness - 1.0) * a_bd * z / (1.0 + z)
            - fitness
        )

    result = minimize_scalar(
        lambda value: -separator(value),
        bounds=(-35.0, 35.0),
        method="bounded",
        options={"xatol": 1e-13},
    )
    candidates = [(-35.0, separator(-35.0)), (35.0, separator(35.0)), (result.x, -result.fun)]
    log_z, score = max(candidates, key=lambda item: item[1])
    return score, math.exp(log_z)


def gadget_score(weights: np.ndarray, portals: np.ndarray, fitness: float) -> dict[str, float]:
    degrees = weights.sum(axis=1)
    bd_plus = fixation_vector(weights, fitness, "Bd")
    bd_minus = fixation_vector(weights, 1.0 / fitness, "Bd")
    db_plus = fixation_vector(weights, fitness, "dB")
    db_minus = fixation_vector(weights, 1.0 / fitness, "dB")
    p = 1.0 - 1.0 / fitness
    a_bd = float(bd_plus.mean() / p)
    a_db = float(db_plus.mean() / p)
    product = float(
        fitness
        * (fitness - 1.0) ** 2
        * np.sum(portals / degrees)
        * np.sum(portals)
        / (np.sum(portals * bd_minus) * np.sum(portals * db_minus / degrees))
    )
    separator, z_bd = max_separator(a_bd, a_db, product, fitness)
    z_db = product / z_bd
    order = len(weights)
    f_bd = order * (a_bd * z_bd / (1.0 + z_bd) - 1.0)
    f_db = order * (a_db * z_db / (1.0 + z_db) - 1.0)
    leaf_ratio = max(0.0, (fitness - 1.0) * (f_db - f_bd) / fitness)
    balanced = min(f_bd + leaf_ratio / (fitness - 1.0), f_db - leaf_ratio)
    return {
        "balanced": balanced,
        "separator": order * separator,
        "Bd": f_bd,
        "dB": f_db,
        "lambda": leaf_ratio,
        "A_Bd": a_bd,
        "A_dB": a_db,
        "K": product,
        "Z_Bd": z_bd,
    }


def support_graph(name: str, order: int) -> nx.Graph:
    if name == "path":
        return nx.path_graph(order)
    if name == "cycle":
        return nx.cycle_graph(order)
    if name == "star":
        return nx.star_graph(order - 1)
    if name == "complete":
        return nx.complete_graph(order)
    if name == "bipartite":
        return nx.complete_bipartite_graph(order // 2, order - order // 2)
    raise ValueError(name)


def decode(graph: nx.Graph, parameters: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    graph = nx.convert_node_labels_to_integers(graph, ordering="sorted")
    edges = list(graph.edges())
    edge_logs = np.r_[0.0, parameters[: len(edges) - 1]]
    portal_logs = np.r_[0.0, parameters[len(edges) - 1 :]]
    edge_logs -= edge_logs.mean()
    portal_logs -= portal_logs.mean()
    weights = np.zeros((len(graph), len(graph)))
    for (left, right), value in zip(edges, np.exp(edge_logs)):
        weights[left, right] = weights[right, left] = value
    return weights, np.exp(portal_logs)


def optimize(
    graph: nx.Graph,
    fitness: float,
    bound: float,
    seed: int,
    maxiter: int,
    objective_name: str,
) -> dict[str, object]:
    dimension = graph.number_of_edges() - 1 + graph.number_of_nodes() - 1

    def objective(parameters: np.ndarray) -> float:
        try:
            weights, portals = decode(graph, parameters)
            return -gadget_score(weights, portals, fitness)[objective_name]
        except (np.linalg.LinAlgError, FloatingPointError, ZeroDivisionError):
            return 1e9

    result = differential_evolution(
        objective,
        [(-bound, bound)] * dimension,
        seed=seed,
        maxiter=maxiter,
        popsize=8,
        polish=True,
        tol=1e-9,
        updating="immediate",
        workers=1,
    )
    weights, portals = decode(graph, result.x)
    score = gadget_score(weights, portals, fitness)
    return {
        **score,
        "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
        "edges": list(graph.edges()),
        "weights": [float(weights[left, right]) for left, right in graph.edges()],
        "portals": portals.tolist(),
        "success": bool(result.success),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=5)
    parser.add_argument("--fitness", type=float, default=1.5028569127905696)
    parser.add_argument("--bound", type=float, default=6.0)
    parser.add_argument("--seed", type=int, default=20260808)
    parser.add_argument("--maxiter", type=int, default=80)
    parser.add_argument("--objective", choices=["balanced", "separator"], default="separator")
    parser.add_argument(
        "--supports",
        nargs="+",
        default=["path", "cycle", "star", "bipartite", "complete"],
    )
    args = parser.parse_args()
    for offset, name in enumerate(args.supports):
        graph = support_graph(name, args.order)
        result = optimize(
            graph,
            args.fitness,
            args.bound,
            args.seed + offset,
            args.maxiter,
            args.objective,
        )
        print(name, result, flush=True)


if __name__ == "__main__":
    main()
