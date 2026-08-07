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
    probs = source_probabilities(network, x)
    out: dict[int, Fraction] = {}
    for source, prob in probs.items():
        ratio = Fraction(falling_factorial(x, target), falling_factorial(x, source))
        add_weighted_signature(out, rational_log_signature(ratio), prob)
    return out
