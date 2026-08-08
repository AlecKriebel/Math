#!/usr/bin/env python3
"""Numerical hostile search for fixed-degree spatial portal episodes.

Discovery only.  The full 2^Q-1 subset resolvent is solved sparsely; no
independent-lineage or cavity closure is imposed.
"""

from __future__ import annotations

import argparse

import networkx as nx
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def episode_hitting(graph, rule, r, blade_load, portal_load, z):
    q = len(graph)
    degree = graph.degree(0)
    if any(graph.degree(a) != degree for a in graph):
        raise ValueError("portal graph must be regular")
    edge = portal_load / degree
    weighted_degree = blade_load + portal_load
    neighbors = [tuple(graph.neighbors(a)) for a in range(q)]
    states = (1 << q) - 1
    rows, columns, values = [], [], []
    rhs = np.zeros(states)

    for mask in range(1, 1 << q):
        row = mask - 1
        active = [a for a in range(q) if mask >> a & 1]
        transitions = []
        if rule == "Bd":
            for a in active:
                mutant_neighbors = sum(mask >> b & 1 for b in neighbors[a])
                transitions.append((
                    mask ^ (1 << a),
                    blade_load
                    + (degree - mutant_neighbors) * edge / weighted_degree,
                ))
            for b in range(q):
                if not (mask >> b & 1):
                    mutant_neighbors = sum(mask >> a & 1 for a in neighbors[b])
                    transitions.append((
                        mask | (1 << b),
                        r * mutant_neighbors * edge / weighted_degree,
                    ))
            killing = (
                len(active) * r**2 * blade_load
                / ((r + 1) * weighted_degree) * (1 - z)
            )
        elif rule == "dB":
            for a in active:
                mutant_neighbors = sum(mask >> b & 1 for b in neighbors[a])
                resident_mass = blade_load + (degree - mutant_neighbors) * edge
                transitions.append((
                    mask ^ (1 << a),
                    resident_mass
                    / (resident_mass + r * mutant_neighbors * edge),
                ))
            for b in range(q):
                if not (mask >> b & 1):
                    mutant_neighbors = sum(mask >> a & 1 for a in neighbors[b])
                    transitions.append((
                        mask | (1 << b),
                        r * mutant_neighbors * edge
                        / (blade_load + (degree - mutant_neighbors) * edge
                           + r * mutant_neighbors * edge),
                    ))
            killing = len(active) * r * blade_load / 2 * (1 - z)
        else:
            raise ValueError(rule)

        rows.append(row); columns.append(row)
        values.append(killing + sum(rate for _, rate in transitions))
        rhs[row] = killing
        for nxt, rate in transitions:
            if nxt:
                rows.append(row); columns.append(nxt - 1); values.append(-rate)
    matrix = coo_matrix((values, (rows, columns)), shape=(states, states)).tocsr()
    return spsolve(matrix, rhs)


def test_margins(graph, r, blade_load, portal_load):
    q = len(graph)
    total_degree = blade_load + portal_load
    hb = episode_hitting(graph, "Bd", r, blade_load, portal_load, 1 / r**2)
    mean_hb = np.mean([hb[(1 << a) - 1] for a in range(q)])
    db = 1 / (1 + r * (r + 1) * total_degree * mean_hb)
    tb = 1 / r**2 - db

    hd = episode_hitting(
        graph, "dB", r, blade_load, portal_load, (2 - r) / r
    )
    mean_hd = np.mean([hd[(1 << a) - 1] for a in range(q)])
    dd = 1 / (1 + 2 * r**2 * mean_hd / total_degree)
    td = (2 - r) / r - dd
    return tb, td


def named_graph(name, q):
    if name == "cycle":
        return nx.cycle_graph(q)
    if name == "cube":
        return nx.cubical_graph()
    if name == "petersen":
        return nx.petersen_graph()
    if name == "random_regular":
        return nx.random_regular_graph(3, q, seed=17)
    raise ValueError(name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", choices=(
        "cycle", "cube", "petersen", "random_regular"
    ), default="cycle")
    parser.add_argument("--portals", type=int, default=8)
    parser.add_argument("--fitness", type=float, default=31 / 20)
    parser.add_argument("--grid", type=int, default=10)
    args = parser.parse_args()
    graph = named_graph(args.graph, args.portals)
    best = (-np.inf, None)
    for blade_load in np.geomspace(0.04, 3.0, args.grid):
        for portal_load in np.geomspace(0.04, 5.0, args.grid):
            tb, td = test_margins(graph, args.fitness, blade_load, portal_load)
            candidate = min(tb, td)
            if candidate > best[0]:
                best = (candidate, (blade_load, portal_load, tb, td))
    print("best min PGF-test margin", best[0])
    print("B,H,T_B,T_D", best[1])


if __name__ == "__main__":
    main()
