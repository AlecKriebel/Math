#!/usr/bin/env python3
"""Minimal parser for indexed classical mass-action reaction networks."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

import sympy as sp


@dataclass(frozen=True)
class Reaction:
    source: tuple[int, ...]
    target: tuple[int, ...]

    @property
    def change(self) -> tuple[int, ...]:
        return tuple(t - s for s, t in zip(self.source, self.target))


@dataclass(frozen=True)
class Network:
    species: tuple[str, ...]
    reactions: tuple[Reaction, ...]

    @property
    def n(self) -> int:
        return len(self.species)

    @property
    def m(self) -> int:
        return len(self.reactions)

    def source_matrix(self) -> sp.Matrix:
        return sp.Matrix(self.n, self.m, lambda i, r: self.reactions[r].source[i])

    def stoichiometric_matrix(self) -> sp.Matrix:
        return sp.Matrix(self.n, self.m, lambda i, r: self.reactions[r].change[i])


def _nonnegative_integer_vector(value: Any, n: int, label: str) -> tuple[int, ...]:
    if not isinstance(value, list) or len(value) != n:
        raise ValueError(f"{label} must be a length-{n} list")
    result: list[int] = []
    for item in value:
        if isinstance(item, bool) or not isinstance(item, int) or item < 0:
            raise ValueError(f"{label} must contain nonnegative integers")
        result.append(item)
    return tuple(result)


def parse_network(data: dict[str, Any]) -> Network:
    raw_species = data.get("species")
    if not isinstance(raw_species, list) or not raw_species or any(not isinstance(x, str) for x in raw_species):
        raise ValueError("species must be a nonempty list of names")
    if len(set(raw_species)) != len(raw_species):
        raise ValueError("species names must be distinct")
    n = len(raw_species)
    raw_reactions = data.get("reactions")
    if not isinstance(raw_reactions, list):
        raise ValueError("reactions must be a list")
    reactions: list[Reaction] = []
    for index, raw in enumerate(raw_reactions):
        if not isinstance(raw, dict):
            raise ValueError(f"reaction {index} must be an object")
        source = _nonnegative_integer_vector(raw.get("source"), n, f"reaction {index} source")
        target = _nonnegative_integer_vector(raw.get("target"), n, f"reaction {index} target")
        if source == target:
            raise ValueError(f"reaction {index} has identical source and target")
        reactions.append(Reaction(source, target))
    return Network(tuple(raw_species), tuple(reactions))
