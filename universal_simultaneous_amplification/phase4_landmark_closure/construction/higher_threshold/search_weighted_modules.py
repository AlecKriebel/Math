#!/usr/bin/env python3
"""Reconnaissance for separated weighted satellite modules.

The internal subset chains are built directly from Bd and dB updating.  A
candidate is scored by its two uniform singleton fixation gaps and by the
exact leading center-degree-window ratio, optimized jointly over positive
attachment weights.  Floating-point output is discovery evidence only.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import differential_evolution

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scan_satellite_module import module_data, z_interval  # noqa: E402


def unpack_graph(size: int, edge_logs: np.ndarray) -> np.ndarray:
    """Return a complete weighted graph, normalized by its largest edge."""
    edge_logs = np.asarray(edge_logs, dtype=float)
    edge_logs = edge_logs - np.max(edge_logs)
    weights = np.zeros((size, size), dtype=float)
    cursor = 0
    for i in range(size):
        for j in range(i + 1, size):
            value = math.exp(float(edge_logs[cursor]))
            weights[i, j] = weights[j, i] = value
            cursor += 1
    return weights


def evaluate(size: int, fitness: float, vector: np.ndarray):
    edge_count = size * (size - 1) // 2
    weights = unpack_graph(size, vector[:edge_count])
    attachment_logs = vector[edge_count:]
    attachment = np.exp(attachment_logs - np.max(attachment_logs))
    data = module_data(weights, fitness)
    baseline = 1.0 - 1.0 / fitness
    alpha_bd = float(data["Bd"][0].mean())
    alpha_db = float(data["dB"][0].mean())
    relative_bd = (alpha_bd - baseline) / baseline
    relative_db = (alpha_db - baseline) / baseline
    interval, _, _ = z_interval(weights, fitness, attachment)
    if interval is None:
        # Preserve a useful gradient while one isolated-establishment
        # condition still fails.  The window ratio only becomes meaningful
        # after both gaps are positive.
        log_ratio = min(relative_bd, relative_db)
    else:
        lower, upper = interval
        log_ratio = math.log(upper / lower)
    # A positive score is exactly the three strict feasibility conditions.
    score = min(relative_bd, relative_db, log_ratio)
    return score, (alpha_bd, alpha_db), interval, weights, attachment


def optimize(
    size: int,
    fitness: float,
    seed: int,
    iterations: int,
    popsize: int,
    mode: str,
):
    dimension = size * (size - 1) // 2 + size
    bounds = [(-16.0, 0.0)] * dimension

    def objective(vector):
        try:
            evaluation = evaluate(size, fitness, vector)
            if mode == "feasible":
                target = evaluation[0]
            elif mode == "alpha":
                baseline = 1.0 - 1.0 / fitness
                target = min(evaluation[1][0] - baseline, evaluation[1][1] - baseline)
            elif mode == "db":
                target = evaluation[1][1]
            else:
                raise ValueError(mode)
            return -target
        except (np.linalg.LinAlgError, FloatingPointError, ValueError):
            return 1000.0

    result = differential_evolution(
        objective,
        bounds,
        seed=seed,
        maxiter=iterations,
        popsize=popsize,
        polish=True,
        updating="immediate",
        workers=1,
        tol=1e-9,
        disp=True,
    )
    score, alphas, interval, weights, attachment = evaluate(size, fitness, result.x)
    print(f"RESULT mode={mode} size={size} r={fitness:.12g} score={score:+.12g}")
    print(f"alphas={alphas} baseline={1-1/fitness:.12g} interval={interval}")
    print("attachment", " ".join(f"{x:.12g}" for x in attachment))
    print("weights")
    for row in weights:
        print(" ".join(f"{x:.12g}" for x in row))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=4)
    parser.add_argument("--fitness", type=float, default=1.55)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=120)
    parser.add_argument("--popsize", type=int, default=8)
    parser.add_argument("--mode", choices=("feasible", "alpha", "db"), default="feasible")
    args = parser.parse_args()
    optimize(
        args.size,
        args.fitness,
        args.seed,
        args.iterations,
        args.popsize,
        args.mode,
    )


if __name__ == "__main__":
    main()
