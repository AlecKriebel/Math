#!/usr/bin/env python3
"""Compare the reference canonical behavior with the root-ordering family.

This is a floating-point convention check, not part of the analytic proof.
It implements Eqs. (13), (15), and (45) of arXiv:2606.21362v3 directly,
then compares their full behavior with the cyclic root ordering and their
Bell-visible first harmonics with the nonuniform root ordering.
"""
from __future__ import annotations

import math

import numpy as np

import cycle_family

TOL = 3e-8


def reference_strategy(d: int):
    """Return the canonical strategy from Eqs. (13), (15), and (45)."""
    omega = np.exp(2j * np.pi / d)
    X = cycle_family.shift(d)
    Z = np.diag(omega ** np.arange(d))
    bob = []
    for y in range(d):
        observable = np.zeros((d, d), dtype=complex)
        for k in range(d):
            coefficient = (
                (-1) ** k
                * omega ** (k * (k + 1) // 2)
                * omega ** (-y * (k + 1))
                / (d * math.sin(math.pi * (k + 0.5) / d))
            )
            observable += (
                coefficient
                * np.linalg.matrix_power(X, k + 1)
                @ np.linalg.matrix_power(Z, k)
            )
        bob.append(observable)
    return omega, [Z, X], bob + [Z.conj().T]


def full_behavior(
    alice: list[np.ndarray], bob: list[np.ndarray], omega: complex
) -> np.ndarray:
    """Return p[x,y,a,b] on the maximally entangled state."""
    d = alice[0].shape[0]
    alice_projectors = [cycle_family.projectors(A, omega) for A in alice]
    bob_projectors = [cycle_family.projectors(B, omega) for B in bob]
    return np.array(
        [
            [
                [
                    [
                        (
                            np.trace(
                                alice_projectors[x][a]
                                @ bob_projectors[y][b].T
                            )
                            / d
                        ).real
                        for b in range(d)
                    ]
                    for a in range(d)
                ]
                for y in range(len(bob))
            ]
            for x in range(len(alice))
        ]
    )


def first_harmonics(
    alice: list[np.ndarray], bob: list[np.ndarray]
) -> np.ndarray:
    """Return the complex correlators <A_x tensor B_y>."""
    d = alice[0].shape[0]
    return np.array(
        [[np.trace(A @ B.T) / d for B in bob] for A in alice]
    )


def ordering_strategy(d: int, order: list[int]):
    omega, _, A0, A1, _, _, bob, Bd = cycle_family.construct(d, order)
    return omega, [A0, A1], bob + [Bd]


def check_dimension(d: int) -> tuple[float, float]:
    omega, alice_reference, bob_reference = reference_strategy(d)
    reference_behavior = full_behavior(alice_reference, bob_reference, omega)
    reference_harmonics = first_harmonics(alice_reference, bob_reference)

    _, alice_cyclic, bob_cyclic = ordering_strategy(d, list(range(d)))
    cyclic_behavior = full_behavior(alice_cyclic, bob_cyclic, omega)
    cyclic_difference = float(np.max(np.abs(reference_behavior - cyclic_behavior)))
    if cyclic_difference > TOL:
        raise AssertionError(
            f"d={d}: cyclic ordering does not reproduce the reference behavior"
        )

    if d < 4:
        return cyclic_difference, 0.0

    _, alice_swapped, bob_swapped = ordering_strategy(
        d, cycle_family.bad_order(d)
    )
    swapped_behavior = full_behavior(alice_swapped, bob_swapped, omega)
    swapped_harmonics = first_harmonics(alice_swapped, bob_swapped)
    harmonic_difference = float(
        np.max(np.abs(reference_harmonics - swapped_harmonics))
    )
    if harmonic_difference > TOL:
        raise AssertionError(
            f"d={d}: Bell-visible first harmonics depend on root ordering"
        )

    full_difference = float(np.max(np.abs(reference_behavior - swapped_behavior)))
    if full_difference <= 1e-10:
        raise AssertionError(f"d={d}: full behaviors unexpectedly coincide")

    target_reference = reference_behavior[1, d]
    target_swapped = swapped_behavior[1, d]
    if np.max(np.abs(target_reference - 1 / d**2)) > TOL:
        raise AssertionError(f"d={d}: reference target table is not uniform")
    if np.max(target_swapped) <= 1 / d**2 + 1e-10:
        raise AssertionError(f"d={d}: swapped target table is not nonuniform")

    print(
        f"PASS reference comparison d={d}: "
        f"first-harmonic diff={harmonic_difference:.2e}, "
        f"full-behavior diff={full_difference:.12f}"
    )
    return cyclic_difference, full_difference


def main() -> None:
    for d in range(2, 13):
        cyclic_difference, full_difference = check_dimension(d)
        if d < 4:
            print(
                f"PASS reference comparison d={d}: "
                f"cyclic full-behavior diff={cyclic_difference:.2e}"
            )


if __name__ == "__main__":
    main()
