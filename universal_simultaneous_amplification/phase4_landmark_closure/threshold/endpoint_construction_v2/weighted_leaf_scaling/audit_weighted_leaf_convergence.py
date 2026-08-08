#!/usr/bin/env python3
"""Finite orbit-chain convergence audit for one distinct heavy leaf.

Floating solves are a diagnostic only.  The transition rows themselves have
already been checked against labelled exact enumeration.
"""

from __future__ import annotations

import argparse

import numpy as np
from flint import fmpq
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

from verify_weighted_leaf_lumping import quotient_changes


Q = fmpq


def fixation(C: int, tau, r, rule: str) -> tuple[float, tuple[float, float, float]]:
    c = C - 1
    extinction = (0, 0, 0)
    full = (1, c, 1)
    states = [
        (hub, ordinary, leaf)
        for hub in (0, 1)
        for ordinary in range(c + 1)
        for leaf in (0, 1)
        if (hub, ordinary, leaf) not in (extinction, full)
    ]
    index = {state: row for row, state in enumerate(states)}
    rows: list[int] = []
    columns: list[int] = []
    entries: list[float] = []
    rhs = np.zeros(len(states))
    for state, row in index.items():
        changes = quotient_changes(C, tau, r, rule, state)
        exit_probability = sum(changes.values(), Q(0))
        rows.append(row)
        columns.append(row)
        entries.append(float(exit_probability))
        for target, probability in changes.items():
            value = float(probability)
            if target == full:
                rhs[row] += value
            elif target != extinction:
                rows.append(row)
                columns.append(index[target])
                entries.append(-value)
    matrix = coo_matrix(
        (entries, (rows, columns)), shape=(len(states), len(states))
    ).tocsr()
    solution = spsolve(matrix, rhs)
    residual = np.max(np.abs(matrix @ solution - rhs))
    assert residual < 2e-9
    singleton = (
        float(solution[index[(1, 0, 0)]]),
        float(solution[index[(0, 1, 0)]]),
        float(solution[index[(0, 0, 1)]]),
    )
    average = (singleton[0] + c * singleton[1] + singleton[2]) / (C + 1)
    return average, singleton


def complete_baseline(n: int, r: float, rule: str) -> float:
    if rule == "Bd":
        return (1.0 - 1.0 / r) / (1.0 - r ** (-n))
    return (n - 1) * (r - 1) * r ** (n - 2) / (n * (r ** (n - 1) - 1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="100,250,500,1000")
    args = parser.parse_args()
    tau = Q(5, 2)
    r = Q(3, 2)
    expected = {"Bd": -2216 / 3535, "dB": -45 / 98}
    print("rule C C*(ratio-1) error hub ordinary leaf")
    for rule in ("Bd", "dB"):
        for C in (int(item) for item in args.sizes.split(",")):
            average, singleton = fixation(C, tau, r, rule)
            baseline = complete_baseline(C + 1, 1.5, rule)
            scaled = C * (average / baseline - 1.0)
            print(
                rule,
                C,
                f"{scaled:.12g}",
                f"{scaled - expected[rule]:+.3e}",
                *(f"{value:.9g}" for value in singleton),
            )


if __name__ == "__main__":
    main()

