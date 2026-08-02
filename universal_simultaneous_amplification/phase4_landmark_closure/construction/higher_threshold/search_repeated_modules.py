#!/usr/bin/env python3
"""Search a complete weak coupling of many identical finite modules.

In the successive rare-edge limit, one internally fixed mutant module behaves
as one macro individual.  The effective Bd and dB fitnesses are computed from
the exact forward and reverse singleton vectors.  The reported large-module-
count fixation limits are numerical reconnaissance.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import differential_evolution

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scan_satellite_module import module_data  # noqa: E402


def decode(size: int, vector: np.ndarray):
    edge_count = size * (size - 1) // 2
    logs = vector[:edge_count] - np.max(vector[:edge_count])
    weights = np.zeros((size, size))
    cursor = 0
    for i in range(size):
        for j in range(i + 1, size):
            weights[i, j] = weights[j, i] = math.exp(float(logs[cursor]))
            cursor += 1
    attach_logs = vector[edge_count:] - np.max(vector[edge_count:])
    return weights, np.exp(attach_logs)


def evaluate(size: int, fitness: float, vector: np.ndarray):
    weights, attachment = decode(size, vector)
    degree = weights.sum(axis=1)
    data = module_data(weights, fitness)
    f_bd, b_bd = data["Bd"]
    f_db, b_db = data["dB"]
    alpha_bd = float(f_bd.mean())
    alpha_db = float(f_db.mean())
    q_bd = fitness * float(attachment @ f_bd) / float(attachment @ b_bd)
    inverse = attachment / degree
    q_db = fitness * fitness * float(inverse @ f_db) / float(inverse @ b_db)
    rho_bd = alpha_bd * max(0.0, 1.0 - 1.0 / q_bd)
    rho_db = alpha_db * max(0.0, 1.0 - 1.0 / q_db)
    baseline = 1.0 - 1.0 / fitness
    return min(rho_bd - baseline, rho_db - baseline), rho_bd, rho_db, q_bd, q_db, weights, attachment


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=3)
    parser.add_argument("--fitness", type=float, default=1.55)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=220)
    parser.add_argument("--popsize", type=int, default=12)
    args = parser.parse_args()
    dimension = args.size * (args.size - 1) // 2 + args.size

    def objective(vector):
        try:
            return -evaluate(args.size, args.fitness, vector)[0]
        except (np.linalg.LinAlgError, FloatingPointError, ValueError):
            return 100.0

    result = differential_evolution(
        objective,
        [(-18.0, 0.0)] * dimension,
        seed=args.seed,
        maxiter=args.iterations,
        popsize=args.popsize,
        polish=True,
        tol=1e-10,
        updating="immediate",
        workers=1,
        disp=True,
    )
    score, rho_bd, rho_db, q_bd, q_db, weights, attachment = evaluate(
        args.size, args.fitness, result.x
    )
    print(f"RESULT n={args.size} r={args.fitness} score={score:+.12g}")
    print(f"rho=({rho_bd:.12g},{rho_db:.12g}) baseline={1-1/args.fitness:.12g}")
    print(f"q=({q_bd:.12g},{q_db:.12g})")
    print("attachment", " ".join(f"{x:.12g}" for x in attachment))
    for row in weights:
        print(" ".join(f"{x:.12g}" for x in row))


if __name__ == "__main__":
    main()
