#!/usr/bin/env python3
"""Canonical decorated ordered source-target relations."""

from __future__ import annotations

from itertools import combinations
from typing import Any, Iterable, Mapping, Sequence

from graphcanon import ColouredMixedGraph, MixedEdge, canonicalize, digest, canonical_json
from primitive import reconstruct_graph
from fourier import (
    displayed_parameter_signature,
    parameter_permutation_witness,
    verify_parameter_permutation_witness,
)


def _edge_records(graph: ColouredMixedGraph, vertex_map: Mapping[str, int]) -> tuple[
    list[list[Any]], dict[str, int]
]:
    keyed: list[tuple[tuple[Any, ...], str]] = []
    for edge in graph.edges:
        a, b = vertex_map[edge.u], vertex_map[edge.v]
        record = ("A", a, b) if edge.kind == "A" else (edge.kind, min(a, b), max(a, b))
        raw_id = f"{edge.kind}:{edge.u}:{edge.v}"
        keyed.append((record, raw_id))
    keyed.sort()
    return [list(record) for record, _raw in keyed], {
        raw_id: index for index, (_record, raw_id) in enumerate(keyed)
    }


def _port_roles(record: Mapping[str, Any], decorations: Mapping[str, Iterable[int]] | None) -> dict[int, tuple[str, ...]]:
    p = int(record["port_count"])
    roles: dict[int, list[str]] = {0: ["IN"]}
    for label in range(1, p):
        roles[label] = ["OUT"]
    sink = set(int(value) for value in record.get("sink_labels", ()))
    for label in sink:
        roles[label].append("SINK")
    if decorations:
        for role, labels in decorations.items():
            for label in labels:
                label = int(label)
                if label not in roles:
                    raise ValueError(f"decoration references absent port {label}")
                roles[label].append(str(role).upper())
    return {label: tuple(sorted(items)) for label, items in roles.items()}


def decorated_relation(
    source: Mapping[str, Any],
    target: Mapping[str, Any],
    port_map: Mapping[int, int] | None = None,
    source_decorations: Mapping[str, Iterable[int]] | None = None,
    target_decorations: Mapping[str, Iterable[int]] | None = None,
    classification: str = "unclassified",
    witness: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    p = int(source["port_count"])
    if p != int(target["port_count"]):
        raise ValueError("source and target need the same port count")
    port_map = dict(port_map or {label: label for label in range(p)})
    if set(port_map) != set(range(p)) or set(port_map.values()) != set(range(p)):
        raise ValueError("port correspondence must be a complete bijection")
    if port_map[0] != 0:
        raise ValueError("the incoming boundary must match the incoming boundary")

    source_graph = reconstruct_graph(source)
    target_graph = reconstruct_graph(target)
    source_ports = {int(label): str(vertex) for label, vertex in source["port_label_vertices"].items()}
    target_ports = {int(label): str(vertex) for label, vertex in target["port_label_vertices"].items()}
    source_roles = _port_roles(source, source_decorations)
    target_roles = _port_roles(target, target_decorations)

    colors: dict[str, tuple[Any, ...]] = {}
    edges: list[MixedEdge] = []
    for side, graph, ports, roles in (
        ("SOURCE", source_graph, source_ports, source_roles),
        ("TARGET", target_graph, target_ports, target_roles),
    ):
        by_vertex = {vertex: label for label, vertex in ports.items()}
        for vertex, color in graph.colors.items():
            name = f"{side}::{vertex}"
            if vertex in by_vertex:
                colors[name] = (side, "PORT", *roles[by_vertex[vertex]])
            else:
                colors[name] = (side, *color)
        for edge in graph.edges:
            edges.append(MixedEdge(edge.kind, f"{side}::{edge.u}", f"{side}::{edge.v}"))
    for source_label, target_label in sorted(port_map.items()):
        edges.append(
            MixedEdge(
                "MATCH",
                f"SOURCE::{source_ports[source_label]}",
                f"TARGET::{target_ports[target_label]}",
            )
        )
    relation_graph = ColouredMixedGraph(colors, tuple(edges)).normalized()
    relation_code, vertex_map = canonicalize(relation_graph)
    canonical_edges, raw_edge_map = _edge_records(relation_graph, vertex_map)
    source_vertex_transport = {
        vertex: vertex_map[f"SOURCE::{vertex}"] for vertex in sorted(source_graph.colors, key=int)
    }
    target_vertex_transport = {
        vertex: vertex_map[f"TARGET::{vertex}"] for vertex in sorted(target_graph.colors, key=int)
    }
    def side_edge_transport(
        side: str,
        graph: ColouredMixedGraph,
        primitive: Mapping[str, Any],
    ) -> dict[str, int]:
        primitive_lookup = {tuple(item): index for index, item in enumerate(primitive["canonical_edges"])}
        result: dict[str, int] = {}
        for edge in graph.edges:
            u, v = int(edge.u), int(edge.v)
            primitive_record = (
                ("A", u, v)
                if edge.kind == "A"
                else (edge.kind, min(u, v), max(u, v))
            )
            primitive_index = primitive_lookup[primitive_record]
            raw_id = f"{edge.kind}:{side}::{edge.u}:{side}::{edge.v}"
            result[str(primitive_index)] = raw_edge_map[raw_id]
        return dict(sorted(result.items(), key=lambda item: int(item[0])))

    source_edge_transport = side_edge_transport("SOURCE", source_graph, source)
    target_edge_transport = side_edge_transport("TARGET", target_graph, target)
    source_parent_transport = [
        [source_edge_transport[str(edge)] for edge in pair]
        for pair in source["incoming_parent_edges"]
    ]
    target_parent_transport = [
        [target_edge_transport[str(edge)] for edge in pair]
        for pair in target["incoming_parent_edges"]
    ]
    mask_transport: dict[str, int] = {}
    for source_mask in range(1 << p):
        target_mask = 0
        for source_label, target_label in port_map.items():
            if source_mask >> source_label & 1:
                target_mask |= 1 << target_label
        mask_transport[str(source_mask)] = target_mask

    binding_body = {
        "source_graph_hash": source["graph_hash"],
        "target_graph_hash": target["graph_hash"],
        "direction": "source_to_target",
        "port_map": {str(k): v for k, v in sorted(port_map.items())},
        "relation_graph_hash": digest(relation_code),
        "classification": classification,
        "witness": witness,
    }
    record = {
        "schema": "decorated-directed-relation-v1",
        "source_graph_hash": source["graph_hash"],
        "target_graph_hash": target["graph_hash"],
        "direction": "source_to_target",
        "port_count": p,
        "port_map": {str(k): v for k, v in sorted(port_map.items())},
        "source_port_roles": {str(k): list(v) for k, v in sorted(source_roles.items())},
        "target_port_roles": {str(k): list(v) for k, v in sorted(target_roles.items())},
        "canonical_relation_graph": relation_code,
        "relation_graph_hash": digest(relation_code),
        "canonical_relation_edges": canonical_edges,
        "source_vertex_transport": source_vertex_transport,
        "target_vertex_transport": target_vertex_transport,
        "source_edge_transport": source_edge_transport,
        "target_edge_transport": target_edge_transport,
        "source_reticulation_transport": [
            source_vertex_transport[str(vertex)] for vertex in source["reticulations"]
        ],
        "target_reticulation_transport": [
            target_vertex_transport[str(vertex)] for vertex in target["reticulations"]
        ],
        "source_inheritance_parent_edge_transport": source_parent_transport,
        "target_inheritance_parent_edge_transport": target_parent_transport,
        "source_port_vertex_transport": {
            str(label): source_vertex_transport[vertex] for label, vertex in sorted(source_ports.items())
        },
        "target_port_vertex_transport": {
            str(label): target_vertex_transport[vertex] for label, vertex in sorted(target_ports.items())
        },
        "raw_relation_edge_transport": raw_edge_map,
        "fourier_mask_transport": mask_transport,
        "classification": classification,
        "witness": witness,
        "witness_binding_hash": digest(binding_body),
    }
    record["relation_id"] = digest(record)
    return record


def _triangle_sets(graph: ColouredMixedGraph) -> list[tuple[str, str, str]]:
    internal = [vertex for vertex, color in graph.colors.items() if color[0] == "INTERNAL"]
    adjacent = {frozenset((edge.u, edge.v)) for edge in graph.edges}
    return [
        tuple(sorted(triple, key=int))
        for triple in combinations(internal, 3)
        if all(frozenset(pair) in adjacent for pair in combinations(triple, 2))
    ]


def _canonical_record_graph_hash(graph: ColouredMixedGraph) -> str:
    code, _vertex_map = canonicalize(graph)
    return digest(code)


def ordinary_t_variants(record: Mapping[str, Any]) -> set[str]:
    graph = reconstruct_graph(record)
    variants: set[str] = set()
    for triangle in _triangle_sets(graph):
        triangle_set = set(triangle)
        triangle_edges = [
            edge for edge in graph.edges if edge.u in triangle_set and edge.v in triangle_set
        ]
        if len(triangle_edges) != 3:
            continue
        sinks = []
        for vertex in triangle:
            incoming = sum(edge.kind == "A" and edge.v == vertex for edge in triangle_edges)
            if incoming == 2:
                sinks.append(vertex)
        if len(sinks) != 1:
            continue
        old_sink = sinks[0]
        if graph.colors[old_sink] != ("INTERNAL", "R"):
            continue
        outside_incoming_old = any(
            edge.kind == "A" and edge.v == old_sink and edge.u not in triangle_set
            for edge in graph.edges
        )
        if outside_incoming_old:
            continue
        retained = [edge for edge in graph.edges if edge not in triangle_edges]
        for new_sink in triangle:
            if new_sink == old_sink:
                continue
            if graph.colors[new_sink] != ("INTERNAL", "T"):
                continue
            if any(
                edge.kind == "A" and edge.v == new_sink and edge.u not in triangle_set
                for edge in graph.edges
            ):
                continue
            colors = dict(graph.colors)
            colors[old_sink] = ("INTERNAL", "T")
            colors[new_sink] = ("INTERNAL", "R")
            others = [vertex for vertex in triangle if vertex != new_sink]
            edges = list(retained)
            edges.extend(MixedEdge("A", vertex, new_sink) for vertex in others)
            edges.append(MixedEdge("U", others[0], others[1]))
            candidate = ColouredMixedGraph(colors, tuple(edges)).normalized()
            variants.add(_canonical_record_graph_hash(candidate))
    return variants


def ordinary_t_related(source: Mapping[str, Any], target: Mapping[str, Any]) -> bool:
    if source["graph_hash"] == target["graph_hash"]:
        return True
    return target["graph_hash"] in ordinary_t_variants(source) or source["graph_hash"] in ordinary_t_variants(target)


def ordinary_t_relations(records: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    lookup = {record["graph_hash"]: record for record in records}
    relations: dict[str, dict[str, Any]] = {}
    raw_ordered_pairs = 0
    missing_variants: list[dict[str, str]] = []
    for source in records:
        for target_hash in sorted(ordinary_t_variants(source)):
            target = lookup.get(target_hash)
            if target is None:
                missing_variants.append({"source": source["graph_hash"], "target": target_hash})
                continue
            raw_ordered_pairs += 1
            relation = decorated_relation(
                source,
                target,
                classification="ordinary_T_topological_relation",
                witness={
                    "kind": "one_step_triangle_redirection",
                    "source_graph_hash": source["graph_hash"],
                    "target_graph_hash": target["graph_hash"],
                },
                source_decorations={"selected_support": range(1, int(source["port_count"]))},
                target_decorations={"selected_support": range(1, int(target["port_count"]))},
            )
            relations.setdefault(relation["relation_id"], relation)
    return [relations[key] for key in sorted(relations)], {
        "raw_ordered_T_pairs": raw_ordered_pairs,
        "canonical_decorated_T_relations": len(relations),
        "missing_T_variants": missing_variants,
    }


def equal_displayed_parameter_relations(records: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_signature: dict[str, list[Mapping[str, Any]]] = {}
    signature_cache: dict[str, dict[str, Any]] = {}
    for record in records:
        signature = record.get("displayed_parameter_signature") or displayed_parameter_signature(record)
        signature_cache[record["graph_hash"]] = signature
        by_signature.setdefault(signature["signature_hash"], []).append(record)

    relations: dict[str, dict[str, Any]] = {}
    collision_groups = 0
    nontrivial_pairs = 0
    non_t_pairs = 0
    for signature_hash, group in sorted(by_signature.items()):
        if len(group) < 2:
            continue
        collision_groups += 1
        ordered = sorted(group, key=lambda item: item["graph_hash"])
        for source in ordered:
            for target in ordered:
                if source["graph_hash"] == target["graph_hash"]:
                    continue
                nontrivial_pairs += 1
                witness = parameter_permutation_witness(source, target)
                if witness is None or not verify_parameter_permutation_witness(source, target, witness):
                    raise AssertionError("equal structural signature lacks a valid parameter witness")
                is_t = ordinary_t_related(source, target)
                classification = "ordinary_T" if is_t else "non_T_equal_displayed_parameter_signature"
                non_t_pairs += int(not is_t)
                relation = decorated_relation(
                    source,
                    target,
                    classification=classification,
                    witness={"signature_hash": signature_hash, **witness},
                    source_decorations={"selected_support": range(1, int(source["port_count"]))},
                    target_decorations={"selected_support": range(1, int(target["port_count"]))},
                )
                existing = relations.get(relation["relation_id"])
                if existing is not None and canonical_json(existing) != canonical_json(relation):
                    raise AssertionError("relation hash collision")
                relations[relation["relation_id"]] = relation
    summary = {
        "signature_groups": len(by_signature),
        "collision_groups": collision_groups,
        "ordered_nonidentity_pairs_before_relation_quotient": nontrivial_pairs,
        "canonical_decorated_relations": len(relations),
        "ordered_non_T_pairs_before_relation_quotient": non_t_pairs,
        "non_T_relation_ids": sorted(
            relation_id
            for relation_id, relation in relations.items()
            if relation["classification"] == "non_T_equal_displayed_parameter_signature"
        ),
    }
    return [relations[key] for key in sorted(relations)], summary
