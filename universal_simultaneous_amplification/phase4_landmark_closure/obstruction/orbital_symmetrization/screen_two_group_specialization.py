#!/usr/bin/env python3
"""Targeted lumped screen for a transposition-specialized regular family.

This is discovery code, not a proof certificate.  There are two distinguished
vertices and two equal outside classes A,B of size m.  The endpoint specializes
the first distinguished vertex toward A and the second toward B; swapping the
two distinguished vertices gives the conjugate endpoint.  Their kernel
midpoint removes the specialization.  The exact orbit state is

    (x_0, x_1, i, j),

where x_0,x_1 are the distinguished mutant indicators and i,j are mutant
counts in A,B.  Transition rates below are derived directly from dB updating
at fitness two.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
import scipy.sparse
import scipy.sparse.linalg


def h(x: float) -> float:
    return 2.0 * x / (1.0 + x)


def fixation(m: int, c: float, gamma: float, specialization: float) -> float:
    """Return the exactly lumped floating-point fixation probability."""
    size = 2 + 2 * m
    s = (1.0 - c) / m
    a = s * (1.0 + specialization) / 2.0
    b = s * (1.0 - specialization) / 2.0
    residual = 1.0 - s
    cross = gamma * residual / m
    internal = (1.0 - gamma) * residual / (m - 1)

    states = [
        state
        for state in itertools.product((0, 1), (0, 1), range(m + 1), range(m + 1))
        if state != (0, 0, 0, 0) and state != (1, 1, m, m)
    ]
    index = {state: row for row, state in enumerate(states)}
    full = (1, 1, m, m)
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    rhs = np.zeros(len(states))

    for row, state in enumerate(states):
        x0, x1, i, j = state
        moves: list[tuple[tuple[int, int, int, int], float]] = []

        mass0 = c * x1 + a * i + b * j
        if x0:
            moves.append(((0, x1, i, j), 1.0 - h(mass0)))
        else:
            moves.append(((1, x1, i, j), h(mass0)))

        mass1 = c * x0 + b * i + a * j
        if x1:
            moves.append(((x0, 0, i, j), 1.0 - h(mass1)))
        else:
            moves.append(((x0, 1, i, j), h(mass1)))

        mass_a_up = a * x0 + b * x1 + internal * i + cross * j
        mass_a_down = a * x0 + b * x1 + internal * (i - 1) + cross * j
        if i < m:
            moves.append(((x0, x1, i + 1, j), (m - i) * h(mass_a_up)))
        if i:
            moves.append(((x0, x1, i - 1, j), i * (1.0 - h(mass_a_down))))

        mass_b_up = b * x0 + a * x1 + cross * i + internal * j
        mass_b_down = b * x0 + a * x1 + cross * i + internal * (j - 1)
        if j < m:
            moves.append(((x0, x1, i, j + 1), (m - j) * h(mass_b_up)))
        if j:
            moves.append(((x0, x1, i, j - 1), j * (1.0 - h(mass_b_down))))

        exit_rate = sum(rate for _, rate in moves)
        rows.append(row)
        cols.append(row)
        data.append(exit_rate)
        for target, rate in moves:
            if not rate:
                continue
            if target == full:
                rhs[row] += rate
            elif target != (0, 0, 0, 0):
                rows.append(row)
                cols.append(index[target])
                data.append(-rate)

    matrix = scipy.sparse.csr_matrix((data, (rows, cols)), shape=(len(states),) * 2)
    values = scipy.sparse.linalg.spsolve(matrix, rhs)
    singleton_sum = values[index[(1, 0, 0, 0)]] + values[index[(0, 1, 0, 0)]]
    singleton_sum += m * values[index[(0, 0, 1, 0)]]
    singleton_sum += m * values[index[(0, 0, 0, 1)]]
    return float(singleton_sum / size)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=80)
    args = parser.parse_args()
    parameters = (
        (0.001, 0.001, 1.0),
        (0.001, 0.5, 1.0),
        (0.001, 0.999, 1.0),
        (0.2, 0.001, 1.0),
        (0.2, 0.8, 1.0),
        (0.7, 0.2, 1.0),
        (0.2, 0.5, 0.5),
    )
    for m in dict.fromkeys((2, 3, 5, 8, 13, 21, 34, 55, args.max_m)):
        if m > args.max_m:
            continue
        minimum = (float("inf"), None)
        for c, gamma, specialization in parameters:
            endpoint = fixation(m, c, gamma, specialization)
            midpoint = fixation(m, c, gamma, 0.0)
            item = (midpoint - endpoint, (c, gamma, specialization, endpoint, midpoint))
            minimum = min(minimum, item)
        print(f"m={m} minimum_slack={minimum[0]:.12g} parameters={minimum[1]}")
    print("NUMERICAL LUMPED SCREEN ONLY")


if __name__ == "__main__":
    main()
