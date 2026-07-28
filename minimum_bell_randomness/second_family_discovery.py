#!/usr/bin/env python3
"""Numerical discovery check for permutation maximizers of the second family.

This is discovery code, not the all-dimensional proof.  It evaluates the
weighted-shift construction against the coefficients printed in
arXiv:2606.21362 and checks d=3,...,12.

Run with a Python environment containing NumPy.
"""

from __future__ import annotations

import math

import numpy as np


def shift(d: int) -> np.ndarray:
    result = np.zeros((d, d), dtype=complex)
    for j in range(d):
        result[(j + 1) % d, j] = 1
    return result


def equality_phases(d: int) -> np.ndarray:
    delta = 0 if d % 2 else 1
    return np.exp(
        1j * np.pi * (2 * np.arange(d) + delta) / d
    )


def bad_order(d: int) -> list[int]:
    return list(range(d - 2)) + [d - 1, d - 2]


def lambda_coefficient(d: int, y: int, k: int) -> complex:
    omega = np.exp(2j * np.pi / d)
    return (
        (-1) ** k
        * omega ** (k * (k + 1) / 2)
        * omega ** (-y * (1 + k))
        / (d * np.sin(np.pi * (k + 0.5) / d))
    )


def spectral_projectors(
    observable: np.ndarray, omega: complex
) -> list[np.ndarray]:
    d = observable.shape[0]
    powers = [
        np.linalg.matrix_power(observable, power)
        for power in range(d)
    ]
    return [
        sum(
            omega ** (-a * power) * powers[power]
            for power in range(d)
        )
        / d
        for a in range(d)
    ]


def target_probabilities(
    alice_target: np.ndarray,
    alice_reference: np.ndarray,
    omega: complex,
) -> np.ndarray:
    d = alice_target.shape[0]
    target = spectral_projectors(alice_target, omega)
    reference = spectral_projectors(alice_reference, omega)
    return np.array(
        [
            [
                (
                    np.trace(target[a] @ reference[(-b) % d])
                    / d
                ).real
                for b in range(d)
            ]
            for a in range(d)
        ]
    )


def construct(d: int) -> dict[str, object]:
    omega = np.exp(2j * np.pi / d)
    roots = equality_phases(d)
    order = bad_order(d) if d >= 4 else list(range(d))
    ordered = roots[np.asarray(order)]
    x_shift = shift(d)

    alice_reference = x_shift
    alice_target = x_shift @ np.diag(ordered)

    bob: list[np.ndarray] = []
    phase_rows: list[np.ndarray] = []
    for y in range(d):
        values = 1 + omega**y * ordered
        phases = values / np.abs(values)
        phase_rows.append(phases)
        bob.append(np.conj(x_shift @ np.diag(phases)))

    alice: list[np.ndarray] = []
    fourier_bob: list[np.ndarray] = []
    for ell in range(d):
        coefficient = lambda_coefficient(
            d, 0, (ell - 1) % d
        )
        transformed = sum(
            omega ** (ell * y) * bob[y] for y in range(d)
        )
        normalized = transformed / (d * coefficient)
        fourier_bob.append(transformed)
        alice.append(np.conj(normalized))

    return {
        "omega": omega,
        "roots": roots,
        "order": order,
        "alice": alice,
        "bob": bob,
        "fourier_bob": fourier_bob,
        "alice_reference": alice_reference,
        "alice_target": alice_target,
    }


def audit_dimension(d: int) -> tuple[float, float, float]:
    data = construct(d)
    omega = data["omega"]
    alice = data["alice"]
    bob = data["bob"]
    fourier_bob = data["fourier_bob"]
    identity = np.eye(d)

    maximum_error = 0.0
    value = 0.0
    for ell in range(d):
        coefficient = lambda_coefficient(
            d, 0, (ell - 1) % d
        )
        transformed = fourier_bob[ell]
        normalized = transformed / (d * coefficient)
        maximum_error = max(
            maximum_error,
            np.linalg.norm(normalized.conj().T @ normalized - identity),
            np.linalg.norm(np.linalg.matrix_power(normalized, d) - identity),
            np.linalg.norm(np.linalg.matrix_power(alice[ell], d) - identity),
        )
        expectation = np.trace(
            alice[ell] @ transformed.T
        ) / d
        value += (np.conj(coefficient) * expectation).real

    for observable in bob:
        maximum_error = max(
            maximum_error,
            np.linalg.norm(
                observable.conj().T @ observable - identity
            ),
            np.linalg.norm(
                np.linalg.matrix_power(observable, d) - identity
            ),
        )

    maximum_error = max(
        maximum_error,
        np.linalg.norm(
            alice[0] - data["alice_reference"]
        ),
        np.linalg.norm(alice[1] - data["alice_target"]),
    )

    probabilities = target_probabilities(
        alice[1], alice[0], omega
    )
    assert abs(value - d) < 2e-10
    assert maximum_error < 2e-10
    assert abs(probabilities.sum() - 1) < 2e-10
    if d >= 4:
        assert probabilities.max() > 1 / d**2 + 1e-12

    augmented_value = value + 1
    return value, augmented_value, probabilities.max()


def main() -> None:
    for d in range(3, 13):
        value, augmented, largest = audit_dimension(d)
        print(
            f"PASS d={d}: F={value:.12f}, "
            f"Fbar={augmented:.12f}, "
            f"target_max={largest:.12f}, "
            f"uniform={1 / d**2:.12f}"
        )
    print(
        "PASS: the final-two permutation maximizes the second family "
        "and is target-nonuniform for d=4,...,12."
    )


if __name__ == "__main__":
    main()
