#!/usr/bin/env python
"""Floating-point atlas screen for dB-dual Poisson-certificate degree.

This is a discovery script, not an exact proof.  The companion C5 verifier
contains the exact smallest hierarchy obstruction found by this screen.
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

import networkx as nx
import numpy as np
from scipy.optimize import linprog


PARENT = Path(__file__).resolve().parents[1] / "stationary_inequality"
sys.path.insert(0, str(PARENT))
from explore_level_reflection import dual_generator, stationary_distribution  # noqa: E402


def popcount(mask: int) -> int:
    return bin(int(mask)).count("1")


def monomials(order: int, degree: int, weights, edge_only: bool = False):
    result = []
    for size in range(1, degree + 1):
        for vertices in combinations(range(order), size):
            if size == 2 and edge_only and not weights[vertices[0], vertices[1]]:
                continue
            result.append(sum(1 << vertex for vertex in vertices))
    return result


def certificate_feasible(graph, degree: int, include_full: bool, edge_only=False):
    weights = nx.to_numpy_array(graph)
    order = len(weights)
    generator = dual_generator(weights, 2.0)
    states = list(range(1, 1 << order))
    basis = monomials(order, degree, weights, edge_only=edge_only)
    evaluations = np.array(
        [[float((state & mask) == mask) for mask in basis] for state in states]
    )
    drift = generator @ evaluations
    complete_mean = (order - 1) * 2 ** (order - 2) / (2 ** (order - 1) - 1)
    target = np.array([popcount(state) - complete_mean for state in states])
    rows = np.arange(len(states)) if include_full else np.arange(len(states) - 1)
    result = linprog(
        np.zeros(len(basis)),
        A_ub=-drift[rows],
        b_ub=-target[rows],
        bounds=[(None, None)] * len(basis),
        method="highs",
    )
    return result.success


def actual_mean(graph) -> tuple[float, float]:
    weights = nx.to_numpy_array(graph)
    order = len(weights)
    invariant = stationary_distribution(weights, 2.0)
    mean = sum(
        popcount(state) * invariant[state - 1]
        for state in range(1, 1 << order)
    )
    complete = (order - 1) * 2 ** (order - 2) / (2 ** (order - 1) - 1)
    return mean, complete


def main() -> None:
    atlas = nx.graph_atlas_g()
    for order in range(3, 7):
        graphs = [
            graph
            for graph in atlas
            if len(graph) == order and nx.is_connected(graph)
        ]
        failures = {}
        for degree in range(1, order):
            for include_full in (False, True):
                failures[degree, include_full] = sum(
                    not certificate_feasible(graph, degree, include_full)
                    for graph in graphs
                )
        maximum_actual_excess = max(
            actual_mean(graph)[0] - actual_mean(graph)[1] for graph in graphs
        )
        print(
            f"n={order}: graphs={len(graphs)}; failures={failures}; "
            f"max actual excess={maximum_actual_excess:.3e}"
        )

    print("NOTE: LP and stationary calculations in this script are numerical.")
    print("Run verify_c5_hierarchy.py for exact C5 claims.")


if __name__ == "__main__":
    main()

