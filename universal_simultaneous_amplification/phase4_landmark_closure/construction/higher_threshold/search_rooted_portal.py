#!/usr/bin/env python3
"""Search a finite portal with favorable Bd- and dB-specific entry laws.

If weak outer edges have column sums ``h_v``, then Bd introductions target
``v`` with weight ``h_v`` (for equal-degree sources), while dB introductions
target it to first order with weight ``h_v/d_v``.  This script searches for a
weighted gadget whose fixation probabilities under both induced entry laws
exceed the infinite-complete baseline.  Output is numerical reconnaissance.
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
    hlogs = vector[edge_count:] - np.max(vector[edge_count:])
    return weights, np.exp(hlogs)


def evaluate(size: int, fitness: float, vector: np.ndarray):
    weights, attachment = decode(size, vector)
    degree = weights.sum(axis=1)
    data = module_data(weights, fitness)
    f_bd = data["Bd"][0]
    f_db = data["dB"][0]
    q_bd = float(attachment @ f_bd / attachment.sum())
    inverse = attachment / degree
    q_db = float(inverse @ f_db / inverse.sum())
    baseline = 1.0 - 1.0 / fitness
    return min(q_bd - baseline, q_db - baseline), q_bd, q_db, weights, attachment, f_bd, f_db


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=3)
    parser.add_argument("--fitness", type=float, default=1.55)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=180)
    parser.add_argument("--popsize", type=int, default=12)
    args = parser.parse_args()
    dimension = args.size * (args.size - 1) // 2 + args.size

    def objective(vector):
        try:
            return -evaluate(args.size, args.fitness, vector)[0]
        except (np.linalg.LinAlgError, FloatingPointError):
            return 100.0

    result = differential_evolution(
        objective,
        [(-18.0, 0.0)] * dimension,
        seed=args.seed,
        maxiter=args.iterations,
        popsize=args.popsize,
        polish=True,
        tol=1e-10,
        workers=1,
        updating="immediate",
        disp=True,
    )
    score, q_bd, q_db, weights, attachment, f_bd, f_db = evaluate(
        args.size, args.fitness, result.x
    )
    print(f"RESULT n={args.size} r={args.fitness} score={score:+.12g}")
    print(f"Q_Bd={q_bd:.12g} Q_dB={q_db:.12g} baseline={1-1/args.fitness:.12g}")
    print("attachment", " ".join(f"{x:.12g}" for x in attachment))
    print("f_Bd", " ".join(f"{x:.12g}" for x in f_bd))
    print("f_dB", " ".join(f"{x:.12g}" for x in f_db))
    for row in weights:
        print(" ".join(f"{x:.12g}" for x in row))


if __name__ == "__main__":
    main()
