#!/usr/bin/env python3
"""Verify gamma-infinity for the graph by the one-guard game definition."""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = HERE / "certificates" / "eternal_family.json"
Configuration = tuple[int, ...]


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    """Independently decode the small graph6 format into ordinary sets."""

    text = record.strip()
    if text.startswith(">>graph6<<"):
        text = text[len(">>graph6<<") :]
    if not text:
        raise ValueError("empty graph6 record")
    values = [ord(character) - 63 for character in text]
    if any(value < 0 or value > 63 for value in values):
        raise ValueError("invalid graph6 character")
    order = values[0]
    if order == 63:
        raise ValueError("only the small graph6 order format is accepted")
    slot_count = order * (order - 1) // 2
    if len(values) != 1 + (slot_count + 5) // 6:
        raise ValueError("graph6 payload has the wrong length")

    bits: list[int] = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if any(bits[slot_count:]):
        raise ValueError("graph6 padding bits are nonzero")

    neighborhoods = [set() for _ in range(order)]
    position = 0
    for upper in range(1, order):
        for lower in range(upper):
            if bits[position]:
                neighborhoods[lower].add(upper)
                neighborhoods[upper].add(lower)
            position += 1
    return tuple(frozenset(neighbors) for neighbors in neighborhoods)


def is_dominating(
    adjacency: tuple[frozenset[int], ...], configuration: Iterable[int]
) -> bool:
    chosen = frozenset(configuration)
    covered = set(chosen)
    for vertex in chosen:
        covered.update(adjacency[vertex])
    return len(covered) == len(adjacency)


def is_independent(
    adjacency: tuple[frozenset[int], ...], configuration: Iterable[int]
) -> bool:
    chosen = frozenset(configuration)
    return all(not (adjacency[vertex] & chosen) for vertex in chosen)


def dominating_configurations(
    adjacency: tuple[frozenset[int], ...], guard_count: int
) -> set[Configuration]:
    return {
        candidate
        for candidate in combinations(range(len(adjacency)), guard_count)
        if is_dominating(adjacency, candidate)
    }


def has_response(
    adjacency: tuple[frozenset[int], ...],
    family: set[Configuration],
    source: Configuration,
    attack: int,
) -> bool:
    occupied = set(source)
    for guard in source:
        if attack not in adjacency[guard]:
            continue
        successor = tuple(sorted((occupied - {guard}) | {attack}))
        if successor in family:
            return True
    return False


def greatest_closed_family(
    adjacency: tuple[frozenset[int], ...], guard_count: int
) -> set[Configuration]:
    """Compute the greatest fixed point of survivable configurations."""

    family = dominating_configurations(adjacency, guard_count)
    while family:
        doomed = {
            source
            for source in family
            if any(
                not has_response(adjacency, family, source, attack)
                for attack in range(len(adjacency))
                if attack not in source
            )
        }
        if not doomed:
            return family
        family -= doomed
    return set()


def independence_number(
    adjacency: tuple[frozenset[int], ...]
) -> tuple[int, Configuration]:
    order = len(adjacency)
    for cardinality in range(order, -1, -1):
        for candidate in combinations(range(order), cardinality):
            if is_independent(adjacency, candidate):
                return cardinality, candidate
    raise AssertionError("the empty set is independent")


def verify_certificate(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("format") != "one-guard-eternal-family-v1":
        raise ValueError("unknown eternal-family format")
    graph6 = data.get("graph6")
    guard_count = data.get("guard_count")
    raw_family = data.get("family")
    if not isinstance(graph6, str):
        raise ValueError("graph6 must be a string")
    if not isinstance(guard_count, int) or guard_count < 1:
        raise ValueError("guard_count must be a positive integer")
    if not isinstance(raw_family, list) or not raw_family:
        raise ValueError("eternal family must be a nonempty list")

    adjacency = decode_graph6(graph6)
    order = len(adjacency)
    family: set[Configuration] = set()
    for raw_configuration in raw_family:
        if (
            not isinstance(raw_configuration, list)
            or len(raw_configuration) != guard_count
            or any(not isinstance(vertex, int) for vertex in raw_configuration)
        ):
            raise ValueError("malformed guard configuration")
        configuration = tuple(sorted(raw_configuration))
        if len(set(configuration)) != guard_count:
            raise ValueError("a configuration repeats a vertex")
        if any(vertex < 0 or vertex >= order for vertex in configuration):
            raise ValueError("configuration contains an out-of-range vertex")
        if configuration in family:
            raise ValueError("duplicate guard configuration")
        if not is_dominating(adjacency, configuration):
            raise ValueError(f"configuration {configuration} is not dominating")
        family.add(configuration)

    attack_pairs = 0
    for source in sorted(family):
        for attack in range(order):
            if attack in source:
                continue
            attack_pairs += 1
            if not has_response(adjacency, family, source, attack):
                raise ValueError(
                    f"no legal closed-family response from {source} to {attack}"
                )

    alpha, independent_witness = independence_number(adjacency)
    if alpha != 3:
        raise ValueError("independence number is not three")
    fixed_point_sizes = {
        guards: len(greatest_closed_family(adjacency, guards))
        for guards in range(1, guard_count + 1)
    }
    if fixed_point_sizes[guard_count] == 0:
        raise ValueError("the proposed guard count is not eternal")
    if any(fixed_point_sizes[guards] for guards in range(1, guard_count)):
        raise ValueError("a smaller eternal guard family exists")
    full_fixed_point = greatest_closed_family(adjacency, guard_count)
    if family != full_fixed_point:
        raise ValueError("saved family is not the exact greatest fixed point")

    size = sum(len(neighbors) for neighbors in adjacency) // 2
    return {
        "graph6": graph6,
        "order": order,
        "size": size,
        "independence_number": alpha,
        "independent_witness": list(independent_witness),
        "guard_count": guard_count,
        "dominating_configurations": len(
            dominating_configurations(adjacency, guard_count)
        ),
        "greatest_closed_family_size": len(full_fixed_point),
        "verified_attack_pairs": attack_pairs,
        "fixed_point_sizes": fixed_point_sizes,
        "gamma_infinity_one_guard": guard_count,
    }


def load_and_verify(path: Path = DEFAULT_CERTIFICATE) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError("certificate root must be an object")
    return verify_certificate(data)


def main() -> None:
    print(json.dumps(load_and_verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
