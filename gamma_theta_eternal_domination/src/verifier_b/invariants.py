"""Exact elementary graph invariants for verifier B."""

from __future__ import annotations

from itertools import combinations
from typing import Iterable

from .graph import Graph


VertexSet = frozenset[int]


def is_dominating(graph: Graph, vertices: Iterable[int]) -> bool:
    chosen = _checked_vertex_set(graph, vertices)
    covered: set[int] = set(chosen)
    for vertex in chosen:
        covered.update(graph.adjacency[vertex])
    return len(covered) == graph.order


def minimum_dominating_set(graph: Graph) -> VertexSet:
    for cardinality in range(graph.order + 1):
        for candidate in combinations(graph.vertices, cardinality):
            if is_dominating(graph, candidate):
                return frozenset(candidate)
    raise AssertionError("the full vertex set must dominate")


def domination_number(graph: Graph) -> int:
    return len(minimum_dominating_set(graph))


def is_independent(graph: Graph, vertices: Iterable[int]) -> bool:
    chosen = _checked_vertex_set(graph, vertices)
    for vertex in chosen:
        if graph.adjacency[vertex].intersection(chosen):
            return False
    return True


def is_maximal_independent(graph: Graph, vertices: Iterable[int]) -> bool:
    chosen = _checked_vertex_set(graph, vertices)
    return is_independent(graph, chosen) and is_dominating(graph, chosen)


def minimum_independent_dominating_set(graph: Graph) -> VertexSet:
    for cardinality in range(graph.order + 1):
        for candidate in combinations(graph.vertices, cardinality):
            if is_maximal_independent(graph, candidate):
                return frozenset(candidate)
    raise AssertionError("at least one maximal independent set must exist")


def independent_domination_number(graph: Graph) -> int:
    return len(minimum_independent_dominating_set(graph))


def maximum_independent_set(graph: Graph) -> VertexSet:
    for cardinality in range(graph.order, -1, -1):
        for candidate in combinations(graph.vertices, cardinality):
            if is_independent(graph, candidate):
                return frozenset(candidate)
    raise AssertionError("the empty set must be independent")


def independence_number(graph: Graph) -> int:
    return len(maximum_independent_set(graph))


def maximal_independent_sets(graph: Graph) -> tuple[VertexSet, ...]:
    found: list[VertexSet] = []
    for cardinality in range(graph.order + 1):
        for candidate in combinations(graph.vertices, cardinality):
            if is_maximal_independent(graph, candidate):
                found.append(frozenset(candidate))
    return tuple(found)


def is_well_covered(graph: Graph) -> bool:
    sizes = {len(candidate) for candidate in maximal_independent_sets(graph)}
    return len(sizes) <= 1


def find_coloring(graph: Graph, color_count: int) -> tuple[int, ...] | None:
    """Return a proper coloring using at most ``color_count`` colors.

    This is a complete DSATUR-style backtracking search.  Color names are
    introduced consecutively, which removes only permutations of color names.
    """

    if not isinstance(color_count, int):
        raise TypeError("color_count must be an integer")
    if color_count < 0:
        return None
    if graph.order == 0:
        return ()
    if color_count == 0:
        return None

    assigned: dict[int, int] = {}

    def choose_uncolored_vertex() -> int:
        uncolored = (vertex for vertex in graph.vertices if vertex not in assigned)

        def priority(vertex: int) -> tuple[int, int, int]:
            neighbor_colors = {
                assigned[neighbor]
                for neighbor in graph.adjacency[vertex]
                if neighbor in assigned
            }
            return (len(neighbor_colors), graph.degree(vertex), -vertex)

        return max(uncolored, key=priority)

    def extend() -> bool:
        if len(assigned) == graph.order:
            return True

        vertex = choose_uncolored_vertex()
        forbidden = {
            assigned[neighbor]
            for neighbor in graph.adjacency[vertex]
            if neighbor in assigned
        }
        used_color_count = len(set(assigned.values()))
        available_name_count = min(color_count, used_color_count + 1)
        for color in range(available_name_count):
            if color in forbidden:
                continue
            assigned[vertex] = color
            if extend():
                return True
            del assigned[vertex]
        return False

    if not extend():
        return None
    return tuple(assigned[vertex] for vertex in graph.vertices)


def is_colorable(graph: Graph, color_count: int) -> bool:
    return find_coloring(graph, color_count) is not None


def chromatic_number(graph: Graph) -> int:
    if graph.order == 0:
        return 0
    for color_count in range(1, graph.order + 1):
        if find_coloring(graph, color_count) is not None:
            return color_count
    raise AssertionError("assigning one color per vertex must work")


def minimum_clique_partition(graph: Graph) -> tuple[VertexSet, ...]:
    if graph.order == 0:
        return ()
    complement_coloring = find_coloring(
        graph.complement(), clique_cover_number(graph)
    )
    if complement_coloring is None:
        raise AssertionError("clique cover coloring unexpectedly absent")
    parts: dict[int, set[int]] = {}
    for vertex, color in enumerate(complement_coloring):
        parts.setdefault(color, set()).add(vertex)
    return tuple(
        frozenset(parts[color])
        for color in sorted(parts)
    )


def clique_cover_number(graph: Graph) -> int:
    """Return θ(G), the chromatic number of the complement of ``graph``."""

    return chromatic_number(graph.complement())


def _checked_vertex_set(graph: Graph, vertices: Iterable[int]) -> VertexSet:
    chosen = frozenset(vertices)
    for vertex in chosen:
        if not isinstance(vertex, int):
            raise TypeError("vertex labels must be integers")
        if vertex < 0 or vertex >= graph.order:
            raise ValueError(f"vertex {vertex} is outside 0..{graph.order - 1}")
    return chosen
