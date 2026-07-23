#!/usr/bin/env python3
"""Exact directed verifier for the full-interval split-kernel barrier."""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
from typing import Optional


Q = Fraction
ROOT = Path(__file__).resolve().parents[1]


def arctangent_bounds(inverse: int, terms: int) -> tuple[Q, Q]:
    """Alternating-series bounds for atan(1/inverse)."""
    x = Q(1, inverse)
    partial = sum(
        (
            (-1 if index % 2 else 1)
            * x ** (2 * index + 1)
            / (2 * index + 1)
            for index in range(terms)
        ),
        Q(0),
    )
    next_magnitude = x ** (2 * terms + 1) / (2 * terms + 1)
    if terms % 2 == 0:
        return partial, partial + next_magnitude
    return partial - next_magnitude, partial


def pi_bounds(terms_5: int, terms_239: int) -> tuple[Q, Q]:
    """Directed rational bounds from Machin's identity."""
    a_lower, a_upper = arctangent_bounds(5, terms_5)
    b_lower, b_upper = arctangent_bounds(239, terms_239)
    return (
        16 * a_lower - 4 * b_upper,
        16 * a_upper - 4 * b_lower,
    )


def cosine_at_rational_bounds(x: Q, terms: int) -> tuple[Q, Q]:
    """Alternating Taylor enclosure for cos(x), 0<=x<=pi."""
    assert x >= 0
    partial = sum(
        (
            (-1 if index % 2 else 1)
            * x ** (2 * index)
            / math.factorial(2 * index)
            for index in range(terms)
        ),
        Q(0),
    )
    next_magnitude = x ** (2 * terms) / math.factorial(2 * terms)
    if terms % 2 == 0:
        return partial, partial + next_magnitude
    return partial - next_magnitude, partial


def cosine_residue_bounds(
    residue: int,
    order: int,
    pi_interval: tuple[Q, Q],
    terms: int,
) -> tuple[Q, Q]:
    """Enclose cos(2*pi*residue/order), with residue<=order/2."""
    if residue == 0:
        return Q(1), Q(1)
    assert 0 < 2 * residue < order
    pi_lower, pi_upper = pi_interval
    x_lower = Q(2 * residue, order) * pi_lower
    x_upper = Q(2 * residue, order) * pi_upper
    # Cosine is decreasing on [0,pi].
    lower, _ = cosine_at_rational_bounds(x_upper, terms)
    _, upper = cosine_at_rational_bounds(x_lower, terms)
    return lower, upper


def verify(certificate_path: Optional[Path] = None) -> dict[str, object]:
    if certificate_path is None:
        certificate_path = (
            ROOT
            / "certificates"
            / "split_kernel_full_interval_counterexample.json"
        )
    data = json.loads(certificate_path.read_text())
    assert data["schema"] == "split-kernel-full-interval-counterexample-v1"
    order = data["order"]
    assert order == 41
    denominator = data["weight_denominator"]

    linear_frequencies = data["linear"]["frequencies"]
    linear_weights = [
        Q(value, denominator)
        for value in data["linear"]["weights_numerators"]
    ]
    quadratic_frequencies = data["quadratic"]["frequencies"]
    quadratic_weights = [
        Q(value, denominator)
        for value in data["quadratic"]["weights_numerators"]
    ]
    assert linear_frequencies == [0, 1, 15]
    assert quadratic_frequencies == [3, 5, 6, 7, 12, 16, 18]
    assert set(linear_frequencies).isdisjoint(quadratic_frequencies)
    assert all(weight > 0 for weight in linear_weights + quadratic_weights)
    assert sum(linear_weights) == 1
    assert sum(quadratic_weights) == 1

    assert data["linear"]["rank"] == 1 + 2 * 2 == 5
    assert data["quadratic"]["rank"] == 2 * 7 == 14
    assert data["combined"]["rank"] == 19
    assert Q(data["linear"]["diagonal"]) == Q(1, 2)
    assert Q(data["quadratic"]["diagonal"]) == Q(4, 5)
    assert Q(data["combined"]["diagonal"]) == Q(13, 10)
    assert Q(data["linear"]["trace"]) == Q(41, 2)
    assert Q(data["quadratic"]["trace"]) == Q(164, 5)

    settings = data["interval_verification"]
    pi_interval = pi_bounds(
        settings["atan_1_over_5_terms"],
        settings["atan_1_over_239_terms"],
    )
    pi_lower, pi_upper = pi_interval
    assert Q(3) < pi_lower < pi_upper < Q(22, 7)

    # Exact tangent audit of the algebra behind Machin's identity.
    tan_a = Q(1, 5)
    tan_2a = 2 * tan_a / (1 - tan_a**2)
    tan_4a = 2 * tan_2a / (1 - tan_2a**2)
    assert tan_2a == Q(5, 12)
    assert tan_4a == Q(120, 119)
    tan_b = Q(1, 239)
    assert (tan_4a - tan_b) / (1 + tan_4a * tan_b) == 1

    cosine_bounds = {0: (Q(1), Q(1))}
    for residue in range(1, 21):
        cosine_bounds[residue] = cosine_residue_bounds(
            residue,
            order,
            pi_interval,
            settings["cosine_terms"],
        )
        lower, upper = cosine_bounds[residue]
        assert -1 < lower < upper < 1

    def bounds_for_frequency(frequency: int, difference: int) -> tuple[Q, Q]:
        residue = (frequency * difference) % order
        residue = min(residue, order - residue)
        return cosine_bounds[residue]

    entry_bounds: list[tuple[Q, Q]] = []
    for difference in range(1, 21):
        lower = Q(0)
        upper = Q(0)
        for weight, frequency in zip(linear_weights, linear_frequencies):
            cosine_lower, cosine_upper = bounds_for_frequency(
                frequency, difference
            )
            lower += Q(1, 2) * weight * cosine_lower
            upper += Q(1, 2) * weight * cosine_upper
        for weight, frequency in zip(
            quadratic_weights, quadratic_frequencies
        ):
            cosine_lower, cosine_upper = bounds_for_frequency(
                frequency, difference
            )
            lower += Q(4, 5) * weight * cosine_lower
            upper += Q(4, 5) * weight * cosine_upper
        entry_bounds.append((lower, upper))

    endpoint_lower = Q(data["combined"]["offdiagonal_lower_bound"])
    endpoint_upper = Q(data["combined"]["offdiagonal_upper_bound"])
    buffer = Q(data["combined"]["certified_endpoint_buffer"])
    assert endpoint_lower == -Q(21, 80)
    assert endpoint_upper == Q(3, 10)
    assert buffer == Q(1, 2000)
    assert all(
        lower > endpoint_lower + buffer
        and upper < endpoint_upper - buffer
        for lower, upper in entry_bounds
    )

    # Exact Fourier eigenvalues.  P_0 has rank one and each nonzero
    # real-frequency projector has rank two.
    linear_eigenvalues = [
        Q(41, 2) * linear_weights[0],
        Q(41, 4) * linear_weights[1],
        Q(41, 4) * linear_weights[2],
    ]
    quadratic_eigenvalues = [
        Q(82, 5) * weight for weight in quadratic_weights
    ]
    assert all(value > 0 for value in linear_eigenvalues)
    assert all(value > 0 for value in quadratic_eigenvalues)
    shifted_constant = linear_eigenvalues[0] - Q(3, 10) * order
    assert shifted_constant < 0
    assert data["shifted"]["negative_eigenvalue_count"] == 1
    assert data["shifted"]["rank"] == 19

    # The rank-five Gram source suggested by A alone is not a code:
    # at cyclic difference 3, its inner product is rigorously above 1/2.
    source_lower = Q(0)
    for weight, frequency in zip(linear_weights, linear_frequencies):
        cosine_lower, _ = bounds_for_frequency(frequency, 3)
        source_lower += weight * cosine_lower
    assert source_lower > Q(1, 2)

    minimum_lower = min(lower for lower, _ in entry_bounds)
    maximum_upper = max(upper for _, upper in entry_bounds)
    return {
        "status": "PASS",
        "order": order,
        "rank_A": 5,
        "rank_B": 14,
        "rank_R": 19,
        "rank_K": 19,
        "negative_eigenvalues_K": 1,
        "all_weights_positive": True,
        "minimum_entry_lower_bound_decimal": f"{float(minimum_lower):.12f}",
        "maximum_entry_upper_bound_decimal": f"{float(maximum_upper):.12f}",
        "certified_endpoint_buffer": str(buffer),
        "full_interval_verified": True,
        "linear_source_violates_code_bound": True,
        "conclusion": (
            "all abstract split-rank, Ky Fan, Lorentzian-sign, and full "
            "entry-interval constraints are feasible at order 41"
        ),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
