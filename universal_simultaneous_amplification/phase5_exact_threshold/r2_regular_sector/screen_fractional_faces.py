#!/usr/bin/env python3
"""Boundary-face screen for regular transposition orbital symmetrization.

Symmetric stochastic zero-diagonal kernels form the fractional perfect
matching polytope.  This discovery script samples sparse convex combinations
of its characteristic building blocks (unit pairs and half-weight cycles),
including disconnected extreme points and near-boundary mixtures.  It then
tests midpoint symmetrization under sigma=(0 1).

All conclusions are floating-point reconnaissance until exactified.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path
from random import Random
import sys

import numpy as np
from scipy.optimize import minimize


HERE = Path(__file__).resolve()
DB_MAX = HERE.parents[2] / "phase4_landmark_closure" / "obstruction" / "db_maximizer"
sys.path.insert(0, str(DB_MAX))
from search_db import fixation  # noqa: E402


def rho(P: np.ndarray) -> float:
    value, residual, _ = fixation(P, 2.0)
    if residual > 5e-8:
        raise np.linalg.LinAlgError(residual)
    return value


def connected(P: np.ndarray) -> bool:
    seen = {0}
    frontier = [0]
    while frontier:
        u = frontier.pop()
        for v in np.flatnonzero(P[u] > 1e-13):
            if int(v) not in seen:
                seen.add(int(v))
                frontier.append(int(v))
    return len(seen) == len(P)


def conjugate(P: np.ndarray) -> np.ndarray:
    order = np.arange(len(P))
    order[0], order[1] = 1, 0
    return P[np.ix_(order, order)]


def gap(P: np.ndarray) -> float:
    M = (P + conjugate(P)) / 2
    return rho(M) - rho(P)


def cycle_kernel(n: int, cycle: list[int], pairs: list[tuple[int, int]]) -> np.ndarray:
    P = np.zeros((n, n))
    if cycle:
        for index, u in enumerate(cycle):
            v = cycle[(index + 1) % len(cycle)]
            P[u, v] = P[v, u] = 0.5
    for u, v in pairs:
        P[u, v] = P[v, u] = 1.0
    if np.max(np.abs(P.sum(axis=1) - 1)) > 1e-12:
        raise AssertionError(P.sum(axis=1))
    return P


def random_fractional_extreme(n: int, rng: Random) -> np.ndarray:
    vertices = list(range(n))
    rng.shuffle(vertices)
    # Select a partition into unit pairs and odd cycles.  These are precisely
    # the connected components of a fractional-perfect-matching extreme
    # support.
    def block_size_partitions(total: int, minimum: int = 2):
        if total == 0:
            return [()]
        answer = []
        for size in (2, *range(3, total + 1, 2)):
            if size < minimum or size > total:
                continue
            for tail in block_size_partitions(total - size, size):
                answer.append((size,) + tail)
        return answer

    sizes = rng.choice(block_size_partitions(n))
    blocks = []
    offset = 0
    for size in sizes:
        blocks.append(vertices[offset : offset + size])
        offset += size
    odd_blocks = [block for block in blocks if len(block) > 2]
    pairs = [tuple(block) for block in blocks if len(block) == 2]
    P = np.zeros((n, n))
    for block in odd_blocks:
        rng.shuffle(block)
        for index, u in enumerate(block):
            v = block[(index + 1) % len(block)]
            P[u, v] = P[v, u] = 0.5
    for u, v in pairs:
        P[u, v] = P[v, u] = 1.0
    if np.max(np.abs(P.sum(axis=1) - 1)) > 1e-12:
        raise AssertionError((odd_blocks, pairs, P.sum(axis=1)))
    return P


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits)
    weights = np.exp(shifted)
    return weights / weights.sum()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=7)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=26080812)
    args = parser.parse_args()
    rng = Random(args.seed)
    best = None

    for trial in range(args.trials):
        count = rng.choice((2, 2, 3, 3, 4, 5, 6))
        components = [random_fractional_extreme(args.n, rng) for _ in range(count)]
        exponents = np.array([rng.uniform(-10, 2) for _ in range(count)])
        coefficients = softmax(exponents)
        P = sum(c * E for c, E in zip(coefficients, components))
        if not connected(P):
            continue
        try:
            value = gap(P)
        except np.linalg.LinAlgError:
            continue
        record = (value, P, coefficients, components)
        if best is None or value < best[0]:
            best = record

        # Optimize only mixture coefficients on this exact boundary face.
        if trial < 100 or value < 1e-5:
            def objective(logits):
                c = softmax(logits)
                candidate = sum(a * E for a, E in zip(c, components))
                if not connected(candidate):
                    return 1.0
                try:
                    return gap(candidate)
                except np.linalg.LinAlgError:
                    return 1.0

            polished = minimize(
                objective,
                exponents,
                method="Nelder-Mead",
                options={"maxiter": 800, "xatol": 1e-10, "fatol": 1e-13},
            )
            c = softmax(polished.x)
            candidate = sum(a * E for a, E in zip(c, components))
            if connected(candidate):
                try:
                    record = (gap(candidate), candidate, c, components)
                    if best is None or record[0] < best[0]:
                        best = record
                except np.linalg.LinAlgError:
                    pass
        if trial and trial % 100 == 0:
            print(f"trial={trial} best_gap={best[0]:.12g}", flush=True)

    if best is None:
        raise RuntimeError("no connected mixture")
    print("best_gap", best[0])
    print("coefficients", best[2])
    print("P=")
    print(np.array2string(best[1], precision=16, max_line_width=240))
    print("NUMERICAL DISCOVERY ONLY")


if __name__ == "__main__":
    main()
