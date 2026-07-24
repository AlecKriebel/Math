#!/usr/bin/env python3
"""Compact residual CNF for one exact branch-18 catalog cube.

Vertex 0 is fixed adjacent to A={1,...,18} and nonadjacent to
B={19,...,42}.  The graph induced by B is fixed to the complement of a
catalog graph J in R(4,5,24).  The only primary variables left are:

* the 153 edges inside A; and
* the 432 edges between A and B.

Ramsey clauses are simplified under the fixed assignment and satisfied
clauses are omitted.  Compact forward counters enforce the global degree
interval [18,24] using only the remaining incidences.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Iterator, Mapping, Sequence

from direct_ramsey_cnf import (
    SequentialCounter,
    allocate_sequential_counter,
    canonical_counter_extension,
)


ORDER = 43
A = tuple(range(1, 19))
B = tuple(range(19, 43))
PRIMARY_COUNT = math.comb(len(A), 2) + len(A) * len(B)
DEGREE_LOWER = 18
DEGREE_UPPER = 24
SCHEMA = "ramsey55.branch18_residual_cnf.v1"


def decode_graph6_order24(record: str | bytes) -> list[int]:
    raw = record.encode("ascii") if isinstance(record, str) else record
    raw = raw.rstrip(b"\r\n")
    if len(raw) != 47 or raw[0] != 63 + 24:
        raise ValueError("expected one short-header order-24 graph6 record")
    bits: list[int] = []
    for character in raw[1:]:
        value = character - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [0] * 24
    offset = 0
    for right in range(1, 24):
        for left in range(right):
            if bits[offset]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            offset += 1
    if offset != math.comb(24, 2):
        raise AssertionError("graph6 bit count mismatch")
    return adjacency


def forbidden_counts(adjacency: Sequence[int], clique: int, independent: int) -> tuple[int, int]:
    clique_count = 0
    independent_count = 0
    for vertices in itertools.combinations(range(len(adjacency)), clique):
        clique_count += all(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
    for vertices in itertools.combinations(range(len(adjacency)), independent):
        independent_count += all(
            not ((adjacency[left] >> right) & 1)
            for left, right in itertools.combinations(vertices, 2)
        )
    return clique_count, independent_count


def validate_catalog_side(catalog_adjacency: Sequence[int]) -> None:
    if len(catalog_adjacency) != 24:
        raise ValueError("catalog side does not have order 24")
    clique4, independent5 = forbidden_counts(catalog_adjacency, 4, 5)
    if clique4 or independent5:
        raise ValueError(
            "catalog side is not in R(4,5,24): "
            f"K4={clique4}, I5={independent5}"
        )


def unknown_pairs() -> tuple[tuple[int, int], ...]:
    return tuple(itertools.combinations(A, 2)) + tuple(
        (left, right) for left in A for right in B
    )


def fixed_edge_value(
    left: int, right: int, catalog_adjacency: Sequence[int]
) -> bool | None:
    if left > right:
        left, right = right, left
    if left == 0:
        return right in A
    if left in B and right in B:
        # The actual antineighbourhood graph is complement(J).
        return not bool(
            (catalog_adjacency[left - B[0]] >> (right - B[0])) & 1
        )
    return None


def _simplified_ramsey_clauses(
    catalog_adjacency: Sequence[int],
    pair_to_variable: Mapping[tuple[int, int], int],
) -> tuple[tuple[int, ...], ...]:
    clauses: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(ORDER), 5):
        pairs = tuple(itertools.combinations(vertices, 2))
        for positive in (False, True):
            residual: list[int] = []
            satisfied = False
            for pair in pairs:
                fixed = fixed_edge_value(*pair, catalog_adjacency)
                if fixed is None:
                    variable = pair_to_variable[pair]
                    residual.append(variable if positive else -variable)
                    continue
                literal_true = fixed if positive else not fixed
                if literal_true:
                    satisfied = True
                    break
            if satisfied:
                continue
            clause = tuple(residual)
            if not clause:
                raise ValueError(
                    "fixed root/catalog assignment already violates Ramsey(5,5)"
                )
            if clause not in seen:
                seen.add(clause)
                clauses.append(clause)
    return tuple(clauses)


@dataclass(frozen=True)
class Branch18Residual:
    catalog_graph6: str
    catalog_edge_count: int
    catalog_degree_sequence: tuple[int, ...]
    pairs: tuple[tuple[int, int], ...]
    ramsey_clauses: tuple[tuple[int, ...], ...]
    counters: tuple[SequentialCounter, ...]
    variable_count: int

    @property
    def primary_variable_count(self) -> int:
        return len(self.pairs)

    @property
    def auxiliary_variable_count(self) -> int:
        return self.variable_count - self.primary_variable_count

    @property
    def degree_clause_count(self) -> int:
        return sum(counter.clause_count for counter in self.counters)

    @property
    def clause_count(self) -> int:
        return len(self.ramsey_clauses) + self.degree_clause_count

    def clauses(self) -> Iterator[tuple[int, ...]]:
        yield from self.ramsey_clauses
        for counter in self.counters:
            yield from counter.clauses()

    def pair_to_variable(self) -> dict[tuple[int, int], int]:
        return {
            pair: variable for variable, pair in enumerate(self.pairs, start=1)
        }

    def primary_adjacency(
        self, assignment: Mapping[int, bool]
    ) -> list[int]:
        catalog = decode_graph6_order24(self.catalog_graph6)
        adjacency = [0] * ORDER
        pair_to_variable = self.pair_to_variable()
        for left, right in itertools.combinations(range(ORDER), 2):
            fixed = fixed_edge_value(left, right, catalog)
            edge = (
                fixed
                if fixed is not None
                else assignment.get(pair_to_variable[(left, right)], False)
            )
            if edge:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
        return adjacency

    def canonical_extension(
        self, primary_assignment: Mapping[int, bool]
    ) -> dict[int, bool]:
        result = dict(primary_assignment)
        for counter in self.counters:
            result.update(canonical_counter_extension(counter, result))
        return result


def build_residual(catalog_graph6: str | bytes) -> Branch18Residual:
    raw = (
        catalog_graph6.decode("ascii")
        if isinstance(catalog_graph6, bytes)
        else catalog_graph6
    ).strip()
    catalog = decode_graph6_order24(raw)
    validate_catalog_side(catalog)
    pairs = unknown_pairs()
    if len(pairs) != PRIMARY_COUNT or len(set(pairs)) != PRIMARY_COUNT:
        raise AssertionError("unexpected primary-pair layout")
    pair_to_variable = {
        pair: variable for variable, pair in enumerate(pairs, start=1)
    }
    ramsey_clauses = _simplified_ramsey_clauses(
        catalog, pair_to_variable
    )

    counters: list[SequentialCounter] = []
    next_variable = PRIMARY_COUNT + 1
    for vertex in A:
        incident = tuple(
            pair_to_variable[tuple(sorted((vertex, other)))]
            for other in (*A, *B)
            if other != vertex
        )
        if len(incident) != 41:
            raise AssertionError("A incidence count mismatch")
        upper, next_variable = allocate_sequential_counter(
            incident,
            23,
            next_variable,
            f"A_{vertex}_remaining_edges_at_most_23",
        )
        counters.append(upper)
        lower, next_variable = allocate_sequential_counter(
            tuple(-literal for literal in incident),
            24,
            next_variable,
            f"A_{vertex}_remaining_nonedges_at_most_24",
        )
        counters.append(lower)

    catalog_degrees = tuple(neighbors.bit_count() for neighbors in catalog)
    for offset, vertex in enumerate(B):
        cross = tuple(
            pair_to_variable[(left, vertex)]
            for left in A
        )
        fixed_degree = 23 - catalog_degrees[offset]
        lower_degree = max(0, DEGREE_LOWER - fixed_degree)
        upper_degree = min(len(cross), DEGREE_UPPER - fixed_degree)
        if lower_degree > upper_degree:
            raise ValueError("catalog vertex cannot meet global degree bounds")
        upper, next_variable = allocate_sequential_counter(
            cross,
            upper_degree,
            next_variable,
            f"B_{vertex}_cross_edges_at_most_{upper_degree}",
        )
        counters.append(upper)
        nonedge_upper = len(cross) - lower_degree
        lower, next_variable = allocate_sequential_counter(
            tuple(-literal for literal in cross),
            nonedge_upper,
            next_variable,
            f"B_{vertex}_cross_nonedges_at_most_{nonedge_upper}",
        )
        counters.append(lower)

    return Branch18Residual(
        catalog_graph6=raw,
        catalog_edge_count=sum(catalog_degrees) // 2,
        catalog_degree_sequence=tuple(sorted(catalog_degrees)),
        pairs=pairs,
        ramsey_clauses=ramsey_clauses,
        counters=tuple(counters),
        variable_count=next_variable - 1,
    )
