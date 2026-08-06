from fractions import Fraction
from math import exp

from phase2_trigger_drain.src.episode_analyzer import StressCycleBounds


def test_exact_tag_bound_and_means() -> None:
    b = StressCycleBounds(Fraction(2), Fraction(3), Fraction(5))
    assert b.tagged_kill_probability_lower_bound == Fraction(3, 10)
    assert b.tagged_survival_probability_upper_bound == Fraction(7, 10)
    assert abs(b.mean_complete_episode() - exp(2 / 5) / 2) < 1e-14


def test_contraction_threshold() -> None:
    b = StressCycleBounds(Fraction(7, 3), Fraction(5, 2), Fraction(11, 4))
    n0 = b.contraction_threshold()
    assert b.expected_A_endpoint_upper_bound(n0) < n0
    if n0:
        # Minimality is not claimed, only validity.
        assert n0 >= 1
