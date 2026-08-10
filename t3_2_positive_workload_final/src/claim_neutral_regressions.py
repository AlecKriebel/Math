"""Exact regression witnesses for recurrence-proof interfaces.

This module deliberately proves no T3-2 theorem.  It contains two generic
Markov-chain counterexamples to tempting Foster arguments and two positive-
recurrent reaction-network stress tests.  Every calculation uses exact
``Fraction`` arithmetic so that the examples can be replayed without a
numerical or simulation dependency.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial
from typing import Iterable, Sequence


Vector = tuple[int, ...]


def _falling(n: int, k: int) -> int:
    if n < 0 or k < 0:
        raise ValueError("population and source counts must be nonnegative")
    if n < k:
        return 0
    product = 1
    for offset in range(k):
        product *= n - offset
    return product


@dataclass(frozen=True)
class ReactionChannel:
    """Minimal labelled stochastic mass-action channel."""

    source: Vector
    target: Vector
    rate: Fraction
    linkage: int
    label: str

    def __post_init__(self) -> None:
        if len(self.source) != len(self.target):
            raise ValueError("source and target dimensions differ")
        if any(value < 0 for value in self.source + self.target):
            raise ValueError("complex counts must be nonnegative")
        if self.rate <= 0:
            raise ValueError("rate constants must be positive")

    @property
    def molecularity(self) -> int:
        return max(sum(self.source), sum(self.target))

    def propensity(self, state: Sequence[int]) -> Fraction:
        if len(state) != len(self.source):
            raise ValueError("state dimension differs from the channel")
        factor = 1
        for population, required in zip(state, self.source):
            factor *= _falling(population, required)
        return self.rate * factor


def is_pairwise_reversible(channels: Iterable[ReactionChannel]) -> bool:
    """Return whether every labelled edge has a reverse in its linkage."""

    channels = tuple(channels)
    edges = {(channel.source, channel.target, channel.linkage) for channel in channels}
    return all(
        (channel.target, channel.source, channel.linkage) in edges
        for channel in channels
    )


# ---------------------------------------------------------------------------
# Regression 1: pointwise shell drift does not imply positive recurrence.
# ---------------------------------------------------------------------------


def shell_probabilities(level: int) -> tuple[Fraction, Fraction]:
    """Return ``(up, down)`` for the null-recurrent birth-death example.

    From level zero the chain moves to one.  For ``level >= 1`` it moves up
    with probability ``level/(2*level+1)`` and down with probability
    ``(level+1)/(2*level+1)``.  The one-step drift is strictly negative at
    every positive level, but its magnitude tends to zero.
    """

    if level < 1:
        raise ValueError("the interior formula requires level >= 1")
    denominator = 2 * level + 1
    return Fraction(level, denominator), Fraction(level + 1, denominator)


def shell_service_margin(level: int) -> Fraction:
    """Pointwise service-minus-arrival margin at one shell."""

    up, down = shell_probabilities(level)
    return down - up


def shell_reversible_weight(level: int) -> Fraction:
    """An unnormalised reversible measure for the shell chain.

    The boundary weight is one and, for ``level >= 1``,

    ``m(level) = (2*level+1)/(level*(level+1))``.

    Thus ``m(level) = 1/level + 1/(level+1)`` and its total mass diverges.
    """

    if level < 0:
        raise ValueError("level must be nonnegative")
    if level == 0:
        return Fraction(1)
    return Fraction(2 * level + 1, level * (level + 1))


def shell_edge_resistance(level: int) -> Fraction:
    """Electrical resistance of the edge ``level <-> level+1``.

    With conductance ``m(level) P(level, level+1)``, the resistance is one at
    the boundary and exactly ``level+1`` thereafter.  Its divergent sum is an
    exact recurrence certificate for this birth-death chain.
    """

    if level < 0:
        raise ValueError("level must be nonnegative")
    if level == 0:
        return Fraction(1)
    up, _ = shell_probabilities(level)
    return Fraction(1, 1) / (shell_reversible_weight(level) * up)


def shell_partial_invariant_mass(cutoff: int) -> Fraction:
    if cutoff < 0:
        raise ValueError("cutoff must be nonnegative")
    return sum((shell_reversible_weight(n) for n in range(cutoff + 1)), Fraction())


# ---------------------------------------------------------------------------
# Regression 2: lexicographic descent can hide infinite lower-level cost.
# ---------------------------------------------------------------------------


def lex_switch_mass(start: int, switch_level: int) -> Fraction:
    """Probability that ``s_start`` first switches at ``s_switch_level``.

    The CTMC rates from ``s_k`` are ``k`` to ``s_(k+1)`` and one to ``t_k``.
    Consequently ``P(M=m)=start/(m(m+1))`` for ``m >= start``.
    """

    if start < 1 or switch_level < start:
        raise ValueError("require 1 <= start <= switch_level")
    return Fraction(start, switch_level * (switch_level + 1))


def lex_switch_tail(start: int, level: int) -> Fraction:
    """Return ``P(M >= level) = start/level``."""

    if start < 1 or level < start:
        raise ValueError("require 1 <= start <= level")
    return Fraction(start, level)


def lex_switch_cdf_truncation(start: int, cutoff: int) -> Fraction:
    """Return ``P(M <= cutoff)`` exactly."""

    if start < 1 or cutoff < start:
        raise ValueError("require 1 <= start <= cutoff")
    return Fraction(1) - Fraction(start, cutoff + 1)


def lex_switch_time_truncation(start: int, cutoff: int) -> Fraction:
    """Expected pre-switch time accumulated through ``s_cutoff``.

    The chance to reach ``s_k`` is ``start/k`` and its mean holding time is
    ``1/(k+1)``.  The truncated sum equals ``1-start/(cutoff+1)`` and tends
    to one even though the switch level has infinite mean.
    """

    if start < 1 or cutoff < start:
        raise ValueError("require 1 <= start <= cutoff")
    return sum(
        (Fraction(start, k * (k + 1)) for k in range(start, cutoff + 1)),
        Fraction(),
    )


def lex_drain_cost_truncation(start: int, cutoff: int) -> Fraction:
    """Truncated expectation of the unit-rate drain after switching.

    Switching at level ``m`` costs ``m`` mean units to descend from ``t_m``
    to ``t_0``.  The truncated expectation is
    ``start * sum(1/(m+1), m=start..cutoff)``, which diverges harmonically.
    """

    if start < 1 or cutoff < start:
        raise ValueError("require 1 <= start <= cutoff")
    return sum(
        (Fraction(start, m + 1) for m in range(start, cutoff + 1)),
        Fraction(),
    )


def lex_joint_box_size(max_secondary: int) -> int:
    """Number of ``t_0, s_k, t_k`` states with ``1 <= k <= max_secondary``."""

    if max_secondary < 0:
        raise ValueError("box radius must be nonnegative")
    return 2 * max_secondary + 1


def lex_jump_increments() -> tuple[tuple[int, int], ...]:
    """All coordinate increments in the lexicographic CTMC."""

    return ((0, 1), (-1, 0), (0, -1), (1, 1))


# ---------------------------------------------------------------------------
# Regression 3: a tight environment can have genuinely infinite support.
# ---------------------------------------------------------------------------


def immigration_death_channels(
    birth_rate: Fraction = Fraction(1),
    death_rate: Fraction = Fraction(1),
) -> tuple[ReactionChannel, ReactionChannel]:
    """The reversible CRN ``0 <-> E``."""

    birth_rate = Fraction(birth_rate)
    death_rate = Fraction(death_rate)
    return (
        ReactionChannel((0,), (1,), birth_rate, 0, "0 -> E"),
        ReactionChannel((1,), (0,), death_rate, 0, "E -> 0"),
    )


def immigration_death_drift(
    population: int,
    birth_rate: Fraction = Fraction(1),
    death_rate: Fraction = Fraction(1),
) -> Fraction:
    if population < 0:
        raise ValueError("population must be nonnegative")
    return Fraction(birth_rate) - Fraction(death_rate) * population


def poisson_unnormalised_weight(
    population: int,
    birth_rate: Fraction = Fraction(1),
    death_rate: Fraction = Fraction(1),
) -> Fraction:
    """Return ``rho**population/population!`` for ``rho=birth/death``."""

    if population < 0:
        raise ValueError("population must be nonnegative")
    birth_rate = Fraction(birth_rate)
    death_rate = Fraction(death_rate)
    if birth_rate <= 0 or death_rate <= 0:
        raise ValueError("rates must be positive")
    rho = birth_rate / death_rate
    return rho**population / factorial(population)


def poisson_markov_tail_bound(
    radius: int,
    birth_rate: Fraction = Fraction(1),
    death_rate: Fraction = Fraction(1),
) -> Fraction:
    """Bound ``P(E > radius)`` by ``rho/(radius+1)``."""

    if radius < 0:
        raise ValueError("radius must be nonnegative")
    birth_rate = Fraction(birth_rate)
    death_rate = Fraction(death_rate)
    if birth_rate <= 0 or death_rate <= 0:
        raise ValueError("rates must be positive")
    rho = birth_rate / death_rate
    return rho / (radius + 1)


def poisson_tight_radius(
    epsilon: Fraction,
    birth_rate: Fraction = Fraction(1),
    death_rate: Fraction = Fraction(1),
) -> int:
    """Find a finite radius with Markov tail bound strictly below epsilon."""

    epsilon = Fraction(epsilon)
    if not 0 < epsilon < 1:
        raise ValueError("epsilon must lie in (0,1)")
    radius = 0
    while poisson_markov_tail_bound(radius, birth_rate, death_rate) >= epsilon:
        radius += 1
    return radius


# ---------------------------------------------------------------------------
# Regression 4: fast neutral CRN jumps need not have a physical-time cost.
# ---------------------------------------------------------------------------


def fast_neutral_channels(
    fast_rate: Fraction = Fraction(1),
    slow_rate: Fraction = Fraction(1),
) -> tuple[ReactionChannel, ...]:
    """Two reversible linkages ``A <-> B`` and ``0 <-> C``.

    On the pre-trace states ``A+B=n, C=0``, the fast aggregate propensity is
    ``fast_rate*n`` and the trace reaction ``0 -> C`` has constant propensity
    ``slow_rate``.
    """

    fast_rate = Fraction(fast_rate)
    slow_rate = Fraction(slow_rate)
    return (
        ReactionChannel((1, 0, 0), (0, 1, 0), fast_rate, 0, "A -> B"),
        ReactionChannel((0, 1, 0), (1, 0, 0), fast_rate, 0, "B -> A"),
        ReactionChannel((0, 0, 0), (0, 0, 1), slow_rate, 1, "0 -> C"),
        ReactionChannel((0, 0, 1), (0, 0, 0), slow_rate, 1, "C -> 0"),
    )


@dataclass(frozen=True)
class FastNeutralRace:
    shell_population: int
    fast_hazard: Fraction
    trace_hazard: Fraction
    expected_fast_jumps: Fraction
    expected_physical_time: Fraction


def fast_neutral_race(
    shell_population: int,
    fast_rate: Fraction = Fraction(1),
    slow_rate: Fraction = Fraction(1),
) -> FastNeutralRace:
    if shell_population < 0:
        raise ValueError("shell population must be nonnegative")
    fast_rate = Fraction(fast_rate)
    slow_rate = Fraction(slow_rate)
    if fast_rate <= 0 or slow_rate <= 0:
        raise ValueError("rates must be positive")
    fast_hazard = fast_rate * shell_population
    return FastNeutralRace(
        shell_population=shell_population,
        fast_hazard=fast_hazard,
        trace_hazard=slow_rate,
        expected_fast_jumps=fast_hazard / slow_rate,
        expected_physical_time=Fraction(1, 1) / slow_rate,
    )


def fast_neutral_pretrace_hazards(
    a_population: int,
    b_population: int,
    fast_rate: Fraction = Fraction(1),
    slow_rate: Fraction = Fraction(1),
) -> tuple[Fraction, Fraction]:
    """Derive aggregate fast and trace hazards from the CRN propensities."""

    if a_population < 0 or b_population < 0:
        raise ValueError("populations must be nonnegative")
    channels = fast_neutral_channels(fast_rate, slow_rate)
    state = (a_population, b_population, 0)
    fast_hazard = sum(
        (channel.propensity(state) for channel in channels if channel.linkage == 0),
        Fraction(),
    )
    trace_hazard = channels[2].propensity(state)
    if channels[3].propensity(state) != 0:
        raise AssertionError("C -> 0 must be disabled before the trace event")
    return fast_hazard, trace_hazard


def fast_neutral_jump_mass(
    shell_population: int,
    jump_count: int,
    fast_rate: Fraction = Fraction(1),
    slow_rate: Fraction = Fraction(1),
) -> Fraction:
    """Geometric mass for fast jumps before the first ``0 -> C`` reaction."""

    if jump_count < 0:
        raise ValueError("jump count must be nonnegative")
    race = fast_neutral_race(shell_population, fast_rate, slow_rate)
    total = race.fast_hazard + race.trace_hazard
    failure = race.fast_hazard / total
    success = race.trace_hazard / total
    return failure**jump_count * success


def fast_neutral_jump_tail(
    shell_population: int,
    jump_count: int,
    fast_rate: Fraction = Fraction(1),
    slow_rate: Fraction = Fraction(1),
) -> Fraction:
    """Return the probability of at least ``jump_count`` fast reactions."""

    if jump_count < 0:
        raise ValueError("jump count must be nonnegative")
    race = fast_neutral_race(shell_population, fast_rate, slow_rate)
    total = race.fast_hazard + race.trace_hazard
    return (race.fast_hazard / total) ** jump_count
