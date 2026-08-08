#!/usr/bin/env python3
"""Exact local chains plus one-dimensional scale optimization.

The graph atlas supplies connected unweighted internal gadgets.  Every local
fixation vector is solved exactly over QQ from the Bd/dB definitions.  Only
the final optimization over the positive common scale is floating-point and
is used for hostile discovery, not as a universal proof.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import networkx as nx
from flint import fmpq, fmpq_mat
from scipy.optimize import minimize_scalar


Q = fmpq
R = Q(3, 2)


def fixation_vector(graph: nx.Graph, fitness: fmpq, rule: str) -> list[fmpq]:
    """Return exact singleton fixation values from the definition."""
    graph = nx.convert_node_labels_to_integers(graph, ordering="sorted")
    n = graph.number_of_nodes()
    full = (1 << n) - 1
    transient = list(range(1, full))
    index = {mask: row for row, mask in enumerate(transient)}
    adjacency = [list(graph.neighbors(vertex)) for vertex in range(n)]
    degrees = [len(row) for row in adjacency]
    matrix = fmpq_mat(len(transient), len(transient))
    rhs = fmpq_mat(len(transient), 1)

    for mask, row in index.items():
        mutant = [(mask >> vertex) & 1 for vertex in range(n)]
        rates: dict[int, fmpq] = {}
        if rule == "Bd":
            # The statewise total-fitness factor cancels in the embedded
            # type-changing chain.
            for parent in range(n):
                parent_fitness = fitness if mutant[parent] else Q(1)
                for target in adjacency[parent]:
                    if mutant[parent] != mutant[target]:
                        next_mask = mask ^ (1 << target)
                        rates[next_mask] = rates.get(next_mask, Q(0)) + (
                            parent_fitness / degrees[parent]
                        )
        elif rule == "dB":
            # The common uniform-death factor likewise cancels.
            for target in range(n):
                denominator = sum(
                    (fitness if mutant[parent] else Q(1))
                    for parent in adjacency[target]
                )
                for parent in adjacency[target]:
                    if mutant[parent] != mutant[target]:
                        parent_fitness = fitness if mutant[parent] else Q(1)
                        next_mask = mask ^ (1 << target)
                        rates[next_mask] = rates.get(next_mask, Q(0)) + (
                            parent_fitness / denominator
                        )
        else:
            raise ValueError(rule)

        exit_rate = sum(rates.values(), Q(0))
        assert exit_rate > 0
        matrix[row, row] = exit_rate
        for target, rate in rates.items():
            if target == full:
                rhs[row, 0] += rate
            elif target:
                matrix[row, index[target]] -= rate

    solution = matrix.solve(rhs)
    assert matrix * solution == rhs
    return [solution[index[1 << vertex], 0] for vertex in range(n)]


@dataclass(frozen=True)
class TangentData:
    order: int
    graph6: str
    edges: int
    z_bd_slope: float
    z_db_numerator: float
    singleton_bd_over_p: float
    singleton_db_over_p: float

    def corrections(self, scale: float) -> tuple[float, float]:
        z_bd = self.z_bd_slope * scale
        z_db = self.z_db_numerator / scale
        bd = self.order * (
            self.singleton_bd_over_p * z_bd / (1.0 + z_bd) - 1.0
        )
        db = self.order * (
            self.singleton_db_over_p * z_db / (1.0 + z_db) - 1.0
        )
        return bd, db

    def balanced(self, scale: float) -> tuple[float, float, float, float]:
        bd, db = self.corrections(scale)
        r_minus_one = 0.5
        leaf_ratio = max(0.0, r_minus_one / 1.5 * (db - bd))
        score = min(bd + leaf_ratio / r_minus_one, db - leaf_ratio)
        separator = db + r_minus_one * bd
        return score, leaf_ratio, separator, min(bd, db)


def tangent_data(graph: nx.Graph) -> TangentData:
    graph = nx.convert_node_labels_to_integers(graph, ordering="sorted")
    n = graph.number_of_nodes()
    degrees = [graph.degree(vertex) for vertex in range(n)]
    bd_plus = fixation_vector(graph, R, "Bd")
    bd_minus = fixation_vector(graph, 1 / R, "Bd")
    db_plus = fixation_vector(graph, R, "dB")
    db_minus = fixation_vector(graph, 1 / R, "dB")
    p = (R - 1) / R

    reciprocal_degrees = sum((Q(1, degree) for degree in degrees), Q(0))
    bd_reverse_sum = sum(bd_minus, Q(0))
    db_reverse_weighted = sum(
        (value / degree for value, degree in zip(db_minus, degrees)), Q(0)
    )
    z_bd_slope = (R - 1) * reciprocal_degrees / bd_reverse_sum
    z_db_numerator = R * (R - 1) * n / db_reverse_weighted
    mean_bd = sum(bd_plus, Q(0)) / n
    mean_db = sum(db_plus, Q(0)) / n
    return TangentData(
        order=n,
        graph6=nx.to_graph6_bytes(graph, header=False).decode().strip(),
        edges=graph.number_of_edges(),
        z_bd_slope=float(z_bd_slope),
        z_db_numerator=float(z_db_numerator),
        singleton_bd_over_p=float(mean_bd / p),
        singleton_db_over_p=float(mean_db / p),
    )


def optimize(data: TangentData) -> dict[str, float | int | str]:
    def objective(log_scale: float) -> float:
        scale = math.exp(log_scale)
        return -data.balanced(scale)[0]

    result = minimize_scalar(
        objective, bounds=(-24.0, 24.0), method="bounded", options={"xatol": 1e-13}
    )
    scale = math.exp(float(result.x))
    score, leaf_ratio, separator, raw_min = data.balanced(scale)
    bd, db = data.corrections(scale)
    return {
        "n": data.order,
        "m": data.edges,
        "graph6": data.graph6,
        "scale": scale,
        "Bd": bd,
        "dB": db,
        "lambda": leaf_ratio,
        "score": score,
        "separator": separator,
        "raw_min": raw_min,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=6)
    parser.add_argument("--top", type=int, default=15)
    args = parser.parse_args()
    if not 2 <= args.max_order <= 7:
        raise ValueError("graph atlas supports this audit only through order 7")

    graphs = [
        graph
        for graph in nx.graph_atlas_g()
        if 2 <= graph.number_of_nodes() <= args.max_order and nx.is_connected(graph)
    ]
    rows = [optimize(tangent_data(graph)) for graph in graphs]
    rows.sort(key=lambda row: float(row["score"]), reverse=True)
    print(f"connected unweighted gadgets checked exactly: {len(rows)}")
    print("n m graph6 scale Bd dB lambda balanced separator")
    for row in rows[: args.top]:
        print(
            f"{row['n']} {row['m']} {row['graph6']} "
            f"{row['scale']:.12g} {row['Bd']:.12g} {row['dB']:.12g} "
            f"{row['lambda']:.12g} {row['score']:.12g} "
            f"{row['separator']:.12g}"
        )
    positive = [row for row in rows if float(row["score"]) > 1e-10]
    print(f"positive balanced tangent gadgets: {len(positive)}")


if __name__ == "__main__":
    main()

