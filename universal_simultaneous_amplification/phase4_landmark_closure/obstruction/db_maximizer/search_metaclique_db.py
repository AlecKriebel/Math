#!/usr/bin/env python3
"""Numerical r=2 search in a weak network of clique modules.

There is no distinguished core.  Module i is a clique K_(m_i) with internal
edge weight a_i, and every vertex of modules i,j is joined with weight
epsilon*b_ij.  In the epsilon->0 limit every module is homogeneous between
rare introductions, giving the exact 2^q-state macro chain derived below.

Optimization is floating-point discovery only.  It is not a positivity or
suppression certificate.
"""

from __future__ import annotations

import argparse

import numpy as np
import scipy.linalg
from scipy.optimize import differential_evolution, minimize


def clique_data(size):
    scale = 2 ** (size - 2)
    alpha = (size - 1) * scale / (size * (2 * scale - 1))
    beta = (size - 1) / (size * (2 * scale - 1))
    return alpha, beta


def complete_baseline(order):
    return (order - 1) / (2 * order) / (1 - 2 ** (-(order - 1)))


class MetaCliqueNetwork:
    def __init__(self, sizes, support):
        self.sizes = np.asarray(sizes, dtype=float)
        self.modules = len(sizes)
        self.order = int(sum(sizes))
        if support == "complete":
            self.edges = [
                (left, right)
                for left in range(self.modules)
                for right in range(left + 1, self.modules)
            ]
        elif support == "cycle":
            if self.modules < 3:
                raise ValueError("cycle support needs at least three modules")
            self.edges = [(i, i + 1) for i in range(self.modules - 1)]
            self.edges.append((0, self.modules - 1))
        else:
            raise ValueError(support)
        data = [clique_data(int(size)) for size in self.sizes]
        self.alpha = np.asarray([item[0] for item in data])
        self.beta = np.asarray([item[1] for item in data])

    @property
    def dimension(self):
        return len(self.edges) + self.modules

    def parameters(self, logs):
        logs = np.asarray(logs, dtype=float)
        logs = logs - logs.mean()
        cross = np.zeros((self.modules, self.modules))
        for (left, right), value in zip(
            self.edges, np.exp(logs[: len(self.edges)])
        ):
            cross[left, right] = cross[right, left] = value
        internal = np.exp(logs[len(self.edges) :])
        return cross, internal

    def fixation(self, logs):
        cross, internal = self.parameters(logs)
        # If target module j is resident, a mutant introduction from module i
        # occurs at leading rate 2*m_j*m_i*b_ij/[a_j*(m_j-1)] and fixes in j
        # with probability alpha_j.  Reversing the types replaces 2*alpha_j
        # by beta_j/2.  Thus the directional target odds are 4*alpha_j/beta_j.
        upward = (
            2
            * self.sizes
            * self.alpha
            / (internal * (self.sizes - 1))
        )
        downward = (
            self.sizes
            * self.beta
            / (2 * internal * (self.sizes - 1))
        )
        full = (1 << self.modules) - 1
        states = np.arange(1, full, dtype=np.int64)
        index = {state: row for row, state in enumerate(states)}
        matrix = np.eye(len(states))
        rhs = np.zeros(len(states))
        for state in states:
            row = index[state]
            mutant = np.asarray(
                [(state >> module) & 1 for module in range(self.modules)]
            )
            changes = []
            for target in range(self.modules):
                source_types = mutant if not mutant[target] else 1 - mutant
                source_mass = np.dot(
                    self.sizes * cross[:, target], source_types
                )
                rate = (
                    upward[target] if not mutant[target] else downward[target]
                ) * source_mass
                if not rate:
                    continue
                target_state = (
                    state | (1 << target)
                    if not mutant[target]
                    else state & ~(1 << target)
                )
                changes.append((target_state, rate))
            changing = sum(rate for _, rate in changes)
            if not changing > 0:
                raise ArithmeticError(state)
            for target_state, rate in changes:
                probability = rate / changing
                if target_state == full:
                    rhs[row] += probability
                elif target_state:
                    matrix[row, index[target_state]] -= probability
        fixation = scipy.linalg.solve(matrix, rhs, check_finite=False)
        residual = float(np.max(np.abs(matrix @ fixation - rhs)))
        local_masses = self.sizes * self.alpha
        rho = sum(
            local_masses[module] * fixation[index[1 << module]]
            for module in range(self.modules)
        ) / self.order
        return float(rho), residual, cross, internal


def optimize(model, bound, iterations, seed):
    target = complete_baseline(model.order)

    def objective(logs):
        try:
            rho, residual, _, _ = model.fixation(logs)
        except Exception:
            return 1.0
        if residual > 1e-8 or not np.isfinite(rho):
            return 1.0
        return target - rho

    result = differential_evolution(
        objective,
        [(-bound, bound)] * model.dimension,
        maxiter=iterations,
        popsize=10,
        polish=False,
        seed=seed,
        tol=1e-10,
    )
    polished = minimize(
        objective,
        result.x,
        method="L-BFGS-B",
        bounds=[(-bound, bound)] * model.dimension,
        options={"maxiter": 3000, "ftol": 1e-15},
    )
    logs = polished.x if polished.fun < result.fun else result.x
    rho, residual, cross, internal = model.fixation(logs)
    return {
        "rho": rho,
        "excess": rho - target,
        "residual": residual,
        "cross": cross,
        "internal": internal,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", required=True, help="comma-separated clique sizes")
    parser.add_argument("--support", choices=("complete", "cycle"), default="complete")
    parser.add_argument("--bound", type=float, default=12)
    parser.add_argument("--iterations", type=int, default=300)
    parser.add_argument("--restarts", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260802)
    args = parser.parse_args()
    sizes = tuple(map(int, args.sizes.split(",")))
    if any(size < 2 for size in sizes):
        raise ValueError("all clique sizes must be at least two")
    model = MetaCliqueNetwork(sizes, args.support)
    records = []
    for restart in range(args.restarts):
        answer = optimize(
            model,
            args.bound,
            args.iterations,
            args.seed + 1009 * restart,
        )
        records.append(answer)
        print(restart, answer, flush=True)
    print("BEST", max(records, key=lambda item: item["excess"]))


if __name__ == "__main__":
    main()
