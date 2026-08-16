#!/usr/bin/env python3
"""Independent exact structural test for Outcome Q's cleanup-rooting fibre.

This file deliberately imports no code from the Outcome Q package.  It checks
an explicit binary rooted level-2 DAG, performs typed semi-directed cleanup,
and records whether the resulting rooting is tree-child.
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from dataclasses import dataclass

if not __debug__:
    raise RuntimeError("This exact verifier refuses optimized Python because it uses assertions.")


ROOT = "r"
LEAVES = {"L1", "L2", "L3"}
ARCS = (
    ("r", "P"),
    ("r", "Q"),
    ("P", "Q"),
    ("P", "p"),
    ("Q", "q"),
    ("p", "q"),
    ("p", "L1"),
    ("q", "t"),
    ("t", "L2"),
    ("t", "L3"),
)


def vertices() -> set[str]:
    return {v for edge in ARCS for v in edge}


def degrees() -> tuple[dict[str, int], dict[str, int]]:
    indeg = {v: 0 for v in vertices()}
    outdeg = {v: 0 for v in vertices()}
    for u, v in ARCS:
        outdeg[u] += 1
        indeg[v] += 1
    return indeg, outdeg


def rooted_types() -> dict[str, str]:
    indeg, outdeg = degrees()
    result: dict[str, str] = {}
    for v in sorted(vertices()):
        pair = (indeg[v], outdeg[v])
        if v == ROOT and pair == (0, 2):
            result[v] = "root"
        elif v in LEAVES and pair == (1, 0):
            result[v] = "leaf"
        elif pair == (1, 2):
            result[v] = "tree"
        elif pair == (2, 1):
            result[v] = "reticulation"
        else:
            raise AssertionError(f"nonbinary vertex {v}: {pair}")
    assert set(result) == vertices()
    return result


def topological_order() -> list[str]:
    indeg, _ = degrees()
    children: dict[str, list[str]] = defaultdict(list)
    for u, v in ARCS:
        children[u].append(v)
    queue = deque(sorted(v for v, d in indeg.items() if d == 0))
    order: list[str] = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in sorted(children[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    assert len(order) == len(vertices()), "directed cycle"
    return order


def root_leaf_paths() -> list[tuple[str, ...]]:
    children: dict[str, list[str]] = defaultdict(list)
    for u, v in ARCS:
        children[u].append(v)
    result: list[tuple[str, ...]] = []

    def visit(u: str, path: tuple[str, ...]) -> None:
        next_path = path + (u,)
        if u in LEAVES:
            result.append(next_path)
            return
        for v in sorted(children[u]):
            visit(v, next_path)

    visit(ROOT, ())
    assert {p[-1] for p in result} == LEAVES
    return result


def lsa_valid() -> tuple[bool, list[str]]:
    common = set(root_leaf_paths()[0])
    for path in root_leaf_paths()[1:]:
        common.intersection_update(path)
    return common == {ROOT}, sorted(common)


def tree_child() -> tuple[bool, list[str]]:
    types = rooted_types()
    children: dict[str, list[str]] = defaultdict(list)
    for u, v in ARCS:
        children[u].append(v)
    offenders = [
        u
        for u in sorted(vertices() - LEAVES)
        if not any(types[v] in {"tree", "leaf"} for v in children[u])
    ]
    return not offenders, offenders


def biconnected_edge_components() -> list[list[tuple[str, str]]]:
    """Tarjan edge-stack algorithm on the underlying simple graph."""

    adjacency: dict[str, list[str]] = defaultdict(list)
    for u, v in ARCS:
        adjacency[u].append(v)
        adjacency[v].append(u)
    discovery: dict[str, int] = {}
    low: dict[str, int] = {}
    parent: dict[str, str | None] = {}
    stack: list[tuple[str, str]] = []
    components: list[list[tuple[str, str]]] = []
    time = 0

    def dfs(u: str) -> None:
        nonlocal time
        time += 1
        discovery[u] = low[u] = time
        for v in sorted(adjacency[u]):
            edge = tuple(sorted((u, v)))
            if v not in discovery:
                parent[v] = u
                stack.append(edge)
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] >= discovery[u]:
                    component: list[tuple[str, str]] = []
                    while stack:
                        popped = stack.pop()
                        component.append(popped)
                        if popped == edge:
                            break
                    components.append(component)
            elif parent.get(u) != v and discovery[v] < discovery[u]:
                stack.append(edge)
                low[u] = min(low[u], discovery[v])

    parent[ROOT] = None
    dfs(ROOT)
    assert len(discovery) == len(vertices())
    return components


def level() -> tuple[int, list[dict[str, object]]]:
    retics = {v for v, typ in rooted_types().items() if typ == "reticulation"}
    records: list[dict[str, object]] = []
    maximum = 0
    for edges in biconnected_edge_components():
        verts = {v for edge in edges for v in edge}
        count = len(verts & retics)
        maximum = max(maximum, count)
        records.append(
            {
                "edges": sorted([list(e) for e in edges]),
                "vertices": sorted(verts),
                "reticulations": sorted(verts & retics),
            }
        )
    return maximum, records


@dataclass(frozen=True)
class MixedEdge:
    u: str
    v: str
    arrowheads: frozenset[str]

    @staticmethod
    def make(u: str, v: str, arrowheads: set[str] | frozenset[str]) -> "MixedEdge":
        left, right = sorted((u, v))
        return MixedEdge(left, right, frozenset(arrowheads))

    @property
    def endpoints(self) -> frozenset[str]:
        return frozenset((self.u, self.v))


def cleanup() -> tuple[list[MixedEdge], list[dict[str, object]]]:
    """Brits-style typed root suppression, parallel merge, and degree-2 cleanup."""

    types = rooted_types()
    edges: list[MixedEdge] = []
    for u, v in ARCS:
        arrows = {v} if types[v] == "reticulation" else set()
        edges.append(MixedEdge.make(u, v, arrows))
    trace: list[dict[str, object]] = []

    def incidence(vertex: str) -> list[int]:
        return [i for i, edge in enumerate(edges) if vertex in edge.endpoints]

    def suppress(vertex: str, reason: str) -> None:
        indexes = incidence(vertex)
        assert len(indexes) == 2, (vertex, indexes)
        first, second = (edges[i] for i in indexes)
        a = next(iter(first.endpoints - {vertex}))
        b = next(iter(second.endpoints - {vertex}))
        assert a != b, f"suppression would make loop at {a}"
        arrows = (set(first.arrowheads) | set(second.arrowheads)) - {vertex}
        for i in sorted(indexes, reverse=True):
            edges.pop(i)
        edges.append(MixedEdge.make(a, b, arrows))
        trace.append(
            {
                "operation": "suppress",
                "reason": reason,
                "vertex": vertex,
                "new_edge": [a, b],
                "new_arrowheads": sorted(arrows),
            }
        )

    suppress(ROOT, "root")

    changed = True
    while changed:
        changed = False
        groups: dict[tuple[str, str], list[int]] = defaultdict(list)
        for i, edge in enumerate(edges):
            groups[(edge.u, edge.v)].append(i)
        parallel = next((key for key, ids in sorted(groups.items()) if len(ids) > 1), None)
        if parallel is not None:
            ids = groups[parallel]
            arrow_sets = {edges[i].arrowheads for i in ids}
            assert len(arrow_sets) == 1, (parallel, arrow_sets)
            keep = edges[ids[0]]
            for i in sorted(ids, reverse=True):
                edges.pop(i)
            edges.append(keep)
            trace.append(
                {
                    "operation": "identify_parallel",
                    "endpoints": list(parallel),
                    "multiplicity": len(ids),
                    "arrowheads": sorted(keep.arrowheads),
                }
            )
            changed = True
            continue

        current_vertices = {v for edge in edges for v in edge.endpoints}
        degree_two = next(
            (
                v
                for v in sorted(current_vertices - LEAVES)
                if len(incidence(v)) == 2
            ),
            None,
        )
        if degree_two is not None:
            suppress(degree_two, "unlabelled_degree_two")
            changed = True

    return sorted(edges, key=lambda e: (e.u, e.v, sorted(e.arrowheads))), trace


def main() -> None:
    assert len(set(ARCS)) == len(ARCS), "parallel directed arcs"
    types = rooted_types()
    order = topological_order()
    paths = root_leaf_paths()
    lsa_ok, stable = lsa_valid()
    tc_ok, offenders = tree_child()
    network_level, blobs = level()
    cleaned, trace = cleanup()
    expected = {
        MixedEdge.make("L1", "t", set()),
        MixedEdge.make("L2", "t", set()),
        MixedEdge.make("L3", "t", set()),
    }
    assert lsa_ok
    assert network_level == 2
    assert not tc_ok and "Q" in offenders
    assert set(cleaned) == expected
    assert all(not edge.arrowheads for edge in cleaned)

    result = {
        "status": "EXACTLY COMPUTED",
        "claim": "Outcome Q complete cleanup rooting fibre contains a non-tree-child level-2 double zipper over the ordinary 3-leaf tree",
        "arcs": [list(edge) for edge in ARCS],
        "types": types,
        "topological_order": order,
        "root_leaf_paths": [list(path) for path in paths],
        "vertices_common_to_all_root_leaf_paths": stable,
        "lsa_valid": lsa_ok,
        "tree_child": tc_ok,
        "tree_child_offenders": offenders,
        "level": network_level,
        "biconnected_components": blobs,
        "cleanup_trace": trace,
        "cleaned_edges": [
            {"endpoints": [edge.u, edge.v], "arrowheads": sorted(edge.arrowheads)}
            for edge in cleaned
        ],
        "cleaned_topology": "ordinary labelled 3-leaf unrooted tree",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
