#!/usr/bin/env python3
"""Small exact coloured-mixed-graph canonicalizer.

This module is intentionally self-contained.  It uses equitable partition
refinement followed by individualization/backtracking; no project or external
graph package is imported.  Graphs in the atlas have at most sixteen vertices,
and labelled boundary vertices make the search trees very small.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Sequence


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value: Any) -> str:
    data = value if isinstance(value, (bytes, bytearray)) else canonical_json(value).encode()
    return sha256(data).hexdigest()


@dataclass(frozen=True, order=True)
class MixedEdge:
    """An undirected, directed, or relation edge.

    `kind` is `U` for an ordinary undirected edge, `A` for a retained
    arrowhead (tail -> head), or `MATCH` for a source-target port match.
    For `U` and `MATCH`, endpoint order has no meaning.
    """

    kind: str
    u: str
    v: str

    def normalized(self) -> "MixedEdge":
        if self.kind in {"U", "MATCH"} and self.v < self.u:
            return MixedEdge(self.kind, self.v, self.u)
        if self.kind not in {"U", "A", "MATCH"}:
            raise ValueError(f"unsupported edge kind {self.kind!r}")
        if self.u == self.v:
            raise ValueError("loops are forbidden")
        return self


@dataclass(frozen=True)
class ColouredMixedGraph:
    colors: Mapping[str, tuple[Any, ...]]
    edges: tuple[MixedEdge, ...]

    def normalized(self) -> "ColouredMixedGraph":
        names = set(self.colors)
        seen: set[frozenset[str]] = set()
        out: list[MixedEdge] = []
        for raw in self.edges:
            edge = raw.normalized()
            if edge.u not in names or edge.v not in names:
                raise ValueError(f"edge endpoint missing from vertex set: {edge}")
            pair = frozenset((edge.u, edge.v))
            if pair in seen:
                raise ValueError(f"parallel mixed edges are forbidden: {edge}")
            seen.add(pair)
            out.append(edge)
        return ColouredMixedGraph(dict(self.colors), tuple(sorted(out)))


def _adjacency(graph: ColouredMixedGraph) -> dict[str, dict[str, str]]:
    adjacency = {v: {} for v in graph.colors}
    for edge in graph.edges:
        if edge.kind in {"U", "MATCH"}:
            adjacency[edge.u][edge.v] = edge.kind
            adjacency[edge.v][edge.u] = edge.kind
        else:
            adjacency[edge.u][edge.v] = "A_OUT"
            adjacency[edge.v][edge.u] = "A_IN"
    return adjacency


def _initial_partition(graph: ColouredMixedGraph) -> tuple[tuple[str, ...], ...]:
    groups: dict[str, list[str]] = {}
    for vertex, color in graph.colors.items():
        groups.setdefault(canonical_json(color), []).append(vertex)
    return tuple(tuple(sorted(groups[key])) for key in sorted(groups))


def _refine(
    graph: ColouredMixedGraph,
    partition: tuple[tuple[str, ...], ...],
    adjacency: Mapping[str, Mapping[str, str]],
) -> tuple[tuple[str, ...], ...]:
    while True:
        changed = False
        refined: list[tuple[str, ...]] = []
        for cell in partition:
            buckets: dict[str, list[str]] = {}
            for vertex in cell:
                signature = []
                neighbors = adjacency[vertex]
                for other_cell in partition:
                    counts: dict[str, int] = {}
                    for other in other_cell:
                        relation = neighbors.get(other, "NONE")
                        counts[relation] = counts.get(relation, 0) + 1
                    signature.append(tuple(sorted(counts.items())))
                key = canonical_json(signature)
                buckets.setdefault(key, []).append(vertex)
            for key in sorted(buckets):
                refined.append(tuple(sorted(buckets[key])))
            changed |= len(buckets) > 1
        new_partition = tuple(refined)
        if not changed:
            return new_partition
        partition = new_partition


def _ordered_code(graph: ColouredMixedGraph, order: Sequence[str]) -> dict[str, Any]:
    position = {vertex: index for index, vertex in enumerate(order)}
    adjacency = _adjacency(graph)
    matrix: list[str] = []
    for i, u in enumerate(order):
        for v in order[i + 1 :]:
            relation = adjacency[u].get(v, "0")
            if relation == "A_OUT":
                matrix.append("2")
            elif relation == "A_IN":
                matrix.append("3")
            elif relation == "U":
                matrix.append("1")
            elif relation == "MATCH":
                matrix.append("4")
            else:
                matrix.append("0")
    return {
        "colors": [list(graph.colors[v]) for v in order],
        "upper_triangle": "".join(matrix),
        "order_size": len(order),
        "edge_count": len(graph.edges),
        "positions": position,
    }


def canonicalize(graph: ColouredMixedGraph) -> tuple[dict[str, Any], dict[str, int]]:
    """Return canonical code and a winning raw-name -> canonical-index map."""

    graph = graph.normalized()
    adjacency = _adjacency(graph)
    start = _refine(graph, _initial_partition(graph), adjacency)
    best_serialized: str | None = None
    best_code: dict[str, Any] | None = None
    best_map: dict[str, int] | None = None

    def visit(partition: tuple[tuple[str, ...], ...]) -> None:
        nonlocal best_serialized, best_code, best_map
        partition = _refine(graph, partition, adjacency)
        if all(len(cell) == 1 for cell in partition):
            order = tuple(cell[0] for cell in partition)
            code = _ordered_code(graph, order)
            positions = code.pop("positions")
            serialized = canonical_json(code)
            if best_serialized is None or serialized < best_serialized:
                best_serialized = serialized
                best_code = code
                best_map = positions
            return

        # The first non-singleton cell is intrinsic because the partition is
        # canonically ordered by colour/refinement signatures.  Every possible
        # individualization is explored; raw names only choose branch order.
        index = next(i for i, cell in enumerate(partition) if len(cell) > 1)
        cell = partition[index]
        for chosen in sorted(cell):
            remainder = tuple(v for v in cell if v != chosen)
            child = list(partition[:index])
            child.append((chosen,))
            if remainder:
                child.append(remainder)
            child.extend(partition[index + 1 :])
            visit(tuple(child))

    visit(start)
    assert best_code is not None and best_map is not None
    return best_code, best_map


def canonical_edge_order(
    graph: ColouredMixedGraph, vertex_map: Mapping[str, int]
) -> tuple[tuple[tuple[Any, ...], ...], dict[int, int]]:
    """Return canonical edge records and raw-index -> canonical-index map."""

    records: list[tuple[tuple[Any, ...], int]] = []
    for raw_index, edge0 in enumerate(graph.normalized().edges):
        edge = edge0.normalized()
        a, b = vertex_map[edge.u], vertex_map[edge.v]
        if edge.kind in {"U", "MATCH"}:
            record = (edge.kind, min(a, b), max(a, b))
        else:
            record = ("A", a, b)
        records.append((record, raw_index))
    records.sort()
    raw_to_canonical = {raw: index for index, (_record, raw) in enumerate(records)}
    return tuple(record for record, _raw in records), raw_to_canonical


def transport_edge(
    edge: MixedEdge, vertex_map: Mapping[str, int]
) -> tuple[Any, ...]:
    a, b = vertex_map[edge.u], vertex_map[edge.v]
    if edge.kind in {"U", "MATCH"}:
        return (edge.kind, min(a, b), max(a, b))
    return ("A", a, b)


def merkle_root(hashes: Iterable[str]) -> str:
    layer = [bytes.fromhex(item) for item in sorted(hashes)]
    if not layer:
        return sha256(b"").hexdigest()
    while len(layer) > 1:
        if len(layer) % 2:
            layer.append(layer[-1])
        layer = [sha256(layer[i] + layer[i + 1]).digest() for i in range(0, len(layer), 2)]
    return layer[0].hex()

