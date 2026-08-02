#!/usr/bin/env python3
"""Targeted numerical falsification search for the two adjoint split lemmas.

Numerical output is discovery evidence only.  Any apparent violation must be
converted to rational weights and independently checked exactly.
"""

from __future__ import annotations

import argparse
import itertools
import pathlib
import sys

import numpy as np
from scipy.optimize import differential_evolution


PARENT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PARENT))
from search_random import baseline, fixation  # noqa: E402


R = 1.5


def weights_from_logs(n: int, logs: np.ndarray) -> np.ndarray:
    weights = np.zeros((n, n))
    logs = logs - logs.mean()
    for (i, j), value in zip(itertools.combinations(range(n), 2), np.exp(logs)):
        weights[i, j] = weights[j, i] = value
    return weights


def link_values(q: np.ndarray) -> np.ndarray:
    """Fixation values for biased arrows with base rates q_uv."""
    n = len(q)
    states = list(range(1, (1 << n) - 1))
    index = {state: row for row, state in enumerate(states)}
    matrix = np.zeros((len(states), len(states)))
    rhs = np.zeros(len(states))
    full = (1 << n) - 1
    for state in states:
        row = index[state]
        rates: dict[int, float] = {}
        for target in range(n):
            if (state >> target) & 1:
                rate = sum(
                    q[source, target]
                    for source in range(n)
                    if not ((state >> source) & 1)
                )
                new_state = state & ~(1 << target)
            else:
                rate = R * sum(
                    q[source, target]
                    for source in range(n)
                    if (state >> source) & 1
                )
                new_state = state | (1 << target)
            if rate:
                rates[new_state] = rates.get(new_state, 0.0) + rate
        total = sum(rates.values())
        matrix[row, row] = total
        for new_state, rate in rates.items():
            if new_state == full:
                rhs[row] += rate
            elif new_state:
                matrix[row, index[new_state]] -= rate
    transient_values = np.linalg.solve(matrix, rhs)
    values = np.zeros(1 << n)
    values[full] = 1
    for state, row in index.items():
        values[state] = transient_values[row]
    return values


def link_fixation(q: np.ndarray) -> float:
    values = link_values(q)
    n = len(q)
    return float(sum(values[1 << i] for i in range(n)) / n)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--span", type=float, default=12.0)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    n = args.n
    edge_count = n * (n - 1) // 2
    b_base = baseline(n, R, "Bd")
    d_base = baseline(n, R, "dB")
    best = [[-np.inf, None], [-np.inf, None], [-np.inf, None]]

    def quantities(logs: np.ndarray) -> tuple[float, float, float]:
        weights = weights_from_logs(n, logs)
        p = weights / weights.sum(axis=1)[:, None]
        rho_l = link_fixation(p)
        rho_c = link_fixation(p.T)
        rho_d = fixation(weights, R, "dB")
        return (
            rho_l * rho_c / (b_base * b_base) - 1,
            (rho_d / rho_c) / (d_base / b_base) - 1,
            (rho_l + rho_c) / (2 * b_base) - 1,
        )

    for which in range(3):
        def objective(logs: np.ndarray) -> float:
            try:
                value = quantities(logs)[which]
            except (FloatingPointError, np.linalg.LinAlgError):
                return 1e3
            if value > best[which][0]:
                best[which] = [value, logs.copy()]
            return -value

        differential_evolution(
            objective,
            [(-args.span, args.span)] * edge_count,
            seed=args.seed + which,
            popsize=10,
            maxiter=args.iterations,
            polish=True,
        )
        value, logs = best[which]
        assert logs is not None
        print("split", which + 1, "best relative excess", value)
        print("weights", weights_from_logs(n, logs).tolist())
        print("both quantities", quantities(logs))


if __name__ == "__main__":
    main()
