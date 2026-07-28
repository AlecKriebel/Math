#!/usr/bin/env python3
"""Finite truth-table audit of the static-gate SAT/CEGAR encoding.

For every labeled graph on four vertices, this script fixes every edge
variable in the SAT base formula and compares satisfiability with a separate
direct test of the mathematical conditions (including the fixed triangle).
For every satisfiable graph, it also verifies that the CEGAR clause generated
from one exact three-coloring excludes that exact graph.

This small audit is not a coverage proof at order seven.  Its role is to catch
polarity, complement, conditional-link-color, and coloring-cut mistakes in the
discovery encoding.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from search_static_gate import build_base, edge_key, exact_coloring, solve


def direct_base(order: int, edge_set: set[tuple[int, int]]) -> bool:
    def has(u: int, v: int) -> bool:
        return edge_key(u, v) in edge_set

    if not all(has(u, v) for u, v in ((0, 1), (0, 2), (1, 2))):
        return False
    for four in itertools.combinations(range(order), 4):
        if all(has(u, v) for u, v in itertools.combinations(four, 2)):
            return False
    for u, v in itertools.combinations(range(order), 2):
        if not any(
            has(u, w) and has(v, w)
            for w in range(order)
            if w not in (u, v)
        ):
            return False
    for root in range(order):
        neighbors = {v for v in range(order) if v != root and has(root, v)}
        colors: dict[int, int] = {}
        for start in neighbors:
            if start in colors:
                continue
            colors[start] = 0
            stack = [start]
            while stack:
                vertex = stack.pop()
                for neighbor in neighbors:
                    if neighbor == vertex:
                        continue
                    if not has(vertex, neighbor):
                        continue
                    if neighbor not in colors:
                        colors[neighbor] = 1 - colors[vertex]
                        stack.append(neighbor)
                    elif colors[neighbor] == colors[vertex]:
                        return False
    return True


def fixed_formula(
    order: int,
    edge_set: set[tuple[int, int]],
    coloring_cuts: list[tuple[int, ...]],
) -> bytes:
    encoding = build_base(order, coloring_cuts)
    for pair, variable in encoding.edge_vars.items():
        encoding.cnf.add(variable if pair in edge_set else -variable)
    return encoding.cnf.dimacs()


def adjacency(order: int, edge_set: set[tuple[int, int]]) -> tuple[int, ...]:
    answer = [0] * order
    for u, v in edge_set:
        answer[u] |= 1 << v
        answer[v] |= 1 << u
    return tuple(answer)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=10.0)
    arguments = parser.parse_args()

    order = 4
    pairs = tuple(itertools.combinations(range(order), 2))
    base_sat_count = 0
    cut_checks = 0
    for mask in range(1 << len(pairs)):
        edge_set = {
            pair
            for position, pair in enumerate(pairs)
            if mask >> position & 1
        }
        expected = direct_base(order, edge_set)
        status, _, _ = solve(
            arguments.cadical,
            fixed_formula(order, edge_set, []),
            arguments.timeout,
        )
        if (status == "SAT") != expected:
            raise AssertionError(
                f"base truth-table mismatch at graph mask {mask}: "
                f"SAT={status}, direct={expected}"
            )
        if not expected:
            continue
        base_sat_count += 1
        colors = exact_coloring(adjacency(order, edge_set), 3)
        if colors is None:
            raise AssertionError("four-vertex base graph unexpectedly needs four colors")
        status_with_cut, _, _ = solve(
            arguments.cadical,
            fixed_formula(order, edge_set, [colors]),
            arguments.timeout,
        )
        if status_with_cut != "UNSAT":
            raise AssertionError("coloring cut did not exclude its source graph")
        cut_checks += 1

    print(
        json.dumps(
            {
                "schema": "gamma-theta-static-gate-cegar-audit-v1",
                "status": "PASS",
                "order": order,
                "labeled_graphs_checked": 1 << len(pairs),
                "base_sat_graphs": base_sat_count,
                "source_graph_coloring_cuts_checked": cut_checks,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
