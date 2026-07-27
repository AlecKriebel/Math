#!/usr/bin/env python3
"""Evaluate the exact weighted-shift maximizers in floating-point arithmetic.

The proof is analytic.  This program is a transparent numerical evaluator and
regression aid; it is not used to establish the all-dimensional theorem.
"""
from __future__ import annotations

import argparse
import math

import numpy as np


def shift(d: int) -> np.ndarray:
    """Return X|j> = |j+1 mod d>."""
    X = np.zeros((d, d), dtype=complex)
    for j in range(d):
        X[(j + 1) % d, j] = 1
    return X


def equality_phases(d: int) -> np.ndarray:
    """The d roots z with z^d=(-1)^(d-1), in cyclic order."""
    delta = 0 if d % 2 else 1
    k = np.arange(d)
    return np.exp(1j * np.pi * (2 * k + delta) / d)


def bad_order(d: int) -> list[int]:
    """Swap the final two equality phases; valid for every d>=4."""
    if d < 4:
        raise ValueError("the nonuniform family is asserted only for d>=4")
    return list(range(d - 2)) + [d - 1, d - 2]


def construct(d: int, order: list[int] | None = None):
    """Construct A_0,A_1,B_0,...,B_d and their polar data.

    In the standard basis,

        A_0 = X,
        A_1 = X diag(z_{order[j]}),
        V_y = X diag((1+omega^y z)/|1+omega^y z|),
        B_y = conjugate(V_y),  B_d = X.
    """
    if d < 2:
        raise ValueError("d must be at least 2")
    if order is None:
        order = bad_order(d) if d >= 4 else list(range(d))
    if sorted(order) != list(range(d)):
        raise ValueError("order must be a permutation of 0,...,d-1")

    omega = np.exp(2j * np.pi / d)
    z = equality_phases(d)
    z_ordered = z[np.asarray(order)]
    X = shift(d)
    Z = np.diag(z_ordered)

    A0 = X
    A1 = X @ Z
    V: list[np.ndarray] = []
    H: list[np.ndarray] = []
    for y in range(d):
        values = 1 + omega**y * z_ordered
        lengths = np.abs(values)
        phases = values / lengths
        V.append(X @ np.diag(phases))
        H.append(np.diag(lengths))
    B = [np.conj(Vy) for Vy in V]
    Bd = X
    return omega, z, A0, A1, V, H, B, Bd


def projectors(A: np.ndarray, omega: complex) -> list[np.ndarray]:
    """Spectral projectors for the eigenvalues 1,omega,...,omega^(d-1)."""
    d = A.shape[0]
    powers = [np.linalg.matrix_power(A, r) for r in range(d)]
    return [
        sum(omega ** (-a * r) * powers[r] for r in range(d)) / d
        for a in range(d)
    ]


def target_probabilities(A0: np.ndarray, A1: np.ndarray, omega: complex) -> np.ndarray:
    """p(a,b|x=1,y=d) on |Phi_d>, where B_d=conjugate(A_0)."""
    d = A0.shape[0]
    P0, P1 = projectors(A0, omega), projectors(A1, omega)
    return np.array(
        [
            [
                (np.trace(P1[a] @ P0[(-b) % d]) / d).real
                for b in range(d)
            ]
            for a in range(d)
        ]
    )


def fourier_probabilities(d: int, order: list[int]) -> np.ndarray:
    """Evaluate the closed Fourier formula for the target table."""
    omega = np.exp(2j * np.pi / d)
    z = equality_phases(d)
    q = np.ones(d, dtype=complex)
    for j in range(1, d):
        q[j] = q[j - 1] * z[order[j - 1]]
    qhat = np.array([sum(q[j] * omega ** (m * j) for j in range(d)) for m in range(d)])
    return np.array(
        [[abs(qhat[-(a + b) % d]) ** 2 / d**3 for b in range(d)] for a in range(d)]
    )


def bell_value(A0, A1, B, Bd, omega) -> tuple[float, float]:
    """Return the unaugmented and augmented expectations on |Phi_d>."""
    d = A0.shape[0]
    bell = sum(
        (np.trace((A0 + omega**y * A1) @ B[y].T) / d).real
        for y in range(d)
    )
    added = (np.trace(A0 @ Bd.T) / d).real
    return bell, bell + added


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("d", type=int, nargs="?", default=4)
    parser.add_argument("--canonical", action="store_true")
    args = parser.parse_args()

    d = args.d
    order = list(range(d)) if args.canonical or d < 4 else bad_order(d)
    omega, _, A0, A1, V, H, B, Bd = construct(d, order)
    p = target_probabilities(A0, A1, omega)
    p_fourier = fourier_probabilities(d, order)
    bell, augmented = bell_value(A0, A1, B, Bd, omega)
    target = 2 / math.sin(math.pi / (2 * d))

    assert np.max(np.abs(p - p_fourier)) < 5e-10
    for y in range(d):
        assert np.linalg.norm(V[y] @ H[y] - (A0 + omega**y * A1)) < 5e-10

    print(f"d={d}, phase order={order}")
    print(f"I_d={bell:.12f}, target={target:.12f}")
    print(f"augmented={augmented:.12f}, target={target + 1:.12f}")
    print(f"p_min={p.min():.12f}, p_max={p.max():.12f}, uniform={1 / d**2:.12f}")
    if d <= 6:
        np.set_printoptions(precision=8, suppress=True)
        print(p)


if __name__ == "__main__":
    main()
