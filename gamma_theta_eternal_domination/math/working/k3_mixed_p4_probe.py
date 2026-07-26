#!/usr/bin/env python3
"""Small-census probe for the mixed three-color P4 response pattern.

Input is a stream of graph6 records.  This exploratory probe keeps only graphs
with gamma=alpha=gamma_infinity=3 and searches the greatest literal one-guard
three-family for an independent reference state whose exact family-response
lists realize

    {a}, {a,c}, {b,c}, {b}

on an induced P4 in the complement.

The output is finite evidence, not a coverage certificate.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys

from verifier_a.core import (
    BitGraph,
    alpha,
    domination_number,
    eternal_fixed_point,
    theta,
)


def vertices(mask: int, order: int) -> tuple[int, ...]:
    return tuple(vertex for vertex in range(order) if mask & (1 << vertex))


def family_lists(
    graph: BitGraph, state: int, family: set[int]
) -> dict[int, frozenset[int]]:
    response_lists: dict[int, frozenset[int]] = {}
    for attacked in range(graph.n):
        if state & (1 << attacked):
            continue
        response_lists[attacked] = frozenset(
            guard
            for guard in vertices(state, graph.n)
            if graph.adj[attacked] & (1 << guard)
            and state ^ (1 << guard) ^ (1 << attacked) in family
        )
    return response_lists


def complement_edge(graph: BitGraph, left: int, right: int) -> bool:
    return not bool(graph.adj[left] & (1 << right))


def mixed_pattern(
    lists: dict[int, frozenset[int]], path: tuple[int, int, int, int]
) -> bool:
    x0, x1, x2, x3 = path
    left, left_middle = lists[x0], lists[x1]
    right_middle, right = lists[x2], lists[x3]
    common = left_middle & right_middle
    return (
        len(left) == 1
        and len(right) == 1
        and left != right
        and len(left_middle) == 2
        and len(right_middle) == 2
        and left < left_middle
        and right < right_middle
        and len(common) == 1
        and not (left & common)
        and not (right & common)
    )


def find_witness(graph: BitGraph, family: set[int]) -> dict[str, object] | None:
    independent_states = sorted(
        state for state in family if graph.is_independent(state)
    )
    for state in independent_states:
        lists = family_lists(graph, state, family)
        for path in itertools.permutations(lists, 4):
            x0, x1, x2, x3 = path
            if not (
                complement_edge(graph, x0, x1)
                and complement_edge(graph, x1, x2)
                and complement_edge(graph, x2, x3)
            ):
                continue
            if (
                complement_edge(graph, x0, x2)
                or complement_edge(graph, x0, x3)
                or complement_edge(graph, x1, x3)
            ):
                continue
            if mixed_pattern(lists, path):
                return {
                    "state": vertices(state, graph.n),
                    "path": path,
                    "lists": {
                        str(vertex): sorted(lists[vertex]) for vertex in path
                    },
                }
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local-model",
        action="store_true",
        help=(
            "enumerate seven-vertex partial-closure models instead of "
            "reading graph6 records"
        ),
    )
    parser.add_argument(
        "--stop-first",
        action="store_true",
        help="stop after printing the first realization",
    )
    arguments = parser.parse_args()
    if arguments.local_model:
        print(json.dumps(local_models(), indent=2, sort_keys=True))
        return 0

    graph_count = 0
    equality_count = 0
    witnesses: list[dict[str, object]] = []
    for raw_line in sys.stdin:
        record = raw_line.strip()
        if not record:
            continue
        graph_count += 1
        graph = BitGraph.from_graph6(record)
        if domination_number(graph) != 3 or alpha(graph) != 3:
            continue
        fixed_point = eternal_fixed_point(graph, 3)
        if not fixed_point.family:
            continue
        equality_count += 1
        witness = find_witness(graph, set(fixed_point.family))
        if witness is None:
            continue
        row = {
            "graph6": record,
            "order": graph.n,
            "theta": theta(graph),
            "greatest_family_size": len(fixed_point.family),
            **witness,
        }
        witnesses.append(row)
        if arguments.stop_first:
            break

    print(
        json.dumps(
            {
                "status": "FINITE_OBSERVATION",
                "graph_count": graph_count,
                "equality_graph_count": equality_count,
                "witness_count": len(witnesses),
                "witnesses": witnesses,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def local_fixed_point(
    graph: BitGraph, allowed: set[int], attacked_vertices: int
) -> set[int]:
    """Greatest closure subset when only the displayed attacks are required."""
    active = set(allowed)
    while True:
        doomed: set[int] = set()
        for state in active:
            unoccupied = attacked_vertices & ~state
            for attacked in vertices(unoccupied, graph.n):
                successors = {
                    state ^ (1 << guard) ^ (1 << attacked)
                    for guard in vertices(state & graph.adj[attacked], graph.n)
                }
                if not (successors & active):
                    doomed.add(state)
                    break
        if not doomed:
            return active
        active -= doomed


def graph_from_edges(
    order: int, edges: set[tuple[int, int]]
) -> BitGraph:
    adjacency = [0] * order
    for left, right in edges:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    return BitGraph(order, tuple(adjacency))


def local_models() -> dict[str, object]:
    """Search the exact named-vertex consequences of the mixed P4.

    Labels are a=0,b=1,c=2,x0=3,x1=4,x2=5,x3=6.  A surviving row is not
    a graph realization: it only proves that closure under attacks at these
    seven named vertices has no contradiction by itself.
    """
    a, b, c, x0, x1, x2, x3 = range(7)
    state = (1 << a) | (1 << b) | (1 << c)
    fixed_edges = {
        (a, x0),
        (a, x1),
        (c, x1),
        (b, x2),
        (c, x2),
        (b, x3),
        (x0, x2),
        (x0, x3),
        (x1, x3),
    }
    optional_edges = (
        (b, x0),
        (c, x0),
        (b, x1),
        (a, x2),
        (a, x3),
        (c, x3),
    )
    listed = {
        state ^ (1 << a) ^ (1 << x0),
        state ^ (1 << a) ^ (1 << x1),
        state ^ (1 << c) ^ (1 << x1),
        state ^ (1 << b) ^ (1 << x2),
        state ^ (1 << c) ^ (1 << x2),
        state ^ (1 << b) ^ (1 << x3),
    }
    forbidden = {
        state ^ (1 << b) ^ (1 << x0),
        state ^ (1 << c) ^ (1 << x0),
        state ^ (1 << b) ^ (1 << x1),
        state ^ (1 << a) ^ (1 << x2),
        state ^ (1 << a) ^ (1 << x3),
        state ^ (1 << c) ^ (1 << x3),
    }
    rows: list[dict[str, object]] = []
    masks_tested = 0
    for mask in range(1 << len(optional_edges)):
        edges = set(fixed_edges)
        for index, edge in enumerate(optional_edges):
            if mask & (1 << index):
                edges.add(edge)
        graph = graph_from_edges(7, edges)
        # x0 and x3 are shared vertices, and alpha(G)=3 is inherited by
        # every induced subgraph.
        if (not (graph.adj[x0] & ((1 << b) | (1 << c)))) or (
            not (graph.adj[x3] & ((1 << a) | (1 << c)))
        ):
            continue
        if alpha(graph) > 3:
            continue
        masks_tested += 1
        allowed = {
            candidate
            for candidate in range(1 << 7)
            if candidate.bit_count() == 3
            and candidate not in forbidden
            and graph.is_dominating(candidate)
        }
        family = local_fixed_point(graph, allowed, graph.full)
        if state not in family or not listed <= family:
            continue
        rows.append(
            {
                "optional_edge_mask": mask,
                "optional_edges": [
                    edge
                    for index, edge in enumerate(optional_edges)
                    if mask & (1 << index)
                ],
                "family_size": len(family),
                "family": [vertices(member, 7) for member in sorted(family)],
            }
        )
    return {
        "status": "FINITE_LOCAL_CONSISTENCY_OBSERVATION",
        "models": rows,
        "models_found": len(rows),
        "masks_tested_after_inherited_filters": masks_tested,
        "warning": (
            "A surviving partial model need not extend to an eternal "
            "equality graph; absence would be a named-vertex contradiction."
        ),
    }


if __name__ == "__main__":
    raise SystemExit(main())
