#!/usr/bin/env python3
"""Numerical conjecture generator for fixed-fitness Bd/dB tradeoffs.

This file is not a proof component.  It constructs the full subset chain
directly from the update definitions and solves the absorbing equations in
double precision for small graphs.
"""

from __future__ import annotations

import argparse
import math
import random

import numpy as np


def fixation(weights: np.ndarray, fitness: float, rule: str) -> float:
    n = len(weights)
    full = (1 << n) - 1
    transient = list(range(1, full))
    index = {state: pos for pos, state in enumerate(transient)}
    matrix = np.eye(len(transient))
    rhs = np.zeros(len(transient))
    degrees = weights.sum(axis=1)

    for state in transient:
        row = index[state]
        mutant = np.array([(state >> i) & 1 for i in range(n)], dtype=float)
        transitions: dict[int, float] = {}
        if rule == "Bd":
            fit = 1.0 + (fitness - 1.0) * mutant
            for parent in range(n):
                for target in range(n):
                    if weights[parent, target] == 0:
                        continue
                    probability = (
                        fit[parent]
                        / fit.sum()
                        * weights[parent, target]
                        / degrees[parent]
                    )
                    if mutant[parent]:
                        new_state = state | (1 << target)
                    else:
                        new_state = state & ~(1 << target)
                    transitions[new_state] = transitions.get(new_state, 0.0) + probability
        else:
            for target in range(n):
                mass = weights[:, target] * (1.0 + (fitness - 1.0) * mutant)
                for parent in range(n):
                    if mass[parent] == 0:
                        continue
                    probability = mass[parent] / (n * mass.sum())
                    if mutant[parent]:
                        new_state = state | (1 << target)
                    else:
                        new_state = state & ~(1 << target)
                    transitions[new_state] = transitions.get(new_state, 0.0) + probability
        # Delete the state-dependent self-loop before building the linear
        # system.  This leaves all hitting probabilities unchanged and is
        # essential when edge scales are separated by many orders of
        # magnitude: the unconditioned matrix otherwise loses the rare
        # effective transitions to floating-point cancellation.
        transitions.pop(state, None)
        effective_mass = sum(transitions.values())
        if not effective_mass > 0.0:
            raise FloatingPointError("no resolvable effective transition")
        transitions = {
            new_state: probability / effective_mass
            for new_state, probability in transitions.items()
        }
        for new_state, probability in transitions.items():
            if new_state == full:
                rhs[row] += probability
            elif new_state:
                matrix[row, index[new_state]] -= probability

    values = np.linalg.solve(matrix, rhs)
    return sum(values[index[1 << i]] for i in range(n)) / n


def baseline(n: int, r: float, rule: str) -> float:
    if rule == "Bd":
        return (1.0 - 1.0 / r) / (1.0 - r ** (-n))
    return (n - 1.0) / n * (1.0 - 1.0 / r) / (1.0 - r ** (-(n - 1)))


def random_weights(n: int, log_span: float, edge_probability: float) -> np.ndarray:
    while True:
        weights = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() <= edge_probability:
                    value = math.exp(random.uniform(-log_span, log_span))
                    weights[i, j] = weights[j, i] = value
        # connectivity
        seen = {0}
        boundary = [0]
        while boundary:
            i = boundary.pop()
            for j in np.flatnonzero(weights[i]):
                if int(j) not in seen:
                    seen.add(int(j))
                    boundary.append(int(j))
        if len(seen) == n:
            return weights


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--r", type=float, default=2.0)
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--span", type=float, default=6.0)
    parser.add_argument("--p", type=float, default=1.0)
    args = parser.parse_args()
    random.seed(args.seed)
    best_db = (-math.inf, None, None)
    best_sim = (-math.inf, None, None)
    for sample in range(args.samples):
        weights = random_weights(args.n, args.span, args.p)
        db_delta = fixation(weights, args.r, "dB") - baseline(args.n, args.r, "dB")
        if db_delta > best_db[0]:
            bd_delta = fixation(weights, args.r, "Bd") - baseline(args.n, args.r, "Bd")
            best_db = (db_delta, bd_delta, weights.copy())
            print("best_db", sample, db_delta, bd_delta, weights.tolist(), flush=True)
        if db_delta > 0:
            bd_delta = fixation(weights, args.r, "Bd") - baseline(args.n, args.r, "Bd")
            score = min(db_delta, bd_delta)
            if score > best_sim[0]:
                best_sim = (score, (bd_delta, db_delta), weights.copy())
                print("best_sim", sample, score, bd_delta, db_delta, weights.tolist(), flush=True)


if __name__ == "__main__":
    main()
