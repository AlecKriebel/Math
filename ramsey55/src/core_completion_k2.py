#!/usr/bin/env python3
"""Independent helpers for delete-two/add-three fixed-core completions."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterable, Sequence

from graph_io import validate_simple


ADDED_VERTEX_COUNT = 3
FORBIDDEN_SIZE = 5


@dataclass(frozen=True)
class K2CompletionInstance:
    core_vertex_count: int
    clauses: tuple[tuple[int, ...], ...]
    clique_counts_by_new_count: tuple[int, int, int]
    independent_counts_by_new_count: tuple[int, int, int]

    @property
    def variable_count(self) -> int:
        return (
            ADDED_VERTEX_COUNT * self.core_vertex_count
            + ADDED_VERTEX_COUNT * (ADDED_VERTEX_COUNT - 1) // 2
        )


def induced_core_two(
    adjacency: list[int], deleted_left: int, deleted_right: int
) -> tuple[list[int], tuple[int, ...]]:
    validate_simple(adjacency)
    if not 0 <= deleted_left < deleted_right < len(adjacency):
        raise ValueError("deleted labels must satisfy 0 <= left < right < n")
    original_vertices = tuple(
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (deleted_left, deleted_right)
    )
    core = [0] * len(original_vertices)
    for new_left, old_left in enumerate(original_vertices):
        for new_right in range(new_left + 1, len(original_vertices)):
            old_right = original_vertices[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                core[new_left] |= 1 << new_right
                core[new_right] |= 1 << new_left
    validate_simple(core)
    return core, original_vertices


def variable_for_unknown_edge(
    core_count: int, left: int, right: int
) -> int:
    """Return a one-based variable in the documented C++ order."""
    if left > right:
        left, right = right, left
    if 0 <= left < core_count and core_count <= right < core_count + 3:
        added = right - core_count
        return added * core_count + left + 1
    added_pairs = ((0, 1), (0, 2), (1, 2))
    if left >= core_count:
        pair = (left - core_count, right - core_count)
        if pair in added_pairs:
            return 3 * core_count + added_pairs.index(pair) + 1
    raise ValueError(f"edge ({left},{right}) is fixed or outside the instance")


def _unknown_variables(
    core_count: int, vertices: Sequence[int]
) -> tuple[int, ...]:
    return tuple(
        variable_for_unknown_edge(core_count, left, right)
        for left, right in itertools.combinations(vertices, 2)
        if right >= core_count
    )


def _fixed_flags(
    core: Sequence[int], core_vertices: Sequence[int]
) -> tuple[bool, bool]:
    all_edges = True
    all_nonedges = True
    for left, right in itertools.combinations(core_vertices, 2):
        if (core[left] >> right) & 1:
            all_nonedges = False
        else:
            all_edges = False
    return all_edges, all_nonedges


def build_k2_completion_instance(core: list[int]) -> K2CompletionInstance:
    validate_simple(core)
    core_count = len(core)
    added = tuple(range(core_count, core_count + 3))
    clique_by_count: list[list[tuple[int, ...]]] = [
        [] for _ in range(4)
    ]
    independent_by_count: list[list[tuple[int, ...]]] = [
        [] for _ in range(4)
    ]
    for new_count in (1, 2, 3):
        for selected_new in itertools.combinations(added, new_count):
            for selected_core in itertools.combinations(
                range(core_count), FORBIDDEN_SIZE - new_count
            ):
                all_edges, all_nonedges = _fixed_flags(
                    core, selected_core
                )
                variables = _unknown_variables(
                    core_count, selected_core + selected_new
                )
                if all_edges:
                    clique_by_count[new_count].append(
                        tuple(-variable for variable in variables)
                    )
                if all_nonedges:
                    independent_by_count[new_count].append(variables)
    clauses = tuple(
        clause
        for new_count in (1, 2, 3)
        for clause in (
            clique_by_count[new_count]
            + independent_by_count[new_count]
        )
    )
    return K2CompletionInstance(
        core_vertex_count=core_count,
        clauses=clauses,
        clique_counts_by_new_count=tuple(
            len(clique_by_count[count]) for count in (1, 2, 3)
        ),
        independent_counts_by_new_count=tuple(
            len(independent_by_count[count]) for count in (1, 2, 3)
        ),
    )


def clause_is_satisfied(
    clause: Sequence[int], assignment: Sequence[bool]
) -> bool:
    return any(
        assignment[abs(literal) - 1] == (literal > 0)
        for literal in clause
    )


def formula_is_satisfied(
    clauses: Iterable[Sequence[int]], assignment: Sequence[bool]
) -> bool:
    return all(clause_is_satisfied(clause, assignment) for clause in clauses)


def completed_adjacency_k2(
    core: list[int], assignment: Sequence[bool]
) -> list[int]:
    validate_simple(core)
    core_count = len(core)
    expected = 3 * core_count + 3
    if len(assignment) != expected:
        raise ValueError(f"expected {expected} assignment values")
    result = core.copy() + [0, 0, 0]
    for core_vertex in range(core_count):
        for added_vertex in range(core_count, core_count + 3):
            variable = variable_for_unknown_edge(
                core_count, core_vertex, added_vertex
            )
            if assignment[variable - 1]:
                result[core_vertex] |= 1 << added_vertex
                result[added_vertex] |= 1 << core_vertex
    for left, right in itertools.combinations(
        range(core_count, core_count + 3), 2
    ):
        variable = variable_for_unknown_edge(core_count, left, right)
        if assignment[variable - 1]:
            result[left] |= 1 << right
            result[right] |= 1 << left
    validate_simple(result)
    return result
