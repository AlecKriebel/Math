#!/usr/bin/env python3
"""Narrow-standard admissible-rooting census for canonical mixed graphs."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterator, Mapping, Sequence

from graphcanon import ColouredMixedGraph


def _acyclic_reachable(vertices: Sequence[str], arcs: Sequence[tuple[str, str]], root: str) -> bool:
    children: dict[str, list[str]] = defaultdict(list)
    indegree = {vertex: 0 for vertex in vertices}
    for tail, head in arcs:
        children[tail].append(head)
        indegree[head] += 1
    queue = [vertex for vertex in vertices if indegree[vertex] == 0]
    visited = 0
    while queue:
        vertex = queue.pop()
        visited += 1
        for child in children[vertex]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if visited != len(vertices):
        return False
    seen = {root}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for child in children[vertex]:
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return seen == set(vertices)


def _lsa_valid(
    graph_vertices: Sequence[str],
    arcs: Sequence[tuple[str, str]],
    root: str,
    leaves: set[str],
) -> bool:
    children: dict[str, list[str]] = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    for removed in graph_vertices:
        if removed == root:
            continue
        seen = {root}
        stack = [root]
        while stack:
            vertex = stack.pop()
            for child in children[vertex]:
                if child == removed or child in seen:
                    continue
                seen.add(child)
                stack.append(child)
        if not (seen & leaves):
            return False
    return True


def _tree_child(
    graph: ColouredMixedGraph,
    arcs: Sequence[tuple[str, str]],
    root: str,
) -> bool:
    children: dict[str, list[str]] = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    for vertex in (root, *graph.colors.keys()):
        color = ("ROOT",) if vertex == root else graph.colors[vertex]
        if color[0] == "PORT":
            continue
        if not children[vertex]:
            return False
        if not any(
            child != root
            and (
                graph.colors[child][0] == "PORT"
                or graph.colors[child] == ("INTERNAL", "T")
            )
            for child in children[vertex]
        ):
            return False
    return True


def admissible_rootings(graph: ColouredMixedGraph) -> Iterator[dict[str, Any]]:
    graph = graph.normalized()
    vertices = tuple(sorted(graph.colors))
    leaves = {vertex for vertex, color in graph.colors.items() if color[0] == "PORT"}
    for split_index, split_edge in enumerate(graph.edges):
        root = "__ROOT__"
        all_vertices = (*vertices, root)
        fixed: list[tuple[str, str]] = [(root, split_edge.u), (root, split_edge.v)]
        undirected = []
        for edge_index, edge in enumerate(graph.edges):
            if edge_index == split_index:
                continue
            if edge.kind == "A":
                fixed.append((edge.u, edge.v))
            elif edge.kind == "U":
                undirected.append((edge.u, edge.v))
            else:
                raise ValueError("relation edges cannot occur in a network rooting census")

        target_in: dict[str, int] = {root: 0}
        target_out: dict[str, int] = {root: 2}
        for vertex, color in graph.colors.items():
            if color[0] == "PORT":
                target_in[vertex], target_out[vertex] = 1, 0
            elif color == ("INTERNAL", "R"):
                target_in[vertex], target_out[vertex] = 2, 1
            elif color == ("INTERNAL", "T"):
                target_in[vertex], target_out[vertex] = 1, 2
            else:
                raise ValueError(f"unsupported network vertex colour {color}")
        in_count = {vertex: 0 for vertex in all_vertices}
        out_count = {vertex: 0 for vertex in all_vertices}
        for tail, head in fixed:
            out_count[tail] += 1
            in_count[head] += 1
        remaining = {vertex: 0 for vertex in all_vertices}
        for u, v in undirected:
            remaining[u] += 1
            remaining[v] += 1
        chosen: list[tuple[str, str] | None] = [None] * len(undirected)

        def recurse(index: int) -> Iterator[dict[str, Any]]:
            if index == len(undirected):
                if in_count != target_in or out_count != target_out:
                    return
                arcs = tuple(fixed) + tuple(item for item in chosen if item is not None)
                if not _acyclic_reachable(all_vertices, arcs, root):
                    return
                if not _lsa_valid(all_vertices, arcs, root, leaves):
                    return
                yield {
                    "split_edge_index": split_index,
                    "split_edge": [split_edge.kind, split_edge.u, split_edge.v],
                    "arcs": [list(item) for item in sorted(arcs)],
                    "tree_child": _tree_child(graph, arcs, root),
                }
                return
            u, v = undirected[index]
            for tail, head in ((u, v), (v, u)):
                chosen[index] = (tail, head)
                out_count[tail] += 1
                in_count[head] += 1
                remaining[u] -= 1
                remaining[v] -= 1
                feasible = True
                for vertex in (u, v):
                    if in_count[vertex] > target_in[vertex] or out_count[vertex] > target_out[vertex]:
                        feasible = False
                    if in_count[vertex] + remaining[vertex] < target_in[vertex]:
                        feasible = False
                    if out_count[vertex] + remaining[vertex] < target_out[vertex]:
                        feasible = False
                if feasible:
                    yield from recurse(index + 1)
                remaining[u] += 1
                remaining[v] += 1
                out_count[tail] -= 1
                in_count[head] -= 1
            chosen[index] = None

        yield from recurse(0)


def rooting_census(graph: ColouredMixedGraph) -> dict[str, Any]:
    rootings = list(admissible_rootings(graph))
    tree_child_count = sum(bool(rooting["tree_child"]) for rooting in rootings)
    return {
        "admissible_rootings": len(rootings),
        "tree_child_rootings": tree_child_count,
        "non_tree_child_rootings": len(rootings) - tree_child_count,
        "W_TC": tree_child_count > 0,
        "S_TC": bool(rootings) and tree_child_count == len(rootings),
        # Edge indices above are deliberately local to the rooting enumerator.
        # Persist intrinsic mixed-edge records instead, so the certificate does
        # not invite interpretation against a separately serialized edge order.
        "root_edges": [
            list(edge)
            for edge in sorted({tuple(rooting["split_edge"]) for rooting in rootings})
        ],
    }
