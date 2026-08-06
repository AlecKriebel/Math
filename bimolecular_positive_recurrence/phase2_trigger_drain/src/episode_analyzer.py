#!/usr/bin/env python3
"""Exact trigger-and-drain bounds for the canonical stress cycle.

Network (falling-factorial convention):
    0 --alpha--> A+B --beta--> B --gamma--> 0.

The episode starts on B=0, waits for the first immigration, and ends at the
first subsequent return to B=0.  The formulas below are analytic identities
or rigorous inequalities; no simulation or floating-point inference is used.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import exp


@dataclass(frozen=True, slots=True)
class StressCycleBounds:
    alpha: Fraction
    beta: Fraction
    gamma: Fraction

    def __post_init__(self) -> None:
        if min(self.alpha, self.beta, self.gamma) <= 0:
            raise ValueError("all rates must be positive")

    @property
    def tagged_kill_probability_lower_bound(self) -> Fraction:
        """Probability the tagged A is killed before the first relevant event.

        Immediately after the trigger B=1.  In the marginal process consisting
        of B and one tagged A, the competing relevant clocks have rates alpha
        (another immigration), gamma (loss of B), and beta (loss of the tag).
        Other A+B firings are self-transitions for this marginal process.
        """
        return self.beta / (self.alpha + self.beta + self.gamma)

    @property
    def tagged_survival_probability_upper_bound(self) -> Fraction:
        return 1 - self.tagged_kill_probability_lower_bound

    def mean_busy_period(self) -> float:
        """Exact mean B-busy-period length, represented as a real expression.

        For the immigration-death B process, rho=alpha/gamma and stationary
        mass at zero is exp(-rho).  A regenerative cycle consists of a mean
        1/alpha hold at zero followed by the busy period.  Hence
        E[T_busy]=(exp(rho)-1)/alpha.
        """
        a, g = float(self.alpha), float(self.gamma)
        return (exp(a / g) - 1.0) / a

    def mean_complete_episode(self) -> float:
        """Mean initial waiting time plus mean busy period: exp(alpha/gamma)/alpha."""
        a, g = float(self.alpha), float(self.gamma)
        return exp(a / g) / a

    def expected_births_during_busy_period(self) -> float:
        """Exact first moment alpha E[T_busy]=exp(alpha/gamma)-1."""
        return float(self.alpha) * self.mean_busy_period()

    def expected_A_endpoint_upper_bound(self, n: int) -> float:
        """Rigorous upper bound on E[A_tau | (A_0,B_0)=(n,0)]."""
        if n < 0:
            raise ValueError("n must be nonnegative")
        q = float(self.tagged_survival_probability_upper_bound)
        return q * (n + 1) + self.expected_births_during_busy_period()

    def contraction_threshold(self) -> int:
        """An integer n0 such that the endpoint mean is < n for n>=n0."""
        delta = float(self.tagged_kill_probability_lower_bound)
        additive = float(self.tagged_survival_probability_upper_bound) + self.expected_births_during_busy_period()
        # Need -delta*n + additive < 0.  Add one to make the inequality strict.
        return int(additive / delta) + 1


def self_test() -> None:
    b = StressCycleBounds(Fraction(1), Fraction(1), Fraction(1))
    assert b.tagged_kill_probability_lower_bound == Fraction(1, 3)
    assert b.tagged_survival_probability_upper_bound == Fraction(2, 3)
    assert abs(b.mean_busy_period() - (exp(1.0) - 1.0)) < 1e-14
    assert abs(b.mean_complete_episode() - exp(1.0)) < 1e-14
    n0 = b.contraction_threshold()
    assert b.expected_A_endpoint_upper_bound(n0) < n0


if __name__ == "__main__":
    self_test()
    print("episode_analyzer.py self-test: OK")
