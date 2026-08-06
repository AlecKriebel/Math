#!/usr/bin/env python3
"""Exact target/source residual identities for the Phase-V proof.

The augmented jump-chain state is (x,t), where t is the target complex of
its most recent reaction and x>=t.  Put r=x-t.  If the next reaction is
s->u, the new residual is x-s, so

    V(x-s+u,u)-V(x,t) = log((x)_t/(x)_s)

for V(x,t)=sum_i log((x_i-t_i)!).  The module verifies the underlying
integer identity exactly; floating logarithms are used only to display or
calibrate the already exact ratio.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import factorial, lgamma, log
from pathlib import Path
import sys
from typing import Iterable, Mapping, Sequence

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT))

from src.generator import Complex, Reaction, propensity_factor  # type: ignore  # noqa:E402

State = tuple[int, ...]


def nontrivial_reactions(reactions: Iterable[Reaction]) -> tuple[Reaction, ...]:
    """Remove zero-vector reactions, which do not occur in the jump chain."""
    return tuple(r for r in reactions if r.source != r.target)


def residual(x: Sequence[int], target: Sequence[int]) -> State:
    if len(x) != len(target):
        raise ValueError("dimension mismatch")
    if any(xi < ti for xi, ti in zip(x, target)):
        raise ValueError("the carried target is not present")
    return tuple(int(xi - ti) for xi, ti in zip(x, target))


def residual_factorial_integer(x: Sequence[int], target: Sequence[int]) -> int:
    """Return prod_i (x_i-target_i)! exactly."""
    r = residual(x, target)
    out = 1
    for ri in r:
        out *= factorial(ri)
    return out


def potential(x: Sequence[int], target: Sequence[int]) -> float:
    """Return V(x,t)=log prod_i (x_i-t_i)! for diagnostics."""
    return sum(lgamma(v + 1) for v in residual(x, target))


def increment_ratio(x: Sequence[int], target: Sequence[int], source: Sequence[int]) -> Fraction:
    """Exact exponential of the residual-potential increment.

    This equals prod_i (x_i-source_i)!/(x_i-target_i)! and also
    (x)_target/(x)_source.
    """
    if any(xi < si for xi, si in zip(x, source)):
        raise ValueError("source is not enabled")
    if any(xi < ti for xi, ti in zip(x, target)):
        raise ValueError("target is not present")
    num = propensity_factor(x, target)
    den = propensity_factor(x, source)
    if num <= 0 or den <= 0:
        raise AssertionError("enabled complexes must have positive factors")
    ratio = Fraction(num, den)
    # For small states, independently check the equivalent factorial ratio.
    # Large factorials are deliberately avoided in production calculations.
    if max(x, default=0) <= 100:
        factorial_ratio = Fraction(
            residual_factorial_integer(x, source),
            residual_factorial_integer(x, target),
        )
        if ratio != factorial_ratio:
            raise AssertionError("target/source factorial identity failed")
    return ratio


def fire_augmented(
    x: Sequence[int], carried_target: Sequence[int], reaction: Reaction
) -> tuple[State, Complex]:
    """Fire one reaction and return the new population and carried target."""
    residual(x, carried_target)  # validate the augmented state
    if not reaction.enabled(x):
        raise ValueError("reaction is not enabled")
    return reaction.fire(x), reaction.target


def aggregate_source_rates(reactions: Iterable[Reaction]) -> dict[Complex, Fraction]:
    out: dict[Complex, Fraction] = defaultdict(Fraction)
    for reaction in nontrivial_reactions(reactions):
        out[reaction.source] += reaction.rate
    return dict(out)


def source_probabilities(
    x: Sequence[int], reactions: Iterable[Reaction]
) -> dict[Complex, Fraction]:
    """Exact source probabilities in the embedded jump chain."""
    rates = aggregate_source_rates(reactions)
    weights: dict[Complex, Fraction] = {}
    for source, rate in rates.items():
        factor = propensity_factor(x, source)
        if factor:
            weights[source] = rate * factor
    total = sum(weights.values(), Fraction(0))
    if total <= 0:
        raise ValueError("state has no enabled nontrivial reaction")
    return {source: weight / total for source, weight in weights.items()}


def expected_increment(
    x: Sequence[int], carried_target: Sequence[int], reactions: Iterable[Reaction]
) -> float:
    """One embedded-jump expected increment of the residual potential."""
    probs = source_probabilities(x, reactions)
    target = tuple(carried_target)
    if target not in probs:
        raise ValueError("carried target has no enabled nontrivial outgoing reaction")
    return sum(float(p) * log(float(increment_ratio(x, target, s))) for s, p in probs.items())


def entropy_rate_constant(reactions: Iterable[Reaction]) -> float:
    """The state-independent C0 in d(x,t) <= log p_x(t)+C0."""
    rates = aggregate_source_rates(reactions)
    if not rates:
        raise ValueError("no nontrivial reactions")
    values = tuple(float(v) for v in rates.values())
    return log(len(rates)) + log(max(values) / min(values))


def entropy_identity_terms(
    x: Sequence[int], carried_target: Sequence[int], reactions: Iterable[Reaction]
) -> Mapping[str, float]:
    """Return both sides of the exact entropy/source-probability rewrite."""
    probs = source_probabilities(x, reactions)
    rates = aggregate_source_rates(reactions)
    t = tuple(carried_target)
    if t not in probs:
        raise ValueError("carried target not an enabled source")
    direct = expected_increment(x, t, reactions)
    entropy = -sum(float(p) * log(float(p)) for p in probs.values())
    rate_term = sum(float(p) * log(float(rates[s])) for s, p in probs.items())
    rewritten = log(float(probs[t])) + entropy + rate_term - log(float(rates[t]))
    return {
        "direct": direct,
        "rewritten": rewritten,
        "upper_bound": log(float(probs[t])) + entropy_rate_constant(reactions),
    }


def proper_sublevel_coordinate_bound(level: float) -> int:
    """Smallest B such that log(B!)>level; every V<=level has r_i<B."""
    if level < 0:
        return 0
    value = 0.0
    b = 1
    while value <= level:
        b += 1
        value += log(b)
    return b


def self_test() -> None:
    reactions = (
        Reaction((0, 0), (1, 1), Fraction(2)),
        Reaction((1, 1), (0, 1), Fraction(3)),
        Reaction((0, 1), (0, 0), Fraction(5)),
    )
    x = (9, 1)
    t = (1, 1)
    for source in ((0, 0), (1, 1), (0, 1)):
        ratio = increment_ratio(x, t, source)
        assert ratio > 0
    # Following the carried target has zero residual reward.
    assert increment_ratio(x, t, t) == 1
    terms = entropy_identity_terms(x, t, reactions)
    assert abs(terms["direct"] - terms["rewritten"]) < 1e-12
    assert terms["direct"] <= terms["upper_bound"] + 1e-12
    x2, t2 = fire_augmented(x, t, reactions[1])
    assert x2 == (8, 1) and t2 == (0, 1)
    assert residual(x2, t2) == residual(x, t)
    assert proper_sublevel_coordinate_bound(0.0) == 2


if __name__ == "__main__":
    self_test()
    print("target_source_residual.py self-test: OK")
