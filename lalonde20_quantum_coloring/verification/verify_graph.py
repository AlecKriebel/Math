#!/usr/bin/env python3
"""Independent, standard-library-only verification of the graph data."""

from __future__ import annotations

import itertools
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_data import (  # noqa: E402
    ADJ19,
    CLIQUES20,
    E19,
    E20,
    GRAPH6_G19,
    TRIANGLES19,
    V19,
    V20,
)


def graph6(vertices: tuple[int, ...], edges: tuple[tuple[int, int], ...]) -> str:
    """Encode a graph of order at most 62 in graph6 format.

    graph6 orders upper-triangular adjacency bits column by column:
    (0,1), (0,2), (1,2), (0,3), ... in zero-based notation.
    """

    n = len(vertices)
    assert n <= 62
    position = {v: i for i, v in enumerate(vertices)}
    edge_positions = {
        tuple(sorted((position[v], position[w]))) for v, w in edges
    }
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(int((i, j) in edge_positions))
    bits.extend([0] * ((-len(bits)) % 6))
    payload = "".join(
        chr(63 + sum(bits[k + offset] << (5 - offset) for offset in range(6)))
        for k in range(0, len(bits), 6)
    )
    return chr(63 + n) + payload


def all_cliques_of_size(vertices: tuple[int, ...], adjacency, size: int):
    return tuple(
        subset
        for subset in itertools.combinations(vertices, size)
        if all(w in adjacency[v] for v, w in itertools.combinations(subset, 2))
    )


def main() -> None:
    assert len(E19) == 36
    assert len(E20) == 55
    assert len(set(E19)) == len(E19)
    assert len(set(E20)) == len(E20)
    assert graph6(V19, E19) == GRAPH6_G19
    assert set(all_cliques_of_size(V19, ADJ19, 3)) == set(TRIANGLES19)
    assert CLIQUES20 == (
        (1, 2, 3, 20),
        (1, 8, 9, 20),
        (3, 4, 5, 20),
        (2, 6, 7, 20),
    )
    print("graph verification: PASS")
    print(f"G19: {len(V19)} vertices, {len(E19)} edges, graph6={graph6(V19, E19)}")
    print(f"H:   {len(V20)} vertices, {len(E20)} edges")
    print(f"triangles(G19): {TRIANGLES19}")


if __name__ == "__main__":
    main()
