#!/usr/bin/env python3
"""Exact stochastic mass-action generator utilities.

All arithmetic is compatible with fractions.Fraction and integers.  The
falling-factorial convention is exactly the convention in the theorem.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial, log
from typing import Callable, Iterable, Sequence, TypeVar

Number = TypeVar("Number")
State = tuple[int, ...]
Complex = tuple[int, ...]


def falling(n: int, m: int) -> int:
    """Return the falling factorial (n)_m, with zero for n<m."""
    if n < 0 or m < 0:
        raise ValueError("n and m must be nonnegative")
    if n < m:
        return 0
    out = 1
    for j in range(m):
        out *= n - j
    return out


def propensity_factor(x: Sequence[int], y: Sequence[int]) -> int:
    """Return (x)_y exactly."""
    if len(x) != len(y):
        raise ValueError("dimension mismatch")
    out = 1
    for xi, yi in zip(x, y):
        out *= falling(int(xi), int(yi))
        if out == 0:
            break
    return out


@dataclass(frozen=True, slots=True)
class Reaction:
    source: Complex
    target: Complex
    rate: Fraction = Fraction(1)

    def __post_init__(self) -> None:
        if len(self.source) != len(self.target):
            raise ValueError("source and target dimensions differ")
        if any(v < 0 for v in self.source + self.target):
            raise ValueError("complex coordinates must be nonnegative")
        if self.rate <= 0:
            raise ValueError("rate constants must be positive")

    @property
    def dimension(self) -> int:
        return len(self.source)

    @property
    def vector(self) -> tuple[int, ...]:
        return tuple(b - a for a, b in zip(self.source, self.target))

    @property
    def source_molecularity(self) -> int:
        return sum(self.source)

    @property
    def target_molecularity(self) -> int:
        return sum(self.target)

    @property
    def delta_molecularity(self) -> int:
        return self.target_molecularity - self.source_molecularity

    def enabled(self, x: Sequence[int]) -> bool:
        return all(xi >= yi for xi, yi in zip(x, self.source))

    def propensity(self, x: Sequence[int]) -> Fraction:
        return self.rate * propensity_factor(x, self.source)

    def fire(self, x: Sequence[int]) -> State:
        if not self.enabled(x):
            raise ValueError("reaction is not enabled")
        return tuple(xi + zi for xi, zi in zip(x, self.vector))


def generator_value(
    x: State,
    reactions: Iterable[Reaction],
    f: Callable[[State], Number],
):
    """Compute Lf(x) exactly when f has exact-valued output."""
    fx = f(x)
    total = 0
    for reaction in reactions:
        a = reaction.propensity(x)
        if a:
            total += a * (f(reaction.fire(x)) - fx)
    return total


def total_count(x: Sequence[int]) -> int:
    return sum(x)


def factorial_weight(x: Sequence[int]) -> Fraction:
    """The unnormalised Poisson(1)^d weight 1/prod_i x_i!."""
    denom = 1
    for xi in x:
        denom *= factorial(xi)
    return Fraction(1, denom)


def entropy_real(x: Sequence[int]) -> float:
    """Exploratory entropy sum_i[x_i log x_i-x_i+1].

    This floating-point helper is not used in any certificate.
    """
    return sum((xi * log(xi) - xi + 1.0) if xi else 1.0 for xi in x)


def self_test() -> None:
    assert falling(5, 0) == 1
    assert falling(5, 2) == 20
    assert falling(1, 2) == 0
    r = Reaction((1,), (2,), Fraction(3, 2))
    assert r.vector == (1,)
    assert r.propensity((4,)) == 6
    assert r.fire((4,)) == (5,)
    assert generator_value((4,), [r], total_count) == 6
    assert factorial_weight((2, 3)) == Fraction(1, 12)


if __name__ == "__main__":
    self_test()
    print("generator.py self-test: OK")
