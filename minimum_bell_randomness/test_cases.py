#!/usr/bin/env python3
"""Dependency-free finite regression tests for d=2,...,6.

The all-dimensional results are analytic.  These checks independently test
their scalar and Fourier ingredients, while the separate exact d=4 verifier
checks the full second-family matrices and SOS over Q(zeta_16).
"""

from __future__ import annotations

import cmath
import math

from verify_binary_2x2 import verify_formal_sos, verify_ideal_strategy
from verify_second_family_d4_exact import main as verify_exact_d4


TOLERANCE = 2e-11


def roots(d: int) -> list[complex]:
    delta = 0 if d % 2 else 1
    return [
        cmath.exp(1j * math.pi * (2 * k + delta) / d)
        for k in range(d)
    ]


def bad_order(d: int) -> list[int]:
    if d < 4:
        return list(range(d))
    return list(range(d - 2)) + [d - 1, d - 2]


def polar_phase(value: complex) -> complex:
    assert abs(value) > 1e-12
    return value / abs(value)


def lambda_coefficient(d: int, ell: int) -> complex:
    eta = cmath.exp(1j * math.pi / d)
    return (
        (-1) ** (ell - 1)
        * eta ** (ell * (ell - 1))
        / (d * math.sin(math.pi * (ell - 0.5) / d))
    )


def audit_dimension(d: int) -> tuple[float, float]:
    omega = cmath.exp(2j * math.pi / d)
    eta = cmath.exp(1j * math.pi / d)
    delta = 0 if d % 2 else 1
    equality_roots = roots(d)
    order = bad_order(d)

    product_roots = math.prod(equality_roots)
    assert abs(product_roots - 1) < TOLERANCE

    scalar_maximum = 2 / math.sin(math.pi / (2 * d))
    for z in equality_roots:
        scalar_value = sum(abs(1 + omega**y * z) for y in range(d))
        assert abs(scalar_value - scalar_maximum) < TOLERANCE

    phase_rows: list[list[complex]] = []
    for y in range(d):
        phases = [
            polar_phase(1 + omega**y * equality_roots[k])
            for k in range(d)
        ]
        phase_rows.append(phases)
        assert abs(math.prod(phases) - 1) < TOLERANCE

    # Exact-form DFT coefficient behind the second-family theorem.
    maximum_dft_error = 0.0
    for ell in range(d):
        coefficient = lambda_coefficient(d, ell)
        q_ell = eta ** (-ell * (ell - 1 + delta))
        for r in range(d):
            direct = sum(
                omega ** (ell * y)
                * phase_rows[y][r].conjugate()
                for y in range(d)
            )
            expected = (
                d * coefficient * q_ell * omega ** (-ell * r)
            )
            maximum_dft_error = max(
                maximum_dft_error, abs(direct - expected)
            )

        order_exponent = (
            ell * (ell - 1 + delta) + ell * (d - 1)
        )
        assert order_exponent % 2 == 0
    assert maximum_dft_error < TOLERANCE

    # Target Fourier table.
    q = [1 + 0j]
    for j in range(d - 1):
        q.append(q[-1] * equality_roots[order[j]])
    assert abs(q[-1] * equality_roots[order[-1]] - 1) < TOLERANCE
    qhat_norms = [
        abs(sum(q[j] * omega ** (m * j) for j in range(d))) ** 2
        for m in range(d)
    ]
    assert abs(sum(qhat_norms) - d**2) < TOLERANCE
    target_maximum = max(qhat_norms) / d**3
    if d <= 3:
        assert abs(target_maximum - 1 / d**2) < TOLERANCE
    else:
        assert target_maximum > 1 / d**2 + 1e-12

    return maximum_dft_error, target_maximum


def main() -> None:
    verify_formal_sos()
    verify_ideal_strategy()
    print("PASS d=2: exact binary SOS and ideal strategy")

    for d in range(2, 7):
        error, target = audit_dimension(d)
        print(
            f"PASS d={d}: cyclic scalar/DFT identities, "
            f"DFT error={error:.3e}, target_max={target:.12f}"
        )

    verify_exact_d4()
    print("PASS: complete finite regression suite for d=2,...,6")


if __name__ == "__main__":
    main()
