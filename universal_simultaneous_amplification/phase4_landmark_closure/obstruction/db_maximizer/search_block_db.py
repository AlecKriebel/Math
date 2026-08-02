#!/usr/bin/env python3
"""dB search on undirected weighted equitable block graphs.

Class a has ``sizes[a]`` exchangeable vertices.  Every edge between classes
a,b has one weight ``W[a,b]=W[b,a]``; ``W[a,a]`` is the common within-class
edge weight.  The exact state is the vector of mutant counts by class.

All search output is numerical reconnaissance only.
"""

from __future__ import annotations

import argparse
from itertools import product

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.optimize import differential_evolution, minimize

from search_db import baseline


class BlockGraph:
    def __init__(self, sizes: tuple[int, ...]):
        self.sizes = np.asarray(sizes, dtype=int)
        self.classes = len(sizes)
        self.order = int(sum(sizes))
        self.extinction = (0,) * self.classes
        self.fixation_state = tuple(sizes)
        self.states = [
            state
            for state in product(*(range(size + 1) for size in sizes))
            if state not in (self.extinction, self.fixation_state)
        ]
        self.index = {state: row for row, state in enumerate(self.states)}
        self.parameters = [
            (a, b)
            for a in range(self.classes)
            for b in range(a, self.classes)
            if a != b or sizes[a] > 1
        ]

    def matrix_from_logs(self, logs):
        logs = np.asarray(logs) - np.mean(logs)
        matrix = np.zeros((self.classes, self.classes))
        for (a, b), value in zip(self.parameters, np.exp(logs)):
            matrix[a, b] = matrix[b, a] = value
        return matrix

    def fixation(self, weights, fitness):
        rows, columns, entries = [], [], []
        rhs = np.zeros(len(self.states))
        for state, row in self.index.items():
            counts = np.asarray(state)
            changes = []
            for target_class in range(self.classes):
                count = counts[target_class]
                size = self.sizes[target_class]
                if count < size:
                    mutant_counts = counts.copy()
                    resident_counts = self.sizes - counts
                    resident_counts[target_class] -= 1
                    mutant_mass = float(weights[target_class] @ mutant_counts)
                    resident_mass = float(weights[target_class] @ resident_counts)
                    denominator = fitness * mutant_mass + resident_mass
                    rate = (size - count) * fitness * mutant_mass / denominator
                    if rate:
                        target = counts.copy(); target[target_class] += 1
                        changes.append((tuple(target), rate))
                if count > 0:
                    mutant_counts = counts.copy()
                    mutant_counts[target_class] -= 1
                    resident_counts = self.sizes - counts
                    mutant_mass = float(weights[target_class] @ mutant_counts)
                    resident_mass = float(weights[target_class] @ resident_counts)
                    denominator = fitness * mutant_mass + resident_mass
                    rate = count * resident_mass / denominator
                    if rate:
                        target = counts.copy(); target[target_class] -= 1
                        changes.append((tuple(target), rate))
            changing = sum(rate for _, rate in changes)
            if not changing > 0:
                raise ArithmeticError((state, changes))
            rows.append(row); columns.append(row); entries.append(1.0)
            for target, rate in changes:
                probability = rate / changing
                if target == self.fixation_state:
                    rhs[row] += probability
                elif target != self.extinction:
                    rows.append(row); columns.append(self.index[target]); entries.append(-probability)
        matrix = sp.csr_matrix(
            (entries, (rows, columns)), shape=(len(self.states), len(self.states))
        )
        values = spla.spsolve(matrix, rhs)
        residual = float(np.max(np.abs(matrix @ values - rhs)))
        rho = 0.0
        for class_index, size in enumerate(self.sizes):
            singleton = tuple(int(candidate == class_index) for candidate in range(self.classes))
            rho += size * values[self.index[singleton]]
        return float(rho / self.order), residual


def optimize(model, fitness, bound, iterations, seed):
    target = baseline(model.order, fitness)
    dimension = len(model.parameters)

    def objective(logs):
        weights = model.matrix_from_logs(logs)
        try:
            value, residual = model.fixation(weights, fitness)
        except Exception:
            return 1.0
        if residual > 1e-7 or not np.isfinite(value) or not (-1e-8 <= value <= 1 + 1e-8):
            return 1.0
        return target - value

    result = differential_evolution(
        objective, [(-bound, bound)] * dimension,
        maxiter=iterations, popsize=8, polish=False, seed=seed, tol=1e-8,
    )
    candidates = [result]
    for start in (result.x, np.zeros(dimension)):
        candidates.append(
            minimize(
                objective, start, method="L-BFGS-B",
                bounds=[(-bound, bound)] * dimension,
                options={"maxiter": 1000, "ftol": 1e-14},
            )
        )
    best = min(candidates, key=lambda item: item.fun)
    weights = model.matrix_from_logs(best.x)
    value, residual = model.fixation(weights, fitness)
    return dict(excess=value - target, value=value, residual=residual,
                weights=weights, logs=np.asarray(best.x) - np.mean(best.x))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", required=True)
    parser.add_argument("--fitness", type=float, required=True)
    parser.add_argument("--bound", type=float, default=8)
    parser.add_argument("--iterations", type=int, default=250)
    parser.add_argument("--restarts", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260802)
    args = parser.parse_args()
    model = BlockGraph(tuple(map(int, args.sizes.split(","))))
    records = []
    for restart in range(args.restarts):
        answer = optimize(
            model, args.fitness, args.bound, args.iterations,
            args.seed + 1009 * restart,
        )
        records.append(answer)
        print(restart, answer, flush=True)
    print("BEST", max(records, key=lambda item: item["excess"]))


if __name__ == "__main__":
    main()
