"""Canonical graph data for the Lalonde 20-vertex problem.

Vertices are numbered as in the problem statement.  All edge tuples are stored
in increasing order.  This module deliberately depends only on the Python
standard library so that certificate verifiers can import it in a minimal
environment.
"""

from __future__ import annotations


V19 = tuple(range(1, 20))
V20 = tuple(range(1, 21))

E19 = (
    (1, 2), (1, 3), (1, 8), (1, 9), (1, 15),
    (2, 3), (2, 6), (2, 7), (2, 14),
    (3, 4), (3, 5), (3, 16),
    (4, 5), (4, 12), (4, 13),
    (5, 10), (5, 11), (5, 17),
    (6, 7), (6, 11), (6, 13),
    (7, 10), (7, 12), (7, 19),
    (8, 9), (8, 11), (8, 12), (8, 18),
    (9, 10), (9, 13),
    (14, 17), (14, 18),
    (15, 17), (15, 19),
    (16, 18), (16, 19),
)

E20 = E19 + tuple((v, 20) for v in V19)

TRIANGLES19 = (
    (1, 2, 3),
    (1, 8, 9),
    (3, 4, 5),
    (2, 6, 7),
)

CLIQUES20 = tuple(tuple(sorted(triangle + (20,))) for triangle in TRIANGLES19)

GRAPH6_G19 = "RxLAKA@AgYAWDGO?O?@??A?W@@OC@_"


def adjacency(vertices: tuple[int, ...], edges: tuple[tuple[int, int], ...]):
    """Return an immutable-neighbour-set adjacency dictionary."""

    mutable = {v: set() for v in vertices}
    for v, w in edges:
        if v >= w:
            raise ValueError(f"edge is not strictly ordered: {(v, w)}")
        if v not in mutable or w not in mutable:
            raise ValueError(f"edge endpoint outside vertex set: {(v, w)}")
        mutable[v].add(w)
        mutable[w].add(v)
    return {v: frozenset(neighbours) for v, neighbours in mutable.items()}


ADJ19 = adjacency(V19, E19)
ADJ20 = adjacency(V20, E20)
