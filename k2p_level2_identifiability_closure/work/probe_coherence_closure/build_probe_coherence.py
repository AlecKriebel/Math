#!/usr/bin/env python3
"""Exact coherent one-/two-port probe closure for every primitive support.

The computation begins with primitive graph encodings and the published raw
four- and five-port ledgers.  Every terminal transport is rebuilt as an exact
labelled incidence-graph mapping.  One- and two-port probes are then classified
topology first; every topology survivor must be a unique exact isomorphism or
an ordinary-triangle relation which restricts its parent transport.
"""

from __future__ import annotations

import argparse
import ast
import collections
import gc
import gzip
import hashlib
import importlib.util
import itertools
import json
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
PACKAGE = PROJECT / "package/referee/k2p_offline_sweep_portable"
ATLAS_PATH = PACKAGE / "atlas/k2p_atlas_core.py"
RAW4 = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
THETA2_CLASSES = PROJECT / "work/theta2_five_port_closure/artifacts/class_partition.json.gz"
THETA2_SUMMARY = PROJECT / "work/theta2_five_port_closure/artifacts/theta2_five_port_summary.json"
CYCLE_RELEASE = PROJECT / "work/cycle_three_port_closure"
CYCLE_SUMMARY = CYCLE_RELEASE / "artifacts/cycle_three_port_summary.json"
CYCLE_QUADRATICS = CYCLE_RELEASE / "artifacts/quadratic_certificates.json"
CYCLE_ANCHORS = CYCLE_RELEASE / "artifacts/physical_anchors.json"
CYCLE_FULL_LEDGER = CYCLE_RELEASE / "artifacts/full_completion_ledger.jsonl.gz"
RESULT4 = PACKAGE / "results/four_port_release_v4"


class ProbeFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProbeFailure(message)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_atlas():
    spec = importlib.util.spec_from_file_location("probe_coherence_atlas", ATLAS_PATH)
    require(spec is not None and spec.loader is not None, "atlas import spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def graph_payload(graph: nx.DiGraph) -> dict[str, object]:
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


def labels_of(graph: nx.DiGraph) -> tuple[int, ...]:
    return tuple(
        sorted(
            data["label"]
            for _, data in graph.nodes(data=True)
            if isinstance(data.get("label"), int)
        )
    )


def internal_candidates(graph: nx.DiGraph) -> list[dict[str, object]]:
    rows = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        if graph.nodes[head].get("role") == "leaf":
            continue
        if graph.nodes[tail].get("role") == "root":
            continue
        rows.append({"tail": repr(tail), "head": repr(head), "edge_role": data.get("edge_role")})
    return rows


def insert_leaf(atlas, graph: nx.DiGraph, candidate: dict[str, object], label: int) -> nx.DiGraph:
    result = graph.copy()
    tail, head = ast.literal_eval(candidate["tail"]), ast.literal_eval(candidate["head"])
    require(result.has_edge(tail, head), f"missing probe edge {candidate}")
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = ("coherent_probe_subdivision", label, repr(tail), repr(head))
    leaf = ("leaf", "coherent_probe", label)
    require(subdivision not in result and leaf not in result, "probe node collision")
    result.add_node(subdivision, role="tree", label=None, dummy=False)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    # Restricted selected graphs do not always carry every optional attribute,
    # so enforce the degree/DAG conditions directly rather than calling the
    # atlas's attribute-sensitive validator.
    require(nx.is_directed_acyclic_graph(result), "probe insertion made a cycle")
    for node, data in result.nodes(data=True):
        degree = (result.in_degree(node), result.out_degree(node))
        expected = {
            "root": (0, 2), "tree": (1, 2), "retic": (2, 1), "leaf": (1, 0)
        }[data["role"]]
        require(degree == expected, f"probe graph is nonbinary at {node}: {degree}")
    return result


def promote_target(atlas, record, permutation: tuple[int, ...], role: str, label: int):
    relabelled = atlas.relabel_record(record, permutation)
    graph = relabelled.graph.copy()
    nodes = [node for node, data in graph.nodes(data=True) if data.get("dummy_name") == role]
    require(len(nodes) == 1, f"promoted role multiplicity {role}: {nodes}")
    graph.nodes[nodes[0]].update(label=label, dummy=False, dummy_name=None)
    return graph


def promote_graph_role(graph: nx.DiGraph, role: str, label: int) -> nx.DiGraph:
    """Promote one named dummy in an already relabelled full completion."""
    result = graph.copy()
    nodes = [node for node, data in result.nodes(data=True) if data.get("dummy_name") == role]
    require(len(nodes) == 1, f"promoted graph role multiplicity {role}: {nodes}")
    result.nodes[nodes[0]].update(label=label, dummy=False, dummy_name=None)
    return result


def selected_from_full_graph(graph: nx.DiGraph) -> nx.DiGraph:
    """Delete every still-dummy leaf and take the clean selected restriction."""
    keep = {
        data["label"]
        for _, data in graph.nodes(data=True)
        if data.get("role") == "leaf" and isinstance(data.get("label"), int)
    }
    return clean_restrict(graph, keep)


def clean_restrict(graph: nx.DiGraph, keep: set[int]) -> nx.DiGraph:
    restricted = graph.copy()
    for node, data in list(restricted.nodes(data=True)):
        if data.get("role") == "leaf" and data.get("label") not in keep:
            restricted.remove_node(node)
    changed = True
    while changed:
        changed = False
        for node, data in list(restricted.nodes(data=True)):
            if restricted.out_degree(node) == 0 and not (
                data.get("role") == "leaf" and data.get("label") in keep
            ):
                restricted.remove_node(node)
                changed = True
                break
        if changed:
            continue
        for node, data in list(restricted.nodes(data=True)):
            if data.get("role") != "leaf" and restricted.in_degree(node) == 1 and restricted.out_degree(node) == 1:
                parent = next(restricted.predecessors(node))
                child = next(restricted.successors(node))
                restricted.remove_node(node)
                if parent != child and not restricted.has_edge(parent, child):
                    restricted.add_edge(parent, child, edge_role="suppressed")
                changed = True
                break
        if changed:
            continue
        roots = [node for node in restricted if restricted.in_degree(node) == 0]
        if len(roots) == 1 and restricted.nodes[roots[0]].get("role") != "leaf" and restricted.out_degree(roots[0]) == 1:
            restricted.remove_node(roots[0])
            changed = True
    for node, data in restricted.nodes(data=True):
        if data.get("label") in keep:
            data["role"] = "leaf"
        elif restricted.in_degree(node) == 0:
            data["role"] = "root"
        elif restricted.in_degree(node) == 2:
            data["role"] = "retic"
        else:
            data["role"] = "tree"
    return restricted


def _prune_unrooted(graph: nx.Graph, keep: set[int], preserve_heads: bool) -> nx.Graph:
    """Root-free pruning and degree-two suppression of a mixed graph."""
    result = graph.copy()
    for node, data in list(result.nodes(data=True)):
        if isinstance(data.get("label"), int) and data.get("label") not in keep:
            result.remove_node(node)
    changed = True
    while changed:
        changed = False
        for node in sorted(tuple(result.nodes()), key=repr):
            if result.nodes[node].get("label") not in keep and result.degree(node) <= 1:
                result.remove_node(node)
                changed = True
                break
        if changed:
            continue
        for node in sorted(tuple(result.nodes()), key=repr):
            if result.nodes[node].get("label") in keep or result.degree(node) != 2:
                continue
            left, right = tuple(result.neighbors(node))
            left_heads = result.edges[left, node].get("heads", frozenset())
            right_heads = result.edges[node, right].get("heads", frozenset())
            inherited = (
                frozenset(
                    endpoint
                    for endpoint, heads in ((left, left_heads), (right, right_heads))
                    if endpoint in heads
                )
                if preserve_heads else frozenset()
            )
            result.remove_node(node)
            if left != right:
                if result.has_edge(left, right):
                    if preserve_heads:
                        old = result.edges[left, right].get("heads", frozenset())
                        result.edges[left, right]["heads"] = frozenset(set(old) | set(inherited))
                else:
                    result.add_edge(left, right, heads=inherited)
            changed = True
            break
    return result


def displayed_splits(atlas, graph: nx.DiGraph, quartet: tuple[int, ...]) -> frozenset[tuple]:
    """Displayed quartet set computed directly from the semi-directed graph."""
    mixed = atlas.sd0_mixed(graph)
    incoming = []
    for node in sorted(mixed.nodes(), key=repr):
        headed = tuple(
            frozenset((node, other))
            for other in mixed.neighbors(node)
            if node in mixed.edges[node, other].get("heads", frozenset())
        )
        if headed:
            require(len(headed) == 2, f"mixed reticulation incoming degree {node}: {headed}")
            incoming.append(headed)
    answer = set()
    for choices in itertools.product(*incoming):
        chosen = set(choices)
        removed = {edge for options in incoming for edge in options if edge not in chosen}
        tree = nx.Graph()
        tree.add_nodes_from((node, dict(data)) for node, data in mixed.nodes(data=True))
        tree.add_edges_from(
            (left, right)
            for left, right in mixed.edges()
            if frozenset((left, right)) not in removed
        )
        tree = _prune_unrooted(tree, set(quartet), preserve_heads=False)
        found = set()
        for left, right in list(tree.edges()):
            tree.remove_edge(left, right)
            components = list(nx.connected_components(tree))
            tree.add_edge(left, right)
            if len(components) != 2:
                continue
            sides = [
                tuple(sorted(tree.nodes[node].get("label") for node in component if tree.nodes[node].get("label") in quartet))
                for component in components
            ]
            if sorted(map(len, sides)) == [2, 2]:
                found.add(tuple(sorted(sides)))
        require(len(found) == 1, f"displayed tree lacks unique quartet split: {found}")
        answer.update(found)
    return frozenset(answer)


def triple_type(atlas, graph: nx.DiGraph, triple: tuple[int, ...]) -> str:
    """Semi-directed-invariant structural finder for the algebraic sign gate."""
    restricted = _prune_unrooted(atlas.sd0_mixed(graph), set(triple), preserve_heads=True)
    cycle_rank = (
        restricted.number_of_edges()
        - restricted.number_of_nodes()
        + nx.number_connected_components(restricted)
    )
    if cycle_rank == 0:
        return "tree"
    triangles = ordinary_triangles(restricted)
    if cycle_rank == 1 and len(triangles) == 1:
        return "sunlet"
    return f"r{cycle_rank}"


def topology_key(atlas, graph: nx.DiGraph) -> tuple:
    labels = labels_of(graph)
    quartets = tuple((q, displayed_splits(atlas, graph, q)) for q in itertools.combinations(labels, 4))
    triples = tuple((t, triple_type(atlas, graph, t)) for t in itertools.combinations(labels, 3))
    return labels, quartets, triples


def serialize_split_set(values: frozenset[tuple]) -> list[list[list[int]]]:
    return sorted([[list(left), list(right)] for left, right in values])


def topology_compare(source_key: tuple, target_key: tuple) -> dict[str, object] | None:
    source_labels, source_quartets, source_triples = source_key
    target_labels, target_quartets, target_triples = target_key
    require(source_labels == target_labels, "probe label mismatch")
    for (quartet, source), (other, target) in zip(source_quartets, target_quartets):
        require(quartet == other, "quartet alignment")
        if source != target:
            return {
                "status": "displayed_quartet_mismatch",
                "quartet": list(quartet),
                "source_splits": serialize_split_set(source),
                "target_splits": serialize_split_set(target),
                "certificate": "Englander-v4 displayed-set pointwise separator",
            }
    source_types, target_types = dict(source_triples), dict(target_triples)
    for triple in sorted(source_types):
        if {source_types[triple], target_types[triple]} == {"tree", "sunlet"}:
            return {
                "status": "strict_tree_sunlet",
                "triple": list(triple),
                "source_type": source_types[triple],
                "target_type": target_types[triple],
                "certificate": "T3 strict sign factor",
            }
    return None


class TopologyMemo:
    """Exact semi-directed-isomorphism cache for invariant topology decks."""

    def __init__(self, atlas):
        self.atlas = atlas
        self.buckets = collections.defaultdict(list)
        self.representatives = []
        self.values = []
        self.queries = 0
        self.hits = 0

    def incidence(self, graph):
        mixed = self.atlas.sd0_mixed(graph)
        raw = self.atlas.mixed_incidence_graph(mixed)
        result = nx.Graph()
        for node, data in raw.nodes(data=True):
            result.add_node(
                node,
                color=f"{data.get('kind')}|{data.get('label')!r}",
                kind=data.get("kind"),
                label=data.get("label"),
            )
        for left, right, data in raw.edges(data=True):
            result.add_edge(left, right, head=bool(data.get("head")))
        return result

    def get(self, graph):
        self.queries += 1
        incidence_graph = self.incidence(graph)
        bucket = nx.weisfeiler_lehman_graph_hash(
            incidence_graph, node_attr="color", edge_attr="head", iterations=8
        )
        node_match = lambda left, right: (
            left.get("kind") == right.get("kind")
            and left.get("label") == right.get("label")
        )
        edge_match = lambda left, right: left.get("head") == right.get("head")
        for class_id in self.buckets[bucket]:
            if nx.is_isomorphic(
                incidence_graph, self.representatives[class_id],
                node_match=node_match, edge_match=edge_match,
            ):
                self.hits += 1
                return self.values[class_id]
        value = topology_key(self.atlas, graph)
        class_id = len(self.representatives)
        self.representatives.append(incidence_graph)
        self.values.append(value)
        self.buckets[bucket].append(class_id)
        return value

    def public(self):
        return {
            "queries": self.queries,
            "exact_isomorphism_hits": self.hits,
            "canonical_decks_computed": len(self.values),
            "collision_policy": "WL bucket followed by exact labelled semi-directed incidence-graph isomorphism",
        }


def edge_public(edge: frozenset) -> list[str]:
    return sorted(map(repr, edge))


def ordinary_triangles(mixed: nx.Graph) -> list[dict[str, object]]:
    answer = []
    for a, b, c in itertools.combinations(sorted(mixed.nodes(), key=repr), 3):
        if not (mixed.has_edge(a, b) and mixed.has_edge(a, c) and mixed.has_edge(b, c)):
            continue
        edges = frozenset((frozenset((a, b)), frozenset((a, c)), frozenset((b, c))))
        headed = []
        for edge in edges:
            u, v = tuple(edge)
            heads = mixed.edges[u, v].get("heads", frozenset())
            require(len(heads) <= 1, "two-headed ordinary triangle edge")
            if heads:
                headed.append(next(iter(heads)))
        if len(headed) == 2 and headed[0] == headed[1] and headed[0] in (a, b, c):
            reticulation = headed[0]
            require(mixed.nodes[reticulation].get("role") == "retic", "ordinary triangle head is not reticulate")
            answer.append({"edges": edges, "reticulation": reticulation})
    return answer


def incidence(mixed: nx.Graph, triangle: frozenset[frozenset] | None = None) -> nx.Graph:
    result = nx.Graph()
    triangle = frozenset() if triangle is None else triangle
    for node, data in mixed.nodes(data=True):
        result.add_node(("v", node), kind="vertex", label=data.get("label"), triangle_edge=False)
    for number, (left, right, data) in enumerate(
        sorted(mixed.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1])))
    ):
        edge = frozenset((left, right))
        edge_node = ("e", number)
        is_triangle = edge in triangle
        result.add_node(edge_node, kind="edge", label=None, triangle_edge=is_triangle)
        heads = data.get("heads", frozenset())
        result.add_edge(edge_node, ("v", left), head=False if is_triangle else left in heads)
        result.add_edge(edge_node, ("v", right), head=False if is_triangle else right in heads)
    return result


def mapping_records(atlas, source_graph: nx.DiGraph, target_graph: nx.DiGraph, status: str) -> list[dict[str, object]]:
    source_mixed, target_mixed = atlas.sd0_mixed(source_graph), atlas.sd0_mixed(target_graph)
    if status == "isomorphic":
        pairs = [(None, None, None, None)]
    elif status == "triangle":
        pairs = [
            (left["edges"], right["edges"], left["reticulation"], right["reticulation"])
            for left in ordinary_triangles(source_mixed)
            for right in ordinary_triangles(target_mixed)
        ]
    else:
        raise ProbeFailure(f"mapping requested for {status}")
    node_match = lambda a, b: (
        a.get("kind") == b.get("kind")
        and a.get("label") == b.get("label")
        and a.get("triangle_edge") == b.get("triangle_edge")
    )
    edge_match = lambda a, b: a.get("head") == b.get("head")
    records = {}
    for source_triangle, target_triangle, source_retic, target_retic in pairs:
        matcher = nx.algorithms.isomorphism.GraphMatcher(
            incidence(source_mixed, source_triangle),
            incidence(target_mixed, target_triangle),
            node_match=node_match,
            edge_match=edge_match,
        )
        for mapping in matcher.isomorphisms_iter():
            vertex_map = {node: mapping[("v", node)][1] for node in source_mixed.nodes()}
            public_map = tuple(sorted((repr(left), repr(right)) for left, right in vertex_map.items()))
            public_source_triangle = None if source_triangle is None else tuple(sorted(tuple(edge_public(edge)) for edge in source_triangle))
            public_target_triangle = None if target_triangle is None else tuple(sorted(tuple(edge_public(edge)) for edge in target_triangle))
            public = {
                "vertex_map": [list(pair) for pair in public_map],
                "source_triangle_edges": public_source_triangle,
                "target_triangle_edges": public_target_triangle,
                "source_triangle_reticulation": None if source_retic is None else repr(source_retic),
                "target_triangle_reticulation": None if target_retic is None else repr(target_retic),
            }
            records[sha(public)] = {
                "vertex_map": vertex_map,
                "source_triangle": source_triangle,
                "target_triangle": target_triangle,
                "public": public,
                "transport_sha256": sha(public),
            }
    return [records[key] for key in sorted(records)]


def exact_relation(atlas, source_graph: nx.DiGraph, target_graph: nx.DiGraph) -> tuple[str, list[dict[str, object]]]:
    isomorphisms = mapping_records(atlas, source_graph, target_graph, "isomorphic")
    if isomorphisms:
        return "isomorphic", isomorphisms
    triangles = mapping_records(atlas, source_graph, target_graph, "triangle")
    if triangles:
        return "triangle", triangles
    return "none", []


def global_triangle_payload(witness: dict[str, object] | None) -> dict[str, object] | None:
    if witness is None or witness["source_triangle"] is None:
        return None
    return {
        "source_triangle_edges": witness["public"]["source_triangle_edges"],
        "target_triangle_edges": witness["public"]["target_triangle_edges"],
        "source_reticulation": witness["public"]["source_triangle_reticulation"],
        "target_reticulation": witness["public"]["target_triangle_reticulation"],
    }


def mapping_restricts(atlas, parent: dict[str, object], child_witness: dict[str, object], child_status: str) -> bool:
    parent_nodes = atlas.sd0_mixed(parent["source_graph"]).nodes()
    parent_map = parent["transport"]["vertex_map"]
    child_map = child_witness["vertex_map"]
    if any(child_map.get(node) != parent_map[node] for node in parent_nodes):
        return False
    global_triangle = parent.get("global_triangle")
    if child_status == "triangle":
        if global_triangle is None:
            return False
        if child_witness["public"]["source_triangle_edges"] != global_triangle["source_triangle_edges"]:
            return False
        if child_witness["public"]["target_triangle_edges"] != global_triangle["target_triangle_edges"]:
            return False
    return True


def underlying_relation_hash(atlas, graph: nx.DiGraph) -> str:
    """Necessary (collision-safe) hash for an iso/triangle relation.

    Both exact isomorphism and ordinary-triangle equivalence preserve the
    underlying labelled mixed graph.  Unequal WL hashes therefore rule out a
    relation; equal hashes are always followed by the full exact matcher.
    """
    incidence_graph = atlas.mixed_incidence_graph(atlas.sd0_mixed(graph))
    for _, data in incidence_graph.nodes(data=True):
        data["underlying_color"] = f"{data.get('kind')}|{data.get('label')!r}"
    return nx.weisfeiler_lehman_graph_hash(
        incidence_graph, node_attr="underlying_color", iterations=8
    )


def _coordinate_index(atlas, k: int, assignment: tuple[int, ...]) -> int:
    representative = atlas.ct_orbit_rep(assignment)
    return atlas.orbit_assignments(k).index(representative)


def t3_pullback(atlas, descriptor, triple: tuple[int, ...], ordering: tuple[int, int, int]):
    """Pull back V^2 X_g - X_s^2 Y_g Z_g on the full k-leaf map."""
    first, second, third = (triple[index] for index in ordering)
    k = descriptor.k
    outputs = atlas.output_sparse_polynomials(descriptor)

    def coordinate(values):
        assignment = [0] * k
        for label, character in values.items():
            assignment[label] = character
        return outputs[_coordinate_index(atlas, k, tuple(assignment))]

    x_s = coordinate({first: 1, second: 1})
    x_g = coordinate({first: 2, second: 2})
    y_g = coordinate({first: 2, third: 2})
    z_g = coordinate({second: 2, third: 2})
    v = coordinate({first: 1, second: 3, third: 2})
    return atlas.sparse_lincomb(
        [atlas.sparse_mul_many((v, v, x_g)), atlas.sparse_mul_many((x_s, x_s, y_g, z_g))],
        (1, -1),
    )


def bernstein_strict_sign(polynomial: dict) -> dict[str, object] | None:
    """Certify a sparse polynomial's strict sign on the open unit cube.

    A common parameter monomial is removed first; it is strictly positive.
    The residual polynomial is converted exactly to its tensor Bernstein
    basis.  All basis functions are positive in the open cube, so one-sided
    coefficients with at least one strict coefficient give a rigorous sign.
    """
    if not polynomial:
        return None
    exponent_rows = tuple(polynomial)
    width = len(exponent_rows[0])
    common = tuple(min(row[index] for row in exponent_rows) for index in range(width))
    reduced = {
        tuple(power - common[index] for index, power in enumerate(row)): Fraction(coefficient)
        for row, coefficient in polynomial.items()
    }
    degrees = tuple(max(row[index] for row in reduced) for index in range(width))
    active = tuple(index for index, degree in enumerate(degrees) if degree)
    grid_size = 1
    for index in active:
        grid_size *= degrees[index] + 1
    require(grid_size <= 250000, f"Bernstein sign grid too large: {grid_size}")
    coefficients = []
    for active_beta in itertools.product(*(range(degrees[index] + 1) for index in active)):
        beta = [0] * width
        for index, value in zip(active, active_beta):
            beta[index] = value
        total = Fraction(0)
        for alpha, coefficient in reduced.items():
            if any(alpha[index] > beta[index] for index in active):
                continue
            multiplier = Fraction(1)
            for index in active:
                multiplier *= Fraction(comb(beta[index], alpha[index]), comb(degrees[index], alpha[index]))
            total += coefficient * multiplier
        coefficients.append(total)
    negative = sum(value < 0 for value in coefficients)
    positive = sum(value > 0 for value in coefficients)
    if negative and not positive:
        sign = -1
    elif positive and not negative:
        sign = 1
    else:
        return None
    public_coefficients = [str(value) for value in coefficients]
    return {
        "sign": sign,
        "common_positive_monomial": list(common),
        "active_parameter_indices": list(active),
        "active_degrees": [degrees[index] for index in active],
        "bernstein_grid_size": grid_size,
        "negative_coefficients": negative,
        "zero_coefficients": grid_size - negative - positive,
        "positive_coefficients": positive,
        "bernstein_coefficients_sha256": sha(public_coefficients),
    }


class SignOracle:
    """Direct full-map algebraic audit of every tree/sunlet separator."""

    def __init__(self, atlas):
        self.atlas = atlas
        self.descriptors = {}
        self.cache = {}
        self.catalog = {}
        self.raw_uses = 0

    def descriptor(self, graph):
        key = sha(graph_payload(graph))
        if key not in self.descriptors:
            self.descriptors[key] = self.atlas.model_descriptor_fast2(graph)
        return self.descriptors[key]

    def certify(self, source_graph, target_graph, topology):
        triple = tuple(topology["triple"])
        source_descriptor = self.descriptor(source_graph)
        target_descriptor = self.descriptor(target_graph)
        cache_key = (source_descriptor, target_descriptor, triple)
        if cache_key in self.cache:
            certificate_id = self.cache[cache_key]
            self.raw_uses += 1
            return certificate_id
        for ordering in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
            source_pullback = t3_pullback(self.atlas, source_descriptor, triple, ordering)
            target_pullback = t3_pullback(self.atlas, target_descriptor, triple, ordering)
            if not source_pullback and target_pullback:
                zero_side, negative_side, nonzero = "source", "target", target_pullback
            elif not target_pullback and source_pullback:
                zero_side, negative_side, nonzero = "target", "source", source_pullback
            else:
                continue
            sign = bernstein_strict_sign(nonzero)
            if sign is None or sign["sign"] != -1:
                continue
            require(topology[f"{zero_side}_type"] == "tree", "T3 zero side is not structural tree")
            require(topology[f"{negative_side}_type"] == "sunlet", "T3 negative side is not structural sunlet")
            certificate = {
                "triple": list(triple),
                "ordered_triple": [triple[index] for index in ordering],
                "invariant": "V^2*X_g-X_s^2*Y_g*Z_g",
                "zero_on": zero_side,
                "strictly_negative_on": negative_side,
                "zero_pullback": "coefficientwise exact zero on the full Fourier map",
                "negative_pullback_sha256": sha(sparse_public(nonzero)),
                "negative_pullback_terms": len(nonzero),
                "bernstein_certificate": sign,
                "domain": "open unit parameter cube, hence principal D_plus and strict continuous-time subdomains",
            }
            certificate_id = f"TS:{sha(certificate)}"
            self.catalog[certificate_id] = certificate
            self.cache[cache_key] = certificate_id
            self.raw_uses += 1
            return certificate_id
        raise ProbeFailure(
            f"TREE_SUNLET_FULL_MAP_SIGN_UNRESOLVED:{triple}:"
            f"{sha(source_descriptor.__dict__)}:{sha(target_descriptor.__dict__)}"
        )

    def public(self):
        return {
            "raw_uses": self.raw_uses,
            "canonical_certificates": len(self.catalog),
            "certificates": dict(sorted(self.catalog.items())),
            "method": "exact full-map T_i pullback plus exact tensor Bernstein sign on the open unit cube",
        }


def classify_pair(
    atlas, parent: dict[str, object], source_graph, target_graph,
    source_key, target_key, source_underlying, target_underlying, sign_oracle,
):
    # Exact labelled relations are load-bearing terminals and take precedence
    # over every topology/sign finder.  Unequal underlying WL hashes safely
    # preclude both exact isomorphism and ordinary-triangle equivalence.
    status, witnesses = ("none", [])
    if source_underlying == target_underlying:
        status, witnesses = exact_relation(atlas, source_graph, target_graph)
    if status in {"isomorphic", "triangle"}:
        coherent = [witness for witness in witnesses if mapping_restricts(atlas, parent, witness, status)]
        require(len(witnesses) == 1, f"nonunique child transport: {len(witnesses)}")
        require(len(coherent) == 1, f"child transport does not uniquely restrict parent: {len(coherent)}")
        witness = coherent[0]
        return {
            "status": status,
            "transport_sha256": witness["transport_sha256"],
            "transport": witness["public"],
            "parent_transport_sha256": parent["transport"]["transport_sha256"],
            "transport_restriction": "exact_on_all_parent_mixed_vertices",
            "global_triangle": parent.get("global_triangle"),
        }, witness

    topology = topology_compare(source_key, target_key)
    require(topology is not None, "equal invariant topology deck has no graph terminal; algebra/lifted separator required")
    if topology["status"] == "strict_tree_sunlet":
        topology = dict(topology)
        topology["sign_certificate_id"] = sign_oracle.certify(source_graph, target_graph, topology)
        topology["certificate"] = "exact full-map T_i pullback and strict Bernstein sign"
    return topology, None


class AnchoredRelationRegistry:
    """Exact canonical dedup of source/target graphs plus their transport."""

    def __init__(self, atlas):
        self.atlas = atlas
        self.buckets: dict[str, list[int]] = collections.defaultdict(list)
        self.representatives: list[nx.Graph] = []

    def combined(self, anchor: dict[str, object]) -> nx.Graph:
        result = nx.Graph()
        for side, graph in (("S", anchor["source_graph"]), ("T", anchor["target_graph"])):
            mixed = self.atlas.sd0_mixed(graph)
            triangle = (
                anchor["transport"]["source_triangle"]
                if side == "S"
                else anchor["transport"]["target_triangle"]
            )
            triangle = frozenset() if triangle is None else triangle
            for node, data in mixed.nodes(data=True):
                result.add_node((side, "v", node), color=f"{side}:vertex:{data.get('label')!r}")
            for number, (u, v, data) in enumerate(sorted(mixed.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1])))):
                edge_node = (side, "e", number)
                edge = frozenset((u, v))
                result.add_node(edge_node, color=f"{side}:edge:{edge in triangle}")
                heads = data.get("heads", frozenset())
                result.add_edge(edge_node, (side, "v", u), color=f"incidence:{u in heads}")
                result.add_edge(edge_node, (side, "v", v), color=f"incidence:{v in heads}")
        for source, target in anchor["transport"]["vertex_map"].items():
            result.add_edge(("S", "v", source), ("T", "v", target), color="transport")
        result.add_node(("relation",), color=f"relation:{anchor['status']}")
        return result

    def add(self, anchor: dict[str, object]) -> int:
        combined = self.combined(anchor)
        bucket = nx.weisfeiler_lehman_graph_hash(combined, node_attr="color", edge_attr="color", iterations=8)
        node_match = lambda a, b: a.get("color") == b.get("color")
        edge_match = lambda a, b: a.get("color") == b.get("color")
        for class_id in self.buckets[bucket]:
            if nx.is_isomorphic(combined, self.representatives[class_id], node_match=node_match, edge_match=edge_match):
                return class_id
        class_id = len(self.representatives)
        self.representatives.append(combined)
        self.buckets[bucket].append(class_id)
        return class_id


def terminal_four_port_inventory(atlas, sources, targets):
    manifests = {}
    terminal_keys = set()
    status_counts = collections.Counter()
    stratum_counts = collections.Counter()
    for path in sorted(RESULT4.glob("source_*/residual_manifest.json")):
        manifest = json.loads(path.read_text())
        source_index = manifest["source_index"]
        manifests[source_index] = manifest
        for row in manifest["records"]:
            if row["status"] in {"isomorphic", "triangle"}:
                key = (source_index, row["canonical_class_id"])
                terminal_keys.add(key)
                status_counts[row["status"]] += 1
                stratum_counts[(row["status"], row["stratum"])] += 1
    require(len(terminal_keys) == 55, "four-port terminal class census")
    members: dict[tuple[int, int], list[dict[str, object]]] = collections.defaultdict(list)
    with gzip.open(RAW4, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            key = (row["source_index"], row.get("class_id"))
            if key in terminal_keys:
                members[key].append(row)
    require(sum(map(len, members.values())) == 80, "four-port terminal member census")
    return manifests, members, status_counts, stratum_counts


def base_anchor(anchor_id, origin, source_graph, target_graph, status, witness, metadata):
    return {
        "anchor_id": anchor_id,
        "origin": origin,
        "labels": len(labels_of(source_graph)),
        "source_graph": source_graph,
        "target_graph": target_graph,
        "status": status,
        "transport": witness,
        "global_triangle": global_triangle_payload(witness),
        "metadata": metadata,
    }


def four_port_anchors(atlas, sources, targets):
    manifests, members, status_counts, stratum_counts = terminal_four_port_inventory(atlas, sources, targets)
    direct, omitted_roots, repaired, first_rows = [], [], [], []
    for key in sorted(members):
        source_index, class_id = key
        manifest_row = manifests[source_index]["records"][class_id]
        for member_index, row in enumerate(members[key]):
            permutation = tuple(row["port_permutation"])
            record = atlas.relabel_record(targets[row["target_index"]], permutation)
            source_graph = sources[source_index].graph
            selected_target = atlas.selected_graph_from_completion(record)
            parent_status, parent_witnesses = exact_relation(atlas, source_graph, selected_target)
            require(parent_status in {"isomorphic", "triangle"}, "terminal member lost graph relation")
            require(len(parent_witnesses) == 1, "four-port parent transport nonunique")
            parent = base_anchor(
                f"four-parent:raw{row['raw_id']}",
                manifest_row["stratum"],
                source_graph,
                selected_target,
                parent_status,
                parent_witnesses[0],
                {"source_index": source_index, "class_id": class_id, "raw_id": row["raw_id"]},
            )
            if not record.dummy_labels:
                target_graph = record.graph
                require(parent_status == row["status"], "direct member status drift")
                direct.append(base_anchor(
                    f"direct:raw{row['raw_id']}", "direct_no_dummy", source_graph, target_graph,
                    parent_status, parent_witnesses[0], parent["metadata"],
                ))
                continue
            omitted_roots.append(parent)
            candidates = internal_candidates(source_graph)
            require(len(candidates) == 7, "four-port source candidate count")
            for role in sorted(record.dummy_labels):
                target_graph = promote_target(atlas, targets[row["target_index"]], permutation, role, 4)
                target_key = topology_key(atlas, target_graph)
                for insertion_index, candidate in enumerate(candidates):
                    child_source = insert_leaf(atlas, source_graph, candidate, 4)
                    topology = topology_compare(topology_key(atlas, child_source), target_key)
                    child_id = f"repair:raw{row['raw_id']}:{role}:i{insertion_index}"
                    if topology is not None:
                        result = {"child_id": child_id, "parent_id": parent["anchor_id"], **topology}
                    else:
                        status, witnesses = exact_relation(atlas, child_source, target_graph)
                        require(status in {"isomorphic", "triangle"}, f"omitted first child equal-deck nonterminal:{child_id}:{source_key if False else ''}")
                        coherent = [w for w in witnesses if mapping_restricts(atlas, parent, w, status)]
                        require(len(witnesses) == len(coherent) == 1, "omitted child parent transport")
                        witness = coherent[0]
                        result = {
                            "child_id": child_id,
                            "parent_id": parent["anchor_id"],
                            "status": status,
                            "transport_sha256": witness["transport_sha256"],
                            "parent_transport_sha256": parent["transport"]["transport_sha256"],
                        }
                        require(not [d for d in target_graph.nodes.values() if d.get("dummy")], "surviving repaired anchor retains dummy")
                        repaired.append(base_anchor(
                            child_id,
                            "omitted_terminal_first_child",
                            child_source,
                            target_graph,
                            status,
                            witness,
                            {
                                "parent_id": parent["anchor_id"], "source_index": source_index,
                                "class_id": class_id, "raw_id": row["raw_id"],
                                "role": role, "source_insertion_index": insertion_index,
                            },
                        ))
                        repaired[-1]["global_triangle"] = parent["global_triangle"]
                    first_rows.append(result)
    counts = collections.Counter(row["status"] for row in first_rows)
    require(len(direct) == 26, f"direct raw anchors {len(direct)}")
    require(len(repaired) == 13, f"repaired raw anchors {len(repaired)}")
    require(counts == collections.Counter({"displayed_quartet_mismatch": 456, "strict_tree_sunlet": 63, "isomorphic": 13}), f"omitted child census {counts}")
    require(all(anchor["status"] == "isomorphic" for anchor in repaired), "repaired anchor not isomorphic")
    return direct + repaired, {
        "terminal_class_statuses": dict(status_counts),
        "terminal_class_strata": {f"{a}:{b}": value for (a, b), value in sorted(stratum_counts.items())},
        "terminal_member_roots": sum(map(len, members.values())),
        "omitted_member_roots": len(omitted_roots),
        "omitted_first_child_raw": len(first_rows),
        "omitted_first_child_counts": dict(counts),
        "omitted_first_child_hashes": [sha(row) for row in first_rows],
    }


def theta2_anchors(atlas):
    sources = atlas.source_supports(("theta2",))
    targets = atlas.target_completions(5, True) + atlas.target_completions(5, False)
    permutations = tuple(itertools.permutations(range(5)))
    with gzip.open(THETA2_CLASSES, "rt") as handle:
        partition = json.load(handle)
    classes = [row for row in partition["classes"] if row["category"] == "isomorphic"]
    require(len(classes) == 32, "theta2 iso class count")
    anchors = []
    roots_by_dummy_count = collections.Counter()
    first_rows = []
    second_rows = []
    first_continuations = []
    by_source_classes = collections.Counter()
    by_source_raw = collections.Counter()
    for row in classes:
        by_source_classes[row["source_index"]] += 1
        for member in row["raw_members"]:
            permutation = permutations[member["permutation_index"]]
            target_record = atlas.relabel_record(targets[member["target_index"]], permutation)
            target_graph = atlas.selected_graph_from_completion(target_record)
            source_graph = sources[row["source_index"]].graph
            status, witnesses = exact_relation(atlas, source_graph, target_graph)
            require(status == "isomorphic" and len(witnesses) == 1, "theta2 iso transport")
            metadata = {
                "source_index": row["source_index"], "repair_index": row["source_repair_index"],
                "class_id": row["class_id"], "raw_id": member["raw_id"],
                "target_index": member["target_index"], "permutation_index": member["permutation_index"],
            }
            root = base_anchor(
                f"theta2-root:raw{member['raw_id']}", "theta2_selected_root",
                source_graph, target_graph, status, witnesses[0], metadata,
            )
            roles = tuple(sorted(target_record.dummy_labels))
            roots_by_dummy_count[len(roles)] += 1
            if not roles:
                anchors.append(base_anchor(
                    f"theta2:raw{member['raw_id']}", "theta2_physical_five_port",
                    source_graph, target_record.graph, status, witnesses[0], metadata,
                ))
            else:
                candidates = internal_candidates(source_graph)
                require(len(candidates) == 8, "theta2 five-port source candidate count")
                for role in roles:
                    promoted_full = promote_graph_role(target_record.graph, role, 5)
                    promoted_selected = selected_from_full_graph(promoted_full)
                    target_key = topology_key(atlas, promoted_selected)
                    for insertion_index, candidate in enumerate(candidates):
                        child_source = insert_leaf(atlas, source_graph, candidate, 5)
                        child_id = f"theta2-r1:raw{member['raw_id']}:{role}:i{insertion_index}"
                        topology = topology_compare(topology_key(atlas, child_source), target_key)
                        if topology is not None:
                            first_rows.append({
                                "child_id": child_id, "parent_id": root["anchor_id"], **topology,
                            })
                            continue
                        child_status, child_witnesses = exact_relation(
                            atlas, child_source, promoted_selected
                        )
                        require(
                            child_status == "isomorphic" and len(child_witnesses) == 1,
                            "theta2 first restoration equal-deck terminal",
                        )
                        coherent = [
                            witness for witness in child_witnesses
                            if mapping_restricts(atlas, root, witness, child_status)
                        ]
                        require(len(coherent) == 1, "theta2 first restoration transport")
                        child = base_anchor(
                            child_id,
                            "theta2_restored_six_port" if len(roles) == 1 else "theta2_first_continuation",
                            child_source, promoted_selected, child_status, coherent[0],
                            {
                                **metadata, "parent_id": root["anchor_id"],
                                "promoted_role": role,
                                "remaining_roles": [value for value in roles if value != role],
                                "source_insertion_index": insertion_index,
                            },
                        )
                        first_rows.append({
                            "child_id": child_id, "parent_id": root["anchor_id"],
                            "status": child_status,
                            "transport_sha256": coherent[0]["transport_sha256"],
                            "parent_transport_sha256": root["transport"]["transport_sha256"],
                        })
                        if len(roles) == 1:
                            require(
                                not [data for data in promoted_full.nodes.values() if data.get("dummy")],
                                "theta2 six-port anchor retains dummy",
                            )
                            child["target_graph"] = promoted_full
                            anchors.append(child)
                        else:
                            first_continuations.append((child, promoted_full, tuple(value for value in roles if value != role)))
            by_source_raw[row["source_index"]] += 1
    require(roots_by_dummy_count == collections.Counter({0: 24, 1: 40, 2: 16}), f"theta2 dummy-root profile {roots_by_dummy_count}")
    require(len(first_rows) == 576, f"theta2 first restoration count {len(first_rows)}")
    first_counts = collections.Counter(row["status"] for row in first_rows)
    require(first_counts == collections.Counter({
        "displayed_quartet_mismatch": 504, "isomorphic": 72,
    }), f"theta2 first restoration census {first_counts}")
    require(len(first_continuations) == 32, "theta2 continuation census")

    for parent, full_target, remaining_roles in first_continuations:
        require(len(remaining_roles) == 1, "theta2 second restoration role count")
        role = remaining_roles[0]
        promoted_full = promote_graph_role(full_target, role, 6)
        promoted_selected = selected_from_full_graph(promoted_full)
        require(
            not [data for data in promoted_full.nodes.values() if data.get("dummy")],
            "theta2 seven-port anchor retains dummy",
        )
        target_key = topology_key(atlas, promoted_selected)
        candidates = internal_candidates(parent["source_graph"])
        require(len(candidates) == 9, "theta2 six-port source candidate count")
        for insertion_index, candidate in enumerate(candidates):
            child_source = insert_leaf(atlas, parent["source_graph"], candidate, 6)
            child_id = f"theta2-r2:{parent['anchor_id']}:{role}:i{insertion_index}"
            topology = topology_compare(topology_key(atlas, child_source), target_key)
            if topology is not None:
                second_rows.append({
                    "child_id": child_id, "parent_id": parent["anchor_id"], **topology,
                })
                continue
            child_status, child_witnesses = exact_relation(atlas, child_source, promoted_selected)
            require(
                child_status == "isomorphic" and len(child_witnesses) == 1,
                "theta2 second restoration equal-deck terminal",
            )
            coherent = [
                witness for witness in child_witnesses
                if mapping_restricts(atlas, parent, witness, child_status)
            ]
            require(len(coherent) == 1, "theta2 second restoration transport")
            second_rows.append({
                "child_id": child_id, "parent_id": parent["anchor_id"],
                "status": child_status,
                "transport_sha256": coherent[0]["transport_sha256"],
                "parent_transport_sha256": parent["transport"]["transport_sha256"],
            })
            anchors.append(base_anchor(
                child_id, "theta2_restored_seven_port", child_source, promoted_full,
                child_status, coherent[0],
                {
                    **parent["metadata"], "parent_id": parent["anchor_id"],
                    "promoted_role": role, "source_insertion_index": insertion_index,
                },
            ))

    require(len(second_rows) == 288, f"theta2 second restoration count {len(second_rows)}")
    second_counts = collections.Counter(row["status"] for row in second_rows)
    require(second_counts == collections.Counter({
        "displayed_quartet_mismatch": 256, "isomorphic": 32,
    }), f"theta2 second restoration census {second_counts}")
    require(len(anchors) == 96, f"theta2 physical raw anchor count {len(anchors)}")
    require(set(by_source_classes.values()) == {8} and set(by_source_raw.values()) == {20}, "theta2 per-repair census")
    return anchors, {
        "selected_iso_canonical_classes": len(classes),
        "selected_iso_raw_roots": sum(by_source_raw.values()),
        "selected_root_dummy_profile": dict(sorted(roots_by_dummy_count.items())),
        "first_restoration_raw": len(first_rows),
        "first_restoration_counts": dict(sorted(first_counts.items())),
        "first_restoration_ordered_hashes": [sha(row) for row in first_rows],
        "second_restoration_raw": len(second_rows),
        "second_restoration_counts": dict(sorted(second_counts.items())),
        "second_restoration_ordered_hashes": [sha(row) for row in second_rows],
        "physical_raw_anchors": len(anchors),
        "classes_per_repair": dict(by_source_classes), "raw_per_repair": dict(by_source_raw),
    }


def three_port_anchors(atlas):
    # The ordinary tree support has no internal component arc: its root
    # suppression is the labelled three-star.  It is included as a terminal
    # anchor, while its arbitrary pendant words are recovered by bridge/tree
    # split reconstruction rather than by an internal-arc probe.
    tree = nx.DiGraph(name="three_port_tree")
    for node, role, label in (
        ("r", "root", None), ("v", "tree", None),
        ("L0", "leaf", 0), ("L1", "leaf", 1), ("L2", "leaf", 2),
    ):
        tree.add_node(node, role=role, label=label, dummy=False, dummy_name=None)
    tree.add_edges_from((("r", "L0"), ("r", "v"), ("v", "L1"), ("v", "L2")))
    status, witnesses = exact_relation(atlas, tree, tree)
    require(status == "isomorphic" and len(witnesses) == 1, "tree identity transport")
    anchors = [base_anchor("three-tree:identity", "three_port_tree", tree, tree, status, witnesses[0], {})]
    return anchors, {
        "tree": 1,
        "internal_component_arcs": 0,
        "closure_mechanism": "ordinary labelled tree split and bridge reconstruction",
    }


def exact_pair_class(atlas, registry, source_graph, target_graph):
    """Canonicalize an ordered labelled source/target mixed-graph pair."""
    pair = nx.Graph()
    for side, graph in (("S", source_graph), ("T", target_graph)):
        mixed = atlas.sd0_mixed(graph)
        incidence_graph = atlas.mixed_incidence_graph(mixed)
        for node, data in incidence_graph.nodes(data=True):
            pair.add_node(
                (side, node), color=(side, data.get("kind"), data.get("label"))
            )
        for left, right, data in incidence_graph.edges(data=True):
            pair.add_edge((side, left), (side, right), color=data.get("head"))
    bucket = nx.weisfeiler_lehman_graph_hash(
        pair, node_attr="color", edge_attr="color", iterations=8
    )
    node_match = lambda left, right: left.get("color") == right.get("color")
    edge_match = lambda left, right: left.get("color") == right.get("color")
    for class_id, (other_bucket, representative) in enumerate(registry):
        if bucket == other_bucket and nx.is_isomorphic(
            pair, representative, node_match=node_match, edge_match=edge_match
        ):
            return class_id
    registry.append((bucket, pair))
    return len(registry) - 1


def sparse_public(polynomial):
    return [
        [list(exponent), str(coefficient)]
        for exponent, coefficient in sorted(polynomial.items())
    ]


def evaluate_sparse(polynomial, point):
    total = 0
    for exponent, coefficient in polynomial.items():
        term = coefficient
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        total += term
    return total


def cycle_quadratic_certificate(atlas, source_graph, target_graph):
    source = atlas.model_descriptor_fast2(source_graph)
    target = atlas.model_descriptor_fast2(target_graph)
    source_rank = atlas.rank_certificate(source)["rank"]
    target_rank = atlas.rank_certificate(target)["rank"]
    separator = atlas.quadratic_separator_fast(source, target, max_block_size=16)
    require(separator is not None, "cycle physical equal-topology pair lacks quadratic")
    target_outputs = atlas.output_sparse_polynomials(target)
    target_columns = [
        atlas.sparse_mul(target_outputs[left], target_outputs[right])
        for left, right in separator["coordinate_pairs"]
    ]
    require(
        not atlas.sparse_lincomb(target_columns, separator["coefficients"]),
        "cycle quadratic nonzero on target",
    )
    source_pullback = separator["source_pullback"]
    require(bool(source_pullback), "cycle quadratic zero on source")
    witness = None
    for salt in range(32):
        edge_pairs, lambdas = atlas.default_exact_point(source, salt)
        require(all(0 < s < 1 and 0 < g < 1 and g > 2 * s - 1 for s, g in edge_pairs), "cycle witness outside D_plus")
        # The chosen exact witness is also in the open continuous-time cone.
        require(all(s * s < g for s, g in edge_pairs), "cycle witness outside strict CT cone")
        point = tuple(value for pair in edge_pairs for value in pair) + tuple(lambdas)
        source_value = evaluate_sparse(source_pullback, point)
        if source_value:
            witness = {
                "salt": salt,
                "edge_pairs": [[str(s), str(g)] for s, g in edge_pairs],
                "lambdas": [str(value) for value in lambdas],
                "source_value": str(source_value),
                "domain": "strict continuous-time K2P (hence D_plus)",
            }
            break
    require(witness is not None, "cycle quadratic lacks exact CT witness")
    public_pullback = sparse_public(source_pullback)
    return {
        "status": "quadratic_excluded",
        "source_rank": source_rank,
        "target_rank": target_rank,
        "weight": list(separator["weight"]),
        "coordinate_pairs": [list(pair) for pair in separator["coordinate_pairs"]],
        "coefficients": [str(value) for value in separator["coefficients"]],
        "source_pullback_sha256": sha(public_pullback),
        "source_pullback_terms": len(public_pullback),
        "strict_CT_witness": witness,
    }


def cycle_anchors(atlas):
    """Close every three-port cycle target, including all dummy restorations."""
    sources = atlas.source_supports(("cycle",))
    targets = atlas.target_completions(3, True) + atlas.target_completions(3, False)
    permutations = tuple(itertools.permutations(range(3)))
    require(len(sources) == 2 and len(targets) == 1120 and len(permutations) == 6, "cycle raw universe dimensions")

    source_states = {}
    target_states = {}

    def source_state(key):
        if key in source_states:
            return source_states[key]
        source_index, path = key
        if not path:
            graph = sources[source_index].graph
        else:
            parent = source_state((source_index, path[:-1]))[0]
            candidates = internal_candidates(parent)
            graph = insert_leaf(atlas, parent, candidates[path[-1]], 2 + len(path))
        value = graph, topology_key(atlas, graph)
        source_states[key] = value
        return value

    def target_state(key):
        if key in target_states:
            return target_states[key]
        target_index, permutation_index, roles = key
        record = atlas.relabel_record(targets[target_index], permutations[permutation_index])
        full_graph = record.graph
        for offset, role in enumerate(roles):
            full_graph = promote_graph_role(full_graph, role, 3 + offset)
        selected_graph = selected_from_full_graph(full_graph)
        value = full_graph, selected_graph, topology_key(atlas, selected_graph)
        target_states[key] = value
        return value

    initial_counts = collections.Counter()
    dummy_roots = []
    anchors = []
    initial_hashes = []
    for source_index, source in enumerate(sources):
        source_topology = source_state((source_index, ()))[1]
        for target_index, target in enumerate(targets):
            for permutation_index, permutation in enumerate(permutations):
                record = atlas.relabel_record(target, permutation)
                selected = atlas.selected_graph_from_completion(record)
                topology = topology_compare(source_topology, topology_key(atlas, selected))
                raw_id = len(initial_hashes)
                if topology is not None:
                    status = topology["status"]
                elif record.dummy_labels:
                    status = "dummy_equal_topology"
                    dummy_roots.append({
                        "root_id": len(dummy_roots), "raw_id": raw_id,
                        "source_index": source_index, "target_index": target_index,
                        "permutation_index": permutation_index,
                        "roles": tuple(sorted(record.dummy_labels)),
                    })
                else:
                    status, witnesses = exact_relation(atlas, source.graph, record.graph)
                    require(status in {"isomorphic", "triangle"} and len(witnesses) == 1, "cycle no-dummy terminal")
                    anchors.append(base_anchor(
                        f"cycle-direct:raw{raw_id}", "cycle_physical_three_port",
                        source.graph, record.graph, status, witnesses[0],
                        {
                            "raw_id": raw_id, "source_index": source_index,
                            "target_index": target_index, "permutation_index": permutation_index,
                        },
                    ))
                row = {
                    "raw_id": raw_id, "source_index": source_index,
                    "target_index": target_index, "permutation_index": permutation_index,
                    "status": status,
                }
                initial_hashes.append(sha(row))
                initial_counts[status] += 1
    require(initial_counts == collections.Counter({
        "strict_tree_sunlet": 7452, "dummy_equal_topology": 5964,
        "triangle": 16, "isomorphic": 8,
    }), f"cycle initial census {initial_counts}")
    require(len(anchors) == 24 and len(dummy_roots) == 5964, "cycle initial anchor/root census")

    states = [
        (row["root_id"], (row["source_index"], ()),
         (row["target_index"], row["permutation_index"], ()), row["roles"])
        for row in dummy_roots
    ]
    depth_reports = []
    nonterminal_leaves = []
    restored_anchor_rows = []
    for depth in range(1, 5):
        counts = collections.Counter()
        hashes = []
        next_states = []
        for root_id, source_key, target_key, remaining in states:
            source_graph = source_state(source_key)[0]
            candidates = internal_candidates(source_graph)
            for role in remaining:
                child_target_key = (target_key[0], target_key[1], target_key[2] + (role,))
                full_target, target_graph, target_topology = target_state(child_target_key)
                child_remaining = tuple(value for value in remaining if value != role)
                for insertion_index in range(len(candidates)):
                    child_source_key = (source_key[0], source_key[1] + (insertion_index,))
                    child_source, source_topology = source_state(child_source_key)
                    topology = topology_compare(source_topology, target_topology)
                    witness = None
                    if topology is not None:
                        status = topology["status"]
                    elif child_remaining:
                        status = "equal_topology_continuation"
                        next_states.append((root_id, child_source_key, child_target_key, child_remaining))
                    else:
                        try:
                            status, witnesses = exact_relation(atlas, child_source, target_graph)
                        except ValueError:
                            status, witnesses = "none", []
                        if status in {"isomorphic", "triangle"}:
                            require(len(witnesses) == 1, "cycle restored terminal transport")
                            witness = witnesses[0]
                            root = dummy_roots[root_id]
                            root_source = sources[root["source_index"]].graph
                            root_target = target_state((root["target_index"], root["permutation_index"], ()))[1]
                            parent_status, parent_witnesses = exact_relation(atlas, root_source, root_target)
                            require(parent_status == "isomorphic" and len(parent_witnesses) == 1, "cycle restored parent transport")
                            parent = base_anchor(
                                f"cycle-root:raw{root['raw_id']}", "cycle_selected_root",
                                root_source, root_target, parent_status, parent_witnesses[0], root,
                            )
                            require(mapping_restricts(atlas, parent, witness, status), "cycle restored transport restriction")
                            anchor = base_anchor(
                                f"cycle-restored:raw{root['raw_id']}:{role}:i{insertion_index}",
                                "cycle_restored_four_port", child_source, full_target,
                                status, witness,
                                {
                                    **root, "parent_id": parent["anchor_id"],
                                    "role_order": list(child_target_key[2]),
                                    "source_insertion_path": list(child_source_key[1]),
                                    "parent_transport_sha256": parent["transport"]["transport_sha256"],
                                },
                            )
                            anchors.append(anchor)
                            restored_anchor_rows.append({
                                "anchor_id": anchor["anchor_id"],
                                "parent_id": parent["anchor_id"],
                                "transport_sha256": witness["transport_sha256"],
                                "parent_transport_sha256": parent["transport"]["transport_sha256"],
                            })
                        else:
                            status = "physical_equal_topology_nonterminal"
                            nonterminal_leaves.append((root_id, child_source_key, child_target_key))
                    counts[status] += 1
                    hashes.append(sha({
                        "root_id": root_id, "source_parent_path": list(source_key[1]),
                        "target_parent_roles": list(target_key[2]), "promoted_role": role,
                        "source_insertion_index": insertion_index, "status": status,
                        "transport_sha256": None if witness is None else witness["transport_sha256"],
                    }))
        depth_reports.append({
            "depth": depth, "parents": len(states), "raw_children": sum(counts.values()),
            "counts": dict(sorted(counts.items())), "continuations": len(next_states),
            "ordered_raw_hashes": hashes, "ordered_raw_hash_root": sha(hashes),
        })
        states = next_states
        if not states:
            break
    expected_depths = [
        (5964, 48924, {"displayed_quartet_mismatch": 36840, "strict_tree_sunlet": 6972, "equal_topology_continuation": 4968, "isomorphic": 12, "physical_equal_topology_nonterminal": 132}),
        (4968, 38560, {"displayed_quartet_mismatch": 34968, "strict_tree_sunlet": 432, "equal_topology_continuation": 3160}),
        (3160, 24440, {"displayed_quartet_mismatch": 22520, "strict_tree_sunlet": 192, "equal_topology_continuation": 1728}),
        (1728, 10368, {"displayed_quartet_mismatch": 10368}),
    ]
    require(len(depth_reports) == 4 and not states, "cycle restoration termination")
    for observed, (parents, raw, counts) in zip(depth_reports, expected_depths):
        require(observed["parents"] == parents and observed["raw_children"] == raw and observed["counts"] == counts, f"cycle restoration depth {observed['depth']} census")
    require(len(anchors) == 36 and len(restored_anchor_rows) == 12, "cycle physical anchor census")
    require(len(nonterminal_leaves) == 132, "cycle physical algebra-leaf census")

    pair_registry = []
    descriptor_registry = {}
    descriptor_examples = {}
    descriptor_multiplicity = collections.Counter()
    raw_algebra_bindings = []
    for root_id, source_key, target_key in nonterminal_leaves:
        source_graph = source_state(source_key)[0]
        target_graph = target_state(target_key)[1]
        graph_class_id = exact_pair_class(
            atlas, pair_registry, source_graph, target_graph
        )
        source_descriptor = atlas.model_descriptor_fast2(source_graph)
        target_descriptor = atlas.model_descriptor_fast2(target_graph)
        descriptor_pair = (source_descriptor, target_descriptor)
        if descriptor_pair not in descriptor_registry:
            descriptor_registry[descriptor_pair] = len(descriptor_registry)
        descriptor_class_id = descriptor_registry[descriptor_pair]
        descriptor_multiplicity[descriptor_class_id] += 1
        descriptor_examples.setdefault(
            descriptor_class_id,
            (root_id, source_key, target_key, source_descriptor, target_descriptor),
        )
        raw_algebra_bindings.append({
            "root_id": root_id,
            "source_state": [source_key[0], list(source_key[1])],
            "target_state": [target_key[0], target_key[1], list(target_key[2])],
            "semi_directed_graph_pair_class_id": graph_class_id,
            "descriptor_pair_class_id": descriptor_class_id,
        })
    require(len(pair_registry) == 30, f"cycle semi-directed graph-pair census {len(pair_registry)}")
    require(len(descriptor_registry) == 54, f"cycle descriptor-pair census {len(descriptor_registry)}")
    algebra_classes = []
    for class_id in sorted(descriptor_examples):
        root_id, source_key, target_key, source_descriptor, target_descriptor = descriptor_examples[class_id]
        algebra_classes.append({
            "descriptor_pair_class_id": class_id,
            "raw_multiplicity": descriptor_multiplicity[class_id],
            "source_descriptor_sha256": sha(source_descriptor.__dict__),
            "target_descriptor_sha256": sha(target_descriptor.__dict__),
            "example": {
                "root_id": root_id,
                "source_state": [source_key[0], list(source_key[1])],
                "target_state": [target_key[0], target_key[1], list(target_key[2])],
            },
            "certificate": cycle_quadratic_certificate(
                atlas, source_state(source_key)[0], target_state(target_key)[1]
            ),
        })
    require(sum(row["raw_multiplicity"] for row in algebra_classes) == 132, "cycle quadratic raw coverage")
    # Bind this independent enumeration to the separately released 54-class
    # compiler without importing its builder or trusting its class identifiers.
    released_quadratics = json.loads(CYCLE_QUADRATICS.read_text())
    released_classes = {
        (
            row["source_descriptor_sha256"], row["target_descriptor_sha256"],
            row["source_pullback_sha256"],
            released_quadratics["raw_multiplicity"][certificate_id],
        )
        for certificate_id, row in released_quadratics["certificates"].items()
    }
    independent_classes = {
        (
            row["source_descriptor_sha256"], row["target_descriptor_sha256"],
            row["certificate"]["source_pullback_sha256"], row["raw_multiplicity"],
        )
        for row in algebra_classes
    }
    require(independent_classes == released_classes, "cycle 54-class released-certificate binding")
    inventory = {
        "raw_initial_relations": 13440,
        "initial_counts": dict(sorted(initial_counts.items())),
        "initial_ordered_raw_hashes": initial_hashes,
        "initial_ordered_raw_hash_root": sha(initial_hashes),
        "dummy_root_profile": dict(sorted(collections.Counter(len(row["roles"]) for row in dummy_roots).items())),
        "restoration_depths": depth_reports,
        "restoration_edges": sum(row["raw_children"] for row in depth_reports),
        "restoration_terminates": True,
        "physical_anchor_presentations": len(anchors),
        "direct_physical_anchors": 24,
        "restored_physical_anchors": len(restored_anchor_rows),
        "restored_anchor_transports": restored_anchor_rows,
        "physical_equal_topology_quadratic_raw": 132,
        "physical_equal_topology_raw_bindings": raw_algebra_bindings,
        "physical_equal_topology_raw_binding_hashes": [sha(row) for row in raw_algebra_bindings],
        "physical_equal_topology_semi_directed_graph_pair_classes": len(pair_registry),
        "physical_equal_topology_descriptor_pair_classes": algebra_classes,
        "quadratic_classes": len(algebra_classes),
        "quadratic_unresolved": 0,
        "released_54_class_binding": {
            "status": "exact set equality by source descriptor, target descriptor, source pullback, and raw multiplicity",
            "released_quadratic_sha256": sha_file(CYCLE_QUADRATICS),
            "released_summary_sha256": sha_file(CYCLE_SUMMARY),
        },
    }
    # Release the large recursive topology caches before the probe stages.
    source_states.clear()
    target_states.clear()
    gc.collect()
    return anchors, inventory


def public_anchor(anchor: dict[str, object], canonical_id: int) -> dict[str, object]:
    return {
        "anchor_id": anchor["anchor_id"], "canonical_anchor_id": canonical_id,
        "origin": anchor["origin"], "labels": anchor["labels"], "status": anchor["status"],
        "source_graph_sha256": sha(graph_payload(anchor["source_graph"])),
        "target_graph_sha256": sha(graph_payload(anchor["target_graph"])),
        "source_internal_candidates": internal_candidates(anchor["source_graph"]),
        "target_internal_candidates": internal_candidates(anchor["target_graph"]),
        "transport_sha256": anchor["transport"]["transport_sha256"],
        "transport": anchor["transport"]["public"],
        "global_triangle": anchor.get("global_triangle"),
        "metadata": anchor["metadata"],
    }


def enumerate_one_port(atlas, anchors, registry, topology_memo, sign_oracle):
    counts = collections.Counter()
    by_origin = collections.Counter()
    hashes = []
    survivors = []
    exemplars = {}
    for anchor in anchors:
        label = anchor["labels"]
        source_candidates, target_candidates = internal_candidates(anchor["source_graph"]), internal_candidates(anchor["target_graph"])
        source_children = [(i, insert_leaf(atlas, anchor["source_graph"], candidate, label)) for i, candidate in enumerate(source_candidates)]
        target_children = [(i, insert_leaf(atlas, anchor["target_graph"], candidate, label)) for i, candidate in enumerate(target_candidates)]
        source_rows = [(i, graph, topology_memo.get(graph), underlying_relation_hash(atlas, graph)) for i, graph in source_children]
        target_rows = [(i, graph, topology_memo.get(graph), underlying_relation_hash(atlas, graph)) for i, graph in target_children]
        for source_index, source_graph, source_key, source_underlying in source_rows:
            for target_index, target_graph, target_key, target_underlying in target_rows:
                result, witness = classify_pair(
                    atlas, anchor, source_graph, target_graph, source_key, target_key,
                    source_underlying, target_underlying, sign_oracle,
                )
                row = {
                    "stage": "A+p", "parent_id": anchor["anchor_id"],
                    "source_insertion_index": source_index, "target_insertion_index": target_index,
                    **result,
                }
                hashes.append(sha(row))
                counts[result["status"]] += 1
                by_origin[(anchor["origin"], result["status"])] += 1
                exemplars.setdefault(f"A+p:{result['status']}", row)
                if witness is None:
                    continue
                child = base_anchor(
                    f"A+p:{anchor['anchor_id']}:{source_index}:{target_index}",
                    anchor["origin"], source_graph, target_graph, result["status"], witness,
                    {
                        "parent_id": anchor["anchor_id"], "source_insertion_index": source_index,
                        "target_insertion_index": target_index,
                    },
                )
                child["global_triangle"] = anchor.get("global_triangle")
                child["labels"] = label + 1
                child["canonical_relation_id"] = registry.add(child)
                child["public_row"] = row
                survivors.append(child)
    return counts, by_origin, hashes, survivors, exemplars


def enumerate_two_port(atlas, parents, registry, exemplars, topology_memo, sign_oracle):
    counts = collections.Counter()
    by_origin = collections.Counter()
    hashes = []
    survivors = []
    for parent_number, parent in enumerate(parents):
        if parent_number and parent_number % 250 == 0:
            print(
                f"probe-coherence: two-port parents {parent_number}/{len(parents)}",
                file=sys.stderr, flush=True,
            )
        label = parent["labels"]
        source_candidates, target_candidates = internal_candidates(parent["source_graph"]), internal_candidates(parent["target_graph"])
        source_rows = []
        for index, candidate in enumerate(source_candidates):
            graph = insert_leaf(atlas, parent["source_graph"], candidate, label)
            source_rows.append((index, graph, topology_memo.get(graph), underlying_relation_hash(atlas, graph)))
        target_rows = []
        for index, candidate in enumerate(target_candidates):
            graph = insert_leaf(atlas, parent["target_graph"], candidate, label)
            target_rows.append((index, graph, topology_memo.get(graph), underlying_relation_hash(atlas, graph)))
        for source_index, source_graph, source_key, source_underlying in source_rows:
            for target_index, target_graph, target_key, target_underlying in target_rows:
                result, witness = classify_pair(
                    atlas, parent, source_graph, target_graph, source_key, target_key,
                    source_underlying, target_underlying, sign_oracle,
                )
                row = {
                    "stage": "A+p+q", "parent_id": parent["anchor_id"],
                    "grandparent_id": parent["metadata"]["parent_id"],
                    "parent_source_insertion_index": parent["metadata"]["source_insertion_index"],
                    "parent_target_insertion_index": parent["metadata"]["target_insertion_index"],
                    "source_insertion_index": source_index, "target_insertion_index": target_index,
                    **result,
                }
                hashes.append(sha(row))
                counts[result["status"]] += 1
                by_origin[(parent["origin"], result["status"])] += 1
                exemplars.setdefault(f"A+p+q:{result['status']}", row)
                if witness is None:
                    continue
                child = base_anchor(
                    f"A+p+q:{parent['anchor_id']}:{source_index}:{target_index}",
                    parent["origin"], source_graph, target_graph, result["status"], witness,
                    {"parent_id": parent["anchor_id"], "source_insertion_index": source_index, "target_insertion_index": target_index},
                )
                child["global_triangle"] = parent.get("global_triangle")
                child["canonical_relation_id"] = registry.add(child)
                survivors.append({
                    "relation_id": child["anchor_id"], "canonical_relation_id": child["canonical_relation_id"],
                    "origin": child["origin"], **row,
                })
    return counts, by_origin, hashes, survivors


def build_certificate():
    atlas = load_atlas()
    sources4 = atlas.source_supports()
    targets4 = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    four_anchors, four_inventory = four_port_anchors(atlas, sources4, targets4)
    theta2, theta2_inventory = theta2_anchors(atlas)
    cycle, cycle_inventory = cycle_anchors(atlas)
    tree, three_inventory = three_port_anchors(atlas)
    anchors = four_anchors + theta2 + cycle + tree
    print(f"probe-coherence: physical anchors {len(anchors)}", file=sys.stderr, flush=True)

    anchor_registry = AnchoredRelationRegistry(atlas)
    coverage: dict[int, list[str]] = collections.defaultdict(list)
    public_anchors = []
    for anchor in anchors:
        class_id = anchor_registry.add(anchor)
        anchor["canonical_anchor_id"] = class_id
        coverage[class_id].append(anchor["anchor_id"])
        public_anchors.append(public_anchor(anchor, class_id))

    relation_registry = AnchoredRelationRegistry(atlas)
    topology_memo = TopologyMemo(atlas)
    sign_oracle = SignOracle(atlas)
    one_counts, one_by_origin, one_hashes, one_survivors, exemplars = enumerate_one_port(
        atlas, anchors, relation_registry, topology_memo, sign_oracle
    )
    print(
        f"probe-coherence: one-port raw {sum(one_counts.values())}, survivors {len(one_survivors)}",
        file=sys.stderr, flush=True,
    )
    two_counts, two_by_origin, two_hashes, two_survivors = enumerate_two_port(
        atlas, one_survivors, relation_registry, exemplars, topology_memo, sign_oracle
    )
    topology_memo_public = topology_memo.public()
    sign_oracle_public = sign_oracle.public()
    one_survivor_count = len(one_survivors)
    one_canonical_terminal_count = len({child["canonical_relation_id"] for child in one_survivors})
    one_public_survivors = [
        {
            "relation_id": child["anchor_id"],
            "canonical_relation_id": child["canonical_relation_id"],
            "origin": child["origin"], **child["public_row"],
        }
        for child in one_survivors
    ]
    two_survivor_count = len(two_survivors)
    two_canonical_terminal_count = len({row["canonical_relation_id"] for row in two_survivors})

    # The graph-bearing registries are no longer needed once public survivor
    # rows and exact canonical IDs have been materialized.  Releasing them
    # keeps the referee replay below the 1 GiB RSS ceiling during JSON sealing.
    topology_memo.representatives.clear()
    topology_memo.values.clear()
    topology_memo.buckets.clear()
    sign_oracle.descriptors.clear()
    sign_oracle.cache.clear()
    relation_registry.representatives.clear()
    relation_registry.buckets.clear()
    one_survivors.clear()
    gc.collect()

    # The previously reviewed 39-anchor subdeck remains an exact regression
    # lock even though the official universe is now larger.
    reviewed_origins = {"direct_no_dummy", "omitted_terminal_first_child"}
    reviewed_one = collections.Counter()
    for (origin, status), count in one_by_origin.items():
        if origin in reviewed_origins:
            reviewed_one[status] += count
    reviewed_two = collections.Counter()
    for (origin, status), count in two_by_origin.items():
        if origin in reviewed_origins:
            reviewed_two[status] += count
    require(reviewed_one == collections.Counter({
        "displayed_quartet_mismatch": 1820, "strict_tree_sunlet": 115,
        "isomorphic": 159, "triangle": 12,
    }), f"reviewed A+p regression {reviewed_one}")
    require(reviewed_two == collections.Counter({
        "displayed_quartet_mismatch": 10952, "strict_tree_sunlet": 170,
        "isomorphic": 1224, "triangle": 60,
    }), f"reviewed A+p+q regression {reviewed_two}")
    require(sum(reviewed_one.values()) == 2106 and sum(reviewed_two.values()) == 12406, "reviewed raw totals")

    one_terminal = one_counts["isomorphic"] + one_counts["triangle"]
    two_terminal = two_counts["isomorphic"] + two_counts["triangle"]
    require(one_terminal == one_survivor_count, "one-port terminal coverage")
    require(two_terminal == two_survivor_count, "two-port terminal coverage")
    require(not (set(one_counts) | set(two_counts)) - {
        "displayed_quartet_mismatch", "strict_tree_sunlet", "isomorphic", "triangle"
    }, "unexpected probe status")

    origin_anchor_counts = collections.Counter(anchor["origin"] for anchor in anchors)
    origin_canonical = collections.defaultdict(set)
    for anchor in anchors:
        origin_canonical[anchor["origin"]].add(anchor["canonical_anchor_id"])
    certificate = {
        "schema": "k2p-complete-coherent-probe-closure-v1",
        "status": "PASS",
        "scope": "all primitive rigid supports: tree, complete cycle raw/restoration universe, theta0/theta1/theta3 four-port anchors, repaired omitted terminals, and all four physically restored theta2 repairs",
        "inputs": {
            "atlas_sha256": sha_file(ATLAS_PATH), "raw_four_port_ledger_sha256": sha_file(RAW4),
            "theta2_class_partition_sha256": sha_file(THETA2_CLASSES),
            "theta2_summary_sha256": sha_file(THETA2_SUMMARY),
            "cycle_three_port_summary_sha256": sha_file(CYCLE_SUMMARY),
            "cycle_quadratic_certificates_sha256": sha_file(CYCLE_QUADRATICS),
            "cycle_physical_anchors_sha256": sha_file(CYCLE_ANCHORS),
            "cycle_full_completion_ledger_sha256": sha_file(CYCLE_FULL_LEDGER),
            "manifests": {
                str(path.relative_to(PROJECT)): sha_file(path)
                for path in sorted(RESULT4.glob("source_*/residual_manifest.json"))
            },
        },
        "four_port_terminal_inventory": four_inventory,
        "theta2_terminal_inventory": theta2_inventory,
        "cycle_terminal_inventory": cycle_inventory,
        "three_port_terminal_inventory": three_inventory,
        "anchors": {
            "raw_total": len(anchors), "raw_by_origin": dict(sorted(origin_anchor_counts.items())),
            "canonical_total": len(anchor_registry.representatives),
            "canonical_by_origin": {key: len(value) for key, value in sorted(origin_canonical.items())},
            "canonical_raw_coverage": {str(key): sorted(value) for key, value in sorted(coverage.items())},
            "records": public_anchors,
        },
        "one_port": {
            "raw_relations": sum(one_counts.values()), "status_counts": dict(sorted(one_counts.items())),
            "status_by_origin": {f"{origin}:{status}": count for (origin, status), count in sorted(one_by_origin.items())},
            "terminal_survivors": one_survivor_count,
            "canonical_terminal_relations": one_canonical_terminal_count,
            "ordered_raw_hashes": one_hashes, "ordered_raw_hash_root": sha(one_hashes),
            "survivors": one_public_survivors,
        },
        "two_port": {
            "parent_relations": one_survivor_count, "raw_relations": sum(two_counts.values()),
            "status_counts": dict(sorted(two_counts.items())),
            "status_by_origin": {f"{origin}:{status}": count for (origin, status), count in sorted(two_by_origin.items())},
            "terminal_survivors": two_survivor_count,
            "canonical_terminal_relations": two_canonical_terminal_count,
            "ordered_raw_hashes": two_hashes, "ordered_raw_hash_root": sha(two_hashes),
            "survivors": two_survivors,
        },
        "reviewed_39_anchor_regression": {
            "one_port_raw": sum(reviewed_one.values()), "one_port": dict(reviewed_one),
            "two_port_raw": sum(reviewed_two.values()), "two_port": dict(reviewed_two),
        },
        "coherence": {
            "anchor_transport_multiplicity": 1,
            "survivor_transport_multiplicity": 1,
            "every_survivor_restricts_parent": True,
            "ordinary_triangle_definition": "exactly two triangle-edge arrowheads enter one common reticulation vertex",
            "one_global_triangle": "a T witness is fixed at the earliest anchor and every descendant T witness uses the same literal triangle and restricted vertex map",
            "segment_location": "all nonterminal A+p edge pairs are pointwise separated; survivors give the unique transported physical arc",
            "segment_order": "only A+p+q relations with the unique A+p transport survive, so the two subdivision orders agree",
            "tree_support": "the three-port tree has no internal component arc; pendant words are recovered by the already separate bridge/split reconstruction",
            "topology_memo": topology_memo_public,
            "tree_sunlet_full_map_sign": sign_oracle_public,
        },
        "algebra_fallback": {
            "invoked": 54,
            "raw_relations": 132,
            "semi_directed_graph_pair_crosswalk_classes": 30,
            "exact_descriptor_pair_certificate_classes": 54,
            "reason": "the complete cycle restoration has 30 semi-directed graph-pair classes but 54 exact compiler descriptor-pair classes; all 54 independently replayed quadratics separate all 132 raw presentations. All later one-/two-port nonrelations are topological.",
        },
        "optimization_adversarial_regression": {
            "unsafe_cache_key": "semi-directed mixed isomorphism (rejected)",
            "unsafe_reviewed_39_A_plus_p": {
                "displayed_quartet_mismatch": 1820, "strict_tree_sunlet": 63,
                "isomorphic": 195, "triangle": 28,
            },
            "correct_cache_key": "exact rooted directed isomorphism preserving root/tree/retic roles and labels",
            "correct_reviewed_39_A_plus_p": {
                "displayed_quartet_mismatch": 1820, "strict_tree_sunlet": 115,
                "isomorphic": 159, "triangle": 12,
            },
            "mutation_result": "unsafe cache changes the frozen census and is rejected",
        },
        "proof_exemplars": exemplars,
        "unresolved": 0,
        "incoherent": 0,
    }
    certificate["payload_sha256"] = sha(certificate)
    return certificate


def main() -> int:
    if not __debug__:
        raise ProbeFailure("PROBE_COHERENCE_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "probe_certificate.json")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    certificate = build_certificate()
    if args.verify:
        observed = json.loads(args.verify.read_text())
        require(observed == certificate, "PROBE_CERTIFICATE_REPLAY_MISMATCH")
        print("K2P_COMPLETE_PROBE_COHERENCE_REPLAY_PASS")
    else:
        args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
        print("K2P_COMPLETE_PROBE_COHERENCE_BUILD_PASS")
    print(json.dumps({
        "payload_sha256": certificate["payload_sha256"],
        "raw_anchors": certificate["anchors"]["raw_total"],
        "canonical_anchors": certificate["anchors"]["canonical_total"],
        "one_port": certificate["one_port"]["raw_relations"],
        "two_port": certificate["two_port"]["raw_relations"],
        "unresolved": certificate["unresolved"], "incoherent": certificate["incoherent"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProbeFailure as error:
        print(f"PROBE_COHERENCE_FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
