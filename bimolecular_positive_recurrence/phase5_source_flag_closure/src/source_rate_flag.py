#!/usr/bin/env python3
"""Finite normalized-log top alternative for bimolecular complex sets.

Given a set I of coordinates diverging along a subsequence and a nonzero
normalized logarithmic weight w supported on I, the routine certifies one of:

* all complexes have the same w-weight (exact conservation);
* a lower terminal complex c makes a strictly higher-weight source s enabled;
* an indicator or service-token conservation law rules out divergence.

The proof is purely combinatorial and uses only molecularity <=2.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations_with_replacement
from typing import Iterable, Sequence

Complex = tuple[int, ...]


@dataclass(frozen=True, slots=True)
class TopAlternative:
    kind: str
    top: tuple[Complex, ...]
    source: Complex | None = None
    terminal: Complex | None = None
    conservation: tuple[Fraction, ...] | None = None
    service_species: tuple[int, ...] = ()

    @property
    def is_available_pair(self) -> bool:
        return self.source is not None and self.terminal is not None


def dot(weight: Sequence[Fraction], y: Sequence[int]) -> Fraction:
    return sum((wi * yi for wi, yi in zip(weight, y)), Fraction(0))


def q_count(y: Sequence[int], indices: Iterable[int]) -> int:
    return sum(y[i] for i in indices)


def _constant_on_complexes(
    complexes: Sequence[Complex], vector: Sequence[Fraction]
) -> bool:
    vals = {dot(vector, y) for y in complexes}
    return len(vals) == 1


def top_availability_or_conservation(
    complexes: Sequence[Complex],
    divergent_species: Iterable[int],
    weight: Sequence[Fraction],
) -> TopAlternative:
    """Return the exact normalized-log alternative.

    `weight` must be nonnegative, zero outside `divergent_species`, and
    nonzero.  Coordinates in I are allowed to have zero normalized weight;
    this is what retains arbitrarily many nested population scales.
    """
    C = tuple(sorted(set(tuple(y) for y in complexes)))
    if not C:
        raise ValueError("empty complex set")
    d = len(C[0])
    if any(len(y) != d for y in C) or len(weight) != d:
        raise ValueError("dimension mismatch")
    if any(sum(y) > 2 or any(v < 0 for v in y) for y in C):
        raise ValueError("complex set is not bimolecular")
    I = frozenset(divergent_species)
    w = tuple(Fraction(v) for v in weight)
    if any(v < 0 for v in w) or not any(v > 0 for v in w):
        raise ValueError("weight must be nonnegative and nonzero")
    if any(w[i] != 0 for i in range(d) if i not in I):
        raise ValueError("weight must vanish outside I")

    values = {y: dot(w, y) for y in C}
    maximum = max(values.values())
    top = tuple(y for y in C if values[y] == maximum)
    lower = tuple(y for y in C if values[y] < maximum)

    if not lower:
        if not _constant_on_complexes(C, w):
            raise AssertionError("all-top conservation check failed")
        return TopAlternative("all_top_conservation", top, conservation=w)

    # A top binary source made entirely from divergent species remains
    # enabled at r+c for every terminal c.
    binary = tuple(y for y in top if q_count(y, I) == 2)
    if binary:
        return TopAlternative("binary_available", top, binary[0], lower[0])

    if maximum <= 0:
        raise AssertionError("a nonzero supported weight must have positive maximum")
    if any(q_count(y, I) != 1 for y in top):
        raise AssertionError("without a top q_I=2 complex, every top has q_I=1")

    K = tuple(sorted({i for y in top for i in I if y[i]}))
    if not K:
        raise AssertionError("positive top weight contains no divergent species")
    # Every K species has normalized weight a, and every complex containing
    # one K species is exactly top.  No complex contains two K species.
    for i in K:
        if w[i] != maximum:
            raise AssertionError("top K species has wrong weight")
    for y in C:
        qk = q_count(y, K)
        if qk > 1:
            raise AssertionError("two K particles would exceed the top weight")
        if (qk == 1) != (y in top):
            raise AssertionError("top set is not exactly q_K=1")

    q0 = tuple(y for y in C if q_count(y, K) == 0)
    if not q0:
        vector = tuple(Fraction(1 if i in K else 0) for i in range(d))
        if not _constant_on_complexes(C, vector):
            raise AssertionError("M_K conservation failed")
        return TopAlternative("top_indicator_conservation", top, conservation=vector)

    unary = tuple(y for y in top if sum(y) == 1)
    if unary:
        return TopAlternative("unary_available", top, unary[0], q0[0])

    service_to_sources: dict[int, list[Complex]] = {}
    for y in top:
        outside = [j for j in range(d) if j not in K and y[j]]
        if len(outside) != 1 or y[outside[0]] != 1:
            raise AssertionError("nonunary q_K=1 complex must be K_i+D")
        D = outside[0]
        # If D were another divergent species, q_I(y)=2, already excluded.
        if D in I:
            raise AssertionError("service species cannot be divergent in this branch")
        service_to_sources.setdefault(D, []).append(y)

    for c in q0:
        for D, sources in sorted(service_to_sources.items()):
            if c[D] > 0:
                return TopAlternative(
                    "service_available",
                    top,
                    sources[0],
                    c,
                    service_species=tuple(sorted(service_to_sources)),
                )

    service = tuple(sorted(service_to_sources))
    vector = tuple(
        Fraction(1 if i in K else (-1 if i in service else 0))
        for i in range(d)
    )
    if not _constant_on_complexes(C, vector):
        raise AssertionError("service-token conservation failed")
    return TopAlternative(
        "service_token_conservation",
        top,
        conservation=vector,
        service_species=service,
    )


def bimolecular_complexes(d: int) -> tuple[Complex, ...]:
    """All molecularity-at-most-two complexes in d species."""
    out: list[Complex] = [tuple(0 for _ in range(d))]
    for i in range(d):
        y = [0] * d
        y[i] = 1
        out.append(tuple(y))
    for i, j in combinations_with_replacement(range(d), 2):
        y = [0] * d
        y[i] += 1
        y[j] += 1
        out.append(tuple(y))
    return tuple(out)


def self_test() -> None:
    C = ((0, 0), (1, 1), (0, 1))
    cert = top_availability_or_conservation(C, {0}, (Fraction(1), Fraction(0)))
    assert cert.kind == "service_available"
    assert cert.source == (1, 1) and cert.terminal == (0, 1)

    paired = ((0, 0), (1, 1))
    cert2 = top_availability_or_conservation(
        paired, {0}, (Fraction(1), Fraction(0))
    )
    assert cert2.kind == "service_token_conservation"
    assert cert2.conservation == (Fraction(1), Fraction(-1))

    binary = ((1, 1), (1, 0), (0, 1))
    cert3 = top_availability_or_conservation(
        binary, {0, 1}, (Fraction(1), Fraction(1))
    )
    assert cert3.kind == "binary_available"

    all_top = ((1, 0), (0, 1), (1, 1))
    cert4 = top_availability_or_conservation(
        all_top, {0, 1}, (Fraction(1), Fraction(1))
    )
    # A+B has weight two, so this is binary availability, not all-top.
    assert cert4.kind == "binary_available"


if __name__ == "__main__":
    self_test()
    print("source_rate_flag.py self-test: OK")
