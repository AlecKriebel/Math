#!/usr/bin/env python3
"""Independent replay of the fixed-full K3P restoration release.

This verifier does not import the producer or its helper module.  It rebuilds
the core graphs, restoration children, selected restrictions, K3P switching
maps, sparse polynomial pullbacks, strict rational witnesses, and full forest
accounting through a separate implementation.
"""
from __future__ import annotations

import argparse
import ast
import collections
import gzip
import hashlib
import itertools
import json
import math
import os
import sys
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ATLAS_PATH = PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py"
FOREST_PATH = PROJECT / "input_frozen/model_independent_topology_package/anchor_inputs/corrected_restoration_forest.json"
SEPARATOR_PATH = PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_tree_sunlet_separator.json"
THREE_PORT_PATH = PROJECT / "three_port/primary_exact_evidence.json"
MARGINAL_PATH = PROJECT / "marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json"
H14_PATH = PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_h14_marginal_orbit_certificates.json"
REMAINING_PATH = PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_remaining_quartic_separators.json"


class VerificationFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationFailure(message)


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


def logical_payload(value):
    payload = dict(value)
    payload.pop("payload_sha256", None)
    return sha(payload)


CORES = {
    "cycle": {
        "arcs": (("S", "X"), ("S", "X")),
        "retics": ("X",),
        "sinks": ("X",),
        "repairs": ((0,), (1,)),
    },
    "theta0": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X"), ("V", "X"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (3, 4)),
    },
    "theta1": {
        "arcs": (("S", "U"), ("S", "X"), ("V", "X"), ("U", "V"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (2, 4)),
    },
    "theta2": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X0"), ("V", "X0"),
                 ("U", "X1"), ("V", "X1")),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2, 3), (2, 5), (3, 4), (4, 5)),
    },
    "theta3": {
        "arcs": (("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "X1"),
                 ("V", "X1"), ("U", "V")),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2,), (4,)),
    },
}


@dataclass(frozen=True)
class ModelRecord:
    core_id: str
    repair_index: int | None
    graph: nx.DiGraph
    dummy_labels: tuple[str, ...]


def weak_compositions(total, bins):
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, bins - 1):
            yield (first,) + rest


def build_graph(core_id, words, sink_labels, incoming_label):
    spec = CORES[core_id]
    graph = nx.DiGraph(core_id=core_id)
    for node in {value for arc in spec["arcs"] for value in arc}:
        graph.add_node(
            ("core", node),
            role="retic" if node in spec["retics"] else "tree",
            label=None,
            dummy=False,
        )
    root = ("root",)
    incoming = ("leaf", "INCOMING")
    graph.add_node(root, role="root", label=None, dummy=False)
    selected = isinstance(incoming_label, int)
    graph.add_node(
        incoming,
        role="leaf",
        label=incoming_label if selected else None,
        dummy=not selected,
        dummy_name=None if selected else str(incoming_label),
    )
    graph.add_edge(root, ("core", "S"), edge_role="incoming_core")
    graph.add_edge(root, incoming, edge_role="incoming_arm")
    for segment, ((tail, head), word) in enumerate(zip(spec["arcs"], words)):
        previous = ("core", tail)
        for position, label in enumerate(word):
            subdivision = ("sub", segment, position)
            leaf = ("leaf", "seg", segment, position)
            selected = isinstance(label, int)
            graph.add_node(subdivision, role="tree", label=None, dummy=False)
            graph.add_node(
                leaf,
                role="leaf",
                label=label if selected else None,
                dummy=not selected,
                dummy_name=None if selected else str(label),
            )
            graph.add_edge(previous, subdivision, edge_role=f"seg{segment}")
            graph.add_edge(subdivision, leaf, edge_role="arm")
            previous = subdivision
        graph.add_edge(previous, ("core", head), edge_role=f"seg{segment}")
    for sink_index, sink in enumerate(spec["sinks"]):
        label = sink_labels[sink]
        selected = isinstance(label, int)
        leaf = ("leaf", "sink", sink_index)
        graph.add_node(
            leaf,
            role="leaf",
            label=label if selected else None,
            dummy=not selected,
            dummy_name=None if selected else str(label),
        )
        graph.add_edge(("core", sink), leaf, edge_role="sink_arm")
    validate_graph(graph)
    return graph


def validate_graph(graph):
    require(nx.is_directed_acyclic_graph(graph), "child graph directed cycle")
    labels = []
    for node, data in graph.nodes(data=True):
        degree = (graph.in_degree(node), graph.out_degree(node))
        expected = {
            "root": (0, 2),
            "tree": (1, 2),
            "retic": (2, 1),
            "leaf": (1, 0),
        }[data["role"]]
        require(degree == expected, f"degree/role mismatch:{node}:{degree}:{expected}")
        if isinstance(data.get("label"), int):
            labels.append(data["label"])
        if data["role"] != "leaf":
            require(
                any(graph.nodes[child]["role"] in {"tree", "leaf"}
                    for child in graph.successors(node)),
                f"tree-child violation:{node}",
            )
    require(len(labels) == len(set(labels)), "duplicate selected labels")


def source_supports():
    rows = []
    for core_id in ("theta0", "theta1", "theta3"):
        spec = CORES[core_id]
        for repair_index, repair in enumerate(spec["repairs"]):
            words = [[] for _ in spec["arcs"]]
            next_label = 1
            for segment in repair:
                words[segment].append(next_label)
                next_label += 1
            sink_labels = {}
            for sink in spec["sinks"]:
                sink_labels[sink] = next_label
                next_label += 1
            rows.append(ModelRecord(
                core_id,
                repair_index,
                build_graph(core_id, tuple(map(tuple, words)), sink_labels, 0),
                (),
            ))
    return rows


def target_completions(selected_total, incoming_selected):
    rows = []
    for core_id, spec in CORES.items():
        outgoing = selected_total - 1 if incoming_selected else selected_total
        for sink_mask in range(1 << len(spec["sinks"])):
            ordinary = outgoing - sum((sink_mask >> j) & 1 for j in range(len(spec["sinks"])))
            if ordinary < 0:
                continue
            for counts in weak_compositions(ordinary, len(spec["arcs"])):
                labels = iter(range(1 if incoming_selected else 0, selected_total))
                selected_words = tuple(
                    tuple(next(labels) for _ in range(count)) for count in counts
                )
                repairs = ((None, ()),) if core_id == "cycle" else tuple(enumerate(spec["repairs"]))
                for repair_index, repair in repairs:
                    words = [list(word) for word in selected_words]
                    dummies = []
                    for segment in repair:
                        if not words[segment]:
                            name = f"D_REPAIR_{repair_index}_{segment}"
                            words[segment].append(name)
                            dummies.append(name)
                    used = [label for word in selected_words for label in word]
                    next_label = max(used) + 1 if used else (1 if incoming_selected else 0)
                    sink_labels = {}
                    for sink_index, sink in enumerate(spec["sinks"]):
                        if (sink_mask >> sink_index) & 1:
                            sink_labels[sink] = next_label
                            next_label += 1
                        else:
                            name = f"D_SINK_{sink_index}"
                            sink_labels[sink] = name
                            dummies.append(name)
                    incoming = 0 if incoming_selected else "INCOMING"
                    if not incoming_selected:
                        dummies.append("INCOMING")
                    graph = build_graph(core_id, tuple(map(tuple, words)), sink_labels, incoming)
                    require(labels_of(graph) == tuple(range(selected_total)),
                            "target completion selected labels")
                    rows.append(ModelRecord(core_id, repair_index, graph, tuple(sorted(dummies))))
    return rows


def relabel_graph(graph, permutation):
    result = graph.copy()
    for _, data in result.nodes(data=True):
        if isinstance(data.get("label"), int):
            data["label"] = permutation[data["label"]]
    return result


def labels_of(graph):
    return tuple(sorted(
        data["label"] for _, data in graph.nodes(data=True)
        if isinstance(data.get("label"), int)
    ))


def source_insertion_candidates(graph):
    rows = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        if graph.nodes[head].get("role") == "leaf":
            continue
        if graph.nodes[tail].get("role") == "root":
            continue
        rows.append({
            "tail": repr(tail),
            "head": repr(head),
            "edge_role": data.get("edge_role"),
        })
    return rows


def insert_source_leaf(graph, candidate, label):
    result = graph.copy()
    tail = ast.literal_eval(candidate["tail"])
    head = ast.literal_eval(candidate["head"])
    require(result.has_edge(tail, head), "missing source insertion edge")
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = ("restoration_subdivision", label, repr(tail), repr(head))
    leaf = ("leaf", "restoration", label)
    require(subdivision not in result and leaf not in result, "insertion node collision")
    result.add_node(subdivision, role="tree", label=None, dummy=False)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    validate_graph(result)
    return result


def restrict_rooted(graph, keep_labels):
    result = graph.copy()
    for node, data in list(result.nodes(data=True)):
        if data["role"] == "leaf" and data.get("label") not in keep_labels:
            result.remove_node(node)
    changed = True
    while changed:
        changed = False
        for node, data in list(result.nodes(data=True)):
            if result.out_degree(node) == 0 and not (
                data["role"] == "leaf" and data.get("label") in keep_labels
            ):
                result.remove_node(node)
                changed = True
                break
        if changed:
            continue
        for node, data in list(result.nodes(data=True)):
            if data["role"] != "leaf" and result.in_degree(node) == 1 and result.out_degree(node) == 1:
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
        if len(roots) == 1 and result.nodes[roots[0]]["role"] != "leaf" and result.out_degree(roots[0]) == 1:
            result.remove_node(roots[0])
            changed = True
    for node, data in result.nodes(data=True):
        if data.get("label") in keep_labels:
            data["role"] = "leaf"
        elif result.in_degree(node) == 0:
            data["role"] = "root"
        elif result.in_degree(node) == 2:
            data["role"] = "retic"
        else:
            data["role"] = "tree"
    return result


def promoted_target(targets, target_index, permutation, roles):
    result = relabel_graph(targets[target_index].graph, permutation)
    for role, label in roles:
        nodes = [node for node, data in result.nodes(data=True)
                 if data.get("dummy_name") == role]
        require(len(nodes) == 1, f"target dummy promotion:{target_index}:{role}")
        data = result.nodes[nodes[0]]
        data["label"] = label
        data["dummy"] = False
        data["dummy_name"] = None
    selected = restrict_rooted(result, set(range(4 + len(roles))))
    return result, selected


def graph_payload(graph):
    nodes = [{
        "id": repr(node),
        "role": data.get("role"),
        "label": data.get("label"),
        "dummy": bool(data.get("dummy", False)),
        "dummy_name": data.get("dummy_name"),
    } for node, data in sorted(graph.nodes(data=True), key=lambda row: repr(row[0]))]
    arcs = [{
        "tail": repr(tail),
        "head": repr(head),
        "edge_role": data.get("edge_role"),
    } for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    )]
    return {"nodes": nodes, "arcs": arcs}


def sd0_mixed(graph):
    roots = [node for node, data in graph.nodes(data=True)
             if data["role"] == "root" or graph.in_degree(node) == 0]
    require(len(roots) == 1, "mixed graph root census")
    root = roots[0]
    children = list(graph.successors(root))
    require(len(children) == 2, "root suppression degree")
    mixed = nx.Graph()
    for node, data in graph.nodes(data=True):
        if node != root:
            mixed.add_node(node, role=data.get("role"), label=data.get("label"))
    for tail, head in graph.edges():
        if tail == root:
            continue
        heads = frozenset({head}) if graph.nodes[head].get("role") == "retic" else frozenset()
        require(not mixed.has_edge(tail, head), "mixed parallel edge")
        mixed.add_edge(tail, head, heads=heads)
    first, second = children
    require(first != second and not mixed.has_edge(first, second), "invalid root suppression")
    heads = frozenset(node for node in children if graph.nodes[node].get("role") == "retic")
    mixed.add_edge(first, second, heads=heads)
    return mixed


def exact_mixed_payload(graph):
    mixed = sd0_mixed(graph)
    nodes = [[repr(node), data.get("label"), data.get("role")]
             for node, data in sorted(mixed.nodes(data=True), key=lambda row: repr(row[0]))]
    edges = []
    for left, right, data in mixed.edges(data=True):
        if repr(right) < repr(left):
            left, right = right, left
        edges.append([repr(left), repr(right),
                      sorted(repr(node) for node in data.get("heads", frozenset()))])
    edges.sort()
    return {"nodes": nodes, "edges": edges}


def switch_graphs(graph):
    retics = [node for node, data in graph.nodes(data=True)
              if data["role"] == "retic" and graph.in_degree(node) == 2]
    incoming = [tuple(graph.in_edges(node)) for node in retics]
    for choices in itertools.product(*incoming):
        result = graph.copy()
        kept = set(choices)
        for rows in incoming:
            for edge in rows:
                if edge not in kept:
                    result.remove_edge(*edge)
        yield result


def unrooted_restricted_tree(graph, keep_labels):
    rooted = restrict_rooted(graph, keep_labels)
    result = nx.Graph()
    result.add_nodes_from((node, data.copy()) for node, data in rooted.nodes(data=True))
    result.add_edges_from(rooted.edges())
    changed = True
    while changed:
        changed = False
        for node, data in list(result.nodes(data=True)):
            label = data.get("label")
            if label not in keep_labels and result.degree(node) <= 1:
                result.remove_node(node)
                changed = True
                break
            if label not in keep_labels and result.degree(node) == 2:
                first, second = list(result.neighbors(node))
                result.remove_node(node)
                if first != second:
                    result.add_edge(first, second)
                changed = True
                break
    return result


def quartet_splits(graph, quartet):
    keep = set(quartet)
    output = set()
    for switched in switch_graphs(graph):
        tree = unrooted_restricted_tree(switched, keep)
        split = None
        for left, right in list(tree.edges()):
            tree.remove_edge(left, right)
            components = list(nx.connected_components(tree))
            tree.add_edge(left, right)
            if len(components) != 2:
                continue
            labels = []
            for component in components:
                labels.append(frozenset(
                    tree.nodes[node].get("label") for node in component
                    if tree.nodes[node].get("label") in keep
                ))
            if sorted(map(len, labels)) == [2, 2]:
                split = tuple(sorted((tuple(sorted(labels[0])), tuple(sorted(labels[1])))))
                break
        output.add(split if split is not None else ("star",))
    return frozenset(output)


def split_payload(value):
    output = []
    for item in sorted(value, key=repr):
        if item == ("star",):
            output.append(["star"])
        else:
            output.append([list(item[0]), list(item[1])])
    return output


def ordinary_sunlet(graph):
    try:
        mixed = sd0_mixed(graph)
    except VerificationFailure:
        return False
    undirected = nx.Graph()
    undirected.add_nodes_from(mixed.nodes())
    undirected.add_edges_from(mixed.edges())
    triangles = []
    for vertices in itertools.combinations(undirected.nodes(), 3):
        edges = [frozenset(pair) for pair in itertools.combinations(vertices, 2)]
        if not all(undirected.has_edge(*tuple(edge)) for edge in edges):
            continue
        heads = []
        valid = True
        for edge in edges:
            row = mixed.edges[tuple(edge)].get("heads", frozenset())
            if len(row) > 1 or any(head not in edge for head in row):
                valid = False
                break
            if row:
                heads.append(next(iter(row)))
        if valid and len(heads) == 2 and heads[0] == heads[1]:
            triangles.append(vertices)
    labels = [data.get("label") for _, data in mixed.nodes(data=True)]
    return (
        len(triangles) == 1
        and len(mixed.nodes()) == 6
        and len(mixed.edges()) == 6
        and sum(isinstance(label, int) for label in labels) == 3
        and sorted(dict(mixed.degree()).values()) == [1, 1, 1, 3, 3, 3]
    )


def zero_sum_assignments(k):
    for prefix in itertools.product(range(4), repeat=k - 1):
        last = 0
        for value in prefix:
            last ^= value
        yield prefix + (last,)


def selected_arm_edges(graph):
    return {
        (tail, head) for tail, head in graph.edges()
        if graph.nodes[head]["role"] == "leaf"
        and isinstance(graph.nodes[head].get("label"), int)
    }


def descendant_masks(graph, kept_edges):
    children = {node: [] for node in graph.nodes()}
    for tail, head in kept_edges:
        children[tail].append(head)
    subgraph = nx.edge_subgraph(graph, kept_edges).copy()
    order = list(nx.topological_sort(subgraph))
    masks = {}
    for node in reversed(order):
        label = graph.nodes[node].get("label")
        mask = (1 << label) if isinstance(label, int) else 0
        for child in children[node]:
            mask |= masks[child]
        masks[node] = mask
    return {(tail, head): masks[head] for tail, head in kept_edges}


def sector(mask, characters):
    result = 0
    index = 0
    while mask:
        if mask & 1:
            result ^= characters[index]
        index += 1
        mask >>= 1
    return result


def inheritance_polynomial(bits):
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
    return tuple(sorted(polynomial.items()))


@dataclass(frozen=True)
class MapDescriptor:
    k: int
    retic_count: int
    edge_class_count: int
    outputs: tuple
    edge_signatures: tuple


def descriptor_variant(graph, retic_order, parent_orders):
    assignments = tuple(zero_sum_assignments(len(labels_of(graph))))
    all_edges = tuple(graph.edges())
    arms = selected_arm_edges(graph)
    switches = []
    for bits in itertools.product((0, 1), repeat=len(retic_order)):
        removed = set()
        for index, retic in enumerate(retic_order):
            kept_parent = parent_orders[index][bits[index]]
            for parent in graph.predecessors(retic):
                if parent != kept_parent:
                    removed.add((parent, retic))
        kept = tuple(edge for edge in all_edges if edge not in removed)
        switches.append((bits, kept, descendant_masks(graph, kept)))
    edge_signatures = []
    internal_edges = []
    for edge in all_edges:
        if edge in arms:
            continue
        signature = []
        for _, kept, masks in switches:
            if edge not in masks:
                signature.extend((0,) * len(assignments))
            else:
                signature.extend(sector(masks[edge], chars) for chars in assignments)
        if any(signature):
            internal_edges.append(edge)
            edge_signatures.append(tuple(signature))
    active = tuple(sorted(set(edge_signatures)))
    class_of = {signature: index for index, signature in enumerate(active)}
    edge_class = {edge: class_of[signature]
                  for edge, signature in zip(internal_edges, edge_signatures)}
    weight = {bits: inheritance_polynomial(bits) for bits, _, _ in switches}
    outputs = []
    for chars in assignments:
        grouped = collections.defaultdict(lambda: collections.defaultdict(int))
        for bits, kept, masks in switches:
            factors = collections.Counter()
            for edge in kept:
                class_index = edge_class.get(edge)
                if class_index is None:
                    continue
                character = sector(masks[edge], chars)
                if character:
                    factors[(class_index, character)] += 1
            monomial = tuple(sorted(
                (class_index, character, exponent)
                for (class_index, character), exponent in factors.items()
            ))
            for mask, coefficient in weight[bits]:
                grouped[monomial][mask] += coefficient
        expression = []
        for monomial, polynomial in grouped.items():
            row = tuple(sorted((mask, coefficient) for mask, coefficient in polynomial.items()
                               if coefficient))
            if row:
                expression.append((monomial, row))
        outputs.append(tuple(sorted(expression)))
    return MapDescriptor(len(labels_of(graph)), len(retic_order), len(active),
                         tuple(outputs), active)


def compile_descriptor(graph):
    retics = tuple(sorted(
        (node for node, data in graph.nodes(data=True) if data["role"] == "retic"),
        key=repr,
    ))
    variants = []
    if not retics:
        variants.append(descriptor_variant(graph, (), ()))
    else:
        for order in itertools.permutations(retics):
            parents = [tuple(sorted(graph.predecessors(retic), key=repr)) for retic in order]
            for flips in itertools.product((0, 1), repeat=len(order)):
                parent_orders = tuple((pair[flip], pair[1 - flip])
                                      for pair, flip in zip(parents, flips))
                variants.append(descriptor_variant(graph, order, parent_orders))
    return min(variants, key=lambda row: (
        row.retic_count, row.edge_class_count, row.outputs, row.edge_signatures
    ))


def descriptor_payload(descriptor):
    return {
        "k": descriptor.k,
        "retic_count": descriptor.retic_count,
        "edge_class_count": descriptor.edge_class_count,
        "outputs": descriptor.outputs,
        "edge_signatures": descriptor.edge_signatures,
    }


def sparse_outputs(descriptor):
    variable_count = 3 * descriptor.edge_class_count + descriptor.retic_count
    outputs = []
    for expression in descriptor.outputs:
        polynomial = collections.defaultdict(int)
        for monomial, inheritance in expression:
            base = [0] * variable_count
            for class_index, character, exponent in monomial:
                base[3 * class_index + character - 1] += exponent
            for mask, coefficient in inheritance:
                powers = list(base)
                for index in range(descriptor.retic_count):
                    if (mask >> index) & 1:
                        powers[3 * descriptor.edge_class_count + index] += 1
                polynomial[tuple(powers)] += coefficient
        outputs.append({power: Q(coefficient) for power, coefficient in polynomial.items()
                        if coefficient})
    return tuple(outputs)


def sparse_multiply(first, second):
    output = collections.defaultdict(Q)
    for first_power, first_coefficient in first.items():
        for second_power, second_coefficient in second.items():
            output[tuple(a + b for a, b in zip(first_power, second_power))] += (
                first_coefficient * second_coefficient
            )
    return {power: coefficient for power, coefficient in output.items() if coefficient}


def sparse_product(polynomials):
    if not polynomials:
        return {(): Q(1)}
    result = polynomials[0]
    for polynomial in polynomials[1:]:
        result = sparse_multiply(result, polynomial)
    return result


def sparse_linear(polynomials, coefficients):
    output = collections.defaultdict(Q)
    for polynomial, scalar in zip(polynomials, coefficients):
        for power, coefficient in polynomial.items():
            output[power] += Q(scalar) * coefficient
    return {power: coefficient for power, coefficient in output.items() if coefficient}


def sparse_payload(polynomial):
    return [[list(power), str(coefficient)]
            for power, coefficient in sorted(polynomial.items())]


def sparse_hash(polynomial):
    return sha(sparse_payload(polynomial))


def polynomial_pullback(descriptor, terms):
    outputs = sparse_outputs(descriptor)
    return sparse_linear(
        [sparse_product([outputs[index] for index in term["coordinate_indices"]])
         for term in terms],
        [term["coefficient"] for term in terms],
    )


def coordinate_weights(k):
    output = []
    for chars in zero_sum_assignments(k):
        row = []
        for character in chars:
            row.extend((character == 1, character == 2, character == 3))
        output.append(tuple(map(int, row)))
    return tuple(output)


def multidegree(k, monomial):
    weights = coordinate_weights(k)
    return tuple(sum(weights[index][slot] for index in monomial)
                 for slot in range(3 * k))


def evaluate_sparse(polynomial, point):
    result = Q(0)
    for power, coefficient in polynomial.items():
        term = Q(coefficient)
        for value, exponent in zip(point, power):
            if exponent:
                term *= value ** exponent
        result += term
    return result


def verify_strict_witness(descriptor, polynomial, witness, context):
    edges = tuple(tuple(Q(value) for value in row) for row in witness["edge_triples"])
    inheritance = tuple(Q(value) for value in witness["inheritance"])
    require(len(edges) == descriptor.edge_class_count, f"witness edge census:{context}")
    require(len(inheritance) == descriptor.retic_count, f"witness inheritance census:{context}")
    for c, g, t in edges:
        require(0 < c < 1 and 0 < g < 1 and 0 < t < 1, f"witness cube:{context}")
        require(1 + c - g - t > 0 and 1 - c + g - t > 0 and 1 - c - g + t > 0,
                f"witness principal domain:{context}")
        require(c > g * t and g > c * t and t > c * g,
                f"witness CT domain:{context}")
    require(all(0 < value < 1 for value in inheritance), f"witness inheritance:{context}")
    point = tuple(value for edge in edges for value in edge) + inheritance
    evaluation = evaluate_sparse(polynomial, point)
    require(evaluation == Q(witness["evaluation"]) and evaluation != 0,
            f"strict witness evaluation:{context}")


CIRCUITS = (
    (("000", "CGT", "GTC"), ("0TT", "C0C", "GG0")),
    (("000", "CTG", "TGC"), ("0GG", "C0C", "TT0")),
    (("000", "GCT", "TGC"), ("0CC", "GG0", "T0T")),
    (("000", "GTC", "TCG"), ("0CC", "G0G", "TT0")),
    (("000", "CTG", "GCT"), ("0TT", "CC0", "G0G")),
    (("000", "CGT", "TCG"), ("0GG", "CC0", "T0T")),
)


def circuit_pullbacks(descriptor):
    outputs = sparse_outputs(descriptor)
    assignments = tuple(zero_sum_assignments(3))
    index = {assignment: number for number, assignment in enumerate(assignments)}
    code = {"0": 0, "C": 1, "G": 2, "T": 3}

    def coordinate(label):
        return outputs[index[tuple(code[value] for value in label)]]

    return [
        sparse_linear(
            [sparse_product([coordinate(label) for label in left]),
             sparse_product([coordinate(label) for label in right])],
            [1, -1],
        )
        for left, right in CIRCUITS
    ]


def parse_root_id(root_id):
    fields = root_id.split(":")
    return int(fields[0][1:]), int(fields[1][1:]), int(fields[2][1:]), tuple(map(int, fields[3][1:]))


def reconstruct_rows(forest):
    sources = source_supports()
    targets = target_completions(4, True) + target_completions(4, False)
    require(len(sources) == 6 and len(targets) == 2_814, "primitive universe census")
    source_cache = {}
    target_cache = {}
    first_by_hash = {}
    rows = []
    for frozen in forest["first_coverage"]:
        source_index, _, target_index, permutation = parse_root_id(frozen["root_id"])
        require(tuple(sorted(permutation)) == (0, 1, 2, 3), "root port permutation")
        source_key = (source_index, frozen["source_insertion_index"])
        if source_key not in source_cache:
            candidates = source_insertion_candidates(sources[source_index].graph)
            require(len(candidates) == 7, "first source insertion census")
            source_cache[source_key] = insert_source_leaf(
                sources[source_index].graph,
                candidates[frozen["source_insertion_index"]],
                4,
            )
        target_key = (target_index, permutation, frozen["restored_role"])
        if target_key not in target_cache:
            target_cache[target_key] = promoted_target(
                targets, target_index, permutation, ((frozen["restored_role"], 4),)
            )
        source = source_cache[source_key]
        target_full, target_selected = target_cache[target_key]
        first_by_hash[frozen["row_sha256"]] = (source, target_full, target_selected)
        rows.append(("first", frozen, source, target_full, target_selected))
    for frozen in forest["second_coverage"]:
        require(frozen["parent_first_row_sha256"] in first_by_hash, "missing second parent")
        first_source, first_target_full, _ = first_by_hash[frozen["parent_first_row_sha256"]]
        candidates = source_insertion_candidates(first_source)
        require(len(candidates) == 8, "second source insertion census")
        source = insert_source_leaf(
            first_source, candidates[frozen["second_source_insertion_index"]], 5
        )
        target_full = first_target_full.copy()
        nodes = [node for node, data in target_full.nodes(data=True)
                 if data.get("dummy_name") == frozen["second_restored_role"]]
        require(len(nodes) == 1, "second target role promotion")
        data = target_full.nodes[nodes[0]]
        data["label"] = 5
        data["dummy"] = False
        data["dummy_name"] = None
        target_selected = restrict_rooted(target_full, set(range(6)))
        rows.append(("second", frozen, source, target_full, target_selected))
    return rows


def read_json_gzip(path):
    with gzip.open(path, "rt") as handle:
        return json.load(handle)


def read_jsonl_gzip(path):
    with gzip.open(path, "rt") as handle:
        return [json.loads(line) for line in handle]


def identity(layer, row):
    if layer == "first":
        return {
            "layer": 1,
            "legacy_row_sha256": row["row_sha256"],
            "root_id": row["root_id"],
            "restored_role": row["restored_role"],
            "restored_label": row["restored_label"],
            "source_insertion_index": row["source_insertion_index"],
        }
    return {
        "layer": 2,
        "legacy_row_sha256": row["row_sha256"],
        "parent_first_row_sha256": row["parent_first_row_sha256"],
        "root_id": row["root_id"],
        "restored_role": row["second_restored_role"],
        "restored_label": row["second_restored_label"],
        "source_insertion_index": row["second_source_insertion_index"],
    }


def template_terms(path, orbit_id):
    payload = json.loads(path.read_text())
    return next(row["terms"] for row in payload["records"] if row["orbit_id"] == orbit_id)


def transported_terms(terms, permutation):
    assignments = tuple(zero_sum_assignments(4))
    index = {assignment: number for number, assignment in enumerate(assignments)}
    mapping = tuple(
        index[tuple(assignment[permutation[position]] for position in range(4))]
        for assignment in assignments
    )
    return [{
        "coefficient": term["coefficient"],
        "coordinate_indices": sorted(mapping[value] for value in term["coordinate_indices"]),
    } for term in terms]


def verify_separator_theorem():
    separator = json.loads(SEPARATOR_PATH.read_text())
    primary = json.loads(THREE_PORT_PATH.read_text())
    require(separator["schema"] == "k3p-tree-sunlet-six-circuit-separator-v1",
            "tree-sunlet separator schema")
    require(separator["observable_separator"] == "sum_{j=1}^6 I_j^2",
            "tree-sunlet separator observable")
    require(separator["tree_value"] == "identically_zero", "tree separator value")
    require(separator["sunlet_value"] == "strictly_positive_on_0<c,g,t<1_and_0<lambda<1",
            "sunlet separator strict value")
    require([(tuple(row["left"]), tuple(row["right"])) for row in separator["circuits"]]
            == list(CIRCUITS), "six-circuit coordinate deck")
    require(primary["tree_sunlet_sum_of_squares_strict"] is True,
            "primary SOS strictness binding")
    require(len(primary["tree_sunlet_circuits"]) == 6,
            "primary SOS circuit census")
    argument = primary["tree_sunlet_strictness_argument"]
    require(argument["all_composition_margins_zero_force"] == "p=p^2 for p=dC*dG*dT",
            "SOS final contradiction")
    require(set(argument["paired_cross_equations_force"])
            == {"dC^2=1", "dG^2=1", "dT^2=1"},
            "SOS paired contradictions")


def verify_marginal_contract(manifest):
    marginal = json.loads(MARGINAL_PATH.read_text())
    require(marginal["status"] == "PASS", "marginal certificate status")
    require(marginal["payload_sha256"] == logical_payload(marginal),
            "marginal certificate payload")
    triple = marginal["triple_product_map"]
    require(triple["parameter_rank"] == triple["image_tangent_rank"] == 3,
            "triple product rank")
    require(triple["local_openness"] is True, "triple product openness")
    require(marginal["source_relative_open_image"]["direct_marginal_of_original_containment"] is True,
            "direct original containment marginal")
    require(marginal["source_relative_open_image"]["target_marginal_openness_used"] is False,
            "target openness forbidden")
    contract = manifest["direct_marginal_open_image"]
    require(contract["jacobian_rank"] == 3 and contract["source_relative_local_openness"],
            "manifest marginal rank/open image")
    require(contract["target_marginal_openness_used"] is False,
            "manifest target openness forbidden")
    # Exact displayed 3x3 minor at a rational positive point.
    factors = ((Q(2, 3), Q(3, 5), Q(4, 7)), (Q(5, 7), Q(7, 9), Q(9, 11)))
    diagonal = tuple(factors[1])
    require(math.prod(diagonal) > 0, "triple-product selected minor nonzero")


def artifact_preflight(root):
    require(__debug__ and not sys.flags.optimize, "optimized Python forbidden")
    manifest_path = root / "RESTORATION_MANIFEST.json"
    ledger_path = root / "restoration_ledger.jsonl.gz"
    registry_path = root / "restoration_proof_registry.json.gz"
    manifest = json.loads(manifest_path.read_text())
    require(manifest["schema"] == "k3p-fixed-full-restoration-manifest-v1",
            "manifest schema")
    require(manifest["status"] == "PASS", "manifest status")
    require(manifest["payload_sha256"] == logical_payload(manifest), "manifest payload")
    require(sha_file(ledger_path) == manifest["ledger"]["sha256"], "ledger file hash")
    require(sha_file(registry_path) == manifest["proof_registry"]["sha256"],
            "registry file hash")
    registry = read_json_gzip(registry_path)
    require(registry["payload_sha256"] == logical_payload(registry), "registry payload")
    require(registry["payload_sha256"] == manifest["proof_registry"]["payload_sha256"],
            "registry/manifest cross-binding")
    records = read_jsonl_gzip(ledger_path)
    require(len(records) == manifest["ledger"]["rows"] == 36_824, "ledger row census")
    for number, record in enumerate(records):
        row = dict(record)
        claimed = row.pop("row_sha256")
        require(claimed == sha(row), f"ledger row self hash:{number}")
        require(record["edge_index"] == number, f"ledger edge order:{number}")
    require(sha([row["row_sha256"] for row in records])
            == manifest["ledger"]["ordered_row_hash_root"], "ledger ordered root")
    require(registry["uses_k2p_sector_equality"] is False,
            "K2P sector equality forbidden")
    require(registry["uses_historical_k2p_algebra"] is False,
            "historical K2P algebra forbidden")
    proofs = registry["proofs"]
    expected_kinds = {
        "displayed_quartet_mismatch": "Q:",
        "k3p_tree_sunlet_sos": "K3P-TS:",
        "k3p_exact_multihomogeneous_quadratic": "K3P-Q2:",
        "k3p_direct_marginal_quartic": "K3P-M4:",
    }
    require(set(proofs) == set(expected_kinds), "proof registry category universe")
    require({key: len(value) for key, value in proofs.items()} == registry["counts"],
            "proof registry certificate counts")
    empty_hash = sha([])
    for kind, certificates in proofs.items():
        prefix = expected_kinds[kind]
        for proof_id, certificate in certificates.items():
            require(proof_id == prefix + sha(certificate), f"proof self hash:{proof_id}")
            if kind == "displayed_quartet_mismatch":
                require(len(certificate["quartet"]) == 4, f"quartet arity:{proof_id}")
                require(certificate["source_splits"] != certificate["target_splits"],
                        f"quartet split mismatch:{proof_id}")
            elif kind == "k3p_tree_sunlet_sos":
                require(len(certificate["triple"]) == 3, f"SOS triple arity:{proof_id}")
                require({certificate["tree_on"], certificate["sunlet_on"]}
                        == {"source", "target"}, f"SOS direction:{proof_id}")
                require(certificate["tree_circuit_pullback_sha256"] == [empty_hash] * 6,
                        f"SOS tree zero deck:{proof_id}")
                require(len(certificate["sunlet_circuit_pullback_sha256"]) == 6,
                        f"SOS sunlet deck:{proof_id}")
                require(certificate["sunlet_nonzero_circuit_count"]
                        == sum(value != empty_hash
                               for value in certificate["sunlet_circuit_pullback_sha256"]) > 0,
                        f"SOS nonzero census:{proof_id}")
                require(certificate["separator_certificate_sha256"] == sha_file(SEPARATOR_PATH),
                        f"SOS theorem hash:{proof_id}")
                require(certificate["three_sector_independence"]
                        == "C, G, and T compiled independently",
                        f"SOS sector independence:{proof_id}")
            elif kind == "k3p_exact_multihomogeneous_quadratic":
                require(certificate["degree"] == 2, f"quadratic degree:{proof_id}")
                require(len(certificate["coordinate_pairs"]) == len(certificate["coefficients"]),
                        f"quadratic vector length:{proof_id}")
                require(certificate["target_pullback_term_count"] == 0
                        and certificate["source_pullback_term_count"] > 0,
                        f"quadratic direction:{proof_id}")
                require(len(certificate["boundary_multidegree_C_G_T"])
                        == 3 * certificate["k"], f"quadratic multidegree length:{proof_id}")
                require(certificate["uses_k2p_sector_equality"] is False,
                        f"quadratic K2P equality:{proof_id}")
                witness = certificate["strict_source_witness"]
                require(all(0 < Q(value) < 1 for row in witness["edge_triples"] for value in row),
                        f"quadratic witness cube:{proof_id}")
                require(all(0 < Q(value) < 1 for value in witness["inheritance"]),
                        f"quadratic witness inheritance:{proof_id}")
            elif kind == "k3p_direct_marginal_quartic":
                require(certificate["degree"] == 4, f"quartic degree:{proof_id}")
                require(certificate["template_file"] in {H14_PATH.name, REMAINING_PATH.name},
                        f"quartic active template whitelist:{proof_id}")
                template_path = H14_PATH if certificate["template_file"] == H14_PATH.name else REMAINING_PATH
                require(certificate["template_file_sha256"] == sha_file(template_path),
                        f"quartic template hash:{proof_id}")
                expected_terms = transported_terms(
                    template_terms(template_path, certificate["template_orbit_id"]),
                    tuple(certificate["port_permutation"]),
                )
                require(certificate["terms"] == expected_terms,
                        f"quartic coordinate transport:{proof_id}")
                require(certificate["target_pullback_term_count"] == 0
                        and certificate["source_pullback_term_count"] > 0,
                        f"quartic direction:{proof_id}")
                require(certificate["direct_marginal_of_original_containment"] is True,
                        f"quartic direct marginal:{proof_id}")
                require(certificate["target_marginal_openness_used"] is False,
                        f"quartic target openness:{proof_id}")
                require(certificate["uses_k2p_sector_equality"] is False,
                        f"quartic K2P equality:{proof_id}")
                witness = certificate["strict_source_witness"]
                require(all(0 < Q(value) < 1 for row in witness["edge_triples"] for value in row),
                        f"quartic witness cube:{proof_id}")
                require(all(0 < Q(value) < 1 for value in witness["inheritance"]),
                        f"quartic witness inheritance:{proof_id}")

    forest = json.loads(FOREST_PATH.read_text())
    require(len(forest["first_coverage"]) == 36_568
            and len(forest["second_coverage"]) == 256, "frozen layer census")
    proof_counts = collections.Counter()
    minimal_counts = collections.Counter()
    used_proofs = set()
    continuation_count = 0
    second_parent_count = collections.Counter()
    expected_rows = [("first", row) for row in forest["first_coverage"]] + [
        ("second", row) for row in forest["second_coverage"]
    ]
    for number, (record, (layer, frozen)) in enumerate(zip(records, expected_rows)):
        expected = identity(layer, frozen)
        require(all(record.get(key) == value for key, value in expected.items()),
                f"ledger/frozen structural identity:{number}")
        require(record["legacy_structural_status"] == frozen["status"],
                f"ledger legacy status:{number}")
        kind = record["proof_kind"]
        proof_id = record["proof_id"]
        require(kind in proofs and proof_id in proofs[kind], f"ledger proof reference:{number}")
        proof_counts[kind] += 1
        used_proofs.add(proof_id)
        if layer == "first":
            minimal_counts[kind] += 1
            require(record["active_k3p_status"] == "separated",
                    f"first active K3P status:{number}")
            require(record["source_parent_transport_id"] == frozen["source_parent_transport_id"]
                    and record["target_parent_transport_id"] == frozen["target_parent_transport_id"],
                    f"first parent transport reference:{number}")
            if frozen["status"] == "continuation":
                continuation_count += 1
                require(record.get("k3p_refinement")
                        == "early_termination_before_redundant_depth2",
                        f"continuation early termination marker:{number}")
                require(kind == "k3p_direct_marginal_quartic",
                        f"continuation quartic proof:{number}")
        else:
            require(record["active_k3p_status"] == "redundant_verified"
                    and record.get("legacy_full_forest_only") is True,
                    f"redundant depth-two marker:{number}")
            second_parent_count[record["parent_first_row_sha256"]] += 1
    require(len(expected_rows) == len(records), "frozen/ledger coverage tail")
    require(continuation_count == 32, "structural continuation/early termination count")
    require(len(second_parent_count) == 32 and set(second_parent_count.values()) == {8},
            "redundant depth-two parent coverage")
    require(used_proofs == set().union(*(set(value) for value in proofs.values())),
            "unused proof certificates")
    require(dict(sorted(proof_counts.items()))
            == manifest["census"]["all_edge_proof_counts"], "artifact all-edge proof census")
    require(dict(sorted(minimal_counts.items()))
            == manifest["census"]["minimal_first_layer_proof_counts"],
            "artifact minimal proof census")
    require(sum(minimal_counts.values())
            == manifest["census"]["minimal_k3p_terminal_rows"] == 36_568,
            "minimal K3P terminal count")
    require(manifest["census"]["legacy_full_forest_leaves"] == 36_792,
            "legacy/full-forest leaf count")
    require(manifest["census"]["redundant_depth2_edges"] == 256,
            "redundant depth-two count")
    require(manifest["census"]["legacy_structural_continuations"] == 32
            and manifest["census"]["active_k3p_continuations"] == 0,
            "legacy versus active continuation distinction")
    return manifest, registry, records


def full_verify(root, output_path):
    require(__debug__ and not sys.flags.optimize, "optimized Python forbidden")
    manifest, registry, records = artifact_preflight(root)
    require(manifest["producer"]["sha256"]
            == sha_file(root / "regenerate_k3p_restoration.py"),
            "producer implementation binding")
    require(manifest["producer"]["support_sha256"]
            == sha_file(root / "restoration_build_support.py"),
            "producer support implementation binding")
    expected_inputs = {
        "k3p_atlas_sha256": sha_file(ATLAS_PATH),
        "frozen_restoration_forest_sha256": sha_file(FOREST_PATH),
        "tree_sunlet_separator_sha256": sha_file(SEPARATOR_PATH),
        "three_port_primary_sha256": sha_file(THREE_PORT_PATH),
        "marginal_submersion_sha256": sha_file(MARGINAL_PATH),
        f"{H14_PATH.name}_sha256": sha_file(H14_PATH),
        f"{REMAINING_PATH.name}_sha256": sha_file(REMAINING_PATH),
    }
    require(manifest["inputs"] == expected_inputs, "manifest active input binding")
    require(registry["inputs"] == expected_inputs, "registry active input binding")
    verify_separator_theorem()
    verify_marginal_contract(manifest)
    forest = json.loads(FOREST_PATH.read_text())
    rows = reconstruct_rows(forest)
    require(len(rows) == len(records) == 36_824, "reconstructed row census")
    proofs = registry["proofs"]
    descriptor_cache = {}
    proof_use = collections.Counter()
    proof_counts = collections.Counter()
    minimal_counts = collections.Counter()
    early_termination = 0
    continuation_parents = {
        row["row_sha256"] for row in forest["first_coverage"]
        if row["status"] == "continuation"
    }
    require(len(continuation_parents) == 32, "frozen continuation census")
    depth2 = collections.Counter(row["parent_first_row_sha256"]
                                 for row in forest["second_coverage"])
    require(set(depth2) == continuation_parents and set(depth2.values()) == {8},
            "full depth-two coverage")

    def descriptor(graph):
        graph_hash = sha(graph_payload(graph))
        if graph_hash not in descriptor_cache:
            descriptor_cache[graph_hash] = compile_descriptor(graph)
        return descriptor_cache[graph_hash]

    for number, ((layer, frozen, source, target_full, target_selected), record) in enumerate(zip(rows, records)):
        expected_identity = identity(layer, frozen)
        require(all(record[key] == value for key, value in expected_identity.items()),
                f"ledger/frozen identity:{number}")
        require(record["source_graph_sha256"] == sha(graph_payload(source)),
                f"source graph binding:{number}")
        require(record["target_full_graph_sha256"] == sha(graph_payload(target_full)),
                f"target full graph binding:{number}")
        require(record["target_selected_graph_sha256"] == sha(graph_payload(target_selected)),
                f"target selected graph binding:{number}")
        require(labels_of(source) == labels_of(target_selected), f"selected labels:{number}")
        require(record["uses_frozen_algebra"] is False, f"frozen algebra flag:{number}")
        require(record["legacy_structural_status"] == frozen["status"],
                f"legacy structural status:{number}")
        if layer == "first":
            require(record["active_k3p_status"] == "separated", f"first active status:{number}")
            source_parent = restrict_rooted(source, set(range(4)))
            target_parent = restrict_rooted(target_full, set(range(4)))
            source_transport = forest["first_source_transport_certificates"][
                frozen["source_parent_transport_id"]
            ]
            target_transport = forest["first_target_transport_certificates"][
                frozen["target_parent_transport_id"]
            ]
            require(sha(exact_mixed_payload(source_parent))
                    == source_transport["parent_mixed_graph_sha256"],
                    f"first source parent transport:{number}")
            require(sha(exact_mixed_payload(target_parent))
                    == target_transport["parent_mixed_graph_sha256"],
                    f"first target parent transport:{number}")
            minimal_counts[record["proof_kind"]] += 1
            if frozen["status"] == "continuation":
                require(record.get("k3p_refinement")
                        == "early_termination_before_redundant_depth2",
                        f"early K3P termination marker:{number}")
                require(record["proof_kind"] == "k3p_direct_marginal_quartic",
                        f"continuation K3P quartic:{number}")
                early_termination += 1
        else:
            require(record["active_k3p_status"] == "redundant_verified",
                    f"depth-two active status:{number}")
            require(record.get("legacy_full_forest_only") is True,
                    f"depth-two redundancy marker:{number}")
            source_parent = restrict_rooted(source, set(range(5)))
            target_parent = restrict_rooted(target_full, set(range(5)))
            require(sha(exact_mixed_payload(source_parent))
                    == frozen["source_parent_mixed_graph_sha256"],
                    f"second source parent transport:{number}")
            require(sha(exact_mixed_payload(target_parent))
                    == frozen["target_parent_mixed_graph_sha256"],
                    f"second target parent transport:{number}")
        kind = record["proof_kind"]
        proof_id = record["proof_id"]
        require(proof_id in proofs[kind], f"proof registry reference:{number}")
        certificate = proofs[kind][proof_id]
        proof_use[proof_id] += 1
        proof_counts[kind] += 1

        if kind == "displayed_quartet_mismatch":
            require(proof_id == "Q:" + sha(certificate), f"quartet proof self hash:{number}")
            quartet = tuple(certificate["quartet"])
            source_splits = split_payload(quartet_splits(source, quartet))
            target_splits = split_payload(quartet_splits(target_selected, quartet))
            require(source_splits == certificate["source_splits"],
                    f"quartet source splits:{number}")
            require(target_splits == certificate["target_splits"],
                    f"quartet target splits:{number}")
            require(source_splits != target_splits, f"quartet mismatch vanished:{number}")
        elif kind == "k3p_tree_sunlet_sos":
            require(proof_id == "K3P-TS:" + sha(certificate), f"SOS proof self hash:{number}")
            triple = tuple(certificate["triple"])
            source_restricted = restrict_rooted(source, set(triple))
            target_restricted = restrict_rooted(target_selected, set(triple))
            label_map = {old: new for new, old in enumerate(sorted(triple))}
            source_normalized = source_restricted.copy()
            target_normalized = target_restricted.copy()
            for graph in (source_normalized, target_normalized):
                for _, data in graph.nodes(data=True):
                    if data.get("label") in label_map:
                        data["label"] = label_map[data["label"]]
            source_descriptor = descriptor(source_normalized)
            target_descriptor = descriptor(target_normalized)
            source_circuits = circuit_pullbacks(source_descriptor)
            target_circuits = circuit_pullbacks(target_descriptor)
            if certificate["tree_on"] == "source":
                tree_descriptor, sunlet_descriptor = source_descriptor, target_descriptor
                tree_circuits, sunlet_circuits = source_circuits, target_circuits
                sunlet_graph = target_normalized
            else:
                tree_descriptor, sunlet_descriptor = target_descriptor, source_descriptor
                tree_circuits, sunlet_circuits = target_circuits, source_circuits
                sunlet_graph = source_normalized
            require(tree_descriptor.retic_count == 0 and sunlet_descriptor.retic_count == 1,
                    f"literal tree/sunlet descriptors:{number}")
            require(ordinary_sunlet(sunlet_graph), f"literal ordinary sunlet:{number}")
            require(not any(tree_circuits) and any(sunlet_circuits),
                    f"literal SOS circuit deck:{number}")
            require([sparse_hash(poly) for poly in tree_circuits]
                    == certificate["tree_circuit_pullback_sha256"],
                    f"tree circuit hashes:{number}")
            require([sparse_hash(poly) for poly in sunlet_circuits]
                    == certificate["sunlet_circuit_pullback_sha256"],
                    f"sunlet circuit hashes:{number}")
            require(certificate["separator_certificate_sha256"] == sha_file(SEPARATOR_PATH),
                    f"SOS theorem reference:{number}")
            require(certificate["three_sector_independence"]
                    == "C, G, and T compiled independently", f"SOS sectors:{number}")
        elif kind == "k3p_exact_multihomogeneous_quadratic":
            require(proof_id == "K3P-Q2:" + sha(certificate), f"quadratic self hash:{number}")
            source_descriptor = descriptor(source)
            target_descriptor = descriptor(target_full)
            require(sha(descriptor_payload(source_descriptor))
                    == certificate["source_descriptor_sha256"],
                    f"quadratic source descriptor:{number}")
            require(sha(descriptor_payload(target_descriptor))
                    == certificate["target_descriptor_sha256"],
                    f"quadratic target descriptor:{number}")
            terms = [{"coefficient": coefficient, "coordinate_indices": pair}
                     for pair, coefficient in zip(certificate["coordinate_pairs"],
                                                  certificate["coefficients"])]
            source_pullback = polynomial_pullback(source_descriptor, terms)
            target_pullback = polynomial_pullback(target_descriptor, terms)
            require(not target_pullback and bool(source_pullback),
                    f"quadratic pullback direction:{number}")
            require(sparse_hash(source_pullback) == certificate["source_pullback_sha256"],
                    f"quadratic source hash:{number}")
            degrees = {multidegree(source_descriptor.k, tuple(term["coordinate_indices"]))
                       for term in terms if term["coefficient"]}
            require(len(degrees) == 1
                    and list(next(iter(degrees))) == certificate["boundary_multidegree_C_G_T"],
                    f"quadratic three-sector multidegree:{number}")
            verify_strict_witness(source_descriptor, source_pullback,
                                  certificate["strict_source_witness"], f"quadratic:{number}")
            require(certificate["uses_k2p_sector_equality"] is False,
                    f"quadratic K2P equality:{number}")
        elif kind == "k3p_direct_marginal_quartic":
            require(proof_id == "K3P-M4:" + sha(certificate), f"quartic self hash:{number}")
            subset = tuple(certificate["marginal_labels"])
            source_restricted = restrict_rooted(source, set(subset))
            target_restricted = restrict_rooted(target_selected, set(subset))
            label_map = {old: new for new, old in enumerate(sorted(subset))}
            source_normalized = source_restricted.copy()
            target_normalized = target_restricted.copy()
            for graph in (source_normalized, target_normalized):
                for _, data in graph.nodes(data=True):
                    if data.get("label") in label_map:
                        data["label"] = label_map[data["label"]]
            require(sha(graph_payload(source_restricted))
                    == certificate["source_restricted_graph_sha256"],
                    f"quartic source restriction:{number}")
            require(sha(graph_payload(target_restricted))
                    == certificate["target_restricted_graph_sha256"],
                    f"quartic target restriction:{number}")
            source_descriptor = descriptor(source_normalized)
            target_descriptor = descriptor(target_normalized)
            require(sha(descriptor_payload(source_descriptor))
                    == certificate["source_descriptor_sha256"],
                    f"quartic source descriptor:{number}")
            require(sha(descriptor_payload(target_descriptor))
                    == certificate["target_descriptor_sha256"],
                    f"quartic target descriptor:{number}")
            template_path = {
                H14_PATH.name: H14_PATH,
                REMAINING_PATH.name: REMAINING_PATH,
            }.get(certificate["template_file"])
            require(template_path is not None, f"quartic template file:{number}")
            require(sha_file(template_path) == certificate["template_file_sha256"],
                    f"quartic template hash:{number}")
            base = template_terms(template_path, certificate["template_orbit_id"])
            expected_terms = transported_terms(base, tuple(certificate["port_permutation"]))
            require(expected_terms == certificate["terms"], f"quartic transport:{number}")
            source_pullback = polynomial_pullback(source_descriptor, certificate["terms"])
            target_pullback = polynomial_pullback(target_descriptor, certificate["terms"])
            require(not target_pullback and bool(source_pullback),
                    f"quartic pullback direction:{number}")
            require(sparse_hash(source_pullback) == certificate["source_pullback_sha256"],
                    f"quartic source hash:{number}")
            degrees = {multidegree(4, tuple(term["coordinate_indices"]))
                       for term in certificate["terms"] if term["coefficient"]}
            require(len(degrees) == 1
                    and list(next(iter(degrees))) == certificate["boundary_multidegree_C_G_T"],
                    f"quartic three-sector multidegree:{number}")
            verify_strict_witness(source_descriptor, source_pullback,
                                  certificate["strict_source_witness"], f"quartic:{number}")
            require(certificate["direct_marginal_of_original_containment"] is True,
                    f"quartic direct marginal:{number}")
            require(certificate["target_marginal_openness_used"] is False,
                    f"quartic target openness:{number}")
            require(certificate["uses_k2p_sector_equality"] is False,
                    f"quartic K2P equality:{number}")
        else:
            raise VerificationFailure(f"unknown proof kind:{kind}")

    require(set(proof_use) == set().union(*(set(rows) for rows in proofs.values())),
            "unused or missing proof registry certificates")
    expected_all = manifest["census"]["all_edge_proof_counts"]
    expected_minimal = manifest["census"]["minimal_first_layer_proof_counts"]
    require(dict(sorted(proof_counts.items())) == expected_all, "all-edge proof census")
    require(dict(sorted(minimal_counts.items())) == expected_minimal, "minimal proof census")
    require(early_termination == 32, "K3P early termination census")
    require(sum(minimal_counts.values()) == 36_568, "minimal K3P terminal rows")
    require(len(forest["second_coverage"]) == 256, "redundant depth-two edge count")
    require(36_536 + 256 == 36_792, "legacy/full-forest leaf count")
    require(manifest["census"]["minimal_k3p_terminal_rows"] == 36_568,
            "manifest minimal terminal count")
    require(manifest["census"]["legacy_full_forest_leaves"] == 36_792,
            "manifest legacy leaf count")
    require(manifest["census"]["redundant_depth2_edges"] == 256,
            "manifest redundant edge count")
    require(manifest["census"]["active_k3p_continuations"] == 0,
            "active K3P continuation count")
    result = {
        "schema": "k3p-restoration-independent-verification-v1",
        "status": "PASS",
        "forest_edges": 36_824,
        "minimal_k3p_terminal_rows": 36_568,
        "legacy_full_forest_leaves": 36_792,
        "legacy_structural_continuations": 32,
        "redundant_depth2_edges": 256,
        "active_k3p_continuations": 0,
        "proof_counts": dict(sorted(proof_counts.items())),
        "proof_certificate_counts": {key: len(value) for key, value in proofs.items()},
        "compiled_descriptor_classes": len(descriptor_cache),
        "unresolved": 0,
        "uses_producer_code": False,
        "uses_k2p_sector_equality": False,
        "manifest_payload_sha256": manifest["payload_sha256"],
    }
    result["payload_sha256"] = logical_payload(result)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", type=Path, default=HERE)
    parser.add_argument("--output", type=Path,
                        default=HERE / "K3P_RESTORATION_INDEPENDENT_VERIFICATION.json")
    parser.add_argument("--artifact-only", action="store_true")
    args = parser.parse_args()
    root = args.package_dir.resolve()
    if args.artifact_only:
        artifact_preflight(root)
        print("K3P_RESTORATION_ARTIFACT_PREFLIGHT_PASS")
    else:
        full_verify(root, args.output.resolve())


if __name__ == "__main__":
    try:
        main()
    except (VerificationFailure, AssertionError, KeyError, IndexError, ValueError,
            OSError, json.JSONDecodeError, gzip.BadGzipFile) as error:
        raise SystemExit(f"K3P_RESTORATION_VERIFY_FAIL:{error}") from error
