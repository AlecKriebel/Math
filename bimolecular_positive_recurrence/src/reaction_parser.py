#!/usr/bin/env python3
"""Deterministic parser/formatter for finite reaction networks.

Accepted syntax, one reaction per line::

    A + B -> 2 B ; 3/2
    0 -> A ; 1

Species names are supplied explicitly to avoid silent reordering.
"""
from __future__ import annotations

from fractions import Fraction
import re
from typing import Iterable, Sequence

from .generator import Complex, Reaction

_TERM = re.compile(r"^\s*(?:(\d+)\s*\*?\s*)?([A-Za-z_][A-Za-z0-9_]*)\s*$")


def parse_complex(text: str, species: Sequence[str]) -> Complex:
    text = text.strip()
    if text in {"", "0", "∅"}:
        return tuple(0 for _ in species)
    index = {name: i for i, name in enumerate(species)}
    out = [0] * len(species)
    for raw in text.split("+"):
        match = _TERM.match(raw)
        if not match:
            raise ValueError(f"cannot parse complex term: {raw!r}")
        coeff = int(match.group(1) or "1")
        name = match.group(2)
        if name not in index:
            raise ValueError(f"unknown species {name!r}")
        out[index[name]] += coeff
    return tuple(out)


def format_complex(y: Sequence[int], species: Sequence[str]) -> str:
    terms: list[str] = []
    for coeff, name in zip(y, species):
        if coeff == 1:
            terms.append(name)
        elif coeff:
            terms.append(f"{coeff}{name}")
    return " + ".join(terms) if terms else "0"


def parse_reaction(line: str, species: Sequence[str]) -> Reaction:
    content = line.split("#", 1)[0].strip()
    if not content:
        raise ValueError("blank/comment-only line")
    pieces = [piece.strip() for piece in content.split(";")]
    if len(pieces) not in {1, 2}:
        raise ValueError(f"expected at most one ';' in {line!r}")
    arrow = pieces[0]
    if "->" not in arrow:
        raise ValueError(f"missing '->' in {line!r}")
    lhs, rhs = [part.strip() for part in arrow.split("->", 1)]
    rate = Fraction(pieces[1]) if len(pieces) == 2 else Fraction(1)
    return Reaction(parse_complex(lhs, species), parse_complex(rhs, species), rate)


def parse_network(lines: Iterable[str], species: Sequence[str]) -> list[Reaction]:
    reactions: list[Reaction] = []
    for line in lines:
        if not line.split("#", 1)[0].strip():
            continue
        reactions.append(parse_reaction(line, species))
    return reactions


def validate_bimolecular(reactions: Iterable[Reaction]) -> None:
    for reaction in reactions:
        if sum(reaction.source) > 2 or sum(reaction.target) > 2:
            raise ValueError(f"non-bimolecular complex in {reaction}")


def self_test() -> None:
    species = ("A", "B")
    r = parse_reaction("A + B -> 2 B ; 3/2", species)
    assert r == Reaction((1, 1), (0, 2), Fraction(3, 2))
    assert parse_complex("0", species) == (0, 0)
    assert format_complex((2, 0), species) == "2A"
    validate_bimolecular([r])


if __name__ == "__main__":
    self_test()
    print("reaction_parser.py self-test: OK")
