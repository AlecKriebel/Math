"""Exact algebraic calibrations introduced for Version 1.1."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable


def _positive_rate(value: Fraction, name: str) -> Fraction:
    value = Fraction(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


@dataclass(frozen=True)
class RateDegenerationFixedMLimit:
    """Formal coefficients in the fixed-``m``, ``kappa_2 -> 0`` limit."""

    a_log_m_coefficient: Fraction
    continue_from_a: Fraction
    limit_log_m_coefficient: Fraction
    limit_log_m_minus_one_coefficient: Fraction


def rate_degeneration_fixed_m_limit(
    m: int,
    kappa_0: Fraction,
    kappa_1: Fraction,
) -> RateDegenerationFixedMLimit:
    """Return the exact formal limit ``a_m(1+p_m)``.

    The result represents

    ``D_0(m,A) -> limit_log_m_coefficient * log(m)``.
    """
    if not isinstance(m, int) or isinstance(m, bool) or m < 2:
        raise ValueError("m must be an integer at least two")
    kappa_0 = _positive_rate(kappa_0, "kappa_0")
    kappa_1 = _positive_rate(kappa_1, "kappa_1")
    total_a = kappa_0 + kappa_1 * m
    a_coefficient = kappa_0 / total_a
    continuation = kappa_1 * m / total_a
    return RateDegenerationFixedMLimit(
        a_log_m_coefficient=a_coefficient,
        continue_from_a=continuation,
        limit_log_m_coefficient=a_coefficient * (1 + continuation),
        limit_log_m_minus_one_coefficient=Fraction(0),
    )


@dataclass(frozen=True)
class ACKUnshiftedEntropyDrift:
    """Formal reward ``log2_coefficient*log(2) + constant``."""

    log2_coefficient: Fraction
    constant: Fraction


def ack_unshifted_entropy_drift(
    n: int,
    kappa_1: Fraction,
) -> ACKUnshiftedEntropyDrift:
    """Generator drift at ACK Example 4.1's ``x_n=(n,1,0)``."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    kappa_1 = _positive_rate(kappa_1, "kappa_1")
    return ACKUnshiftedEntropyDrift(
        log2_coefficient=2 * kappa_1 * n,
        constant=-kappa_1 * n,
    )


@dataclass(frozen=True)
class ACKMarkedEpisode:
    """Exact marked-target reward for the path ``A->A+B->A+C->C``.

    The expected reward is represented without floating point as

    ``log2_coefficient*log(2)``
    ``+ log_n_coefficient*log(n)``
    ``+ log_n_minus_one_coefficient*log(n-1)``.
    """

    continue_a: Fraction
    continue_ab: Fraction
    continue_ac: Fraction
    log2_coefficient: Fraction
    log_n_coefficient: Fraction
    log_n_minus_one_coefficient: Fraction


def ack_marked_target_episode(
    n: int,
    kappa_1: Fraction,
    kappa_2: Fraction,
    kappa_3: Fraction,
    kappa_4: Fraction,
    kappa_5: Fraction,
) -> ACKMarkedEpisode:
    """Return the complete exact episode reward in ACK Example 4.1.

    The start is the reachable marked state ``((n,1,0), A)`` and the fixed
    target-following path is ``A -> A+B -> A+C -> C``.  At terminal ``C``
    the episode takes one final ordinary jump.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("n must be an integer at least two")
    kappa_1 = _positive_rate(kappa_1, "kappa_1")
    kappa_2 = _positive_rate(kappa_2, "kappa_2")
    kappa_3 = _positive_rate(kappa_3, "kappa_3")
    kappa_4 = _positive_rate(kappa_4, "kappa_4")
    kappa_5 = _positive_rate(kappa_5, "kappa_5")

    continue_a = kappa_1 / (kappa_1 + kappa_2)

    total_ab = n * (kappa_1 + 2 * kappa_2) + 2 * kappa_5
    continue_ab = 2 * kappa_2 * n / total_ab
    ab_log2 = kappa_1 * n / total_ab
    ab_log_n = 2 * kappa_5 / total_ab

    source_sum = kappa_1 + kappa_2 + kappa_3
    total_ac = n * source_sum + kappa_4
    continue_ac = kappa_3 * n / total_ac
    ac_log_n = kappa_4 / total_ac

    total_c = (n - 1) * source_sum + kappa_4
    c_log_n_minus_one = -(n - 1) * source_sum / total_c

    return ACKMarkedEpisode(
        continue_a=continue_a,
        continue_ab=continue_ab,
        continue_ac=continue_ac,
        log2_coefficient=continue_a * ab_log2,
        log_n_coefficient=(
            continue_a * ab_log_n
            + continue_a * continue_ab * ac_log_n
        ),
        log_n_minus_one_coefficient=(
            continue_a
            * continue_ab
            * continue_ac
            * c_log_n_minus_one
        ),
    )


def ack_marked_target_log_coefficient(
    kappa_1: Fraction,
    kappa_2: Fraction,
    kappa_3: Fraction,
) -> Fraction:
    """Return ``-alpha``, the coefficient of ``log(n)`` at infinity."""
    kappa_1 = _positive_rate(kappa_1, "kappa_1")
    kappa_2 = _positive_rate(kappa_2, "kappa_2")
    kappa_3 = _positive_rate(kappa_3, "kappa_3")
    alpha = (
        kappa_1
        / (kappa_1 + kappa_2)
        * (2 * kappa_2)
        / (kappa_1 + 2 * kappa_2)
        * kappa_3
        / (kappa_1 + kappa_2 + kappa_3)
    )
    return -alpha


@dataclass(frozen=True)
class DirectedCycleOccupation:
    """Exact regenerative occupation for a finite directed CTMC cycle."""

    expected_cycle_time: Fraction
    unnormalized_occupation: tuple[Fraction, ...]
    stationary: tuple[Fraction, ...]


def directed_cycle_return_occupation(
    rates: Iterable[Fraction],
) -> DirectedCycleOccupation:
    """Normalize one mean holding time at each state of a directed cycle."""
    positive_rates = tuple(
        _positive_rate(rate, f"rate_{index}")
        for index, rate in enumerate(rates)
    )
    if len(positive_rates) < 2:
        raise ValueError("a directed calibration cycle needs at least two states")
    occupation = tuple(Fraction(1) / rate for rate in positive_rates)
    cycle_time = sum(occupation, Fraction(0))
    return DirectedCycleOccupation(
        expected_cycle_time=cycle_time,
        unnormalized_occupation=occupation,
        stationary=tuple(value / cycle_time for value in occupation),
    )
