#!/usr/bin/env python3
"""Independent graph and JC algebra primitives for the final hard-cover audit.

This module imports no producer code and no earlier clean-room engine.  The
only project inputs it accepts are the frozen machine-readable primitive-core
and support encodings and the seven invariant templates.  In particular,
hard-cover topology identifiers are never used to select an invariant.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations, permutations, product
import json
import math
from typing import Iterable, Iterator, Mapping, Sequence


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def stable_hash(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def natural(label: str) -> tuple[str, int, str]:
    prefix, _, suffix = label.rpartition("_")
    return prefix, int(suffix) if suffix.isdigit() else -1, label


def weak_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


@dataclass(frozen=True)
class RootedGraph:
    root: int
    labels: tuple[tuple[int, str], ...]
    arcs: tuple[tuple[int, int], ...]

    @property
    def label_map(self) -> dict[int, str]:
        return dict(self.labels)

    @property
    def vertices(self) -> tuple[int, ...]:
        values = {self.root, *dict(self.labels)}
        for u, v in self.arcs:
            values.add(u)
            values.add(v)
        return tuple(sorted(values))

    def degrees(self) -> tuple[dict[int, int], dict[int, int]]:
        indegree = {v: 0 for v in self.vertices}
        outdegree = {v: 0 for v in self.vertices}
        for u, v in self.arcs:
            outdegree[u] += 1
            indegree[v] += 1
        return indegree, outdegree


@dataclass(frozen=True, order=True)
class MixedEdge:
    u: int
    v: int
    head_u: int = 0
    head_v: int = 0

    @classmethod
    def make(cls, u: int, v: int, heads: Iterable[int] = ()) -> "MixedEdge":
        marked = set(heads)
        if u < v:
            return cls(u, v, int(u in marked), int(v in marked))
        return cls(v, u, int(v in marked), int(u in marked))

    def endpoints(self) -> tuple[int, int]:
        return self.u, self.v

    def heads(self) -> frozenset[int]:
        return frozenset(
            vertex
            for vertex, marked in ((self.u, self.head_u), (self.v, self.head_v))
            if marked
        )

    def other(self, vertex: int) -> int:
        if vertex == self.u:
            return self.v
        if vertex == self.v:
            return self.u
        raise KeyError(vertex)

    def head_at(self, vertex: int) -> int:
        if vertex == self.u:
            return self.head_u
        if vertex == self.v:
            return self.head_v
        raise KeyError(vertex)


@dataclass(frozen=True)
class MixedGraph:
    labels: tuple[tuple[int, str], ...]
    edges: tuple[MixedEdge, ...]

    @property
    def label_map(self) -> dict[int, str]:
        return dict(self.labels)

    @property
    def vertices(self) -> tuple[int, ...]:
        values = set(dict(self.labels))
        for edge in self.edges:
            values.update(edge.endpoints())
        return tuple(sorted(values))

    def incidence(self) -> dict[int, list[MixedEdge]]:
        answer = {v: [] for v in self.vertices}
        for edge in self.edges:
            answer[edge.u].append(edge)
            answer[edge.v].append(edge)
        return answer

    def reticulations(self) -> frozenset[int]:
        counts = Counter(v for edge in self.edges for v in edge.heads())
        return frozenset(v for v, count in counts.items() if count == 2)


def rooted_validation(graph: RootedGraph) -> tuple[bool, tuple[str, ...]]:
    problems: list[str] = []
    indegree, outdegree = graph.degrees()
    labels = graph.label_map
    if len(set(graph.arcs)) != len(graph.arcs):
        problems.append("parallel arc")
    if len(labels) != len(set(labels.values())):
        problems.append("duplicate label")
    if (indegree[graph.root], outdegree[graph.root]) != (0, 2):
        problems.append("root bidegree")
    for vertex in graph.vertices:
        if vertex == graph.root:
            continue
        degree = indegree[vertex], outdegree[vertex]
        if vertex in labels:
            if degree != (1, 0):
                problems.append(f"leaf {labels[vertex]} bidegree {degree}")
        elif degree not in {(1, 2), (2, 1)}:
            problems.append(f"internal {vertex} bidegree {degree}")
    children: dict[int, list[int]] = defaultdict(list)
    for u, v in graph.arcs:
        children[u].append(v)
    work = dict(indegree)
    queue = deque(sorted(v for v in graph.vertices if work[v] == 0))
    visited = []
    while queue:
        vertex = queue.popleft()
        visited.append(vertex)
        for child in children[vertex]:
            work[child] -= 1
            if work[child] == 0:
                queue.append(child)
    if len(visited) != len(graph.vertices):
        problems.append("directed cycle")
    reached = {graph.root}
    queue = deque((graph.root,))
    while queue:
        vertex = queue.popleft()
        for child in children[vertex]:
            if child not in reached:
                reached.add(child)
                queue.append(child)
    if reached != set(graph.vertices):
        problems.append("not root reachable")
    return not problems, tuple(problems)


def root_is_lsa(graph: RootedGraph) -> bool:
    labelled = set(graph.label_map)
    children: dict[int, list[int]] = defaultdict(list)
    for u, v in graph.arcs:
        children[u].append(v)
    for omitted in graph.vertices:
        if omitted == graph.root:
            continue
        reached = {graph.root}
        queue = deque((graph.root,))
        while queue:
            vertex = queue.popleft()
            for child in children[vertex]:
                if child != omitted and child not in reached:
                    reached.add(child)
                    queue.append(child)
        if not (labelled & reached):
            return False
    return True


def rooted_tree_child(graph: RootedGraph) -> bool:
    indegree, outdegree = graph.degrees()
    labels = set(graph.label_map)
    children: dict[int, list[int]] = defaultdict(list)
    for u, v in graph.arcs:
        children[u].append(v)
    ordinary_children = labels | {
        v for v in graph.vertices if (indegree[v], outdegree[v]) == (1, 2)
    }
    return all(
        any(child in ordinary_children for child in children[v])
        for v in graph.vertices
        if outdegree[v]
    )


def internal_vertex_audit(graph: RootedGraph) -> dict[str, object]:
    """Audit the rooted tree-child clauses without ever testing a leaf.

    The quantifier is over vertices of positive outdegree.  This explicit
    ledger guards against the review bug in which leaves were incorrectly
    required to possess a child.
    """
    indegree, outdegree = graph.degrees()
    labels = set(graph.label_map)
    children: dict[int, list[int]] = defaultdict(list)
    for u, v in graph.arcs:
        children[u].append(v)
    tree_or_leaf = labels | {
        v for v in graph.vertices if (indegree[v], outdegree[v]) == (1, 2)
    }
    internals = tuple(v for v in graph.vertices if outdegree[v] > 0)
    leaves = tuple(v for v in graph.vertices if outdegree[v] == 0)
    missing_good_child = tuple(
        v for v in internals if not any(child in tree_or_leaf for child in children[v])
    )
    reticulation_to_reticulation = tuple(
        (u, v)
        for u, v in graph.arcs
        if indegree[u] == 2 and indegree[v] == 2
    )
    return {
        "internal_vertex_count": len(internals),
        "leaf_count": len(leaves),
        "checked_vertex_count": len(internals),
        "leaf_vertices_excluded": len(leaves) > 0 and not (set(leaves) & set(internals)),
        "internal_vertices_without_tree_or_leaf_child": list(missing_good_child),
        "reticulation_to_reticulation_arcs": [list(edge) for edge in reticulation_to_reticulation],
        "passes": not missing_good_child and not reticulation_to_reticulation,
    }


def sd0(graph: RootedGraph) -> MixedGraph:
    valid, problems = rooted_validation(graph)
    if not valid:
        raise ValueError(problems)
    indegree, _ = graph.degrees()
    edges = [
        MixedEdge.make(u, v, (v,) if indegree[v] == 2 else ())
        for u, v in graph.arcs
    ]
    incident = [e for e in edges if graph.root in e.endpoints()]
    if len(incident) != 2:
        raise ValueError("root incidence")
    kept = [e for e in edges if graph.root not in e.endpoints()]
    left, right = incident
    a, b = left.other(graph.root), right.other(graph.root)
    if a == b:
        raise ValueError("root suppression loop")
    heads = set()
    if left.head_at(a):
        heads.add(a)
    if right.head_at(b):
        heads.add(b)
    kept.append(MixedEdge.make(a, b, heads))
    if len(kept) != len(set(kept)):
        raise ValueError("root suppression parallel edge")
    mixed = MixedGraph(graph.labels, tuple(sorted(kept)))
    incidence = mixed.incidence()
    labels = mixed.label_map
    if any(len(incidence[v]) != (1 if v in labels else 3) for v in mixed.vertices):
        raise ValueError("not simple binary after root suppression")
    if any(len(edge.heads()) > 1 for edge in mixed.edges):
        raise ValueError("bidirected edge")
    for reticulation in mixed.reticulations():
        if sum(edge.head_at(reticulation) for edge in incidence[reticulation]) != 2:
            raise ValueError("reticulation arrowheads lost")
    return mixed


def mixed_local_strong(graph: MixedGraph) -> bool:
    incidence = graph.incidence()
    for edge in graph.edges:
        heads = edge.heads()
        if len(heads) != 1:
            continue
        head = next(iter(heads))
        tail = edge.other(head)
        if sum(not local.heads() for local in incidence[tail]) != 2:
            return False
    return True


def underlying_triangles(graph: MixedGraph) -> tuple[tuple[int, int, int], ...]:
    adjacency = {v: set() for v in graph.vertices}
    for edge in graph.edges:
        adjacency[edge.u].add(edge.v)
        adjacency[edge.v].add(edge.u)
    answer = []
    for a, b, c in combinations(graph.vertices, 3):
        if b in adjacency[a] and c in adjacency[a] and c in adjacency[b]:
            answer.append((a, b, c))
    return tuple(answer)


def t_quotient(graph: MixedGraph) -> MixedGraph:
    triangles = underlying_triangles(graph)
    if not triangles:
        return graph
    if len(triangles) != 1:
        raise ValueError("multiple triangles")
    triangle = set(triangles[0])
    edges = [
        MixedEdge.make(edge.u, edge.v)
        if edge.u in triangle and edge.v in triangle
        else edge
        for edge in graph.edges
    ]
    return MixedGraph(graph.labels, tuple(sorted(edges)))


def _wl_colours(graph: MixedGraph) -> dict[int, int]:
    labels = graph.label_map
    incidence = graph.incidence()
    reticulations = graph.reticulations()
    signatures: dict[int, object] = {
        vertex: (
            ("L", labels[vertex])
            if vertex in labels
            else (("R",) if vertex in reticulations else ("I",))
        )
        for vertex in graph.vertices
    }
    while True:
        enriched = {}
        for vertex in graph.vertices:
            neighbours = []
            for edge in incidence[vertex]:
                other = edge.other(vertex)
                neighbours.append(
                    (edge.head_at(vertex), edge.head_at(other), signatures[other])
                )
            enriched[vertex] = (signatures[vertex], tuple(sorted(neighbours, key=repr)))
        palette = {
            signature: index
            for index, signature in enumerate(sorted(set(enriched.values()), key=repr))
        }
        new = {vertex: palette[enriched[vertex]] for vertex in graph.vertices}
        if all(
            (signatures[a] == signatures[b]) == (new[a] == new[b])
            for a in graph.vertices
            for b in graph.vertices
        ):
            return new
        signatures = new


def canonical_mixed(graph: MixedGraph) -> tuple[str, dict[int, int]]:
    """Exact labelled mixed-graph canonical form and raw-to-canonical map."""
    labels = graph.label_map
    colours = _wl_colours(graph)
    cells: dict[int, list[int]] = defaultdict(list)
    for vertex, colour in colours.items():
        cells[colour].append(vertex)
    ordered_cells = [tuple(sorted(cells[colour])) for colour in sorted(cells)]
    best: tuple | None = None
    best_map: dict[int, int] | None = None
    for moved_cells in product(*(tuple(permutations(cell)) for cell in ordered_cells)):
        order = tuple(vertex for cell in moved_cells for vertex in cell)
        mapping = {vertex: index for index, vertex in enumerate(order)}
        encoded_labels = tuple(sorted((mapping[v], label) for v, label in labels.items()))
        encoded_edges = []
        for edge in graph.edges:
            heads = {mapping[v] for v in edge.heads()}
            encoded_edges.append(MixedEdge.make(mapping[edge.u], mapping[edge.v], heads))
        code = (encoded_labels, tuple(sorted(encoded_edges)))
        if best is None or code < best:
            best = code
            best_map = mapping
    if best is None or best_map is None:
        raise AssertionError("empty canonicalization")
    return repr(best), best_map


def canonical_mixed_with_multiplicity(
    graph: MixedGraph,
) -> tuple[str, dict[int, int], int]:
    """Canonical code, one transport, and exact automorphism multiplicity.

    The number of raw-to-canonical labellings attaining the least code is the
    labelled mixed-graph automorphism-group order.  This is deliberately
    recomputed rather than read from a producer transport record.
    """
    labels = graph.label_map
    colours = _wl_colours(graph)
    cells: dict[int, list[int]] = defaultdict(list)
    for vertex, colour in colours.items():
        cells[colour].append(vertex)
    ordered_cells = [tuple(sorted(cells[colour])) for colour in sorted(cells)]
    best: tuple | None = None
    best_map: dict[int, int] | None = None
    multiplicity = 0
    for moved_cells in product(*(tuple(permutations(cell)) for cell in ordered_cells)):
        order = tuple(vertex for cell in moved_cells for vertex in cell)
        mapping = {vertex: index for index, vertex in enumerate(order)}
        encoded_labels = tuple(sorted((mapping[v], label) for v, label in labels.items()))
        encoded_edges = []
        for edge in graph.edges:
            heads = {mapping[v] for v in edge.heads()}
            encoded_edges.append(MixedEdge.make(mapping[edge.u], mapping[edge.v], heads))
        code = (encoded_labels, tuple(sorted(encoded_edges)))
        if best is None or code < best:
            best = code
            best_map = mapping
            multiplicity = 1
        elif code == best:
            multiplicity += 1
    if best is None or best_map is None:
        raise AssertionError("empty canonicalization")
    return repr(best), best_map, multiplicity


def biconnected_blocks(graph: MixedGraph) -> tuple[frozenset[int], ...]:
    adjacency = {v: set() for v in graph.vertices}
    for edge in graph.edges:
        adjacency[edge.u].add(edge.v)
        adjacency[edge.v].add(edge.u)
    discovery: dict[int, int] = {}
    low: dict[int, int] = {}
    parent: dict[int, int | None] = {}
    stack: list[tuple[int, int]] = []
    blocks: list[frozenset[int]] = []
    clock = 0

    def dfs(vertex: int) -> None:
        nonlocal clock
        clock += 1
        discovery[vertex] = low[vertex] = clock
        for other in sorted(adjacency[vertex]):
            edge = tuple(sorted((vertex, other)))
            if other not in discovery:
                parent[other] = vertex
                stack.append(edge)
                dfs(other)
                low[vertex] = min(low[vertex], low[other])
                if low[other] >= discovery[vertex]:
                    vertices = set()
                    while stack:
                        popped = stack.pop()
                        vertices.update(popped)
                        if popped == edge:
                            break
                    blocks.append(frozenset(vertices))
            elif other != parent.get(vertex) and discovery[other] < discovery[vertex]:
                low[vertex] = min(low[vertex], discovery[other])
                stack.append(edge)

    for vertex in graph.vertices:
        if vertex not in discovery:
            parent[vertex] = None
            dfs(vertex)
            if stack:
                vertices = {v for edge in stack for v in edge}
                blocks.append(frozenset(vertices))
                stack.clear()
    return tuple(blocks)


def level_at_most_two(graph: MixedGraph) -> bool:
    reticulations = graph.reticulations()
    return all(len(block & reticulations) <= 2 for block in biconnected_blocks(graph))


def class_audit(graph: RootedGraph) -> dict[str, object]:
    valid, problems = rooted_validation(graph)
    if not valid:
        return {"rooted_valid": False, "problems": list(problems)}
    try:
        mixed = sd0(graph)
    except ValueError as error:
        return {"rooted_valid": True, "sd0_valid": False, "problems": [str(error)]}
    internal = internal_vertex_audit(graph)
    return {
        "rooted_valid": True,
        "root_is_lsa": root_is_lsa(graph),
        "rooted_tree_child": rooted_tree_child(graph),
        "internal_vertex_audit": internal,
        "sd0_valid": True,
        "standard_strong_local": mixed_local_strong(mixed),
        "level_at_most_two": level_at_most_two(mixed),
        "triangle_count": len(underlying_triangles(mixed)),
    }


def source_and_sinks(arcs: Sequence[tuple[str, str]]) -> tuple[str, tuple[str, ...]]:
    indegree = Counter(v for _, v in arcs)
    outdegree = Counter(u for u, _ in arcs)
    vertices = {v for arc in arcs for v in arc}
    sources = sorted(v for v in vertices if indegree[v] == 0)
    if len(sources) != 1:
        raise AssertionError(sources)
    sinks = tuple(sorted(v for v in vertices if indegree[v] == 2 and outdegree[v] == 0))
    return sources[0], sinks


def build_graph(
    core_arcs: Sequence[tuple[str, str]],
    words: Sequence[Sequence[str]],
    sink_labels: Mapping[str, str],
) -> RootedGraph:
    ids: dict[tuple, int] = {}

    def vertex(key: tuple) -> int:
        if key not in ids:
            ids[key] = len(ids)
        return ids[key]

    vertices = sorted({name for arc in core_arcs for name in arc})
    for name in vertices:
        vertex(("core", name))
    source, _ = source_and_sinks(core_arcs)
    root = vertex(("root",))
    incoming_leaf = vertex(("leaf", "INCOMING"))
    labels = {incoming_leaf: "INCOMING"}
    directed: list[tuple[int, int]] = [
        (root, vertex(("core", source))),
        (root, incoming_leaf),
    ]
    for arc_index, ((tail, head), word) in enumerate(zip(core_arcs, words)):
        prior = vertex(("core", tail))
        for position, label in enumerate(word):
            subdivision = vertex(("subdivision", arc_index, position))
            leaf = vertex(("leaf", label))
            labels[leaf] = label
            directed.extend(((prior, subdivision), (subdivision, leaf)))
            prior = subdivision
        directed.append((prior, vertex(("core", head))))
    for sink, label in sorted(sink_labels.items()):
        leaf = vertex(("sink_leaf", sink))
        labels[leaf] = label
        directed.append((vertex(("core", sink)), leaf))
    return RootedGraph(root, tuple(sorted(labels.items())), tuple(directed))


def relabel(graph: RootedGraph, mapping: Mapping[str, str]) -> RootedGraph:
    return RootedGraph(
        graph.root,
        tuple(sorted((vertex, mapping.get(label, label)) for vertex, label in graph.labels)),
        graph.arcs,
    )


@dataclass(frozen=True)
class Completion:
    core_id: str
    selected_labels: tuple[str, ...]
    dummy_labels: tuple[str, ...]
    selected_sink_mask: int
    repair_index: int | None
    words: tuple[tuple[str, ...], ...]
    graph: RootedGraph
    incoming_selected: bool


def core_rows(core_payload: dict) -> tuple[dict, ...]:
    rows = []
    for row in core_payload["cores"]:
        rows.append({
            "id": row["id"],
            "arcs": tuple((str(edge["tail"]), str(edge["head"])) for edge in row["segments"]),
            "repairs": tuple(tuple(int(value) for value in repair) for repair in row["minimum_repairs"]),
        })
    return tuple(rows)


def completions(core_payload: dict, selected_total: int, incoming_selected: bool) -> Iterator[Completion]:
    """Enumerate selected completions in either structural-incoming mode."""
    selected_outgoing = selected_total - 1 if incoming_selected else selected_total
    for core in core_rows(core_payload):
        arcs = core["arcs"]
        _, sinks = source_and_sinks(arcs)
        for sink_mask in range(1 << len(sinks)):
            selected_sinks = {
                sink for index, sink in enumerate(sinks) if sink_mask & (1 << index)
            }
            ordinary = selected_outgoing - len(selected_sinks)
            if ordinary < 0:
                continue
            for counts in weak_compositions(ordinary, len(arcs)):
                labels = iter(f"O_{index}" for index in range(ordinary))
                selected_words = tuple(
                    tuple(next(labels) for _ in range(count)) for count in counts
                )
                indexed_repairs = (
                    ((None, ()),)
                    if core["id"] == "cycle"
                    else tuple(enumerate(core["repairs"]))
                )
                for repair_index, repair in indexed_repairs:
                    words = [list(word) for word in selected_words]
                    dummies = [] if incoming_selected else ["INCOMING"]
                    for arc_index in repair:
                        if not words[arc_index]:
                            dummy = f"D_REPAIR_{repair_index}_{arc_index}"
                            words[arc_index].append(dummy)
                            dummies.append(dummy)
                    sink_labels: dict[str, str] = {}
                    for index, sink in enumerate(sinks):
                        if sink in selected_sinks:
                            sink_labels[sink] = f"SINK_{index}"
                        else:
                            dummy = f"D_SINK_{index}"
                            sink_labels[sink] = dummy
                            dummies.append(dummy)
                    selected = tuple(sorted(
                        [label for word in selected_words for label in word]
                        + [sink_labels[sink] for sink in selected_sinks]
                    ))
                    full_words = tuple(tuple(word) for word in words)
                    yield Completion(
                        core["id"], selected, tuple(sorted(dummies)), sink_mask,
                        repair_index, full_words,
                        build_graph(arcs, full_words, sink_labels), incoming_selected,
                    )


def completion_retains_core(completion: Completion, core_payload: dict) -> bool:
    if not completion.incoming_selected:
        return False
    core = {row["id"]: row for row in core_rows(core_payload)}[completion.core_id]
    _, sinks = source_and_sinks(core["arcs"])
    all_sinks = completion.selected_sink_mask == (1 << len(sinks)) - 1
    occupied = {
        index
        for index, word in enumerate(completion.words)
        if any(not label.startswith("D_") for label in word)
    }
    return all_sinks and any(set(repair) <= occupied for repair in core["repairs"])


Descriptor = tuple[int, tuple[tuple[int, ...], ...]]
Poly = dict[tuple[int, ...], int]


def raw_descriptor(graph: RootedGraph, ordered_labels: Sequence[str]) -> Descriptor:
    indegree, _ = graph.degrees()
    reticulations = tuple(sorted(v for v in graph.vertices if indegree[v] == 2))
    incoming = {
        r: tuple(index for index, (_, head) in enumerate(graph.arcs) if head == r)
        for r in reticulations
    }
    displays = tuple(product((0, 1), repeat=len(reticulations)))
    signatures = [[0] * len(displays) for _ in graph.arcs]
    label_index = {label: index for index, label in enumerate(ordered_labels)}
    all_leaves = set(graph.label_map)
    for display_index, choices in enumerate(displays):
        removed = {
            incoming[r][1 - choice] for r, choice in zip(reticulations, choices)
        }
        active = tuple(index for index in range(len(graph.arcs)) if index not in removed)
        children: dict[int, list[int]] = defaultdict(list)
        for index in active:
            u, v = graph.arcs[index]
            children[u].append(v)
        memo: dict[int, int] = {}

        def descendants(vertex: int) -> int:
            if vertex in memo:
                return memo[vertex]
            if vertex in all_leaves:
                label = graph.label_map[vertex]
                value = (1 << label_index[label]) if label in label_index else 0
            else:
                value = 0
                for child in children[vertex]:
                    value |= descendants(child)
            memo[vertex] = value
            return value

        for edge_index in active:
            signatures[edge_index][display_index] = descendants(graph.arcs[edge_index][1])
    return len(reticulations), tuple(tuple(row) for row in signatures if any(row))


def canonicalize_descriptor(reticulations: int, signatures: Iterable[Sequence[int]]) -> Descriptor:
    rows = tuple(sorted(set(tuple(row) for row in signatures if any(row))))
    if not reticulations:
        return 0, rows
    displays = tuple(product((0, 1), repeat=reticulations))
    index = {bits: position for position, bits in enumerate(displays)}
    candidates = []
    for permutation in permutations(range(reticulations)):
        for flips in product((0, 1), repeat=reticulations):
            moved_rows = []
            for row in rows:
                moved = [0] * len(displays)
                for old_position, old_bits in enumerate(displays):
                    new_bits = tuple(
                        old_bits[permutation[j]] ^ flips[j]
                        for j in range(reticulations)
                    )
                    moved[index[new_bits]] = row[old_position]
                moved_rows.append(tuple(moved))
            candidates.append((reticulations, tuple(sorted(set(moved_rows)))))
    return min(candidates)


def ordered_quartet_deck(graph: RootedGraph, labels: Sequence[str]) -> dict[tuple[int, int, int, int], Descriptor]:
    reticulations, rows = raw_descriptor(graph, labels)
    answer = {}
    for ordered in permutations(range(len(labels)), 4):
        restricted = []
        for row in rows:
            moved_row = []
            for mask in row:
                moved_mask = 0
                for new_index, old_index in enumerate(ordered):
                    if mask & (1 << old_index):
                        moved_mask |= 1 << new_index
                moved_row.append(moved_mask)
            restricted.append(tuple(moved_row))
        answer[ordered] = canonicalize_descriptor(reticulations, restricted)
    return answer


def quartet_descriptor(graph: RootedGraph, labels: Sequence[str], quartet: Sequence[int]) -> Descriptor:
    reticulations, rows = raw_descriptor(graph, labels)
    restricted = []
    for row in rows:
        moved_row = []
        for mask in row:
            moved_mask = 0
            for new_index, old_index in enumerate(quartet):
                if mask & (1 << old_index):
                    moved_mask |= 1 << new_index
            moved_row.append(moved_mask)
        restricted.append(tuple(moved_row))
    return canonicalize_descriptor(reticulations, restricted)


@lru_cache(maxsize=1)
def jc_representatives() -> tuple[tuple[int, int, int, int], ...]:
    colour_maps = [(0, *row) for row in permutations((1, 2, 3))]

    def canon(row: tuple[int, ...]) -> tuple[int, ...]:
        return min(tuple(mapping[value] for value in row) for mapping in colour_maps)

    rows = sorted({
        canon(row)
        for row in product(range(4), repeat=4)
        if row[0] ^ row[1] ^ row[2] ^ row[3] == 0
    })
    if len(rows) != 15:
        raise AssertionError(len(rows))
    return tuple(rows)


def invariant_orbit(payload: dict) -> tuple[tuple[tuple[tuple[int, ...], int], ...], ...]:
    reps = jc_representatives()
    rep_index = {row: index for index, row in enumerate(reps)}
    colour_maps = [(0, *row) for row in permutations((1, 2, 3))]

    def canon(row: tuple[int, ...]) -> tuple[int, ...]:
        return min(tuple(mapping[value] for value in row) for mapping in colour_maps)

    templates = []
    for template in payload["templates"]:
        templates.append(tuple((tuple(int(i) for i in monomial), int(coefficient)) for coefficient, monomial in template))
    templates.append(tuple((tuple(int(i) + 1 for i in monomial), int(coefficient)) for coefficient, monomial in payload["seventh"]))
    orbit = set()
    for template in templates:
        for leaf_permutation in permutations(range(4)):
            terms: dict[tuple[int, ...], int] = defaultdict(int)
            for monomial, coefficient in template:
                moved = []
                for coordinate in monomial:
                    assignment = reps[coordinate]
                    transported = tuple(
                        assignment[leaf_permutation[index]] for index in range(4)
                    )
                    moved.append(rep_index[canon(transported)])
                terms[tuple(sorted(moved))] += coefficient
            normalized = tuple(sorted((m, c) for m, c in terms.items() if c))
            if normalized and normalized[0][1] < 0:
                normalized = tuple((m, -c) for m, c in normalized)
            orbit.add(normalized)
    answer = tuple(sorted(orbit))
    if len(answer) != 84:
        raise AssertionError(("invariant orbit", len(answer)))
    return answer


def poly_add(left: Poly, right: Poly, scale: int = 1) -> Poly:
    answer = dict(left)
    for monomial, coefficient in right.items():
        value = answer.get(monomial, 0) + scale * coefficient
        if value:
            answer[monomial] = value
        else:
            answer.pop(monomial, None)
    return answer


def poly_mul(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return {}
    answer: dict[tuple[int, ...], int] = defaultdict(int)
    for a, ca in left.items():
        for b, cb in right.items():
            answer[tuple(x + y for x, y in zip(a, b))] += ca * cb
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def poly_const(value: int, variables: int) -> Poly:
    return {} if not value else {(0,) * variables: value}


@lru_cache(maxsize=8192)
def coordinate_polynomials(descriptor: Descriptor) -> tuple[Poly, ...]:
    reticulations, rows = descriptor
    displays = tuple(product((0, 1), repeat=reticulations))
    variables = len(rows) + reticulations
    answer = []
    for assignment in jc_representatives():
        total: Poly = {}
        for display_index, choices in enumerate(displays):
            exponent = [0] * variables
            for variable, row in enumerate(rows):
                mask = row[display_index]
                state = 0
                for leaf_index, character in enumerate(assignment):
                    if mask & (1 << leaf_index):
                        state ^= character
                if state:
                    exponent[variable] = 1
            term: Poly = {tuple(exponent): 1}
            for reticulation, choice in enumerate(choices):
                variable = len(rows) + reticulation
                unit = [0] * variables
                unit[variable] = 1
                factor = (
                    {tuple(unit): 1}
                    if choice == 0
                    else {(0,) * variables: 1, tuple(unit): -1}
                )
                term = poly_mul(term, factor)
            total = poly_add(total, term)
        answer.append(total)
    return tuple(answer)


@lru_cache(maxsize=32768)
def pullback(descriptor: Descriptor, invariant: tuple[tuple[tuple[int, ...], int], ...]) -> Poly:
    coordinates = coordinate_polynomials(descriptor)
    variables = len(descriptor[1]) + descriptor[0]
    cache: dict[tuple[int, ...], Poly] = {(): poly_const(1, variables)}

    def monomial(indices: tuple[int, ...]) -> Poly:
        if indices not in cache:
            cache[indices] = poly_mul(monomial(indices[:-1]), coordinates[indices[-1]])
        return cache[indices]

    answer: Poly = {}
    for indices, coefficient in invariant:
        answer = poly_add(answer, monomial(tuple(indices)), coefficient)
    return answer


def exact_poly_hash(poly: Poly) -> str:
    return hashlib.sha256(repr(tuple(sorted(poly.items()))).encode()).hexdigest()


def primitive_poly(poly: Poly) -> tuple[tuple[tuple[int, ...], int], ...]:
    if not poly:
        return ()
    content = 0
    for coefficient in poly.values():
        content = math.gcd(content, abs(coefficient))
    reduced = {m: c // content for m, c in poly.items()}
    first = min(reduced)
    if reduced[first] < 0:
        reduced = {m: -c for m, c in reduced.items()}
    return tuple(sorted(reduced.items()))


def coordinate_values_mod(descriptor: Descriptor, seed: int, prime: int = 2_147_483_647) -> tuple[int, ...]:
    reticulations, rows = descriptor
    displays = tuple(product((0, 1), repeat=reticulations))
    values = []
    for index in range(len(rows) + reticulations):
        value = (seed + 37 * index + 11) % prime
        values.append(2 if value in (0, 1) else value)
    edges = values[: len(rows)]
    inheritance = values[len(rows):]
    answer = []
    for assignment in jc_representatives():
        total = 0
        for display_index, choices in enumerate(displays):
            term = 1
            for reticulation, choice in enumerate(choices):
                lam = inheritance[reticulation]
                term = term * (lam if choice == 0 else 1 - lam) % prime
            for edge_value, row in zip(edges, rows):
                state = 0
                for leaf_index, character in enumerate(assignment):
                    if row[display_index] & (1 << leaf_index):
                        state ^= character
                if state:
                    term = term * edge_value % prime
            total = (total + term) % prime
        answer.append(total)
    return tuple(answer)


def invariant_value_mod(coordinates: Sequence[int], invariant, prime: int = 2_147_483_647) -> int:
    total = 0
    for monomial, coefficient in invariant:
        term = coefficient % prime
        for index in monomial:
            term = term * coordinates[index] % prime
        total = (total + term) % prime
    return total


def descriptor_bits_exact(descriptor: Descriptor, invariants) -> int:
    values = tuple(coordinate_values_mod(descriptor, seed) for seed in (101, 1009, 10007))
    bits = 0
    for index, invariant in enumerate(invariants):
        if any(invariant_value_mod(row, invariant) for row in values):
            bits |= 1 << index
        elif pullback(descriptor, invariant):
            bits |= 1 << index
    return bits


def bernstein_sign(poly_expression, symbols, max_elevation: int = 5) -> dict[str, object]:
    import sympy as sp

    polynomial = sp.Poly(poly_expression, *symbols, domain=sp.QQ)
    degrees_all = polynomial.degree_list()
    used = tuple(index for index, degree in enumerate(degrees_all) if degree)
    if not used:
        value = Fraction(polynomial.LC())
        return {
            "certified": value != 0,
            "sign": 1 if value > 0 else -1 if value < 0 else 0,
            "constant": str(value),
            "used_variables": [],
        }
    power_coefficients = {
        tuple(exponents[index] for index in used): Fraction(coefficient)
        for exponents, coefficient in polynomial.terms()
    }
    native = tuple(degrees_all[index] for index in used)
    for elevation in range(max_elevation + 1):
        degrees = tuple(degree + elevation for degree in native)
        coefficients = []
        for bernstein_index in product(*(range(degree + 1) for degree in degrees)):
            value = Fraction(0)
            for powers, coefficient in power_coefficients.items():
                if all(power <= index for power, index in zip(powers, bernstein_index)):
                    ratio = Fraction(1)
                    for index, power, degree in zip(bernstein_index, powers, degrees):
                        ratio *= Fraction(math.comb(index, power), math.comb(degree, power))
                    value += coefficient * ratio
            coefficients.append(value)
        positive = all(value >= 0 for value in coefficients) and any(value > 0 for value in coefficients)
        negative = all(value <= 0 for value in coefficients) and any(value < 0 for value in coefficients)
        if positive or negative:
            return {
                "certified": True,
                "sign": 1 if positive else -1,
                "used_variables": list(used),
                "degrees": list(degrees),
                "elevation": elevation,
                "coefficient_count": len(coefficients),
                "minimum": str(min(coefficients)),
                "maximum": str(max(coefficients)),
            }
    return {
        "certified": False,
        "used_variables": list(used),
        "native_degrees": list(native),
        "max_elevation": max_elevation,
    }


def independent_strict_sign(poly: Poly) -> dict[str, object]:
    if not poly:
        return {"certified": False, "reason": "zero"}
    coefficients = tuple(poly.values())
    if all(value >= 0 for value in coefficients) and any(value > 0 for value in coefficients):
        return {"certified": True, "sign": 1, "method": "power-coefficients"}
    if all(value <= 0 for value in coefficients) and any(value < 0 for value in coefficients):
        return {"certified": True, "sign": -1, "method": "power-coefficients"}
    import sympy as sp

    variables = len(next(iter(poly)))
    symbols = sp.symbols(f"z0:{variables}")
    expression = sp.Integer(0)
    for exponents, coefficient in poly.items():
        term = sp.Integer(coefficient)
        for symbol, exponent in zip(symbols, exponents):
            if exponent:
                term *= symbol ** exponent
        expression += term
    constant, factors = sp.factor_list(sp.expand(expression), *symbols)
    sign = 1 if constant > 0 else -1
    for factor, multiplicity in factors:
        proof = bernstein_sign(factor, symbols)
        if not proof.get("certified"):
            return {"certified": False, "reason": "factor sign unresolved"}
        if multiplicity % 2:
            sign *= int(proof["sign"])
    return {"certified": True, "sign": sign, "method": "factor-bernstein"}


def independent_sign_certificate(poly: Poly, max_elevation: int = 5) -> dict[str, object]:
    """Rebuild the complete factor/Bernstein proof instead of trusting a flag."""
    if not poly:
        return {"certified": False, "reason": "zero polynomial"}
    coefficients = tuple(poly.values())
    primitive_hash = hashlib.sha256(repr(primitive_poly(poly)).encode()).hexdigest()
    if all(value >= 0 for value in coefficients) and any(value > 0 for value in coefficients):
        return {
            "certified": True,
            "strict_sign": 1,
            "polynomial_sha256": primitive_hash,
            "term_count": len(poly),
            "factors": [],
            "method": "same-sign sparse power coefficients",
        }
    if all(value <= 0 for value in coefficients) and any(value < 0 for value in coefficients):
        return {
            "certified": True,
            "strict_sign": -1,
            "polynomial_sha256": primitive_hash,
            "term_count": len(poly),
            "factors": [],
            "method": "same-sign sparse power coefficients",
        }
    import sympy as sp

    variable_count = len(next(iter(poly)))
    symbols = sp.symbols(f"z0:{variable_count}")
    expression = sp.Integer(0)
    for exponents, coefficient in poly.items():
        term = sp.Integer(coefficient)
        for symbol, exponent in zip(symbols, exponents):
            if exponent:
                term *= symbol ** exponent
        expression += term
    expression = sp.expand(expression)
    constant, factors = sp.factor_list(expression, *symbols)
    reconstructed = sp.Integer(constant)
    sign = 1 if constant > 0 else -1
    rows = []
    for factor, multiplicity in factors:
        expanded = sp.expand(factor)
        reconstructed *= expanded ** multiplicity
        proof = bernstein_sign(expanded, symbols, max_elevation=max_elevation)
        row = {
            "expanded_sha256": hashlib.sha256(str(expanded).encode()).hexdigest(),
            "degree": int(sp.Poly(expanded, *symbols).total_degree()),
            "terms": len(sp.Poly(expanded, *symbols).terms()),
            "multiplicity": int(multiplicity),
            "proof": proof,
        }
        rows.append(row)
        if not proof.get("certified"):
            return {
                "certified": False,
                "polynomial_sha256": primitive_hash,
                "term_count": len(poly),
                "factors": rows,
                "factorization_exact": sp.expand(reconstructed - expression) == 0,
            }
        if multiplicity % 2:
            sign *= int(proof["sign"])
    return {
        "certified": True,
        "strict_sign": sign,
        "polynomial_sha256": primitive_hash,
        "term_count": len(poly),
        "factors": rows,
        "factorization_exact": sp.expand(reconstructed - expression) == 0,
        "method": "exact factorization plus Bernstein coefficients",
    }
