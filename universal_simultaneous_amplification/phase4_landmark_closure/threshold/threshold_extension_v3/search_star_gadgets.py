#!/usr/bin/env python3
"""Lumped search for arbitrarily large star satellite gadgets."""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

from search_invariant_gadgets import max_separator


def star_singletons(leaves: int, fitness: float, rule: str) -> tuple[float, float]:
    empty = (0, 0)
    full = (1, leaves)
    states = [
        (hub, count)
        for hub in (0, 1)
        for count in range(leaves + 1)
        if (hub, count) not in (empty, full)
    ]
    index = {state: row for row, state in enumerate(states)}
    rows: list[int] = []
    columns: list[int] = []
    entries: list[float] = []
    rhs = np.zeros(len(states))
    for state, row in index.items():
        hub, count = state
        moves: list[tuple[tuple[int, int], float]] = []
        if rule == "Bd":
            if hub == 0 and count:
                moves.append(((1, count), fitness * count))
                moves.append(((0, count - 1), count / leaves))
            if hub == 1 and count < leaves:
                moves.append(((1, count + 1), fitness * (leaves - count) / leaves))
                moves.append(((0, count), leaves - count))
        elif rule == "dB":
            if hub == 0 and count:
                moves.append(
                    ((1, count), fitness * count / (fitness * count + leaves - count))
                )
                moves.append(((0, count - 1), count))
            if hub == 1 and count < leaves:
                moves.append(
                    ((0, count), (leaves - count) / (fitness * count + leaves - count))
                )
                moves.append(((1, count + 1), leaves - count))
        else:
            raise ValueError(rule)
        total = sum(rate for _, rate in moves)
        rows.append(row)
        columns.append(row)
        entries.append(1.0)
        for target, rate in moves:
            probability = rate / total
            if target == full:
                rhs[row] += probability
            elif target != empty:
                rows.append(row)
                columns.append(index[target])
                entries.append(-probability)
    matrix = coo_matrix((entries, (rows, columns)), shape=(len(states), len(states))).tocsr()
    harmonic = spsolve(matrix, rhs)
    return float(harmonic[index[(1, 0)]]), float(harmonic[index[(0, 1)]])


def score_star(leaves: int, fitness: float) -> dict[str, float]:
    bh, bl = star_singletons(leaves, fitness, "Bd")
    dh, dl = star_singletons(leaves, fitness, "dB")
    bmh, bml = star_singletons(leaves, 1.0 / fitness, "Bd")
    dmh, dml = star_singletons(leaves, 1.0 / fitness, "dB")
    order = leaves + 1
    p = 1.0 - 1.0 / fitness
    a_bd = (bh + leaves * bl) / (order * p)
    a_db = (dh + leaves * dl) / (order * p)

    def product(log_ratio: float) -> float:
        # Total leaf portal load is one; hub load is exp(log_ratio).
        hub = math.exp(log_ratio)
        leaf = 1.0
        return (
            fitness
            * (fitness - 1.0) ** 2
            * (hub / leaves + leaf)
            * (hub + leaf)
            / ((hub * bmh + leaf * bml) * (hub * dmh / leaves + leaf * dml))
        )

    result = minimize_scalar(
        lambda value: -product(value),
        bounds=(-40.0, 40.0),
        method="bounded",
        options={"xatol": 1e-12},
    )
    candidates = [(-40.0, product(-40.0)), (40.0, product(40.0)), (result.x, -result.fun)]
    log_ratio, gate_product = max(candidates, key=lambda item: item[1])
    separator, z_bd = max_separator(a_bd, a_db, gate_product, fitness)
    return {
        "order": order,
        "separator": order * separator,
        "per_vertex": separator,
        "K": gate_product,
        "portal_hub_over_all_leaves": math.exp(log_ratio),
        "A_Bd": a_bd,
        "A_dB": a_db,
        "Z_Bd": z_bd,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=200)
    parser.add_argument("--fitness", type=float, default=1.5028569127905696)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()
    rows = [score_star(order - 1, args.fitness) for order in range(3, args.max_order + 1)]
    rows.sort(key=lambda row: float(row["per_vertex"]), reverse=True)
    for row in rows[: args.top]:
        print(row)


if __name__ == "__main__":
    main()
