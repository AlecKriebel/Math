#!/usr/bin/env python3
"""Clean-room graph census for the non-four-port equality-anchor seeds.

This module deliberately contains its own finite graph grammar.  It does not
import the submitted atlas, any producer, a frozen theta/cycle certificate, or
the probe-input contract.  The only non-stdlib dependency is NetworkX, used
for exact finite graph isomorphism.

The computation is model-independent.  In particular, there are no Fourier,
Jacobian, rank, invariant, or parameter-domain calculations here.  A row is
retained precisely when its rooted graph pair has the exact labelled
semi-directed relation (ordinary-triangle equivalence included where it is
actually present), subject to the explicit primitive-seed convention that a
theta target with a marginalized distinguished incoming boundary is not a
fixed-full seed parent.  The excluded family is separately enumerated below;
graph isomorphism by itself does not eliminate it.
"""

from __future__ import annotations

import ast
import collections
import dataclasses
import hashlib
import itertools
import json
from typing import Any, Iterable, Iterator, Sequence

import networkx as nx


class IndependentUniverseError(RuntimeError):
    """A fail-closed error in the independent finite census."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IndependentUniverseError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


# Literal directed-core grammar.  Dictionary order is part of the target
# enumeration: cycle, theta0, theta1, theta2, theta3.
CORE_SPECS: dict[str, dict[str, tuple[Any, ...]]] = {
    "cycle": {
        "arcs": (("S", "X"), ("S", "X")),
        "reticulations": ("X",),
        "sinks": ("X",),
        "repairs": ((0,), (1,)),
    },
    "theta0": {
        "arcs": (
            ("S", "U"), ("S", "V"), ("U", "X"),
            ("V", "X"), ("U", "V"),
        ),
        "reticulations": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (3, 4)),
    },
    "theta1": {
        "arcs": (
            ("S", "U"), ("S", "X"), ("V", "X"),
            ("U", "V"), ("U", "V"),
        ),
        "reticulations": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (2, 4)),
    },
    "theta2": {
        "arcs": (
            ("S", "U"), ("S", "V"), ("U", "X0"),
            ("V", "X0"), ("U", "X1"), ("V", "X1"),
        ),
        "reticulations": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2, 3), (2, 5), (3, 4), (4, 5)),
    },
    "theta3": {
        "arcs": (
            ("S", "U"), ("S", "X0"), ("V", "X0"),
            ("U", "X1"), ("V", "X1"), ("U", "V"),
        ),
        "reticulations": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2,), (4,)),
    },
}


@dataclasses.dataclass(frozen=True)
class GraphRecord:
    core_id: str
    incoming_selected: bool
    repair_index: int | None
    selected_sink_mask: int
    words: tuple[tuple[object, ...], ...]
    graph: nx.DiGraph
    selected_labels: tuple[int, ...]
    dummy_labels: tuple[str, ...]


def weak_compositions(total: int, bins: int) -> Iterator[tuple[int, ...]]:
    require(total >= 0 and bins >= 1, "weak-composition domain")
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, bins - 1):
            yield (first,) + rest


def build_graph(
    core_id: str,
    words: tuple[tuple[object, ...], ...],
    sink_labels: dict[str, object],
    incoming_label: object,
) -> nx.DiGraph:
    """Realize one rooted completion using literal, stable node names."""

    spec = CORE_SPECS[core_id]
    arcs = spec["arcs"]
    require(len(words) == len(arcs), f"word/arcs:{core_id}")
    graph = nx.DiGraph(core_id=core_id)

    # Node insertion order is deliberately irrelevant: graph_payload sorts by
    # repr.  Sorting here makes debugging reproducible across hash seeds.
    core_nodes = sorted({name for arc in arcs for name in arc})
    for name in core_nodes:
        graph.add_node(
            ("core", name),
            role="retic" if name in spec["reticulations"] else "tree",
            label=None,
            dummy=False,
        )

    root = ("root",)
    incoming = ("leaf", "INCOMING")
    selected = isinstance(incoming_label, int)
    graph.add_node(root, role="root", label=None, dummy=False)
    graph.add_node(
        incoming,
        role="leaf",
        label=incoming_label if selected else None,
        dummy=not selected,
        dummy_name=None if selected else str(incoming_label),
    )
    graph.add_edge(root, ("core", "S"), edge_role="incoming_core")
    graph.add_edge(root, incoming, edge_role="incoming_arm")

    for arc_index, ((tail, head), word) in enumerate(zip(arcs, words)):
        previous: object = ("core", tail)
        for position, label in enumerate(word):
            subdivision = ("sub", arc_index, position)
            leaf = ("leaf", "seg", arc_index, position)
            selected = isinstance(label, int)
            graph.add_node(subdivision, role="tree", label=None, dummy=False)
            graph.add_node(
                leaf,
                role="leaf",
                label=label if selected else None,
                dummy=not selected,
                dummy_name=None if selected else str(label),
            )
            graph.add_edge(previous, subdivision, edge_role=f"seg{arc_index}")
            graph.add_edge(subdivision, leaf, edge_role="arm")
            previous = subdivision
        graph.add_edge(previous, ("core", head), edge_role=f"seg{arc_index}")

    for sink_index, sink in enumerate(spec["sinks"]):
        label = sink_labels[sink]
        leaf = ("leaf", "sink", sink_index)
        selected = isinstance(label, int)
        graph.add_node(
            leaf,
            role="leaf",
            label=label if selected else None,
            dummy=not selected,
            dummy_name=None if selected else str(label),
        )
        graph.add_edge(("core", sink), leaf, edge_role="sink_arm")

    validate_rooted_binary(graph)
    return graph


def validate_rooted_binary(graph: nx.DiGraph) -> None:
    require(nx.is_directed_acyclic_graph(graph), "directed cycle")
    expected = {
        "root": (0, 2),
        "tree": (1, 2),
        "retic": (2, 1),
        "leaf": (1, 0),
    }
    labels: list[int] = []
    for node, data in graph.nodes(data=True):
        role = data.get("role")
        require(role in expected, f"unknown role:{node}:{role}")
        degree = (graph.in_degree(node), graph.out_degree(node))
        require(degree == expected[role], f"nonbinary:{node}:{degree}:{role}")
        if isinstance(data.get("label"), int):
            labels.append(data["label"])
        if role != "leaf":
            require(
                any(
                    graph.nodes[child].get("role") in {"tree", "leaf"}
                    for child in graph.successors(node)
                ),
                f"not tree-child:{node}",
            )
    require(len(labels) == len(set(labels)), "repeated selected label")


def source_supports(core_id: str) -> list[GraphRecord]:
    """Enumerate the minimum-repaired primitive sources for one core."""

    spec = CORE_SPECS[core_id]
    records: list[GraphRecord] = []
    for repair_index, repair in enumerate(spec["repairs"]):
        words: list[list[object]] = [[] for _ in spec["arcs"]]
        next_label = 1  # label 0 is the incoming arm
        for arc_index in repair:
            words[arc_index].append(next_label)
            next_label += 1
        sink_labels: dict[str, object] = {}
        for sink in spec["sinks"]:
            sink_labels[sink] = next_label
            next_label += 1
        ordered = tuple(tuple(word) for word in words)
        graph = build_graph(core_id, ordered, sink_labels, 0)
        labels = selected_labels(graph)
        records.append(
            GraphRecord(
                core_id=core_id,
                incoming_selected=True,
                repair_index=repair_index,
                selected_sink_mask=(1 << len(spec["sinks"])) - 1,
                words=ordered,
                graph=graph,
                selected_labels=labels,
                dummy_labels=(),
            )
        )
    return records


def target_completions(
    selected_total: int, incoming_selected: bool
) -> list[GraphRecord]:
    """Enumerate all target completions in the literal grammar order."""

    records: list[GraphRecord] = []
    for core_id, spec in CORE_SPECS.items():
        outgoing_total = selected_total - 1 if incoming_selected else selected_total
        sink_count = len(spec["sinks"])
        for mask in range(1 << sink_count):
            chosen_sinks = sum(bool(mask & (1 << index)) for index in range(sink_count))
            ordinary = outgoing_total - chosen_sinks
            if ordinary < 0:
                continue
            for counts in weak_compositions(ordinary, len(spec["arcs"])):
                label_stream = iter(
                    range(1 if incoming_selected else 0, selected_total)
                )
                selected_words = tuple(
                    tuple(next(label_stream) for _ in range(count))
                    for count in counts
                )
                repairs: Iterable[tuple[int | None, Sequence[int]]]
                if core_id == "cycle":
                    repairs = ((None, ()),)
                else:
                    repairs = tuple(enumerate(spec["repairs"]))
                for repair_index, repair in repairs:
                    full_words = [list(word) for word in selected_words]
                    dummies: list[str] = []
                    for arc_index in repair:
                        if not full_words[arc_index]:
                            name = f"D_REPAIR_{repair_index}_{arc_index}"
                            full_words[arc_index].append(name)
                            dummies.append(name)

                    used = [value for word in selected_words for value in word]
                    next_label = (
                        max(used) + 1
                        if used
                        else (1 if incoming_selected else 0)
                    )
                    sink_labels: dict[str, object] = {}
                    for sink_index, sink in enumerate(spec["sinks"]):
                        if mask & (1 << sink_index):
                            sink_labels[sink] = next_label
                            next_label += 1
                        else:
                            name = f"D_SINK_{sink_index}"
                            sink_labels[sink] = name
                            dummies.append(name)

                    incoming: object = 0 if incoming_selected else "INCOMING"
                    if not incoming_selected:
                        dummies.append("INCOMING")
                    ordered = tuple(tuple(word) for word in full_words)
                    graph = build_graph(core_id, ordered, sink_labels, incoming)
                    labels = selected_labels(graph)
                    require(
                        labels == tuple(range(selected_total)),
                        f"target labels:{selected_total}:{labels}",
                    )
                    records.append(
                        GraphRecord(
                            core_id=core_id,
                            incoming_selected=incoming_selected,
                            repair_index=repair_index,
                            selected_sink_mask=mask,
                            words=ordered,
                            graph=graph,
                            selected_labels=labels,
                            dummy_labels=tuple(sorted(dummies)),
                        )
                    )
    return records


def selected_labels(graph: nx.DiGraph) -> tuple[int, ...]:
    return tuple(
        sorted(
            data["label"]
            for _, data in graph.nodes(data=True)
            if isinstance(data.get("label"), int)
        )
    )


def relabel_graph(graph: nx.DiGraph, permutation: Sequence[int]) -> nx.DiGraph:
    result = graph.copy()
    for _, data in result.nodes(data=True):
        label = data.get("label")
        if isinstance(label, int):
            data["label"] = permutation[label]
    return result


def graph_payload(graph: nx.DiGraph) -> dict[str, list[Any]]:
    """The public repr-sensitive directed-graph serialization."""

    return {
        "nodes": [
            [
                repr(node),
                {key: repr(value) for key, value in sorted(data.items())},
            ]
            for node, data in sorted(
                graph.nodes(data=True), key=lambda row: repr(row[0])
            )
        ],
        "edges": [
            [
                repr(tail),
                repr(head),
                {key: repr(value) for key, value in sorted(data.items())},
            ]
            for tail, head, data in sorted(
                graph.edges(data=True),
                key=lambda row: (repr(row[0]), repr(row[1])),
            )
        ],
    }


def graph_sha256(graph: nx.DiGraph) -> str:
    return digest(graph_payload(graph))


def restrict_to_labels(graph: nx.DiGraph, keep: set[int]) -> nx.DiGraph:
    """Delete other leaves and repeatedly take the rooted binary reduction."""

    result = graph.copy()
    for node, data in list(result.nodes(data=True)):
        if data.get("role") == "leaf" and data.get("label") not in keep:
            result.remove_node(node)

    changed = True
    while changed:
        changed = False
        for node, data in list(result.nodes(data=True)):
            if result.out_degree(node) == 0 and not (
                data.get("role") == "leaf" and data.get("label") in keep
            ):
                result.remove_node(node)
                changed = True
                break
        if changed:
            continue
        for node, data in list(result.nodes(data=True)):
            if (
                data.get("role") != "leaf"
                and result.in_degree(node) == 1
                and result.out_degree(node) == 1
            ):
                parent = next(result.predecessors(node))
                child = next(result.successors(node))
                result.remove_node(node)
                if parent != child and not result.has_edge(parent, child):
                    result.add_edge(parent, child, edge_role="suppressed")
                changed = True
                break
        if changed:
            continue
        roots = [node for node in result if result.in_degree(node) == 0]
        if (
            len(roots) == 1
            and result.nodes[roots[0]].get("role") != "leaf"
            and result.out_degree(roots[0]) == 1
        ):
            result.remove_node(roots[0])
            changed = True

    for node, data in result.nodes(data=True):
        if data.get("label") in keep:
            data["role"] = "leaf"
        elif result.in_degree(node) == 0:
            data["role"] = "root"
        elif result.in_degree(node) == 2:
            data["role"] = "retic"
        else:
            data["role"] = "tree"
    return result


def selected_graph(record: GraphRecord) -> nx.DiGraph:
    return restrict_to_labels(record.graph, set(record.selected_labels))


def mixed_graph(graph: nx.DiGraph) -> nx.Graph:
    """Suppress the artificial root and retain endpoint arrowhead flags."""

    roots = [
        node
        for node, data in graph.nodes(data=True)
        if data.get("role") == "root" or graph.in_degree(node) == 0
    ]
    require(len(roots) == 1, f"mixed roots:{roots}")
    root = roots[0]
    children = list(graph.successors(root))
    require(len(children) == 2, f"mixed root degree:{len(children)}")

    mixed = nx.Graph()
    for node, data in graph.nodes(data=True):
        if node != root:
            mixed.add_node(node, role=data.get("role"), label=data.get("label"))
    for tail, head in graph.edges():
        if tail == root:
            continue
        require(not mixed.has_edge(tail, head), "mixed parallel edge")
        heads = frozenset({head}) if graph.nodes[head].get("role") == "retic" else frozenset()
        mixed.add_edge(tail, head, heads=heads)

    left, right = children
    require(left != right and not mixed.has_edge(left, right), "bad root suppression")
    heads: set[object] = set()
    if graph.nodes[left].get("role") == "retic":
        heads.add(left)
    if graph.nodes[right].get("role") == "retic":
        heads.add(right)
    mixed.add_edge(left, right, heads=frozenset(heads))
    return mixed


def ordinary_triangles(mixed: nx.Graph) -> list[frozenset[frozenset[object]]]:
    """Return exactly the licensed two-arrowhead ordinary triangles."""

    triangles: list[frozenset[frozenset[object]]] = []
    nodes = sorted(mixed.nodes(), key=repr)
    for left, middle, right in itertools.combinations(nodes, 3):
        if not (
            mixed.has_edge(left, middle)
            and mixed.has_edge(left, right)
            and mixed.has_edge(middle, right)
        ):
            continue
        edges = frozenset(
            {
                frozenset((left, middle)),
                frozenset((left, right)),
                frozenset((middle, right)),
            }
        )
        headed: list[object] = []
        valid = True
        for edge in edges:
            a, b = tuple(edge)
            heads = mixed.edges[a, b].get("heads", frozenset())
            if len(heads) > 1 or any(head not in edge for head in heads):
                valid = False
                break
            if heads:
                headed.append(next(iter(heads)))
        if not valid or len(headed) != 2 or headed[0] != headed[1]:
            continue
        reticulation = headed[0]
        if mixed.nodes[reticulation].get("role") != "retic":
            continue
        triangles.append(edges)
    return triangles


@dataclasses.dataclass
class IncidencePattern:
    mixed: nx.Graph
    plain: nx.Graph
    plain_hash: str
    triangles: list[tuple[nx.Graph, str]]
    ignore_label_values: bool


def _incidence_graph(
    mixed: nx.Graph,
    forgotten_triangle: frozenset[frozenset[object]] | None,
    ignore_label_values: bool,
) -> nx.Graph:
    incidence = nx.Graph()
    forgotten = frozenset() if forgotten_triangle is None else forgotten_triangle
    for node, data in mixed.nodes(data=True):
        label = data.get("label")
        if ignore_label_values:
            label_color: object = "selected" if isinstance(label, int) else "internal"
        else:
            label_color = label
        incidence.add_node(
            ("v", node),
            color=repr(("vertex", label_color)),
        )

    def undirected_key(row: tuple[object, object, dict[str, Any]]) -> tuple[str, str]:
        left, right, _ = row
        return tuple(sorted((repr(left), repr(right))))  # type: ignore[return-value]

    for edge_index, (left, right, data) in enumerate(
        sorted(mixed.edges(data=True), key=undirected_key)
    ):
        edge = frozenset((left, right))
        collapsed = edge in forgotten
        edge_node = ("e", edge_index)
        incidence.add_node(
            edge_node,
            color=repr(("triangle_edge" if collapsed else "edge", None)),
        )
        heads = data.get("heads", frozenset())
        incidence.add_edge(
            edge_node,
            ("v", left),
            head="0" if collapsed or left not in heads else "1",
        )
        incidence.add_edge(
            edge_node,
            ("v", right),
            head="0" if collapsed or right not in heads else "1",
        )
    return incidence


def _wl_hash(graph: nx.Graph) -> str:
    return nx.weisfeiler_lehman_graph_hash(
        graph,
        node_attr="color",
        edge_attr="head",
        iterations=8,
    )


def prepare_incidence(
    graph: nx.DiGraph, *, ignore_label_values: bool
) -> IncidencePattern:
    mixed = mixed_graph(graph)
    plain = _incidence_graph(mixed, None, ignore_label_values)
    triangle_rows: list[tuple[nx.Graph, str]] = []
    for triangle in ordinary_triangles(mixed):
        incidence = _incidence_graph(mixed, triangle, ignore_label_values)
        triangle_rows.append((incidence, _wl_hash(incidence)))
    return IncidencePattern(
        mixed=mixed,
        plain=plain,
        plain_hash=_wl_hash(plain),
        triangles=triangle_rows,
        ignore_label_values=ignore_label_values,
    )


def prepare_incidence_if_simple(
    graph: nx.DiGraph, *, ignore_label_values: bool
) -> IncidencePattern | None:
    """Return ``None`` when artificial-root suppression is not a simple graph.

    Such restricted target completions have exact relation ``none``.  This is
    the same mathematical domain check as the defining root-suppression
    construction, expressed without importing an atlas helper.
    """

    try:
        return prepare_incidence(
            graph, ignore_label_values=ignore_label_values
        )
    except IndependentUniverseError as exc:
        if str(exc).startswith(
            ("mixed roots:", "mixed root degree:", "mixed parallel edge", "bad root suppression")
        ):
            return None
        raise


def _matcher(left: nx.Graph, right: nx.Graph) -> nx.algorithms.isomorphism.GraphMatcher:
    return nx.algorithms.isomorphism.GraphMatcher(
        left,
        right,
        node_match=lambda a, b: a.get("color") == b.get("color"),
        edge_match=lambda a, b: a.get("head") == b.get("head"),
    )


def _permutation_from_mapping(
    source: IncidencePattern,
    target: IncidencePattern,
    mapping: dict[object, object],
    port_count: int,
) -> tuple[int, ...] | None:
    result: list[int | None] = [None] * port_count
    for source_node, source_data in source.mixed.nodes(data=True):
        source_label = source_data.get("label")
        if not isinstance(source_label, int):
            continue
        target_wrapper = mapping.get(("v", source_node))
        if not (
            isinstance(target_wrapper, tuple)
            and len(target_wrapper) == 2
            and target_wrapper[0] == "v"
        ):
            return None
        target_label = target.mixed.nodes[target_wrapper[1]].get("label")
        if not isinstance(target_label, int):
            return None
        if result[target_label] not in {None, source_label}:
            return None
        result[target_label] = source_label
    if any(value is None for value in result):
        return None
    permutation = tuple(int(value) for value in result)
    if sorted(permutation) != list(range(port_count)):
        return None
    return permutation


def relation_permutations(
    source: IncidencePattern,
    target: IncidencePattern,
    port_count: int,
) -> dict[tuple[int, ...], str]:
    """Derive every relabelling giving the exact or ordinary-T relation.

    Rather than assuming any one of the ``port_count!`` relabellings, this
    enumerates all unlabelled incidence isomorphisms.  Each mapping uniquely
    induces the required target-label permutation, so completeness is exact.
    """

    require(source.ignore_label_values and target.ignore_label_values, "permutation pattern mode")
    exact: set[tuple[int, ...]] = set()
    if source.plain_hash == target.plain_hash:
        for mapping in _matcher(source.plain, target.plain).isomorphisms_iter():
            permutation = _permutation_from_mapping(source, target, mapping, port_count)
            if permutation is not None:
                exact.add(permutation)

    triangle: set[tuple[int, ...]] = set()
    for source_graph, source_hash in source.triangles:
        for target_graph, target_hash in target.triangles:
            if source_hash != target_hash:
                continue
            for mapping in _matcher(source_graph, target_graph).isomorphisms_iter():
                permutation = _permutation_from_mapping(source, target, mapping, port_count)
                if permutation is not None:
                    triangle.add(permutation)

    relations = {permutation: "triangle" for permutation in triangle - exact}
    relations.update({permutation: "isomorphic" for permutation in exact})
    return relations


def fixed_relation(
    source: IncidencePattern, target: IncidencePattern
) -> str:
    require(
        not source.ignore_label_values and not target.ignore_label_values,
        "fixed pattern mode",
    )
    if source.plain_hash == target.plain_hash and _matcher(
        source.plain, target.plain
    ).is_isomorphic():
        return "isomorphic"
    for source_graph, source_hash in source.triangles:
        for target_graph, target_hash in target.triangles:
            if source_hash == target_hash and _matcher(
                source_graph, target_graph
            ).is_isomorphic():
                return "triangle"
    return "none"


def canonical_vertex_transport(
    source: IncidencePattern, target: IncidencePattern
) -> tuple[str, dict[object, object]]:
    """Return the first exact mixed-vertex transport and its public hash."""

    require(
        not source.ignore_label_values and not target.ignore_label_values,
        "transport pattern mode",
    )
    require(source.plain_hash == target.plain_hash, "transport WL bucket")
    public_mappings: list[
        tuple[list[list[str]], dict[object, object]]
    ] = []
    for mapping in _matcher(source.plain, target.plain).isomorphisms_iter():
        rows = [
            [repr(node), repr(mapping[("v", node)][1])]
            for node in sorted(source.mixed.nodes(), key=repr)
        ]
        vertex_mapping = {
            node: mapping[("v", node)][1] for node in source.mixed.nodes()
        }
        public_mappings.append((rows, vertex_mapping))
    require(public_mappings, "missing exact vertex transport")
    public, vertex_mapping = min(
        public_mappings, key=lambda row: canonical_bytes(row[0])
    )
    return digest(public), vertex_mapping


def removed_label_attachment_site(
    full_graph: nx.DiGraph,
    restricted_graph: nx.DiGraph,
    removed_label: int,
) -> tuple[str, frozenset[object]]:
    """Recover the mixed edge on which one removed leaf was attached."""

    leaves = [
        node
        for node, data in full_graph.nodes(data=True)
        if data.get("label") == removed_label
    ]
    require(len(leaves) == 1, f"removed label leaf:{removed_label}:{leaves}")
    leaf = leaves[0]
    parent = next(full_graph.predecessors(leaf))
    if full_graph.nodes[parent].get("role") == "root":
        roots = [
            node
            for node, data in restricted_graph.nodes(data=True)
            if data.get("role") == "root" or restricted_graph.in_degree(node) == 0
        ]
        require(len(roots) == 1, "root-movement restricted root")
        root = roots[0]
        endpoints = frozenset(restricted_graph.successors(root))
        site_type = "root_suppressed_segment"
    else:
        require(
            full_graph.nodes[parent].get("role") == "tree"
            and full_graph.in_degree(parent) == 1
            and full_graph.out_degree(parent) == 2,
            f"removed label subdivision:{parent}",
        )
        tail = next(full_graph.predecessors(parent))
        other_children = [
            node for node in full_graph.successors(parent) if node != leaf
        ]
        require(len(other_children) == 1, "removed label other child")
        endpoints = frozenset((tail, other_children[0]))
        site_type = "mixed_edge"

    require(len(endpoints) == 2, f"attachment endpoints:{endpoints}")
    restricted_mixed = mixed_graph(restricted_graph)
    left, right = tuple(endpoints)
    require(
        restricted_mixed.has_edge(left, right),
        f"attachment site absent after restriction:{endpoints}",
    )
    return site_type, endpoints


def triple_type(graph: nx.DiGraph) -> str:
    labels = selected_labels(graph)
    require(len(labels) == 3, f"triple labels:{labels}")
    reduced = restrict_to_labels(graph, set(labels))
    reticulations = sum(
        data.get("role") == "retic" and reduced.in_degree(node) == 2
        for node, data in reduced.nodes(data=True)
    )
    if reticulations == 0:
        return "tree"
    if reticulations == 1:
        return "sunlet"
    return f"r{reticulations}"


def insertion_candidates(graph: nx.DiGraph) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        if graph.nodes[head].get("role") == "leaf":
            continue
        if graph.nodes[tail].get("role") == "root":
            continue
        rows.append(
            {
                "tail": repr(tail),
                "head": repr(head),
                "edge_role": data.get("edge_role"),
            }
        )
    return rows


def insert_theta_leaf(
    graph: nx.DiGraph,
    candidate: dict[str, object],
    label: int,
    namespace: str,
) -> nx.DiGraph:
    tail = ast.literal_eval(str(candidate["tail"]))
    head = ast.literal_eval(str(candidate["head"]))
    require(graph.has_edge(tail, head), f"theta insertion edge:{candidate}")
    result = graph.copy()
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = (namespace, "subdivision", label, repr(tail), repr(head))
    leaf = (namespace, "leaf", label, repr(tail), repr(head))
    require(subdivision not in result and leaf not in result, "theta insertion collision")
    result.add_node(
        subdivision, role="tree", label=None, dummy=False, dummy_name=None
    )
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    validate_rooted_binary(result)
    return result


def insert_cycle_leaf(
    graph: nx.DiGraph, candidate: dict[str, object], label: int
) -> nx.DiGraph:
    tail = ast.literal_eval(str(candidate["tail"]))
    head = ast.literal_eval(str(candidate["head"]))
    require(graph.has_edge(tail, head), f"cycle insertion edge:{candidate}")
    result = graph.copy()
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = (
        "cycle_restoration_subdivision",
        label,
        repr(tail),
        repr(head),
    )
    leaf = ("leaf", "cycle_restoration", label)
    require(subdivision not in result and leaf not in result, "cycle insertion collision")
    result.add_node(subdivision, role="tree", label=None, dummy=False)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    validate_rooted_binary(result)
    return result


def promote_role(graph: nx.DiGraph, role: str, label: int) -> nx.DiGraph:
    result = graph.copy()
    nodes = [
        node
        for node, data in result.nodes(data=True)
        if data.get("dummy_name") == role
    ]
    require(len(nodes) == 1, f"dummy role:{role}:{nodes}")
    result.nodes[nodes[0]]["label"] = label
    result.nodes[nodes[0]]["dummy"] = False
    result.nodes[nodes[0]]["dummy_name"] = None
    return result


def promote_roles_in_order(
    graph: nx.DiGraph, roles: Sequence[str], first_label: int
) -> nx.DiGraph:
    result = graph
    for offset, role in enumerate(roles):
        result = promote_role(result, role, first_label + offset)
    validate_rooted_binary(result)
    return result


@dataclasses.dataclass
class CycleConfiguration:
    placement_path: tuple[int, ...]
    graph: nx.DiGraph
    pattern: IncidencePattern


def cycle_configurations(
    source: nx.DiGraph, depth: int
) -> list[CycleConfiguration]:
    states: list[tuple[tuple[int, ...], nx.DiGraph]] = [((), source)]
    for current_depth in range(1, depth + 1):
        label = 2 + current_depth
        children: list[tuple[tuple[int, ...], nx.DiGraph]] = []
        for path, graph in states:
            candidates = insertion_candidates(graph)
            require(
                len(candidates) == 2 + current_depth,
                f"cycle candidates:{current_depth}:{len(candidates)}",
            )
            for candidate_index, candidate in enumerate(candidates):
                children.append(
                    (
                        path + (candidate_index,),
                        insert_cycle_leaf(graph, candidate, label),
                    )
                )
        states = children
    return [
        CycleConfiguration(
            placement_path=path,
            graph=graph,
            pattern=prepare_incidence(graph, ignore_label_values=False),
        )
        for path, graph in states
    ]


def three_port_tree() -> nx.DiGraph:
    graph = nx.DiGraph(name="three_port_tree")
    for node, role, label in (
        ("r", "root", None),
        ("v", "tree", None),
        ("L0", "leaf", 0),
        ("L1", "leaf", 1),
        ("L2", "leaf", 2),
    ):
        graph.add_node(node, role=role, label=label, dummy=False, dummy_name=None)
    graph.add_edges_from(
        (
            ("r", "L0", {"edge_role": "incoming_arm"}),
            ("r", "v", {"edge_role": "incoming_core"}),
            ("v", "L1", {"edge_role": "arm"}),
            ("v", "L2", {"edge_role": "arm"}),
        )
    )
    validate_rooted_binary(graph)
    return graph


def anchor_row(
    *,
    origin: str,
    port_count: int,
    relation: str,
    source: nx.DiGraph,
    target: nx.DiGraph,
    locator: dict[str, Any],
) -> dict[str, Any]:
    body = {
        "origin": origin,
        "port_count": port_count,
        "relation": relation,
        "source_graph_sha256": graph_sha256(source),
        "target_graph_sha256": graph_sha256(target),
        "structural_locator": locator,
    }
    return {"anchor_key": digest(body), **body}


@dataclasses.dataclass
class CycleRoot:
    source_index: int
    target_index: int
    permutation_index: int
    permutation: tuple[int, ...]
    base_raw_id: int
    roles: tuple[str, ...]
    record: GraphRecord


@dataclasses.dataclass
class ThetaRoot:
    source_index: int
    target_index: int
    permutation_index: int
    permutation: tuple[int, ...]
    base_raw_id: int
    roles: tuple[str, ...]
    source: nx.DiGraph
    target: nx.DiGraph


@dataclasses.dataclass
class ThetaSeedPair:
    anchor_key: str
    origin: str
    source: nx.DiGraph
    target: nx.DiGraph


def relabel_selected_by_map(
    graph: nx.DiGraph, mapping: dict[int, int]
) -> nx.DiGraph:
    result = graph.copy()
    for _, data in result.nodes(data=True):
        label = data.get("label")
        if isinstance(label, int):
            require(label in mapping, f"relabel map missing:{label}")
            data["label"] = mapping[label]
    return result


def _audit_marginalized_theta_restorations(
    sources: Sequence[GraphRecord],
    roots: Sequence[ThetaRoot],
    seed_pairs: Sequence[ThetaSeedPair],
) -> dict[str, Any]:
    """Count and root-movement-map the incoming-marginalized family.

    These rows demonstrate why the 133-row result must be described as an
    anchor-*seed* universe.  If the explicit incoming-boundary seed convention
    is dropped, the excluded abstract parents do have fully restored exact
    graph-isomorphism paths.  They belong to downstream/root-movement probe
    handling rather than to the fixed-full seed list checked here.
    """

    dummy_multiplicity: collections.Counter[int] = collections.Counter(
        len(root.roles) for root in roots
    )
    require(
        dummy_multiplicity == {1: 56, 2: 88, 3: 32},
        f"marginalized theta dummy multiplicity:{dummy_multiplicity}",
    )

    # Collapse the 96 theta seed presentations to exact ordered graph-pair
    # classes.  Sorting first makes the canonical member key deterministic.
    seed_classes: list[dict[str, Any]] = []
    for seed in sorted(seed_pairs, key=lambda row: row.anchor_key):
        source_pattern = prepare_incidence(
            seed.source, ignore_label_values=False
        )
        target_pattern = prepare_incidence(
            seed.target, ignore_label_values=False
        )
        port_count = len(selected_labels(seed.source))
        found = None
        for row in seed_classes:
            if (
                row["port_count"] == port_count
                and fixed_relation(source_pattern, row["source_pattern"])
                == "isomorphic"
                and fixed_relation(target_pattern, row["target_pattern"])
                == "isomorphic"
            ):
                found = row
                break
        if found is None:
            seed_classes.append(
                {
                    "class_key": seed.anchor_key,
                    "port_count": port_count,
                    "origin": seed.origin,
                    "representative": seed,
                    "source_pattern": source_pattern,
                    "target_pattern": target_pattern,
                    "member_keys": [seed.anchor_key],
                }
            )
        else:
            require(found["origin"] == seed.origin, "theta seed class origin drift")
            found["member_keys"].append(seed.anchor_key)

    # All configurations are constructed independently.  Paths are retained
    # so that every excluded terminal has a checkable restriction record.
    configurations: dict[
        tuple[int, int],
        list[tuple[tuple[int, ...], nx.DiGraph, IncidencePattern]],
    ] = {}
    buckets: dict[tuple[int, int], dict[str, list[int]]] = {}
    for source_index, record in enumerate(sources):
        states: list[tuple[tuple[int, ...], nx.DiGraph]] = [((), record.graph)]
        for depth in range(1, 4):
            children: list[tuple[tuple[int, ...], nx.DiGraph]] = []
            label = 4 + depth
            for path, graph in states:
                for candidate_index, candidate in enumerate(
                    insertion_candidates(graph)
                ):
                    children.append(
                        (
                            path + (candidate_index,),
                            insert_theta_leaf(
                                graph,
                                candidate,
                                label,
                                f"excluded_theta_depth_{depth}",
                            ),
                        )
                    )
            states = children
            expected = {1: 8, 2: 72, 3: 720}[depth]
            require(
                len(states) == expected,
                f"excluded theta configurations:{source_index}:{depth}:{len(states)}",
            )
            rows = [
                (
                    path,
                    graph,
                    prepare_incidence(graph, ignore_label_values=False),
                )
                for path, graph in states
            ]
            by_hash: dict[str, list[int]] = collections.defaultdict(list)
            for index, (_path, _graph, pattern) in enumerate(rows):
                by_hash[pattern.plain_hash].append(index)
            configurations[(source_index, depth)] = rows
            buckets[(source_index, depth)] = dict(by_hash)

    isomorphic_by_depth: collections.Counter[int] = collections.Counter()
    prefix_exact_equality_checks = 0
    mapped_by_seed_origin: collections.Counter[str] = collections.Counter()
    mapped_by_seed_class: collections.Counter[str] = collections.Counter()
    mapping_rows: list[dict[str, Any]] = []
    for root in roots:
        depth = len(root.roles)
        source_rows = configurations[(root.source_index, depth)]
        source_buckets = buckets[(root.source_index, depth)]
        for role_order in itertools.permutations(root.roles):
            target = promote_roles_in_order(root.target, role_order, 5)
            target_pattern = prepare_incidence(
                target, ignore_label_values=False
            )
            for index in source_buckets.get(target_pattern.plain_hash, []):
                path, source_graph, source_pattern = source_rows[index]
                relation = fixed_relation(source_pattern, target_pattern)
                require(
                    relation in {"none", "isomorphic"},
                    f"excluded theta restoration relation:{relation}",
                )
                if relation != "isomorphic":
                    continue
                isomorphic_by_depth[depth] += 1

                # Verify that the terminal path is an exact equality at every
                # preceding restoration depth as well, not merely at its end.
                for prefix_depth in range(1, depth + 1):
                    keep = set(range(5 + prefix_depth))
                    prefix_source = restrict_to_labels(source_graph, keep)
                    prefix_target = restrict_to_labels(target, keep)
                    require(
                        fixed_relation(
                            prepare_incidence(
                                prefix_source, ignore_label_values=False
                            ),
                            prepare_incidence(
                                prefix_target, ignore_label_values=False
                            ),
                        )
                        == "isomorphic",
                        f"excluded theta intermediate equality:{root.base_raw_id}:{role_order}:{path}:{prefix_depth}",
                    )
                    prefix_exact_equality_checks += 1

                # Root movement: remove the restored label occupying the
                # distinguished target incoming boundary, then compact the
                # remaining labels.  The resulting pair must land in exactly
                # one canonical class of the 96 theta seeds.
                incoming_position = role_order.index("INCOMING")
                incoming_label = 5 + incoming_position
                full_labels = list(selected_labels(source_graph))
                remaining_labels = [
                    label for label in full_labels if label != incoming_label
                ]
                compact = {
                    old_label: new_label
                    for new_label, old_label in enumerate(remaining_labels)
                }
                restricted_source = relabel_selected_by_map(
                    restrict_to_labels(
                        source_graph, set(remaining_labels)
                    ),
                    compact,
                )
                restricted_target = relabel_selected_by_map(
                    restrict_to_labels(target, set(remaining_labels)), compact
                )
                restricted_source_pattern = prepare_incidence(
                    restricted_source, ignore_label_values=False
                )
                restricted_target_pattern = prepare_incidence(
                    restricted_target, ignore_label_values=False
                )
                matching_classes = [
                    row
                    for row in seed_classes
                    if row["port_count"] == len(remaining_labels)
                    and fixed_relation(
                        restricted_source_pattern, row["source_pattern"]
                    )
                    == "isomorphic"
                    and fixed_relation(
                        restricted_target_pattern, row["target_pattern"]
                    )
                    == "isomorphic"
                ]
                require(
                    len(matching_classes) == 1,
                    f"excluded theta seed mapping:{root.base_raw_id}:{role_order}:{path}:{len(matching_classes)}",
                )
                seed_class = matching_classes[0]
                (
                    source_transport_sha256,
                    source_vertex_mapping,
                ) = canonical_vertex_transport(
                    restricted_source_pattern,
                    seed_class["source_pattern"],
                )
                (
                    target_transport_sha256,
                    target_vertex_mapping,
                ) = canonical_vertex_transport(
                    restricted_target_pattern,
                    seed_class["target_pattern"],
                )
                source_site_type, source_site = removed_label_attachment_site(
                    source_graph,
                    restricted_source,
                    incoming_label,
                )
                target_site_type, target_site = removed_label_attachment_site(
                    target,
                    restricted_target,
                    incoming_label,
                )
                transported_source_site = frozenset(
                    source_vertex_mapping[node] for node in source_site
                )
                transported_target_site = frozenset(
                    target_vertex_mapping[node] for node in target_site
                )
                require(
                    seed_class["source_pattern"].mixed.has_edge(
                        *tuple(transported_source_site)
                    ),
                    "transported source one-port site",
                )
                require(
                    seed_class["target_pattern"].mixed.has_edge(
                        *tuple(transported_target_site)
                    ),
                    "transported target one-port site",
                )
                mapped_by_seed_origin[seed_class["origin"]] += 1
                mapped_by_seed_class[seed_class["class_key"]] += 1
                mapping_rows.append(
                    {
                        "excluded_base_raw_id": root.base_raw_id,
                        "source_index": root.source_index,
                        "target_index": root.target_index,
                        "permutation_index": root.permutation_index,
                        "restored_role_order": list(role_order),
                        "source_placement_path": list(path),
                        "incoming_label_removed": incoming_label,
                        "restricted_port_count": len(remaining_labels),
                        "canonical_seed_key": seed_class["class_key"],
                        "canonical_seed_origin": seed_class["origin"],
                        "source_restriction_transport_sha256":
                            source_transport_sha256,
                        "target_restriction_transport_sha256":
                            target_transport_sha256,
                        "source_one_port_site_type": source_site_type,
                        "source_one_port_site_on_seed": sorted(
                            (repr(node) for node in transported_source_site)
                        ),
                        "target_one_port_site_type": target_site_type,
                        "target_one_port_site_on_seed": sorted(
                            (repr(node) for node in transported_target_site)
                        ),
                    }
                )

    require(
        isomorphic_by_depth == {1: 56, 2: 176, 3: 192},
        f"excluded theta full isomorphisms:{isomorphic_by_depth}",
    )
    require(
        prefix_exact_equality_checks == 984,
        f"excluded theta prefix equalities:{prefix_exact_equality_checks}",
    )
    require(len(mapping_rows) == 424, "excluded theta mapping coverage")
    require(
        mapped_by_seed_origin
        == {
            "theta2_physical_k5": 56,
            "theta2_physical_k6": 176,
            "theta2_physical_k7": 192,
        },
        f"excluded theta seed origins:{mapped_by_seed_origin}",
    )
    ordered_mapping_rows = sorted(mapping_rows, key=canonical_bytes)
    return {
        "dummy_multiplicity": dummy_multiplicity,
        "isomorphic_by_depth": isomorphic_by_depth,
        "prefix_exact_equality_checks": prefix_exact_equality_checks,
        "canonical_seed_class_count": len(seed_classes),
        "canonical_seed_class_member_census": collections.Counter(
            len(row["member_keys"]) for row in seed_classes
        ),
        "mapped_by_seed_origin": mapped_by_seed_origin,
        "mapped_by_seed_class": mapped_by_seed_class,
        "mapping_rows": ordered_mapping_rows,
        "mapping_rows_sha256": digest(ordered_mapping_rows),
        "unmatched": 0,
    }


def _enumerate_cycle() -> tuple[list[dict[str, Any]], dict[str, int], dict[str, Any]]:
    sources = source_supports("cycle")
    targets = target_completions(3, True) + target_completions(3, False)
    permutations = tuple(itertools.permutations(range(3)))
    require((len(sources), len(targets), len(permutations)) == (2, 1120, 6), "cycle primitive census")

    source_structural = [
        prepare_incidence(source.graph, ignore_label_values=True)
        for source in sources
    ]
    source_triples = [triple_type(source.graph) for source in sources]
    anchors: list[dict[str, Any]] = []
    roots: list[CycleRoot] = []
    base_relations: collections.Counter[str] = collections.Counter()
    root_multiplicity: collections.Counter[int] = collections.Counter()
    tree_sunlet_exclusions = 0

    for source_index, source in enumerate(sources):
        for target_index, target_record in enumerate(targets):
            target_selected = selected_graph(target_record)
            target_pattern = prepare_incidence_if_simple(
                target_selected, ignore_label_values=True
            )
            relations = (
                {}
                if target_pattern is None
                else relation_permutations(
                    source_structural[source_index], target_pattern, 3
                )
            )
            target_triple = triple_type(target_selected)
            incompatible = {
                source_triples[source_index], target_triple
            } == {"tree", "sunlet"}

            for permutation_index, permutation in enumerate(permutations):
                raw_id = (
                    source_index * len(targets) * len(permutations)
                    + target_index * len(permutations)
                    + permutation_index
                )
                relation = relations.get(permutation)
                if incompatible:
                    tree_sunlet_exclusions += 1
                    require(relation is None, f"cycle excluded equality:{raw_id}")
                    continue
                if target_record.dummy_labels:
                    roles = tuple(sorted(target_record.dummy_labels))
                    roots.append(
                        CycleRoot(
                            source_index=source_index,
                            target_index=target_index,
                            permutation_index=permutation_index,
                            permutation=permutation,
                            base_raw_id=raw_id,
                            roles=roles,
                            record=target_record,
                        )
                    )
                    root_multiplicity[len(roles)] += 1
                    continue
                require(relation in {"isomorphic", "triangle"}, f"cycle no-dummy gap:{raw_id}:{relation}")
                target = relabel_graph(target_record.graph, permutation)
                anchors.append(
                    anchor_row(
                        origin="cycle_physical_k3",
                        port_count=3,
                        relation=relation,
                        source=source.graph,
                        target=target,
                        locator={
                            "source_index": source_index,
                            "target_index": target_index,
                            "permutation_index": permutation_index,
                            "port_permutation": list(permutation),
                            "base_raw_id": raw_id,
                        },
                    )
                )
                base_relations[relation] += 1

    require(tree_sunlet_exclusions == 7452, f"cycle triple exclusions:{tree_sunlet_exclusions}")
    require(len(roots) == 5964, f"cycle roots:{len(roots)}")
    require(root_multiplicity == {1: 324, 2: 1896, 3: 2784, 4: 960}, f"cycle root multiplicity:{root_multiplicity}")
    require(base_relations == {"isomorphic": 8, "triangle": 16}, f"cycle base relations:{base_relations}")

    configuration_cache: dict[tuple[int, int], list[CycleConfiguration]] = {}
    plain_buckets: dict[tuple[int, int], dict[str, list[int]]] = {}
    triangle_buckets: dict[tuple[int, int], dict[str, list[int]]] = {}
    for source_index, source in enumerate(sources):
        for depth, expected in ((1, 3), (2, 12), (3, 60), (4, 360)):
            rows = cycle_configurations(source.graph, depth)
            require(len(rows) == expected, f"cycle configurations:{source_index}:{depth}:{len(rows)}")
            configuration_cache[(source_index, depth)] = rows
            plain: dict[str, list[int]] = collections.defaultdict(list)
            triangles: dict[str, list[int]] = collections.defaultdict(list)
            for index, row in enumerate(rows):
                plain[row.pattern.plain_hash].append(index)
                for _, triangle_hash in row.pattern.triangles:
                    triangles[triangle_hash].append(index)
            plain_buckets[(source_index, depth)] = dict(plain)
            triangle_buckets[(source_index, depth)] = dict(triangles)

    full_raw_id = 0
    restored_relations: collections.Counter[str] = collections.Counter()
    for root in roots:
        depth = len(root.roles)
        configurations = configuration_cache[(root.source_index, depth)]
        target = promote_roles_in_order(
            relabel_graph(root.record.graph, root.permutation), root.roles, 3
        )
        target_pattern = prepare_incidence(target, ignore_label_values=False)
        candidate_indices = set(
            plain_buckets[(root.source_index, depth)].get(
                target_pattern.plain_hash, []
            )
        )
        for _, triangle_hash in target_pattern.triangles:
            candidate_indices.update(
                triangle_buckets[(root.source_index, depth)].get(
                    triangle_hash, []
                )
            )

        for configuration_index in sorted(candidate_indices):
            configuration = configurations[configuration_index]
            relation = fixed_relation(configuration.pattern, target_pattern)
            if relation == "none":
                continue
            require(relation == "isomorphic", f"cycle restored relation:{relation}")
            anchors.append(
                anchor_row(
                    origin="cycle_restored_physical_k4",
                    port_count=3 + depth,
                    relation=relation,
                    source=configuration.graph,
                    target=target,
                    locator={
                        "source_index": root.source_index,
                        "target_index": root.target_index,
                        "permutation_index": root.permutation_index,
                        "port_permutation": list(root.permutation),
                        "base_raw_id": root.base_raw_id,
                        "dummy_roles_in_label_order": list(root.roles),
                        "source_placement_path": list(configuration.placement_path),
                        "full_raw_id": full_raw_id + configuration_index,
                    },
                )
            )
            restored_relations[relation] += 1
        full_raw_id += len(configurations)

    require(full_raw_id == 536_364, f"cycle full children:{full_raw_id}")
    require(restored_relations == {"isomorphic": 12}, f"cycle restored:{restored_relations}")
    require(len(anchors) == 36, f"cycle anchors:{len(anchors)}")
    stage = {
        "cycle_base_raw_presentations": 13_440,
        "cycle_tree_sunlet_excluded": tree_sunlet_exclusions,
        "cycle_dummy_restoration_roots": len(roots),
        "cycle_full_restoration_children": full_raw_id,
        "cycle_base_physical_equalities": sum(base_relations.values()),
        "cycle_restored_physical_equalities": sum(restored_relations.values()),
    }
    diagnostics = {
        "base_relation_census": dict(sorted(base_relations.items())),
        "root_multiplicity_by_dummy_count": {
            str(key): value for key, value in sorted(root_multiplicity.items())
        },
    }
    return anchors, stage, diagnostics


def _enumerate_theta2() -> tuple[list[dict[str, Any]], dict[str, int], dict[str, Any]]:
    sources = source_supports("theta2")
    selected_targets = target_completions(5, True)
    marginalized_targets = target_completions(5, False)
    targets = selected_targets + marginalized_targets
    permutations = tuple(itertools.permutations(range(5)))
    require(
        (
            len(sources), len(selected_targets), len(marginalized_targets),
            len(targets), len(permutations),
        ) == (4, 1983, 4155, 6138, 120),
        "theta2 primitive census",
    )

    source_patterns = [
        prepare_incidence(source.graph, ignore_label_values=True)
        for source in sources
    ]
    permutation_indices = {
        permutation: index for index, permutation in enumerate(permutations)
    }
    roots: list[ThetaRoot] = []
    anchors: list[dict[str, Any]] = []
    seed_pairs: list[ThetaSeedPair] = []
    base_relation_census: collections.Counter[str] = collections.Counter()
    dummy_multiplicity: collections.Counter[int] = collections.Counter()
    incoming_boundary_mismatches = 0
    marginalized_roots: list[ThetaRoot] = []

    for target_index, target_record in enumerate(targets):
        target_selected = selected_graph(target_record)
        target_pattern = prepare_incidence_if_simple(
            target_selected, ignore_label_values=True
        )
        for source_index, source in enumerate(sources):
            relations = (
                {}
                if target_pattern is None
                else relation_permutations(
                    source_patterns[source_index], target_pattern, 5
                )
            )
            for permutation, relation in sorted(
                relations.items(), key=lambda item: permutation_indices[item[0]]
            ):
                require(relation == "isomorphic", f"theta2 base triangle:{source_index}:{target_index}:{permutation}")
                # The distinguished incoming boundary is one of the five
                # physical ports of a theta2 anchor.  A completion generated
                # with a dummy incoming boundary is a selected marginal, not a
                # physical five-port anchor or a fixed-full repair obligation.
                # This distinction is literal grammar metadata; it does not
                # appeal to a model rank or separator.
                permutation_index = permutation_indices[permutation]
                raw_id = (
                    source_index * len(targets) * len(permutations)
                    + target_index * len(permutations)
                    + permutation_index
                )
                target = relabel_graph(target_record.graph, permutation)
                roles = tuple(sorted(target_record.dummy_labels))
                if not target_record.incoming_selected:
                    incoming_boundary_mismatches += 1
                    marginalized_roots.append(
                        ThetaRoot(
                            source_index=source_index,
                            target_index=target_index,
                            permutation_index=permutation_index,
                            permutation=permutation,
                            base_raw_id=raw_id,
                            roles=roles,
                            source=source.graph,
                            target=target,
                        )
                    )
                    continue
                root = ThetaRoot(
                    source_index=source_index,
                    target_index=target_index,
                    permutation_index=permutation_index,
                    permutation=permutation,
                    base_raw_id=raw_id,
                    roles=roles,
                    source=source.graph,
                    target=target,
                )
                dummy_multiplicity[len(roles)] += 1
                base_relation_census[relation] += 1
                if roles:
                    roots.append(root)
                else:
                    row = anchor_row(
                        origin="theta2_physical_k5",
                        port_count=5,
                        relation=relation,
                        source=source.graph,
                        target=target,
                        locator={
                            "source_index": source_index,
                            "target_index": target_index,
                            "permutation_index": permutation_index,
                            "port_permutation": list(permutation),
                            "base_raw_id": raw_id,
                        },
                    )
                    anchors.append(row)
                    seed_pairs.append(
                        ThetaSeedPair(
                            anchor_key=row["anchor_key"],
                            origin=row["origin"],
                            source=source.graph,
                            target=target,
                        )
                    )

    require(base_relation_census == {"isomorphic": 80}, f"theta2 base equality:{base_relation_census}")
    require(
        incoming_boundary_mismatches == 176,
        f"theta2 incoming-boundary selected isomorphisms:{incoming_boundary_mismatches}",
    )
    require(dummy_multiplicity == {0: 24, 1: 40, 2: 16}, f"theta2 dummy multiplicity:{dummy_multiplicity}")
    require(len(roots) == 56 and len(anchors) == 24, "theta2 roots/no-dummy")

    roots.sort(key=lambda row: row.base_raw_id)
    continuations: list[tuple[ThetaRoot, str, int, dict[str, object]]] = []
    first_relation_census: collections.Counter[str] = collections.Counter()
    first_requests = 0
    first_children = 0
    for root in roots:
        candidates = insertion_candidates(root.source)
        require(len(candidates) == 8, f"theta2 base candidates:{root.source_index}:{len(candidates)}")
        for restored_role in root.roles:
            first_requests += 1
            promoted_target = promote_role(root.target, restored_role, 5)
            remaining = tuple(role for role in root.roles if role != restored_role)
            comparison_target = (
                restrict_to_labels(promoted_target, set(range(6)))
                if remaining
                else promoted_target
            )
            target_pattern = prepare_incidence(
                comparison_target, ignore_label_values=False
            )
            for insertion_index, candidate in enumerate(candidates):
                first_children += 1
                restored_source = insert_theta_leaf(
                    root.source, candidate, 5, "theta2_k6"
                )
                relation = fixed_relation(
                    prepare_incidence(restored_source, ignore_label_values=False),
                    target_pattern,
                )
                if relation == "none":
                    continue
                require(relation == "isomorphic", f"theta2 k6 relation:{relation}")
                first_relation_census["isomorphic"] += 1
                if remaining:
                    require(len(remaining) == 1, "theta2 continuation roles")
                    continuations.append(
                        (root, restored_role, insertion_index, candidate)
                    )
                else:
                    row = anchor_row(
                        origin="theta2_physical_k6",
                        port_count=6,
                        relation=relation,
                        source=restored_source,
                        target=promoted_target,
                        locator={
                            "source_index": root.source_index,
                            "target_index": root.target_index,
                            "permutation_index": root.permutation_index,
                            "port_permutation": list(root.permutation),
                            "base_raw_id": root.base_raw_id,
                            "restored_role": restored_role,
                            "source_insertion_index": insertion_index,
                            "source_insertion": candidate,
                        },
                    )
                    anchors.append(row)
                    seed_pairs.append(
                        ThetaSeedPair(
                            anchor_key=row["anchor_key"],
                            origin=row["origin"],
                            source=restored_source,
                            target=promoted_target,
                        )
                    )

    require(first_requests == 72, f"theta2 first requests:{first_requests}")
    require(first_children == 576, f"theta2 first children:{first_children}")
    require(first_relation_census == {"isomorphic": 72}, f"theta2 first equality:{first_relation_census}")
    require(len(continuations) == 32, f"theta2 continuations:{len(continuations)}")
    require(sum(row["origin"] == "theta2_physical_k6" for row in anchors) == 40, "theta2 k6 physical")

    second_children = 0
    second_relation_census: collections.Counter[str] = collections.Counter()
    for root, first_role, first_index, first_candidate in continuations:
        remaining = tuple(role for role in root.roles if role != first_role)
        require(len(remaining) == 1, "theta2 second remaining role")
        second_role = remaining[0]
        # The public terminal graph uses the active, explicit namespaces rather
        # than the legacy restoration-certificate node names.
        source_six = insert_theta_leaf(
            root.source, first_candidate, 5, "theta2_k7_first"
        )
        candidates = insertion_candidates(source_six)
        require(len(candidates) == 9, f"theta2 second candidates:{len(candidates)}")
        target = promote_role(promote_role(root.target, first_role, 5), second_role, 6)
        target_pattern = prepare_incidence(target, ignore_label_values=False)
        for insertion_index, candidate in enumerate(candidates):
            second_children += 1
            source = insert_theta_leaf(
                source_six, candidate, 6, "theta2_k7_second"
            )
            relation = fixed_relation(
                prepare_incidence(source, ignore_label_values=False),
                target_pattern,
            )
            if relation == "none":
                continue
            require(relation == "isomorphic", f"theta2 k7 relation:{relation}")
            second_relation_census["isomorphic"] += 1
            row = anchor_row(
                origin="theta2_physical_k7",
                port_count=7,
                relation=relation,
                source=source,
                target=target,
                locator={
                    "source_index": root.source_index,
                    "target_index": root.target_index,
                    "permutation_index": root.permutation_index,
                    "port_permutation": list(root.permutation),
                    "base_raw_id": root.base_raw_id,
                    "first_restored_role": first_role,
                    "first_source_insertion_index": first_index,
                    "first_source_insertion": first_candidate,
                    "restored_role": second_role,
                    "source_insertion_index": insertion_index,
                    "source_insertion": candidate,
                },
            )
            anchors.append(row)
            seed_pairs.append(
                ThetaSeedPair(
                    anchor_key=row["anchor_key"],
                    origin=row["origin"],
                    source=source,
                    target=target,
                )
            )

    require(second_children == 288, f"theta2 second children:{second_children}")
    require(second_relation_census == {"isomorphic": 32}, f"theta2 second equality:{second_relation_census}")
    marginalized_audit = _audit_marginalized_theta_restorations(
        sources, marginalized_roots, seed_pairs
    )
    marginalized_dummy_multiplicity = marginalized_audit["dummy_multiplicity"]
    marginalized_full_isomorphisms = marginalized_audit["isomorphic_by_depth"]
    by_origin = collections.Counter(row["origin"] for row in anchors)
    require(
        by_origin
        == {
            "theta2_physical_k5": 24,
            "theta2_physical_k6": 40,
            "theta2_physical_k7": 32,
        },
        f"theta2 physical census:{by_origin}",
    )

    stage = {
        "theta2_base_raw_presentations": 2_946_240,
        "theta2_selected_graph_isomorphisms_before_boundary_filter": 256,
        "theta2_incoming_boundary_mismatches": incoming_boundary_mismatches,
        "theta2_excluded_full_restoration_isomorphic_paths": sum(
            marginalized_full_isomorphisms.values()
        ),
        "theta2_base_exact_equalities": 80,
        "theta2_no_dummy_physical_equalities": 24,
        "theta2_dummy_restoration_roots": 56,
        "theta2_first_layer_role_requests": first_requests,
        "theta2_six_port_children": first_children,
        "theta2_six_port_exact_equalities": sum(first_relation_census.values()),
        "theta2_six_port_physical_equalities": 40,
        "theta2_six_port_continuations": len(continuations),
        "theta2_seven_port_children": second_children,
        "theta2_seven_port_exact_equalities": sum(second_relation_census.values()),
    }
    diagnostics = {
        "base_relation_census": dict(sorted(base_relation_census.items())),
        "incoming_boundary_mismatches": incoming_boundary_mismatches,
        "marginalized_incoming_dummy_multiplicity": {
            str(key): value
            for key, value in sorted(marginalized_dummy_multiplicity.items())
        },
        "marginalized_incoming_full_isomorphic_paths_by_depth": {
            str(key): value
            for key, value in sorted(marginalized_full_isomorphisms.items())
        },
        "marginalized_root_movement_mapping": {
            "claim": (
                "Remove the restored label occupying target INCOMING, compact "
                "the remaining labels, and compare both restricted sides to "
                "the canonical theta seed graph-pair classes.  The removed "
                "label is therefore one downstream probe after root movement."
            ),
            "canonical_seed_class_count": marginalized_audit[
                "canonical_seed_class_count"
            ],
            "canonical_seed_class_member_census": {
                str(key): value
                for key, value in sorted(
                    marginalized_audit[
                        "canonical_seed_class_member_census"
                    ].items()
                )
            },
            "mapped_by_seed_origin": dict(
                sorted(marginalized_audit["mapped_by_seed_origin"].items())
            ),
            "mapped_by_seed_class": dict(
                sorted(marginalized_audit["mapped_by_seed_class"].items())
            ),
            "terminal_paths_with_every_prefix_checked": len(
                marginalized_audit["mapping_rows"]
            ),
            "prefix_exact_equality_checks": marginalized_audit[
                "prefix_exact_equality_checks"
            ],
            "mapping_rows": marginalized_audit["mapping_rows"],
            "mapping_rows_sha256": marginalized_audit[
                "mapping_rows_sha256"
            ],
            "mapped": len(marginalized_audit["mapping_rows"]),
            "unmatched": marginalized_audit["unmatched"],
        },
        "base_dummy_multiplicity": {
            str(key): value for key, value in sorted(dummy_multiplicity.items())
        },
        "first_layer_relation_census": dict(sorted(first_relation_census.items())),
        "second_layer_relation_census": dict(sorted(second_relation_census.items())),
    }
    return anchors, stage, diagnostics


def enumerate_non_four_anchor_universe() -> dict[str, Any]:
    """Derive the complete 1+36+96 non-four-core semantic-key multiset."""

    tree = three_port_tree()
    tree_rows = [
        anchor_row(
            origin="tree_physical_k3",
            port_count=3,
            relation="isomorphic",
            source=tree,
            target=tree,
            locator={},
        )
    ]
    cycle_rows, cycle_stage, cycle_diagnostics = _enumerate_cycle()
    theta_rows, theta_stage, theta_diagnostics = _enumerate_theta2()
    anchors = tree_rows + cycle_rows + theta_rows
    require(len(anchors) == 133, f"non-four anchors:{len(anchors)}")
    keys = [row["anchor_key"] for row in anchors]
    require(len(keys) == len(set(keys)), "duplicate semantic anchor key")

    by_origin = collections.Counter(row["origin"] for row in anchors)
    by_relation = collections.Counter(row["relation"] for row in anchors)
    by_port_count = collections.Counter(row["port_count"] for row in anchors)
    expected_origin = {
        "cycle_physical_k3": 24,
        "cycle_restored_physical_k4": 12,
        "theta2_physical_k5": 24,
        "theta2_physical_k6": 40,
        "theta2_physical_k7": 32,
        "tree_physical_k3": 1,
    }
    require(by_origin == expected_origin, f"origin census:{by_origin}")
    require(by_relation == {"isomorphic": 117, "triangle": 16}, f"relation census:{by_relation}")
    require(by_port_count == {3: 25, 4: 12, 5: 24, 6: 40, 7: 32}, f"port census:{by_port_count}")

    return {
        "primitive_counts": {
            "tree_sources": 1,
            "cycle_sources": 2,
            "cycle_targets": 1120,
            "cycle_port_permutations": 6,
            "theta2_sources": 4,
            "theta2_selected_incoming_targets": 1983,
            "theta2_marginalized_incoming_targets": 4155,
            "theta2_targets": 6138,
            "theta2_port_permutations": 120,
        },
        "stage_counts": {
            **cycle_stage,
            **theta_stage,
        },
        "census": {
            "total": len(anchors),
            "by_origin": dict(sorted(by_origin.items())),
            "by_relation": dict(sorted(by_relation.items())),
            "by_port_count": {
                str(key): value for key, value in sorted(by_port_count.items())
            },
            "unique_anchor_keys": len(set(keys)),
        },
        "anchors": anchors,
        "ordered_anchor_key_sha256": digest(sorted(keys)),
        "diagnostics": {
            "cycle": cycle_diagnostics,
            "theta2": theta_diagnostics,
        },
    }


__all__ = [
    "IndependentUniverseError",
    "canonical_bytes",
    "digest",
    "enumerate_non_four_anchor_universe",
]
