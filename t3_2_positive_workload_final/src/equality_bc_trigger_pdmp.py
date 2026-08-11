"""Claim-neutral algebra for the equality BC-trigger trace.

The analytic stopped-PDMP argument lives in the accompanying research
note. This module freezes only exact finite-N path probabilities, generator
increments, and leading coefficient formulas. It does not certify global
recurrence.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Rates:
    alpha: Fraction
    beta: Fraction
    lam: Fraction
    mu: Fraction
    nu: Fraction
    delta: Fraction

    def __post_init__(self) -> None:
        assert all(value > 0 for value in vars(self).values())


REACTION_DELTAS = {
    "0_to_BC": (0, 1, 1),
    "BC_to_0": (0, -1, -1),
    "B_to_A": (1, -1, 0),
    "A_to_AB": (0, 1, 0),
    "AB_to_2B": (-1, 1, 0),
    "2B_to_B": (0, -1, 0),
}


def q_value(state: tuple[int, int, int]) -> int:
    """Return Q=C-A-B."""

    a, b, c = state
    return c - a - b


def q_increment(reaction: str) -> int:
    """Exact Q increment of one reaction."""

    da, db, dc = REACTION_DELTAS[reaction]
    return dc - da - db


def trigger_asymptotic_coefficients(
    rates: Rates,
) -> tuple[Fraction, Fraction]:
    """Return c1,c2 in p_N=c1/N+c2/N^2+O(N^-3)."""

    c1 = rates.lam / rates.beta
    c2 = (
        rates.lam
        * (rates.alpha - rates.beta - rates.lam)
        / (rates.beta * rates.beta)
    )
    return c1, c2


def direct_trigger_probability(n: int, rates: Rates) -> Fraction:
    """First-event B->A probability after the primary entry."""

    assert n >= 1
    return rates.lam / (
        rates.beta * (n + 1) + rates.lam + rates.alpha
    )


def positive_unit_history_probability(n: int, rates: Rates) -> Fraction:
    """Exact probability of the three-edge positive history (2.7)."""

    assert n >= 1
    first = rates.alpha / (
        rates.beta * (n + 1) + rates.lam + rates.alpha
    )
    second = 2 * rates.delta / (
        2 * rates.beta * (n + 2)
        + 2 * rates.lam
        + 2 * rates.delta
        + rates.alpha
    )
    third = rates.beta * (n + 2) / (
        rates.beta * (n + 2) + rates.lam + rates.alpha
    )
    return first * second * third


def positive_unit_leading_coefficient(rates: Rates) -> Fraction:
    """Limit of N^2 times the probability in (2.8)."""

    return rates.alpha * rates.delta / (rates.beta * rates.beta)


def killed_potential(a: int, rates: Rates) -> Fraction:
    """Integrand beta*mu*a/(alpha+mu*a) in -log R."""

    assert a >= 0
    return (
        rates.beta * rates.mu * a
        / (rates.alpha + rates.mu * a)
    )


def power_drift_leading_coefficient(
    power_moment: Fraction,
    rates: Rates,
) -> Fraction:
    """Coefficient of N^(p-1) for a supplied E[R^p]."""

    assert 0 <= power_moment < 1
    return (rates.lam / rates.beta) * (power_moment - 1)


def certificate() -> dict[str, object]:
    rates = Rates(
        alpha=Fraction(2),
        beta=Fraction(3),
        lam=Fraction(5),
        mu=Fraction(7),
        nu=Fraction(11),
        delta=Fraction(13),
    )
    q_increments = {
        reaction: q_increment(reaction)
        for reaction in REACTION_DELTAS
    }
    assert q_increments == {
        "0_to_BC": 0,
        "BC_to_0": 0,
        "B_to_A": 0,
        "A_to_AB": -1,
        "AB_to_2B": 0,
        "2B_to_B": 1,
    }
    assert power_drift_leading_coefficient(Fraction(3, 4), rates) < 0

    return {
        "network": (
            ("0", "BC"),
            ("B", "A", "AB", "2B"),
        ),
        "q": "C-A-B",
        "q_increments": q_increments,
        "trigger_order": "N^-1",
        "conditional_duration_order": "N",
        "unconditional_mean_duration_order": "1",
        "all_higher_raw_duration_moments_uniform": False,
        "leading_power_drift_sign": "strictly negative",
        "physical_c3_found_by_this_trace": False,
        "global_pair_recurrence_certified": False,
    }


if __name__ == "__main__":
    print(certificate())
