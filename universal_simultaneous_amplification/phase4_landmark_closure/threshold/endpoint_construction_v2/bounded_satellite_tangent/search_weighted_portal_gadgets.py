#!/usr/bin/env python3
"""Hostile discovery search over weighted gadgets and nonuniform portals.

This script uses numerical local linear algebra only for discovery.  Any
positive result must be reconstructed over exact rational/algebraic weights.
"""

from __future__ import annotations

import argparse
import math

import networkx as nx
import numpy as np
from scipy.optimize import differential_evolution


def fixation_vector(weights: np.ndarray, fitness: float, rule: str) -> np.ndarray:
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
        else:
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
        exit_rate = sum(rates.values())
        matrix[row, row] = exit_rate
        for target, rate in rates.items():
            if target == full:
                rhs[row] += rate
            elif target:
                matrix[row, index[target]] -= rate
    solution = np.linalg.solve(matrix, rhs)
    return np.array([solution[index[1 << vertex]] for vertex in range(n)])


def decode(graph: nx.Graph, parameters: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    graph = nx.convert_node_labels_to_integers(graph, ordering="sorted")
    edges = list(graph.edges())
    edge_logs = np.r_[0.0, parameters[: len(edges) - 1]]
    offset = len(edges) - 1
    portal_logs = np.r_[0.0, parameters[offset : offset + graph.number_of_nodes() - 1]]
    log_scale = parameters[-1]
    edge_logs -= edge_logs.mean()
    portal_logs -= portal_logs.mean()
    matrix = np.zeros((graph.number_of_nodes(), graph.number_of_nodes()))
    for (left, right), value in zip(edges, np.exp(edge_logs)):
        matrix[left, right] = matrix[right, left] = value
    return matrix, np.exp(portal_logs), math.exp(float(log_scale))


def tangent_score(graph: nx.Graph, parameters: np.ndarray, fitness: float) -> tuple[float, ...]:
    weights, portals, scale = decode(graph, parameters)
    degrees = weights.sum(axis=1)
    bd_plus = fixation_vector(weights, fitness, "Bd")
    bd_minus = fixation_vector(weights, 1.0 / fitness, "Bd")
    db_plus = fixation_vector(weights, fitness, "dB")
    db_minus = fixation_vector(weights, 1.0 / fitness, "dB")
    order = len(weights)
    p = 1.0 - 1.0 / fitness
    z_bd = (
        scale
        * (fitness - 1.0)
        * np.sum(portals / degrees)
        / np.sum(portals * bd_minus)
    )
    z_db = (
        fitness
        * (fitness - 1.0)
        * np.sum(portals)
        / (scale * np.sum(portals * db_minus / degrees))
    )
    f_bd = order * (bd_plus.mean() * z_bd / (p * (1.0 + z_bd)) - 1.0)
    f_db = order * (db_plus.mean() * z_db / (p * (1.0 + z_db)) - 1.0)
    leaf_ratio = max(0.0, (fitness - 1.0) / fitness * (f_db - f_bd))
    balanced = min(f_bd + leaf_ratio / (fitness - 1.0), f_db - leaf_ratio)
    separator = f_db + (fitness - 1.0) * f_bd
    return balanced, separator, f_bd, f_db, leaf_ratio, scale


def optimize(graph: nx.Graph, fitness: float, seed: int, bound: float) -> dict[str, object]:
    dimension = graph.number_of_edges() - 1 + graph.number_of_nodes() - 1 + 1
    bounds = [(-bound, bound)] * dimension

    def objective(parameters: np.ndarray) -> float:
        try:
            return -tangent_score(graph, parameters, fitness)[0]
        except np.linalg.LinAlgError:
            return 1e6

    result = differential_evolution(
        objective,
        bounds,
        seed=seed,
        maxiter=180,
        popsize=10,
        polish=True,
        updating="immediate",
        workers=1,
        tol=1e-10,
    )
    score = tangent_score(graph, result.x, fitness)
    weights, portals, _ = decode(graph, result.x)
    return {
        "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
        "n": graph.number_of_nodes(),
        "m": graph.number_of_edges(),
        "balanced": score[0],
        "separator": score[1],
        "Bd": score[2],
        "dB": score[3],
        "lambda": score[4],
        "scale": score[5],
        "weights": [weights[left, right] for left, right in graph.edges()],
        "portals": portals.tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=4)
    parser.add_argument("--fitness", type=float, default=1.5028569127905696)
    parser.add_argument("--seed", type=int, default=20260808)
    parser.add_argument("--bound", type=float, default=5.0)
    args = parser.parse_args()
    graphs = [
        graph
        for graph in nx.graph_atlas_g()
        if graph.number_of_nodes() == args.order and nx.is_connected(graph)
    ]
    rows = [optimize(graph, args.fitness, args.seed + k, args.bound) for k, graph in enumerate(graphs)]
    rows.sort(key=lambda row: float(row["balanced"]), reverse=True)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()

