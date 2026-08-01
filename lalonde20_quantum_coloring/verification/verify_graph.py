#!/usr/bin/env python3
"""Independent, standard-library-only verification of the graph data."""

from __future__ import annotations

import itertools
import pathlib
import sys


if not __debug__:
    raise RuntimeError(
        "verify_graph.py relies on executable assertions; rerun without Python -O"
    )


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


# Lalonde Section 4.2's published classical four-coloring, indexed by V19.
# Keeping the literal witness here makes the classical upper bound
# independently executable.
PUBLISHED_FOUR_COLORING = (
    1, 2, 3, 2, 1, 3, 1, 3, 2, 3, 2, 4, 1, 1, 2, 1, 3, 2, 3,
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


def is_proper_coloring(
    vertices: tuple[int, ...],
    edges: tuple[tuple[int, int], ...],
    colors: dict[int, int],
) -> bool:
    """Check a total proper coloring exactly."""

    return set(colors) == set(vertices) and all(colors[v] != colors[w] for v, w in edges)


def exhaustive_coloring_search(
    vertices: tuple[int, ...],
    adjacency,
    color_count: int,
    fixed: dict[int, int] | None = None,
):
    """Return a proper coloring or prove none exists by exhaustive search.

    The recursion tries every color not already used by a colored neighbor.
    Choosing a maximum-saturation vertex is only an ordering heuristic: it
    removes no feasible branch.  ``visited`` counts recursive states, making
    the completed finite search visible in the verifier output.
    """

    colors = dict(fixed or {})
    assert all(0 <= color < color_count for color in colors.values())
    assert all(
        colors[v] != colors[w]
        for v in colors
        for w in adjacency[v]
        if w in colors
    )
    visited = 0

    def search():
        nonlocal visited
        visited += 1
        if len(colors) == len(vertices):
            return dict(colors)

        uncolored = [vertex for vertex in vertices if vertex not in colors]

        def priority(vertex):
            neighbor_colors = {colors[w] for w in adjacency[vertex] if w in colors}
            # The final component makes ties deterministic by preferring the
            # lower vertex label.
            return (len(neighbor_colors), len(adjacency[vertex]), -vertex)

        vertex = max(uncolored, key=priority)
        forbidden = {colors[w] for w in adjacency[vertex] if w in colors}
        for color in range(color_count):
            if color in forbidden:
                continue
            colors[vertex] = color
            result = search()
            if result is not None:
                return result
            del colors[vertex]
        return None

    return search(), visited


def main() -> None:
    assert len(E19) == 36
    assert len(E20) == 55
    assert len(set(E19)) == len(E19)
    assert len(set(E20)) == len(E20)
    assert graph6(V19, E19) == GRAPH6_G19
    assert set(all_cliques_of_size(V19, ADJ19, 3)) == set(TRIANGLES19)
    assert all_cliques_of_size(V19, ADJ19, 4) == ()
    assert CLIQUES20 == (
        (1, 2, 3, 20),
        (1, 8, 9, 20),
        (3, 4, 5, 20),
        (2, 6, 7, 20),
    )

    published_coloring = dict(zip(V19, PUBLISHED_FOUR_COLORING, strict=True))
    assert set(published_coloring.values()) == {1, 2, 3, 4}
    assert is_proper_coloring(V19, E19, published_coloring)

    # Vertices 1,2,3 form a triangle, so every hypothetical three-coloring
    # uses three distinct colors there.  Permuting color names lets us fix
    # them to 0,1,2 without losing any solution.  The remaining recursion is
    # exhaustive and prunes only an immediately monochromatic edge.
    assert (1, 2, 3) in TRIANGLES19
    three_coloring, visited = exhaustive_coloring_search(
        V19,
        ADJ19,
        3,
        fixed={1: 0, 2: 1, 3: 2},
    )
    assert three_coloring is None

    print("graph verification: PASS")
    print(f"G19: {len(V19)} vertices, {len(E19)} edges, graph6={graph6(V19, E19)}")
    print(f"H:   {len(V20)} vertices, {len(E20)} edges")
    print(f"triangles(G19): {TRIANGLES19}")
    print("K4(G19): none")
    print("published four-coloring(G19): PASS")
    print(f"three-coloring(G19): UNSAT by exhaustive backtracking ({visited} states)")
    print("chi(G19): 4")


if __name__ == "__main__":
    main()
