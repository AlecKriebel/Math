#!/usr/bin/env python3
"""Enumerate unweighted gadgets and optimize arbitrary portal loads.

The isolated subset chains are solved once per graph.  Since the optimized
separator is monotone in the gate-odds product K, the inner search maximizes
K over the positive portal simplex.
"""

from __future__ import annotations

import argparse
import math

import networkx as nx
import numpy as np
from scipy.optimize import differential_evolution

from search_invariant_gadgets import fixation_vector, max_separator


def graph_matrix(graph: nx.Graph) -> np.ndarray:
    graph = nx.convert_node_labels_to_integers(graph, ordering="sorted")
    matrix = np.zeros((len(graph), len(graph)))
    for left, right in graph.edges():
        matrix[left, right] = matrix[right, left] = 1.0
    return matrix


def invariants(weights: np.ndarray, fitness: float) -> tuple[float, float, np.ndarray, np.ndarray, np.ndarray]:
    degrees = weights.sum(axis=1)
    p = 1.0 - 1.0 / fitness
    bd_plus = fixation_vector(weights, fitness, "Bd")
    bd_minus = fixation_vector(weights, 1.0 / fitness, "Bd")
    db_plus = fixation_vector(weights, fitness, "dB")
    db_minus = fixation_vector(weights, 1.0 / fitness, "dB")
    return bd_plus.mean() / p, db_plus.mean() / p, degrees, bd_minus, db_minus


def portal_product(
    logs: np.ndarray,
    degrees: np.ndarray,
    bd_minus: np.ndarray,
    db_minus: np.ndarray,
    fitness: float,
) -> float:
    centered = logs - logs.mean()
    portals = np.exp(centered)
    return float(
        fitness
        * (fitness - 1.0) ** 2
        * np.sum(portals / degrees)
        * np.sum(portals)
        / (np.sum(portals * bd_minus) * np.sum(portals * db_minus / degrees))
    )


def optimize_graph(graph: nx.Graph, fitness: float, bound: float, seed: int, maxiter: int) -> dict[str, object]:
    weights = graph_matrix(graph)
    a_bd, a_db, degrees, bd_minus, db_minus = invariants(weights, fitness)
    order = len(weights)

    def objective(parameters: np.ndarray) -> float:
        return -portal_product(np.r_[0.0, parameters], degrees, bd_minus, db_minus, fitness)

    result = differential_evolution(
        objective,
        [(-bound, bound)] * (order - 1),
        seed=seed,
        maxiter=maxiter,
        popsize=8,
        polish=True,
        tol=1e-10,
        updating="immediate",
        workers=1,
    )
    logs = np.r_[0.0, result.x]
    portals = np.exp(logs - logs.mean())
    product = portal_product(logs, degrees, bd_minus, db_minus, fitness)
    separator, z_bd = max_separator(a_bd, a_db, product, fitness)
    return {
        "separator": order * separator,
        "K": product,
        "A_Bd": a_bd,
        "A_dB": a_db,
        "Z_Bd": z_bd,
        "portals": portals.tolist(),
        "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
        "edges": list(graph.edges()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-order", type=int, default=3)
    parser.add_argument("--max-order", type=int, default=6)
    parser.add_argument("--fitness", type=float, default=1.5028569127905696)
    parser.add_argument("--bound", type=float, default=10.0)
    parser.add_argument("--seed", type=int, default=20260808)
    parser.add_argument("--maxiter", type=int, default=100)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()
    rows: list[dict[str, object]] = []
    graphs = [
        graph
        for graph in nx.graph_atlas_g()
        if args.min_order <= graph.number_of_nodes() <= args.max_order and nx.is_connected(graph)
    ]
    for offset, graph in enumerate(graphs):
        row = optimize_graph(graph, args.fitness, args.bound, args.seed + offset, args.maxiter)
        rows.append(row)
        if (offset + 1) % 25 == 0:
            print(f"processed {offset + 1}/{len(graphs)}", flush=True)
    rows.sort(key=lambda row: float(row["separator"]), reverse=True)
    for row in rows[: args.top]:
        print(row)


if __name__ == "__main__":
    main()
