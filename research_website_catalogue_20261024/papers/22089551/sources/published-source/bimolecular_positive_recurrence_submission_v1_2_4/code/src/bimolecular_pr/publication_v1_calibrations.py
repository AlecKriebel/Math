"""Exact calibrations added for the publication-candidate audit.

These routines do not attempt to prove the universal recurrence theorem.
They encode a few finite algebraic interfaces whose omission or reversal is
easy to detect in regression tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable


@dataclass(frozen=True)
class RateDegenerationEpisode:
    """Exact recursion data for ``0 -> A -> A+B -> 0``.

    Starting from population ``(m, 0)`` with carried target ``A``, the
    target-following path has two designated edges and then one final ordinary
    jump at terminal complex zero.  The total expected potential increment is

    ``log_m_coefficient * log(m)``
    ``+ log_m_minus_one_coefficient * log(m - 1)``.
    """

    phase_a_increment_log_m: Fraction
    continue_from_a: Fraction
    phase_ab_increment_log_m: Fraction
    continue_from_ab: Fraction
    terminal_increment_log_m_minus_one: Fraction
    log_m_coefficient: Fraction
    log_m_minus_one_coefficient: Fraction


def _positive_rate(value: Fraction, name: str) -> Fraction:
    value = Fraction(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def rate_degeneration_episode(
    m: int,
    kappa_0: Fraction,
    kappa_1: Fraction,
    kappa_2: Fraction,
) -> RateDegenerationEpisode:
    """Return the exact finite episode recursion for the three-complex cycle."""
    if not isinstance(m, int) or isinstance(m, bool) or m < 2:
        raise ValueError("m must be an integer at least two")
    kappa_0 = _positive_rate(kappa_0, "kappa_0")
    kappa_1 = _positive_rate(kappa_1, "kappa_1")
    kappa_2 = _positive_rate(kappa_2, "kappa_2")

    total_a = kappa_0 + kappa_1 * m
    phase_a = kappa_0 / total_a
    continue_a = kappa_1 * m / total_a

    total_ab = kappa_0 + (kappa_1 + kappa_2) * m
    phase_ab = kappa_0 / total_ab
    continue_ab = kappa_2 * m / total_ab

    total_zero = kappa_0 + kappa_1 * (m - 1)
    terminal = -kappa_1 * (m - 1) / total_zero

    return RateDegenerationEpisode(
        phase_a_increment_log_m=phase_a,
        continue_from_a=continue_a,
        phase_ab_increment_log_m=phase_ab,
        continue_from_ab=continue_ab,
        terminal_increment_log_m_minus_one=terminal,
        log_m_coefficient=phase_a + continue_a * phase_ab,
        log_m_minus_one_coefficient=continue_a * continue_ab * terminal,
    )


def rate_degeneration_asymptotic_coefficient(
    kappa_1: Fraction,
    kappa_2: Fraction,
) -> Fraction:
    """Coefficient of ``log(m)`` in the fixed-rate large-``m`` asymptotic."""
    kappa_1 = _positive_rate(kappa_1, "kappa_1")
    kappa_2 = _positive_rate(kappa_2, "kappa_2")
    return -kappa_2 / (kappa_1 + kappa_2)


@dataclass(frozen=True)
class TwoStateOccupation:
    expected_cycle_time: Fraction
    occupation_0: Fraction
    occupation_1: Fraction
    stationary_0: Fraction
    stationary_1: Fraction


def two_state_return_cycle_occupation(
    rate_01: Fraction,
    rate_10: Fraction,
) -> TwoStateOccupation:
    """Exact return-cycle occupation formula for a two-state CTMC."""
    rate_01 = _positive_rate(rate_01, "rate_01")
    rate_10 = _positive_rate(rate_10, "rate_10")
    occupation_0 = Fraction(1, 1) / rate_01
    occupation_1 = Fraction(1, 1) / rate_10
    cycle_time = occupation_0 + occupation_1
    return TwoStateOccupation(
        expected_cycle_time=cycle_time,
        occupation_0=occupation_0,
        occupation_1=occupation_1,
        stationary_0=occupation_0 / cycle_time,
        stationary_1=occupation_1 / cycle_time,
    )


def absorbing_singleton_stationary(state: Hashable) -> dict[Hashable, Fraction]:
    """The stationary law for a separately handled absorbing singleton."""
    return {state: Fraction(1)}


def stopped_foster_increment(
    current_potential: Fraction,
    transitions: tuple[tuple[Fraction, Fraction], ...],
    *,
    in_exceptional_set: bool = False,
) -> Fraction:
    """Exact conditional increment of ``V(Y_{n∧σ}) + n∧σ``.

    ``transitions`` contains ``(probability, next_potential)`` pairs for one
    endpoint-chain step.  Once the exceptional set has been hit the stopped
    process has increment zero.
    """
    current_potential = Fraction(current_potential)
    if current_potential < 0:
        raise ValueError("potential must be nonnegative")
    if in_exceptional_set:
        return Fraction(0)
    if not transitions:
        raise ValueError("an unstopped state needs at least one transition")
    probability_sum = sum((Fraction(p) for p, _ in transitions), Fraction(0))
    if probability_sum != 1:
        raise ValueError("transition probabilities must sum to one")
    if any(Fraction(p) < 0 or Fraction(value) < 0 for p, value in transitions):
        raise ValueError("probabilities and potentials must be nonnegative")
    expected_next = sum(
        (Fraction(p) * Fraction(value) for p, value in transitions),
        Fraction(0),
    )
    return expected_next - current_potential + 1
