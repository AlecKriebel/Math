"""Exact algebra certificate for the residual two-linkage pair.

This module checks only the finite rate identities used in
``research_notes/residual_pair_full_proof.md``.  It is not a numerical
simulation and does not replace the physical-time estimates in that note.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional


Q = Fraction


@dataclass(frozen=True)
class FastRates:
    """Rates on B, 2A, B+C in the order used by the proof note."""

    x: Q  # B -> 2A
    y: Q  # B -> B+C
    s: Q  # 2A -> B
    r: Q  # 2A -> B+C
    t: Q  # B+C -> B
    v: Q  # B+C -> 2A


@dataclass(frozen=True)
class SlowRates:
    """Rates on 0, A, C."""

    k_0a: Q
    k_0c: Q
    k_a0: Q
    k_ac: Q
    k_c0: Q
    k_ca: Q


def falling_two(value: int) -> int:
    return value * (value - 1) if value >= 2 else 0


def fast_scalars(rate: FastRates) -> tuple[Q, Q, Q]:
    d = rate.t + rate.v
    if d <= 0:
        raise ValueError("B+C must have an outgoing edge")
    zeta = 2 * rate.v / d
    alpha = rate.x + rate.v * rate.y / d
    beta = 2 * (rate.s + rate.r * rate.t / d)
    if alpha <= 0 or beta <= 0:
        raise ValueError("strong connectivity forces alpha,beta > 0")
    return zeta, alpha, beta


def _near_one(lower: Q, upper: Optional[Q]) -> Q:
    """Choose a rational point in an open interval whose closure contains 1."""

    if lower < 1 and (upper is None or upper > 1):
        return Q(1)
    if lower == 1:
        if upper is not None and upper <= 1:
            raise ValueError("empty interval at one")
        gap = Q(1, 10) if upper is None else min(Q(1, 10), (upper - 1) / 2)
        return 1 + gap
    if upper == 1 and lower < 1:
        return 1 - min(Q(1, 10), (1 - lower) / 2)
    raise ValueError("interval closure must contain one")


def choose_weights(fast: FastRates, slow: SlowRates) -> tuple[Q, Q]:
    """Return lambda,rho from the two strict intervals in the proof."""

    if fast.s + fast.r <= 0:
        raise ValueError("2A must have an outgoing edge")
    lower_0 = fast.r / (fast.s + fast.r)
    upper_0 = None if fast.v == 0 else (fast.t + fast.v) / fast.v
    lam = _near_one(lower_0, upper_0)

    if slow.k_a0 + slow.k_ac <= 0 or slow.k_c0 + slow.k_ca <= 0:
        raise ValueError("A and C must each have an outgoing edge")
    lower_1 = slow.k_ac / (slow.k_a0 + slow.k_ac)
    upper_1 = (
        None
        if slow.k_ca == 0
        else (slow.k_c0 + slow.k_ca) / slow.k_ca
    )
    rho = _near_one(lower_1, upper_1)
    if 2 * rho - lam <= 0:
        raise AssertionError("near-one choices must give a positive B weight")
    return lam, rho


def workload_coefficients(
    fast: FastRates, slow: SlowRates, lam: Q, rho: Q
) -> dict[str, Q]:
    values = {
        "p_a": rho,
        "p_b": 2 * rho - lam,
        "p_c": Q(1),
        "c_b": fast.x * lam + fast.y,
        "c_2": (fast.s + fast.r) * lam - fast.r,
        "c_bc": fast.t + fast.v - fast.v * lam,
        "d_a": (slow.k_a0 + slow.k_ac) * rho - slow.k_ac,
        "d_c": slow.k_c0 + slow.k_ca - slow.k_ca * rho,
        "k_0": slow.k_0a * rho + slow.k_0c,
    }
    for key in ("p_a", "p_b", "p_c", "c_2", "c_bc", "d_a", "d_c"):
        if values[key] <= 0:
            raise ValueError(f"nonpositive certified coefficient: {key}")
    return values


def certified_generator(state: tuple[int, int, int], coeff: dict[str, Q]) -> Q:
    a, b, c = state
    return (
        coeff["k_0"]
        + coeff["c_b"] * b
        - coeff["c_2"] * falling_two(a)
        - coeff["c_bc"] * b * c
        - coeff["d_a"] * a
        - coeff["d_c"] * c
    )


def direct_generator(
    state: tuple[int, int, int], fast: FastRates, slow: SlowRates, coeff: dict[str, Q]
) -> Q:
    a, b, c = state
    weight = (coeff["p_a"], coeff["p_b"], coeff["p_c"])
    total = Q(0)

    def add(rate: Q, propensity: int, jump: tuple[int, int, int]) -> None:
        nonlocal total
        total += rate * propensity * sum(weight[i] * jump[i] for i in range(3))

    add(fast.x, b, (2, -1, 0))
    add(fast.y, b, (0, 0, 1))
    add(fast.s, falling_two(a), (-2, 1, 0))
    add(fast.r, falling_two(a), (-2, 1, 1))
    add(fast.t, b * c, (0, 0, -1))
    add(fast.v, b * c, (2, -1, -1))
    add(slow.k_0a, 1, (1, 0, 0))
    add(slow.k_0c, 1, (0, 0, 1))
    add(slow.k_a0, a, (-1, 0, 0))
    add(slow.k_ac, a, (-1, 0, 1))
    add(slow.k_c0, c, (0, 0, -1))
    add(slow.k_ca, c, (1, 0, -1))
    return total


def direct_riccati(state: tuple[int, int, int], fast: FastRates) -> Q:
    a, b, c = state
    zeta, _, _ = fast_scalars(fast)
    total = Q(0)
    total += fast.x * b * 2
    total += fast.y * b * zeta
    total += fast.s * falling_two(a) * -2
    total += fast.r * falling_two(a) * (-2 + zeta)
    total += fast.t * b * c * -zeta
    total += fast.v * b * c * (2 - zeta)
    return total


def certified_riccati(state: tuple[int, int, int], fast: FastRates) -> Q:
    a, b, _ = state
    _, alpha, beta = fast_scalars(fast)
    return 2 * alpha * b - beta * falling_two(a)
