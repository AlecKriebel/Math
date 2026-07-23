#!/usr/bin/env python3
"""Exact finite checks accompanying the forced-negative-tail proof."""

import importlib.util
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANTIPODAL_PATH = ROOT / "verifiers" / "verify_antipodal_bound.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_antipodal_bound_for_negative_tail", ANTIPODAL_PATH
)
assert SPEC is not None and SPEC.loader is not None
ANTIPODAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANTIPODAL)


def sharp_graph() -> tuple[frozenset[tuple[int, int]], int]:
    """Return C5 disjoint union 18 K2, with 41 vertices."""

    edges: set[tuple[int, int]] = set()
    for i in range(5):
        edges.add(tuple(sorted((i, (i + 1) % 5))))
    next_vertex = 5
    for _ in range(18):
        edges.add((next_vertex, next_vertex + 1))
        next_vertex += 2
    assert next_vertex == 41
    return frozenset(edges), next_vertex


def is_triangle_free(edges: frozenset[tuple[int, int]], n: int) -> bool:
    adjacency = [set() for _ in range(n)]
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    return not any(
        adjacency[i].intersection(adjacency[j])
        for i, j in edges
    )


def independent_number_bitset(
    edges: frozenset[tuple[int, int]], n: int
) -> int:
    """Exact branch recursion; the sharp graph separates into tiny pieces."""

    adjacency = [0] * n
    for i, j in edges:
        adjacency[i] |= 1 << j
        adjacency[j] |= 1 << i

    def solve(vertices: int) -> int:
        if vertices == 0:
            return 0
        # Component splitting makes the 18 isolated K2 components immediate.
        seed = vertices & -vertices
        component = seed
        frontier = seed
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            v = bit.bit_length() - 1
            new = adjacency[v] & vertices & ~component
            component |= new
            frontier |= new
        rest = vertices & ~component
        if rest:
            return solve(component) + solve(rest)
        v = (vertices & -vertices).bit_length() - 1
        without_v = solve(vertices & ~(1 << v))
        with_v = 1 + solve(vertices & ~(1 << v) & ~adjacency[v])
        return max(without_v, with_v)

    return solve((1 << n) - 1)


def verify() -> dict[str, object]:
    assert ANTIPODAL.verify()["status"] == "PASS"

    # Arithmetic cases in the graph proof.
    n = 41
    alpha_limit = 20
    tau_min = n - alpha_limit
    asserted_edge_minimum = 23
    assert tau_min == 21
    assert asserted_edge_minimum == tau_min + 2
    assert Q(3) + 2 * 3 * Q(-1, 2) == 0
    # Therefore three strict inequalities t_ij < -1/2 make
    # 3 + 2(t_12+t_13+t_23) strictly negative.

    edges, vertex_count = sharp_graph()
    assert vertex_count == n
    assert len(edges) == asserted_edge_minimum
    assert is_triangle_free(edges, vertex_count)
    alpha = independent_number_bitset(edges, vertex_count)
    assert alpha == alpha_limit

    return {
        "vertices": vertex_count,
        "edge_lower_bound": asserted_edge_minimum,
        "sharp_example_edges": len(edges),
        "sharp_example_independence_number": alpha,
        "sharp_example_triangle_free": True,
        "ordered_negative_pair_lower_bound": 2 * asserted_edge_minimum,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
