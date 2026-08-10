#!/usr/bin/env python3
"""First-principles primitive cycle/theta enumeration.

The generator starts from the two graph-theoretic kernels forced by binary
degree and cyclomatic number, then enumerates reticulation placements and all
edge orientations satisfying the rooted bidegrees.  No catalogue or frozen
topology list is read.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations
from collections import defaultdict
from typing import Any, Iterable, Iterator, Mapping, Sequence

from graphcanon import ColouredMixedGraph, MixedEdge, canonical_json, canonicalize, digest


@dataclass(frozen=True)
class LocalPresentation:
    core: str
    port_count: int
    vertices: tuple[str, ...]
    internal_edges: tuple[tuple[str, str], ...]
    directed_internal_edges: tuple[tuple[str, str], ...]
    port_parents: tuple[str, ...]
    entry: str
    reticulations: tuple[str, ...]
    path_words: tuple[tuple[str, ...], ...]
    provenance: tuple[Any, ...]

    @property
    def outgoing_parents(self) -> tuple[str, ...]:
        return tuple(v for v in self.port_parents if v != self.entry)


def weak_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first,) + tail


def _theta_structure(counts: tuple[int, int, int]) -> tuple[
    tuple[str, ...], tuple[tuple[str, ...], ...], tuple[tuple[str, str], ...], tuple[str, ...]
]:
    vertices = ["pole_a", "pole_b"]
    paths: list[tuple[str, ...]] = []
    ports: list[str] = []
    edges: list[tuple[str, str]] = []
    for path_index, interior_count in enumerate(counts):
        interior = [f"q{path_index}_{j}" for j in range(interior_count)]
        ports.extend(interior)
        path = ("pole_a", *interior, "pole_b")
        paths.append(path)
        vertices.extend(interior)
        edges.extend((u, v) for u, v in zip(path, path[1:]))
    return tuple(vertices), tuple(paths), tuple(edges), tuple(ports)


def _cycle_structure(port_count: int) -> tuple[
    tuple[str, ...], tuple[tuple[str, ...], ...], tuple[tuple[str, str], ...], tuple[str, ...]
]:
    vertices = tuple(f"q0_{i}" for i in range(port_count))
    edges = tuple((vertices[i], vertices[(i + 1) % port_count]) for i in range(port_count))
    return vertices, (vertices + (vertices[0],),), edges, vertices


def _is_acyclic(vertices: Sequence[str], arcs: Sequence[tuple[str, str]]) -> bool:
    indegree = {v: 0 for v in vertices}
    children: dict[str, list[str]] = {v: [] for v in vertices}
    for tail, head in arcs:
        indegree[head] += 1
        children[tail].append(head)
    queue = [v for v in vertices if indegree[v] == 0]
    visited = 0
    while queue:
        vertex = queue.pop()
        visited += 1
        for child in children[vertex]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    return visited == len(vertices)


def _reachable_from(entry: str, vertices: Sequence[str], arcs: Sequence[tuple[str, str]]) -> bool:
    children: dict[str, list[str]] = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    seen = {entry}
    stack = [entry]
    while stack:
        vertex = stack.pop()
        for child in children[vertex]:
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return seen == set(vertices)


def _rooted_tree_child(
    vertices: Sequence[str],
    arcs: Sequence[tuple[str, str]],
    port_parents: Sequence[str],
    entry: str,
    reticulations: set[str],
) -> bool:
    children: dict[str, list[str]] = defaultdict(list)
    for tail, head in arcs:
        children[tail].append(head)
    outgoing_port = set(port_parents) - {entry}
    for vertex in vertices:
        internal_children = children[vertex]
        has_leaf_child = vertex in outgoing_port
        if vertex in reticulations:
            if has_leaf_child:
                continue
            if len(internal_children) != 1 or internal_children[0] in reticulations:
                return False
        elif not has_leaf_child and not any(child not in reticulations for child in internal_children):
            return False
    return True


def _strong_arrow_tail(
    vertices: Sequence[str],
    arcs: Sequence[tuple[str, str]],
    port_parents: Sequence[str],
    reticulations: set[str],
) -> bool:
    """Locked local criterion for every admissible rooting to be tree-child.

    A retained arrow is precisely an internal arc whose head is a
    reticulation.  Its tail must have two other ordinary (undirected after
    semi-deorientation) incidences.  This excludes both a reticulation child
    of a reticulation and a tree vertex with two reticulation children.
    """

    undirected_incidence = {v: 0 for v in vertices}
    arrow_tails: list[str] = []
    for tail, head in arcs:
        if head in reticulations:
            arrow_tails.append(tail)
        else:
            undirected_incidence[tail] += 1
            undirected_incidence[head] += 1
    for parent in port_parents:
        undirected_incidence[parent] += 1
    return all(undirected_incidence[tail] == 2 for tail in arrow_tails)


def _orientations(
    vertices: Sequence[str],
    edges: Sequence[tuple[str, str]],
    port_parents: Sequence[str],
    entry: str,
    reticulations: set[str],
    audit: dict[str, int] | None = None,
) -> Iterator[tuple[tuple[str, str], ...]]:
    audit = audit if audit is not None else {}
    if entry in reticulations:
        audit["rejected_entry_reticulation"] = audit.get("rejected_entry_reticulation", 0) + 1
        return
    internal_degree = {v: 0 for v in vertices}
    incident: dict[str, list[int]] = defaultdict(list)
    for index, (u, v) in enumerate(edges):
        internal_degree[u] += 1
        internal_degree[v] += 1
        incident[u].append(index)
        incident[v].append(index)
    outgoing_boundary = {v: int(v in port_parents and v != entry) for v in vertices}
    incoming_boundary = {v: int(v == entry) for v in vertices}
    target_out = {
        v: (1 if v in reticulations else 2) - outgoing_boundary[v] for v in vertices
    }
    target_in = {
        v: (2 if v in reticulations else 1) - incoming_boundary[v] for v in vertices
    }
    if any(target_out[v] < 0 or target_in[v] < 0 for v in vertices):
        return
    if any(target_out[v] + target_in[v] != internal_degree[v] for v in vertices):
        return

    out_count = {v: 0 for v in vertices}
    in_count = {v: 0 for v in vertices}
    remaining = dict(internal_degree)
    chosen: list[tuple[str, str] | None] = [None] * len(edges)

    def recurse(edge_index: int) -> Iterator[tuple[tuple[str, str], ...]]:
        if edge_index == len(edges):
            arcs = tuple(item for item in chosen if item is not None)
            if out_count != target_out or in_count != target_in:
                return
            audit["bidegree_orientation_completions"] = audit.get("bidegree_orientation_completions", 0) + 1
            if not _is_acyclic(vertices, arcs):
                audit["rejected_directed_cycle"] = audit.get("rejected_directed_cycle", 0) + 1
                return
            if not _reachable_from(entry, vertices, arcs):
                audit["rejected_unreachable"] = audit.get("rejected_unreachable", 0) + 1
                return
            if not _rooted_tree_child(vertices, arcs, port_parents, entry, reticulations):
                audit["rejected_rooted_tree_child"] = audit.get("rejected_rooted_tree_child", 0) + 1
                return
            if not _strong_arrow_tail(vertices, arcs, port_parents, reticulations):
                audit["rejected_strong_arrow_tail"] = audit.get("rejected_strong_arrow_tail", 0) + 1
                return
            audit["accepted_orientations"] = audit.get("accepted_orientations", 0) + 1
            yield arcs
            return

        u, v = edges[edge_index]
        for tail, head in ((u, v), (v, u)):
            chosen[edge_index] = (tail, head)
            out_count[tail] += 1
            in_count[head] += 1
            remaining[u] -= 1
            remaining[v] -= 1
            feasible = True
            for vertex in (u, v):
                if out_count[vertex] > target_out[vertex] or in_count[vertex] > target_in[vertex]:
                    feasible = False
                if out_count[vertex] + remaining[vertex] < target_out[vertex]:
                    feasible = False
                if in_count[vertex] + remaining[vertex] < target_in[vertex]:
                    feasible = False
            if feasible:
                yield from recurse(edge_index + 1)
            remaining[u] += 1
            remaining[v] += 1
            out_count[tail] -= 1
            in_count[head] -= 1
        chosen[edge_index] = None

    yield from recurse(0)


def raw_presentations(
    port_count: int, audit: dict[str, int] | None = None
) -> Iterator[LocalPresentation]:
    if port_count < 3:
        raise ValueError("a simple ported cycle/theta needs at least three ports")
    audit = audit if audit is not None else {}

    # Cycle rank one: every internal vertex has blob degree two and therefore
    # carries exactly one boundary port.
    vertices, paths, edges, ports = _cycle_structure(port_count)
    for entry in ports:
        for reticulation in ports:
            if reticulation == entry:
                audit["cycle_entry_reticulation_pairs_excluded"] = audit.get(
                    "cycle_entry_reticulation_pairs_excluded", 0
                ) + 1
                continue
            audit["cycle_reticulation_placements"] = audit.get("cycle_reticulation_placements", 0) + 1
            retics = {reticulation}
            for arcs in _orientations(vertices, edges, ports, entry, retics, audit):
                yield LocalPresentation(
                    "cycle",
                    port_count,
                    vertices,
                    edges,
                    arcs,
                    ports,
                    entry,
                    tuple(sorted(retics)),
                    paths,
                    ("cycle", port_count, entry, reticulation),
                )

    # Cycle rank two: after suppressing all port-bearing path vertices, the
    # two cubic poles are joined by three paths.  Two empty words would be
    # parallel pole-to-pole edges and are excluded by the locked simple graph.
    for counts in weak_compositions(port_count, 3):
        if sum(value == 0 for value in counts) > 1:
            audit["theta_parallel_path_compositions_excluded"] = audit.get(
                "theta_parallel_path_compositions_excluded", 0
            ) + 1
            continue
        audit["theta_simple_path_compositions"] = audit.get("theta_simple_path_compositions", 0) + 1
        vertices, paths, edges, ports = _theta_structure(counts)
        for entry in ports:
            for reticulation_pair in combinations((v for v in vertices if v != entry), 2):
                audit["theta_reticulation_placements"] = audit.get("theta_reticulation_placements", 0) + 1
                retics = set(reticulation_pair)
                for arcs in _orientations(vertices, edges, ports, entry, retics, audit):
                    yield LocalPresentation(
                        "theta",
                        port_count,
                        vertices,
                        edges,
                        arcs,
                        ports,
                        entry,
                        tuple(sorted(retics)),
                        paths,
                        ("theta", counts, entry, tuple(sorted(retics))),
                    )


def boundary_name(parent: str) -> str:
    return f"boundary::{parent}"


def mixed_graph(
    presentation: LocalPresentation,
    outgoing_labels: Mapping[str, int] | None = None,
    relation_mode: bool = False,
) -> ColouredMixedGraph:
    reticulations = set(presentation.reticulations)
    colors: dict[str, tuple[Any, ...]] = {
        vertex: ("INTERNAL", "R" if vertex in reticulations else "T")
        for vertex in presentation.vertices
    }
    for parent in presentation.port_parents:
        boundary = boundary_name(parent)
        if parent == presentation.entry:
            colors[boundary] = ("PORT", "IN")
        elif outgoing_labels is None or relation_mode:
            colors[boundary] = ("PORT", "OUT")
        else:
            colors[boundary] = ("PORT", "OUT", int(outgoing_labels[parent]))

    edges: list[MixedEdge] = []
    arc_set = set(presentation.directed_internal_edges)
    for u, v in presentation.internal_edges:
        if (u, v) in arc_set:
            tail, head = u, v
        elif (v, u) in arc_set:
            tail, head = v, u
        else:
            raise AssertionError("every internal edge must be oriented")
        edges.append(MixedEdge("A", tail, head) if head in reticulations else MixedEdge("U", u, v))
    for parent in presentation.port_parents:
        edges.append(MixedEdge("U", parent, boundary_name(parent)))
    return ColouredMixedGraph(colors, tuple(edges)).normalized()


def _canonical_edges(graph: ColouredMixedGraph, vertex_map: Mapping[str, int]) -> tuple[
    tuple[tuple[Any, ...], ...], dict[tuple[Any, ...], int]
]:
    keyed = []
    for edge in graph.edges:
        a, b = vertex_map[edge.u], vertex_map[edge.v]
        if edge.kind == "A":
            record = ("A", a, b)
        else:
            record = (edge.kind, min(a, b), max(a, b))
        keyed.append(record)
    ordered = tuple(sorted(keyed))
    return ordered, {record: index for index, record in enumerate(ordered)}


def transport_for(
    presentation: LocalPresentation,
    graph: ColouredMixedGraph,
    vertex_map: Mapping[str, int],
) -> dict[str, Any]:
    canonical_edges, edge_lookup = _canonical_edges(graph, vertex_map)
    raw_edge_map: dict[str, int] = {}
    for edge in graph.edges:
        a, b = vertex_map[edge.u], vertex_map[edge.v]
        record = ("A", a, b) if edge.kind == "A" else (edge.kind, min(a, b), max(a, b))
        raw_id = f"{edge.kind}:{edge.u}:{edge.v}"
        raw_edge_map[raw_id] = edge_lookup[record]

    retic_order = sorted(presentation.reticulations, key=lambda vertex: vertex_map[vertex])
    parent_edges: list[list[int]] = []
    parent_swaps: list[bool] = []
    for reticulation in retic_order:
        raw_incoming: list[tuple[str, int]] = []
        for edge in graph.edges:
            if edge.kind == "A" and edge.v == reticulation:
                record = ("A", vertex_map[edge.u], vertex_map[edge.v])
                raw_incoming.append((edge.u, edge_lookup[record]))
        raw_incoming.sort()
        canonical_incoming = sorted(index for _parent, index in raw_incoming)
        if len(canonical_incoming) != 2:
            raise AssertionError("each reticulation must have two incoming arrow edges")
        parent_edges.append(canonical_incoming)
        parent_swaps.append([index for _parent, index in raw_incoming] != canonical_incoming)

    return {
        "vertex_map": {vertex: vertex_map[vertex] for vertex in sorted(vertex_map)},
        "edge_map": dict(sorted(raw_edge_map.items())),
        "canonical_edges": [list(record) for record in canonical_edges],
        "port_map": {
            ("IN" if parent == presentation.entry else f"RAW::{parent}"):
            vertex_map[boundary_name(parent)]
            for parent in sorted(presentation.port_parents)
        },
        "reticulation_order": [vertex_map[v] for v in retic_order],
        "incoming_parent_edges": parent_edges,
        "inheritance_parent_swapped": parent_swaps,
    }


def validation_trace(presentation: LocalPresentation) -> dict[str, Any]:
    reticulations = set(presentation.reticulations)
    arcs = presentation.directed_internal_edges
    graph = mixed_graph(presentation)
    degree = {v: 0 for v in graph.colors}
    for edge in graph.edges:
        degree[edge.u] += 1
        degree[edge.v] += 1
    internal_edge_count = len(presentation.internal_edges)
    cycle_rank = internal_edge_count - len(presentation.vertices) + 1
    return {
        "simple_standard": all(value == 3 for v, value in degree.items() if graph.colors[v][0] == "INTERNAL")
        and all(value == 1 for v, value in degree.items() if graph.colors[v][0] == "PORT"),
        "entry_not_reticulation": presentation.entry not in reticulations,
        "binary_bidegrees": True,  # enforced by target in/out quotas in `_orientations`
        "acyclic": _is_acyclic(presentation.vertices, arcs),
        "reachable_from_incoming_boundary": _reachable_from(presentation.entry, presentation.vertices, arcs),
        "rooted_tree_child": _rooted_tree_child(
            presentation.vertices, arcs, presentation.port_parents, presentation.entry, reticulations
        ),
        "strong_arrow_tail": _strong_arrow_tail(
            presentation.vertices, arcs, presentation.port_parents, reticulations
        ),
        "cycle_rank": cycle_rank,
        "reticulation_count": len(reticulations),
        "level_two": len(reticulations) <= 2,
        "core_rank_matches_reticulations": cycle_rank == len(reticulations),
    }


def _presentation_orientation_code(
    presentation: LocalPresentation, vertex_map: Mapping[str, int]
) -> tuple[tuple[int, int], ...]:
    return tuple(sorted((vertex_map[u], vertex_map[v]) for u, v in presentation.directed_internal_edges))


def enumerate_role_classes(port_count: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    classes: dict[str, dict[str, Any]] = {}
    raw_count = 0
    raw_core_counts: dict[str, int] = defaultdict(int)
    audit_counts: dict[str, int] = {}
    for presentation in raw_presentations(port_count, audit_counts):
        raw_count += 1
        raw_core_counts[presentation.core] += 1
        trace = validation_trace(presentation)
        if not all(
            trace[key]
            for key in (
                "simple_standard",
                "entry_not_reticulation",
                "binary_bidegrees",
                "acyclic",
                "reachable_from_incoming_boundary",
                "rooted_tree_child",
                "strong_arrow_tail",
                "level_two",
                "core_rank_matches_reticulations",
            )
        ):
            raise AssertionError((presentation, trace))
        graph = mixed_graph(presentation)
        code, vertex_map = canonicalize(graph)
        role_hash = digest(code)
        transport = transport_for(presentation, graph, vertex_map)
        raw_record = {
            "provenance": list(presentation.provenance),
            "vertex_transport": transport["vertex_map"],
            "edge_transport": transport["edge_map"],
            "port_transport": transport["port_map"],
            "reticulation_transport": transport["reticulation_order"],
            "inheritance_parent_swapped": transport["inheritance_parent_swapped"],
        }
        orientation_code = _presentation_orientation_code(presentation, vertex_map)
        if role_hash not in classes:
            classes[role_hash] = {
                "role_hash": role_hash,
                "canonical_graph": code,
                "representative": presentation,
                "representative_vertex_map": dict(vertex_map),
                "representative_transport": transport,
                "representative_orientation_code": orientation_code,
                "raw_transports": [raw_record],
            }
        else:
            record = classes[role_hash]
            record["raw_transports"].append(raw_record)
            if orientation_code < record["representative_orientation_code"]:
                record["representative"] = presentation
                record["representative_vertex_map"] = dict(vertex_map)
                record["representative_transport"] = transport
                record["representative_orientation_code"] = orientation_code

    result = [classes[key] for key in sorted(classes)]
    summary = {
        "port_count": port_count,
        "raw_presentations": raw_count,
        "raw_core_counts": dict(sorted(raw_core_counts.items())),
        "role_classes": len(result),
        "orientation_audit": dict(sorted(audit_counts.items())),
        "role_core_counts": dict(
            sorted(
                (core, sum(item["representative"].core == core for item in result))
                for core in ("cycle", "theta")
            )
        ),
    }
    return result, summary


def serializable_role_class(role: Mapping[str, Any]) -> dict[str, Any]:
    from rootings import rooting_census

    presentation: LocalPresentation = role["representative"]
    graph = mixed_graph(presentation)
    vertex_map = role["representative_vertex_map"]
    canonical_edges, _edge_lookup = _canonical_edges(graph, vertex_map)
    return {
        "schema": "primitive-role-v1",
        "role_hash": role["role_hash"],
        "core": presentation.core,
        "port_count": presentation.port_count,
        "canonical_graph": role["canonical_graph"],
        "canonical_edges": [list(item) for item in canonical_edges],
        "representative_directed_internal_edges": [
            list(item) for item in role["representative_orientation_code"]
        ],
        "representative_transport": role["representative_transport"],
        "validation": validation_trace(presentation),
        "independent_admissible_rooting_census": rooting_census(
            reconstruct_graph({"canonical_graph": role["canonical_graph"]})
        ),
        "raw_transports": role["raw_transports"],
        "raw_transport_count": len(role["raw_transports"]),
    }


def enumerate_labelled_classes(
    port_count: int,
    roles: Sequence[Mapping[str, Any]] | None = None,
    role_summary: Mapping[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    if roles is None or role_summary is None:
        roles, role_summary = enumerate_role_classes(port_count)
    labelled: dict[str, dict[str, Any]] = {}
    role_transport_records: list[dict[str, Any]] = []
    raw_label_assignments = 0
    for role in roles:
        presentation: LocalPresentation = role["representative"]
        outgoing = tuple(sorted(presentation.outgoing_parents))
        for labels in permutations(range(1, port_count)):
            raw_label_assignments += 1
            assignment = dict(zip(outgoing, labels))
            graph = mixed_graph(presentation, assignment)
            code, vertex_map = canonicalize(graph)
            graph_hash = digest(code)
            transport = transport_for(presentation, graph, vertex_map)
            port_labels = {0: vertex_map[boundary_name(presentation.entry)]}
            port_labels.update({assignment[parent]: vertex_map[boundary_name(parent)] for parent in outgoing})
            directed_arcs = []
            for tail, head in presentation.directed_internal_edges:
                directed_arcs.append((vertex_map[tail], vertex_map[head]))
            directed_arcs.append(
                (vertex_map[boundary_name(presentation.entry)], vertex_map[presentation.entry])
            )
            for parent in outgoing:
                directed_arcs.append((vertex_map[parent], vertex_map[boundary_name(parent)]))
            canonical_edges, edge_lookup = _canonical_edges(graph, vertex_map)
            edge_by_record = {record: index for index, record in enumerate(canonical_edges)}
            directed_edge_records = []
            for tail, head in directed_arcs:
                undirected_record = ("U", min(tail, head), max(tail, head))
                arrow_record = ("A", tail, head)
                if arrow_record in edge_by_record:
                    edge_index = edge_by_record[arrow_record]
                else:
                    edge_index = edge_by_record[undirected_record]
                directed_edge_records.append((edge_index, tail, head))
            reticulation_order = sorted(vertex_map[v] for v in presentation.reticulations)
            incoming_parent_edges = []
            for reticulation in reticulation_order:
                incoming_parent_edges.append(
                    sorted(edge_index for edge_index, _tail, head in directed_edge_records if head == reticulation)
                )
            sink_labels = sorted(
                label for parent, label in assignment.items() if parent in set(presentation.reticulations)
            )
            raw_to_labelled = {
                "role_hash": role["role_hash"],
                "outgoing_assignment": {parent: assignment[parent] for parent in sorted(assignment)},
                "vertex_map": {name: vertex_map[name] for name in sorted(vertex_map)},
                "edge_map": transport["edge_map"],
                "port_label_vertices": {str(k): port_labels[k] for k in sorted(port_labels)},
                "reticulation_order": reticulation_order,
                "incoming_parent_edges": incoming_parent_edges,
            }
            role_transport_records.append({"graph_hash": graph_hash, **raw_to_labelled})
            candidate = {
                "schema": "primitive-labelled-v1",
                "graph_hash": graph_hash,
                "core": presentation.core,
                "port_count": port_count,
                "canonical_graph": code,
                "canonical_edges": [list(record) for record in canonical_edges],
                "directed_edges": [list(record) for record in sorted(directed_edge_records)],
                "port_label_vertices": {str(k): port_labels[k] for k in sorted(port_labels)},
                "entry_vertex": vertex_map[presentation.entry],
                "reticulations": reticulation_order,
                "incoming_parent_edges": incoming_parent_edges,
                "sink_labels": sink_labels,
                "validation": validation_trace(presentation),
                "role_hash": role["role_hash"],
            }
            if graph_hash in labelled:
                if canonical_json(labelled[graph_hash]) != canonical_json(candidate):
                    raise AssertionError("canonical hash collision or inconsistent representative")
            else:
                labelled[graph_hash] = candidate

    records = [labelled[key] for key in sorted(labelled)]
    summary = {
        **dict(role_summary),
        "raw_label_assignments": raw_label_assignments,
        "labelled_classes": len(records),
        "labelled_core_counts": dict(
            sorted((core, sum(item["core"] == core for item in records)) for core in ("cycle", "theta"))
        ),
        "raw_to_labelled_transport_records": len(role_transport_records),
    }
    return records, summary, role_transport_records


def reconstruct_graph(record: Mapping[str, Any]) -> ColouredMixedGraph:
    code = record["canonical_graph"]
    colors = {str(index): tuple(color) for index, color in enumerate(code["colors"])}
    edges: list[MixedEdge] = []
    cursor = 0
    size = int(code["order_size"])
    for i in range(size):
        for j in range(i + 1, size):
            symbol = code["upper_triangle"][cursor]
            cursor += 1
            if symbol == "1":
                edges.append(MixedEdge("U", str(i), str(j)))
            elif symbol == "2":
                edges.append(MixedEdge("A", str(i), str(j)))
            elif symbol == "3":
                edges.append(MixedEdge("A", str(j), str(i)))
            elif symbol == "4":
                edges.append(MixedEdge("MATCH", str(i), str(j)))
            elif symbol != "0":
                raise ValueError(f"bad adjacency symbol {symbol}")
    return ColouredMixedGraph(colors, tuple(edges)).normalized()
