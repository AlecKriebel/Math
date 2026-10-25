from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial
from typing import Iterable, Sequence

Complex = tuple[int, ...]
State = tuple[int, ...]


def molecularity(y: Complex) -> int:
    return sum(y)


def falling_factorial(x: Sequence[int], y: Sequence[int]) -> int:
    if len(x) != len(y) or any(a < b or b < 0 for a, b in zip(x, y)):
        return 0
    out = 1
    for a, b in zip(x, y):
        out *= factorial(a) // factorial(a - b)
    return out


@dataclass(frozen=True, slots=True)
class Channel:
    source: Complex
    target: Complex
    rate: Fraction
    label: str = ""

    def __post_init__(self) -> None:
        if len(self.source) != len(self.target):
            raise ValueError("source and target dimensions differ")
        if self.rate <= 0:
            raise ValueError("rate must be positive")
        if any(v < 0 for v in self.source + self.target):
            raise ValueError("complex entries must be nonnegative")

    @property
    def displacement(self) -> Complex:
        return tuple(b - a for a, b in zip(self.source, self.target))


@dataclass(frozen=True)
class Network:
    species: tuple[str, ...]
    channels: tuple[Channel, ...]

    def __post_init__(self) -> None:
        d = len(self.species)
        if not self.channels:
            raise ValueError("at least one channel is required")
        if any(len(c.source) != d for c in self.channels):
            raise ValueError("channel dimension does not match species")

    @property
    def complexes(self) -> tuple[Complex, ...]:
        return tuple(sorted({c.source for c in self.channels} | {c.target for c in self.channels}))

    @property
    def is_binary(self) -> bool:
        return all(molecularity(y) <= 2 for y in self.complexes)

    def enabled_channels(self, x: State) -> tuple[Channel, ...]:
        return tuple(c for c in self.channels if c.source != c.target and falling_factorial(x, c.source) > 0)

    def propensity(self, x: State, channel: Channel) -> Fraction:
        return channel.rate * falling_factorial(x, channel.source)

    def total_rate(self, x: State) -> Fraction:
        return sum((self.propensity(x, c) for c in self.enabled_channels(x)), Fraction(0))

    def source_rate(self, x: State, source: Complex) -> Fraction:
        return sum((self.propensity(x, c) for c in self.enabled_channels(x) if c.source == source), Fraction(0))

    def successor(self, x: State, channel: Channel) -> State:
        if falling_factorial(x, channel.source) == 0:
            raise ValueError("channel is disabled")
        return tuple(a - b + c for a, b, c in zip(x, channel.source, channel.target))

    def combined_parallel(self) -> "Network":
        rates: dict[tuple[Complex, Complex], Fraction] = {}
        for channel in self.channels:
            if channel.source == channel.target:
                continue
            key = (channel.source, channel.target)
            rates[key] = rates.get(key, Fraction(0)) + channel.rate
        channels = tuple(
            Channel(s, t, r, f"{s}->{t}") for (s, t), r in sorted(rates.items())
        )
        return Network(self.species, channels)

    def strongly_connected(self) -> bool:
        vertices = set(self.complexes)
        adjacency = {v: set() for v in vertices}
        for c in self.channels:
            if c.source != c.target:
                adjacency[c.source].add(c.target)
        for start in vertices:
            seen = {start}
            stack = [start]
            while stack:
                current = stack.pop()
                for nxt in adjacency[current]:
                    if nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
            if seen != vertices:
                return False
        return True


def add(x: Sequence[int], y: Sequence[int]) -> State:
    return tuple(a + b for a, b in zip(x, y))


def subtract(x: Sequence[int], y: Sequence[int]) -> State:
    if any(a < b for a, b in zip(x, y)):
        raise ValueError("negative residual")
    return tuple(a - b for a, b in zip(x, y))
