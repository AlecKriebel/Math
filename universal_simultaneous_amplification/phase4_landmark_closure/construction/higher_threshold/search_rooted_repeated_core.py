#!/usr/bin/env python3
"""Search a large weak clique of finite portal modules from a rooted entry.

An external mutant first enters one finite portal according to ``entry``.  If
that portal fixes, mutant and resident portal modules compete on a complete
weak macrograph.  ``macro`` controls the vertex attachment law between portal
modules.  The large-macrograph survival factor is ``1-1/q_U``.  Output is
numerical reconnaissance.
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
    entry_logs = vector[edge_count : edge_count + size]
    macro_logs = vector[edge_count + size :]
    entry = np.exp(entry_logs - np.max(entry_logs))
    macro = np.exp(macro_logs - np.max(macro_logs))
    return weights, entry, macro


def evaluate(size: int, fitness: float, vector: np.ndarray):
    weights, entry, macro = decode(size, vector)
    degree = weights.sum(axis=1)
    data = module_data(weights, fitness)
    f_bd, b_bd = data["Bd"]
    f_db, b_db = data["dB"]
    entry_bd = float(entry @ f_bd / entry.sum())
    inverse_entry = entry / degree
    entry_db = float(inverse_entry @ f_db / inverse_entry.sum())
    q_bd = fitness * float(macro @ f_bd) / float(macro @ b_bd)
    inverse_macro = macro / degree
    q_db = fitness * fitness * float(inverse_macro @ f_db) / float(inverse_macro @ b_db)
    core_bd = entry_bd * max(0.0, 1.0 - 1.0 / q_bd)
    core_db = entry_db * max(0.0, 1.0 - 1.0 / q_db)
    baseline = 1.0 - 1.0 / fitness
    return (
        min(core_bd - baseline, core_db - baseline),
        core_bd,
        core_db,
        entry_bd,
        entry_db,
        q_bd,
        q_db,
        weights,
        entry,
        macro,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=3)
    parser.add_argument("--fitness", type=float, default=1.55)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=260)
    parser.add_argument("--popsize", type=int, default=16)
    args = parser.parse_args()
    dimension = args.size * (args.size - 1) // 2 + 2 * args.size

    def objective(vector):
        try:
            return -evaluate(args.size, args.fitness, vector)[0]
        except (np.linalg.LinAlgError, FloatingPointError, ValueError):
            return 100.0

    result = differential_evolution(
        objective,
        [(-20.0, 0.0)] * dimension,
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
    score, core_bd, core_db, entry_bd, entry_db, q_bd, q_db = values[:7]
    weights, entry, macro = values[7:]
    print(f"RESULT n={args.size} r={args.fitness} score={score:+.12g}")
    print(f"core=({core_bd:.12g},{core_db:.12g}) baseline={1-1/args.fitness:.12g}")
    print(f"entry=({entry_bd:.12g},{entry_db:.12g}) q=({q_bd:.12g},{q_db:.12g})")
    print("entry_weights", " ".join(f"{x:.12g}" for x in entry))
    print("macro_weights", " ".join(f"{x:.12g}" for x in macro))
    for row in weights:
        print(" ".join(f"{x:.12g}" for x in row))


if __name__ == "__main__":
    main()
