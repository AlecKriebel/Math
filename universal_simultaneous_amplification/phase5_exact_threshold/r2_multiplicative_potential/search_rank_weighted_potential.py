#!/usr/bin/env python3
"""Hostile LP screen for an exact r=2 multiplicative potential.

For real vertex weights a with sum a=1, test whether

    F_a(S)=2^(-|S|) (1 + sum_{i in S} a_i)

is a dB submartingale at fitness two.  If feasible, optional stopping gives
the exact complete-graph finite baseline after uniform singleton averaging.
This file is discovery code, not a proof.
"""

from __future__ import annotations

import argparse
from itertools import combinations

import numpy as np
from scipy.optimize import linprog


def constraints(weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n = len(weights)
    degree = weights.sum(axis=1)
    P = weights / degree[:, None]
    rows: list[np.ndarray] = []
    constants: list[float] = []
    for mask in range(1, (1 << n) - 1):
        inside = np.array([(mask >> i) & 1 for i in range(n)], dtype=bool)
        x = P[:, inside].sum(axis=1)
        gain = 2.0 * x / (1.0 + x)
        loss = (1.0 - x) / (1.0 + x)
        c0 = -gain[~inside].sum() + 2.0 * loss[inside].sum()
        row = np.empty(n)
        row[~inside] = gain[~inside]
        row[inside] = c0 - 4.0 * loss[inside]
        # Need c0 + row.a >= 0, or -row.a <= c0.
        rows.append(-row)
        constants.append(c0)
    return np.array(rows), np.array(constants)


def solve(weights: np.ndarray, nonnegative: bool = False):
    A, b = constraints(weights)
    n = len(weights)
    bounds = [(0.0, None)] * n if nonnegative else [(None, None)] * n
    result = linprog(
        np.zeros(n), A_ub=A, b_ub=b,
        A_eq=np.ones((1, n)), b_eq=np.ones(1),
        bounds=bounds, method="highs",
    )
    return result


def polynomial_system(weights: np.ndarray, degree: int):
    """Return the linear drift system for the degree-bounded potential."""
    n = len(weights)
    vertex_sets = [
        subset
        for order in range(1, degree + 1)
        for subset in combinations(range(n), order)
    ]
    degree_one = [position for position, subset in enumerate(vertex_sets)
                  if len(subset) == 1]
    higher = [position for position, subset in enumerate(vertex_sets)
              if len(subset) >= 2]
    P = weights / weights.sum(axis=1)[:, None]
    rows = []
    bounds = []
    for mask in range(1, (1 << n) - 1):
        inside = np.array([(mask >> i) & 1 for i in range(n)], dtype=bool)
        x = P[:, inside].sum(axis=1)
        gain = 2.0 * x / (1.0 + x)
        loss = (1.0 - x) / (1.0 + x)
        # Constant G=1 contribution.
        constant = -gain[~inside].sum() + 2.0 * loss[inside].sum()
        row = np.zeros(len(vertex_sets))
        for column, subset in enumerate(vertex_sets):
            present = all(inside[i] for i in subset)
            value = float(present)
            contribution = 0.0
            for v in range(n):
                if inside[v]:
                    derivative = float(v in subset and all(
                        inside[i] for i in subset if i != v
                    ))
                    contribution += 2.0 * loss[v] * (value - 2.0 * derivative)
                else:
                    derivative = float(v in subset and all(
                        inside[i] for i in subset if i != v
                    ))
                    contribution += gain[v] * (derivative - value)
            row[column] = contribution
        rows.append(-row)
        bounds.append(constant)

    # Exact baseline boundary conditions: sum singleton coefficients=1,
    # and every higher-degree coefficient sums to zero separately in total.
    equalities = []
    targets = []
    row = np.zeros(len(vertex_sets)); row[degree_one] = 1.0
    equalities.append(row); targets.append(1.0)
    if higher:
        row = np.zeros(len(vertex_sets)); row[higher] = 1.0
        equalities.append(row); targets.append(0.0)
    return (
        vertex_sets, np.array(rows), np.array(bounds),
        np.array(equalities), np.array(targets),
    )


def solve_polynomial(weights: np.ndarray, degree: int):
    """LP for G(S)=1+sum_{1<=|I|<=degree} c_I 1_{I subset S}."""
    vertex_sets, rows, bounds, equalities, targets = polynomial_system(weights, degree)
    return linprog(
        np.zeros(len(vertex_sets)), A_ub=rows, b_ub=bounds,
        A_eq=equalities, b_eq=targets,
        bounds=[(None, None)] * len(vertex_sets), method="highs",
    )


def random_graph(n: int, rng: np.random.Generator, span: float) -> np.ndarray:
    weights = np.zeros((n, n))
    for i, j in combinations(range(n), 2):
        value = np.exp(rng.uniform(-span, span))
        weights[i, j] = weights[j, i] = value
    return weights


def candidate_slack(weights: np.ndarray, a: np.ndarray) -> float:
    A, b = constraints(weights)
    return float(np.min(b - A @ a))


def scalar_internal_variance_interval(weights: np.ndarray):
    """Feasible beta for G=1+k/n+beta*sum_{v in S}x_v(1-x_v)."""
    n = len(weights)
    P = weights / weights.sum(axis=1)[:, None]

    def correction(mask: int) -> float:
        inside = np.array([(mask >> i) & 1 for i in range(n)], dtype=bool)
        x = P[:, inside].sum(axis=1)
        return float(np.sum(x[inside] * (1.0 - x[inside])))

    low, high = -np.inf, np.inf
    witness = None
    for mask in range(1, (1 << n) - 1):
        inside = np.array([(mask >> i) & 1 for i in range(n)], dtype=bool)
        x = P[:, inside].sum(axis=1)
        gain = 2.0 * x / (1.0 + x)
        loss = (1.0 - x) / (1.0 + x)
        k = int(inside.sum())
        base_g = 1.0 + k / n
        corr_g = correction(mask)
        base_drift = 0.0
        corr_drift = 0.0
        for v in range(n):
            if inside[v]:
                next_mask = mask & ~(1 << v)
                base_delta = 2.0 * (1.0 + (k - 1) / n) - base_g
                corr_delta = 2.0 * correction(next_mask) - corr_g
                base_drift += 2.0 * loss[v] * base_delta
                corr_drift += 2.0 * loss[v] * corr_delta
            else:
                next_mask = mask | (1 << v)
                base_delta = (1.0 + (k + 1) / n) - 2.0 * base_g
                corr_delta = correction(next_mask) - 2.0 * corr_g
                base_drift += gain[v] * base_delta
                corr_drift += gain[v] * corr_delta
        # Common positive 2^{-k}/n factors are omitted.
        if abs(corr_drift) < 1e-13:
            if base_drift < -1e-10:
                return None, (mask, base_drift, corr_drift)
        elif corr_drift > 0:
            low = max(low, -base_drift / corr_drift)
        else:
            high = min(high, -base_drift / corr_drift)
        if low > high + 1e-10:
            witness = (mask, base_drift, corr_drift)
            return None, witness
    return (low, high), witness


def solve_vertex_internal_variance(weights: np.ndarray):
    """Restricted cubic LP with singleton a_i and c_v x_v(1-x_v) terms."""
    n = len(weights)
    P = weights / weights.sum(axis=1)[:, None]

    def basis(mask: int) -> np.ndarray:
        inside = np.array([(mask >> i) & 1 for i in range(n)], dtype=bool)
        x = P[:, inside].sum(axis=1)
        return np.concatenate((inside.astype(float), inside * x * (1.0 - x)))

    rows, bounds = [], []
    for mask in range(1, (1 << n) - 1):
        inside = np.array([(mask >> i) & 1 for i in range(n)], dtype=bool)
        x = P[:, inside].sum(axis=1)
        gain = 2.0 * x / (1.0 + x)
        loss = (1.0 - x) / (1.0 + x)
        value = basis(mask)
        constant = -gain[~inside].sum() + 2.0 * loss[inside].sum()
        row = np.zeros(2 * n)
        for v in range(n):
            if inside[v]:
                row += 2.0 * loss[v] * (2.0 * basis(mask & ~(1 << v)) - value)
            else:
                row += gain[v] * (basis(mask | (1 << v)) - 2.0 * value)
        rows.append(-row); bounds.append(constant)
    equality = np.zeros((1, 2 * n)); equality[0, :n] = 1.0
    return linprog(
        np.zeros(2 * n), A_ub=np.array(rows), b_ub=np.array(bounds),
        A_eq=equality, b_eq=np.ones(1), bounds=[(None, None)] * (2 * n),
        method="highs",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--trials", type=int, default=500)
    parser.add_argument("--span", type=float, default=8.0)
    parser.add_argument("--seed", type=int, default=20260808)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    worst = 1.0
    for trial in range(args.trials):
        weights = random_graph(args.n, rng, args.span)
        result = solve(weights)
        if not result.success:
            print("INFEASIBLE", trial)
            print(weights)
            return
        slack = candidate_slack(weights, result.x)
        worst = min(worst, slack)
        if trial < 3:
            degree = weights.sum(axis=1)
            candidates = {
                "uniform": np.ones(args.n) / args.n,
                "degree": degree / degree.sum(),
                "inverse_degree": (1.0 / degree) / (1.0 / degree).sum(),
            }
            print("trial", trial, "LP", result.x, "slack", slack)
            print({name: candidate_slack(weights, value)
                   for name, value in candidates.items()})
    print("PASS numerical feasibility", args.trials, "worst slack", worst)


if __name__ == "__main__":
    main()
