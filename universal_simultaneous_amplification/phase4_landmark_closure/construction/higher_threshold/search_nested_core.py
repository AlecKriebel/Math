#!/usr/bin/env python3
"""Search a finite portal feeding a large clique across a rarer scale.

An outer mutant first enters a portal gadget.  If the portal fixes internally,
it competes either to seed a large resident clique or to be erased by it.  The
two successful-clock odds below are derived directly from Bd and dB updating.
The result is the rooted fixation probability of the composite core in the
successive rare-edge limit.  Numerical optimization is reconnaissance only.
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
    edge_logs = vector[:edge_count] - np.max(vector[:edge_count])
    weights = np.zeros((size, size))
    cursor = 0
    for i in range(size):
        for j in range(i + 1, size):
            weights[i, j] = weights[j, i] = math.exp(float(edge_logs[cursor]))
            cursor += 1
    entry_logs = vector[edge_count : edge_count + size]
    handoff_logs = vector[edge_count + size : edge_count + 2 * size]
    entry = np.exp(entry_logs - np.max(entry_logs))
    handoff = np.exp(handoff_logs - np.max(handoff_logs))
    center_degree = math.exp(float(vector[-1]))
    return weights, entry, handoff, center_degree


def evaluate(size: int, fitness: float, vector: np.ndarray):
    weights, entry, handoff, center_degree = decode(size, vector)
    degree = weights.sum(axis=1)
    data = module_data(weights, fitness)
    forward_bd, reverse_bd = data["Bd"]
    forward_db, reverse_db = data["dB"]
    baseline = 1.0 - 1.0 / fitness

    entry_bd = float(entry @ forward_bd / entry.sum())
    inverse_entry = entry / degree
    entry_db = float(inverse_entry @ forward_db / inverse_entry.sum())

    x = float(np.sum(handoff / degree))
    y_bd = float(handoff @ reverse_bd)
    total = float(handoff.sum())
    y_db = float((handoff / degree) @ reverse_db)
    odds_bd = center_degree * fitness * baseline * x / y_bd
    odds_db = fitness * fitness * baseline * total / (center_degree * y_db)
    core_bd = entry_bd * odds_bd / (1.0 + odds_bd)
    core_db = entry_db * odds_db / (1.0 + odds_db)
    score = min(core_bd - baseline, core_db - baseline)
    return (
        score,
        core_bd,
        core_db,
        entry_bd,
        entry_db,
        odds_bd,
        odds_db,
        weights,
        entry,
        handoff,
        center_degree,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=3)
    parser.add_argument("--fitness", type=float, default=1.55)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=240)
    parser.add_argument("--popsize", type=int, default=14)
    args = parser.parse_args()
    dimension = args.size * (args.size - 1) // 2 + 2 * args.size + 1
    bounds = [(-18.0, 0.0)] * (dimension - 1) + [(-12.0, 12.0)]

    def objective(vector):
        try:
            return -evaluate(args.size, args.fitness, vector)[0]
        except (np.linalg.LinAlgError, FloatingPointError, ValueError):
            return 100.0

    result = differential_evolution(
        objective,
        bounds,
        seed=args.seed,
        maxiter=args.iterations,
        popsize=args.popsize,
        polish=True,
        tol=1e-10,
        workers=1,
        updating="immediate",
        disp=True,
    )
    values = evaluate(args.size, args.fitness, result.x)
    score, core_bd, core_db, entry_bd, entry_db, odds_bd, odds_db = values[:7]
    weights, entry, handoff, center_degree = values[7:]
    print(f"RESULT n={args.size} r={args.fitness} score={score:+.12g}")
    print(f"core=({core_bd:.12g},{core_db:.12g}) baseline={1-1/args.fitness:.12g}")
    print(f"entry=({entry_bd:.12g},{entry_db:.12g}) odds=({odds_bd:.12g},{odds_db:.12g})")
    print(f"center_degree={center_degree:.12g}")
    print("entry_weights", " ".join(f"{x:.12g}" for x in entry))
    print("handoff_weights", " ".join(f"{x:.12g}" for x in handoff))
    for row in weights:
        print(" ".join(f"{x:.12g}" for x in row))


if __name__ == "__main__":
    main()
