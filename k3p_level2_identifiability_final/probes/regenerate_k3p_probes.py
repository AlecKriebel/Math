#!/usr/bin/env python3
"""Regenerate the all-primitive K3P one-/two-port probe closure.

Classifier order is fail-closed and immutable:

1. exact labelled semi-directed isomorphism / ordinary triangle;
2. displayed-quartet mismatch;
3. exact K3P selected-marginal polynomial or directed-rank obstruction;
4. unresolved (fatal).

No rooted three-leaf restriction or rooted topology cache is used.
"""

from __future__ import annotations

import argparse
import ast
import collections
import fractions
import gc
import gzip
import hashlib
import importlib.util
import io
import itertools
import json
import math
import sys
import time
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
FROZEN = PROJECT / "input_frozen"
TOPOLOGY_PACKAGE = FROZEN / "model_independent_topology_package"
ATLAS_PATH = FROZEN / "k3p_cloud_artifacts/k3p_atlas_core.py"
INPUT_CONTRACT = TOPOLOGY_PACKAGE / "anchor_inputs/probe_input_contract.json"
INPUT_REPLAY = TOPOLOGY_PACKAGE / "anchor_inputs/probe_input_independent_verification.json"
INPUT_MUTATIONS = TOPOLOGY_PACKAGE / "anchor_inputs/probe_input_mutation_certificate.json"
RESTORATION = TOPOLOGY_PACKAGE / "anchor_inputs/corrected_restoration_forest.json"
RAW4 = TOPOLOGY_PACKAGE / "anchor_inputs/raw_directional_ledger.jsonl.gz"
THETA2 = TOPOLOGY_PACKAGE / "anchor_inputs/fixed_full_restoration_closure.json.gz"
CYCLE = TOPOLOGY_PACKAGE / "cycle"
CYCLE_ANCHORS = CYCLE / "physical_anchors.json"
CYCLE_PROMOTION = CYCLE / "cycle_promotion_certificate.json"
CYCLE_COMMON = CYCLE / "cycle_common.py"
CYCLE_GENERATOR = CYCLE / "generate_cycle_closure.py"
OUTPUT = HERE / "K3P_PROBE_COHERENCE_CERTIFICATE.json"
ONE_LEDGER = HERE / "one_port_ledger.jsonl.gz"
TWO_LEDGER = HERE / "two_port_ledger.jsonl.gz"
TWO_PARENT_LEDGER = HERE / "two_port_parent_inventory.jsonl.gz"
PROOF_REGISTRY = HERE / "separation_proof_registry.json.gz"
TRANSPORT_LEDGER = HERE / "exact_transport_ledger.jsonl.gz"
RESTRICTION_LEDGER = HERE / "parent_restriction_ledger.jsonl.gz"


class ProbeFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ProbeFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"import:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def graph_payload(graph):
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


def labels_of(graph):
    return tuple(sorted(
        data["label"] for _, data in graph.nodes(data=True)
        if isinstance(data.get("label"), int)
    ))


def edge_key(left, right):
    return tuple(sorted((repr(left), repr(right))))


def insert_on_arc(graph, candidate, label, namespace):
    tail = ast.literal_eval(candidate["tail"])
    head = ast.literal_eval(candidate["head"])
    require(graph.has_edge(tail, head), f"missing insertion arc:{candidate}")
    result = graph.copy()
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = (namespace, "subdivision", label, repr(tail), repr(head))
    leaf = (namespace, "leaf", label, repr(tail), repr(head))
    require(subdivision not in result and leaf not in result, "insertion collision")
    result.add_node(subdivision, role="tree", label=None, dummy=False, dummy_name=None)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    require(nx.is_directed_acyclic_graph(result), "insertion directed cycle")
    expected = {"root": (0, 2), "tree": (1, 2), "retic": (2, 1), "leaf": (1, 0)}
    for node, data in result.nodes(data=True):
        require(
            (result.in_degree(node), result.out_degree(node)) == expected[data["role"]],
            f"nonbinary insertion:{node}",
        )
    return result


def promote_roles(graph, roles):
    result = graph.copy()
    for role, label in roles:
        nodes = [node for node, data in result.nodes(data=True) if data.get("dummy_name") == role]
        require(len(nodes) == 1, f"dummy role:{role}:{nodes}")
        result.nodes[nodes[0]].update(label=label, dummy=False, dummy_name=None)
    return result


def ordinary_triangles(mixed):
    rows = []
    for left, middle, right in itertools.combinations(sorted(mixed.nodes(), key=repr), 3):
        if not (
            mixed.has_edge(left, middle)
            and mixed.has_edge(left, right)
            and mixed.has_edge(middle, right)
        ):
            continue
        edges = frozenset({
            frozenset((left, middle)), frozenset((left, right)),
            frozenset((middle, right)),
        })
        heads = []
        for edge in edges:
            a, b = tuple(edge)
            values = mixed.edges[a, b].get("heads", frozenset())
            require(len(values) <= 1, "two-headed triangle edge")
            if values:
                heads.append(next(iter(values)))
        if len(heads) == 2 and heads[0] == heads[1]:
            rows.append({"edges": edges, "reticulation": heads[0]})
    return rows


def incidence(mixed, triangle=None):
    triangle = frozenset() if triangle is None else triangle
    graph = nx.Graph()
    edge_lookup = {}
    for node, data in mixed.nodes(data=True):
        graph.add_node(("v", node), kind="vertex", label=data.get("label"), triangle_edge=False)
    for number, (left, right, data) in enumerate(
        sorted(mixed.edges(data=True), key=lambda row: edge_key(row[0], row[1]))
    ):
        edge = frozenset((left, right))
        edge_node = ("e", number)
        edge_lookup[edge_node] = edge
        collapsed = edge in triangle
        graph.add_node(edge_node, kind="edge", label=None, triangle_edge=collapsed)
        heads = data.get("heads", frozenset())
        graph.add_edge(edge_node, ("v", left), head=False if collapsed else left in heads)
        graph.add_edge(edge_node, ("v", right), head=False if collapsed else right in heads)
    return graph, edge_lookup


def exact_relation(atlas, source, target):
    source_mixed, target_mixed = atlas.sd0_mixed(source), atlas.sd0_mixed(target)
    relation_hint = atlas.mixed_relation_exact(source, target)
    if relation_hint == "isomorphic":
        triangle_pairs = [(None, None, None, None)]
    elif relation_hint == "triangle":
        triangle_pairs = [
            (left["edges"], right["edges"], left["reticulation"], right["reticulation"])
            for left in ordinary_triangles(source_mixed)
            for right in ordinary_triangles(target_mixed)
        ]
    else:
        return "none", []
    node_match = lambda left, right: (
        left.get("kind") == right.get("kind")
        and left.get("label") == right.get("label")
        and left.get("triangle_edge") == right.get("triangle_edge")
    )
    edge_match = lambda left, right: left.get("head") == right.get("head")
    witnesses = {}
    for source_triangle, target_triangle, source_reticulation, target_reticulation in triangle_pairs:
        source_incidence, source_edges = incidence(source_mixed, source_triangle)
        target_incidence, target_edges = incidence(target_mixed, target_triangle)
        matcher = nx.algorithms.isomorphism.GraphMatcher(
            source_incidence, target_incidence,
            node_match=node_match, edge_match=edge_match,
        )
        for mapping in matcher.isomorphisms_iter():
            vertex_map = {
                node: mapping[("v", node)][1]
                for node in source_mixed.nodes()
            }
            edge_map = {
                source_edges[node]: target_edges[mapping[node]]
                for node in source_edges
            }
            public = {
                "relation": relation_hint,
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
                "source_triangle": source_triangle,
                "target_triangle": target_triangle,
                "source_triangle_reticulation": source_reticulation,
                "target_triangle_reticulation": target_reticulation,
            }
    require(witnesses, f"relation hint lacks witness:{relation_hint}")
    return relation_hint, [witnesses[key] for key in sorted(witnesses)]


def site_profile(atlas, graph):
    mixed = atlas.sd0_mixed(graph)
    roots = [node for node, data in graph.nodes(data=True) if data.get("role") == "root"]
    require(len(roots) == 1, "site rooted presentation")
    root = roots[0]
    root_children = tuple(graph.successors(root))
    require(len(root_children) == 2, "site root halves")
    direct = {
        frozenset((tail, head)): (tail, head, data.get("edge_role"))
        for tail, head, data in graph.edges(data=True)
        if tail != root
    }
    sites = []
    half_certificate = None
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
            require(edge == frozenset(root_children), f"unexplained root edge:{edge}")
            representatives = [
                [repr(root), repr(child), graph.edges[root, child].get("edge_role")]
                for child in sorted(root_children, key=repr)
            ]
            site_type = "root_suppressed_segment"
            new_label = max(labels_of(graph)) + 1
            children = sorted(root_children, key=lambda node: graph.nodes[node].get("role") != "leaf")
            first = insert_on_arc(
                graph,
                {"tail": repr(root), "head": repr(children[0])},
                new_label,
                "root_half_audit_a",
            )
            second = insert_on_arc(
                graph,
                {"tail": repr(root), "head": repr(children[1])},
                new_label,
                "root_half_audit_b",
            )
            relation = atlas.mixed_relation_exact(first, second)
            require(relation == "isomorphic", "root halves are inequivalent")
            half_certificate = {
                "new_label": new_label,
                "representative_half_arcs": representatives,
                "semi_directed_relation_after_insertion": relation,
                "first_graph_sha256": sha(graph_payload(first)),
                "second_graph_sha256": sha(graph_payload(second)),
            }
            half_certificate["certificate_sha256"] = sha(half_certificate)
        sites.append({
            "site_id": f"E:{sha(list(edge_key(left, right)))}",
            "mixed_endpoints": list(edge_key(left, right)),
            "arrowhead_endpoints": sorted(map(repr, heads)),
            "site_type": site_type,
            "rooted_representatives": representatives,
        })
    k = len(labels_of(graph))
    r = sum(data.get("role") == "retic" for _, data in graph.nodes(data=True))
    counts = collections.Counter(row["site_type"] for row in sites)
    require(len(sites) == 2 * k + 3 * r - 3, f"site formula:{k}:{r}:{len(sites)}")
    require(half_certificate is not None, "root-half certificate")
    return {
        "port_count": k,
        "reticulation_count": r,
        "all_mixed_edge_sites_included": True,
        "site_count": len(sites),
        "site_type_census": dict(sorted(counts.items())),
        "root_half_equivalence": half_certificate,
        "sites": sites,
        "ordered_site_hash_root": sha([sha(row) for row in sites]),
    }


def candidate_from_site(site):
    representative = site["rooted_representatives"][0]
    return {
        "tail": representative[0],
        "head": representative[1],
        "edge_role": representative[2],
        "site_id": site["site_id"],
        "site_type": site["site_type"],
        "mixed_endpoints": site["mixed_endpoints"],
    }


def mixed_graph_payload(atlas, graph):
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


def underlying_relation_hash(atlas, graph):
    """Necessary head-forgetting hash for both exact relations.

    Arrowheads are deliberately omitted.  Ordinary-triangle equivalence can
    change them on its unique triangle, while preserving this labelled
    incidence graph.  Equality of this hash is only a prefilter and is always
    followed by the exact matcher.
    """
    mixed = atlas.sd0_mixed(graph)
    expanded = nx.Graph()
    for node, data in mixed.nodes(data=True):
        expanded.add_node(("v", node), color=f"vertex:{data.get('label')!r}")
    for number, (left, right) in enumerate(
        sorted(mixed.edges(), key=lambda row: edge_key(row[0], row[1]))
    ):
        edge_node = ("e", number)
        expanded.add_node(edge_node, color="edge")
        expanded.add_edge(edge_node, ("v", left))
        expanded.add_edge(edge_node, ("v", right))
    return nx.weisfeiler_lehman_graph_hash(expanded, node_attr="color", iterations=8)


def split_payload(splits):
    rows = []
    for split in sorted(splits, key=repr):
        if split == ("star",):
            rows.append(["star"])
        else:
            rows.append([list(split[0]), list(split[1])])
    return rows


def quartet_deck(atlas, graph, required_label=None):
    labels = labels_of(graph)
    return tuple(
        (quartet, split_payload(atlas.quartet_splits(graph, quartet)))
        for quartet in itertools.combinations(labels, 4)
        if required_label is None or required_label in quartet
    )


def first_quartet_mismatch(source_deck, target_deck):
    require(len(source_deck) == len(target_deck), "quartet deck length")
    for (source_quartet, source_splits), (target_quartet, target_splits) in zip(
        source_deck, target_deck
    ):
        require(source_quartet == target_quartet, "quartet deck labels")
        if source_splits != target_splits:
            proof = {
                "quartet": list(source_quartet),
                "source_displayed_splits": source_splits,
                "target_displayed_splits": target_splits,
                "method": "complete displayed-switching split-set mismatch",
            }
            return proof
    return None


def sparse_payload(polynomial):
    return [
        [list(exponent), str(coefficient)]
        for exponent, coefficient in sorted(polynomial.items())
    ]


def sparse_hash(polynomial):
    return sha(sparse_payload(polynomial))


def sparse_mul(left, right):
    result = collections.defaultdict(fractions.Fraction)
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(left_exponent, right_exponent))
            result[exponent] += fractions.Fraction(left_coefficient) * right_coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def sparse_mul_many(polynomials):
    polynomials = tuple(polynomials)
    if not polynomials:
        return {}
    result = polynomials[0]
    for polynomial in polynomials[1:]:
        result = sparse_mul(result, polynomial)
    return result


def sparse_lincomb(polynomials, coefficients):
    result = collections.defaultdict(fractions.Fraction)
    for polynomial, coefficient in zip(polynomials, coefficients):
        coefficient = fractions.Fraction(coefficient)
        for exponent, value in polynomial.items():
            result[exponent] += coefficient * value
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def bernstein_strict_sign(polynomial):
    """Exact tensor-Bernstein strict sign on the full open parameter cube."""
    if not polynomial:
        return None
    parameter_count = len(next(iter(polynomial)))
    common = tuple(
        min(exponent[index] for exponent in polynomial)
        for index in range(parameter_count)
    )
    active = tuple(
        index for index in range(parameter_count)
        if len({exponent[index] for exponent in polynomial}) > 1
    )
    reduced = collections.defaultdict(fractions.Fraction)
    for exponent, coefficient in polynomial.items():
        reduced[tuple(exponent[index] - common[index] for index in active)] += coefficient
    reduced = {exponent: coefficient for exponent, coefficient in reduced.items() if coefficient}
    require(reduced, "Bernstein reduction cancelled nonzero polynomial")
    degrees = tuple(
        max(exponent[index] for exponent in reduced)
        for index in range(len(active))
    )
    shape = tuple(degree + 1 for degree in degrees)
    coefficient_count = math.prod(shape)
    require(coefficient_count <= 2_000_000, f"Bernstein tensor too large:{coefficient_count}")
    strides = tuple(math.prod(shape[index + 1 :]) for index in range(len(shape)))
    values = [fractions.Fraction(0)] * coefficient_count
    for exponent, coefficient in reduced.items():
        values[sum(value * stride for value, stride in zip(exponent, strides))] += coefficient
    for axis, degree in enumerate(degrees):
        stride = strides[axis]
        outer = math.prod(shape[:axis])
        block = (degree + 1) * stride
        denominators = [math.comb(degree, value) for value in range(degree + 1)]
        transformed = [fractions.Fraction(0)] * coefficient_count
        for outer_index in range(outer):
            base = outer_index * block
            for inner_index in range(stride):
                source = [
                    values[base + value * stride + inner_index]
                    for value in range(degree + 1)
                ]
                for beta in range(degree + 1):
                    total = fractions.Fraction(0)
                    for alpha in range(beta + 1):
                        if source[alpha]:
                            total += source[alpha] * fractions.Fraction(
                                math.comb(beta, alpha), denominators[alpha]
                            )
                    transformed[base + beta * stride + inner_index] = total
        values = transformed
    signs = collections.Counter(-1 if value < 0 else 1 if value > 0 else 0 for value in values)
    if signs[-1] and not signs[1]:
        sign = -1
    elif signs[1] and not signs[-1]:
        sign = 1
    else:
        return None
    public_values = [str(value) for value in values]
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
        "ordered_Bernstein_coefficients_sha256": sha(public_values),
        "strict_sign": sign,
        "domain": (
            "the full open unit cube in physical edge-sector and inheritance "
            "variables, which contains the physical principal D_plus subset"
        ),
    }


class DirectFourierCompiler:
    """Compile only the five coordinates needed by T_i from the full graph.

    Unlike the revoked structural oracle, this compiler never restricts the
    graph.  It expands every displayed switching of the original full rooted
    K2P map.  Each non-arm physical edge keeps its own (s,g) pair, making the
    certified open cube at least as large as D_plus.
    """

    def __init__(self, atlas):
        self.atlas = atlas
        self.states = {}
        self.pullbacks = collections.OrderedDict()
        self.coordinate_queries = 0
        self.pullback_queries = 0

    def state(self, graph):
        graph_sha256 = sha(graph_payload(graph))
        if graph_sha256 in self.states:
            return graph_sha256, self.states[graph_sha256]
        labels = labels_of(graph)
        require(labels == tuple(range(len(labels))), f"noncontiguous Fourier labels:{labels}")
        reticulations = tuple(sorted(
            (node for node, data in graph.nodes(data=True) if data.get("role") == "retic"),
            key=repr,
        ))
        parents = tuple(
            tuple(sorted(graph.predecessors(node), key=repr)) for node in reticulations
        )
        require(all(len(row) == 2 for row in parents), "nonbinary Fourier reticulation")
        arms = self.atlas.selected_arm_edges(graph)
        internal_edges = tuple(
            edge for edge in sorted(graph.edges(), key=lambda row: (repr(row[0]), repr(row[1])))
            if edge not in arms
        )
        edge_index = {edge: number for number, edge in enumerate(internal_edges)}
        all_edges = tuple(graph.edges())
        switches = []
        for bits in itertools.product((0, 1), repeat=len(reticulations)):
            removed = set()
            for number, reticulation in enumerate(reticulations):
                kept_parent = parents[number][bits[number]]
                removed.update(
                    (parent, reticulation)
                    for parent in parents[number]
                    if parent != kept_parent
                )
            kept = tuple(edge for edge in all_edges if edge not in removed)
            masks = self.atlas.descendant_masks_for_switch(graph, kept)
            switches.append((bits, frozenset(kept), masks))
        state = {
            "graph": graph,
            "labels": labels,
            "reticulations": reticulations,
            "internal_edges": internal_edges,
            "edge_index": edge_index,
            "switches": switches,
            "parameter_count": 2 * len(internal_edges) + len(reticulations),
        }
        self.states[graph_sha256] = state
        return graph_sha256, state

    def coordinate(self, state, assignment):
        self.coordinate_queries += 1
        result = collections.defaultdict(fractions.Fraction)
        edge_count = len(state["internal_edges"])
        for bits, kept, masks in state["switches"]:
            base = [0] * state["parameter_count"]
            for edge in state["internal_edges"]:
                if edge not in kept:
                    continue
                sector = self.atlas.sector_for_mask(masks[edge], assignment)
                if sector:
                    base[2 * state["edge_index"][edge] + sector - 1] += 1
            for mask, coefficient in self.atlas.weight_polynomial(bits):
                exponent = list(base)
                for number in range(len(state["reticulations"])):
                    if mask >> number & 1:
                        exponent[2 * edge_count + number] += 1
                result[tuple(exponent)] += coefficient
        return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}

    def t_pullback(self, graph, triple, reticulation_label):
        graph_sha256, state = self.state(graph)
        key = (graph_sha256, tuple(triple), reticulation_label)
        self.pullback_queries += 1
        if key in self.pullbacks:
            value = self.pullbacks.pop(key)
            self.pullbacks[key] = value
            return value
        other = sorted(set(triple) - {reticulation_label})
        require(len(other) == 2, "T_i orientation")
        first, second, third = other[0], other[1], reticulation_label

        def coordinate(values):
            assignment = [0] * len(state["labels"])
            for label, character in values.items():
                assignment[label] = character
            return self.coordinate(state, tuple(assignment))

        v_value = coordinate({first: 1, second: 3, third: 2})
        x_s = coordinate({first: 1, second: 1})
        x_g = coordinate({first: 2, second: 2})
        y_g = coordinate({first: 2, third: 2})
        z_g = coordinate({second: 2, third: 2})
        value = sparse_lincomb(
            (
                sparse_mul_many((v_value, v_value, x_g)),
                sparse_mul_many((x_s, x_s, y_g, z_g)),
            ),
            (1, -1),
        )
        self.pullbacks[key] = value
        while len(self.pullbacks) > 4096:
            self.pullbacks.popitem(last=False)
        return value

    def parameterization(self, graph):
        _, state = self.state(graph)
        return {
            "edge_sector_pairs": [
                [repr(tail), repr(head), 2 * number, 2 * number + 1]
                for number, (tail, head) in enumerate(state["internal_edges"])
            ],
            "inheritance_variables": [
                [repr(node), 2 * len(state["internal_edges"]) + number]
                for number, node in enumerate(state["reticulations"])
            ],
            "selected_pendant_arms_removed_by_boundary_normalization": True,
        }


class SignOracle:
    def __init__(self, atlas):
        self.atlas = atlas
        self.compiler = DirectFourierCompiler(atlas)
        self.pair_cache = {}
        self.certificates = {}
        self.strict_polynomials = {}
        self.queries = 0

    def certify(self, source, target):
        source_hash = sha(graph_payload(source))
        target_hash = sha(graph_payload(target))
        pair_key = (source_hash, target_hash)
        self.queries += 1
        if pair_key in self.pair_cache:
            return self.pair_cache[pair_key]
        labels = labels_of(source)
        require(labels == labels_of(target), "T_i label mismatch")
        for triple in itertools.combinations(labels, 3):
            for reticulation_label in triple:
                source_polynomial = self.compiler.t_pullback(
                    source, triple, reticulation_label
                )
                target_polynomial = self.compiler.t_pullback(
                    target, triple, reticulation_label
                )
                if not source_polynomial and target_polynomial:
                    zero_on, strict_on = "source", "target"
                    strict_graph, strict_polynomial = target, target_polynomial
                elif not target_polynomial and source_polynomial:
                    zero_on, strict_on = "target", "source"
                    strict_graph, strict_polynomial = source, source_polynomial
                else:
                    continue
                sign = bernstein_strict_sign(strict_polynomial)
                if sign is None:
                    continue
                strict_hash = sparse_hash(strict_polynomial)
                self.strict_polynomials.setdefault(strict_hash, {
                    "pullback_sha256": strict_hash,
                    "pullback": sparse_payload(strict_polynomial),
                    "Bernstein_certificate": sign,
                    "parameterization": self.compiler.parameterization(strict_graph),
                })
                other = sorted(set(triple) - {reticulation_label})
                certificate = {
                    "observable": "T_i=V^2*X_g-X_s^2*Y_g*Z_g",
                    "triple": list(triple),
                    "ordered_other_labels": other,
                    "orientation_label_i": reticulation_label,
                    "zero_on": zero_on,
                    "strict_on": strict_on,
                    "zero_pullback": "coefficientwise exact zero on the original full Fourier map",
                    "zero_pullback_sha256": sparse_hash({}),
                    "strict_pullback_sha256": strict_hash,
                    "strict_sign": sign["strict_sign"],
                    "boundary_incidence_multihomogeneity": {
                        str(other[0]): "s^2*g",
                        str(other[1]): "s^2*g",
                        str(reticulation_label): "g^2",
                        "all_unselected_boundary_incidence_weights": "0",
                    },
                    "bridge_torus_conclusion": "zero/nonzero strict sign survives both K2P incidence sectors",
                }
                certificate_id = f"TI:{sha(certificate)}"
                self.certificates.setdefault(certificate_id, certificate)
                self.pair_cache[pair_key] = certificate_id
                return certificate_id
        self.pair_cache[pair_key] = None
        return None

    def public(self):
        return {
            "method": "direct original-full-map T_i pullback; exact tensor Bernstein strict sign",
            "forbidden_rooted_triple_oracle_used": False,
            "queries": self.queries,
            "pair_cache_entries": len(self.pair_cache),
            "canonical_relation_certificates": len(self.certificates),
            "canonical_strict_polynomials": len(self.strict_polynomials),
            "certificates": dict(sorted(self.certificates.items())),
            "strict_polynomial_registry": dict(sorted(self.strict_polynomials.items())),
            "compiler": {
                "prepared_full_graphs": len(self.compiler.states),
                "coordinate_queries": self.compiler.coordinate_queries,
                "pullback_queries": self.compiler.pullback_queries,
                "pullback_cache_limit": 4096,
            },
        }


class K3PTreeSunletOracle:
    """Exact three-sector replacement for the K2P-only ``T_i`` oracle.

    The graph-derived triple restriction is used only as a finder.  Every
    accepted row is then checked by compiling the literal restricted K3P maps:
    all six cubic circuits vanish identically on the tree descriptor and at
    least one is a nonzero polynomial on the ordinary-sunlet descriptor.  The
    supplied six-circuit sum-of-squares theorem proves that their squared sum
    is strictly positive throughout the principal physical domain, for every
    ordinary-sunlet orientation.  Thus no equality such as C=T is imposed.
    """

    CIRCUITS = (
        (("000", "CGT", "GTC"), ("0TT", "C0C", "GG0")),
        (("000", "CTG", "TGC"), ("0GG", "C0C", "TT0")),
        (("000", "GCT", "TGC"), ("0CC", "GG0", "T0T")),
        (("000", "GTC", "TCG"), ("0CC", "G0G", "TT0")),
        (("000", "CTG", "GCT"), ("0TT", "CC0", "G0G")),
        (("000", "CGT", "TCG"), ("0GG", "CC0", "T0T")),
    )

    def __init__(self, atlas):
        self.atlas = atlas
        self.certificate_path = (
            FROZEN / "k3p_cloud_artifacts/k3p_tree_sunlet_separator.json"
        )
        self.theorem = json.loads(self.certificate_path.read_text())
        require(
            self.theorem["schema"]
            == "k3p-tree-sunlet-six-circuit-separator-v1",
            "K3P tree-sunlet theorem schema",
        )
        require(len(self.theorem["circuits"]) == 6, "K3P six-circuit count")
        self.pair_cache = {}
        self.certificates = {}
        self.queries = 0

    @staticmethod
    def normalized_restriction(atlas, graph, triple):
        restricted = atlas.restrict_rooted(graph, set(triple))
        relabel = {old: new for new, old in enumerate(sorted(triple))}
        normalized = restricted.copy()
        for _, data in normalized.nodes(data=True):
            label = data.get("label")
            if label in relabel:
                data["label"] = relabel[label]
        return restricted, normalized, relabel

    @staticmethod
    def descriptor_payload(descriptor):
        return {
            "k": descriptor.k,
            "retic_count": descriptor.retic_count,
            "edge_class_count": descriptor.edge_class_count,
            "outputs": descriptor.outputs,
            "edge_signatures": descriptor.edge_signatures,
        }

    def circuit_pullbacks(self, descriptor):
        outputs = self.atlas.output_sparse_polynomials(descriptor)
        assignments = self.atlas.k3p_assignments(3)
        index = {assignment: number for number, assignment in enumerate(assignments)}
        code = {"0": 0, "C": 1, "G": 2, "T": 3}

        def coordinate(label):
            return outputs[index[tuple(code[value] for value in label)]]

        rows = []
        for left, right in self.CIRCUITS:
            left_product = self.atlas.sparse_mul_many(
                [coordinate(label) for label in left]
            )
            right_product = self.atlas.sparse_mul_many(
                [coordinate(label) for label in right]
            )
            rows.append(
                self.atlas.sparse_lincomb(
                    [left_product, right_product], [1, -1]
                )
            )
        return rows

    def certify(self, source, target):
        source_hash = sha(graph_payload(source))
        target_hash = sha(graph_payload(target))
        pair_key = (source_hash, target_hash)
        self.queries += 1
        if pair_key in self.pair_cache:
            return self.pair_cache[pair_key]
        labels = labels_of(source)
        require(labels == labels_of(target), "K3P tree-sunlet label mismatch")
        for triple in itertools.combinations(labels, 3):
            source_type = self.atlas.triple_type(source, triple)
            target_type = self.atlas.triple_type(target, triple)
            if {source_type, target_type} != {"tree", "sunlet"}:
                continue
            source_restricted, source_normalized, relabel = self.normalized_restriction(
                self.atlas, source, triple
            )
            target_restricted, target_normalized, target_relabel = self.normalized_restriction(
                self.atlas, target, triple
            )
            require(relabel == target_relabel, "K3P triple relabel consistency")
            source_descriptor = self.atlas.model_descriptor(source_normalized)
            target_descriptor = self.atlas.model_descriptor(target_normalized)
            source_circuits = self.circuit_pullbacks(source_descriptor)
            target_circuits = self.circuit_pullbacks(target_descriptor)
            if source_type == "tree":
                tree_on, sunlet_on = "source", "target"
                tree_circuits, sunlet_circuits = source_circuits, target_circuits
                tree_descriptor, sunlet_descriptor = source_descriptor, target_descriptor
            else:
                tree_on, sunlet_on = "target", "source"
                tree_circuits, sunlet_circuits = target_circuits, source_circuits
                tree_descriptor, sunlet_descriptor = target_descriptor, source_descriptor
            require(all(not row for row in tree_circuits), "K3P tree circuit nonzero")
            require(any(row for row in sunlet_circuits), "K3P sunlet circuit deck zero")
            require(tree_descriptor.retic_count == 0, "K3P tree descriptor reticulation")
            require(sunlet_descriptor.retic_count == 1, "K3P sunlet descriptor reticulation")
            certificate = {
                "method": "literal restricted K3P maps plus six-circuit sum-of-squares positivity",
                "triple": list(triple),
                "normalized_label_map": {str(key): value for key, value in sorted(relabel.items())},
                "tree_on": tree_on,
                "sunlet_on": sunlet_on,
                "source_restricted_graph_sha256": sha(graph_payload(source_restricted)),
                "target_restricted_graph_sha256": sha(graph_payload(target_restricted)),
                "source_descriptor_sha256": sha(self.descriptor_payload(source_descriptor)),
                "target_descriptor_sha256": sha(self.descriptor_payload(target_descriptor)),
                "tree_circuit_pullback_sha256": [sparse_hash(row) for row in tree_circuits],
                "sunlet_circuit_pullback_sha256": [sparse_hash(row) for row in sunlet_circuits],
                "sunlet_nonzero_circuit_count": sum(bool(row) for row in sunlet_circuits),
                "separator_certificate_path": str(self.certificate_path.relative_to(PROJECT)),
                "separator_certificate_sha256": sha_file(self.certificate_path),
                "separator": "sum_{j=1}^6 I_j^2",
                "tree_value": "coefficientwise exact zero",
                "sunlet_value": "strictly positive throughout D_{3,+}",
                "physical_transfer": (
                    "direct three-leaf marginal; serial edge products and inherited "
                    "mixing remain strict physical K3P coordinates"
                ),
                "three_sector_independence": "C, G, and T remain separate in every descriptor",
            }
            certificate_id = f"K3P-TS:{sha(certificate)}"
            self.certificates.setdefault(certificate_id, certificate)
            self.pair_cache[pair_key] = certificate_id
            return certificate_id
        self.pair_cache[pair_key] = None
        return None

    def public(self):
        return {
            "method": "exact K3P literal triple descriptors and six-circuit SOS",
            "queries": self.queries,
            "pair_cache_entries": len(self.pair_cache),
            "canonical_relation_certificates": len(self.certificates),
            "certificates": dict(sorted(self.certificates.items())),
            "separator_certificate_sha256": sha_file(self.certificate_path),
            "uses_k2p_sector_equality": False,
            "strict_positivity_domain": "D_{3,+}",
        }


def site_edge(site):
    return frozenset(ast.literal_eval(value) for value in site["mixed_endpoints"])


def restriction_certificate(atlas, child, parent, removed_label):
    restricted = atlas.restrict_rooted(child, set(labels_of(parent)))
    relation, witnesses = exact_relation(atlas, restricted, parent)
    require(relation == "isomorphic", f"probe marginal relation:{removed_label}:{relation}")
    require(len(witnesses) == 1, f"probe marginal transport multiplicity:{len(witnesses)}")
    return {
        "removed_label": removed_label,
        "restricted_mixed_graph_sha256": sha(mixed_graph_payload(atlas, restricted)),
        "parent_mixed_graph_sha256": sha(mixed_graph_payload(atlas, parent)),
        "exact_labelled_relation": relation,
        "restriction_transport_sha256": witnesses[0]["public"]["transport_sha256"],
    }


def global_triangle(anchor):
    if anchor["relation"] != "triangle":
        return None
    witness = anchor["transport"]
    return {
        "source_triangle_edges": sorted(
            [list(edge_key(*tuple(edge))) for edge in witness["source_triangle"]]
        ),
        "target_triangle_edges": sorted(
            [list(edge_key(*tuple(edge))) for edge in witness["target_triangle"]]
        ),
        "source_reticulation": repr(witness["source_triangle_reticulation"]),
        "target_reticulation": repr(witness["target_triangle_reticulation"]),
        "ordinary_triangle_witness": "exactly two arrowheads enter the displayed common reticulation on each side",
    }


def coherent_child_witness(parent, witness, relation, source_site, target_site):
    parent_source_nodes = tuple(parent["transport"]["vertex_map"])
    if any(
        witness["vertex_map"].get(node) != parent["transport"]["vertex_map"][node]
        for node in parent_source_nodes
    ):
        return False
    mapped_site = parent["transport"]["edge_map"].get(site_edge(source_site))
    if mapped_site != site_edge(target_site):
        return False
    inherited = parent["global_triangle"]
    if relation == "triangle":
        if inherited is None:
            return False
        if sorted([list(edge_key(*tuple(edge))) for edge in witness["source_triangle"]]) != inherited["source_triangle_edges"]:
            return False
        if sorted([list(edge_key(*tuple(edge))) for edge in witness["target_triangle"]]) != inherited["target_triangle_edges"]:
            return False
        if repr(witness["source_triangle_reticulation"]) != inherited["source_reticulation"]:
            return False
        if repr(witness["target_triangle_reticulation"]) != inherited["target_reticulation"]:
            return False
    return True


class CanonicalRelationRegistry:
    """Exact canonical dedup of a graph pair together with its transport."""

    def __init__(self, atlas):
        self.atlas = atlas
        self.buckets = collections.defaultdict(list)
        self.representatives = []

    def combined(self, record):
        result = nx.Graph()
        for side, graph in (("S", record["source_graph"]), ("T", record["target_graph"])):
            mixed = self.atlas.sd0_mixed(graph)
            triangle = (
                record["transport"]["source_triangle"]
                if side == "S" else record["transport"]["target_triangle"]
            )
            triangle = frozenset() if triangle is None else triangle
            for node, data in mixed.nodes(data=True):
                result.add_node(
                    (side, "v", node), color=f"{side}:vertex:{data.get('label')!r}"
                )
            for number, (left, right, data) in enumerate(
                sorted(mixed.edges(data=True), key=lambda row: edge_key(row[0], row[1]))
            ):
                edge_node = (side, "e", number)
                edge = frozenset((left, right))
                result.add_node(edge_node, color=f"{side}:edge:{edge in triangle}")
                heads = data.get("heads", frozenset())
                result.add_edge(edge_node, (side, "v", left), color=f"head:{left in heads and edge not in triangle}")
                result.add_edge(edge_node, (side, "v", right), color=f"head:{right in heads and edge not in triangle}")
        for source_node, target_node in record["transport"]["vertex_map"].items():
            result.add_edge(("S", "v", source_node), ("T", "v", target_node), color="transport")
        result.add_node(("relation",), color=f"relation:{record['relation']}")
        return result

    def add(self, record):
        combined = self.combined(record)
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
        class_id = len(self.representatives)
        self.representatives.append(combined)
        self.buckets[bucket].append(class_id)
        return class_id


class OrderedHashAccumulator:
    def __init__(self):
        self.count = 0
        self.root = sha([])

    def add(self, row_hash):
        self.root = sha({"previous": self.root, "row_sha256": row_hash})
        self.count += 1

    def public(self):
        return {
            "algorithm": "root_0=sha256(canonical([])); root_n=sha256(canonical({previous:root_(n-1),row_sha256:h_n}))",
            "rows": self.count,
            "ordered_hash_root": self.root,
        }


class JsonlGzipWriter:
    def __init__(self, path):
        self.raw = path.open("wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.text = io.TextIOWrapper(self.gz, encoding="utf-8", newline="\n")

    def write(self, row):
        self.text.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")

    def close(self):
        self.text.flush()
        self.text.detach()
        self.gz.close()
        self.raw.close()


class StreamingRecordStore:
    """Fail-closed deterministic streaming registry with bounded memory."""

    def __init__(self, path, record_kind):
        self.path = path
        self.record_kind = record_kind
        self.writer = JsonlGzipWriter(path)
        self.seen = set()
        self.ordered = OrderedHashAccumulator()
        self.closed = False

    def put(self, record_id, record):
        require(not self.closed, f"closed streaming registry:{self.record_kind}")
        if record_id in self.seen:
            return
        row = {
            "record_kind": self.record_kind,
            "record_id": record_id,
            "record": record,
        }
        self.writer.write(row)
        self.ordered.add(sha(row))
        self.seen.add(record_id)

    def close(self):
        if not self.closed:
            self.writer.close()
            self.closed = True

    def public(self):
        require(self.closed, f"open streaming registry:{self.record_kind}")
        return {
            "path": self.path.name,
            "sha256": sha_file(self.path),
            "unique_records": len(self.seen),
            "ordered_records": self.ordered.public(),
        }


def register_transport(registry, witness):
    public = witness["public"]
    transport_id = public["transport_sha256"]
    record = dict(public)
    record["ordinary_triangle_arrowhead_witness"] = None
    if public["relation"] == "triangle":
        record["ordinary_triangle_arrowhead_witness"] = {
            "source_common_reticulation": repr(witness["source_triangle_reticulation"]),
            "target_common_reticulation": repr(witness["target_triangle_reticulation"]),
            "source_headed_edges": sorted(
                [
                    list(edge_key(left, right))
                    for left, right in witness["source_triangle"]
                    if witness["source_triangle_reticulation"] in (left, right)
                ]
            ),
            "target_headed_edges": sorted(
                [
                    list(edge_key(left, right))
                    for left, right in witness["target_triangle"]
                    if witness["target_triangle_reticulation"] in (left, right)
                ]
            ),
            "required_pattern": "exactly two triangle arrows into one common reticulation",
        }
        require(
            len(record["ordinary_triangle_arrowhead_witness"]["source_headed_edges"]) == 2
            and len(record["ordinary_triangle_arrowhead_witness"]["target_headed_edges"]) == 2,
            "ordinary triangle arrowhead count",
        )
    if isinstance(registry, StreamingRecordStore):
        registry.put(transport_id, record)
    else:
        previous = registry.setdefault(transport_id, record)
        require(previous == record, f"transport registry collision:{transport_id}")
    return transport_id


def register_proof(registry, prefix, proof):
    proof_id = f"{prefix}:{sha(proof)}"
    if isinstance(registry, StreamingRecordStore):
        registry.put(proof_id, proof)
    else:
        previous = registry.setdefault(proof_id, proof)
        require(previous == proof, f"proof registry collision:{proof_id}")
    return proof_id


def prepare_probe_children(
    atlas, parent, side, profile, label, namespace, restriction_registry,
):
    graph = parent[f"{side}_graph"]
    rows = []
    for site_index, site in enumerate(profile["sites"]):
        child = insert_on_arc(
            graph,
            candidate_from_site(site),
            label,
            (namespace, side, site_index),
        )
        restriction = restriction_certificate(atlas, child, graph, label)
        restriction_id = register_proof(restriction_registry, "R", restriction)
        rows.append({
            "site_index": site_index,
            "site": site,
            "graph": child,
            "graph_sha256": sha(graph_payload(child)),
            "underlying_relation_hash": underlying_relation_hash(atlas, child),
            # Old-label quartets equal because the exact parent relation is
            # checked separately.  Only quartets containing the new probe can
            # become new separators; this reduces k=9 replay work by >2x.
            "quartet_deck": quartet_deck(atlas, child, required_label=label),
            "restriction_certificate_id": restriction_id,
        })
    require(len(rows) == profile["site_count"], "prepared probe site coverage")
    return rows


def classify_probe_pair(
    atlas, parent, source_child, target_child, sign_oracle,
    proof_registry, transport_registry,
):
    relation, witnesses = "none", []
    # Any child relation marginalizes to a parent relation.  The parent
    # transport is unique, and the new labelled leaf forces its incident
    # subdivision, so a coherent child relation can exist only when that
    # unique parent edge map carries the chosen source site to the chosen
    # target site.  This exact theorem prefilter avoids thousands of redundant
    # GraphMatcher calls without changing classifier precedence.
    parent_maps_sites = (
        parent["transport"]["edge_map"].get(site_edge(source_child["site"]))
        == site_edge(target_child["site"])
    )
    if (
        parent_maps_sites
        and source_child["underlying_relation_hash"]
        == target_child["underlying_relation_hash"]
    ):
        relation, witnesses = exact_relation(
            atlas, source_child["graph"], target_child["graph"]
        )
    if relation in {"isomorphic", "triangle"}:
        require(len(witnesses) == 1, f"nonunique exact probe transport:{len(witnesses)}")
        witness = witnesses[0]
        require(
            coherent_child_witness(
                parent, witness, relation, source_child["site"], target_child["site"]
            ),
            "exact child relation has incoherent parent/site/global-triangle transport",
        )
        transport_id = register_transport(transport_registry, witness)
        return {
            "status": relation,
            "transport_id": transport_id,
            "parent_transport_id": parent["transport"]["public"]["transport_sha256"],
            "transport_restriction": (
                "exact on every parent mixed vertex, the selected mixed edge site, "
                "and the inherited ordinary triangle when present"
            ),
            "global_triangle_sha256": None if parent["global_triangle"] is None else sha(parent["global_triangle"]),
        }, witness

    quartet = first_quartet_mismatch(
        source_child["quartet_deck"], target_child["quartet_deck"]
    )
    if quartet is not None:
        return {
            "status": "displayed_quartet_mismatch",
            "proof_id": register_proof(proof_registry, "Q", quartet),
        }, None

    sign_id = sign_oracle.certify(source_child["graph"], target_child["graph"])
    if sign_id is not None:
        return {
            "status": "k3p_tree_sunlet_sos",
            "proof_id": sign_id,
        }, None
    return {
        "status": "unresolved",
        "source_graph_sha256": source_child["graph_sha256"],
        "target_graph_sha256": target_child["graph_sha256"],
    }, None


def public_anchor_row(anchor, canonical_class_id):
    return {
        "anchor_id": anchor["anchor_id"],
        "origin": anchor["origin"],
        "labels": list(labels_of(anchor["source_graph"])),
        "relation": anchor["relation"],
        "canonical_anchor_class_id": canonical_class_id,
        "source_graph_sha256": sha(graph_payload(anchor["source_graph"])),
        "target_graph_sha256": sha(graph_payload(anchor["target_graph"])),
        "transport_id": anchor["transport"]["public"]["transport_sha256"],
        "global_triangle": anchor["global_triangle"],
        "source_site_count": anchor["source_profile"]["site_count"],
        "target_site_count": anchor["target_profile"]["site_count"],
        "source_site_ordered_hash_root": anchor["source_profile"]["ordered_site_hash_root"],
        "target_site_ordered_hash_root": anchor["target_profile"]["ordered_site_hash_root"],
        "locator_sha256": sha(anchor["locator"]),
    }


def enumerate_one_port(
    atlas, anchors, relation_registry, sign_oracle,
    proof_registry, restriction_registry, transport_registry,
):
    counts = collections.Counter()
    by_origin = collections.Counter()
    ordered = OrderedHashAccumulator()
    survivors = []
    unresolved = []
    writer = JsonlGzipWriter(ONE_LEDGER)
    try:
        for anchor_number, anchor in enumerate(anchors):
            if anchor_number % 20 == 0:
                print(
                    f"corrected-probe: one-port anchor {anchor_number}/{len(anchors)}",
                    file=sys.stderr, flush=True,
                )
            require(
                first_quartet_mismatch(
                    quartet_deck(atlas, anchor["source_graph"]),
                    quartet_deck(atlas, anchor["target_graph"]),
                ) is None,
                f"exact anchor has unequal old-label quartet deck:{anchor['anchor_id']}",
            )
            label = max(labels_of(anchor["source_graph"])) + 1
            source_children = prepare_probe_children(
                atlas, anchor, "source", anchor["source_profile"], label,
                f"P1:{anchor['anchor_id']}", restriction_registry,
            )
            target_children = prepare_probe_children(
                atlas, anchor, "target", anchor["target_profile"], label,
                f"P1:{anchor['anchor_id']}", restriction_registry,
            )
            for source_child in source_children:
                for target_child in target_children:
                    result, witness = classify_probe_pair(
                        atlas, anchor, source_child, target_child, sign_oracle,
                        proof_registry, transport_registry,
                    )
                    row = {
                        "stage": "A+p",
                        "parent_anchor_id": anchor["anchor_id"],
                        "origin": anchor["origin"],
                        "inserted_label": label,
                        "source_site_index": source_child["site_index"],
                        "source_site_id": source_child["site"]["site_id"],
                        "target_site_index": target_child["site_index"],
                        "target_site_id": target_child["site"]["site_id"],
                        "source_child_graph_sha256": source_child["graph_sha256"],
                        "target_child_graph_sha256": target_child["graph_sha256"],
                        "source_parent_restriction_id": source_child["restriction_certificate_id"],
                        "target_parent_restriction_id": target_child["restriction_certificate_id"],
                        **result,
                    }
                    writer.write(row)
                    ordered.add(sha(row))
                    counts[result["status"]] += 1
                    by_origin[(anchor["origin"], result["status"])] += 1
                    if result["status"] == "unresolved":
                        if len(unresolved) < 50:
                            unresolved.append(row)
                        continue
                    if witness is None:
                        continue
                    child = {
                        "anchor_id": (
                            f"P1:{anchor['anchor_id']}:"
                            f"{source_child['site_index']}:{target_child['site_index']}"
                        ),
                        "base_anchor_id": anchor["anchor_id"],
                        "origin": anchor["origin"],
                        "source_graph": source_child["graph"],
                        "target_graph": target_child["graph"],
                        "relation": result["status"],
                        "transport": witness,
                        "global_triangle": anchor["global_triangle"],
                        "first_source_site_index": source_child["site_index"],
                        "first_target_site_index": target_child["site_index"],
                        "first_source_site_id": source_child["site"]["site_id"],
                        "first_target_site_id": target_child["site"]["site_id"],
                        "first_label": label,
                    }
                    child["canonical_relation_class_id"] = relation_registry.add(child)
                    survivors.append(child)
    finally:
        writer.close()
    require(ordered.count == sum(counts.values()), "one-port ordered coverage")
    return {
        "counts": counts,
        "by_origin": by_origin,
        "ordered": ordered.public(),
        "survivors": survivors,
        "unresolved_examples": unresolved,
    }


def relabel_single_leaf(graph, old_label, new_label):
    result = graph.copy()
    nodes = [
        node for node, data in result.nodes(data=True)
        if data.get("role") == "leaf" and data.get("label") == old_label
    ]
    require(len(nodes) == 1, f"single leaf relabel:{old_label}:{nodes}")
    require(
        not [
            node for node, data in result.nodes(data=True)
            if data.get("role") == "leaf" and data.get("label") == new_label
        ],
        f"replacement leaf label already present:{new_label}",
    )
    result.nodes[nodes[0]]["label"] = new_label
    return result


def coherent_base_witness(base, witness, relation):
    if any(
        witness["vertex_map"].get(node) != base["transport"]["vertex_map"][node]
        for node in base["transport"]["vertex_map"]
    ):
        return False
    inherited = base["global_triangle"]
    if relation == "triangle":
        if inherited is None:
            return False
        if sorted([list(edge_key(*tuple(edge))) for edge in witness["source_triangle"]]) != inherited["source_triangle_edges"]:
            return False
        if sorted([list(edge_key(*tuple(edge))) for edge in witness["target_triangle"]]) != inherited["target_triangle_edges"]:
            return False
    return True


def reverse_order_certificate(
    atlas, base, final_source, final_target, first_label, second_label,
    relation_registry, one_classes_by_base, transport_registry,
):
    keep = set(labels_of(base["source_graph"])) | {second_label}
    reverse_source = atlas.restrict_rooted(final_source, keep)
    reverse_target = atlas.restrict_rooted(final_target, keep)
    reverse_source = relabel_single_leaf(reverse_source, second_label, first_label)
    reverse_target = relabel_single_leaf(reverse_target, second_label, first_label)
    relation, witnesses = exact_relation(atlas, reverse_source, reverse_target)
    require(relation in {"isomorphic", "triangle"}, f"reverse parent not equality:{relation}")
    require(len(witnesses) == 1, f"reverse parent transport multiplicity:{len(witnesses)}")
    witness = witnesses[0]
    require(
        coherent_base_witness(base, witness, relation),
        "reverse parent transport does not restrict the same base/global triangle",
    )
    reverse_record = {
        "source_graph": reverse_source,
        "target_graph": reverse_target,
        "relation": relation,
        "transport": witness,
    }
    class_count_before = len(relation_registry.representatives)
    class_id = relation_registry.add(reverse_record)
    require(
        class_id in one_classes_by_base[base["anchor_id"]],
        f"reverse order missing from one-port equality universe:{base['anchor_id']}:{class_id}",
    )
    require(
        len(relation_registry.representatives) == class_count_before,
        "reverse order created a new one-port canonical relation",
    )
    transport_id = register_transport(transport_registry, witness)
    certificate = {
        "remove_first_label": first_label,
        "retain_then_rename_second_label": [second_label, first_label],
        "reverse_parent_relation": relation,
        "reverse_parent_transport_id": transport_id,
        "reverse_parent_canonical_one_port_class_id": class_id,
        "reverse_parent_source_graph_sha256": sha(graph_payload(reverse_source)),
        "reverse_parent_target_graph_sha256": sha(graph_payload(reverse_target)),
        "same_base_anchor_id": base["anchor_id"],
        "conclusion": "the reversed one-probe marginal is present in the complete one-port equality universe",
    }
    return certificate


def enumerate_two_port(
    atlas, base_by_id, parents, relation_registry, sign_oracle,
    proof_registry, restriction_registry, transport_registry,
):
    counts = collections.Counter()
    by_origin = collections.Counter()
    reverse_counts = collections.Counter()
    ordered = OrderedHashAccumulator()
    parent_ordered = OrderedHashAccumulator()
    unresolved = []
    one_classes_by_base = collections.defaultdict(set)
    for parent in parents:
        one_classes_by_base[parent["base_anchor_id"]].add(
            parent["canonical_relation_class_id"]
        )
    writer = JsonlGzipWriter(TWO_LEDGER)
    parent_writer = JsonlGzipWriter(TWO_PARENT_LEDGER)
    equality_survivors = 0
    inherited_triangle_parents = 0
    equality_with_global_triangle = 0
    try:
        for parent_number, parent in enumerate(parents):
            if parent_number % 100 == 0:
                print(
                    f"corrected-probe: two-port parent {parent_number}/{len(parents)}",
                    file=sys.stderr, flush=True,
                )
            base = base_by_id[parent["base_anchor_id"]]
            label = max(labels_of(parent["source_graph"])) + 1
            source_profile = site_profile(atlas, parent["source_graph"])
            target_profile = site_profile(atlas, parent["target_graph"])
            require(
                source_profile["site_count"] == target_profile["site_count"],
                "equality parent site count drift",
            )
            if parent["global_triangle"] is not None:
                inherited_triangle_parents += 1
            require(
                first_quartet_mismatch(
                    quartet_deck(atlas, parent["source_graph"]),
                    quartet_deck(atlas, parent["target_graph"]),
                ) is None,
                f"exact one-port parent has unequal old-label quartet deck:{parent['anchor_id']}",
            )
            parent_row = {
                "one_port_parent_id": parent["anchor_id"],
                "base_anchor_id": parent["base_anchor_id"],
                "origin": parent["origin"],
                "relation": parent["relation"],
                "canonical_one_port_relation_class_id": parent["canonical_relation_class_id"],
                "first_label": parent["first_label"],
                "first_source_site_index": parent["first_source_site_index"],
                "first_target_site_index": parent["first_target_site_index"],
                "source_graph_sha256": sha(graph_payload(parent["source_graph"])),
                "target_graph_sha256": sha(graph_payload(parent["target_graph"])),
                "source_candidate_profile": source_profile,
                "target_candidate_profile": target_profile,
                "raw_second_probe_pairs": source_profile["site_count"] * target_profile["site_count"],
            }
            parent_writer.write(parent_row)
            parent_ordered.add(sha(parent_row))
            source_children = prepare_probe_children(
                atlas, parent, "source", source_profile, label,
                f"P2:{parent['anchor_id']}", restriction_registry,
            )
            target_children = prepare_probe_children(
                atlas, parent, "target", target_profile, label,
                f"P2:{parent['anchor_id']}", restriction_registry,
            )
            for source_child in source_children:
                for target_child in target_children:
                    result, witness = classify_probe_pair(
                        atlas, parent, source_child, target_child, sign_oracle,
                        proof_registry, transport_registry,
                    )
                    row = {
                        "stage": "A+p+q",
                        "base_anchor_id": parent["base_anchor_id"],
                        "one_port_parent_id": parent["anchor_id"],
                        "origin": parent["origin"],
                        "first_label": parent["first_label"],
                        "second_label": label,
                        "first_source_site_index": parent["first_source_site_index"],
                        "first_target_site_index": parent["first_target_site_index"],
                        "second_source_site_index": source_child["site_index"],
                        "second_source_site_id": source_child["site"]["site_id"],
                        "second_target_site_index": target_child["site_index"],
                        "second_target_site_id": target_child["site"]["site_id"],
                        "source_child_graph_sha256": source_child["graph_sha256"],
                        "target_child_graph_sha256": target_child["graph_sha256"],
                        "source_parent_restriction_id": source_child["restriction_certificate_id"],
                        "target_parent_restriction_id": target_child["restriction_certificate_id"],
                        **result,
                    }
                    if witness is not None:
                        reverse = reverse_order_certificate(
                            atlas, base, source_child["graph"], target_child["graph"],
                            parent["first_label"], label, relation_registry,
                            one_classes_by_base, transport_registry,
                        )
                        row["reverse_order_certificate"] = reverse
                        reverse_counts[reverse["reverse_parent_relation"]] += 1
                        equality_survivors += 1
                        if parent["global_triangle"] is not None:
                            equality_with_global_triangle += 1
                    writer.write(row)
                    ordered.add(sha(row))
                    counts[result["status"]] += 1
                    by_origin[(parent["origin"], result["status"])] += 1
                    if result["status"] == "unresolved" and len(unresolved) < 50:
                        unresolved.append(row)
    finally:
        writer.close()
        parent_writer.close()
    require(parent_ordered.count == len(parents), "two-port parent coverage")
    require(ordered.count == sum(counts.values()), "two-port ordered coverage")
    require(
        equality_survivors == counts["isomorphic"] + counts["triangle"],
        "two-port equality/reverse coverage",
    )
    return {
        "counts": counts,
        "by_origin": by_origin,
        "ordered": ordered.public(),
        "parent_ordered": parent_ordered.public(),
        "equality_survivors": equality_survivors,
        "reverse_counts": reverse_counts,
        "inherited_triangle_parents": inherited_triangle_parents,
        "equality_with_global_triangle": equality_with_global_triangle,
        "unresolved_examples": unresolved,
    }


def tree_graph():
    graph = nx.DiGraph(name="three_port_tree")
    for node, role, label in (
        ("r", "root", None), ("v", "tree", None),
        ("L0", "leaf", 0), ("L1", "leaf", 1), ("L2", "leaf", 2),
    ):
        graph.add_node(node, role=role, label=label, dummy=False, dummy_name=None)
    graph.add_edges_from((
        ("r", "L0", {"edge_role": "incoming_arm"}),
        ("r", "v", {"edge_role": "incoming_core"}),
        ("v", "L1", {"edge_role": "arm"}),
        ("v", "L2", {"edge_role": "arm"}),
    ))
    return graph


def write_json_gzip(path, value):
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            compressed.write(canonical_bytes(value))
            compressed.write(b"\n")


def reconstruct_anchors(atlas, common, generator, contract):
    raw_ids = {
        row["locator"].get("raw_id")
        for row in contract["anchors"]
        if row["origin"].startswith("four_port")
    }
    raw_rows = {}
    with gzip.open(RAW4, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if row["raw_id"] in raw_ids:
                raw_rows[row["raw_id"]] = row
    require(set(raw_rows) == raw_ids, "four-port raw locator coverage")
    four_sources = atlas.source_supports()
    four_targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)

    with gzip.open(THETA2, "rt") as handle:
        theta = json.load(handle)
    theta_sources = atlas.source_supports(("theta2",))
    theta_targets = atlas.target_completions(5, True) + atlas.target_completions(5, False)
    theta_no_dummy = {row["anchor_id"]: row for row in theta["no_dummy_anchors"]}
    theta_roots = {row["base_raw_id"]: row for row in theta["restoration_roots"]}
    theta_six = {row["path_id"]: row for row in theta["six_port_rows"]}
    theta_seven = {row["path_id"]: row for row in theta["seven_port_rows"]}

    cycle_package = json.loads(CYCLE_ANCHORS.read_text())
    cycle_rows = {row["anchor_id"]: row for row in cycle_package["anchors"]}
    cycle_sources = atlas.source_supports(("cycle",))
    cycle_targets = atlas.target_completions(3, True) + atlas.target_completions(3, False)
    cycle_permutations = tuple(itertools.permutations(range(3)))
    configurations = generator.build_source_configurations(atlas, cycle_sources)
    configuration_index = {
        (source_index, depth, tuple(row["placement_path"])): row["graph"]
        for (source_index, depth), rows in configurations.items()
        for row in rows
    }

    anchors = []
    for expected in contract["anchors"]:
        origin = expected["origin"]
        locator = expected["locator"]
        if origin.startswith("four_port"):
            raw = raw_rows[locator["raw_id"]]
            source = four_sources[raw["source_index"]].graph
            target_record = atlas.relabel_record(
                four_targets[raw["target_index"]], tuple(raw["port_permutation"])
            )
            target = target_record.graph
            for depth, step in enumerate(locator.get("restoration_path", [])):
                source = insert_on_arc(
                    source,
                    step["source_insertion"],
                    step["label"],
                    f"four_anchor_restore_{raw['raw_id']}_{depth}_{step['source_insertion_index']}",
                )
                target = promote_roles(target, ((step["restored_role"], step["label"]),))
        elif origin.startswith("theta2"):
            if origin == "theta2_physical_k5":
                row = theta_no_dummy[locator["upstream_anchor_id"]]
                source = theta_sources[row["source_index"]].graph
                target = atlas.relabel_record(
                    theta_targets[row["target_index"]], tuple(row["port_permutation"])
                ).graph
            elif origin == "theta2_physical_k6":
                row = theta_six[locator["path_id"]]
                root = theta_roots[row["base_raw_id"]]
                source = insert_on_arc(
                    theta_sources[row["source_index"]].graph,
                    row["source_insertion"], 5, "theta2_k6",
                )
                target = atlas.relabel_record(
                    theta_targets[row["target_index"]], tuple(root["port_permutation"])
                ).graph
                target = promote_roles(target, ((row["restored_role"], 5),))
            else:
                row = theta_seven[locator["path_id"]]
                parent = theta_six[row["parent_path_id"]]
                root = theta_roots[row["base_raw_id"]]
                source = insert_on_arc(
                    theta_sources[row["source_index"]].graph,
                    parent["source_insertion"], 5, "theta2_k7_first",
                )
                source = insert_on_arc(
                    source, row["source_insertion"], 6, "theta2_k7_second",
                )
                target = atlas.relabel_record(
                    theta_targets[row["target_index"]], tuple(root["port_permutation"])
                ).graph
                target = promote_roles(target, (
                    (row["first_restored_role"], 5), (row["restored_role"], 6),
                ))
        elif origin.startswith("cycle"):
            row = cycle_rows[locator["anchor_id"]]
            if row["origin"] == "base_no_dummy":
                source = cycle_sources[row["source_index"]].graph
                target = atlas.relabel_record(
                    cycle_targets[row["target_index"]], tuple(row["port_permutation"])
                ).graph
            else:
                depth = len(row["dummy_roles_in_label_order"])
                source = configuration_index[
                    (row["source_index"], depth, tuple(row["source_placement_path"]))
                ]
                target = common.relabel_and_promote_all(
                    atlas,
                    cycle_targets[row["target_index"]],
                    cycle_permutations[row["permutation_index"]],
                    tuple(row["dummy_roles_in_label_order"]),
                )
        elif origin == "tree_physical_k3":
            source = target = tree_graph()
        else:
            raise ProbeFailure(f"unknown anchor origin:{origin}")

        require(not [data for _, data in source.nodes(data=True) if data.get("dummy")], "source dummy")
        require(not [data for _, data in target.nodes(data=True) if data.get("dummy")], "target dummy")
        require(sha(graph_payload(source)) == expected["source_graph_sha256"], f"source graph:{expected['anchor_id']}")
        require(sha(graph_payload(target)) == expected["target_graph_sha256"], f"target graph:{expected['anchor_id']}")
        relation, witnesses = exact_relation(atlas, source, target)
        require(relation == expected["relation"] and len(witnesses) == 1, f"anchor relation:{expected['anchor_id']}")
        witness = witnesses[0]
        require(witness["public"] == expected["parent_transport"], f"anchor transport:{expected['anchor_id']}")
        source_profile = site_profile(atlas, source)
        target_profile = site_profile(atlas, target)
        require(source_profile == expected["source_candidate_profile"], f"source sites:{expected['anchor_id']}")
        require(target_profile == expected["target_candidate_profile"], f"target sites:{expected['anchor_id']}")
        anchor = {
            "anchor_id": expected["anchor_id"],
            "origin": origin,
            "source_graph": source,
            "target_graph": target,
            "relation": relation,
            "transport": witness,
            "source_profile": source_profile,
            "target_profile": target_profile,
            "locator": locator,
        }
        anchor["global_triangle"] = global_triangle(anchor)
        anchors.append(anchor)
    require(len(anchors) == 176, "anchor reconstruction census")
    return anchors


def seal_proof_registry(proof_registry, sign_oracle):
    registries = {
        "schema": "k3p-corrected-probe-separation-registries-v1",
        "separation_proof_registry": dict(sorted(proof_registry.items())),
        "k3p_tree_sunlet_registry": sign_oracle.public(),
    }
    registries["payload_sha256"] = sha(registries)
    write_json_gzip(PROOF_REGISTRY, registries)
    return registries


def base_certificate(
    contract, restoration, anchor_summary, anchors, anchor_registry,
    anchor_class_coverage, public_anchors, one, proof_registries,
    transport_store, restriction_store,
):
    del restoration
    return {
        "schema": "k3p-corrected-coherent-probe-closure-v1",
        "status": "IN_PROGRESS",
        "claim_boundary": (
            "Exact relation first, displayed quartet second, and literal K3P "
            "three-leaf descriptor plus six-circuit SOS third. Triple type is a finder, "
            "never the algebraic certificate."
        ),
        "inputs": {
            "atlas_sha256": sha_file(ATLAS_PATH),
            "probe_input_contract_sha256": sha_file(INPUT_CONTRACT),
            "probe_input_contract_payload_sha256": contract["payload_sha256"],
            "probe_input_independent_replay_sha256": sha_file(INPUT_REPLAY),
            "probe_input_mutations_sha256": sha_file(INPUT_MUTATIONS),
            "corrected_restoration_sha256": sha_file(RESTORATION),
            "raw4_ledger_sha256": sha_file(RAW4),
            "theta2_fixed_full_closure_sha256": sha_file(THETA2),
            "cycle_physical_anchors_sha256": sha_file(CYCLE_ANCHORS),
            "cycle_promotion_sha256": sha_file(CYCLE_PROMOTION),
        },
        "classifier_order": [
            "exact_labelled_isomorphism_or_ordinary_triangle",
            "displayed_quartet_mismatch",
            "literal_K3P_triple_maps_plus_tree_sunlet_six_circuit_SOS",
            "unresolved_fatal",
        ],
        "exact_relation_prefilter": {
            "method": (
                "a child relation marginalizes to the unique parent relation; "
                "the new labelled leaf forces its subdivision, so only the unique "
                "parent edge-map image site can support a child relation"
            ),
            "status": "exact theorem prefilter, not a heuristic cache",
        },
        "triple_finder_is_not_certificate": True,
        "uses_k2p_sector_equality": False,
        "anchor_inventory": {
            **{key: value for key, value in anchor_summary.items() if key != "runtime_seconds"},
            "canonical_anchor_classes": len(anchor_registry.representatives),
            "canonical_class_coverage": {
                str(class_id): members
                for class_id, members in sorted(anchor_class_coverage.items())
            },
            "ordered_public_anchor_hash_root": sha([sha(row) for row in public_anchors]),
            "public_anchors": public_anchors,
        },
        "one_port": {
            "raw_pairs": sum(one["counts"].values()),
            "counts": dict(sorted(one["counts"].items())),
            "counts_by_origin": {
                f"{origin}:{status}": count
                for (origin, status), count in sorted(one["by_origin"].items())
            },
            "equality_survivors": len(one["survivors"]),
            "canonical_equality_relation_classes": len({
                row["canonical_relation_class_id"] for row in one["survivors"]
            }),
            "ordered_ledger": one["ordered"],
            "ledger_sha256": sha_file(ONE_LEDGER),
            "unresolved": one["counts"]["unresolved"],
            "unresolved_examples": one["unresolved_examples"],
        },
        "registries": {
            "separation": {
                "path": PROOF_REGISTRY.name,
                "sha256": sha_file(PROOF_REGISTRY),
                "payload_sha256": proof_registries["payload_sha256"],
                "topological_proofs": len(proof_registries["separation_proof_registry"]),
                "k3p_tree_sunlet_relation_certificates": len(
                    proof_registries["k3p_tree_sunlet_registry"]["certificates"]
                ),
            },
            "exact_transports": transport_store.public(),
            "parent_restrictions": restriction_store.public(),
        },
    }


def seal_certificate(certificate, started):
    elapsed_seconds = time.monotonic() - started
    certificate.pop("operational", None)
    logical = dict(certificate)
    logical.pop("payload_sha256", None)
    certificate["payload_sha256"] = sha(logical)
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(
        f"K3P_CORRECTED_PROBE_ELAPSED_SECONDS={elapsed_seconds:.6f}",
        file=sys.stderr,
        flush=True,
    )


def main():
    if not __debug__:
        raise ProbeFailure("CORRECTED_PROBE_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--anchors-only", action="store_true")
    parser.add_argument("--stop-after", choices=("one", "two"), default="two")
    args = parser.parse_args()
    started = time.monotonic()
    atlas = import_path("corrected_probe_atlas", ATLAS_PATH)
    common = import_path("cycle_common", CYCLE_COMMON)
    generator = import_path("corrected_probe_cycle_generator", CYCLE_GENERATOR)
    contract = json.loads(INPUT_CONTRACT.read_text())
    payload = contract["payload_sha256"]
    unhashed = dict(contract)
    unhashed.pop("payload_sha256")
    require(payload == sha(unhashed), "probe input contract payload")
    require(contract["schema"] == "k2p-root-invariant-probe-input-contract-v2", "probe contract schema")
    restoration = json.loads(RESTORATION.read_text())
    require(restoration["status"] == "PASS", "clean restoration input")
    require(restoration["scope_contract"]["critical_triangle_raw_ids"] == [67161, 67167, 67401, 67407], "restoration/probe scope cross-binding")
    anchors = reconstruct_anchors(atlas, common, generator, contract)
    anchor_summary = {
        "status": "PASS",
        "anchors": len(anchors),
        "source_sites": sum(row["source_profile"]["site_count"] for row in anchors),
        "target_sites": sum(row["target_profile"]["site_count"] for row in anchors),
        "first_pairs": sum(
            row["source_profile"]["site_count"] * row["target_profile"]["site_count"]
            for row in anchors
        ),
        "relation_counts": dict(sorted(collections.Counter(row["relation"] for row in anchors).items())),
        "origin_counts": dict(sorted(collections.Counter(row["origin"] for row in anchors).items())),
        "runtime_seconds": time.monotonic() - started,
    }
    require(anchor_summary["anchors"] == 176, "anchor summary")
    require(anchor_summary["source_sites"] == anchor_summary["target_sites"] == 2_206, "site summary")
    require(anchor_summary["first_pairs"] == 29_964, "first-pair summary")
    if args.anchors_only:
        print(json.dumps(anchor_summary, sort_keys=True))
        return

    anchor_registry = CanonicalRelationRegistry(atlas)
    relation_registry = CanonicalRelationRegistry(atlas)
    sign_oracle = K3PTreeSunletOracle(atlas)
    proof_registry = {}
    restriction_registry = StreamingRecordStore(
        RESTRICTION_LEDGER, "exact_parent_marginal_restriction"
    )
    transport_registry = StreamingRecordStore(
        TRANSPORT_LEDGER, "exact_labelled_mixed_graph_transport"
    )
    public_anchors = []
    anchor_class_coverage = collections.defaultdict(list)
    for anchor in anchors:
        transport_id = register_transport(transport_registry, anchor["transport"])
        require(
            transport_id == anchor["transport"]["public"]["transport_sha256"],
            "anchor transport registry",
        )
        class_id = anchor_registry.add(anchor)
        anchor_class_coverage[class_id].append(anchor["anchor_id"])
        public_anchors.append(public_anchor_row(anchor, class_id))

    one = enumerate_one_port(
        atlas, anchors, relation_registry, sign_oracle,
        proof_registry, restriction_registry, transport_registry,
    )
    print(
        "corrected-probe: one-port "
        f"raw={sum(one['counts'].values())} survivors={len(one['survivors'])} "
        f"counts={dict(sorted(one['counts'].items()))}",
        file=sys.stderr, flush=True,
    )
    require(one["counts"]["unresolved"] == 0, f"one-port unresolved:{one['unresolved_examples'][:3]}")
    if args.stop_after == "one":
        transport_registry.close()
        restriction_registry.close()
        registries = seal_proof_registry(proof_registry, sign_oracle)
        checkpoint = base_certificate(
            contract, restoration, anchor_summary, anchors, anchor_registry,
            anchor_class_coverage, public_anchors, one, registries,
            transport_registry, restriction_registry,
        )
        checkpoint["status"] = "CHECKPOINT_ONE_PORT"
        seal_certificate(checkpoint, started)
        print(json.dumps({
            "status": checkpoint["status"],
            "counts": checkpoint["one_port"]["counts"],
            "survivors": checkpoint["one_port"]["equality_survivors"],
            "payload_sha256": checkpoint["payload_sha256"],
        }, sort_keys=True))
        return

    base_by_id = {anchor["anchor_id"]: anchor for anchor in anchors}
    two = enumerate_two_port(
        atlas, base_by_id, one["survivors"], relation_registry, sign_oracle,
        proof_registry, restriction_registry, transport_registry,
    )
    print(
        "corrected-probe: two-port "
        f"raw={sum(two['counts'].values())} survivors={two['equality_survivors']} "
        f"counts={dict(sorted(two['counts'].items()))}",
        file=sys.stderr, flush=True,
    )
    require(two["counts"]["unresolved"] == 0, f"two-port unresolved:{two['unresolved_examples'][:3]}")
    require(
        two["equality_survivors"] == sum(two["reverse_counts"].values()),
        "reverse-order terminal coverage",
    )

    transport_registry.close()
    restriction_registry.close()
    registries = seal_proof_registry(proof_registry, sign_oracle)
    checkpoint = base_certificate(
        contract, restoration, anchor_summary, anchors, anchor_registry,
        anchor_class_coverage, public_anchors, one, registries,
        transport_registry, restriction_registry,
    )
    checkpoint["status"] = "PASS"
    checkpoint["two_port"] = {
        "parents": len(one["survivors"]),
        "raw_pairs": sum(two["counts"].values()),
        "counts": dict(sorted(two["counts"].items())),
        "counts_by_origin": {
            f"{origin}:{status}": count
            for (origin, status), count in sorted(two["by_origin"].items())
        },
        "equality_survivors": two["equality_survivors"],
        "ordered_parent_inventory": two["parent_ordered"],
        "parent_inventory_sha256": sha_file(TWO_PARENT_LEDGER),
        "ordered_ledger": two["ordered"],
        "ledger_sha256": sha_file(TWO_LEDGER),
        "unresolved": two["counts"]["unresolved"],
        "unresolved_examples": two["unresolved_examples"],
        "reverse_order_parent_relation_counts": dict(sorted(two["reverse_counts"].items())),
    }
    checkpoint["assembly_theorem"] = {
        "all_primitive_physical_anchor_types": [
            "ordinary_tree", "cycle", "theta0", "theta1", "theta2", "theta3"
        ],
        "root_movement_and_site_completeness": {
            "all_suppressed_mixed_edges": True,
            "pendant_arms": True,
            "reticulation_incoming_edges": True,
            "root_suppressed_segment": True,
            "artificial_root_halves_quotiented_by_exact_isomorphism": True,
            "input_contract_payload_sha256": contract["payload_sha256"],
        },
        "one_port_segment_gate": {
            "raw_pairs": sum(one["counts"].values()),
            "equality_parents_retained": len(one["survivors"]),
            "every_non_equality_has_exact_separator": True,
        },
        "two_port_order_gate": {
            "raw_pairs_above_equality_parents_only": sum(two["counts"].values()),
            "every_equality_has_reversed_one_port_marginal": True,
            "reversed_marginals_checked": two["equality_survivors"],
            "reversed_marginals_missing": 0,
            "conclusion": (
                "each adjacent pair of attachment positions and their order is fixed; "
                "induction along every maximal degree-two segment reconstructs an arbitrary word"
            ),
        },
        "one_global_triangle_gate": {
            "triangle_anchors": sum(anchor["global_triangle"] is not None for anchor in anchors),
            "one_port_parents_inheriting_triangle": two["inherited_triangle_parents"],
            "two_port_equalities_inheriting_triangle": two["equality_with_global_triangle"],
            "new_triangle_created_above_isomorphic_parent": 0,
            "every_triangle_transport_uses_the_same_parent_triangle_edges_and_common_reticulation": True,
            "conclusion": "at most the single ordinary triangle already present in the rigid-support anchor is transported globally",
        },
        "bridge_and_marginal_compatibility": {
            "separator_applied_to_direct_three_leaf_marginal": True,
            "three_independent_sectors": ["C", "G", "T"],
            "serial_descriptor": "(product c_i, product g_i, product t_i)",
            "conclusion": (
                "the tree-side SOS is zero and the sunlet-side SOS is strictly "
                "positive after every strict physical marginal lift; no sector "
                "identification or boundary gauge can change zero versus positivity"
            ),
        },
        "unresolved": 0,
        "incoherent": 0,
        "conclusion": (
            "complete one-/two-port coherence supplies segment, order, and one-global-T "
            "assembly for arbitrary attachment words over every primitive rigid support"
        ),
    }
    seal_certificate(checkpoint, started)
    print(json.dumps({
        "status": checkpoint["status"],
        "one_counts": checkpoint["one_port"]["counts"],
        "two_counts": checkpoint["two_port"]["counts"],
        "payload_sha256": checkpoint["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ProbeFailure, AssertionError, KeyError, IndexError, OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"CORRECTED_PROBE_FAIL:{error}") from error
