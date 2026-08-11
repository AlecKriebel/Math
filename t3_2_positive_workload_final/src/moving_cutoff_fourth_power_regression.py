"""Claim-neutral exponent arithmetic for the moving-cutoff endpoint lemma."""

from __future__ import annotations

from fractions import Fraction


def boundary_exponents(delta: Fraction) -> dict[str, Fraction]:
    """Return raw, completed, endpoint, and expected-cost powers of N."""

    raw_probability = -3 + 6 * delta
    completed_probability = raw_probability + 2
    endpoint_cost = 3 + delta
    expected_cost = completed_probability + endpoint_cost
    return {
        "raw_boundary_probability": raw_probability,
        "completed_boundary_probability": completed_probability,
        "boundary_endpoint_cost": endpoint_cost,
        "expected_boundary_cost": expected_cost,
        "service_cost": Fraction(3),
    }


def cutoff_is_lower_order(delta: Fraction) -> bool:
    row = boundary_exponents(delta)
    return row["expected_boundary_cost"] < row["service_cost"]


def canonical_cutoff() -> Fraction:
    return Fraction(1, 8)

