"""Independent rooted and semi-directed graph checks for the root/cut audit."""

from __future__ import annotations

import itertools
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class MixedEdge:
    endpoints: frozenset[str]
    arrowheads: frozenset[str]

    @classmethod
    def make(
        cls, left: str, right: str, arrowheads: Iterable[str] = ()
    ) -> "MixedEdge":
        if left == right:
            raise ValueError("mixed loop")
        endpoints = frozenset((left, right))
        heads = frozenset(arrowheads)
        if not heads <= endpoints:
            raise ValueError("arrowhead is not an endpoint")
        return cls(endpoints, heads)

    def other(self, vertex: str) -> str:
        return next(iter(self.endpoints - {vertex}))


def degree_maps(arcs: Sequence[tuple[str, str]]) -> tuple[Counter[str], Counter[str]]:
    indegree: Counter[str] = Counter()
    outdegree: Counter[str] = Counter()
    for tail, head in arcs:
        outdegree[tail] += 1
        indegree[head] += 1
        indegree.setdefault(tail, 0)
        outdegree.setdefault(head, 0)
    return indegree, outdegree


def descendants_from(arcs: Sequence[tuple[str, str]], start: str, avoid: str | None = None) -> set[str]:
    children: dict[str, list[str]] = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    reached: set[str] = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex == avoid or vertex in reached:
            continue
        reached.add(vertex)
        stack.extend(children[vertex])
    return reached


def rooted_checks(
    root: str, arcs: Sequence[tuple[str, str]], labels: Mapping[str, int]
) -> dict[str, object]:
    arcs = tuple(arcs)
    vertices = {vertex for arc in arcs for vertex in arc}
    indegree, outdegree = degree_maps(arcs)
    failures: set[str] = set()
    if len(arcs) != len(set(arcs)):
        failures.add("parallel_directed_arc")
    if any(tail == head for tail, head in arcs):
        failures.add("directed_loop")
    if (indegree[root], outdegree[root]) != (0, 2):
        failures.add("root_bidegree")
    for vertex in vertices:
        degree = (indegree[vertex], outdegree[vertex])
        if vertex in labels:
            if degree != (1, 0):
                failures.add("leaf_bidegree")
        elif vertex != root and degree not in {(1, 2), (2, 1)}:
            failures.add("internal_bidegree")

    indegrees = {vertex: indegree[vertex] for vertex in vertices}
    children: dict[str, list[str]] = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    queue = deque(sorted(vertex for vertex in vertices if indegrees[vertex] == 0))
    seen: list[str] = []
    while queue:
        vertex = queue.popleft()
        seen.append(vertex)
        for child in children[vertex]:
            indegrees[child] -= 1
            if indegrees[child] == 0:
                queue.append(child)
    if len(seen) != len(vertices):
        failures.add("directed_cycle")
    if descendants_from(arcs, root) != vertices:
        failures.add("not_root_reachable")

    leaves = set(labels)
    lsa = True
    for candidate in vertices - leaves - {root}:
        avoiding = descendants_from(arcs, root, candidate)
        if not any(leaf in avoiding for leaf in leaves):
            lsa = False
            failures.add("root_not_lowest_stable_ancestor")
            break

    tree_child = True
    for vertex in vertices - leaves:
        if not any(child in leaves or indegree[child] == 1 for child in children[vertex]):
            tree_child = False
            failures.add("rooting_not_tree_child")
            break
    return {
        "valid": not failures,
        "failures": sorted(failures),
        "root_is_lsa": lsa,
        "tree_child": tree_child,
        "reticulations": sorted(
            vertex
            for vertex in vertices
            if (indegree[vertex], outdegree[vertex]) == (2, 1)
        ),
    }


def suppress_root_once(
    root: str, arcs: Sequence[tuple[str, str]]
) -> tuple[list[MixedEdge], set[str]]:
    """Apply the literal Englander Definition 2.2 operation once.

    Ordinary directions are forgotten, reticulation arrowheads are retained,
    and the former root is suppressed.  No parallel identification or further
    degree-two suppression is performed here.
    """

    indegree, outdegree = degree_maps(arcs)
    reticulations = {
        vertex
        for vertex in set(indegree) | set(outdegree)
        if (indegree[vertex], outdegree[vertex]) == (2, 1)
    }
    root_incident: list[MixedEdge] = []
    retained: list[MixedEdge] = []
    for tail, head in arcs:
        edge = MixedEdge.make(tail, head, (head,) if head in reticulations else ())
        if root in edge.endpoints:
            root_incident.append(edge)
        else:
            retained.append(edge)
    if len(root_incident) != 2:
        raise ValueError("root does not have two incident edges")
    left, right = root_incident
    u, v = left.other(root), right.other(root)
    inherited = ({u} & left.arrowheads) | ({v} & right.arrowheads)
    retained.append(MixedEdge.make(u, v, inherited))
    return retained, reticulations


def incidence(edges: Sequence[MixedEdge]) -> dict[str, list[MixedEdge]]:
    result: dict[str, list[MixedEdge]] = defaultdict(list)
    for edge in edges:
        for vertex in edge.endpoints:
            result[vertex].append(edge)
    return result


def validate_literal_standard(
    edges: Sequence[MixedEdge], labels: Mapping[str, int]
) -> dict[str, object]:
    failures: set[str] = set()
    endpoint_counts = Counter(edge.endpoints for edge in edges)
    if any(count > 1 for count in endpoint_counts.values()):
        failures.add("parallel_mixed_edge")
    local_incidence = incidence(edges)
    incoming = Counter(vertex for edge in edges for vertex in edge.arrowheads)
    undirected = Counter()
    tails: set[str] = set()
    for edge in edges:
        if len(edge.arrowheads) > 1:
            failures.add("multiheaded_edge")
        if not edge.arrowheads:
            for vertex in edge.endpoints:
                undirected[vertex] += 1
        elif len(edge.arrowheads) == 1:
            head = next(iter(edge.arrowheads))
            tails.update(edge.endpoints - {head})
    for vertex, adjacent in local_incidence.items():
        degree = len(adjacent)
        if vertex in labels:
            if degree != 1:
                failures.add("mixed_leaf_degree")
            continue
        if degree != 3:
            failures.add("mixed_internal_degree")
        if incoming[vertex] not in {0, 2}:
            failures.add("mixed_arrowhead_count")
    for tail in tails:
        if undirected[tail] != 2:
            failures.add("local_strong_tail_condition")
    return {
        "valid_standard_strong": not failures,
        "failures": sorted(failures),
        "parallel_pairs": [
            sorted(endpoints)
            for endpoints, count in endpoint_counts.items()
            if count > 1
        ],
    }


def merge_all_parallel(edges: Sequence[MixedEdge]) -> list[MixedEdge]:
    grouped: dict[frozenset[str], set[str]] = defaultdict(set)
    for edge in edges:
        grouped[edge.endpoints].update(edge.arrowheads)
    return [MixedEdge(endpoints, frozenset(heads)) for endpoints, heads in grouped.items()]


def suppress_degree_two(edges: Sequence[MixedEdge], vertex: str) -> list[MixedEdge]:
    adjacent = [edge for edge in edges if vertex in edge.endpoints]
    if len(adjacent) != 2:
        raise ValueError("suppression vertex is not degree two")
    left, right = adjacent
    u, v = left.other(vertex), right.other(vertex)
    result = [edge for edge in edges if edge not in adjacent]
    if u != v:
        heads = ({u} & left.arrowheads) | ({v} & right.arrowheads)
        result.append(MixedEdge.make(u, v, heads))
    return merge_all_parallel(result)


def broad_artifact_reduction(
    root: str, arcs: Sequence[tuple[str, str]], labels: Mapping[str, int]
) -> list[MixedEdge]:
    edges, _ = suppress_root_once(root, arcs)
    edges = merge_all_parallel(edges)
    while True:
        local = incidence(edges)
        candidates = sorted(
            vertex
            for vertex, adjacent in local.items()
            if vertex not in labels and len(adjacent) == 2
        )
        if not candidates:
            return merge_all_parallel(edges)
        edges = suppress_degree_two(edges, candidates[0])


def ordinary_triangle_status(
    edges: Sequence[MixedEdge], labels: Mapping[str, int]
) -> dict[str, object]:
    vertices = sorted(set(incidence(edges)) - set(labels))
    by_pair = {edge.endpoints: edge for edge in edges}
    triangles: list[tuple[set[str], set[frozenset[str]]]] = []
    for triple in itertools.combinations(vertices, 3):
        triangle_pairs = {
            frozenset(pair) for pair in itertools.combinations(triple, 2)
        }
        if triangle_pairs <= set(by_pair):
            triangles.append((set(triple), triangle_pairs))
    if not triangles:
        return {"triangle_count": 0, "ordinary": True}
    if len(triangles) != 1:
        return {"triangle_count": len(triangles), "ordinary": False}
    vertices_set, triangle_pairs = triangles[0]
    local = [by_pair[pair] for pair in triangle_pairs]
    heads = Counter(vertex for edge in local for vertex in edge.arrowheads)
    external = [
        edge
        for edge in edges
        if edge.endpoints not in triangle_pairs
        and len(edge.endpoints & vertices_set) == 1
    ]
    ordinary = (
        sorted(heads.values()) == [2]
        and sum(bool(edge.arrowheads) for edge in local) == 2
        and all(not edge.arrowheads for edge in external)
    )
    return {
        "triangle_count": 1,
        "ordinary": ordinary,
        "vertices": sorted(vertices_set),
    }


def ordinary_triangle_quotient(
    edges: Sequence[MixedEdge], labels: Mapping[str, int]
) -> list[MixedEdge]:
    """Forget only the arrowheads changed by the ordinary T operation.

    This is intentionally undefined for a nonordinary triangle.  It is not
    the historical operation that blindly erases every triangle arrowhead.
    """

    status = ordinary_triangle_status(edges, labels)
    if status["triangle_count"] == 0:
        return list(edges)
    if status["triangle_count"] != 1 or not status["ordinary"]:
        raise ValueError("ordinary T quotient requested for a nonordinary triangle")
    vertices = set(status["vertices"])
    triangle_pairs = {
        frozenset(pair) for pair in itertools.combinations(vertices, 2)
    }
    return [
        MixedEdge(edge.endpoints, frozenset())
        if edge.endpoints in triangle_pairs
        else edge
        for edge in edges
    ]


def canonical_mixed_code(
    edges: Sequence[MixedEdge], labels: Mapping[str, int]
) -> tuple[tuple[tuple[object, ...], ...], tuple[tuple[int, int, tuple[int, ...]], ...]]:
    """Canonical labelled mixed-graph code by refinement/individualization."""

    vertices = sorted({vertex for edge in edges for vertex in edge.endpoints})
    local = incidence(edges)
    initial: dict[tuple[object, ...], list[str]] = defaultdict(list)
    for vertex in vertices:
        initial[("L", labels[vertex]) if vertex in labels else ("I",)].append(vertex)
    cells = tuple(
        tuple(sorted(initial[colour])) for colour in sorted(initial, key=repr)
    )

    def refine(partition: tuple[tuple[str, ...], ...]):
        while True:
            cell_of = {
                vertex: index
                for index, cell in enumerate(partition)
                for vertex in cell
            }
            updated = []
            changed = False
            for cell in partition:
                buckets: dict[tuple[object, ...], list[str]] = defaultdict(list)
                for vertex in cell:
                    signature = tuple(
                        sorted(
                            Counter(
                                (
                                    int(vertex in edge.arrowheads),
                                    int(edge.other(vertex) in edge.arrowheads),
                                    cell_of[edge.other(vertex)],
                                )
                                for edge in local[vertex]
                            ).items()
                        )
                    )
                    buckets[signature].append(vertex)
                changed |= len(buckets) > 1
                for signature in sorted(buckets, key=repr):
                    updated.append(tuple(sorted(buckets[signature])))
            partition = tuple(updated)
            if not changed:
                return partition

    def leaf_code(partition: tuple[tuple[str, ...], ...]):
        order = tuple(cell[0] for cell in partition)
        index = {vertex: position for position, vertex in enumerate(order)}
        colours = tuple(
            ("L", labels[vertex]) if vertex in labels else ("I",)
            for vertex in order
        )
        encoded = []
        for edge in edges:
            left, right = sorted(index[vertex] for vertex in edge.endpoints)
            heads = tuple(sorted(index[vertex] for vertex in edge.arrowheads))
            encoded.append((left, right, heads))
        return colours, tuple(sorted(encoded))

    def search(partition: tuple[tuple[str, ...], ...]):
        partition = refine(partition)
        if all(len(cell) == 1 for cell in partition):
            return leaf_code(partition)
        split = next(index for index, cell in enumerate(partition) if len(cell) > 1)
        results = []
        for chosen in partition[split]:
            remainder = tuple(
                vertex for vertex in partition[split] if vertex != chosen
            )
            results.append(
                search(
                    partition[:split]
                    + ((chosen,), remainder)
                    + partition[split + 1 :]
                )
            )
        return min(results)

    return search(cells)


def serialize_edges(edges: Sequence[MixedEdge]) -> list[dict[str, list[str]]]:
    return [
        {
            "endpoints": sorted(edge.endpoints),
            "arrowheads": sorted(edge.arrowheads),
        }
        for edge in sorted(
            edges,
            key=lambda edge: (sorted(edge.endpoints), sorted(edge.arrowheads)),
        )
    ]
