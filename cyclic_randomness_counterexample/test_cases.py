#!/usr/bin/env python3
"""Independent floating-point regressions for the weighted-shift family.

These tests exercise the formulas for d=2,...,12.  They support the analytic
proof but do not replace its all-dimensional argument.  The exact d=4
certificate is checked separately by verify_exact.py.
"""
from __future__ import annotations

import itertools
import math

import numpy as np

import cycle_family

TOL = 2e-8


def assert_close(value: float, target: float, label: str, tolerance: float = TOL) -> None:
    if abs(value - target) > tolerance:
        raise AssertionError(f"{label}: {value} != {target}")


def check_strategy(d: int, order: list[int], expect_uniform: bool) -> np.ndarray:
    omega, z, A0, A1, V, H, B, Bd = cycle_family.construct(d, order)
    identity = np.eye(d)
    for label, observable in [
        ("A0", A0),
        ("A1", A1),
        *[(f"V{y}", V[y]) for y in range(d)],
        *[(f"B{y}", B[y]) for y in range(d)],
        ("Bd", Bd),
    ]:
        assert np.linalg.norm(observable.conj().T @ observable - identity) < TOL, (
            d,
            label,
            "unitarity",
        )
        assert np.linalg.norm(np.linalg.matrix_power(observable, d) - identity) < TOL, (
            d,
            label,
            "order",
        )

    for y in range(d):
        C = A0 + omega**y * A1
        assert np.linalg.norm(V[y] @ H[y] - C) < TOL
        assert np.min(np.diag(H[y]).real) > 0

    bell, augmented = cycle_family.bell_value(A0, A1, B, Bd, omega)
    target = 2 / math.sin(math.pi / (2 * d))
    assert_close(bell, target, f"d={d} Bell value")
    assert_close(augmented, target + 1, f"d={d} augmented value")

    probabilities = cycle_family.target_probabilities(A0, A1, omega)
    fourier_probabilities = cycle_family.fourier_probabilities(d, order)
    assert np.max(np.abs(probabilities - fourier_probabilities)) < TOL
    assert_close(float(probabilities.sum()), 1.0, f"d={d} probability normalization")
    assert np.max(np.abs(probabilities.sum(axis=0) - 1 / d)) < TOL
    assert np.max(np.abs(probabilities.sum(axis=1) - 1 / d)) < TOL

    if expect_uniform:
        assert np.max(np.abs(probabilities - 1 / d**2)) < TOL
    return probabilities


def canonical_test(d: int) -> None:
    probabilities = check_strategy(d, list(range(d)), expect_uniform=True)
    print(
        f"PASS canonical d={d}: "
        f"p_min={probabilities.min():.12f}, p_max={probabilities.max():.12f}"
    )


def counterexample_test(d: int) -> None:
    order = cycle_family.bad_order(d)
    probabilities = check_strategy(d, order, expect_uniform=False)
    uniform = 1 / d**2
    explicit_bound = uniform + (
        2
        * math.sin(math.pi / d)
        * math.sin(3 * math.pi / d)
        / (d**2 * (d - 1))
    )
    if probabilities.max() <= uniform + 1e-10:
        raise AssertionError(f"d={d}: target table unexpectedly uniform")
    if probabilities.max() + TOL < explicit_bound:
        raise AssertionError(f"d={d}: explicit guessing lower bound failed")

    # Check the closed second-autocorrelation formula directly.
    z = cycle_family.equality_phases(d)
    q = np.ones(d, dtype=complex)
    for j in range(1, d):
        q[j] = q[j - 1] * z[order[j - 1]]
    C2 = sum(q[(j + 2) % d] * np.conj(q[j]) for j in range(d))
    formula = (z[d - 1] - z[d - 2]) * (z[d - 3] - z[0])
    assert abs(C2 - formula) < TOL
    assert_close(
        abs(C2),
        4 * math.sin(math.pi / d) * math.sin(3 * math.pi / d),
        f"d={d} autocorrelation magnitude",
    )
    print(
        f"PASS nonuniform d={d}: "
        f"G={probabilities.max():.12f} >= {explicit_bound:.12f} > {uniform:.12f}"
    )


def d4_table_test() -> None:
    probabilities = check_strategy(4, [0, 1, 3, 2], expect_uniform=False)
    expected = np.array(
        [[1 / 32 if (a + b) % 2 == 0 else 3 / 32 for b in range(4)] for a in range(4)]
    )
    assert np.max(np.abs(probabilities - expected)) < TOL
    print("PASS d=4 sparse witness: alternating table and G=3/32")


def small_dimension_ordering_test() -> None:
    for d in (2, 3):
        for order_tuple in itertools.permutations(range(d)):
            check_strategy(d, list(order_tuple), expect_uniform=True)
        print(f"PASS d={d}: every root ordering has a uniform target table")


def main() -> None:
    for d in range(2, 13):
        canonical_test(d)
    for d in range(4, 13):
        counterexample_test(d)
    d4_table_test()
    small_dimension_ordering_test()


if __name__ == "__main__":
    main()
