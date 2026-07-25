"""Exact one-guard eternal domination via an explicit colored digraph.

Each vertex of the configuration digraph is a dominating k-subset.  An arc
records its source, the attacked (unoccupied) vertex that colors the arc, the
single guard that traverses an edge, and the resulting dominating target.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable

from .graph import Graph
from .invariants import domination_number, is_dominating


Configuration = frozenset[int]


def _configuration_key(configuration: Configuration) -> tuple[int, ...]:
    return tuple(sorted(configuration))


@dataclass(frozen=True, slots=True)
class Move:
    source: Configuration
    attack: int
    guard: int
    target: Configuration


@dataclass(slots=True)
class ColoredConfigurationDigraph:
    graph: Graph
    guard_count: int
    configurations: tuple[Configuration, ...]
    outgoing: dict[Configuration, dict[int, tuple[Move, ...]]]

    def attacks_from(self, source: Configuration) -> tuple[int, ...]:
        return tuple(sorted(self.outgoing[source]))

    def moves(self, source: Configuration, attack: int) -> tuple[Move, ...]:
        return self.outgoing[source].get(attack, ())


@dataclass(frozen=True, slots=True)
class EternalCertificate:
    guard_count: int
    family: frozenset[Configuration]
    responses: tuple[Move, ...]


def build_colored_configuration_digraph(
    graph: Graph, guard_count: int
) -> ColoredConfigurationDigraph:
    """Build all legal one-guard arcs between dominating configurations."""

    if not isinstance(guard_count, int):
        raise TypeError("guard_count must be an integer")
    if guard_count < 0 or guard_count > graph.order:
        return ColoredConfigurationDigraph(graph, guard_count, (), {})

    configurations = tuple(
        frozenset(candidate)
        for candidate in combinations(graph.vertices, guard_count)
        if is_dominating(graph, candidate)
    )
    configuration_set = set(configurations)
    outgoing: dict[Configuration, dict[int, tuple[Move, ...]]] = {}

    for source in configurations:
        by_attack: dict[int, tuple[Move, ...]] = {}
        for attack in graph.vertices:
            if attack in source:
                continue
            legal_moves: list[Move] = []
            for guard in sorted(source):
                if attack not in graph.adjacency[guard]:
                    continue
                target = frozenset((source - {guard}) | {attack})
                if target in configuration_set:
                    legal_moves.append(Move(source, attack, guard, target))
            by_attack[attack] = tuple(legal_moves)
        outgoing[source] = by_attack

    return ColoredConfigurationDigraph(
        graph=graph,
        guard_count=guard_count,
        configurations=configurations,
        outgoing=outgoing,
    )


def greatest_closed_family(
    digraph: ColoredConfigurationDigraph,
) -> frozenset[Configuration]:
    """Return the greatest family closed against every attack color."""

    surviving = set(digraph.configurations)
    while surviving:
        doomed: set[Configuration] = set()
        for source in sorted(surviving, key=_configuration_key):
            for moves in digraph.outgoing[source].values():
                if not any(move.target in surviving for move in moves):
                    doomed.add(source)
                    break
        if not doomed:
            return frozenset(surviving)
        surviving.difference_update(doomed)
    return frozenset()


def find_eternal_family(
    graph: Graph, guard_count: int
) -> frozenset[Configuration] | None:
    digraph = build_colored_configuration_digraph(graph, guard_count)
    family = greatest_closed_family(digraph)
    return family if family else None


def eternal_domination_decision(graph: Graph, guard_count: int) -> bool:
    """Decide whether an eternal dominating family of this size exists."""

    if not isinstance(guard_count, int):
        raise TypeError("guard_count must be an integer")
    if guard_count < 0 or guard_count > graph.order:
        return False
    if graph.order == 0:
        return guard_count == 0
    if guard_count == 0:
        return False
    return find_eternal_family(graph, guard_count) is not None


def eternal_domination_number(graph: Graph) -> int:
    """Return the one-guard-moves eternal domination number γ∞(G)."""

    if graph.order == 0:
        return 0
    for guard_count in range(domination_number(graph), graph.order + 1):
        if eternal_domination_decision(graph, guard_count):
            return guard_count
    raise AssertionError("the full vertex set is an eternal family")


def make_eternal_certificate(
    graph: Graph, guard_count: int
) -> EternalCertificate | None:
    digraph = build_colored_configuration_digraph(graph, guard_count)
    family = greatest_closed_family(digraph)
    if not family:
        return None

    responses: list[Move] = []
    for source in sorted(family, key=_configuration_key):
        for attack in sorted(digraph.outgoing[source]):
            legal = tuple(
                move
                for move in digraph.outgoing[source][attack]
                if move.target in family
            )
            if not legal:
                raise AssertionError("greatest closed family has a missing response")
            responses.append(legal[0])
    return EternalCertificate(guard_count, family, tuple(responses))


def verify_eternal_family(
    graph: Graph, guard_count: int, family: Iterable[Iterable[int]]
) -> bool:
    """Check a proposed family directly from the definition.

    This checker intentionally rebuilds no configuration digraph.
    """

    if not isinstance(guard_count, int):
        return False
    if guard_count < 0 or guard_count > graph.order:
        return False
    normalized = frozenset(frozenset(configuration) for configuration in family)
    if not normalized:
        return False

    for source in normalized:
        if len(source) != guard_count:
            return False
        if any(
            not isinstance(vertex, int)
            or vertex < 0
            or vertex >= graph.order
            for vertex in source
        ):
            return False
        if not is_dominating(graph, source):
            return False

        for attack in graph.vertices:
            if attack in source:
                continue
            has_response = False
            for guard in source:
                if attack not in graph.adjacency[guard]:
                    continue
                target = frozenset((source - {guard}) | {attack})
                if target in normalized:
                    has_response = True
                    break
            if not has_response:
                return False
    return True


def verify_eternal_certificate(
    graph: Graph, certificate: EternalCertificate
) -> bool:
    """Check all explicit response records without trusting the search."""

    if not verify_eternal_family(
        graph, certificate.guard_count, certificate.family
    ):
        return False

    expected_pairs = {
        (source, attack)
        for source in certificate.family
        for attack in graph.vertices
        if attack not in source
    }
    recorded_pairs: set[tuple[Configuration, int]] = set()

    for move in certificate.responses:
        pair = (move.source, move.attack)
        if pair in recorded_pairs or pair not in expected_pairs:
            return False
        recorded_pairs.add(pair)
        if move.guard not in move.source:
            return False
        if move.attack in move.source:
            return False
        if move.attack not in graph.adjacency[move.guard]:
            return False
        expected_target = frozenset(
            (move.source - {move.guard}) | {move.attack}
        )
        if move.target != expected_target:
            return False
        if move.target not in certificate.family:
            return False
        if not is_dominating(graph, move.target):
            return False

    return recorded_pairs == expected_pairs
