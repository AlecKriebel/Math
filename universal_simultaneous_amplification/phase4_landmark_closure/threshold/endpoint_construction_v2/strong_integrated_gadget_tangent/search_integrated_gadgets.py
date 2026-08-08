#!/usr/bin/env python3
"""Bounded optimizer for strong integrated gadgets of order 3--7."""

from __future__ import annotations

import argparse
import numpy as np
from scipy.optimize import differential_evolution, minimize

from integrated_gadget import decode_complete, tangent_coefficients


def optimize(order: int, fitness: float, seed: int, bound: float, budget: int):
    dimension = order * (order - 1) // 2 + order
    bounds = [(-bound, bound)] * dimension

    def objective(parameters):
        try:
            internal, portal = decode_complete(order, parameters)
            return -tangent_coefficients(internal, portal, fitness).balanced
        except (np.linalg.LinAlgError, FloatingPointError, ValueError):
            return 1e6

    # A short global phase followed by exact-objective local polishing keeps
    # the order-seven cycle bounded on the shared workstation.
    population = max(4, min(8, budget // max(1, dimension * 20)))
    iterations = max(8, budget // max(1, population * dimension))
    discovery = differential_evolution(
        objective,
        bounds,
        seed=seed,
        popsize=population,
        maxiter=iterations,
        polish=False,
        updating="immediate",
        workers=1,
        tol=1e-8,
    )
    edge_count = order * (order - 1) // 2
    core_clone = np.r_[np.full(edge_count, -bound), np.zeros(order)]
    seeds = [discovery.x, core_clone]
    if order >= 2:
        rare_pair = core_clone.copy()
        # The final complete-support edge joins vertices order-2 and order-1.
        rare_pair[edge_count - 1] = 1.7
        rare_pair[edge_count + order - 2 :] = -bound
        seeds.append(rare_pair)
    candidates = [(objective(seed), seed) for seed in seeds]
    polished = minimize(
        objective,
        discovery.x,
        method="L-BFGS-B",
        bounds=bounds,
        options={"maxiter": 250, "ftol": 1e-14, "gtol": 1e-8},
    )
    candidates.append((polished.fun, polished.x))
    _, parameters = min(candidates, key=lambda item: item[0])
    internal, portal = decode_complete(order, parameters)
    result = tangent_coefficients(internal, portal, fitness)
    return {
        "order": order,
        "fitness": fitness,
        "Bd": result.Bd,
        "dB": result.dB,
        "separator": result.separator,
        "balanced": result.balanced,
        "lambda": result.leaf_ratio,
        "internal": internal.tolist(),
        "portal": portal.tolist(),
        "parameters": parameters.tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orders", default="3,4,5,6,7")
    parser.add_argument("--fitnesses", default="1.51,1.55,2")
    parser.add_argument("--seed", type=int, default=20260808)
    parser.add_argument("--bound", type=float, default=7.0)
    parser.add_argument("--budget", type=int, default=2400)
    args = parser.parse_args()
    rows = []
    count = 0
    for fitness in (float(item) for item in args.fitnesses.split(",")):
        for order in (int(item) for item in args.orders.split(",")):
            row = optimize(order, fitness, args.seed + count, args.bound, args.budget)
            count += 1
            rows.append(row)
            print(
                f"r={fitness:g} s={order} balanced={row['balanced']:.12g} "
                f"separator={row['separator']:.12g} "
                f"Bd={row['Bd']:.12g} dB={row['dB']:.12g}"
            )


if __name__ == "__main__":
    main()
