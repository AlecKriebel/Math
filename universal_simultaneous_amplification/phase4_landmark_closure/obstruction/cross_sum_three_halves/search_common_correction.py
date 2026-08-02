#!/usr/bin/env python3
"""Test a common-potential certificate for the cross-sum inequality.

Let phi_B(k), phi_D(k) be the complete-graph fixation harmonics.  A function
h on subsets with h(empty)=h(V)=0 certifies the desired cross-sum if

    L_B (phi_B+h) <= 0,       L_D (phi_D-h) <= 0.

Indeed the h terms cancel pointwise when the two processes start from the
same singleton.  This script tests feasibility of those linear inequalities
on exact finite generators in floating point and inspects candidate h.  It is
discovery code, not a proof.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
from scipy.optimize import linprog


PARENT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PARENT))
from search_random import random_weights  # noqa: E402


R = 1.5
Q = 2 / 3


def harmonics(n):
    bd = np.array([(1 - Q**k) / (1 - Q**n) for k in range(n + 1)])
    db = np.array(
        [
            (n - (n + k / 2) * Q**k) / (n * (1 - Q ** (n - 1)))
            for k in range(n + 1)
        ]
    )
    return bd, db


def generator(weights, rule):
    n = len(weights)
    full = (1 << n) - 1
    transient = list(range(1, full))
    index = {state: row for row, state in enumerate(transient)}
    degree = weights.sum(axis=1)
    matrix = np.zeros((len(transient), len(transient)))
    boundary = np.zeros((len(transient), 2))
    for state in transient:
        row = index[state]
        for target in range(n):
            mutant = bool(state & (1 << target))
            if rule == "Bd":
                mutant_mass = sum(
                    weights[parent, target] / degree[parent]
                    for parent in range(n)
                    if state & (1 << parent)
                )
                resident_mass = sum(
                    weights[parent, target] / degree[parent]
                    for parent in range(n)
                    if not state & (1 << parent)
                )
                rate = resident_mass if mutant else R * mutant_mass
            else:
                mutant_mass = sum(
                    weights[parent, target]
                    for parent in range(n)
                    if state & (1 << parent)
                )
                resident_mass = degree[target] - mutant_mass
                denominator = R * mutant_mass + resident_mass
                rate = (
                    resident_mass / denominator
                    if mutant
                    else R * mutant_mass / denominator
                )
            if rate == 0:
                continue
            target_state = state ^ (1 << target)
            matrix[row, row] -= rate
            if target_state == 0:
                boundary[row, 0] += rate
            elif target_state == full:
                boundary[row, 1] += rate
            else:
                matrix[row, index[target_state]] += rate
    return transient, matrix, boundary


def test(weights, tangent=False):
    n = len(weights)
    states, lb, bb = generator(weights, "Bd")
    _, ld, bdry_d = generator(weights, "dB")
    phi_b, phi_d = harmonics(n)
    vector_b = np.array([phi_b[bin(state).count("1")] for state in states])
    vector_d = np.array([phi_d[bin(state).count("1")] for state in states])
    drift_b = lb @ vector_b + bb[:, 1]
    drift_d = ld @ vector_d + bdry_d[:, 1]
    if tangent:
        base_b = phi_b[1]
        base_d = phi_d[1]
        drift_b = base_d * drift_b
        drift_d = base_b * drift_d
    # L_B h <= -drift_b; -L_D h <= -drift_d.
    a_ub = np.vstack((lb, -ld))
    b_ub = np.concatenate((-drift_b, -drift_d))
    solution = linprog(
        np.zeros(len(states)),
        A_ub=a_ub,
        b_ub=b_ub,
        bounds=[(None, None)] * len(states),
        method="highs",
    )
    if not solution.success:
        return False, solution.message, None
    residual = max(np.max(lb @ solution.x + drift_b), np.max(drift_d - ld @ solution.x))
    return True, residual, solution.x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--tangent", action="store_true")
    args = parser.parse_args()
    np.random.seed(args.seed)
    import random

    random.seed(args.seed)
    for sample in range(args.samples):
        weights = random_weights(args.n, log_span=6, edge_probability=0.7)
        feasible, status, h = test(weights, tangent=args.tangent)
        if not feasible:
            print("INFEASIBLE", sample, status)
            print(repr(weights.tolist()))
            return
        if sample % 10 == 0:
            print("feasible", sample, "residual", status, "h_range", (h.min(), h.max()))
    print("ALL FEASIBLE", args.n, args.samples)


if __name__ == "__main__":
    main()
