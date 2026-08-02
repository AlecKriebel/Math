#!/usr/bin/env python3
"""Independent checks of the heterogeneous-windmill dB reduction.

The theorem is proved in WINDMILL_SEQUENCE.md.  Finite numerical convergence
checks here are diagnostics; the booster and homogeneous-chain identities are
also checked symbolically.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from search_windmill_macro import population_fixation  # noqa: E402


def full_fixation(weights: np.ndarray, fitness: float, rule: str) -> float:
    """Build the full labelled subset chain directly from the update rule."""

    order = len(weights)
    degrees = weights.sum(axis=1)
    full = (1 << order) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    matrix = np.zeros((len(states), len(states)))
    rhs = np.zeros(len(states))
    for state, row in index.items():
        mutant = np.array([(state >> vertex) & 1 for vertex in range(order)], dtype=float)
        changes: list[tuple[int, float]] = []
        if rule == "Bd":
            total_fitness = order + (fitness - 1.0) * mutant.sum()
            for target in range(order):
                if mutant[target]:
                    rate = float(weights[:, target] @ ((1.0 - mutant) / degrees)) / total_fitness
                    target_state = state & ~(1 << target)
                else:
                    rate = fitness * float(weights[:, target] @ (mutant / degrees)) / total_fitness
                    target_state = state | (1 << target)
                if rate:
                    changes.append((target_state, rate))
        elif rule == "dB":
            for target in range(order):
                mutant_mass = float(weights[:, target] @ mutant)
                resident_mass = float(weights[:, target] @ (1.0 - mutant))
                denominator = fitness * mutant_mass + resident_mass
                if mutant[target]:
                    rate = resident_mass / (order * denominator)
                    target_state = state & ~(1 << target)
                else:
                    rate = fitness * mutant_mass / (order * denominator)
                    target_state = state | (1 << target)
                if rate:
                    changes.append((target_state, rate))
        else:
            raise ValueError(rule)
        total = sum(rate for _, rate in changes)
        matrix[row, row] = total
        for target_state, rate in changes:
            if target_state == full:
                rhs[row] += rate
            elif target_state:
                matrix[row, index[target_state]] -= rate
    values = np.linalg.solve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    assert residual < 2e-10
    return float(sum(values[index[1 << vertex]] for vertex in range(order)) / order)


def windmill(outer_probability: np.ndarray, ell: np.ndarray, eta: float) -> np.ndarray:
    blades = len(outer_probability)
    order = 2 * blades + 1
    weights = np.zeros((order, order))
    for blade in range(blades):
        left, right = 2 * blade + 1, 2 * blade + 2
        outer = float(outer_probability[blade])
        ratio = eta * float(ell[blade])
        inside = outer / ratio
        weights[0, left] = weights[left, 0] = outer
        weights[0, right] = weights[right, 0] = outer
        weights[left, right] = weights[right, left] = inside
    return weights


def check_trace_convergence() -> None:
    fitness = 1.51
    cases = (
        (np.array((1.0, 2.0)), np.array((0.4, 1.0))),
        (np.array((1.0, 3.0, 8.0)), np.array((0.2, 0.5, 1.0))),
    )
    checks = 0
    for outer, ell in cases:
        outer = outer / outer.sum()
        previous = float("inf")
        for eta in (1e-2, 1e-3, 1e-4):
            trace = population_fixation(outer, eta * ell, fitness)
            weights = windmill(outer, ell, eta)
            full = full_fixation(weights, fitness, "dB")
            error = abs(full - trace["dB"][0])
            assert error < previous
            previous = error
            checks += 1
        assert previous < 2e-5
    print(f"PASS: {checks} full-chain/dB-reduction comparisons converge")


def check_symbolic_identities() -> None:
    R, x, y = sp.symbols("R x y", positive=True)
    pi = R * x / (R * x + y)
    effective_odds = sp.factor(R * pi / (1 - pi))
    assert sp.simplify(effective_odds - R**2 * x / y) == 0

    Q = sp.symbols("Q", positive=True)
    m = sp.symbols("m", integer=True, positive=True)
    fixation = (1 - 1 / Q) / (1 - Q ** (-m))
    # The standard biased-count recurrence has increments proportional to
    # Q^{-k}; this checks the normalized closed form at k=1.
    normalization = sum(Q ** (-k) for k in range(4))
    assert sp.simplify(
        fixation.subs(m, 4) - 1 / normalization
    ) == 0

    r = sp.symbols("r", positive=True)
    alpha = (m - 1) / m * (1 - 1 / r) / (1 - r ** (-(m - 1)))
    leading = (1 - 1 / m) * (1 - 1 / r)
    expected_remainder = (
        (m - 1) * (r - 1) / (m * r * (r ** (m - 1) - 1))
    )
    assert sp.simplify(alpha - leading - expected_remainder) == 0
    print("PASS: booster squaring, homogeneous fixation, and clique formulas")


def check_booster_reconnaissance() -> None:
    # A moderate finite hierarchy, not an asymptotic proof.
    blades, boosters, K = 8, 2, 10.0
    ordinary = blades - boosters
    parent = [1.0] * ordinary
    target = [1.0] * ordinary
    parent_total = float(ordinary)
    target_max = 1.0
    for _ in range(boosters):
        new_parent = K * parent_total
        new_target = K * new_parent * target_max
        parent.append(new_parent)
        target.append(new_target)
        parent_total += new_parent
        target_max = new_target
    p = np.asarray(parent) / sum(parent)
    lam = 1e-4 * np.asarray(target) / max(target)
    values = population_fixation(p, lam, 1.5)
    ordinary_mean = float(values["dB"][2][:ordinary].mean())
    assert ordinary_mean > 0.97
    handoff_bound = 2 * 1.5 * (1.5 + 1) * lam[0] / p[0]
    assert handoff_bound < 1e-5
    print(
        "PASS: finite booster diagnostic "
        f"ordinary_dB={ordinary_mean:.12g}, Bd_handoff_bound={handoff_bound:.12g}"
    )


def main() -> None:
    check_trace_convergence()
    check_symbolic_identities()
    check_booster_reconnaissance()


if __name__ == "__main__":
    main()
