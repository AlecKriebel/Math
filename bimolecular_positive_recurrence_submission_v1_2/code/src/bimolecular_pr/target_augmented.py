from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import factorial
from typing import Mapping, Sequence

from .network import Channel, Complex, Network, State, falling_factorial, subtract


def residual(x: State, target: Complex) -> State:
    return subtract(x, target)


def factorial_product(x: Sequence[int]) -> int:
    out = 1
    for value in x:
        out *= factorial(value)
    return out


def exp_potential_increment(x: State, carried_target: Complex, next_source: Complex) -> Fraction:
    """Exact exponential of the log-factorial potential increment."""
    numerator = falling_factorial(x, carried_target)
    denominator = falling_factorial(x, next_source)
    if numerator <= 0 or denominator <= 0:
        raise ValueError("both carried target and next source must be enabled")
    return Fraction(numerator, denominator)


def direct_exp_increment(x: State, carried_target: Complex, channel: Channel) -> Fraction:
    new_x = tuple(a - b + c for a, b, c in zip(x, channel.source, channel.target))
    old_residual = residual(x, carried_target)
    new_residual = residual(new_x, channel.target)
    return Fraction(factorial_product(new_residual), factorial_product(old_residual))


def marked_successor(x: State, channel: Channel) -> tuple[State, Complex]:
    return tuple(a - b + c for a, b, c in zip(x, channel.source, channel.target)), channel.target


def source_probabilities(network: Network, x: State) -> dict[Complex, Fraction]:
    total = network.total_rate(x)
    if total <= 0:
        return {}
    return {
        source: network.source_rate(x, source) / total
        for source in network.complexes
        if network.source_rate(x, source) > 0
    }


def prime_signature(value: int) -> dict[int, int]:
    if value <= 0:
        raise ValueError("signature requires a positive integer")
    out: dict[int, int] = defaultdict(int)
    p = 2
    n = value
    while p * p <= n:
        while n % p == 0:
            out[p] += 1
            n //= p
        p += 1
    if n > 1:
        out[n] += 1
    return dict(out)


def rational_log_signature(value: Fraction) -> dict[int, int]:
    out: dict[int, int] = defaultdict(int)
    for p, e in prime_signature(value.numerator).items():
        out[p] += e
    for p, e in prime_signature(value.denominator).items():
        out[p] -= e
    return {p: e for p, e in out.items() if e}


def add_weighted_signature(acc: dict[int, Fraction], signature: Mapping[int, int], weight: Fraction) -> None:
    for p, e in signature.items():
        acc[p] = acc.get(p, Fraction(0)) + weight * e
        if acc[p] == 0:
            del acc[p]


def expected_increment_signature(network: Network, x: State, target: Complex) -> dict[int, Fraction]:
    """Prime-exponent signature of the left side of the entropy identity."""
    probs = source_probabilities(network, x)
    if target not in probs:
        raise ValueError("the carried target must be an enabled source")
    out: dict[int, Fraction] = {}
    for source, prob in probs.items():
        ratio = Fraction(falling_factorial(x, target), falling_factorial(x, source))
        add_weighted_signature(out, rational_log_signature(ratio), prob)
    return out


def source_rate_constants(network: Network) -> dict[Complex, Fraction]:
    """Aggregate genuine-channel constants by source complex.

    Parallel channels are combined here exactly as in the manuscript's
    ``bar kappa`` notation.  Null self-channels do not participate in the
    embedded chain and are therefore excluded.
    """
    out: dict[Complex, Fraction] = {}
    for channel in network.channels:
        if channel.source == channel.target:
            continue
        out[channel.source] = out.get(channel.source, Fraction(0)) + channel.rate
    return out


def entropy_rewrite_signature(network: Network, x: State, target: Complex) -> dict[int, Fraction]:
    """Prime-exponent signature of the entropy-rewrite right side.

    This evaluates, without floating-point logarithms,

        log p(target) - sum_s p(s) log p(s)
        + sum_s p(s) log kappa_bar(s) - log kappa_bar(target).

    Equality with :func:`expected_increment_signature` is therefore an exact
    rational check of the manuscript's entropy identity.
    """
    probabilities = source_probabilities(network, x)
    if target not in probabilities:
        raise ValueError("the carried target must be an enabled source")
    rate_constants = source_rate_constants(network)
    out: dict[int, Fraction] = {}

    add_weighted_signature(
        out,
        rational_log_signature(probabilities[target]),
        Fraction(1),
    )
    for source, probability in probabilities.items():
        add_weighted_signature(
            out,
            rational_log_signature(probability),
            -probability,
        )
        add_weighted_signature(
            out,
            rational_log_signature(rate_constants[source]),
            probability,
        )
    add_weighted_signature(
        out,
        rational_log_signature(rate_constants[target]),
        Fraction(-1),
    )
    return out
