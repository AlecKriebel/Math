#!/usr/bin/env python3
"""Dependency-free exact verification of Eliahou's published seed."""

from __future__ import annotations

from collections import Counter

from construction import goethals_seidel, pack_row, packed_dot
from seed import (
    ELIAHOU_Q,
    ELIAHOU_Q_RUNS,
    ELIAHOU_RESIDUALS,
    ELIAHOU_S,
    ELIAHOU_S_RUNS,
    N,
    fixed_q_edges,
    fixed_q_reduced_sums,
    reduced_blocks,
    special_quadruple,
    summed_aperiodic_correlations,
    summed_periodic_correlations,
)


EXPECTED_ROW_DOTS = Counter(
    {
        0: 641,
        -64: 4,
        128: 6,
        -192: 4,
        256: 4,
        -256: 2,
        -320: 2,
        384: 2,
        -512: 2,
    }
)


def verify() -> None:
    assert len(ELIAHOU_Q_RUNS) == 4
    assert sum(ELIAHOU_Q_RUNS) == N
    assert len(ELIAHOU_S_RUNS) == 85
    assert sum(ELIAHOU_S_RUNS) == N
    assert len(ELIAHOU_Q) == len(ELIAHOU_S) == N

    quadruple = special_quadruple(ELIAHOU_S)
    aperiodic = summed_aperiodic_correlations(quadruple)
    actual_residuals = {
        lag: value for lag, value in enumerate(aperiodic) if lag and value
    }
    assert actual_residuals == ELIAHOU_RESIDUALS
    assert all(value % 64 == 0 for value in aperiodic[1:])

    reduced = fixed_q_reduced_sums(ELIAHOU_S)
    assert all(4 * reduced[lag] == aperiodic[lag] for lag in range(N))
    expected_edge_counts = tuple(164 - 2 * lag for lag in range(1, 82))
    assert tuple(len(fixed_q_edges(lag)) for lag in range(1, 82)) == expected_edge_counts
    assert len(fixed_q_edges(82)) == 2
    assert len(fixed_q_edges(83)) == 0
    assert all(not fixed_q_edges(lag) for lag in range(83, N))

    x, y, u, v = reduced_blocks(ELIAHOU_S)
    for lag in range(1, 81):
        x_corr = sum(x[i] * x[i + lag] for i in range(len(x) - lag))
        y_corr = sum(y[i] * y[i + lag] for i in range(len(y) - lag))
        assert 4 * (x_corr + y_corr) == aperiodic[lag]
    assert 4 * (x[0] * x[81] + x[1] * x[82]) == aperiodic[81]
    assert 4 * (x[0] * x[82] + u * v) == aperiodic[82]

    periodic = summed_periodic_correlations(quadruple)
    assert periodic[0] == 4 * N
    assert all(value % 64 == 0 for value in periodic[1:])

    matrix = goethals_seidel(quadruple)
    assert len(matrix) == 4 * N
    assert all(len(row) == 4 * N for row in matrix)
    packed = tuple(pack_row(row) for row in matrix)
    for row_index, row in enumerate(packed):
        dots = Counter(
            packed_dot(row, other, 4 * N)
            for other_index, other in enumerate(packed)
            if other_index != row_index
        )
        assert dots == EXPECTED_ROW_DOTS


if __name__ == "__main__":
    verify()
    print("PASS: Eliahou's length-167 seed and full 668x668 GS array")
    print("PASS: exactly 13 aperiodic residual lags, all divisible by 64")
    print("PASS: every GS row has 641 exact orthogonal partners and 26 defects")
