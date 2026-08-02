#!/usr/bin/env python3
"""Reconnaissance for exactly lumpable dense two-class families.

This is a discovery tool, not a proof certificate.  It imports the transition
formulas already independently checked against the subset chain in Phase 3,
removes holding probabilities, and solves the sparse Dirichlet system.  Every
reported solution is checked by its infinity-norm residual.
"""

from __future__ import annotations

import argparse
import itertools
import math
import pathlib
import sys

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as spla


PROGRAM = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROGRAM))
from phase3_asymptotic.scan_lumpable import TwoClass, baseline  # noqa: E402


def fixation(graph: TwoClass, fitness: float, rule: str) -> tuple[float, float]:
    a, b = graph.size_a, graph.size_b
    states = [
        (i, j)
        for i in range(a + 1)
        for j in range(b + 1)
        if (i, j) not in ((0, 0), (a, b))
    ]
    index = {state: k for k, state in enumerate(states)}
    rows: list[int] = []
    columns: list[int] = []
    data: list[float] = []
    rhs = np.zeros(len(states))
    full = (a, b)
    for state, source in index.items():
        changes = graph.changing_transitions(state, fitness, rule)
        mass = sum(probability for _, probability in changes)
        if not mass > 0:
            raise AssertionError((state, changes))
        rows.append(source)
        columns.append(source)
        data.append(1.0)
        for target, probability in changes:
            probability /= mass
            if target == full:
                rhs[source] += probability
            elif target != (0, 0):
                rows.append(source)
                columns.append(index[target])
                data.append(-probability)
    matrix = sparse.csr_matrix((data, (rows, columns)), shape=(len(states),) * 2)
    values = spla.spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    average = (a * values[index[(1, 0)]] + b * values[index[(0, 1)]]) / (a + b)
    return float(average), residual


def evaluate(graph: TwoClass, fitnesses: tuple[float, ...]) -> tuple[float, ...]:
    result: list[float] = []
    for fitness in fitnesses:
        for rule in ("Bd", "dB"):
            value, residual = fixation(graph, fitness, rule)
            if residual > 2.0e-9:
                raise AssertionError((graph, fitness, rule, residual))
            result.append(value - baseline(graph.n, fitness, rule))
    return tuple(result)


def power_grid(n: int) -> None:
    fitnesses = (1.02, 1.1, 1.2, 1.5, 2.0, 5.0, 10.0)
    sizes = sorted({1, 2, max(1, round(n ** 0.25)), round(n ** 0.5), n // 4, n // 2})
    exponents = (-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0)
    candidates: list[tuple[float, tuple[object, ...], tuple[float, ...]]] = []
    for size_a, pa, pb, pc in itertools.product(sizes, exponents, exponents, exponents):
        if not 0 < size_a < n:
            continue
        # Common rescaling is immaterial.  Normalize the cross weight to one.
        wa = n ** (pa - pc)
        wb = n ** (pb - pc)
        graph = TwoClass(size_a, n - size_a, wa, wb, 1.0)
        values = evaluate(graph, fitnesses)
        score = min(values)
        candidates.append((score, (size_a, pa - pc, pb - pc), values))
    candidates.sort(reverse=True, key=lambda item: item[0])
    for score, parameters, values in candidates[:30]:
        formatted = " ".join(f"{value:+.4e}" for value in values)
        print(f"score={score:+.4e} m,ea,eb={parameters} {formatted}")


def random_grid(n: int, samples: int, seed: int) -> None:
    rng = np.random.default_rng(seed)
    fitnesses = (1.02, 1.1, 1.2, 1.5, 2.0, 5.0, 10.0, 50.0)
    candidates: list[tuple[float, tuple[object, ...], tuple[float, ...]]] = []
    for _ in range(samples):
        size_exponent = rng.uniform(0.0, 1.0)
        size_a = min(n - 1, max(1, round(n**size_exponent)))
        log_wa, log_wb = rng.uniform(-4 * math.log(n), 4 * math.log(n), size=2)
        wa, wb = math.exp(log_wa), math.exp(log_wb)
        graph = TwoClass(size_a, n - size_a, wa, wb, 1.0)
        values = evaluate(graph, fitnesses)
        score = min(values)
        candidates.append((score, (size_a, log_wa / math.log(n), log_wb / math.log(n)), values))
    candidates.sort(reverse=True, key=lambda item: item[0])
    for score, parameters, values in candidates[:40]:
        formatted = " ".join(f"{value:+.4e}" for value in values)
        print(f"score={score:+.4e} m,ea,eb={parameters} {formatted}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=40)
    parser.add_argument("--random", type=int, default=0)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    if args.random:
        random_grid(args.n, args.random, args.seed)
    else:
        power_grid(args.n)


if __name__ == "__main__":
    main()
