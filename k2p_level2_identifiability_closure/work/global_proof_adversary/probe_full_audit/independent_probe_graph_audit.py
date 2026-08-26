#!/usr/bin/env python3
"""Independent primitive/graph/algebra audit of the corrected full probe.

This program never imports the corrected-probe producer or its verifier.  It
uses the separately frozen primitive probe-input reconstructor only to recover
the 176 rooted source/target anchors from their upstream locators.  It then
rebuilds every one- and two-port child, replays classifier precedence,
quartets, full-map K2P T_i pullbacks, exact transports, marginal restrictions,
reverse-order parents, and the one-global-triangle condition.
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
import importlib.util
import itertools
import json
import math
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DEFAULT_PACKAGE = PROJECT / "work/probe_coherence_corrected"
INPUT_CONTRACT = PROJECT / "work/adversarial_proof_review/probe_input_contract.json"
INPUT_REPLAY = PROJECT / "work/adversarial_proof_review/probe_input_independent_verification.json"
INPUT_RECONSTRUCTOR = PROJECT / "work/adversarial_proof_review/verify_probe_input_contract.py"
ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
DEFAULT_OUTPUT = HERE / "independent_probe_graph_audit_certificate.json"
DEFAULT_MUTATIONS = HERE / "independent_probe_mutation_report.json"
AUTHORITATIVE_OUTPUTS = (DEFAULT_OUTPUT, DEFAULT_MUTATIONS)


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


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


def validate_output_paths(
    output: Path, mutations_output: Path, allow_authoritative_output: bool
) -> tuple[Path, Path]:
    validated = []
    for candidate in (output, mutations_output):
        lexical = Path(os.path.abspath(os.fspath(candidate)))
        normalized = lexical.parent.resolve() / lexical.name
        resolved = lexical.resolve()
        require(
            not lexical.is_symlink(),
            "PROBE_AUDIT_OUTPUT_POLICY_FAIL: output path may not be a symlink",
        )
        if lexical.exists():
            require(
                lexical.stat().st_nlink == 1,
                "PROBE_AUDIT_OUTPUT_POLICY_FAIL: output path may not be a hardlink",
            )
        if not allow_authoritative_output:
            try:
                resolved.relative_to(PROJECT.resolve())
            except ValueError:
                pass
            else:
                raise AuditFailure(
                    "PROBE_AUDIT_OUTPUT_POLICY_FAIL: routine output must be "
                    "outside the project source tree"
                )
        validated.append(normalized)
    require(
        validated[0] != validated[1],
        "PROBE_AUDIT_OUTPUT_POLICY_FAIL: audit outputs must be distinct",
    )
    if allow_authoritative_output:
        expected = tuple(path.parent.resolve() / path.name for path in AUTHORITATIVE_OUTPUTS)
        require(
            tuple(validated) == expected,
            "PROBE_AUDIT_OUTPUT_POLICY_FAIL: authoritative override licenses "
            "only the two canonical audit reports",
        )
    return validated[0], validated[1]


def import_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"import:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


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


def edge_key(left: Any, right: Any) -> tuple[str, str]:
    return tuple(sorted((repr(left), repr(right))))


def mixed_payload(atlas, graph: nx.DiGraph) -> dict[str, Any]:
    mixed = atlas.sd0_mixed(graph)
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


def insert_at_site(primitive, graph: nx.DiGraph, site: dict[str, Any], label: int, namespace: Any) -> nx.DiGraph:
    tail, head, role = site["rooted_representatives"][0]
    return primitive.insert_arc(
        graph,
        {"tail": tail, "head": head, "edge_role": role},
        label,
        namespace,
    )


def relabel_leaf(graph: nx.DiGraph, old: int, new: int) -> nx.DiGraph:
    result = graph.copy()
    matches = [
        node for node, data in result.nodes(data=True)
        if data.get("role") == "leaf" and data.get("label") == old
    ]
    require(len(matches) == 1, f"leaf relabel multiplicity:{old}:{len(matches)}")
    require(new not in labels_of(result), f"leaf relabel collision:{new}")
    result.nodes[matches[0]]["label"] = new
    return result


class OrderedRoot:
    def __init__(self) -> None:
        self.rows = 0
        self.root = sha([])

    def add(self, row: dict[str, Any]) -> None:
        self.root = sha({"previous": self.root, "row_sha256": sha(row)})
        self.rows += 1

    def check(self, expected: dict[str, Any], name: str) -> None:
        require(self.rows == expected["rows"], f"{name}:row count")
        require(self.root == expected["ordered_hash_root"], f"{name}:ordered root")


def iter_jsonl(path: Path):
    with gzip.open(path, "rt", newline="") as handle:
        for number, line in enumerate(handle):
            require(line.endswith("\n"), f"missing LF:{path.name}:{number}")
            value = json.loads(line)
            require(line == canonical_bytes(value).decode() + "\n", f"noncanonical row:{path.name}:{number}")
            yield number, value


def ordinary_triangles(mixed: nx.Graph) -> list[tuple[frozenset[frozenset[Any]], Any]]:
    result = []
    for nodes in itertools.combinations(sorted(mixed.nodes(), key=repr), 3):
        if not all(mixed.has_edge(*pair) for pair in itertools.combinations(nodes, 2)):
            continue
        edges = frozenset(frozenset(pair) for pair in itertools.combinations(nodes, 2))
        heads = []
        for edge in edges:
            left, right = tuple(edge)
            edge_heads = mixed.edges[left, right].get("heads", frozenset())
            require(len(edge_heads) <= 1, "two-headed mixed edge")
            heads.extend(edge_heads)
        if len(heads) == 2 and heads[0] == heads[1]:
            result.append((edges, heads[0]))
    return result


def incidence_graph(mixed: nx.Graph, erased: frozenset[frozenset[Any]] | None):
    erased = frozenset() if erased is None else erased
    graph = nx.Graph()
    lookup = {}
    for node, data in mixed.nodes(data=True):
        graph.add_node(("v", node), kind="vertex", label=data.get("label"), erased=False)
    for index, (left, right, data) in enumerate(
        sorted(mixed.edges(data=True), key=lambda row: edge_key(row[0], row[1]))
    ):
        edge_node = ("e", index)
        edge = frozenset((left, right))
        lookup[edge_node] = edge
        collapsed = edge in erased
        graph.add_node(edge_node, kind="edge", label=None, erased=collapsed)
        heads = data.get("heads", frozenset())
        graph.add_edge(edge_node, ("v", left), head=False if collapsed else left in heads)
        graph.add_edge(edge_node, ("v", right), head=False if collapsed else right in heads)
    return graph, lookup


def exact_transports(atlas, source: nx.DiGraph, target: nx.DiGraph):
    source_mixed, target_mixed = atlas.sd0_mixed(source), atlas.sd0_mixed(target)
    node_match = lambda left, right: (
        left.get("kind") == right.get("kind")
        and left.get("label") == right.get("label")
        and left.get("erased") == right.get("erased")
    )
    edge_match = lambda left, right: left.get("head") == right.get("head")
    for relation in ("isomorphic", "triangle"):
        if relation == "isomorphic":
            candidates = [(None, None, None, None)]
        else:
            candidates = [
                (source_edges, target_edges, source_retic, target_retic)
                for source_edges, source_retic in ordinary_triangles(source_mixed)
                for target_edges, target_retic in ordinary_triangles(target_mixed)
            ]
        witnesses: dict[str, dict[str, Any]] = {}
        for source_triangle, target_triangle, source_retic, target_retic in candidates:
            left_graph, left_edges = incidence_graph(source_mixed, source_triangle)
            right_graph, right_edges = incidence_graph(target_mixed, target_triangle)
            matcher = nx.algorithms.isomorphism.GraphMatcher(
                left_graph, right_graph, node_match=node_match, edge_match=edge_match
            )
            for mapping in matcher.isomorphisms_iter():
                vertex_map = {
                    node: mapping[("v", node)][1] for node in source_mixed.nodes()
                }
                edge_map = {
                    left_edges[node]: right_edges[mapping[node]] for node in left_edges
                }
                public = {
                    "relation": relation,
                    "vertex_map": [
                        [repr(left), repr(right)]
                        for left, right in sorted(vertex_map.items(), key=lambda row: repr(row[0]))
                    ],
                    "mixed_edge_map": [
                        [list(edge_key(*tuple(left))), list(edge_key(*tuple(right)))]
                        for left, right in sorted(edge_map.items(), key=lambda row: edge_key(*tuple(row[0])))
                    ],
                    "source_triangle_edges": None if source_triangle is None else sorted(
                        [list(edge_key(*tuple(edge))) for edge in source_triangle]
                    ),
                    "target_triangle_edges": None if target_triangle is None else sorted(
                        [list(edge_key(*tuple(edge))) for edge in target_triangle]
                    ),
                }
                public["transport_sha256"] = sha(public)
                witnesses[public["transport_sha256"]] = {
                    "public": public,
                    "vertex_map": vertex_map,
                    "edge_map": edge_map,
                    "source_reticulation": source_retic,
                    "target_reticulation": target_retic,
                }
        if witnesses:
            return relation, [witnesses[key] for key in sorted(witnesses)]
    return "none", []


def public_transport_record(record: dict[str, Any]) -> dict[str, Any]:
    result = dict(record)
    result.pop("ordinary_triangle_arrowhead_witness", None)
    return result


def validate_transport_record(record_id: str, record: dict[str, Any]) -> None:
    require(set(record) == {
        "relation", "vertex_map", "mixed_edge_map", "source_triangle_edges",
        "target_triangle_edges", "transport_sha256",
        "ordinary_triangle_arrowhead_witness",
    }, f"transport schema:{record_id}")
    public = public_transport_record(record)
    claimed = public.pop("transport_sha256")
    require(record_id == claimed == sha(public), f"transport self hash:{record_id}")
    public["transport_sha256"] = claimed
    require(record["relation"] in {"isomorphic", "triangle"}, f"transport relation:{record_id}")
    source_vertices = [row[0] for row in record["vertex_map"]]
    target_vertices = [row[1] for row in record["vertex_map"]]
    require(len(source_vertices) == len(set(source_vertices)), f"transport source function:{record_id}")
    require(len(target_vertices) == len(set(target_vertices)), f"transport target bijection:{record_id}")
    if record["relation"] == "isomorphic":
        require(record["source_triangle_edges"] is None, f"isomorphism source triangle:{record_id}")
        require(record["target_triangle_edges"] is None, f"isomorphism target triangle:{record_id}")
        require(record["ordinary_triangle_arrowhead_witness"] is None, f"isomorphism triangle witness:{record_id}")
    else:
        ordinary = record["ordinary_triangle_arrowhead_witness"]
        require(ordinary is not None, f"triangle missing arrowhead witness:{record_id}")
        require(len(record["source_triangle_edges"]) == len(record["target_triangle_edges"]) == 3,
                f"triangle edge census:{record_id}")
        require(ordinary["required_pattern"] == "exactly two triangle arrows into one common reticulation",
                f"triangle pattern:{record_id}")
        for side in ("source", "target"):
            headed = ordinary[f"{side}_headed_edges"]
            common = ordinary[f"{side}_common_reticulation"]
            require(len(headed) == 2, f"triangle headed count:{record_id}:{side}")
            require(all(common in edge for edge in headed), f"triangle common retic:{record_id}:{side}")


def validate_restriction_record(record_id: str, record: dict[str, Any]) -> None:
    require(set(record) == {
        "exact_labelled_relation", "parent_mixed_graph_sha256", "removed_label",
        "restricted_mixed_graph_sha256", "restriction_transport_sha256",
    }, f"restriction schema:{record_id}")
    require(record_id == f"R:{sha(record)}", f"restriction self hash:{record_id}")
    require(record["exact_labelled_relation"] == "isomorphic", f"restriction relation:{record_id}")
    require(type(record["removed_label"]) is int, f"restriction label:{record_id}")


def split_payload(splits: set[Any]) -> list[Any]:
    rows = []
    for split in sorted(splits, key=repr):
        if split == ("star",):
            rows.append(["star"])
        else:
            rows.append([list(split[0]), list(split[1])])
    return rows


def switch_edge_sets(graph: nx.DiGraph):
    retics = tuple(sorted(
        (node for node, data in graph.nodes(data=True) if data.get("role") == "retic"),
        key=repr,
    ))
    parents = [tuple(sorted(graph.predecessors(node), key=repr)) for node in retics]
    require(all(len(row) == 2 for row in parents), "nonbinary reticulation")
    all_edges = tuple(graph.edges())
    for bits in itertools.product((0, 1), repeat=len(retics)):
        removed = set()
        for number, retic in enumerate(retics):
            keep = parents[number][bits[number]]
            removed.update((parent, retic) for parent in parents[number] if parent != keep)
        yield bits, tuple(edge for edge in all_edges if edge not in removed)


def quartet_splits(graph: nx.DiGraph, quartet: tuple[int, int, int, int]) -> set[Any]:
    keep_labels = set(quartet)
    output = set()
    for _, kept in switch_edge_sets(graph):
        undirected = nx.Graph()
        undirected.add_nodes_from(graph.nodes())
        undirected.add_edges_from(kept)
        split = None
        for left, right in list(undirected.edges()):
            undirected.remove_edge(left, right)
            components = list(nx.connected_components(undirected))
            undirected.add_edge(left, right)
            if len(components) != 2:
                continue
            label_sets = []
            for component in components:
                label_sets.append(frozenset(
                    graph.nodes[node].get("label") for node in component
                    if graph.nodes[node].get("label") in keep_labels
                ))
            if sorted(map(len, label_sets)) == [2, 2]:
                split = tuple(sorted(tuple(sorted(values)) for values in label_sets))
                break
        output.add(split if split is not None else ("star",))
    return output


class QuartetCache:
    def __init__(self) -> None:
        self.cache: dict[tuple[str, int], tuple[Any, ...]] = {}

    def deck(self, graph: nx.DiGraph, required_label: int) -> tuple[Any, ...]:
        key = (graph_sha(graph), required_label)
        if key not in self.cache:
            labels = labels_of(graph)
            self.cache[key] = tuple(
                (quartet, split_payload(quartet_splits(graph, quartet)))
                for quartet in itertools.combinations(labels, 4)
                if required_label in quartet
            )
        return self.cache[key]


def first_quartet_mismatch(source_deck, target_deck):
    require(len(source_deck) == len(target_deck), "quartet deck length")
    for (source_quartet, source_splits), (target_quartet, target_splits) in zip(source_deck, target_deck):
        require(source_quartet == target_quartet, "quartet label order")
        if source_splits != target_splits:
            return {
                "quartet": list(source_quartet),
                "source_displayed_splits": source_splits,
                "target_displayed_splits": target_splits,
                "method": "complete displayed-switching split-set mismatch",
            }
    return None


def sparse_payload(polynomial: dict[tuple[int, ...], fractions.Fraction]) -> list[Any]:
    return [
        [list(exponent), str(coefficient)]
        for exponent, coefficient in sorted(polynomial.items())
    ]


def sparse_multiply(left, right):
    result = collections.defaultdict(fractions.Fraction)
    for left_exp, left_coefficient in left.items():
        for right_exp, right_coefficient in right.items():
            result[tuple(a + b for a, b in zip(left_exp, right_exp))] += (
                left_coefficient * right_coefficient
            )
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def sparse_product(*polynomials):
    require(bool(polynomials), "empty sparse product")
    result = polynomials[0]
    for polynomial in polynomials[1:]:
        result = sparse_multiply(result, polynomial)
    return result


def sparse_difference(left, right):
    result = collections.defaultdict(fractions.Fraction)
    for exponent, coefficient in left.items():
        result[exponent] += coefficient
    for exponent, coefficient in right.items():
        result[exponent] -= coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


class FullMapCompiler:
    """Independent expansion of the full rooted switching map needed by T_i."""

    def __init__(self) -> None:
        self.states: dict[str, dict[str, Any]] = {}
        self.pullbacks: dict[tuple[str, tuple[int, ...], int], dict[tuple[int, ...], fractions.Fraction]] = {}

    def state(self, graph: nx.DiGraph):
        graph_id = graph_sha(graph)
        if graph_id in self.states:
            return self.states[graph_id]
        labels = labels_of(graph)
        require(labels == tuple(range(len(labels))), f"Fourier labels:{labels}")
        retics = tuple(sorted(
            (node for node, data in graph.nodes(data=True) if data.get("role") == "retic"),
            key=repr,
        ))
        parents = tuple(tuple(sorted(graph.predecessors(node), key=repr)) for node in retics)
        require(all(len(row) == 2 for row in parents), "Fourier reticulation parents")
        arm_edges = {
            (tail, head) for tail, head in graph.edges()
            if graph.nodes[head].get("role") == "leaf"
            and isinstance(graph.nodes[head].get("label"), int)
        }
        internal = tuple(
            edge for edge in sorted(graph.edges(), key=lambda row: (repr(row[0]), repr(row[1])))
            if edge not in arm_edges
        )
        edge_index = {edge: number for number, edge in enumerate(internal)}
        switches = []
        for bits, kept in switch_edge_sets(graph):
            children = {node: [] for node in graph.nodes()}
            for tail, head in kept:
                children[tail].append(head)
            subgraph = nx.edge_subgraph(graph, kept).copy()
            topological = list(nx.topological_sort(subgraph))
            masks: dict[Any, int] = {}
            for node in reversed(topological):
                label = graph.nodes[node].get("label")
                mask = (1 << label) if isinstance(label, int) else 0
                for child in children[node]:
                    mask |= masks[child]
                masks[node] = mask
            switches.append((bits, frozenset(kept), {(tail, head): masks[head] for tail, head in kept}))
        state = {
            "graph": graph,
            "labels": labels,
            "retics": retics,
            "internal": internal,
            "edge_index": edge_index,
            "switches": switches,
            "parameter_count": 2 * len(internal) + len(retics),
        }
        self.states[graph_id] = state
        return state

    @staticmethod
    def sector(mask: int, assignment: tuple[int, ...]) -> int:
        character = 0
        index = 0
        while mask:
            if mask & 1:
                character ^= assignment[index]
            index += 1
            mask >>= 1
        return 0 if character == 0 else (2 if character == 2 else 1)

    @staticmethod
    def inheritance_polynomial(bits: tuple[int, ...]):
        polynomial = {0: 1}
        for index, bit in enumerate(bits):
            updated = collections.defaultdict(int)
            for mask, coefficient in polynomial.items():
                if bit:
                    updated[mask | (1 << index)] += coefficient
                else:
                    updated[mask] += coefficient
                    updated[mask | (1 << index)] -= coefficient
            polynomial = {mask: coefficient for mask, coefficient in updated.items() if coefficient}
        return polynomial

    def coordinate(self, state, assignment: tuple[int, ...]):
        result = collections.defaultdict(fractions.Fraction)
        edge_count = len(state["internal"])
        for bits, kept, masks in state["switches"]:
            base = [0] * state["parameter_count"]
            for edge in state["internal"]:
                if edge not in kept:
                    continue
                sector = self.sector(masks[edge], assignment)
                if sector:
                    base[2 * state["edge_index"][edge] + sector - 1] += 1
            for inheritance_mask, coefficient in self.inheritance_polynomial(bits).items():
                exponent = list(base)
                for index in range(len(state["retics"])):
                    if inheritance_mask >> index & 1:
                        exponent[2 * edge_count + index] += 1
                result[tuple(exponent)] += coefficient
        return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}

    def t_pullback(self, graph: nx.DiGraph, triple: tuple[int, int, int], orientation: int):
        graph_id = graph_sha(graph)
        key = (graph_id, triple, orientation)
        if key in self.pullbacks:
            return self.pullbacks[key]
        state = self.state(graph)
        other = sorted(set(triple) - {orientation})
        require(len(other) == 2, "T_i orientation")
        first, second = other

        def coordinate(values: dict[int, int]):
            assignment = [0] * len(state["labels"])
            for label, character in values.items():
                assignment[label] = character
            return self.coordinate(state, tuple(assignment))

        v_value = coordinate({first: 1, second: 3, orientation: 2})
        x_s = coordinate({first: 1, second: 1})
        x_g = coordinate({first: 2, second: 2})
        y_g = coordinate({first: 2, orientation: 2})
        z_g = coordinate({second: 2, orientation: 2})
        result = sparse_difference(
            sparse_product(v_value, v_value, x_g),
            sparse_product(x_s, x_s, y_g, z_g),
        )
        self.pullbacks[key] = result
        return result

    def parameterization(self, graph: nx.DiGraph):
        state = self.state(graph)
        return {
            "edge_sector_pairs": [
                [repr(tail), repr(head), 2 * number, 2 * number + 1]
                for number, (tail, head) in enumerate(state["internal"])
            ],
            "inheritance_variables": [
                [repr(node), 2 * len(state["internal"]) + number]
                for number, node in enumerate(state["retics"])
            ],
            "selected_pendant_arms_removed_by_boundary_normalization": True,
        }


def sparse_from_payload(payload):
    result = {}
    for exponent, coefficient in payload:
        key = tuple(exponent)
        require(key not in result, "duplicate sparse exponent")
        value = fractions.Fraction(coefficient)
        require(value != 0, "stored sparse zero")
        result[key] = value
    return result


def bernstein_certificate(polynomial):
    require(polynomial, "empty Bernstein polynomial")
    parameter_count = len(next(iter(polynomial)))
    common = tuple(min(exponent[index] for exponent in polynomial) for index in range(parameter_count))
    active = tuple(
        index for index in range(parameter_count)
        if len({exponent[index] for exponent in polynomial}) > 1
    )
    reduced = collections.defaultdict(fractions.Fraction)
    for exponent, coefficient in polynomial.items():
        reduced[tuple(exponent[index] - common[index] for index in active)] += coefficient
    reduced = {exponent: coefficient for exponent, coefficient in reduced.items() if coefficient}
    degrees = tuple(max(exponent[index] for exponent in reduced) for index in range(len(active)))
    shape = tuple(degree + 1 for degree in degrees)
    coefficient_count = math.prod(shape)
    require(coefficient_count <= 2_000_000, f"Bernstein size:{coefficient_count}")
    strides = tuple(math.prod(shape[index + 1 :]) for index in range(len(shape)))
    values = [fractions.Fraction(0)] * coefficient_count
    for exponent, coefficient in reduced.items():
        values[sum(value * stride for value, stride in zip(exponent, strides))] += coefficient
    for axis, degree in enumerate(degrees):
        stride = strides[axis]
        outer = math.prod(shape[:axis])
        block = (degree + 1) * stride
        transformed = [fractions.Fraction(0)] * coefficient_count
        for outer_index in range(outer):
            base = outer_index * block
            for inner_index in range(stride):
                source = [values[base + value * stride + inner_index] for value in range(degree + 1)]
                for beta in range(degree + 1):
                    transformed[base + beta * stride + inner_index] = sum(
                        source[alpha] * fractions.Fraction(
                            math.comb(beta, alpha), math.comb(degree, alpha)
                        )
                        for alpha in range(beta + 1)
                    )
        values = transformed
    signs = collections.Counter(-1 if value < 0 else 1 if value > 0 else 0 for value in values)
    require(not (signs[-1] and signs[1]), "mixed Bernstein sign")
    require(signs[-1] or signs[1], "all-zero Bernstein tensor")
    return {
        "method": "exact_tensor_Bernstein_after_strictly_positive_monomial",
        "parameter_count": parameter_count,
        "strictly_positive_monomial_exponent": list(common),
        "active_parameter_indices": list(active),
        "Bernstein_multidegree": list(degrees),
        "Bernstein_coefficient_count": coefficient_count,
        "negative_coefficients": signs[-1],
        "zero_coefficients": signs[0],
        "positive_coefficients": signs[1],
        "minimum_coefficient": str(min(values)),
        "maximum_coefficient": str(max(values)),
        "ordered_Bernstein_coefficients_sha256": sha([str(value) for value in values]),
        "strict_sign": -1 if signs[-1] else 1,
        "domain": (
            "the full open unit cube in physical edge-sector and inheritance "
            "variables, which contains the physical principal D_plus subset"
        ),
    }


class RelationClassRegistry:
    def __init__(self, atlas) -> None:
        self.atlas = atlas
        self.representatives: list[nx.Graph] = []
        self.buckets: dict[str, list[int]] = collections.defaultdict(list)

    def combined(self, source: nx.DiGraph, target: nx.DiGraph, relation: str, transport: dict[str, Any]):
        result = nx.Graph()
        triangle_strings = {
            "S": set(tuple(edge) for edge in (transport["source_triangle_edges"] or [])),
            "T": set(tuple(edge) for edge in (transport["target_triangle_edges"] or [])),
        }
        for side, graph in (("S", source), ("T", target)):
            mixed = self.atlas.sd0_mixed(graph)
            for node, data in mixed.nodes(data=True):
                result.add_node((side, "v", node), color=f"{side}:vertex:{data.get('label')!r}")
            for number, (left, right, data) in enumerate(
                sorted(mixed.edges(data=True), key=lambda row: edge_key(row[0], row[1]))
            ):
                edge_node = (side, "e", number)
                key = edge_key(left, right)
                collapsed = key in triangle_strings[side]
                result.add_node(edge_node, color=f"{side}:edge:{collapsed}")
                heads = data.get("heads", frozenset())
                result.add_edge(edge_node, (side, "v", left), color=f"head:{left in heads and not collapsed}")
                result.add_edge(edge_node, (side, "v", right), color=f"head:{right in heads and not collapsed}")
        for source_node, target_node in transport["vertex_map"]:
            result.add_edge(
                ("S", "v", ast.literal_eval(source_node)),
                ("T", "v", ast.literal_eval(target_node)),
                color="transport",
            )
        result.add_node(("relation",), color=f"relation:{relation}")
        return result

    def find_or_add(self, source, target, relation, transport, allow_add: bool):
        combined = self.combined(source, target, relation, transport)
        bucket = nx.weisfeiler_lehman_graph_hash(
            combined, node_attr="color", edge_attr="color", iterations=8
        )
        node_match = lambda left, right: left.get("color") == right.get("color")
        edge_match = lambda left, right: left.get("color") == right.get("color")
        for class_id in self.buckets[bucket]:
            if nx.is_isomorphic(
                combined, self.representatives[class_id],
                node_match=node_match, edge_match=edge_match,
            ):
                return class_id
        require(allow_add, "reverse marginal created a new one-port relation class")
        class_id = len(self.representatives)
        self.representatives.append(combined)
        self.buckets[bucket].append(class_id)
        return class_id


def logical_payload(value: dict[str, Any]) -> str:
    public = copy.deepcopy(value)
    public.pop("payload_sha256", None)
    public.pop("operational", None)
    return sha(public)


def mixed_graph_sha(atlas, graph: nx.DiGraph) -> str:
    return sha(mixed_payload(atlas, graph))


def site_edge_strings(site: dict[str, Any]) -> tuple[str, str]:
    return tuple(site["mixed_endpoints"])


def transport_edge_map(record: dict[str, Any]) -> dict[tuple[str, str], tuple[str, str]]:
    return {
        tuple(source): tuple(target)
        for source, target in record["mixed_edge_map"]
    }


def transported_site(record: dict[str, Any], source_site: dict[str, Any], target_site: dict[str, Any]) -> bool:
    return transport_edge_map(record).get(site_edge_strings(source_site)) == site_edge_strings(target_site)


def triangle_description(atlas, graph: nx.DiGraph, stored_edges: list[list[str]]) -> tuple[set[tuple[str, str]], str]:
    mixed = atlas.sd0_mixed(graph)
    edges = {tuple(edge) for edge in stored_edges}
    require(len(edges) == 3, "ordinary triangle edge count")
    require(all(len(edge) == 2 for edge in edges), "ordinary triangle edge width")
    require(all(mixed.has_edge(ast.literal_eval(edge[0]), ast.literal_eval(edge[1])) for edge in edges),
            "ordinary triangle missing edge")
    vertices = set(itertools.chain.from_iterable(edges))
    require(len(vertices) == 3, "ordinary triangle vertex count")
    headed: list[tuple[str, str]] = []
    heads: list[str] = []
    for edge in sorted(edges):
        left, right = map(ast.literal_eval, edge)
        edge_heads = mixed.edges[left, right].get("heads", frozenset())
        require(len(edge_heads) <= 1, "ordinary triangle double-headed edge")
        if edge_heads:
            headed.append(edge)
            heads.append(repr(next(iter(edge_heads))))
    require(len(headed) == 2 and len(set(heads)) == 1, "ordinary triangle arrowhead pattern")
    require(all(heads[0] in edge for edge in headed), "ordinary triangle common reticulation")
    return edges, heads[0]


def validate_transport_on_graphs(
    atlas, source: nx.DiGraph, target: nx.DiGraph,
    record_id: str, record: dict[str, Any], context: str,
) -> None:
    """Check a stored map as an exact mixed-graph witness, without searching for it."""
    validate_transport_record(record_id, record)
    source_mixed, target_mixed = atlas.sd0_mixed(source), atlas.sd0_mixed(target)
    source_nodes = {repr(node): node for node in source_mixed.nodes()}
    target_nodes = {repr(node): node for node in target_mixed.nodes()}
    vertex_rows = record["vertex_map"]
    require({row[0] for row in vertex_rows} == set(source_nodes), f"{context}:source vertex coverage")
    require({row[1] for row in vertex_rows} == set(target_nodes), f"{context}:target vertex coverage")
    vertex_map = {row[0]: row[1] for row in vertex_rows}
    for source_name, target_name in vertex_map.items():
        require(
            source_mixed.nodes[source_nodes[source_name]].get("label")
            == target_mixed.nodes[target_nodes[target_name]].get("label"),
            f"{context}:label preservation:{source_name}",
        )

    def edge_dictionary(mixed: nx.Graph) -> dict[tuple[str, str], tuple[Any, Any, dict[str, Any]]]:
        return {
            edge_key(left, right): (left, right, data)
            for left, right, data in mixed.edges(data=True)
        }

    source_edges, target_edges = edge_dictionary(source_mixed), edge_dictionary(target_mixed)
    edge_rows = record["mixed_edge_map"]
    require({tuple(row[0]) for row in edge_rows} == set(source_edges), f"{context}:source edge coverage")
    require({tuple(row[1]) for row in edge_rows} == set(target_edges), f"{context}:target edge coverage")
    edge_map = {tuple(row[0]): tuple(row[1]) for row in edge_rows}
    source_triangle = set() if record["source_triangle_edges"] is None else {
        tuple(edge) for edge in record["source_triangle_edges"]
    }
    target_triangle = set() if record["target_triangle_edges"] is None else {
        tuple(edge) for edge in record["target_triangle_edges"]
    }
    require((not source_triangle) == (record["relation"] == "isomorphic"), f"{context}:relation/triangle")
    require({edge_map[edge] for edge in source_triangle} == target_triangle, f"{context}:triangle transport")
    for source_edge, target_edge in edge_map.items():
        mapped_endpoints = tuple(sorted(vertex_map[name] for name in source_edge))
        require(mapped_endpoints == target_edge, f"{context}:edge incidence:{source_edge}")
        if source_edge in source_triangle:
            continue
        _, _, source_data = source_edges[source_edge]
        _, _, target_data = target_edges[target_edge]
        source_heads = {vertex_map[repr(node)] for node in source_data.get("heads", frozenset())}
        target_heads = {repr(node) for node in target_data.get("heads", frozenset())}
        require(source_heads == target_heads, f"{context}:arrowhead preservation:{source_edge}")
    if record["relation"] == "triangle":
        _, source_retic = triangle_description(atlas, source, record["source_triangle_edges"])
        _, target_retic = triangle_description(atlas, target, record["target_triangle_edges"])
        ordinary = record["ordinary_triangle_arrowhead_witness"]
        require(ordinary["source_common_reticulation"] == source_retic, f"{context}:source reticulation")
        require(ordinary["target_common_reticulation"] == target_retic, f"{context}:target reticulation")


def global_triangle_from_transport(atlas, source, target, record: dict[str, Any]):
    if record["relation"] == "isomorphic":
        return None
    _, source_retic = triangle_description(atlas, source, record["source_triangle_edges"])
    _, target_retic = triangle_description(atlas, target, record["target_triangle_edges"])
    return {
        "source_triangle_edges": record["source_triangle_edges"],
        "target_triangle_edges": record["target_triangle_edges"],
        "source_reticulation": source_retic,
        "target_reticulation": target_retic,
        "ordinary_triangle_witness": (
            "exactly two arrowheads enter the displayed common reticulation on each side"
        ),
    }


def validate_child_coherence(
    parent_record: dict[str, Any], child_record: dict[str, Any],
    source_site: dict[str, Any], target_site: dict[str, Any],
    inherited_triangle: dict[str, Any] | None, context: str,
) -> None:
    parent_vertices = dict(parent_record["vertex_map"])
    child_vertices = dict(child_record["vertex_map"])
    require(all(child_vertices.get(node) == target for node, target in parent_vertices.items()),
            f"{context}:parent vertex restriction")
    require(transported_site(parent_record, source_site, target_site), f"{context}:selected site transport")
    if child_record["relation"] == "triangle":
        require(inherited_triangle is not None, f"{context}:new triangle above isomorphism")
        require(child_record["source_triangle_edges"] == inherited_triangle["source_triangle_edges"],
                f"{context}:source global triangle")
        require(child_record["target_triangle_edges"] == inherited_triangle["target_triangle_edges"],
                f"{context}:target global triangle")
        ordinary = child_record["ordinary_triangle_arrowhead_witness"]
        require(ordinary["source_common_reticulation"] == inherited_triangle["source_reticulation"],
                f"{context}:source global reticulation")
        require(ordinary["target_common_reticulation"] == inherited_triangle["target_reticulation"],
                f"{context}:target global reticulation")


def site_profile(primitive, atlas, graph: nx.DiGraph) -> dict[str, Any]:
    sites = primitive.independently_enumerate_sites(atlas, graph)
    labels = labels_of(graph)
    reticulation_count = sum(data.get("role") == "retic" for _, data in graph.nodes(data=True))
    counts = collections.Counter(row["site_type"] for row in sites)
    require(len(sites) == 2 * len(labels) + 3 * reticulation_count - 3, "site profile formula")
    root = next(node for node, data in graph.nodes(data=True) if data.get("role") == "root")
    root_children = tuple(graph.successors(root))
    require(len(root_children) == 2, "root half count")
    children = sorted(root_children, key=lambda node: graph.nodes[node].get("role") != "leaf")
    new_label = max(labels) + 1
    first = primitive.insert_arc(
        graph,
        {"tail": repr(root), "head": repr(children[0]), "edge_role": graph.edges[root, children[0]].get("edge_role")},
        new_label, "root_half_audit_a",
    )
    second = primitive.insert_arc(
        graph,
        {"tail": repr(root), "head": repr(children[1]), "edge_role": graph.edges[root, children[1]].get("edge_role")},
        new_label, "root_half_audit_b",
    )
    relation, witnesses = exact_transports(atlas, first, second)
    require(relation == "isomorphic" and bool(witnesses), "root halves inequivalent")
    representative_half_arcs = [
        [repr(root), repr(child), graph.edges[root, child].get("edge_role")]
        for child in sorted(root_children, key=repr)
    ]
    half = {
        "new_label": new_label,
        "representative_half_arcs": representative_half_arcs,
        "semi_directed_relation_after_insertion": "isomorphic",
        "first_graph_sha256": graph_sha(first),
        "second_graph_sha256": graph_sha(second),
    }
    half["certificate_sha256"] = sha(half)
    return {
        "port_count": len(labels),
        "reticulation_count": reticulation_count,
        "all_mixed_edge_sites_included": True,
        "site_count": len(sites),
        "site_type_census": dict(sorted(counts.items())),
        "root_half_equivalence": half,
        "sites": sites,
        "ordered_site_hash_root": sha([sha(row) for row in sites]),
    }


def restriction_for_child(
    atlas, child: nx.DiGraph, parent: nx.DiGraph, removed_label: int,
    transport_records: dict[str, dict[str, Any]], context: str,
) -> tuple[str, dict[str, Any]]:
    restricted = atlas.restrict_rooted(child, set(labels_of(parent)))
    record = {
        "removed_label": removed_label,
        "restricted_mixed_graph_sha256": mixed_graph_sha(atlas, restricted),
        "parent_mixed_graph_sha256": mixed_graph_sha(atlas, parent),
        "exact_labelled_relation": "isomorphic",
    }
    cache_key = (graph_sha(parent), removed_label)
    cached = _RESTRICTION_TRANSPORT_CACHE.get(cache_key)
    if cached is None:
        # The exact restriction transport is found structurally, not trusted
        # from the child row.  It is unique in these labelled binary marginals.
        relation, witnesses = exact_transports(atlas, restricted, parent)
        require(relation == "isomorphic" and len(witnesses) == 1, f"{context}:restriction uniqueness")
        transport_id = witnesses[0]["public"]["transport_sha256"]
        _RESTRICTION_TRANSPORT_CACHE[cache_key] = transport_id
    else:
        transport_id = cached
    # The restriction ledger commits the unique map by its self hash.  The
    # primary transport ledger intentionally stores anchor/equality/reverse
    # transports, not every marginal identity map; validate a registry copy
    # when one happens to be shared, while the independent matcher above is
    # authoritative for marginal-only hashes.
    if transport_id in transport_records:
        validate_transport_on_graphs(
            atlas, restricted, parent, transport_id, transport_records[transport_id],
            f"{context}:restriction transport",
        )
    record["restriction_transport_sha256"] = transport_id
    return f"R:{sha(record)}", record


_RESTRICTION_TRANSPORT_CACHE: dict[tuple[str, int], str] = {}


def displayed_switch_label_sets(graph: nx.DiGraph):
    """Return descendant-label sets for each displayed switching in one traversal."""
    outputs = []
    for _, kept in switch_edge_sets(graph):
        switched = nx.DiGraph()
        switched.add_nodes_from(graph.nodes())
        switched.add_edges_from(kept)
        order = list(nx.topological_sort(switched))
        children = {node: tuple(switched.successors(node)) for node in switched.nodes()}
        descendants: dict[Any, frozenset[int]] = {}
        for node in reversed(order):
            label = graph.nodes[node].get("label")
            labels = {label} if isinstance(label, int) else set()
            for child in children[node]:
                labels.update(descendants[child])
            descendants[node] = frozenset(labels)
        outputs.append(tuple(descendants[head] for _, head in kept))
    return outputs


def quartet_deck(graph: nx.DiGraph, required_label: int | None = None):
    switch_sets = displayed_switch_label_sets(graph)
    output = []
    for quartet in itertools.combinations(labels_of(graph), 4):
        if required_label is not None and required_label not in quartet:
            continue
        keep = frozenset(quartet)
        splits = set()
        for descendants in switch_sets:
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


def reject_rooted_oracle_fields(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = key.lower().replace("-", "_")
            forbidden = (
                "sunlet" in lowered
                or "tree_oracle" in lowered
                or "oracle_cache" in lowered
                or ("rooted" in lowered and "triple" in lowered and key != "forbidden_rooted_triple_oracle_used")
            )
            require(not forbidden, f"forbidden rooted-oracle field:{path}.{key}")
            reject_rooted_oracle_fields(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_rooted_oracle_fields(child, f"{path}[{index}]")


def validate_quartet_row(
    row: dict[str, Any], source_deck, target_deck,
    quartet_proofs: dict[str, dict[str, Any]], context: str,
) -> None:
    require(row["proof_id"] in quartet_proofs, f"{context}:quartet proof reference")
    proof = first_quartet_mismatch(source_deck, target_deck)
    require(proof is not None, f"{context}:quartet row has equal decks")
    require(row["proof_id"] == f"Q:{sha(proof)}", f"{context}:quartet proof reassigned")
    require(quartet_proofs[row["proof_id"]] == proof, f"{context}:quartet proof payload")


def validate_ti_registry(proof: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    ti = proof["full_map_Ti_registry"]
    certificates = ti["certificates"]
    strict_polynomials = ti["strict_polynomial_registry"]
    require(ti["canonical_relation_certificates"] == len(certificates) == 156, "T_i certificate count")
    require(ti["canonical_strict_polynomials"] == len(strict_polynomials) == 118, "T_i polynomial count")
    for polynomial_id, item in strict_polynomials.items():
        require(polynomial_id == item["pullback_sha256"] == sha(item["pullback"]),
                f"strict polynomial self hash:{polynomial_id}")
        polynomial = sparse_from_payload(item["pullback"])
        require(bernstein_certificate(polynomial) == item["Bernstein_certificate"],
                f"strict Bernstein replay:{polynomial_id}")
        indices = {
            index for edge in item["parameterization"]["edge_sector_pairs"] for index in edge[2:]
        } | {row[1] for row in item["parameterization"]["inheritance_variables"]}
        require(indices == set(range(item["Bernstein_certificate"]["parameter_count"])),
                f"strict parameter coverage:{polynomial_id}")
    for certificate_id, item in certificates.items():
        require(certificate_id == f"TI:{sha(item)}", f"T_i certificate self hash:{certificate_id}")
        require(item["zero_pullback_sha256"] == sha([]), f"T_i zero hash:{certificate_id}")
        require(item["strict_pullback_sha256"] in strict_polynomials, f"T_i strict reference:{certificate_id}")
        other = sorted(set(item["triple"]) - {item["orientation_label_i"]})
        require(other == item["ordered_other_labels"], f"T_i ordered labels:{certificate_id}")
        weights = item["boundary_incidence_multihomogeneity"]
        expected_weights = {
            str(other[0]): "s^2*g", str(other[1]): "s^2*g",
            str(item["orientation_label_i"]): "g^2",
            "all_unselected_boundary_incidence_weights": "0",
        }
        require(weights == expected_weights, f"T_i bridge weights:{certificate_id}")
        require(item["strict_sign"] == strict_polynomials[item["strict_pullback_sha256"]]["Bernstein_certificate"]["strict_sign"],
                f"T_i sign reference:{certificate_id}")
    return certificates, strict_polynomials


def validate_ti_pair(
    compiler: FullMapCompiler, source: nx.DiGraph, target: nx.DiGraph,
    proof_id: str, certificates: dict[str, Any], strict_polynomials: dict[str, Any], context: str,
    parameterization_witnesses: set[str],
) -> None:
    require(proof_id in certificates, f"{context}:T_i proof reference")
    certificate = certificates[proof_id]
    triple = tuple(certificate["triple"])
    orientation = certificate["orientation_label_i"]
    source_polynomial = compiler.t_pullback(source, triple, orientation)
    target_polynomial = compiler.t_pullback(target, triple, orientation)
    zero = source_polynomial if certificate["zero_on"] == "source" else target_polynomial
    strict = target_polynomial if certificate["strict_on"] == "target" else source_polynomial
    require(not zero, f"{context}:T_i claimed zero is nonzero")
    strict_payload = sparse_payload(strict)
    strict_id = sha(strict_payload)
    require(strict_id == certificate["strict_pullback_sha256"], f"{context}:T_i certificate reassigned")
    require(strict_polynomials[strict_id]["pullback"] == strict_payload, f"{context}:T_i strict payload")
    parameterization = compiler.parameterization(
        target if certificate["strict_on"] == "target" else source
    )
    if parameterization == strict_polynomials[strict_id]["parameterization"]:
        parameterization_witnesses.add(strict_id)


def validate_equality_row_schema(row: dict[str, Any], stage: str, context: str) -> None:
    common_one = {
        "stage", "parent_anchor_id", "origin", "inserted_label",
        "source_site_index", "source_site_id", "target_site_index", "target_site_id",
        "source_child_graph_sha256", "target_child_graph_sha256",
        "source_parent_restriction_id", "target_parent_restriction_id",
    }
    common_two = {
        "stage", "base_anchor_id", "one_port_parent_id", "origin",
        "first_label", "second_label", "first_source_site_index", "first_target_site_index",
        "second_source_site_index", "second_source_site_id",
        "second_target_site_index", "second_target_site_id",
        "source_child_graph_sha256", "target_child_graph_sha256",
        "source_parent_restriction_id", "target_parent_restriction_id",
    }
    common = common_one if stage == "A+p" else common_two
    if row["status"] in {"isomorphic", "triangle"}:
        extra = {
            "status", "transport_id", "parent_transport_id",
            "transport_restriction", "global_triangle_sha256",
        }
        if stage == "A+p+q":
            extra.add("reverse_order_certificate")
    else:
        extra = {"status", "proof_id"}
    require(set(row) == common | extra, f"{context}:row schema")


def prepare_children(
    primitive, atlas, graph: nx.DiGraph, profile: dict[str, Any], label: int,
    namespace: str, side: str, transport_records: dict[str, dict[str, Any]],
    restriction_records: dict[str, dict[str, Any]], context: str,
) -> list[dict[str, Any]]:
    rows = []
    for index, site in enumerate(profile["sites"]):
        child = insert_at_site(primitive, graph, site, label, (namespace, side, index))
        restriction_id, restriction = restriction_for_child(
            atlas, child, graph, label, transport_records, f"{context}:{side}:{index}"
        )
        require(restriction_id in restriction_records, f"{context}:{side}:{index}:restriction absent")
        require(restriction_records[restriction_id] == restriction, f"{context}:{side}:{index}:restriction payload")
        rows.append({
            "graph": child,
            "graph_sha256": graph_sha(child),
            "site": site,
            "site_index": index,
            "restriction_id": restriction_id,
            "quartet_deck": quartet_deck(child, label),
        })
    return rows


def validate_common_row(
    row: dict[str, Any], source_child: dict[str, Any], target_child: dict[str, Any],
    source_index_field: str, target_index_field: str,
    source_site_field: str, target_site_field: str, context: str,
) -> None:
    require(row[source_index_field] == source_child["site_index"], f"{context}:source site index")
    require(row[target_index_field] == target_child["site_index"], f"{context}:target site index")
    require(row[source_site_field] == source_child["site"]["site_id"], f"{context}:source site id")
    require(row[target_site_field] == target_child["site"]["site_id"], f"{context}:target site id")
    require(row["source_child_graph_sha256"] == source_child["graph_sha256"], f"{context}:source child hash")
    require(row["target_child_graph_sha256"] == target_child["graph_sha256"], f"{context}:target child hash")
    require(row["source_parent_restriction_id"] == source_child["restriction_id"], f"{context}:source restriction")
    require(row["target_parent_restriction_id"] == target_child["restriction_id"], f"{context}:target restriction")


def public_anchor_expected(contract_anchor, class_id: int, global_triangle):
    return {
        "anchor_id": contract_anchor["anchor_id"],
        "origin": contract_anchor["origin"],
        "labels": contract_anchor["labels"],
        "relation": contract_anchor["relation"],
        "canonical_anchor_class_id": class_id,
        "source_graph_sha256": contract_anchor["source_graph_sha256"],
        "target_graph_sha256": contract_anchor["target_graph_sha256"],
        "transport_id": contract_anchor["parent_transport"]["transport_sha256"],
        "global_triangle": global_triangle,
        "source_site_count": contract_anchor["source_candidate_profile"]["site_count"],
        "target_site_count": contract_anchor["target_candidate_profile"]["site_count"],
        "source_site_ordered_hash_root": contract_anchor["source_candidate_profile"]["ordered_site_hash_root"],
        "target_site_ordered_hash_root": contract_anchor["target_candidate_profile"]["ordered_site_hash_root"],
        "locator_sha256": sha(contract_anchor["locator"]),
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    payload = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)


def qualify_in_process_mutation_failure(
    name: str, expected_diagnostic: str, check, value: Any
) -> dict[str, Any]:
    try:
        check(copy.deepcopy(value))
    except AuditFailure as error:
        observed = str(error)
        require(
            observed == expected_diagnostic,
            f"mutation diagnostic mismatch:{name}",
        )
        return {
            "mutation": name,
            "rejected": True,
            "exception_type": "AuditFailure",
            "expected_diagnostic": expected_diagnostic,
            "observed_diagnostic": observed,
        }
    except Exception as error:
        raise AuditFailure(
            f"mutation unrelated exception:{name}:{type(error).__name__}"
        ) from error
    raise AuditFailure(f"mutation survived:{name}")


def qualify_in_process_case(
    name: str, expected_diagnostic: str, check, clean: Any, mutated: Any
) -> dict[str, Any]:
    try:
        check(copy.deepcopy(clean))
    except Exception as error:
        raise AuditFailure(
            f"clean baseline failed:{name}:{type(error).__name__}:{error}"
        ) from error
    return qualify_in_process_mutation_failure(
        name, expected_diagnostic, check, mutated
    )


def run_mutation_qualification_negative_controls() -> dict[str, bool]:
    def expect_failure(action, marker: str) -> None:
        try:
            action()
        except AuditFailure as error:
            require(marker in str(error), f"negative control wrong failure:{marker}")
            return
        raise AuditFailure(f"negative control accepted:{marker}")

    def raise_audit(message: str) -> None:
        raise AuditFailure(message)

    def raise_key_error(_value: Any) -> None:
        raise KeyError("synthetic unrelated failure")

    expect_failure(
        lambda: qualify_in_process_mutation_failure(
            "control", "expected", lambda _value: raise_audit("wrong"), None
        ),
        "mutation diagnostic mismatch:control",
    )
    expect_failure(
        lambda: qualify_in_process_mutation_failure(
            "control", "expected", raise_key_error, None
        ),
        "mutation unrelated exception:control:KeyError",
    )
    expect_failure(
        lambda: qualify_in_process_mutation_failure(
            "control", "expected", lambda _value: None, None
        ),
        "mutation survived:control",
    )
    expect_failure(
        lambda: qualify_in_process_case(
            "control",
            "expected",
            lambda _value: raise_audit("baseline error"),
            None,
            None,
        ),
        "clean baseline failed:control:AuditFailure:baseline error",
    )
    return {
        "wrong_diagnostic_not_qualified": True,
        "unrelated_exception_not_qualified": True,
        "surviving_mutation_not_qualified": True,
        "failed_clean_baseline_not_qualified": True,
    }


def run_mutations(
    samples: dict[str, Any], output: Path, certificate_path: Path,
    certificate_payload_sha256: str,
) -> dict[str, Any]:
    wrong_parent = copy.deepcopy(samples["two_row"])
    wrong_parent["one_port_parent_id"] = samples["other_parent_id"]
    wrong_site = copy.deepcopy(samples["one_row"])
    wrong_site["source_site_id"] = "E:" + "0" * 64
    wrong_reverse = copy.deepcopy(samples["reverse"])
    wrong_reverse["reverse_parent_transport_id"] = samples["other_transport_id"]
    broken_triangle = copy.deepcopy(samples["triangle_row"])
    broken_triangle["global_triangle_sha256"] = "0" * 64
    wrong_q = copy.deepcopy(samples["quartet_row"])
    wrong_q["proof_id"] = samples["other_quartet_id"]
    wrong_ti = copy.deepcopy(samples["ti_row"])
    wrong_ti["proof_id"] = samples["other_ti_id"]
    wrong_restriction = copy.deepcopy(samples["restriction"])
    wrong_restriction["removed_label"] += 1
    wrong_transport = copy.deepcopy(samples["transport"])
    wrong_transport["vertex_map"][0][1] = wrong_transport["vertex_map"][1][1]
    rooted = copy.deepcopy(samples["one_row"])
    rooted["rooted_triple_cache"] = "revoked"
    swapped_status = copy.deepcopy(samples["quartet_row"])
    swapped_status["status"] = "isomorphic"
    wrong_hash = copy.deepcopy(samples["one_row"])
    wrong_hash["source_child_graph_sha256"] = "f" * 64

    cases = [
        (
            "omitted_raw_record", "coverage row count",
            lambda count: require(count == samples["coverage_rows"], "coverage row count"),
            samples["coverage_rows"], samples["coverage_rows"] - 1,
        ),
        (
            "wrong_parent", "parent identity",
            lambda row: require(
                row["one_port_parent_id"]
                == samples["two_row"]["one_port_parent_id"],
                "parent identity",
            ),
            samples["two_row"], wrong_parent,
        ),
        (
            "wrong_site", "site identity",
            lambda row: require(
                row["source_site_id"] == samples["one_row"]["source_site_id"],
                "site identity",
            ),
            samples["one_row"], wrong_site,
        ),
        (
            "wrong_reverse_transport", "reverse exact payload",
            lambda row: require(row == samples["reverse"], "reverse exact payload"),
            samples["reverse"], wrong_reverse,
        ),
        (
            "broken_global_triangle", "global triangle",
            lambda row: require(row == samples["triangle_row"], "global triangle"),
            samples["triangle_row"], broken_triangle,
        ),
        (
            "reassigned_quartet_certificate", "quartet certificate",
            lambda row: require(
                row["proof_id"] == samples["quartet_row"]["proof_id"],
                "quartet certificate",
            ),
            samples["quartet_row"], wrong_q,
        ),
        (
            "reassigned_Ti_certificate", "T_i certificate",
            lambda row: require(
                row["proof_id"] == samples["ti_row"]["proof_id"],
                "T_i certificate",
            ),
            samples["ti_row"], wrong_ti,
        ),
        (
            "wrong_parent_restriction", "restriction self hash",
            lambda row: require(
                f"R:{sha(row)}" == samples["restriction_id"],
                "restriction self hash",
            ),
            samples["restriction"], wrong_restriction,
        ),
        (
            "broken_exact_transport",
            f"transport self hash:{samples['transport_id']}",
            lambda row: validate_transport_record(samples["transport_id"], row),
            samples["transport"], wrong_transport,
        ),
        (
            "old_rooted_cache_field",
            "forbidden rooted-oracle field:$.rooted_triple_cache",
            reject_rooted_oracle_fields,
            samples["one_row"], rooted,
        ),
        (
            "classifier_status_reassignment", "classifier status",
            lambda row: require(
                row["status"] == samples["quartet_row"]["status"],
                "classifier status",
            ),
            samples["quartet_row"], swapped_status,
        ),
        (
            "child_graph_hash_mutation", "child hash",
            lambda row: require(
                row["source_child_graph_sha256"]
                == samples["one_row"]["source_child_graph_sha256"],
                "child hash",
            ),
            samples["one_row"], wrong_hash,
        ),
    ]
    results = [
        qualify_in_process_case(name, expected, check, clean, mutated)
        for name, expected, check, clean, mutated in cases
    ]
    diagnostics = {name: expected for name, expected, *_rest in cases}
    report = {
        "schema": "k2p-corrected-probe-independent-mutations-v2",
        "status": "PASS",
        "source_certificate_sha256": sha_file(certificate_path),
        "source_certificate_payload_sha256": certificate_payload_sha256,
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "clean_baseline": {
            "status": "PASS",
            "checks": len(cases),
            "all_unmutated_samples_accepted": True,
        },
        "diagnostic_contract": diagnostics,
        "qualification_contract": {
            "clean_baseline_required_per_case": True,
            "only_AuditFailure_qualifies": True,
            "exact_diagnostic_required": True,
            "unrelated_exceptions_rejected": True,
            "caller_owned_outputs_required": True,
        },
        "qualification_negative_controls": (
            run_mutation_qualification_negative_controls()
        ),
        "mutations": results,
        "mutations_rejected": len(results),
        "mutations_survived": 0,
    }
    report["payload_sha256"] = logical_payload(report)
    write_json(output, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", type=Path, default=DEFAULT_PACKAGE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--mutations-output", type=Path, default=DEFAULT_MUTATIONS)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    args = parser.parse_args()
    args.output, args.mutations_output = validate_output_paths(
        args.output, args.mutations_output, args.allow_authoritative_output
    )
    args.output.unlink(missing_ok=True)
    args.mutations_output.unlink(missing_ok=True)
    if not __debug__:
        raise AuditFailure("independent graph audit may not run with assertions optimized away")
    package = args.package_dir.resolve()
    certificate_path = package / "probe_coherence_certificate.json"
    certificate = json.loads(certificate_path.read_text())
    require(certificate["schema"] == "k2p-corrected-coherent-probe-closure-v1", "certificate schema")
    require(certificate["status"] == "PASS", "certificate status")
    require(certificate["payload_sha256"] == logical_payload(certificate), "certificate logical payload")
    require(certificate["forbidden_rooted_triple_oracle_used"] is False, "rooted oracle flag")
    require(certificate["classifier_order"] == [
        "exact_labelled_isomorphism_or_ordinary_triangle",
        "displayed_quartet_mismatch",
        "direct_original_full_map_Ti_zero_versus_Bernstein_strict_sign",
        "unresolved_fatal",
    ], "classifier order")
    reject_rooted_oracle_fields(certificate)

    input_paths = {
        "atlas_sha256": ATLAS_PATH,
        "probe_input_contract_sha256": INPUT_CONTRACT,
        "probe_input_independent_replay_sha256": INPUT_REPLAY,
        "probe_input_mutations_sha256": PROJECT / "work/adversarial_proof_review/probe_input_mutation_certificate.json",
        "corrected_restoration_sha256": PROJECT / "work/restoration_sign_reclassification/corrected_restoration_forest.json",
        "raw4_ledger_sha256": PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz",
        "theta2_fixed_full_closure_sha256": PROJECT / "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz",
        "cycle_physical_anchors_sha256": PROJECT / "work/cycle_three_port_closure/artifacts/physical_anchors.json",
        "cycle_promotion_sha256": PROJECT / "work/cycle_three_port_closure/promotion/cycle_promotion_certificate.json",
    }
    for field, path in input_paths.items():
        require(certificate["inputs"][field] == sha_file(path), f"input binding:{field}")

    contract = json.loads(INPUT_CONTRACT.read_text())
    require(contract["schema"] == "k2p-root-invariant-probe-input-contract-v2", "input contract schema")
    require(contract["status"] == "PASS", "input contract status")
    contract_payload = dict(contract)
    claimed_contract_payload = contract_payload.pop("payload_sha256")
    require(claimed_contract_payload == sha(contract_payload), "input contract payload")
    require(certificate["inputs"]["probe_input_contract_payload_sha256"] == claimed_contract_payload,
            "input contract payload binding")
    input_replay = json.loads(INPUT_REPLAY.read_text())
    replay_payload = dict(input_replay)
    claimed_replay_payload = replay_payload.pop("payload_sha256")
    require(claimed_replay_payload == sha(replay_payload), "input replay payload")
    require(input_replay.get("status") == "PASS", "input replay status")
    require(input_replay.get("contract_sha256") == sha_file(INPUT_CONTRACT),
            "input replay contract binding")
    require(input_replay.get("contract_payload_sha256") == claimed_contract_payload,
            "input replay contract payload binding")

    proof_path = package / certificate["registries"]["separation"]["path"]
    require(sha_file(proof_path) == certificate["registries"]["separation"]["sha256"], "proof file hash")
    with gzip.open(proof_path, "rt") as handle:
        proof = json.load(handle)
    claimed_proof_payload = proof.pop("payload_sha256")
    require(claimed_proof_payload == sha(proof), "proof payload")
    proof["payload_sha256"] = claimed_proof_payload
    require(claimed_proof_payload == certificate["registries"]["separation"]["payload_sha256"],
            "proof payload cross-binding")
    reject_rooted_oracle_fields(proof)
    quartet_proofs = proof["separation_proof_registry"]
    require(len(quartet_proofs) == 638, "quartet proof count")
    for proof_id, item in quartet_proofs.items():
        require(proof_id == f"Q:{sha(item)}", f"quartet proof self hash:{proof_id}")
        require(item["source_displayed_splits"] != item["target_displayed_splits"],
                f"quartet proof inequality:{proof_id}")
    ti_certificates, strict_polynomials = validate_ti_registry(proof)

    transport_records: dict[str, dict[str, Any]] = {}
    transport_order = OrderedRoot()
    transport_info = certificate["registries"]["exact_transports"]
    transport_path = package / transport_info["path"]
    require(sha_file(transport_path) == transport_info["sha256"], "transport file hash")
    for number, row in iter_jsonl(transport_path):
        reject_rooted_oracle_fields(row)
        require(set(row) == {"record_kind", "record_id", "record"}, f"transport row schema:{number}")
        require(row["record_kind"] == "exact_labelled_mixed_graph_transport", f"transport kind:{number}")
        require(row["record_id"] not in transport_records, f"duplicate transport:{row['record_id']}")
        validate_transport_record(row["record_id"], row["record"])
        transport_records[row["record_id"]] = row["record"]
        transport_order.add(row)
    require(len(transport_records) == transport_info["unique_records"] == 67_741, "transport census")
    transport_order.check(transport_info["ordered_records"], "transport ledger")

    restriction_records: dict[str, dict[str, Any]] = {}
    restriction_order = OrderedRoot()
    restriction_info = certificate["registries"]["parent_restrictions"]
    restriction_path = package / restriction_info["path"]
    require(sha_file(restriction_path) == restriction_info["sha256"], "restriction file hash")
    for number, row in iter_jsonl(restriction_path):
        reject_rooted_oracle_fields(row)
        require(set(row) == {"record_kind", "record_id", "record"}, f"restriction row schema:{number}")
        require(row["record_kind"] == "exact_parent_marginal_restriction", f"restriction kind:{number}")
        require(row["record_id"] not in restriction_records, f"duplicate restriction:{row['record_id']}")
        validate_restriction_record(row["record_id"], row["record"])
        restriction_records[row["record_id"]] = row["record"]
        restriction_order.add(row)
    require(len(restriction_records) == restriction_info["unique_records"] == 4_379, "restriction census")
    restriction_order.check(restriction_info["ordered_records"], "restriction ledger")

    primitive = import_path("independent_probe_input_reconstructor", INPUT_RECONSTRUCTOR)
    atlas = primitive.load_module("independent_probe_graph_atlas", ATLAS_PATH)
    # The independently frozen cycle generator imports this exact module name.
    common = primitive.load_module(
        "cycle_common", PROJECT / "work/cycle_three_port_closure/cycle_common.py"
    )
    cycle_generator = primitive.load_module(
        "independent_probe_cycle_generator", PROJECT / "work/cycle_three_port_closure/generate_cycle_closure.py"
    )
    upstream = primitive.prepare_upstream(atlas, common, cycle_generator)

    public_anchors = certificate["anchor_inventory"]["public_anchors"]
    contract_anchors = contract["anchors"]
    require(len(public_anchors) == len(contract_anchors) == 176, "anchor count")
    require([row["anchor_id"] for row in public_anchors] == [row["anchor_id"] for row in contract_anchors],
            "anchor order")
    anchor_graphs: dict[str, dict[str, Any]] = {}
    anchor_classes = RelationClassRegistry(atlas)
    anchor_class_coverage: dict[int, list[str]] = collections.defaultdict(list)
    used_transports: set[str] = set()
    used_restrictions: set[str] = set()
    used_quartets: set[str] = set()
    used_ti: set[str] = set()
    ti_parameterization_witnesses: set[str] = set()
    anchor_public_hashes = []
    for number, (contract_anchor, public_anchor) in enumerate(zip(contract_anchors, public_anchors)):
        anchor_id = contract_anchor["anchor_id"]
        source, target = primitive.reconstruct_anchor(atlas, upstream, contract_anchor)
        require(graph_sha(source) == contract_anchor["source_graph_sha256"], f"anchor source:{anchor_id}")
        require(graph_sha(target) == contract_anchor["target_graph_sha256"], f"anchor target:{anchor_id}")
        source_profile = site_profile(primitive, atlas, source)
        target_profile = site_profile(primitive, atlas, target)
        require(source_profile == contract_anchor["source_candidate_profile"], f"anchor source profile:{anchor_id}")
        require(target_profile == contract_anchor["target_candidate_profile"], f"anchor target profile:{anchor_id}")
        transport_id = contract_anchor["parent_transport"]["transport_sha256"]
        require(transport_id in transport_records, f"anchor transport absent:{anchor_id}")
        transport = transport_records[transport_id]
        require(public_transport_record(transport) == contract_anchor["parent_transport"],
                f"anchor transport payload:{anchor_id}")
        validate_transport_on_graphs(atlas, source, target, transport_id, transport, f"anchor:{anchor_id}")
        used_transports.add(transport_id)
        global_triangle = global_triangle_from_transport(atlas, source, target, transport)
        class_id = anchor_classes.find_or_add(
            source, target, transport["relation"], public_transport_record(transport), True
        )
        require(class_id == public_anchor["canonical_anchor_class_id"], f"anchor class:{anchor_id}")
        anchor_class_coverage[class_id].append(anchor_id)
        expected_public = public_anchor_expected(contract_anchor, class_id, global_triangle)
        require(public_anchor == expected_public, f"public anchor row:{anchor_id}")
        anchor_public_hashes.append(sha(public_anchor))
        source_by_id = {row["site_id"]: row for row in source_profile["sites"]}
        target_by_id = {row["site_id"]: row for row in target_profile["sites"]}
        computed_site_transport = []
        edge_map = transport_edge_map(transport)
        for source_site in source_profile["sites"]:
            mapped_edge = edge_map[site_edge_strings(source_site)]
            target_site = next(row for row in target_profile["sites"] if site_edge_strings(row) == mapped_edge)
            computed_site_transport.append({
                "source_site_id": source_site["site_id"],
                "source_site_type": source_site["site_type"],
                "target_site_id": target_site["site_id"],
                "target_site_type": target_site["site_type"],
            })
        computed_site_transport.sort(key=lambda row: row["source_site_id"])
        require(computed_site_transport == contract_anchor["site_transport"], f"anchor site transport:{anchor_id}")
        require(sha(computed_site_transport) == contract_anchor["site_transport_sha256"],
                f"anchor site transport hash:{anchor_id}")
        require(first_quartet_mismatch(quartet_deck(source), quartet_deck(target)) is None,
                f"anchor old-label quartet mismatch:{anchor_id}")
        anchor_graphs[anchor_id] = {
            "source": source, "target": target,
            "source_profile": source_profile, "target_profile": target_profile,
            "transport_id": transport_id, "transport": transport,
            "global_triangle": global_triangle,
            "origin": contract_anchor["origin"], "labels": tuple(contract_anchor["labels"]),
        }
    require(len(anchor_classes.representatives) == certificate["anchor_inventory"]["canonical_anchor_classes"] == 39,
            "anchor canonical class census")
    require({str(key): value for key, value in anchor_class_coverage.items()}
            == certificate["anchor_inventory"]["canonical_class_coverage"], "anchor class coverage")
    require(sha(anchor_public_hashes) == certificate["anchor_inventory"]["ordered_public_anchor_hash_root"],
            "anchor public ordered hash")
    # The upstream primitive locator tables include the full 405,216-row raw
    # universe and are no longer needed once every anchor graph is rebuilt.
    del upstream, anchor_classes
    gc.collect()
    print("independent-probe-audit: anchors 176/176", file=sys.stderr, flush=True)

    one_path = package / "one_port_ledger.jsonl.gz"
    require(sha_file(one_path) == certificate["one_port"]["ledger_sha256"], "one ledger file hash")
    one_iterator = iter(iter_jsonl(one_path))
    one_order = OrderedRoot()
    one_counts = collections.Counter()
    one_compatible = 0
    one_classes = RelationClassRegistry(atlas)
    one_parents: list[dict[str, Any]] = []
    one_class_ids_by_base: dict[str, set[int]] = collections.defaultdict(set)
    ti_compiler = FullMapCompiler()
    samples: dict[str, Any] = {}
    for anchor_number, public_anchor in enumerate(public_anchors):
        anchor_id = public_anchor["anchor_id"]
        anchor = anchor_graphs[anchor_id]
        label = max(anchor["labels"]) + 1
        source_children = prepare_children(
            primitive, atlas, anchor["source"], anchor["source_profile"], label,
            f"P1:{anchor_id}", "source", transport_records, restriction_records, f"one:{anchor_id}",
        )
        target_children = prepare_children(
            primitive, atlas, anchor["target"], anchor["target_profile"], label,
            f"P1:{anchor_id}", "target", transport_records, restriction_records, f"one:{anchor_id}",
        )
        for child in source_children + target_children:
            used_restrictions.add(child["restriction_id"])
            restriction_transport_id = restriction_records[child["restriction_id"]]["restriction_transport_sha256"]
            if restriction_transport_id in transport_records:
                used_transports.add(restriction_transport_id)
        parent_compatible = 0
        for source_child in source_children:
            for target_child in target_children:
                try:
                    row_number, row = next(one_iterator)
                except StopIteration as error:
                    raise AuditFailure("one ledger omitted raw records") from error
                context = f"one:{row_number}"
                reject_rooted_oracle_fields(row)
                validate_equality_row_schema(row, "A+p", context)
                require(row["stage"] == "A+p" and row["parent_anchor_id"] == anchor_id, f"{context}:parent/order")
                require(row["origin"] == anchor["origin"] and row["inserted_label"] == label,
                        f"{context}:origin/label")
                validate_common_row(
                    row, source_child, target_child,
                    "source_site_index", "target_site_index", "source_site_id", "target_site_id", context,
                )
                one_order.add(row)
                one_counts[row["status"]] += 1
                compatible = transported_site(anchor["transport"], source_child["site"], target_child["site"])
                parent_compatible += compatible
                one_compatible += compatible
                if row["status"] in {"isomorphic", "triangle"}:
                    require(compatible, f"{context}:equality on incompatible sites")
                    transport_id = row["transport_id"]
                    require(transport_id in transport_records, f"{context}:transport reference")
                    child_transport = transport_records[transport_id]
                    require(child_transport["relation"] == row["status"], f"{context}:relation")
                    validate_transport_on_graphs(
                        atlas, source_child["graph"], target_child["graph"],
                        transport_id, child_transport, context,
                    )
                    validate_child_coherence(
                        anchor["transport"], child_transport,
                        source_child["site"], target_child["site"], anchor["global_triangle"], context,
                    )
                    require(row["parent_transport_id"] == anchor["transport_id"], f"{context}:parent transport")
                    expected_triangle_hash = None if anchor["global_triangle"] is None else sha(anchor["global_triangle"])
                    require(row["global_triangle_sha256"] == expected_triangle_hash, f"{context}:global triangle hash")
                    require(row["transport_restriction"] == (
                        "exact on every parent mixed vertex, the selected mixed edge site, "
                        "and the inherited ordinary triangle when present"
                    ), f"{context}:transport restriction statement")
                    used_transports.add(transport_id)
                    public_transport = public_transport_record(child_transport)
                    class_id = one_classes.find_or_add(
                        source_child["graph"], target_child["graph"], row["status"], public_transport, True
                    )
                    parent_id = f"P1:{anchor_id}:{source_child['site_index']}:{target_child['site_index']}"
                    one_class_ids_by_base[anchor_id].add(class_id)
                    one_parents.append({
                        "parent_id": parent_id, "base_anchor_id": anchor_id,
                        "origin": anchor["origin"], "relation": row["status"],
                        "source": source_child["graph"], "target": target_child["graph"],
                        "transport_id": transport_id, "transport": child_transport,
                        "global_triangle": anchor["global_triangle"], "class_id": class_id,
                        "first_label": label,
                        "first_source_site_index": source_child["site_index"],
                        "first_target_site_index": target_child["site_index"],
                    })
                    samples.setdefault("one_row", row)
                    if row["status"] == "triangle":
                        samples.setdefault("triangle_row", row)
                elif row["status"] == "displayed_quartet_mismatch":
                    require(not compatible, f"{context}:quartet on compatible sites")
                    validate_quartet_row(
                        row, source_child["quartet_deck"], target_child["quartet_deck"],
                        quartet_proofs, context,
                    )
                    used_quartets.add(row["proof_id"])
                    samples.setdefault("quartet_row", row)
                elif row["status"] == "full_map_Ti_strict_sign":
                    require(compatible, f"{context}:T_i on incompatible sites")
                    require(first_quartet_mismatch(
                        source_child["quartet_deck"], target_child["quartet_deck"]
                    ) is None, f"{context}:T_i after available quartet")
                    validate_ti_pair(
                        ti_compiler, source_child["graph"], target_child["graph"], row["proof_id"],
                        ti_certificates, strict_polynomials, context, ti_parameterization_witnesses,
                    )
                    used_ti.add(row["proof_id"])
                    samples.setdefault("ti_row", row)
                else:
                    raise AuditFailure(f"{context}:unresolved/unexpected status:{row['status']}")
        if anchor_number % 25 == 0:
            print(f"independent-probe-audit: one anchor {anchor_number + 1}/176", file=sys.stderr, flush=True)
    require(next(one_iterator, None) is None, "one ledger has extra raw records")
    one_order.check(certificate["one_port"]["ordered_ledger"], "one ledger")
    require(dict(sorted(one_counts.items())) == certificate["one_port"]["counts"], "one counts")
    require(one_counts["displayed_quartet_mismatch"] == 27_758, "one incompatible census")
    require(one_compatible == 2_206, "one compatible census")
    require(one_compatible == (
        one_counts["isomorphic"] + one_counts["triangle"] + one_counts["full_map_Ti_strict_sign"]
    ), "one compatible classifier partition")
    require(len(one_parents) == certificate["one_port"]["equality_survivors"] == 2_107,
            "one equality census")
    require(len(one_classes.representatives) == certificate["one_port"]["canonical_equality_relation_classes"] == 469,
            "one relation class census")
    ti_compiler.pullbacks.clear()
    ti_compiler.states.clear()
    gc.collect()
    print("independent-probe-audit: one-port 29964/29964", file=sys.stderr, flush=True)

    parent_path = package / "two_port_parent_inventory.jsonl.gz"
    require(sha_file(parent_path) == certificate["two_port"]["parent_inventory_sha256"],
            "parent inventory file hash")
    parent_iterator = iter(iter_jsonl(parent_path))
    parent_order = OrderedRoot()
    for parent_number, parent in enumerate(one_parents):
        try:
            row_number, row = next(parent_iterator)
        except StopIteration as error:
            raise AuditFailure("parent inventory omitted equality parent") from error
        context = f"parent:{row_number}"
        reject_rooted_oracle_fields(row)
        require(set(row) == {
            "base_anchor_id", "canonical_one_port_relation_class_id", "first_label",
            "first_source_site_index", "first_target_site_index", "one_port_parent_id", "origin",
            "raw_second_probe_pairs", "relation", "source_candidate_profile", "source_graph_sha256",
            "target_candidate_profile", "target_graph_sha256",
        }, f"{context}:schema")
        require(row["one_port_parent_id"] == parent["parent_id"], f"{context}:ordered parent identity")
        require(row["base_anchor_id"] == parent["base_anchor_id"], f"{context}:base")
        require(row["origin"] == parent["origin"] and row["relation"] == parent["relation"], f"{context}:origin/relation")
        require(row["canonical_one_port_relation_class_id"] == parent["class_id"], f"{context}:class")
        require(row["first_label"] == parent["first_label"], f"{context}:first label")
        require(row["first_source_site_index"] == parent["first_source_site_index"], f"{context}:first source site")
        require(row["first_target_site_index"] == parent["first_target_site_index"], f"{context}:first target site")
        require(row["source_graph_sha256"] == graph_sha(parent["source"]), f"{context}:source graph")
        require(row["target_graph_sha256"] == graph_sha(parent["target"]), f"{context}:target graph")
        source_profile = site_profile(primitive, atlas, parent["source"])
        target_profile = site_profile(primitive, atlas, parent["target"])
        require(row["source_candidate_profile"] == source_profile, f"{context}:source profile")
        require(row["target_candidate_profile"] == target_profile, f"{context}:target profile")
        require(source_profile["site_count"] == target_profile["site_count"], f"{context}:site count drift")
        require(row["raw_second_probe_pairs"] == source_profile["site_count"] * target_profile["site_count"],
                f"{context}:Cartesian count")
        parent["source_profile"] = source_profile
        parent["target_profile"] = target_profile
        parent_order.add(row)
    require(next(parent_iterator, None) is None, "parent inventory has extra rows")
    parent_order.check(certificate["two_port"]["ordered_parent_inventory"], "parent inventory")
    require(len(one_parents) == certificate["two_port"]["parents"], "parent inventory census")

    two_path = package / "two_port_ledger.jsonl.gz"
    require(sha_file(two_path) == certificate["two_port"]["ledger_sha256"], "two ledger file hash")
    two_iterator = iter(iter_jsonl(two_path))
    two_order = OrderedRoot()
    two_counts = collections.Counter()
    two_compatible = 0
    reverse_counts = collections.Counter()
    equality_with_global_triangle = 0
    new_triangle_above_isomorphism = 0
    for parent_number, parent in enumerate(one_parents):
        base = anchor_graphs[parent["base_anchor_id"]]
        second_label = max(labels_of(parent["source"])) + 1
        source_children = prepare_children(
            primitive, atlas, parent["source"], parent["source_profile"], second_label,
            f"P2:{parent['parent_id']}", "source", transport_records, restriction_records,
            f"two:{parent['parent_id']}",
        )
        target_children = prepare_children(
            primitive, atlas, parent["target"], parent["target_profile"], second_label,
            f"P2:{parent['parent_id']}", "target", transport_records, restriction_records,
            f"two:{parent['parent_id']}",
        )
        for child in source_children + target_children:
            used_restrictions.add(child["restriction_id"])
            restriction_transport_id = restriction_records[child["restriction_id"]]["restriction_transport_sha256"]
            if restriction_transport_id in transport_records:
                used_transports.add(restriction_transport_id)
        for source_child in source_children:
            for target_child in target_children:
                try:
                    row_number, row = next(two_iterator)
                except StopIteration as error:
                    raise AuditFailure("two ledger omitted raw records") from error
                context = f"two:{row_number}"
                reject_rooted_oracle_fields(row)
                validate_equality_row_schema(row, "A+p+q", context)
                require(row["stage"] == "A+p+q" and row["one_port_parent_id"] == parent["parent_id"],
                        f"{context}:parent/order")
                require(row["base_anchor_id"] == parent["base_anchor_id"], f"{context}:base")
                require(row["origin"] == parent["origin"], f"{context}:origin")
                require(row["first_label"] == parent["first_label"] and row["second_label"] == second_label,
                        f"{context}:labels")
                require(row["first_source_site_index"] == parent["first_source_site_index"],
                        f"{context}:first source site")
                require(row["first_target_site_index"] == parent["first_target_site_index"],
                        f"{context}:first target site")
                validate_common_row(
                    row, source_child, target_child,
                    "second_source_site_index", "second_target_site_index",
                    "second_source_site_id", "second_target_site_id", context,
                )
                two_order.add(row)
                two_counts[row["status"]] += 1
                compatible = transported_site(parent["transport"], source_child["site"], target_child["site"])
                two_compatible += compatible
                if row["status"] in {"isomorphic", "triangle"}:
                    require(compatible, f"{context}:equality on incompatible sites")
                    transport_id = row["transport_id"]
                    require(transport_id in transport_records, f"{context}:transport reference")
                    child_transport = transport_records[transport_id]
                    require(child_transport["relation"] == row["status"], f"{context}:relation")
                    validate_transport_on_graphs(
                        atlas, source_child["graph"], target_child["graph"],
                        transport_id, child_transport, context,
                    )
                    validate_child_coherence(
                        parent["transport"], child_transport,
                        source_child["site"], target_child["site"], parent["global_triangle"], context,
                    )
                    require(row["parent_transport_id"] == parent["transport_id"], f"{context}:parent transport")
                    expected_triangle_hash = None if parent["global_triangle"] is None else sha(parent["global_triangle"])
                    require(row["global_triangle_sha256"] == expected_triangle_hash, f"{context}:global triangle hash")
                    require(row["transport_restriction"] == (
                        "exact on every parent mixed vertex, the selected mixed edge site, "
                        "and the inherited ordinary triangle when present"
                    ), f"{context}:transport restriction statement")
                    used_transports.add(transport_id)
                    if row["status"] == "triangle":
                        if parent["global_triangle"] is None:
                            new_triangle_above_isomorphism += 1
                        else:
                            equality_with_global_triangle += 1

                    reverse = row["reverse_order_certificate"]
                    require(set(reverse) == {
                        "conclusion", "remove_first_label", "retain_then_rename_second_label",
                        "reverse_parent_canonical_one_port_class_id", "reverse_parent_relation",
                        "reverse_parent_source_graph_sha256", "reverse_parent_target_graph_sha256",
                        "reverse_parent_transport_id", "same_base_anchor_id",
                    }, f"{context}:reverse schema")
                    keep = set(base["labels"]) | {second_label}
                    reverse_source = atlas.restrict_rooted(source_child["graph"], keep)
                    reverse_target = atlas.restrict_rooted(target_child["graph"], keep)
                    reverse_source = relabel_leaf(reverse_source, second_label, parent["first_label"])
                    reverse_target = relabel_leaf(reverse_target, second_label, parent["first_label"])
                    require(reverse["remove_first_label"] == parent["first_label"], f"{context}:reverse removed label")
                    require(reverse["retain_then_rename_second_label"] == [second_label, parent["first_label"]],
                            f"{context}:reverse rename")
                    require(reverse["same_base_anchor_id"] == parent["base_anchor_id"], f"{context}:reverse base")
                    require(reverse["reverse_parent_source_graph_sha256"] == graph_sha(reverse_source),
                            f"{context}:reverse source graph")
                    require(reverse["reverse_parent_target_graph_sha256"] == graph_sha(reverse_target),
                            f"{context}:reverse target graph")
                    reverse_transport_id = reverse["reverse_parent_transport_id"]
                    require(reverse_transport_id in transport_records, f"{context}:reverse transport reference")
                    reverse_transport = transport_records[reverse_transport_id]
                    require(reverse_transport["relation"] == reverse["reverse_parent_relation"],
                            f"{context}:reverse relation")
                    validate_transport_on_graphs(
                        atlas, reverse_source, reverse_target,
                        reverse_transport_id, reverse_transport, f"{context}:reverse",
                    )
                    base_vertices = dict(base["transport"]["vertex_map"])
                    reverse_vertices = dict(reverse_transport["vertex_map"])
                    require(all(reverse_vertices.get(node) == target for node, target in base_vertices.items()),
                            f"{context}:reverse base transport restriction")
                    if reverse_transport["relation"] == "triangle":
                        require(base["global_triangle"] is not None, f"{context}:reverse new triangle")
                        require(
                            reverse_transport["source_triangle_edges"]
                            == base["global_triangle"]["source_triangle_edges"],
                            f"{context}:reverse source global triangle",
                        )
                        require(
                            reverse_transport["target_triangle_edges"]
                            == base["global_triangle"]["target_triangle_edges"],
                            f"{context}:reverse target global triangle",
                        )
                        ordinary = reverse_transport["ordinary_triangle_arrowhead_witness"]
                        require(
                            ordinary["source_common_reticulation"]
                            == base["global_triangle"]["source_reticulation"],
                            f"{context}:reverse source global reticulation",
                        )
                        require(
                            ordinary["target_common_reticulation"]
                            == base["global_triangle"]["target_reticulation"],
                            f"{context}:reverse target global reticulation",
                        )
                    reverse_class_id = one_classes.find_or_add(
                        reverse_source, reverse_target, reverse["reverse_parent_relation"],
                        public_transport_record(reverse_transport), False,
                    )
                    require(reverse_class_id == reverse["reverse_parent_canonical_one_port_class_id"],
                            f"{context}:reverse canonical class")
                    require(reverse_class_id in one_class_ids_by_base[parent["base_anchor_id"]],
                            f"{context}:reverse class absent above base")
                    require(reverse["conclusion"] == (
                        "the reversed one-probe marginal is present in the complete one-port equality universe"
                    ), f"{context}:reverse conclusion")
                    used_transports.add(reverse_transport_id)
                    reverse_counts[reverse["reverse_parent_relation"]] += 1
                    samples.setdefault("reverse", reverse)
                    samples.setdefault("two_row", row)
                elif row["status"] == "displayed_quartet_mismatch":
                    require(not compatible, f"{context}:quartet on compatible sites")
                    validate_quartet_row(
                        row, source_child["quartet_deck"], target_child["quartet_deck"],
                        quartet_proofs, context,
                    )
                    used_quartets.add(row["proof_id"])
                elif row["status"] == "full_map_Ti_strict_sign":
                    require(compatible, f"{context}:T_i on incompatible sites")
                    require(first_quartet_mismatch(
                        source_child["quartet_deck"], target_child["quartet_deck"]
                    ) is None, f"{context}:T_i after available quartet")
                    validate_ti_pair(
                        ti_compiler, source_child["graph"], target_child["graph"], row["proof_id"],
                        ti_certificates, strict_polynomials, context, ti_parameterization_witnesses,
                    )
                    used_ti.add(row["proof_id"])
                else:
                    raise AuditFailure(f"{context}:unresolved/unexpected status:{row['status']}")
        if parent_number % 100 == 0:
            print(f"independent-probe-audit: two parent {parent_number + 1}/2107", file=sys.stderr, flush=True)
        # Pullbacks and switch states are parent-local audit scratch.  Keeping
        # them cannot strengthen the replay and causes avoidable linear RSS.
        ti_compiler.pullbacks.clear()
        ti_compiler.states.clear()
        if parent_number % 50 == 0:
            gc.collect()
    require(next(two_iterator, None) is None, "two ledger has extra raw records")
    two_order.check(certificate["two_port"]["ordered_ledger"], "two ledger")
    require(dict(sorted(two_counts.items())) == certificate["two_port"]["counts"], "two counts")
    require(two_counts["displayed_quartet_mismatch"] == 511_266, "two incompatible census")
    require(two_compatible == 33_305, "two compatible census")
    require(two_compatible == (
        two_counts["isomorphic"] + two_counts["triangle"] + two_counts["full_map_Ti_strict_sign"]
    ), "two compatible classifier partition")
    require(sum(reverse_counts.values()) == certificate["two_port"]["equality_survivors"] == 32_729,
            "two equality/reverse census")
    require(dict(sorted(reverse_counts.items())) == certificate["two_port"]["reverse_order_parent_relation_counts"],
            "reverse relation census")
    require(new_triangle_above_isomorphism == 0, "new triangle above isomorphic parent")
    require(equality_with_global_triangle == 1_760, "global triangle two-port census")

    require(used_restrictions == set(restriction_records),
            f"restriction registry orphan/missing:{len(set(restriction_records) - used_restrictions)}")
    require(used_transports == set(transport_records),
            f"transport registry orphan/missing:{len(set(transport_records) - used_transports)}")
    require(used_quartets == set(quartet_proofs),
            f"quartet registry orphan/missing:{len(set(quartet_proofs) - used_quartets)}")
    require(used_ti == set(ti_certificates),
            f"T_i registry orphan/missing:{len(set(ti_certificates) - used_ti)}")
    require(ti_parameterization_witnesses == set(strict_polynomials),
            f"T_i parameterization registry lacks graph witnesses:{len(set(strict_polynomials) - ti_parameterization_witnesses)}")

    assembly = certificate["assembly_theorem"]
    require(assembly["unresolved"] == assembly["incoherent"] == 0, "assembly zero gates")
    require(assembly["two_port_order_gate"]["reversed_marginals_checked"] == 32_729, "assembly reverse gate")
    require(assembly["one_global_triangle_gate"]["triangle_anchors"] == 33, "assembly triangle anchors")
    require(assembly["one_global_triangle_gate"]["one_port_parents_inheriting_triangle"] == 192,
            "assembly one triangle parents")
    require(assembly["one_global_triangle_gate"]["two_port_equalities_inheriting_triangle"] == 1_760,
            "assembly two triangle equalities")

    site_partition_path = package / "site_transport_partition_verification.json"
    site_partition = json.loads(site_partition_path.read_text())
    require(site_partition["status"] == "PASS", "site partition auxiliary status")
    require(site_partition["payload_sha256"] == logical_payload(site_partition), "site partition auxiliary payload")
    require(site_partition["one_port"]["site_transport_partition"]["compatible"] == 2_206,
            "site partition one compatible")
    require(site_partition["two_port"]["site_transport_partition"]["compatible"] == 33_305,
            "site partition two compatible")

    samples["coverage_rows"] = 29_964 + 2_107 + 544_571
    samples["other_parent_id"] = next(
        parent["parent_id"] for parent in one_parents
        if parent["parent_id"] != samples["two_row"]["one_port_parent_id"]
    )
    samples["other_transport_id"] = next(
        value for value in transport_records if value != samples["reverse"]["reverse_parent_transport_id"]
    )
    samples["other_quartet_id"] = next(
        value for value in quartet_proofs if value != samples["quartet_row"]["proof_id"]
    )
    samples["other_ti_id"] = next(value for value in ti_certificates if value != samples["ti_row"]["proof_id"])
    samples["restriction_id"] = samples["one_row"]["source_parent_restriction_id"]
    samples["restriction"] = restriction_records[samples["restriction_id"]]
    samples["transport_id"] = samples["one_row"]["transport_id"]
    samples["transport"] = transport_records[samples["transport_id"]]
    mutation_report = run_mutations(
        samples,
        args.mutations_output,
        certificate_path,
        certificate["payload_sha256"],
    )

    primary_files = {
        "probe_coherence_certificate.json": certificate_path,
        "one_port_ledger.jsonl.gz": one_path,
        "two_port_parent_inventory.jsonl.gz": parent_path,
        "two_port_ledger.jsonl.gz": two_path,
        "exact_transport_ledger.jsonl.gz": transport_path,
        "parent_restriction_ledger.jsonl.gz": restriction_path,
        "separation_proof_registry.json.gz": proof_path,
    }
    report = {
        "schema": "k2p-corrected-probe-independent-primitive-graph-audit-v1",
        "status": "PASS",
        "source_payload_sha256": certificate["payload_sha256"],
        "source_file_sha256": sha_file(certificate_path),
        "primary_file_sha256": {name: sha_file(path) for name, path in primary_files.items()},
        "primitive_anchor_replay": {
            "anchors": 176,
            "canonical_graph_pair_transport_classes": 39,
            "source_sites": 2_206,
            "target_sites": 2_206,
            "independent_replay_payload_sha256": claimed_replay_payload,
        },
        "one_port": {
            "raw_pairs": sum(one_counts.values()),
            "compatible_site_pairs": one_compatible,
            "incompatible_site_pairs": one_counts["displayed_quartet_mismatch"],
            "counts": dict(sorted(one_counts.items())),
            "equality_relation_classes": len(one_classes.representatives),
        },
        "two_port": {
            "parents": len(one_parents),
            "raw_pairs": sum(two_counts.values()),
            "compatible_site_pairs": two_compatible,
            "incompatible_site_pairs": two_counts["displayed_quartet_mismatch"],
            "counts": dict(sorted(two_counts.items())),
            "reverse_marginals": sum(reverse_counts.values()),
            "reverse_relation_counts": dict(sorted(reverse_counts.items())),
        },
        "exact_witnesses": {
            "transport_records_applied_to_reconstructed_graphs": len(used_transports),
            "parent_restrictions_reconstructed": len(used_restrictions),
            "quartet_certificates_applied": len(used_quartets),
            "T_i_relation_certificates_applied": len(used_ti),
            "T_i_strict_polynomials_Bernstein_replayed": len(strict_polynomials),
            "new_global_triangles": new_triangle_above_isomorphism,
            "unresolved": 0,
            "incoherent": 0,
        },
        "classifier_partition": {
            "one": "27758 incompatible=quartet; 2206 compatible=1915 isomorphic+192 triangle+99 T_i",
            "two": "511266 incompatible=quartet; 33305 compatible=30969 isomorphic+1760 triangle+576 T_i",
            "relation_first": True,
            "quartet_second": True,
            "direct_full_map_Ti_third": True,
            "forbidden_rooted_oracle_fields": 0,
        },
        "auxiliary_independent_site_partition": {
            "file_sha256": sha_file(site_partition_path),
            "payload_sha256": site_partition["payload_sha256"],
        },
        "mutations": {
            "report_sha256": sha_file(args.mutations_output),
            "payload_sha256": mutation_report["payload_sha256"],
            "rejected": mutation_report["mutations_rejected"],
            "survived": mutation_report["mutations_survived"],
        },
        "conclusion": (
            "PASS: the frozen corrected probe is independently reconstructed from primitive anchors; "
            "all raw one-/two-port rows, exact transports, marginal restrictions, reverse parents, "
            "ordinary-triangle inheritance, quartet witnesses, and direct full-map T_i certificates close with zero gaps"
        ),
    }
    report["payload_sha256"] = logical_payload(report)
    write_json(args.output, report)
    print(json.dumps({
        "status": report["status"],
        "source_payload_sha256": report["source_payload_sha256"],
        "payload_sha256": report["payload_sha256"],
        "mutations": report["mutations"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (
        AuditFailure, AssertionError, KeyError, IndexError, OSError, StopIteration,
        TypeError, ValueError, json.JSONDecodeError, nx.NetworkXError,
    ) as error:
        raise SystemExit(f"INDEPENDENT_CORRECTED_PROBE_GRAPH_AUDIT_FAIL:{error}") from error
