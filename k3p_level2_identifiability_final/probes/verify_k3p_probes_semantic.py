#!/usr/bin/env python3
"""Independent semantic replay of every K3P one-/two-port probe row.

This verifier intentionally imports neither ``regenerate_k3p_probes.py`` nor
``k3p_atlas_core.py``.  It reconstructs rooted graphs from the frozen public
candidate profiles, derives the one-step root-suppressed mixed graphs, inserts
every probe leaf, recomputes marginal restrictions and displayed quartets,
and expands the literal three-sector K3P switching maps used by the six
tree--sunlet circuits.  Stored hashes are bindings, never semantic premises.

The current K3P probe registry contains no Bernstein-sign certificate.  The
generic exact Bernstein replay below is nevertheless fail-closed: if a future
registry claims one, its sparse pullback and tensor coefficients must replay.
"""

from __future__ import annotations

import argparse
import ast
import collections
import copy
import fractions
import gc
import gzip
import hashlib
import itertools
import json
import math
import os
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
TOPOLOGY = PROJECT / "input_frozen/model_independent_topology_package"
CONTRACT_PATH = TOPOLOGY / "anchor_inputs/probe_input_contract.json"
REPLAY_PATH = TOPOLOGY / "anchor_inputs/probe_input_independent_verification.json"
DEFAULT_OUTPUT = HERE / "K3P_PROBE_SEMANTIC_VERIFICATION.json"
DEFAULT_MUTATIONS = HERE / "K3P_PROBE_SEMANTIC_MUTATIONS.json"
TRANSPORT_RESTRICTION_CLAIM = (
    "exact on every parent mixed vertex, the selected mixed edge site, and "
    "the inherited ordinary triangle when present"
)


class SemanticFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SemanticFailure(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def logical_payload(value: dict[str, Any]) -> str:
    public = copy.deepcopy(value)
    public.pop("payload_sha256", None)
    public.pop("operational", None)
    return sha(public)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2, sort_keys=True).encode() + b"\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def edge_key(left: Any, right: Any) -> tuple[str, str]:
    return tuple(sorted((repr(left), repr(right))))


def graph_payload(graph: nx.DiGraph) -> dict[str, Any]:
    return {
        "nodes": [
            [repr(node), {key: repr(value) for key, value in sorted(data.items())}]
            for node, data in sorted(graph.nodes(data=True), key=lambda row: repr(row[0]))
        ],
        "edges": [
            [repr(tail), repr(head), {key: repr(value) for key, value in sorted(data.items())}]
            for tail, head, data in sorted(
                graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
            )
        ],
    }


def graph_sha(graph: nx.DiGraph) -> str:
    return sha(graph_payload(graph))


def labels_of(graph: nx.DiGraph) -> tuple[int, ...]:
    return tuple(sorted(
        data["label"] for _, data in graph.nodes(data=True)
        if isinstance(data.get("label"), int)
    ))


def validate_binary(graph: nx.DiGraph, context: str) -> None:
    require(nx.is_directed_acyclic_graph(graph), f"{context}:directed cycle")
    expected = {"root": (0, 2), "tree": (1, 2), "retic": (2, 1), "leaf": (1, 0)}
    labels = []
    for node, data in graph.nodes(data=True):
        role = data.get("role")
        require(role in expected, f"{context}:role:{node}")
        require((graph.in_degree(node), graph.out_degree(node)) == expected[role],
                f"{context}:degree:{node}")
        if isinstance(data.get("label"), int):
            labels.append(data["label"])
    require(len(labels) == len(set(labels)), f"{context}:duplicate labels")


def infer_source_leaf_labels(profile: dict[str, Any], labels: list[int]) -> dict[Any, int]:
    nodes: set[Any] = set()
    for site in profile["sites"]:
        for tail, head, _role in site["rooted_representatives"]:
            nodes.update((ast.literal_eval(tail), ast.literal_eval(head)))
    result: dict[Any, int] = {}
    for node in nodes:
        if isinstance(node, str) and node.startswith("L") and node[1:].isdigit():
            result[node] = int(node[1:])
        elif isinstance(node, tuple):
            if len(node) >= 3 and node[1] == "leaf" and isinstance(node[2], int):
                result[node] = node[2]
            elif node[:2] == ("leaf", "INCOMING"):
                result[node] = 0
            elif node and node[0] == "leaf" and isinstance(node[-1], int) \
                    and len(node) >= 2 and node[1] not in {"seg", "sink"}:
                result[node] = node[-1]
    unassigned = [
        node for node in nodes
        if isinstance(node, tuple) and node and node[0] == "leaf" and node not in result
    ]
    rank = lambda node: ({"seg": 0, "sink": 1}.get(node[1] if len(node) > 1 else "", 2), repr(node))
    remaining = iter(sorted(set(labels) - set(result.values())))
    for node in sorted(unassigned, key=rank):
        try:
            result[node] = next(remaining)
        except StopIteration as error:
            raise SemanticFailure("anchor leaf-label inference overflow") from error
    require(set(result.values()) == set(labels), "anchor leaf-label inference coverage")
    return result


def profile_graph(profile: dict[str, Any], leaf_labels: dict[Any, int], context: str) -> nx.DiGraph:
    arcs: dict[tuple[Any, Any], dict[str, Any]] = {}
    for site in profile["sites"]:
        for tail_text, head_text, role in site["rooted_representatives"]:
            edge = (ast.literal_eval(tail_text), ast.literal_eval(head_text))
            previous = arcs.setdefault(edge, {"edge_role": role})
            require(previous == {"edge_role": role}, f"{context}:edge-role collision:{edge}")
    nodes = {node for edge in arcs for node in edge}
    incoming = collections.Counter(head for _tail, head in arcs)
    outgoing = collections.Counter(tail for tail, _head in arcs)
    graph = nx.DiGraph()
    for node in nodes:
        label = leaf_labels.get(node)
        role = (
            "leaf" if label is not None else
            "root" if incoming[node] == 0 else
            "retic" if incoming[node] == 2 else "tree"
        )
        attributes = {"role": role, "label": label, "dummy": False}
        if (role == "leaf" or isinstance(node, str)
                or (isinstance(node, tuple) and len(node) >= 2
                    and node[1] == "subdivision")):
            attributes["dummy_name"] = None
        graph.add_node(node, **attributes)
    for (tail, head), data in arcs.items():
        graph.add_edge(tail, head, **data)
    validate_binary(graph, context)
    return graph


def insert_at_site(
    graph: nx.DiGraph, site: dict[str, Any], label: int, namespace: str,
    side: str, site_index: int,
) -> tuple[nx.DiGraph, tuple[Any, Any]]:
    tail_text, head_text, _role = site["rooted_representatives"][0]
    tail, head = ast.literal_eval(tail_text), ast.literal_eval(head_text)
    require(graph.has_edge(tail, head), f"insert missing arc:{namespace}:{side}:{site_index}")
    result = graph.copy()
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    stem = (namespace, side, site_index)
    subdivision = (stem, "subdivision", label, repr(tail), repr(head))
    leaf = (stem, "leaf", label, repr(tail), repr(head))
    require(subdivision not in result and leaf not in result, "insert node collision")
    result.add_node(subdivision, role="tree", label=None, dummy=False, dummy_name=None)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    validate_binary(result, f"insert:{namespace}:{side}:{site_index}")
    return result, (subdivision, leaf)


def restrict_rooted(graph: nx.DiGraph, keep_labels: set[int]) -> nx.DiGraph:
    result = graph.copy()
    for node, data in list(result.nodes(data=True)):
        if data.get("role") == "leaf" and data.get("label") not in keep_labels:
            result.remove_node(node)
    while True:
        dead = next((
            node for node, data in result.nodes(data=True)
            if result.out_degree(node) == 0
            and not (data.get("role") == "leaf" and data.get("label") in keep_labels)
        ), None)
        if dead is not None:
            result.remove_node(dead)
            continue
        suppress = next((
            node for node, data in result.nodes(data=True)
            if data.get("role") != "leaf"
            and result.in_degree(node) == result.out_degree(node) == 1
        ), None)
        if suppress is not None:
            parent = next(result.predecessors(suppress))
            child = next(result.successors(suppress))
            result.remove_node(suppress)
            if parent != child and not result.has_edge(parent, child):
                result.add_edge(parent, child, edge_role="suppressed")
            continue
        roots = [node for node in result if result.in_degree(node) == 0]
        if len(roots) == 1 and result.nodes[roots[0]].get("role") != "leaf" \
                and result.out_degree(roots[0]) == 1:
            result.remove_node(roots[0])
            continue
        break
    for node, data in result.nodes(data=True):
        data["role"] = (
            "leaf" if data.get("label") in keep_labels else
            "root" if result.in_degree(node) == 0 else
            "retic" if result.in_degree(node) == 2 else "tree"
        )
    return result


def relabel_leaf(graph: nx.DiGraph, old: int, new: int) -> nx.DiGraph:
    result = graph.copy()
    nodes = [
        node for node, data in result.nodes(data=True)
        if data.get("role") == "leaf" and data.get("label") == old
    ]
    require(len(nodes) == 1 and new not in labels_of(result), f"leaf relabel:{old}:{new}")
    result.nodes[nodes[0]]["label"] = new
    return result


def sd0_mixed(graph: nx.DiGraph) -> nx.Graph:
    roots = [
        node for node, data in graph.nodes(data=True)
        if data.get("role") == "root" or graph.in_degree(node) == 0
    ]
    require(len(roots) == 1, f"mixed root count:{roots}")
    root = roots[0]
    children = list(graph.successors(root))
    require(len(children) == 2, "mixed root degree")
    mixed = nx.Graph()
    for node, data in graph.nodes(data=True):
        if node != root:
            mixed.add_node(node, role=data.get("role"), label=data.get("label"))
    for tail, head in graph.edges():
        if tail == root:
            continue
        require(not mixed.has_edge(tail, head), "mixed parallel edge")
        heads = frozenset((head,)) if graph.nodes[head].get("role") == "retic" else frozenset()
        mixed.add_edge(tail, head, heads=heads)
    left, right = children
    require(left != right and not mixed.has_edge(left, right), "invalid root suppression")
    heads = frozenset(
        child for child in children if graph.nodes[child].get("role") == "retic"
    )
    mixed.add_edge(left, right, heads=heads)
    return mixed


def mixed_payload(graph: nx.DiGraph) -> dict[str, Any]:
    mixed = sd0_mixed(graph)
    return {
        "nodes": [
            [repr(node), {key: repr(value) for key, value in sorted(data.items())}]
            for node, data in sorted(mixed.nodes(data=True), key=lambda row: repr(row[0]))
        ],
        "edges": [
            [list(edge_key(left, right)), sorted(map(repr, data.get("heads", frozenset())))]
            for left, right, data in sorted(
                mixed.edges(data=True), key=lambda row: edge_key(row[0], row[1])
            )
        ],
    }


def validate_profile(graph: nx.DiGraph, profile: dict[str, Any], context: str) -> None:
    mixed = sd0_mixed(graph)
    roots = [node for node, data in graph.nodes(data=True) if data.get("role") == "root"]
    require(len(roots) == 1, f"{context}:profile root")
    root = roots[0]
    root_children = tuple(graph.successors(root))
    direct = {
        frozenset((tail, head)): (tail, head, data.get("edge_role"))
        for tail, head, data in graph.edges(data=True) if tail != root
    }
    expected_sites = []
    for left, right, data in sorted(
        mixed.edges(data=True), key=lambda row: edge_key(row[0], row[1])
    ):
        edge = frozenset((left, right))
        heads = data.get("heads", frozenset())
        if edge in direct:
            tail, head, role = direct[edge]
            representatives = [[repr(tail), repr(head), role]]
            if graph.nodes[head].get("role") == "leaf" or graph.nodes[tail].get("role") == "leaf":
                site_type = "pendant_arm"
            elif heads:
                site_type = "reticulation_incoming"
            else:
                site_type = "core_unheaded"
        else:
            require(edge == frozenset(root_children), f"{context}:unexplained mixed edge")
            representatives = [
                [repr(root), repr(child), graph.edges[root, child].get("edge_role")]
                for child in sorted(root_children, key=repr)
            ]
            site_type = "root_suppressed_segment"
        expected_sites.append({
            "site_id": f"E:{sha(list(edge_key(left, right)))}",
            "mixed_endpoints": list(edge_key(left, right)),
            "arrowhead_endpoints": sorted(map(repr, heads)),
            "site_type": site_type,
            "rooted_representatives": representatives,
        })
    require(profile["sites"] == expected_sites, f"{context}:site semantics")
    retics = sum(data.get("role") == "retic" for _, data in graph.nodes(data=True))
    require(profile["site_count"] == len(expected_sites) == 2 * len(labels_of(graph)) + 3 * retics - 3,
            f"{context}:site formula")
    require(profile["port_count"] == len(labels_of(graph)), f"{context}:port count")
    require(profile["reticulation_count"] == retics, f"{context}:retic count")
    require(profile["all_mixed_edge_sites_included"] is True, f"{context}:site completeness flag")
    require(profile["site_type_census"] == dict(sorted(collections.Counter(
        row["site_type"] for row in expected_sites
    ).items())), f"{context}:site census")
    require(profile["ordered_site_hash_root"] == sha([sha(row) for row in expected_sites]),
            f"{context}:site root")

    new_label = max(labels_of(graph)) + 1
    audit_children = sorted(root_children, key=lambda node: graph.nodes[node].get("role") != "leaf")
    # insert_at_site wraps its namespace to make production probe nodes.  The
    # root-half audit uses a scalar namespace, so rebuild those two exact names.
    def scalar_insert(child_graph: nx.DiGraph, which: Any, namespace: str) -> nx.DiGraph:
        tail, head = root, which
        out = child_graph.copy()
        data = dict(out.edges[tail, head]); out.remove_edge(tail, head)
        subdivision = (namespace, "subdivision", new_label, repr(tail), repr(head))
        leaf = (namespace, "leaf", new_label, repr(tail), repr(head))
        out.add_node(subdivision, role="tree", label=None, dummy=False, dummy_name=None)
        out.add_node(leaf, role="leaf", label=new_label, dummy=False, dummy_name=None)
        out.add_edge(tail, subdivision, **data); out.add_edge(subdivision, head, **data)
        out.add_edge(subdivision, leaf, edge_role="arm")
        return out
    first = scalar_insert(graph, audit_children[0], "root_half_audit_a")
    second = scalar_insert(graph, audit_children[1], "root_half_audit_b")
    half = {
        "new_label": new_label,
        "representative_half_arcs": [
            [repr(root), repr(child), graph.edges[root, child].get("edge_role")]
            for child in sorted(root_children, key=repr)
        ],
        "semi_directed_relation_after_insertion": "isomorphic",
        "first_graph_sha256": graph_sha(first),
        "second_graph_sha256": graph_sha(second),
    }
    half["certificate_sha256"] = sha(half)
    require(profile["root_half_equivalence"] == half, f"{context}:root-half certificate")
    left, right = sd0_mixed(first), sd0_mixed(second)
    node_match = lambda a, b: a.get("label") == b.get("label")
    edge_match = lambda a, b: a.get("heads", frozenset()) == b.get("heads", frozenset())
    require(nx.is_isomorphic(left, right, node_match=node_match, edge_match=edge_match),
            f"{context}:root halves not isomorphic")


def public_transport(record: dict[str, Any]) -> dict[str, Any]:
    result = dict(record)
    result.pop("ordinary_triangle_arrowhead_witness", None)
    return result


def validate_transport_schema(record_id: str, record: dict[str, Any]) -> None:
    require(set(record) == {
        "relation", "vertex_map", "mixed_edge_map", "source_triangle_edges",
        "target_triangle_edges", "transport_sha256", "ordinary_triangle_arrowhead_witness",
    }, f"transport schema:{record_id}")
    public = public_transport(record)
    claimed = public.pop("transport_sha256")
    require(record_id == claimed == sha(public), f"transport self hash:{record_id}")


def triangle_description(graph: nx.DiGraph, stored: list[list[str]]) -> tuple[set[tuple[str, str]], str]:
    mixed = sd0_mixed(graph)
    edges = {tuple(edge) for edge in stored}
    require(len(edges) == 3 and len(set(itertools.chain.from_iterable(edges))) == 3,
            "ordinary triangle edge/vertex count")
    headed, heads = [], []
    for edge in sorted(edges):
        left, right = map(ast.literal_eval, edge)
        require(mixed.has_edge(left, right), "ordinary triangle missing edge")
        edge_heads = mixed.edges[left, right].get("heads", frozenset())
        require(len(edge_heads) <= 1, "ordinary triangle double head")
        if edge_heads:
            headed.append(edge); heads.append(repr(next(iter(edge_heads))))
    require(len(headed) == 2 and len(set(heads)) == 1, "ordinary triangle arrowhead pattern")
    require(all(heads[0] in edge for edge in headed), "ordinary triangle common reticulation")
    return edges, heads[0]


def validate_transport_on_graphs(
    source: nx.DiGraph, target: nx.DiGraph, record_id: str,
    record: dict[str, Any], context: str,
) -> None:
    validate_transport_schema(record_id, record)
    source_mixed, target_mixed = sd0_mixed(source), sd0_mixed(target)
    source_nodes = {repr(node): node for node in source_mixed}
    target_nodes = {repr(node): node for node in target_mixed}
    vertex_rows = record["vertex_map"]
    require(len(source_nodes) == len(target_nodes) == len(vertex_rows),
            f"{context}:vertex cardinality")
    require({row[0] for row in vertex_rows} == set(source_nodes), f"{context}:source vertex coverage")
    require({row[1] for row in vertex_rows} == set(target_nodes), f"{context}:target vertex coverage")
    require(len({row[1] for row in vertex_rows}) == len(vertex_rows),
            f"{context}:target vertex injectivity")
    vertex_map = dict(vertex_rows)
    require(len(vertex_map) == len(vertex_rows), f"{context}:vertex function")
    for source_name, target_name in vertex_map.items():
        require(source_mixed.nodes[source_nodes[source_name]].get("label")
                == target_mixed.nodes[target_nodes[target_name]].get("label"),
                f"{context}:label preservation:{source_name}")

    def edge_dictionary(mixed: nx.Graph):
        return {edge_key(left, right): (left, right, data)
                for left, right, data in mixed.edges(data=True)}
    source_edges, target_edges = edge_dictionary(source_mixed), edge_dictionary(target_mixed)
    edge_rows = record["mixed_edge_map"]
    require(len(source_edges) == len(target_edges) == len(edge_rows),
            f"{context}:edge cardinality")
    require({tuple(row[0]) for row in edge_rows} == set(source_edges), f"{context}:source edge coverage")
    require({tuple(row[1]) for row in edge_rows} == set(target_edges), f"{context}:target edge coverage")
    require(len({tuple(row[1]) for row in edge_rows}) == len(edge_rows),
            f"{context}:target edge injectivity")
    edge_map = {tuple(left): tuple(right) for left, right in edge_rows}
    require(len(edge_map) == len(edge_rows), f"{context}:edge function")
    source_triangle = set(map(tuple, record["source_triangle_edges"] or []))
    target_triangle = set(map(tuple, record["target_triangle_edges"] or []))
    require((not source_triangle) == (record["relation"] == "isomorphic"),
            f"{context}:relation/triangle")
    require({edge_map[edge] for edge in source_triangle} == target_triangle,
            f"{context}:triangle transport")
    for source_edge, target_edge in edge_map.items():
        require(tuple(sorted(vertex_map[node] for node in source_edge)) == target_edge,
                f"{context}:edge incidence:{source_edge}")
        if source_edge in source_triangle:
            continue
        _sl, _sr, source_data = source_edges[source_edge]
        _tl, _tr, target_data = target_edges[target_edge]
        mapped_heads = {vertex_map[repr(node)] for node in source_data.get("heads", frozenset())}
        target_heads = {repr(node) for node in target_data.get("heads", frozenset())}
        require(mapped_heads == target_heads, f"{context}:arrowheads:{source_edge}")
    if record["relation"] == "isomorphic":
        require(record["ordinary_triangle_arrowhead_witness"] is None,
                f"{context}:isomorphism triangle witness")
    else:
        source_edges_actual, source_retic = triangle_description(source, record["source_triangle_edges"])
        target_edges_actual, target_retic = triangle_description(target, record["target_triangle_edges"])
        require(source_edges_actual == source_triangle and target_edges_actual == target_triangle,
                f"{context}:triangle deck")
        ordinary = record["ordinary_triangle_arrowhead_witness"]
        require(ordinary is not None, f"{context}:triangle witness absent")
        require(ordinary["required_pattern"] ==
                "exactly two triangle arrows into one common reticulation",
                f"{context}:triangle pattern")
        require(ordinary["source_common_reticulation"] == source_retic,
                f"{context}:source triangle reticulation")
        require(ordinary["target_common_reticulation"] == target_retic,
                f"{context}:target triangle reticulation")


def global_triangle(source: nx.DiGraph, target: nx.DiGraph, record: dict[str, Any]):
    if record["relation"] == "isomorphic":
        return None
    _source_edges, source_retic = triangle_description(source, record["source_triangle_edges"])
    _target_edges, target_retic = triangle_description(target, record["target_triangle_edges"])
    return {
        "source_triangle_edges": record["source_triangle_edges"],
        "target_triangle_edges": record["target_triangle_edges"],
        "source_reticulation": source_retic,
        "target_reticulation": target_retic,
        "ordinary_triangle_witness":
            "exactly two arrowheads enter the displayed common reticulation on each side",
    }


class OrderedRoot:
    def __init__(self) -> None:
        self.rows = 0
        self.root = sha([])

    def add(self, row: dict[str, Any]) -> None:
        self.root = sha({"previous": self.root, "row_sha256": sha(row)})
        self.rows += 1

    def check(self, expected: dict[str, Any], context: str) -> None:
        require(self.rows == expected["rows"], f"{context}:row count")
        require(self.root == expected["ordered_hash_root"], f"{context}:ordered root")


def iter_jsonl(path: Path):
    with gzip.open(path, "rt", newline="") as handle:
        for number, line in enumerate(handle):
            require(line.endswith("\n"), f"missing LF:{path.name}:{number}")
            row = json.loads(line)
            require(line == canonical_bytes(row).decode() + "\n",
                    f"noncanonical JSONL:{path.name}:{number}")
            yield number, row


def load_registry(
    path: Path, expected: dict[str, Any], record_kind: str, schema_validator,
) -> dict[str, dict[str, Any]]:
    require(sha_file(path) == expected["sha256"], f"{record_kind}:file hash")
    result: dict[str, dict[str, Any]] = {}
    ordered = OrderedRoot()
    for number, row in iter_jsonl(path):
        require(set(row) == {"record_kind", "record_id", "record"},
                f"{record_kind}:row schema:{number}")
        require(row["record_kind"] == record_kind, f"{record_kind}:kind:{number}")
        record_id = row["record_id"]
        require(record_id not in result, f"{record_kind}:duplicate:{record_id}")
        schema_validator(record_id, row["record"])
        result[record_id] = row["record"]
        ordered.add(row)
    require(len(result) == expected["unique_records"], f"{record_kind}:unique count")
    ordered.check(expected["ordered_records"], record_kind)
    return result


def validate_restriction_schema(record_id: str, record: dict[str, Any]) -> None:
    require(set(record) == {
        "exact_labelled_relation", "parent_mixed_graph_sha256", "removed_label",
        "restricted_mixed_graph_sha256", "restriction_transport_sha256",
    }, f"restriction schema:{record_id}")
    require(record_id == f"R:{sha(record)}", f"restriction self hash:{record_id}")
    require(record["exact_labelled_relation"] == "isomorphic",
            f"restriction relation:{record_id}")
    require(type(record["removed_label"]) is int, f"restriction label:{record_id}")


def identity_public_transport(source: nx.DiGraph, target: nx.DiGraph) -> dict[str, Any]:
    source_mixed, target_mixed = sd0_mixed(source), sd0_mixed(target)
    require(set(source_mixed) == set(target_mixed), "restriction identity vertices")
    source_edges = {frozenset((left, right)) for left, right in source_mixed.edges()}
    target_edges = {frozenset((left, right)) for left, right in target_mixed.edges()}
    require(source_edges == target_edges, "restriction identity edges")
    public = {
        "relation": "isomorphic",
        "vertex_map": [[repr(node), repr(node)] for node in sorted(source_mixed, key=repr)],
        "mixed_edge_map": [
            [list(edge_key(*tuple(edge))), list(edge_key(*tuple(edge)))]
            for edge in sorted(source_edges, key=lambda value: edge_key(*tuple(value)))
        ],
        "source_triangle_edges": None,
        "target_triangle_edges": None,
    }
    public["transport_sha256"] = sha(public)
    return public


def restriction_for_child(
    child: nx.DiGraph, parent: nx.DiGraph, removed_label: int,
) -> tuple[str, dict[str, Any]]:
    restricted = restrict_rooted(child, set(labels_of(parent)))
    public = identity_public_transport(restricted, parent)
    record = {
        "removed_label": removed_label,
        "restricted_mixed_graph_sha256": sha(mixed_payload(restricted)),
        "parent_mixed_graph_sha256": sha(mixed_payload(parent)),
        "exact_labelled_relation": "isomorphic",
        "restriction_transport_sha256": public["transport_sha256"],
    }
    return f"R:{sha(record)}", record


def switch_edge_sets(graph: nx.DiGraph):
    reticulations = tuple(sorted(
        (node for node, data in graph.nodes(data=True) if data.get("role") == "retic"),
        key=repr,
    ))
    parents = [tuple(sorted(graph.predecessors(node), key=repr)) for node in reticulations]
    require(all(len(row) == 2 for row in parents), "nonbinary switching reticulation")
    all_edges = tuple(graph.edges())
    for bits in itertools.product((0, 1), repeat=len(reticulations)):
        removed = set()
        for number, reticulation in enumerate(reticulations):
            keep = parents[number][bits[number]]
            removed.update(
                (parent, reticulation) for parent in parents[number] if parent != keep
            )
        yield bits, tuple(edge for edge in all_edges if edge not in removed)


def displayed_switch_label_sets(graph: nx.DiGraph) -> tuple[tuple[frozenset[int], ...], ...]:
    output = []
    for _bits, kept in switch_edge_sets(graph):
        switched = nx.DiGraph()
        switched.add_nodes_from(graph.nodes())
        switched.add_edges_from(kept)
        order = list(nx.topological_sort(switched))
        descendants: dict[Any, frozenset[int]] = {}
        for node in reversed(order):
            label = graph.nodes[node].get("label")
            labels = {label} if isinstance(label, int) else set()
            for child in switched.successors(node):
                labels.update(descendants[child])
            descendants[node] = frozenset(labels)
        output.append(tuple(descendants[head] for _tail, head in kept))
    return tuple(output)


def split_payload(splits: set[Any]) -> list[Any]:
    output = []
    for split in sorted(splits, key=repr):
        if split == ("star",):
            output.append(["star"])
        else:
            output.append([list(split[0]), list(split[1])])
    return output


def quartet_deck(graph: nx.DiGraph, required_label: int | None = None):
    switches = displayed_switch_label_sets(graph)
    output = []
    for quartet in itertools.combinations(labels_of(graph), 4):
        if required_label is not None and required_label not in quartet:
            continue
        keep = frozenset(quartet)
        splits = set()
        for descendants in switches:
            split = None
            for descendant_labels in descendants:
                left = descendant_labels & keep
                if len(left) == 2:
                    right = keep - left
                    split = tuple(sorted((tuple(sorted(left)), tuple(sorted(right)))))
                    break
            splits.add(split if split is not None else ("star",))
        output.append((quartet, split_payload(splits)))
    return tuple(output)


def first_quartet_mismatch(source_deck, target_deck):
    require(len(source_deck) == len(target_deck), "quartet deck length")
    for (source_quartet, source_splits), (target_quartet, target_splits) in zip(
        source_deck, target_deck
    ):
        require(source_quartet == target_quartet, "quartet label order")
        if source_splits != target_splits:
            return {
                "quartet": list(source_quartet),
                "source_displayed_splits": source_splits,
                "target_displayed_splits": target_splits,
                "method": "complete displayed-switching split-set mismatch",
            }
    return None


@dataclass(frozen=True)
class MapDescriptor:
    k: int
    retic_count: int
    edge_class_count: int
    outputs: tuple[Any, ...]
    edge_signatures: tuple[Any, ...]


def k3p_assignments(k: int):
    for prefix in itertools.product(range(4), repeat=k - 1):
        final = 0
        for value in prefix:
            final ^= value
        yield prefix + (final,)


def sector_for_mask(mask: int, assignment: tuple[int, ...]) -> int:
    value = 0
    index = 0
    while mask:
        if mask & 1:
            value ^= assignment[index]
        index += 1
        mask >>= 1
    return value


def descendant_masks(graph: nx.DiGraph, kept: tuple[tuple[Any, Any], ...]):
    switched = nx.DiGraph()
    switched.add_nodes_from(graph.nodes())
    switched.add_edges_from(kept)
    masks: dict[Any, int] = {}
    for node in reversed(list(nx.topological_sort(switched))):
        label = graph.nodes[node].get("label")
        mask = (1 << label) if isinstance(label, int) else 0
        for child in switched.successors(node):
            mask |= masks[child]
        masks[node] = mask
    return {(tail, head): masks[head] for tail, head in kept}


def inheritance_polynomial(bits: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    polynomial = {0: 1}
    for number, selected_second in enumerate(bits):
        updated = collections.defaultdict(int)
        for mask, coefficient in polynomial.items():
            if selected_second:
                updated[mask | (1 << number)] += coefficient
            else:
                updated[mask] += coefficient
                updated[mask | (1 << number)] -= coefficient
        polynomial = {mask: coefficient for mask, coefficient in updated.items() if coefficient}
    return tuple(sorted(polynomial.items()))


def descriptor_variant(
    graph: nx.DiGraph, reticulation_order: tuple[Any, ...],
    parent_orders: tuple[tuple[Any, Any], ...],
) -> MapDescriptor:
    k = len(labels_of(graph))
    assignments = tuple(k3p_assignments(k))
    all_edges = tuple(graph.edges())
    arms = {
        (tail, head) for tail, head in all_edges
        if graph.nodes[head].get("role") == "leaf"
        and isinstance(graph.nodes[head].get("label"), int)
    }
    switches = []
    for bits in itertools.product((0, 1), repeat=len(reticulation_order)):
        removed = set()
        for number, reticulation in enumerate(reticulation_order):
            keep_parent = parent_orders[number][bits[number]]
            removed.update(
                (parent, reticulation) for parent in graph.predecessors(reticulation)
                if parent != keep_parent
            )
        kept = tuple(edge for edge in all_edges if edge not in removed)
        switches.append((bits, kept, descendant_masks(graph, kept)))
    edge_signatures, internal_edges = [], []
    for edge in all_edges:
        if edge in arms:
            continue
        signature = []
        for _bits, _kept, masks in switches:
            if edge not in masks:
                signature.extend((0,) * len(assignments))
            else:
                signature.extend(sector_for_mask(masks[edge], assignment)
                                 for assignment in assignments)
        if any(signature):
            internal_edges.append(edge); edge_signatures.append(tuple(signature))
    active = tuple(sorted(set(edge_signatures)))
    class_of = {signature: number for number, signature in enumerate(active)}
    edge_class = {edge: class_of[signature]
                  for edge, signature in zip(internal_edges, edge_signatures)}
    outputs = []
    weights = {bits: inheritance_polynomial(bits) for bits, _kept, _masks in switches}
    for assignment in assignments:
        grouped: dict[Any, collections.defaultdict[int, int]] = collections.defaultdict(
            lambda: collections.defaultdict(int)
        )
        for bits, kept, masks in switches:
            factors = collections.Counter()
            for edge in kept:
                class_index = edge_class.get(edge)
                if class_index is None:
                    continue
                sector = sector_for_mask(masks[edge], assignment)
                if sector:
                    factors[(class_index, sector)] += 1
            monomial = tuple(sorted(
                (class_index, sector, exponent)
                for (class_index, sector), exponent in factors.items()
            ))
            for mask, coefficient in weights[bits]:
                grouped[monomial][mask] += coefficient
        expression = []
        for monomial, polynomial in grouped.items():
            terms = tuple(sorted((mask, coefficient) for mask, coefficient in polynomial.items()
                                 if coefficient))
            if terms:
                expression.append((monomial, terms))
        outputs.append(tuple(sorted(expression)))
    return MapDescriptor(k, len(reticulation_order), len(active), tuple(outputs), active)


def model_descriptor(graph: nx.DiGraph) -> MapDescriptor:
    reticulations = tuple(sorted(
        (node for node, data in graph.nodes(data=True) if data.get("role") == "retic"),
        key=repr,
    ))
    variants = []
    if not reticulations:
        variants.append(descriptor_variant(graph, (), ()))
    else:
        for order in itertools.permutations(reticulations):
            parents = [tuple(sorted(graph.predecessors(node), key=repr)) for node in order]
            require(all(len(row) == 2 for row in parents), "descriptor reticulation parents")
            for flips in itertools.product((0, 1), repeat=len(order)):
                parent_orders = tuple((row[flip], row[1 - flip])
                                      for row, flip in zip(parents, flips))
                variants.append(descriptor_variant(graph, order, parent_orders))
    return min(variants, key=lambda item: (
        item.retic_count, item.edge_class_count, item.outputs, item.edge_signatures
    ))


def descriptor_payload(descriptor: MapDescriptor) -> dict[str, Any]:
    return {
        "k": descriptor.k,
        "retic_count": descriptor.retic_count,
        "edge_class_count": descriptor.edge_class_count,
        "outputs": descriptor.outputs,
        "edge_signatures": descriptor.edge_signatures,
    }


def output_sparse_polynomials(descriptor: MapDescriptor):
    width = 3 * descriptor.edge_class_count + descriptor.retic_count
    output = []
    for expression in descriptor.outputs:
        polynomial = collections.defaultdict(int)
        for monomial, inheritance in expression:
            base = [0] * width
            for class_index, sector, exponent in monomial:
                base[3 * class_index + sector - 1] += exponent
            for mask, coefficient in inheritance:
                exponent = list(base)
                for number in range(descriptor.retic_count):
                    if mask >> number & 1:
                        exponent[3 * descriptor.edge_class_count + number] += 1
                polynomial[tuple(exponent)] += coefficient
        output.append({exponent: coefficient for exponent, coefficient in polynomial.items()
                       if coefficient})
    return tuple(output)


def sparse_multiply(left, right):
    output = collections.defaultdict(fractions.Fraction)
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            output[tuple(a + b for a, b in zip(left_exponent, right_exponent))] += (
                fractions.Fraction(left_coefficient) * right_coefficient
            )
    return {exponent: coefficient for exponent, coefficient in output.items() if coefficient}


def sparse_difference(left, right):
    output = collections.defaultdict(fractions.Fraction, left)
    for exponent, coefficient in right.items():
        output[exponent] -= coefficient
    return {exponent: coefficient for exponent, coefficient in output.items() if coefficient}


def sparse_payload(polynomial) -> list[Any]:
    return [[list(exponent), str(coefficient)]
            for exponent, coefficient in sorted(polynomial.items())]


CIRCUITS = (
    (("000", "CGT", "GTC"), ("0TT", "C0C", "GG0")),
    (("000", "CTG", "TGC"), ("0GG", "C0C", "TT0")),
    (("000", "GCT", "TGC"), ("0CC", "GG0", "T0T")),
    (("000", "GTC", "TCG"), ("0CC", "G0G", "TT0")),
    (("000", "CTG", "GCT"), ("0TT", "CC0", "G0G")),
    (("000", "CGT", "TCG"), ("0GG", "CC0", "T0T")),
)


def circuit_pullbacks(descriptor: MapDescriptor):
    outputs = output_sparse_polynomials(descriptor)
    assignments = tuple(k3p_assignments(3))
    index = {assignment: number for number, assignment in enumerate(assignments)}
    code = {"0": 0, "C": 1, "G": 2, "T": 3}
    coordinate = lambda text: outputs[index[tuple(code[letter] for letter in text)]]
    result = []
    for left, right in CIRCUITS:
        left_product = {(0,) * (3 * descriptor.edge_class_count + descriptor.retic_count):
                        fractions.Fraction(1)}
        right_product = dict(left_product)
        for text in left:
            left_product = sparse_multiply(left_product, coordinate(text))
        for text in right:
            right_product = sparse_multiply(right_product, coordinate(text))
        result.append(sparse_difference(left_product, right_product))
    return tuple(result)


def ordinary_sunlet(graph: nx.DiGraph) -> bool:
    try:
        mixed = sd0_mixed(graph)
    except SemanticFailure:
        return False
    triangles = []
    for nodes in itertools.combinations(sorted(mixed.nodes(), key=repr), 3):
        edges = [frozenset(pair) for pair in itertools.combinations(nodes, 2)]
        if all(mixed.has_edge(*tuple(edge)) for edge in edges):
            heads = [next(iter(mixed.edges[tuple(edge)].get("heads", frozenset())))
                     for edge in edges if mixed.edges[tuple(edge)].get("heads", frozenset())]
            if len(heads) == 2 and heads[0] == heads[1]:
                triangles.append(edges)
    degrees = sorted(dict(mixed.degree()).values())
    return (len(triangles) == 1 and len(mixed) == len(mixed.edges()) == 6
            and degrees == [1, 1, 1, 3, 3, 3])


def tree_sunlet_certificate(
    source: nx.DiGraph, target: nx.DiGraph, separator_path: Path,
):
    labels = labels_of(source)
    require(labels == labels_of(target), "tree-sunlet labels")
    for triple in itertools.combinations(labels, 3):
        source_restricted = restrict_rooted(source, set(triple))
        target_restricted = restrict_rooted(target, set(triple))
        source_retics = sum(data.get("role") == "retic"
                            for _, data in source_restricted.nodes(data=True))
        target_retics = sum(data.get("role") == "retic"
                            for _, data in target_restricted.nodes(data=True))
        if {source_retics, target_retics} != {0, 1}:
            continue
        relabel = {old: new for new, old in enumerate(sorted(triple))}
        source_normalized, target_normalized = source_restricted.copy(), target_restricted.copy()
        for graph in (source_normalized, target_normalized):
            for _node, data in graph.nodes(data=True):
                if data.get("label") in relabel:
                    data["label"] = relabel[data["label"]]
        source_descriptor = model_descriptor(source_normalized)
        target_descriptor = model_descriptor(target_normalized)
        source_circuits = circuit_pullbacks(source_descriptor)
        target_circuits = circuit_pullbacks(target_descriptor)
        if source_retics == 0:
            tree_on, sunlet_on = "source", "target"
            tree_circuits, sunlet_circuits = source_circuits, target_circuits
            sunlet_graph = target_normalized
        else:
            tree_on, sunlet_on = "target", "source"
            tree_circuits, sunlet_circuits = target_circuits, source_circuits
            sunlet_graph = source_normalized
        if not ordinary_sunlet(sunlet_graph) or any(tree_circuits) or not any(sunlet_circuits):
            continue
        certificate = {
            "method": "literal restricted K3P maps plus six-circuit sum-of-squares positivity",
            "triple": list(triple),
            "normalized_label_map": {str(key): value for key, value in sorted(relabel.items())},
            "tree_on": tree_on,
            "sunlet_on": sunlet_on,
            "source_restricted_graph_sha256": graph_sha(source_restricted),
            "target_restricted_graph_sha256": graph_sha(target_restricted),
            "source_descriptor_sha256": sha(descriptor_payload(source_descriptor)),
            "target_descriptor_sha256": sha(descriptor_payload(target_descriptor)),
            "tree_circuit_pullback_sha256": [sha(sparse_payload(row)) for row in tree_circuits],
            "sunlet_circuit_pullback_sha256": [sha(sparse_payload(row)) for row in sunlet_circuits],
            "sunlet_nonzero_circuit_count": sum(bool(row) for row in sunlet_circuits),
            "separator_certificate_path": str(separator_path.relative_to(PROJECT)),
            "separator_certificate_sha256": sha_file(separator_path),
            "separator": "sum_{j=1}^6 I_j^2",
            "tree_value": "coefficientwise exact zero",
            "sunlet_value": "strictly positive throughout D_{3,+}",
            "physical_transfer": (
                "direct three-leaf marginal; serial edge products and inherited "
                "mixing remain strict physical K3P coordinates"
            ),
            "three_sector_independence": "C, G, and T remain separate in every descriptor",
        }
        return f"K3P-TS:{sha(certificate)}", certificate
    return None, None


def sparse_from_payload(payload):
    output = {}
    for exponent, coefficient in payload:
        key = tuple(exponent)
        require(key not in output, "duplicate sparse exponent")
        value = fractions.Fraction(coefficient)
        require(value, "stored sparse zero")
        output[key] = value
    return output


def bernstein_certificate(polynomial):
    require(polynomial, "empty Bernstein polynomial")
    width = len(next(iter(polynomial)))
    common = tuple(min(exponent[index] for exponent in polynomial) for index in range(width))
    active = tuple(index for index in range(width)
                   if len({exponent[index] for exponent in polynomial}) > 1)
    reduced = collections.defaultdict(fractions.Fraction)
    for exponent, coefficient in polynomial.items():
        reduced[tuple(exponent[index] - common[index] for index in active)] += coefficient
    reduced = {exponent: coefficient for exponent, coefficient in reduced.items() if coefficient}
    degrees = tuple(max(exponent[index] for exponent in reduced)
                    for index in range(len(active)))
    shape = tuple(degree + 1 for degree in degrees)
    count = math.prod(shape)
    require(count <= 2_000_000, "Bernstein tensor cap")
    strides = tuple(math.prod(shape[index + 1:]) for index in range(len(shape)))
    values = [fractions.Fraction(0)] * count
    for exponent, coefficient in reduced.items():
        values[sum(value * stride for value, stride in zip(exponent, strides))] += coefficient
    for axis, degree in enumerate(degrees):
        stride = strides[axis]; outer = math.prod(shape[:axis]); block = (degree + 1) * stride
        transformed = [fractions.Fraction(0)] * count
        for outer_index in range(outer):
            base = outer_index * block
            for inner_index in range(stride):
                source = [values[base + value * stride + inner_index]
                          for value in range(degree + 1)]
                for beta in range(degree + 1):
                    transformed[base + beta * stride + inner_index] = sum(
                        source[alpha] * fractions.Fraction(
                            math.comb(beta, alpha), math.comb(degree, alpha)
                        ) for alpha in range(beta + 1)
                    )
        values = transformed
    signs = collections.Counter(-1 if value < 0 else 1 if value > 0 else 0
                                 for value in values)
    require(not (signs[-1] and signs[1]) and (signs[-1] or signs[1]),
            "Bernstein non-strict/mixed sign")
    return {
        "method": "exact_tensor_Bernstein_after_strictly_positive_monomial",
        "parameter_count": width,
        "strictly_positive_monomial_exponent": list(common),
        "active_parameter_indices": list(active),
        "Bernstein_multidegree": list(degrees),
        "Bernstein_coefficient_count": count,
        "negative_coefficients": signs[-1], "zero_coefficients": signs[0],
        "positive_coefficients": signs[1], "minimum_coefficient": str(min(values)),
        "maximum_coefficient": str(max(values)),
        "ordered_Bernstein_coefficients_sha256": sha([str(value) for value in values]),
        "strict_sign": -1 if signs[-1] else 1,
        "domain": (
            "the full open unit cube in physical edge-sector and inheritance "
            "variables, which contains the physical principal D_plus subset"
        ),
    }


class RelationClassRegistry:
    """Canonical pair+transport classes, independently rebuilt by isomorphism."""

    def __init__(self) -> None:
        self.representatives: list[nx.Graph] = []
        self.buckets: dict[str, list[int]] = collections.defaultdict(list)

    @staticmethod
    def combined(
        source: nx.DiGraph, target: nx.DiGraph, relation: str,
        transport: dict[str, Any],
    ) -> nx.Graph:
        result = nx.Graph()
        triangle_strings = {
            "S": set(map(tuple, transport["source_triangle_edges"] or [])),
            "T": set(map(tuple, transport["target_triangle_edges"] or [])),
        }
        for side, rooted in (("S", source), ("T", target)):
            mixed = sd0_mixed(rooted)
            for node, data in mixed.nodes(data=True):
                result.add_node((side, "v", node), color=f"{side}:vertex:{data.get('label')!r}")
            for number, (left, right, data) in enumerate(
                sorted(mixed.edges(data=True), key=lambda row: edge_key(row[0], row[1]))
            ):
                edge_node = (side, "e", number)
                collapsed = edge_key(left, right) in triangle_strings[side]
                result.add_node(edge_node, color=f"{side}:edge:{collapsed}")
                heads = data.get("heads", frozenset())
                result.add_edge(edge_node, (side, "v", left),
                                color=f"head:{left in heads and not collapsed}")
                result.add_edge(edge_node, (side, "v", right),
                                color=f"head:{right in heads and not collapsed}")
        for source_node, target_node in transport["vertex_map"]:
            result.add_edge(
                ("S", "v", ast.literal_eval(source_node)),
                ("T", "v", ast.literal_eval(target_node)), color="transport",
            )
        result.add_node(("relation",), color=f"relation:{relation}")
        return result

    def find_or_add(
        self, source: nx.DiGraph, target: nx.DiGraph, relation: str,
        transport: dict[str, Any], allow_add: bool,
    ) -> int:
        combined = self.combined(source, target, relation, transport)
        bucket = nx.weisfeiler_lehman_graph_hash(
            combined, node_attr="color", edge_attr="color", iterations=8
        )
        node_match = lambda left, right: left.get("color") == right.get("color")
        edge_match = lambda left, right: left.get("color") == right.get("color")
        for class_id in self.buckets[bucket]:
            if nx.is_isomorphic(combined, self.representatives[class_id],
                                node_match=node_match, edge_match=edge_match):
                return class_id
        require(allow_add, "reverse marginal created a new one-port relation class")
        class_id = len(self.representatives)
        self.representatives.append(combined)
        self.buckets[bucket].append(class_id)
        return class_id


def site_edge(site: dict[str, Any]) -> tuple[str, str]:
    return tuple(site["mixed_endpoints"])


def transport_edge_map(record: dict[str, Any]) -> dict[tuple[str, str], tuple[str, str]]:
    return {tuple(source): tuple(target) for source, target in record["mixed_edge_map"]}


def transported_site(
    record: dict[str, Any], source_site: dict[str, Any], target_site: dict[str, Any]
) -> bool:
    return transport_edge_map(record).get(site_edge(source_site)) == site_edge(target_site)


def validate_child_coherence(
    parent: dict[str, Any], child: dict[str, Any],
    source_site: dict[str, Any], target_site: dict[str, Any],
    inherited_triangle: dict[str, Any] | None, context: str,
) -> None:
    parent_vertices = dict(parent["vertex_map"])
    child_vertices = dict(child["vertex_map"])
    require(all(child_vertices.get(node) == target for node, target in parent_vertices.items()),
            f"{context}:parent vertex restriction")
    require(transported_site(parent, source_site, target_site),
            f"{context}:selected-site transport")
    if child["relation"] == "triangle":
        require(inherited_triangle is not None, f"{context}:new triangle")
        require(child["source_triangle_edges"] == inherited_triangle["source_triangle_edges"],
                f"{context}:source inherited triangle")
        require(child["target_triangle_edges"] == inherited_triangle["target_triangle_edges"],
                f"{context}:target inherited triangle")
        ordinary = child["ordinary_triangle_arrowhead_witness"]
        require(ordinary["source_common_reticulation"] == inherited_triangle["source_reticulation"],
                f"{context}:source inherited reticulation")
        require(ordinary["target_common_reticulation"] == inherited_triangle["target_reticulation"],
                f"{context}:target inherited reticulation")


def validate_row_schema(row: dict[str, Any], stage: str, context: str) -> None:
    one = {
        "stage", "parent_anchor_id", "origin", "inserted_label",
        "source_site_index", "source_site_id", "target_site_index", "target_site_id",
        "source_child_graph_sha256", "target_child_graph_sha256",
        "source_parent_restriction_id", "target_parent_restriction_id",
    }
    two = {
        "stage", "base_anchor_id", "one_port_parent_id", "origin", "first_label",
        "second_label", "first_source_site_index", "first_target_site_index",
        "second_source_site_index", "second_source_site_id", "second_target_site_index",
        "second_target_site_id", "source_child_graph_sha256", "target_child_graph_sha256",
        "source_parent_restriction_id", "target_parent_restriction_id",
    }
    common = one if stage == "A+p" else two
    if row["status"] in {"isomorphic", "triangle"}:
        extra = {"status", "transport_id", "parent_transport_id",
                 "transport_restriction", "global_triangle_sha256"}
        if stage == "A+p+q":
            extra.add("reverse_order_certificate")
    else:
        extra = {"status", "proof_id"}
    require(set(row) == common | extra, f"{context}:row schema")
    if row["status"] in {"isomorphic", "triangle"}:
        require(row["transport_restriction"] == TRANSPORT_RESTRICTION_CLAIM,
                f"{context}:transport restriction claim")


def prepare_children(
    parent: nx.DiGraph, profile: dict[str, Any], label: int, namespace: str,
    side: str, restriction_records: dict[str, dict[str, Any]], context: str,
) -> list[dict[str, Any]]:
    result = []
    for index, site in enumerate(profile["sites"]):
        child, inserted = insert_at_site(parent, site, label, namespace, side, index)
        restriction_id, restriction = restriction_for_child(child, parent, label)
        require(restriction_records.get(restriction_id) == restriction,
                f"{context}:{side}:{index}:restriction semantics")
        result.append({
            "graph": child, "graph_sha256": graph_sha(child), "site": site,
            "site_index": index, "restriction_id": restriction_id,
            "quartet_deck": quartet_deck(child, label), "inserted_nodes": inserted,
        })
    require(len(result) == profile["site_count"], f"{context}:{side}:child coverage")
    return result


def validate_common_row(
    row: dict[str, Any], source: dict[str, Any], target: dict[str, Any],
    source_index: str, target_index: str, source_site: str, target_site: str,
    context: str,
) -> None:
    require(row[source_index] == source["site_index"], f"{context}:source index")
    require(row[target_index] == target["site_index"], f"{context}:target index")
    require(row[source_site] == source["site"]["site_id"], f"{context}:source site")
    require(row[target_site] == target["site"]["site_id"], f"{context}:target site")
    require(row["source_child_graph_sha256"] == source["graph_sha256"],
            f"{context}:source child hash")
    require(row["target_child_graph_sha256"] == target["graph_sha256"],
            f"{context}:target child hash")
    require(row["source_parent_restriction_id"] == source["restriction_id"],
            f"{context}:source restriction")
    require(row["target_parent_restriction_id"] == target["restriction_id"],
            f"{context}:target restriction")


def validate_quartet_row(
    row: dict[str, Any], source_deck, target_deck,
    proofs: dict[str, dict[str, Any]], context: str,
) -> None:
    proof = first_quartet_mismatch(source_deck, target_deck)
    require(proof is not None, f"{context}:quartet deck equality")
    proof_id = f"Q:{sha(proof)}"
    require(row["proof_id"] == proof_id and proofs.get(proof_id) == proof,
            f"{context}:quartet proof semantics")


def validate_tree_sunlet_row(
    row: dict[str, Any], source: nx.DiGraph, target: nx.DiGraph,
    certificates: dict[str, dict[str, Any]], separator_path: Path, context: str,
) -> None:
    certificate_id, certificate = tree_sunlet_certificate(source, target, separator_path)
    require(certificate_id is not None, f"{context}:no literal tree-sunlet certificate")
    require(row["proof_id"] == certificate_id and certificates.get(certificate_id) == certificate,
            f"{context}:tree-sunlet proof semantics")


def public_anchor_expected(
    contract: dict[str, Any], class_id: int, triangle: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "anchor_id": contract["anchor_id"], "origin": contract["origin"],
        "labels": contract["labels"], "relation": contract["relation"],
        "canonical_anchor_class_id": class_id,
        "source_graph_sha256": contract["source_graph_sha256"],
        "target_graph_sha256": contract["target_graph_sha256"],
        "transport_id": contract["parent_transport"]["transport_sha256"],
        "global_triangle": triangle,
        "source_site_count": contract["source_candidate_profile"]["site_count"],
        "target_site_count": contract["target_candidate_profile"]["site_count"],
        "source_site_ordered_hash_root":
            contract["source_candidate_profile"]["ordered_site_hash_root"],
        "target_site_ordered_hash_root":
            contract["target_candidate_profile"]["ordered_site_hash_root"],
        "locator_sha256": sha(contract["locator"]),
    }


def replay_declared_bernstein_claims(value: Any) -> int:
    """Replay every sparse-pullback Bernstein claim recursively, if present."""
    count = 0
    if isinstance(value, dict):
        if "Bernstein_certificate" in value:
            require("pullback" in value, "Bernstein claim lacks sparse pullback")
            polynomial = sparse_from_payload(value["pullback"])
            require(bernstein_certificate(polynomial) == value["Bernstein_certificate"],
                    "Bernstein certificate replay")
            count += 1
        for child in value.values():
            count += replay_declared_bernstein_claims(child)
    elif isinstance(value, list):
        for child in value:
            count += replay_declared_bernstein_claims(child)
    return count


def reseal_transport(record: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    result = copy.deepcopy(record)
    public = public_transport(result)
    public.pop("transport_sha256", None)
    new_id = sha(public)
    result["transport_sha256"] = new_id
    return new_id, result


def expect_mutation_failure(name: str, clean, mutated) -> dict[str, Any]:
    clean()
    try:
        mutated()
    except SemanticFailure as error:
        return {"name": name, "status": "REJECTED", "diagnostic": str(error)}
    raise SemanticFailure(f"semantic mutation survived:{name}")


def run_mutations(
    samples: dict[str, Any], output: Path, source_path: Path, source_payload: str,
) -> dict[str, Any]:
    transport_record = samples["transport_record"]
    broken_transport = copy.deepcopy(transport_record)
    require(len(broken_transport["mixed_edge_map"]) >= 2, "transport mutation edge count")
    broken_transport["mixed_edge_map"][0][1], broken_transport["mixed_edge_map"][1][1] = (
        broken_transport["mixed_edge_map"][1][1], broken_transport["mixed_edge_map"][0][1]
    )
    broken_transport_id, broken_transport = reseal_transport(broken_transport)

    restriction_id = samples["restriction_id"]
    restriction_record = samples["restriction_record"]
    broken_restriction = copy.deepcopy(restriction_record)
    broken_restriction["removed_label"] += 1
    broken_restriction_id = f"R:{sha(broken_restriction)}"

    quartet_row = samples["quartet_row"]
    quartet_proof = samples["quartet_proof"]
    broken_quartet = copy.deepcopy(quartet_proof)
    broken_quartet["source_displayed_splits"], broken_quartet["target_displayed_splits"] = (
        broken_quartet["target_displayed_splits"], broken_quartet["source_displayed_splits"]
    )
    broken_quartet_id = f"Q:{sha(broken_quartet)}"
    broken_quartet_row = dict(quartet_row, proof_id=broken_quartet_id)

    sunlet_row = samples["sunlet_row"]
    sunlet_certificate = samples["sunlet_certificate"]
    broken_sunlet = copy.deepcopy(sunlet_certificate)
    broken_sunlet["sunlet_circuit_pullback_sha256"][0] = "f" * 64
    broken_sunlet_id = f"K3P-TS:{sha(broken_sunlet)}"
    broken_sunlet_row = dict(sunlet_row, proof_id=broken_sunlet_id)

    broken_profile = copy.deepcopy(samples["profile"])
    broken_profile["sites"].pop()
    broken_profile["site_count"] = len(broken_profile["sites"])
    broken_profile["site_type_census"] = dict(sorted(collections.Counter(
        row["site_type"] for row in broken_profile["sites"]
    ).items()))
    broken_profile["ordered_site_hash_root"] = sha([sha(row) for row in broken_profile["sites"]])

    equality_row = samples["equality_row"]
    broken_equality_row = copy.deepcopy(equality_row)
    broken_equality_row["transport_restriction"] = (
        "claimed exact without retaining the selected mixed edge site"
    )

    def restriction_check(candidate_id, candidate):
        validate_restriction_schema(candidate_id, candidate)
        derived_id, derived = restriction_for_child(
            samples["restriction_child"], samples["restriction_parent"],
            samples["restriction_label"],
        )
        require(candidate_id == derived_id and candidate == derived,
                "coherently resealed restriction disagrees with marginal")

    cases = [
        expect_mutation_failure(
            "coherently_resealed_nonincidence_transport",
            lambda: validate_transport_on_graphs(
                samples["transport_source"], samples["transport_target"],
                samples["transport_id"], transport_record, "mutation-clean-transport",
            ),
            lambda: validate_transport_on_graphs(
                samples["transport_source"], samples["transport_target"],
                broken_transport_id, broken_transport, "mutation-broken-transport",
            ),
        ),
        expect_mutation_failure(
            "coherently_resealed_wrong_marginal_label",
            lambda: restriction_check(restriction_id, restriction_record),
            lambda: restriction_check(broken_restriction_id, broken_restriction),
        ),
        expect_mutation_failure(
            "coherently_resealed_false_quartet",
            lambda: validate_quartet_row(
                quartet_row, samples["quartet_source_deck"], samples["quartet_target_deck"],
                {quartet_row["proof_id"]: quartet_proof}, "mutation-clean-quartet",
            ),
            lambda: validate_quartet_row(
                broken_quartet_row, samples["quartet_source_deck"],
                samples["quartet_target_deck"], {broken_quartet_id: broken_quartet},
                "mutation-broken-quartet",
            ),
        ),
        expect_mutation_failure(
            "coherently_resealed_false_six_circuit_deck",
            lambda: validate_tree_sunlet_row(
                sunlet_row, samples["sunlet_source"], samples["sunlet_target"],
                {sunlet_row["proof_id"]: sunlet_certificate}, samples["separator_path"],
                "mutation-clean-sunlet",
            ),
            lambda: validate_tree_sunlet_row(
                broken_sunlet_row, samples["sunlet_source"], samples["sunlet_target"],
                {broken_sunlet_id: broken_sunlet}, samples["separator_path"],
                "mutation-broken-sunlet",
            ),
        ),
        expect_mutation_failure(
            "coherently_resealed_incomplete_site_profile",
            lambda: validate_profile(samples["profile_graph"], samples["profile"],
                                     "mutation-clean-profile"),
            lambda: validate_profile(samples["profile_graph"], broken_profile,
                                     "mutation-broken-profile"),
        ),
        expect_mutation_failure(
            "altered_transport_restriction_claim",
            lambda: validate_row_schema(equality_row, equality_row["stage"],
                                        "mutation-clean-restriction-claim"),
            lambda: validate_row_schema(broken_equality_row,
                                        broken_equality_row["stage"],
                                        "mutation-broken-restriction-claim"),
        ),
        expect_mutation_failure(
            "mixed_sign_Bernstein_polynomial",
            lambda: bernstein_certificate({(0, 0): fractions.Fraction(1),
                                           (1, 0): fractions.Fraction(1)}),
            lambda: bernstein_certificate({(3, 0): fractions.Fraction(1),
                                           (0, 3): fractions.Fraction(-1)}),
        ),
    ]
    report = {
        "schema": "k3p-probe-semantic-coherent-mutations-v1",
        "status": "PASS", "source_certificate_sha256": sha_file(source_path),
        "source_certificate_payload_sha256": source_payload,
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "clean_baselines_required": True,
        "coherent_inner_hashes_recomputed": True,
        "mutations": cases, "mutations_rejected": len(cases), "mutations_survived": 0,
    }
    report["payload_sha256"] = logical_payload(report)
    write_json(output, report)
    return report


def main() -> None:
    if not __debug__ or sys.flags.optimize:
        raise SemanticFailure("K3P_PROBE_SEMANTIC_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", type=Path, default=HERE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--mutations-output", type=Path, default=DEFAULT_MUTATIONS)
    args = parser.parse_args()
    started = time.monotonic()
    package = args.package_dir.resolve()
    certificate_path = package / "K3P_PROBE_COHERENCE_CERTIFICATE.json"
    certificate = json.loads(certificate_path.read_text())
    require(certificate["schema"] == "k3p-corrected-coherent-probe-closure-v1",
            "certificate schema")
    require(certificate["status"] == "PASS", "certificate status")
    require(certificate["payload_sha256"] == logical_payload(certificate),
            "certificate logical payload")
    require(certificate["classifier_order"] == [
        "exact_labelled_isomorphism_or_ordinary_triangle",
        "displayed_quartet_mismatch",
        "literal_K3P_triple_maps_plus_tree_sunlet_six_circuit_SOS",
        "unresolved_fatal",
    ], "classifier order")

    input_paths = {
        "atlas_sha256": PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py",
        "probe_input_contract_sha256": CONTRACT_PATH,
        "probe_input_independent_replay_sha256": REPLAY_PATH,
        "probe_input_mutations_sha256":
            TOPOLOGY / "anchor_inputs/probe_input_mutation_certificate.json",
        "corrected_restoration_sha256":
            TOPOLOGY / "anchor_inputs/corrected_restoration_forest.json",
        "raw4_ledger_sha256": TOPOLOGY / "anchor_inputs/raw_directional_ledger.jsonl.gz",
        "theta2_fixed_full_closure_sha256":
            TOPOLOGY / "anchor_inputs/fixed_full_restoration_closure.json.gz",
        "cycle_physical_anchors_sha256": TOPOLOGY / "cycle/physical_anchors.json",
        "cycle_promotion_sha256": TOPOLOGY / "cycle/cycle_promotion_certificate.json",
    }
    for field, path in input_paths.items():
        require(certificate["inputs"][field] == sha_file(path), f"input binding:{field}")

    contract = json.loads(CONTRACT_PATH.read_text())
    require(contract["schema"] == "k2p-root-invariant-probe-input-contract-v2"
            and contract["status"] == "PASS", "contract schema/status")
    contract_public = dict(contract); claimed_contract = contract_public.pop("payload_sha256")
    require(claimed_contract == sha(contract_public), "contract payload")
    require(certificate["inputs"]["probe_input_contract_payload_sha256"] == claimed_contract,
            "contract payload cross-binding")
    input_replay = json.loads(REPLAY_PATH.read_text())
    replay_public = dict(input_replay); claimed_replay = replay_public.pop("payload_sha256")
    require(claimed_replay == sha(replay_public) and input_replay["status"] == "PASS",
            "input replay payload/status")
    require(input_replay["contract_sha256"] == sha_file(CONTRACT_PATH)
            and input_replay["contract_payload_sha256"] == claimed_contract,
            "input replay contract binding")

    proof_path = package / certificate["registries"]["separation"]["path"]
    require(sha_file(proof_path) == certificate["registries"]["separation"]["sha256"],
            "proof file hash")
    with gzip.open(proof_path, "rt") as handle:
        proof = json.load(handle)
    proof_public = dict(proof); claimed_proof = proof_public.pop("payload_sha256")
    require(claimed_proof == sha(proof_public), "proof payload")
    require(claimed_proof == certificate["registries"]["separation"]["payload_sha256"],
            "proof cross-binding")
    quartet_proofs = proof["separation_proof_registry"]
    for proof_id, item in quartet_proofs.items():
        require(proof_id == f"Q:{sha(item)}", f"quartet self hash:{proof_id}")
        require(item["source_displayed_splits"] != item["target_displayed_splits"],
                f"quartet inequality:{proof_id}")
    k3p_registry = proof["k3p_tree_sunlet_registry"]
    k3p_certificates = k3p_registry["certificates"]
    for proof_id, item in k3p_certificates.items():
        require(proof_id == f"K3P-TS:{sha(item)}", f"tree-sunlet self hash:{proof_id}")
    separator_path = PROJECT / "three_port/literal_separator_v2/K3P_TREE_SUNLET_LITERAL_SEPARATOR_V2.json"
    require(k3p_registry["separator_certificate_sha256"] == sha_file(separator_path),
            "separator theorem binding")
    bernstein_claims = replay_declared_bernstein_claims(proof)

    transport_records = load_registry(
        package / certificate["registries"]["exact_transports"]["path"],
        certificate["registries"]["exact_transports"],
        "exact_labelled_mixed_graph_transport", validate_transport_schema,
    )
    restriction_records = load_registry(
        package / certificate["registries"]["parent_restrictions"]["path"],
        certificate["registries"]["parent_restrictions"],
        "exact_parent_marginal_restriction", validate_restriction_schema,
    )

    public_anchors = certificate["anchor_inventory"]["public_anchors"]
    contract_anchors = contract["anchors"]
    require(len(public_anchors) == len(contract_anchors) == 176, "anchor census")
    require([row["anchor_id"] for row in public_anchors]
            == [row["anchor_id"] for row in contract_anchors], "anchor order")
    anchors: dict[str, dict[str, Any]] = {}
    anchor_classes = RelationClassRegistry()
    anchor_class_coverage: dict[int, list[str]] = collections.defaultdict(list)
    used_transports: set[str] = set()
    used_restrictions: set[str] = set()
    used_quartets: set[str] = set()
    used_k3p: set[str] = set()
    public_hashes = []
    samples: dict[str, Any] = {}
    for number, (contract_anchor, public_anchor) in enumerate(
        zip(contract_anchors, public_anchors)
    ):
        anchor_id = contract_anchor["anchor_id"]
        source_labels = infer_source_leaf_labels(
            contract_anchor["source_candidate_profile"], contract_anchor["labels"]
        )
        parent_vertex_map = {
            ast.literal_eval(source): ast.literal_eval(target)
            for source, target in contract_anchor["parent_transport"]["vertex_map"]
        }
        target_labels = {parent_vertex_map[node]: label for node, label in source_labels.items()}
        source = profile_graph(contract_anchor["source_candidate_profile"], source_labels,
                               f"anchor:{anchor_id}:source")
        target = profile_graph(contract_anchor["target_candidate_profile"], target_labels,
                               f"anchor:{anchor_id}:target")
        require(graph_sha(source) == contract_anchor["source_graph_sha256"],
                f"anchor source hash:{anchor_id}")
        require(graph_sha(target) == contract_anchor["target_graph_sha256"],
                f"anchor target hash:{anchor_id}")
        validate_profile(source, contract_anchor["source_candidate_profile"],
                         f"anchor:{anchor_id}:source-profile")
        validate_profile(target, contract_anchor["target_candidate_profile"],
                         f"anchor:{anchor_id}:target-profile")
        transport_id = contract_anchor["parent_transport"]["transport_sha256"]
        require(transport_id in transport_records, f"anchor transport:{anchor_id}")
        transport = transport_records[transport_id]
        require(public_transport(transport) == contract_anchor["parent_transport"],
                f"anchor transport payload:{anchor_id}")
        validate_transport_on_graphs(source, target, transport_id, transport,
                                     f"anchor:{anchor_id}")
        used_transports.add(transport_id)
        triangle = global_triangle(source, target, transport)
        class_id = anchor_classes.find_or_add(
            source, target, transport["relation"], public_transport(transport), True
        )
        require(public_anchor == public_anchor_expected(contract_anchor, class_id, triangle),
                f"public anchor:{anchor_id}")
        anchor_class_coverage[class_id].append(anchor_id); public_hashes.append(sha(public_anchor))
        target_sites = {site_edge(row): row
                        for row in contract_anchor["target_candidate_profile"]["sites"]}
        computed_transport = []
        edge_map = transport_edge_map(transport)
        for source_site in contract_anchor["source_candidate_profile"]["sites"]:
            target_site = target_sites[edge_map[site_edge(source_site)]]
            computed_transport.append({
                "source_site_id": source_site["site_id"],
                "source_site_type": source_site["site_type"],
                "target_site_id": target_site["site_id"],
                "target_site_type": target_site["site_type"],
            })
        computed_transport.sort(key=lambda row: row["source_site_id"])
        require(computed_transport == contract_anchor["site_transport"]
                and sha(computed_transport) == contract_anchor["site_transport_sha256"],
                f"anchor site transport:{anchor_id}")
        require(first_quartet_mismatch(quartet_deck(source), quartet_deck(target)) is None,
                f"anchor quartet drift:{anchor_id}")
        anchors[anchor_id] = {
            "source": source, "target": target,
            "source_profile": contract_anchor["source_candidate_profile"],
            "target_profile": contract_anchor["target_candidate_profile"],
            "transport_id": transport_id, "transport": transport, "global_triangle": triangle,
            "origin": contract_anchor["origin"], "labels": tuple(contract_anchor["labels"]),
        }
        if number == 0:
            samples.update(profile_graph=source, profile=contract_anchor["source_candidate_profile"])
    require(len(anchor_classes.representatives)
            == certificate["anchor_inventory"]["canonical_anchor_classes"] == 39,
            "anchor class census")
    require({str(key): value for key, value in anchor_class_coverage.items()}
            == certificate["anchor_inventory"]["canonical_class_coverage"],
            "anchor class coverage")
    require(sha(public_hashes) == certificate["anchor_inventory"]["ordered_public_anchor_hash_root"],
            "public anchor ordered root")
    print("K3P semantic replay: anchors 176/176", file=sys.stderr, flush=True)

    one_path = package / "one_port_ledger.jsonl.gz"
    require(sha_file(one_path) == certificate["one_port"]["ledger_sha256"],
            "one ledger hash")
    one_iterator = iter(iter_jsonl(one_path)); one_order = OrderedRoot()
    one_counts = collections.Counter(); one_compatible = 0
    one_classes = RelationClassRegistry(); one_parents = []
    one_class_ids_by_base: dict[str, set[int]] = collections.defaultdict(set)
    for anchor_number, public_anchor in enumerate(public_anchors):
        anchor_id = public_anchor["anchor_id"]; anchor = anchors[anchor_id]
        label = max(anchor["labels"]) + 1
        source_children = prepare_children(
            anchor["source"], anchor["source_profile"], label, f"P1:{anchor_id}",
            "source", restriction_records, f"one:{anchor_id}",
        )
        target_children = prepare_children(
            anchor["target"], anchor["target_profile"], label, f"P1:{anchor_id}",
            "target", restriction_records, f"one:{anchor_id}",
        )
        for child in source_children + target_children:
            used_restrictions.add(child["restriction_id"])
            marginal_transport = restriction_records[child["restriction_id"]]["restriction_transport_sha256"]
            if marginal_transport in transport_records:
                used_transports.add(marginal_transport)
        for source_child in source_children:
            for target_child in target_children:
                try:
                    row_number, row = next(one_iterator)
                except StopIteration as error:
                    raise SemanticFailure("one ledger omitted raw row") from error
                context = f"one:{row_number}"
                validate_row_schema(row, "A+p", context)
                require(row["stage"] == "A+p" and row["parent_anchor_id"] == anchor_id,
                        f"{context}:parent/order")
                require(row["origin"] == anchor["origin"] and row["inserted_label"] == label,
                        f"{context}:origin/label")
                validate_common_row(row, source_child, target_child,
                                    "source_site_index", "target_site_index",
                                    "source_site_id", "target_site_id", context)
                one_order.add(row); one_counts[row["status"]] += 1
                compatible = transported_site(anchor["transport"], source_child["site"],
                                               target_child["site"])
                one_compatible += compatible
                if row["status"] in {"isomorphic", "triangle"}:
                    samples.setdefault("equality_row", row)
                    require(compatible, f"{context}:equality on incompatible sites")
                    transport_id = row["transport_id"]
                    require(transport_id in transport_records, f"{context}:transport reference")
                    transport = transport_records[transport_id]
                    require(transport["relation"] == row["status"], f"{context}:relation")
                    validate_transport_on_graphs(source_child["graph"], target_child["graph"],
                                                 transport_id, transport, context)
                    validate_child_coherence(anchor["transport"], transport,
                                             source_child["site"], target_child["site"],
                                             anchor["global_triangle"], context)
                    require(row["parent_transport_id"] == anchor["transport_id"],
                            f"{context}:parent transport")
                    triangle_hash = None if anchor["global_triangle"] is None else sha(anchor["global_triangle"])
                    require(row["global_triangle_sha256"] == triangle_hash,
                            f"{context}:global triangle hash")
                    used_transports.add(transport_id)
                    class_id = one_classes.find_or_add(
                        source_child["graph"], target_child["graph"], row["status"],
                        public_transport(transport), True,
                    )
                    parent_id = (f"P1:{anchor_id}:{source_child['site_index']}:"
                                 f"{target_child['site_index']}")
                    one_class_ids_by_base[anchor_id].add(class_id)
                    one_parents.append({
                        "parent_id": parent_id, "base_anchor_id": anchor_id,
                        "origin": anchor["origin"], "relation": row["status"],
                        "source": source_child["graph"], "target": target_child["graph"],
                        "transport_id": transport_id, "transport": transport,
                        "global_triangle": anchor["global_triangle"], "class_id": class_id,
                        "first_label": label,
                        "first_source_site_index": source_child["site_index"],
                        "first_target_site_index": target_child["site_index"],
                    })
                    if "transport_record" not in samples:
                        samples.update(
                            transport_id=transport_id, transport_record=transport,
                            transport_source=source_child["graph"],
                            transport_target=target_child["graph"],
                            restriction_id=source_child["restriction_id"],
                            restriction_record=restriction_records[source_child["restriction_id"]],
                            restriction_child=source_child["graph"],
                            restriction_parent=anchor["source"], restriction_label=label,
                        )
                elif row["status"] == "displayed_quartet_mismatch":
                    require(not compatible, f"{context}:quartet on compatible sites")
                    validate_quartet_row(row, source_child["quartet_deck"],
                                         target_child["quartet_deck"], quartet_proofs, context)
                    used_quartets.add(row["proof_id"])
                    if "quartet_row" not in samples:
                        samples.update(
                            quartet_row=row, quartet_proof=quartet_proofs[row["proof_id"]],
                            quartet_source_deck=source_child["quartet_deck"],
                            quartet_target_deck=target_child["quartet_deck"],
                        )
                elif row["status"] == "k3p_tree_sunlet_sos":
                    require(compatible, f"{context}:tree-sunlet on incompatible sites")
                    require(first_quartet_mismatch(source_child["quartet_deck"],
                                                    target_child["quartet_deck"]) is None,
                            f"{context}:tree-sunlet after available quartet")
                    validate_tree_sunlet_row(row, source_child["graph"], target_child["graph"],
                                             k3p_certificates, separator_path, context)
                    used_k3p.add(row["proof_id"])
                    if "sunlet_row" not in samples:
                        samples.update(
                            sunlet_row=row, sunlet_certificate=k3p_certificates[row["proof_id"]],
                            sunlet_source=source_child["graph"],
                            sunlet_target=target_child["graph"], separator_path=separator_path,
                        )
                else:
                    raise SemanticFailure(f"{context}:unexpected status:{row['status']}")
        if anchor_number % 25 == 0:
            print(f"K3P semantic replay: one anchor {anchor_number + 1}/176",
                  file=sys.stderr, flush=True)
    require(next(one_iterator, None) is None, "one ledger extra rows")
    one_order.check(certificate["one_port"]["ordered_ledger"], "one ledger")
    require(dict(sorted(one_counts.items())) == certificate["one_port"]["counts"],
            "one counts")
    require(one_compatible == 2_206 == (
        one_counts["isomorphic"] + one_counts["triangle"]
        + one_counts["k3p_tree_sunlet_sos"]
    ), "one compatible partition")
    require(len(one_parents) == certificate["one_port"]["equality_survivors"] == 2_107,
            "one equality census")
    require(len(one_classes.representatives)
            == certificate["one_port"]["canonical_equality_relation_classes"] == 469,
            "one class census")
    print("K3P semantic replay: one-port 29964/29964", file=sys.stderr, flush=True)

    parent_path = package / "two_port_parent_inventory.jsonl.gz"
    require(sha_file(parent_path) == certificate["two_port"]["parent_inventory_sha256"],
            "parent inventory hash")
    parent_iterator = iter(iter_jsonl(parent_path)); parent_order = OrderedRoot()
    for parent_number, parent in enumerate(one_parents):
        try:
            row_number, row = next(parent_iterator)
        except StopIteration as error:
            raise SemanticFailure("parent inventory omitted row") from error
        context = f"parent:{row_number}"
        require(row["one_port_parent_id"] == parent["parent_id"], f"{context}:identity")
        require(row["base_anchor_id"] == parent["base_anchor_id"]
                and row["canonical_one_port_relation_class_id"] == parent["class_id"],
                f"{context}:base/class")
        require(row["origin"] == parent["origin"] and row["relation"] == parent["relation"],
                f"{context}:origin/relation")
        require(row["first_label"] == parent["first_label"]
                and row["first_source_site_index"] == parent["first_source_site_index"]
                and row["first_target_site_index"] == parent["first_target_site_index"],
                f"{context}:first probe")
        require(row["source_graph_sha256"] == graph_sha(parent["source"])
                and row["target_graph_sha256"] == graph_sha(parent["target"]),
                f"{context}:parent graph hashes")
        source_leaf_labels = {node: data["label"] for node, data in parent["source"].nodes(data=True)
                              if isinstance(data.get("label"), int)}
        target_leaf_labels = {node: data["label"] for node, data in parent["target"].nodes(data=True)
                              if isinstance(data.get("label"), int)}
        rebuilt_source = profile_graph(row["source_candidate_profile"], source_leaf_labels,
                                       f"{context}:source-rebuild")
        rebuilt_target = profile_graph(row["target_candidate_profile"], target_leaf_labels,
                                       f"{context}:target-rebuild")
        require(graph_payload(rebuilt_source) == graph_payload(parent["source"])
                and graph_payload(rebuilt_target) == graph_payload(parent["target"]),
                f"{context}:profile graph reconstruction")
        validate_profile(rebuilt_source, row["source_candidate_profile"],
                         f"{context}:source-profile")
        validate_profile(rebuilt_target, row["target_candidate_profile"],
                         f"{context}:target-profile")
        require(row["raw_second_probe_pairs"] ==
                row["source_candidate_profile"]["site_count"]
                * row["target_candidate_profile"]["site_count"],
                f"{context}:Cartesian count")
        parent["source_profile"] = row["source_candidate_profile"]
        parent["target_profile"] = row["target_candidate_profile"]
        parent_order.add(row)
    require(next(parent_iterator, None) is None, "parent inventory extra rows")
    parent_order.check(certificate["two_port"]["ordered_parent_inventory"], "parent inventory")

    two_path = package / "two_port_ledger.jsonl.gz"
    require(sha_file(two_path) == certificate["two_port"]["ledger_sha256"], "two ledger hash")
    two_iterator = iter(iter_jsonl(two_path)); two_order = OrderedRoot()
    two_counts = collections.Counter(); two_compatible = 0
    reverse_counts = collections.Counter(); new_triangles = 0; inherited_two = 0
    for parent_number, parent in enumerate(one_parents):
        base = anchors[parent["base_anchor_id"]]
        second_label = max(labels_of(parent["source"])) + 1
        source_children = prepare_children(
            parent["source"], parent["source_profile"], second_label,
            f"P2:{parent['parent_id']}", "source", restriction_records,
            f"two:{parent['parent_id']}",
        )
        target_children = prepare_children(
            parent["target"], parent["target_profile"], second_label,
            f"P2:{parent['parent_id']}", "target", restriction_records,
            f"two:{parent['parent_id']}",
        )
        for child in source_children + target_children:
            used_restrictions.add(child["restriction_id"])
            marginal_transport = restriction_records[child["restriction_id"]]["restriction_transport_sha256"]
            if marginal_transport in transport_records:
                used_transports.add(marginal_transport)
        for source_child in source_children:
            for target_child in target_children:
                try:
                    row_number, row = next(two_iterator)
                except StopIteration as error:
                    raise SemanticFailure("two ledger omitted raw row") from error
                context = f"two:{row_number}"
                validate_row_schema(row, "A+p+q", context)
                require(row["stage"] == "A+p+q"
                        and row["one_port_parent_id"] == parent["parent_id"],
                        f"{context}:parent/order")
                require(row["base_anchor_id"] == parent["base_anchor_id"]
                        and row["origin"] == parent["origin"], f"{context}:base/origin")
                require(row["first_label"] == parent["first_label"]
                        and row["second_label"] == second_label
                        and row["first_source_site_index"] == parent["first_source_site_index"]
                        and row["first_target_site_index"] == parent["first_target_site_index"],
                        f"{context}:first/second labels")
                validate_common_row(row, source_child, target_child,
                                    "second_source_site_index", "second_target_site_index",
                                    "second_source_site_id", "second_target_site_id", context)
                two_order.add(row); two_counts[row["status"]] += 1
                compatible = transported_site(parent["transport"], source_child["site"],
                                               target_child["site"])
                two_compatible += compatible
                if row["status"] in {"isomorphic", "triangle"}:
                    require(compatible, f"{context}:equality on incompatible sites")
                    transport_id = row["transport_id"]
                    require(transport_id in transport_records, f"{context}:transport reference")
                    transport = transport_records[transport_id]
                    require(transport["relation"] == row["status"], f"{context}:relation")
                    validate_transport_on_graphs(source_child["graph"], target_child["graph"],
                                                 transport_id, transport, context)
                    validate_child_coherence(parent["transport"], transport,
                                             source_child["site"], target_child["site"],
                                             parent["global_triangle"], context)
                    require(row["parent_transport_id"] == parent["transport_id"],
                            f"{context}:parent transport")
                    triangle_hash = None if parent["global_triangle"] is None else sha(parent["global_triangle"])
                    require(row["global_triangle_sha256"] == triangle_hash,
                            f"{context}:global triangle hash")
                    used_transports.add(transport_id)
                    if row["status"] == "triangle":
                        if parent["global_triangle"] is None:
                            new_triangles += 1
                        else:
                            inherited_two += 1
                    reverse = row["reverse_order_certificate"]
                    keep = set(base["labels"]) | {second_label}
                    reverse_source = relabel_leaf(
                        restrict_rooted(source_child["graph"], keep),
                        second_label, parent["first_label"],
                    )
                    reverse_target = relabel_leaf(
                        restrict_rooted(target_child["graph"], keep),
                        second_label, parent["first_label"],
                    )
                    require(reverse["remove_first_label"] == parent["first_label"]
                            and reverse["retain_then_rename_second_label"]
                            == [second_label, parent["first_label"]],
                            f"{context}:reverse labels")
                    require(reverse["same_base_anchor_id"] == parent["base_anchor_id"],
                            f"{context}:reverse base")
                    require(reverse["reverse_parent_source_graph_sha256"] == graph_sha(reverse_source)
                            and reverse["reverse_parent_target_graph_sha256"] == graph_sha(reverse_target),
                            f"{context}:reverse graph hashes")
                    reverse_id = reverse["reverse_parent_transport_id"]
                    require(reverse_id in transport_records, f"{context}:reverse transport")
                    reverse_transport = transport_records[reverse_id]
                    require(reverse_transport["relation"] == reverse["reverse_parent_relation"],
                            f"{context}:reverse relation")
                    validate_transport_on_graphs(reverse_source, reverse_target, reverse_id,
                                                 reverse_transport, f"{context}:reverse")
                    base_vertices = dict(base["transport"]["vertex_map"])
                    reverse_vertices = dict(reverse_transport["vertex_map"])
                    require(all(reverse_vertices.get(node) == target
                                for node, target in base_vertices.items()),
                            f"{context}:reverse base restriction")
                    if reverse_transport["relation"] == "triangle":
                        require(base["global_triangle"] is not None,
                                f"{context}:reverse new triangle")
                        require(reverse_transport["source_triangle_edges"]
                                == base["global_triangle"]["source_triangle_edges"],
                                f"{context}:reverse source global triangle")
                        require(reverse_transport["target_triangle_edges"]
                                == base["global_triangle"]["target_triangle_edges"],
                                f"{context}:reverse target global triangle")
                        ordinary = reverse_transport["ordinary_triangle_arrowhead_witness"]
                        require(ordinary["source_common_reticulation"]
                                == base["global_triangle"]["source_reticulation"],
                                f"{context}:reverse source reticulation")
                        require(ordinary["target_common_reticulation"]
                                == base["global_triangle"]["target_reticulation"],
                                f"{context}:reverse target reticulation")
                    reverse_class = one_classes.find_or_add(
                        reverse_source, reverse_target, reverse_transport["relation"],
                        public_transport(reverse_transport), False,
                    )
                    require(reverse_class == reverse["reverse_parent_canonical_one_port_class_id"]
                            and reverse_class in one_class_ids_by_base[parent["base_anchor_id"]],
                            f"{context}:reverse class")
                    require(reverse["conclusion"] ==
                            "the reversed one-probe marginal is present in the complete one-port equality universe",
                            f"{context}:reverse conclusion")
                    used_transports.add(reverse_id); reverse_counts[reverse_transport["relation"]] += 1
                elif row["status"] == "displayed_quartet_mismatch":
                    require(not compatible, f"{context}:quartet on compatible sites")
                    validate_quartet_row(row, source_child["quartet_deck"],
                                         target_child["quartet_deck"], quartet_proofs, context)
                    used_quartets.add(row["proof_id"])
                elif row["status"] == "k3p_tree_sunlet_sos":
                    require(compatible, f"{context}:tree-sunlet on incompatible sites")
                    require(first_quartet_mismatch(source_child["quartet_deck"],
                                                    target_child["quartet_deck"]) is None,
                            f"{context}:tree-sunlet after available quartet")
                    validate_tree_sunlet_row(row, source_child["graph"], target_child["graph"],
                                             k3p_certificates, separator_path, context)
                    used_k3p.add(row["proof_id"])
                else:
                    raise SemanticFailure(f"{context}:unexpected status:{row['status']}")
        if parent_number % 100 == 0:
            print(f"K3P semantic replay: two parent {parent_number + 1}/2107",
                  file=sys.stderr, flush=True)
        if parent_number % 50 == 0:
            gc.collect()
    require(next(two_iterator, None) is None, "two ledger extra rows")
    two_order.check(certificate["two_port"]["ordered_ledger"], "two ledger")
    require(dict(sorted(two_counts.items())) == certificate["two_port"]["counts"],
            "two counts")
    require(two_compatible == 33_305 == (
        two_counts["isomorphic"] + two_counts["triangle"]
        + two_counts["k3p_tree_sunlet_sos"]
    ), "two compatible partition")
    require(dict(sorted(reverse_counts.items()))
            == certificate["two_port"]["reverse_order_parent_relation_counts"],
            "reverse relation counts")
    require(sum(reverse_counts.values()) == certificate["two_port"]["equality_survivors"] == 32_729,
            "reverse census")
    require(new_triangles == 0 and inherited_two == 1_760,
            "one-global-triangle census")

    require(used_transports == set(transport_records),
            f"transport registry semantic orphans:{len(set(transport_records) - used_transports)}")
    require(used_restrictions == set(restriction_records),
            f"restriction registry semantic orphans:{len(set(restriction_records) - used_restrictions)}")
    require(used_quartets == set(quartet_proofs),
            f"quartet registry semantic orphans:{len(set(quartet_proofs) - used_quartets)}")
    require(used_k3p == set(k3p_certificates),
            f"tree-sunlet registry semantic orphans:{len(set(k3p_certificates) - used_k3p)}")
    assembly = certificate["assembly_theorem"]
    require(assembly["unresolved"] == assembly["incoherent"] == 0, "assembly zero gates")
    require(assembly["two_port_order_gate"]["reversed_marginals_checked"] == 32_729,
            "assembly reverse count")

    mutation_report = run_mutations(
        samples, args.mutations_output, certificate_path, certificate["payload_sha256"]
    )
    runtime = time.monotonic() - started
    report = {
        "schema": "k3p-probe-independent-full-semantic-replay-v1",
        "status": "PASS", "source_certificate_sha256": sha_file(certificate_path),
        "source_payload_sha256": certificate["payload_sha256"],
        "independence": {
            "producer_imported": False, "atlas_imported": False,
            "graphs_reconstructed_from_public_candidate_profiles": True,
            "stored_hashes_used_only_as_bindings": True,
        },
        "coverage": {
            "anchors": 176, "one_port_rows": sum(one_counts.values()),
            "two_port_parent_rows": len(one_parents),
            "two_port_rows": sum(two_counts.values()),
            "all_probe_rows": sum(one_counts.values()) + sum(two_counts.values()),
        },
        "one_port_counts": dict(sorted(one_counts.items())),
        "two_port_counts": dict(sorted(two_counts.items())),
        "semantic_witnesses": {
            "exact_transports": len(used_transports),
            "marginal_restrictions": len(used_restrictions),
            "quartet_certificates": len(used_quartets),
            "tree_sunlet_six_circuit_certificates": len(used_k3p),
            "declared_Bernstein_certificates_replayed": bernstein_claims,
            "reverse_order_marginals": sum(reverse_counts.values()),
            "new_global_triangles": new_triangles, "unresolved": 0, "incoherent": 0,
        },
        "mutations": {
            "report_sha256": sha_file(args.mutations_output),
            "payload_sha256": mutation_report["payload_sha256"],
            "rejected": mutation_report["mutations_rejected"], "survived": 0,
        },
        "conclusion": (
            "PASS: every one-/two-port row was reconstructed semantically from rooted graphs; "
            "incidence, arrowheads, restrictions, displayed quartets, literal K3P three-sector "
            "maps, six circuit pullbacks, reverse parents, and ordinary-triangle inheritance close"
        ),
        "operational": {"runtime_seconds": runtime},
    }
    report["payload_sha256"] = logical_payload(report)
    write_json(args.output, report)
    print("K3P_PROBE_SEMANTIC_REPLAY_PASS")
    print(json.dumps({
        "status": "PASS", "rows": report["coverage"]["all_probe_rows"],
        "runtime_seconds": runtime, "payload_sha256": report["payload_sha256"],
        "mutations_rejected": mutation_report["mutations_rejected"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (
        SemanticFailure, AssertionError, KeyError, IndexError, OSError,
        StopIteration, TypeError, ValueError, json.JSONDecodeError, nx.NetworkXError,
    ) as error:
        raise SystemExit(f"K3P_PROBE_SEMANTIC_REPLAY_FAIL:{error}") from error
