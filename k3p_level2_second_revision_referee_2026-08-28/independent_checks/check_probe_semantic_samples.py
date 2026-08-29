#!/usr/bin/env python3
"""Fresh semantic reconstruction of representative K3P probe rows.

The script reconstructs two equality rows (isomorphic and ordinary-triangle),
a displayed-quartet separator, a literal six-circuit tree/sunlet separator,
and a two-port equality/restriction row from public candidate profiles.  It
imports no producer, verifier, or atlas module.  This is a deterministic sample
and is not a substitute for the package's claimed all-row semantic replay.
"""

from __future__ import annotations

import argparse
import ast
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path

import networkx as nx


if not __debug__:
    raise RuntimeError("run without -O so fail-closed assertions remain active")


BASE_SOURCE_LABELS = {
    ("leaf", "INCOMING"): 0,
    ("leaf", "seg", 2, 0): 1,
    ("leaf", "seg", 3, 0): 2,
    ("leaf", "sink", 0): 3,
}
CIRCUITS = (
    (("000", "CGT", "GTC"), ("0TT", "C0C", "GG0")),
    (("000", "CTG", "TGC"), ("0GG", "C0C", "TT0")),
    (("000", "GCT", "TGC"), ("0CC", "GG0", "T0T")),
    (("000", "GTC", "TCG"), ("0CC", "G0G", "TT0")),
    (("000", "CTG", "GCT"), ("0TT", "CC0", "G0G")),
    (("000", "CGT", "TCG"), ("0GG", "CC0", "T0T")),
)


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def locate_proof_root(package_root):
    for candidate in (package_root / "proof_package", package_root):
        if (candidate / "probes/one_port_ledger.jsonl.gz").is_file():
            return candidate
    raise FileNotFoundError("could not locate proof_package beneath --package-root")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def read_rows(path, indices):
    wanted = set(indices)
    rows = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for number, line in enumerate(handle):
            if number in wanted:
                rows[number] = json.loads(line)
            if len(rows) == len(wanted):
                break
    assert set(rows) == wanted
    return rows


def load_records(path, record_ids):
    wanted = set(record_ids)
    records = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if row["record_id"] in wanted:
                records[row["record_id"]] = row["record"]
            if len(records) == len(wanted):
                break
    assert set(records) == wanted
    return records


@dataclass
class Rooted:
    attributes: dict
    arcs: dict

    def copy(self):
        return Rooted(
            {node: dict(data) for node, data in self.attributes.items()},
            {edge: dict(data) for edge, data in self.arcs.items()},
        )


@dataclass
class Mixed:
    attributes: dict
    edges: dict


def parsed_vertex_map(record):
    return {
        ast.literal_eval(source): ast.literal_eval(target)
        for source, target in record["vertex_map"]
    }


def anchor_label_maps(anchor):
    source = dict(BASE_SOURCE_LABELS)
    parent_map = {
        ast.literal_eval(left): ast.literal_eval(right)
        for left, right in anchor["parent_transport"]["vertex_map"]
    }
    target = {parent_map[node]: label for node, label in source.items()}
    assert set(source.values()) == set(target.values()) == set(anchor["labels"])
    return source, target


def degree_maps(graph):
    incoming = {node: [] for node in graph.attributes}
    outgoing = {node: [] for node in graph.attributes}
    for tail, head in graph.arcs:
        outgoing[tail].append(head)
        incoming[head].append(tail)
    return incoming, outgoing


def inferred_label(node, base_labels):
    if node in base_labels:
        return base_labels[node]
    if isinstance(node, tuple) and len(node) >= 3 and node[1] == "leaf" and isinstance(node[2], int):
        return node[2]
    return None


def build_from_profile(profile, base_labels):
    arcs = {}
    for site in profile["sites"]:
        assert site["site_id"] == "E:" + sha(site["mixed_endpoints"])
        for tail, head, role in site["rooted_representatives"]:
            edge = (ast.literal_eval(tail), ast.literal_eval(head))
            previous = arcs.setdefault(edge, {"edge_role": role})
            assert previous == {"edge_role": role}
    nodes = {node for edge in arcs for node in edge}
    shell = Rooted({node: {} for node in nodes}, arcs)
    incoming, outgoing = degree_maps(shell)
    attributes = {}
    for node in nodes:
        label = inferred_label(node, base_labels)
        if label is not None:
            data = {"role": "leaf", "label": label, "dummy": False, "dummy_name": None}
        else:
            role = "root" if not incoming[node] else "retic" if len(incoming[node]) == 2 else "tree"
            data = {"role": role, "label": None, "dummy": False}
            if isinstance(node, tuple) and len(node) >= 2 and node[1] == "subdivision":
                data["dummy_name"] = None
        attributes[node] = data
    graph = Rooted(attributes, arcs)
    for node, data in attributes.items():
        expected = {"root": (0, 2), "tree": (1, 2), "retic": (2, 1), "leaf": (1, 0)}[data["role"]]
        assert (len(incoming[node]), len(outgoing[node])) == expected
    return graph


def graph_payload(graph):
    return {
        "nodes": [
            [repr(node), {key: repr(value) for key, value in sorted(data.items())}]
            for node, data in sorted(graph.attributes.items(), key=lambda row: repr(row[0]))
        ],
        "edges": [
            [
                repr(tail),
                repr(head),
                {key: repr(value) for key, value in sorted(data.items())},
            ]
            for (tail, head), data in sorted(
                graph.arcs.items(), key=lambda row: (repr(row[0][0]), repr(row[0][1]))
            )
        ],
    }


def insert_at_site(graph, site, label, namespace, side, site_index):
    result = graph.copy()
    tail_text, head_text, _ = site["rooted_representatives"][0]
    tail, head = ast.literal_eval(tail_text), ast.literal_eval(head_text)
    assert (tail, head) in result.arcs
    edge_data = result.arcs.pop((tail, head))
    stem = (namespace, side, site_index)
    subdivision = (stem, "subdivision", label, repr(tail), repr(head))
    leaf = (stem, "leaf", label, repr(tail), repr(head))
    assert subdivision not in result.attributes and leaf not in result.attributes
    result.attributes[subdivision] = {
        "role": "tree", "label": None, "dummy": False, "dummy_name": None,
    }
    result.attributes[leaf] = {
        "role": "leaf", "label": label, "dummy": False, "dummy_name": None,
    }
    result.arcs[(tail, subdivision)] = dict(edge_data)
    result.arcs[(subdivision, head)] = dict(edge_data)
    result.arcs[(subdivision, leaf)] = {"edge_role": "arm"}
    return result, subdivision, leaf


def to_mixed(graph):
    incoming, outgoing = degree_maps(graph)
    roots = [
        node for node, data in graph.attributes.items()
        if data["role"] == "root" or not incoming[node]
    ]
    assert len(roots) == 1
    root = roots[0]
    children = list(outgoing[root])
    assert len(children) == 2
    attributes = {
        node: {"role": data["role"], "label": data["label"]}
        for node, data in graph.attributes.items()
        if node != root
    }
    edges = {}
    for tail, head in graph.arcs:
        if tail == root:
            continue
        edge = frozenset((tail, head))
        assert len(edge) == 2 and edge not in edges
        edges[edge] = frozenset((head,)) if graph.attributes[head]["role"] == "retic" else frozenset()
    root_edge = frozenset(children)
    assert len(root_edge) == 2 and root_edge not in edges
    edges[root_edge] = frozenset(
        child for child in children if graph.attributes[child]["role"] == "retic"
    )
    return Mixed(attributes, edges)


def mixed_payload(mixed):
    return {
        "nodes": [
            [repr(node), {key: repr(value) for key, value in sorted(data.items())}]
            for node, data in sorted(mixed.attributes.items(), key=lambda row: repr(row[0]))
        ],
        "edges": [
            [sorted(map(repr, edge)), sorted(map(repr, heads))]
            for edge, heads in sorted(
                mixed.edges.items(), key=lambda row: tuple(sorted(map(repr, row[0])))
            )
        ],
    }


def remove_node(graph, node):
    graph.attributes.pop(node)
    graph.arcs = {edge: data for edge, data in graph.arcs.items() if node not in edge}


def restrict_rooted(graph, keep_labels):
    result = graph.copy()
    for node, data in list(result.attributes.items()):
        if data["role"] == "leaf" and data["label"] not in keep_labels:
            remove_node(result, node)
    while True:
        incoming, outgoing = degree_maps(result)
        dead = next((
            node for node, data in result.attributes.items()
            if not outgoing[node]
            and not (data["role"] == "leaf" and data["label"] in keep_labels)
        ), None)
        if dead is not None:
            remove_node(result, dead)
            continue
        incoming, outgoing = degree_maps(result)
        suppress = next((
            node for node, data in result.attributes.items()
            if data["role"] != "leaf"
            and len(incoming[node]) == len(outgoing[node]) == 1
        ), None)
        if suppress is not None:
            parent, child = incoming[suppress][0], outgoing[suppress][0]
            remove_node(result, suppress)
            result.arcs.setdefault((parent, child), {"edge_role": "suppressed"})
            continue
        incoming, outgoing = degree_maps(result)
        roots = [node for node in result.attributes if not incoming[node]]
        if len(roots) == 1 and result.attributes[roots[0]]["role"] != "leaf" and len(outgoing[roots[0]]) == 1:
            remove_node(result, roots[0])
            continue
        break
    incoming, outgoing = degree_maps(result)
    for node, data in result.attributes.items():
        data["role"] = (
            "leaf" if data["label"] in keep_labels
            else "root" if not incoming[node]
            else "retic" if len(incoming[node]) == 2
            else "tree"
        )
    return result


def actual_triangle(mixed):
    nodes = sorted(mixed.attributes, key=repr)
    found = []
    for left_index, left in enumerate(nodes):
        for middle_index, middle in enumerate(nodes[left_index+1:], left_index+1):
            for right in nodes[middle_index+1:]:
                deck = {
                    frozenset((left, middle)),
                    frozenset((left, right)),
                    frozenset((middle, right)),
                }
                if not deck.issubset(mixed.edges):
                    continue
                heads = [next(iter(mixed.edges[edge])) for edge in deck if mixed.edges[edge]]
                if len(heads) == 2 and heads[0] == heads[1]:
                    found.append((deck, heads[0]))
    assert len(found) <= 1
    return found[0] if found else None


def semantic_transport(source, target, record):
    source_mixed, target_mixed = to_mixed(source), to_mixed(target)
    mapping = parsed_vertex_map(record)
    assert set(mapping) == set(source_mixed.attributes)
    assert set(mapping.values()) == set(target_mixed.attributes)
    assert len(mapping) == len(set(mapping.values()))
    for source_node, target_node in mapping.items():
        assert source_mixed.attributes[source_node]["label"] == target_mixed.attributes[target_node]["label"]
    induced = {edge: frozenset(mapping[node] for node in edge) for edge in source_mixed.edges}
    assert set(induced.values()) == set(target_mixed.edges)
    stored_edges = {
        frozenset(ast.literal_eval(node) for node in source_edge):
        frozenset(ast.literal_eval(node) for node in target_edge)
        for source_edge, target_edge in record["mixed_edge_map"]
    }
    assert stored_edges == induced
    relation = record["relation"]
    source_triangle, target_triangle = actual_triangle(source_mixed), actual_triangle(target_mixed)
    if relation == "isomorphic":
        assert (source_triangle is None) == (target_triangle is None)
        for edge, target_edge in induced.items():
            expected_heads = frozenset(mapping[node] for node in source_mixed.edges[edge])
            assert expected_heads == target_mixed.edges[target_edge]
        assert record["source_triangle_edges"] is None
        assert record["target_triangle_edges"] is None
        assert record["ordinary_triangle_arrowhead_witness"] is None
    else:
        assert relation == "triangle" and source_triangle and target_triangle
        source_deck, source_reticulation = source_triangle
        target_deck, target_reticulation = target_triangle
        stored_source = {
            frozenset(ast.literal_eval(node) for node in edge)
            for edge in record["source_triangle_edges"]
        }
        stored_target = {
            frozenset(ast.literal_eval(node) for node in edge)
            for edge in record["target_triangle_edges"]
        }
        assert stored_source == source_deck and stored_target == target_deck
        assert {induced[edge] for edge in source_deck} == target_deck
        for edge, target_edge in induced.items():
            if edge not in source_deck:
                expected_heads = frozenset(mapping[node] for node in source_mixed.edges[edge])
                assert expected_heads == target_mixed.edges[target_edge]
        ordinary = record["ordinary_triangle_arrowhead_witness"]
        assert ast.literal_eval(ordinary["source_common_reticulation"]) == source_reticulation
        assert ast.literal_eval(ordinary["target_common_reticulation"]) == target_reticulation
        for side, deck, reticulation, mixed in (
            ("source", source_deck, source_reticulation, source_mixed),
            ("target", target_deck, target_reticulation, target_mixed),
        ):
            actual_headed = {edge for edge in deck if mixed.edges[edge] == frozenset((reticulation,))}
            stored_headed = {
                frozenset(ast.literal_eval(node) for node in edge)
                for edge in ordinary[f"{side}_headed_edges"]
            }
            assert len(actual_headed) == 2 and stored_headed == actual_headed
    return {
        "relation": relation,
        "vertices": len(mapping),
        "mixed_edges": len(induced),
        "labels_incidence_and_arrowheads_verified": True,
    }


def identity_transport_public(source_mixed, target_mixed):
    assert set(source_mixed.attributes) == set(target_mixed.attributes)
    assert set(source_mixed.edges) == set(target_mixed.edges)
    assert source_mixed.attributes == target_mixed.attributes
    assert source_mixed.edges == target_mixed.edges
    return {
        "relation": "isomorphic",
        "vertex_map": [[repr(node), repr(node)] for node in sorted(source_mixed.attributes, key=repr)],
        "mixed_edge_map": [
            [sorted(map(repr, edge)), sorted(map(repr, edge))]
            for edge in sorted(source_mixed.edges, key=lambda item: tuple(sorted(map(repr, item))))
        ],
        "source_triangle_edges": None,
        "target_triangle_edges": None,
    }


def validate_restriction(child, parent, removed_label, record):
    keep = {
        data["label"] for data in parent.attributes.values()
        if isinstance(data["label"], int)
    }
    restricted = restrict_rooted(child, keep)
    restricted_mixed, parent_mixed = to_mixed(restricted), to_mixed(parent)
    restricted_hash = sha(mixed_payload(restricted_mixed))
    parent_hash = sha(mixed_payload(parent_mixed))
    assert record["removed_label"] == removed_label
    assert record["restricted_mixed_graph_sha256"] == restricted_hash
    assert record["parent_mixed_graph_sha256"] == parent_hash
    assert record["exact_labelled_relation"] == "isomorphic"
    identity = identity_transport_public(restricted_mixed, parent_mixed)
    assert sha(identity) == record["restriction_transport_sha256"]
    return {
        "removed_label": removed_label,
        "restricted_mixed_graph_sha256": restricted_hash,
        "parent_mixed_graph_sha256": parent_hash,
        "identity_transport_reconstructed": True,
    }


def displayed_splits(graph, quartet):
    quartet = set(quartet)
    incoming, _ = degree_maps(graph)
    reticulations = sorted((
        node for node, data in graph.attributes.items()
        if data["role"] == "retic" and len(incoming[node]) == 2
    ), key=repr)
    choices = [tuple((parent, reticulation) for parent in incoming[reticulation]) for reticulation in reticulations]
    splits = set()
    for kept_incoming in product(*choices):
        keep = set(kept_incoming)
        switched = [
            edge for edge in graph.arcs
            if edge[1] not in reticulations or edge in keep
        ]
        undirected = nx.Graph()
        undirected.add_nodes_from(graph.attributes)
        undirected.add_edges_from(switched)
        while True:
            changed = False
            for node in list(undirected):
                label = graph.attributes[node]["label"]
                if label not in quartet and undirected.degree(node) <= 1:
                    undirected.remove_node(node)
                    changed = True
                    break
                if label not in quartet and undirected.degree(node) == 2:
                    left, right = list(undirected.neighbors(node))
                    undirected.remove_node(node)
                    if left != right:
                        undirected.add_edge(left, right)
                    changed = True
                    break
            if not changed:
                break
        split = None
        for left, right in list(undirected.edges()):
            undirected.remove_edge(left, right)
            components = list(nx.connected_components(undirected))
            undirected.add_edge(left, right)
            if len(components) != 2:
                continue
            labels = [
                tuple(sorted(
                    graph.attributes[node]["label"]
                    for node in component
                    if graph.attributes[node]["label"] in quartet
                ))
                for component in components
            ]
            if sorted(map(len, labels)) == [2, 2]:
                split = tuple(sorted(labels))
                break
        splits.add(split if split is not None else ("star",))
    return tuple(sorted(splits, key=repr))


def sparse_add(target, exponent, coefficient):
    target[exponent] += coefficient
    if not target[exponent]:
        del target[exponent]


def polynomial_multiply(left, right):
    result = defaultdict(Q)
    for left_exp, left_coefficient in left.items():
        for right_exp, right_coefficient in right.items():
            sparse_add(
                result,
                tuple(a+b for a, b in zip(left_exp, right_exp)),
                left_coefficient*right_coefficient,
            )
    return dict(result)


def inheritance_expansion(bits):
    result = {0: Q(1)}
    for index, selected_second in enumerate(bits):
        nxt = defaultdict(Q)
        for mask, coefficient in result.items():
            if selected_second:
                nxt[mask | (1 << index)] += coefficient
            else:
                nxt[mask] += coefficient
                nxt[mask | (1 << index)] -= coefficient
        result = {mask: coefficient for mask, coefficient in nxt.items() if coefficient}
    return result


def compile_three_leaf(graph, ordered_labels):
    label_position = {label: index for index, label in enumerate(ordered_labels)}
    assert len(label_position) == 3
    edges = sorted(graph.arcs, key=lambda edge: (repr(edge[0]), repr(edge[1])))
    incoming, _ = degree_maps(graph)
    reticulations = sorted((
        node for node, data in graph.attributes.items() if data["role"] == "retic"
    ), key=repr)
    parent_orders = [tuple(sorted(incoming[node], key=repr)) for node in reticulations]
    width = 3*len(edges) + len(reticulations)
    outputs = {}
    assignments = [prefix + (prefix[0] ^ prefix[1],) for prefix in product(range(4), repeat=2)]
    for word in assignments:
        polynomial = defaultdict(Q)
        for bits in product((0, 1), repeat=len(reticulations)):
            removed = set()
            for index, reticulation in enumerate(reticulations):
                keep_parent = parent_orders[index][bits[index]]
                removed.update(
                    (parent, reticulation)
                    for parent in parent_orders[index]
                    if parent != keep_parent
                )
            kept = tuple(edge for edge in edges if edge not in removed)
            children = defaultdict(list)
            for tail, head in kept:
                children[tail].append(head)
            memo = {}

            def descendant_mask(node):
                if node in memo:
                    return memo[node]
                label = graph.attributes[node]["label"]
                mask = 1 << label_position[label] if label in label_position else 0
                for child in children[node]:
                    mask |= descendant_mask(child)
                memo[node] = mask
                return mask

            for node in graph.attributes:
                descendant_mask(node)
            base = [0] * width
            for edge_index, edge in enumerate(edges):
                if edge not in kept:
                    continue
                mask = memo[edge[1]]
                sector = 0
                for leaf_index in range(3):
                    if (mask >> leaf_index) & 1:
                        sector ^= word[leaf_index]
                if sector:
                    base[3*edge_index+sector-1] += 1
            for inheritance_mask, coefficient in inheritance_expansion(bits).items():
                exponent = base.copy()
                for index in range(len(reticulations)):
                    if (inheritance_mask >> index) & 1:
                        exponent[3*len(edges)+index] += 1
                sparse_add(polynomial, tuple(exponent), coefficient)
        outputs[word] = dict(polynomial)
    return outputs, width, len(edges), len(reticulations)


def circuit_deck(outputs, width):
    code = {letter: index for index, letter in enumerate("0CGT")}

    def coordinate(text):
        return outputs[tuple(code[letter] for letter in text)]

    deck = []
    for left, right in CIRCUITS:
        left_polynomial = {(0,) * width: Q(1)}
        right_polynomial = {(0,) * width: Q(1)}
        for text in left:
            left_polynomial = polynomial_multiply(left_polynomial, coordinate(text))
        for text in right:
            right_polynomial = polynomial_multiply(right_polynomial, coordinate(text))
        difference = defaultdict(Q, left_polynomial)
        for exponent, coefficient in right_polynomial.items():
            sparse_add(difference, exponent, -coefficient)
        deck.append(dict(difference))
    return deck


def evaluate(polynomial, point):
    total = Q(0)
    for exponent, coefficient in polynomial.items():
        term = coefficient
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        total += term
    return total


def sample_children(anchor, row):
    source_labels, target_labels = anchor_label_maps(anchor)
    children, inserted = {}, {}
    for side, labels in (("source", source_labels), ("target", target_labels)):
        profile = anchor[f"{side}_candidate_profile"]
        parent = build_from_profile(profile, labels)
        assert sha(graph_payload(parent)) == anchor[f"{side}_graph_sha256"]
        index = row[f"{side}_site_index"]
        assert profile["sites"][index]["site_id"] == row[f"{side}_site_id"]
        child, subdivision, leaf = insert_at_site(
            parent,
            profile["sites"][index],
            row["inserted_label"],
            "P1:" + row["parent_anchor_id"],
            side,
            index,
        )
        assert sha(graph_payload(child)) == row[f"{side}_child_graph_sha256"]
        children[side] = (parent, child)
        inserted[side] = (subdivision, leaf)
    return children, inserted


def main():
    args = arguments()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    proof_root = locate_proof_root(args.package_root)
    probes = proof_root / "probes"
    contract_path = proof_root / "input_frozen/model_independent_topology_package/anchor_inputs/probe_input_contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    anchors = {row["anchor_id"]: row for row in contract["anchors"]}
    one = read_rows(probes / "one_port_ledger.jsonl.gz", {0, 1, 122, 145})
    parent_inventory = read_rows(probes / "two_port_parent_inventory.jsonl.gz", {0})[0]
    two_row = read_rows(probes / "two_port_ledger.jsonl.gz", {0})[0]
    assert [one[index]["status"] for index in (0, 1, 122, 145)] == [
        "isomorphic", "displayed_quartet_mismatch", "k3p_tree_sunlet_sos", "triangle",
    ]
    assert two_row["status"] == "isomorphic"

    all_rows = list(one.values()) + [two_row]
    restriction_ids = {
        row[f"{side}_parent_restriction_id"]
        for row in all_rows
        for side in ("source", "target")
    }
    restrictions = load_records(probes / "parent_restriction_ledger.jsonl.gz", restriction_ids)
    transport_ids = {
        row["transport_id"] for row in (one[0], one[145], two_row)
    } | {
        row["parent_transport_id"] for row in (one[0], one[145], two_row)
    }
    transports = load_records(probes / "exact_transport_ledger.jsonl.gz", transport_ids)

    equality_results = []
    cached_children = {}
    for row_number in (0, 145):
        row = one[row_number]
        anchor = anchors[row["parent_anchor_id"]]
        children, inserted = sample_children(anchor, row)
        cached_children[row_number] = (children, inserted)
        semantic = semantic_transport(
            children["source"][1], children["target"][1], transports[row["transport_id"]]
        )
        parent_map = {
            ast.literal_eval(left): ast.literal_eval(right)
            for left, right in anchor["parent_transport"]["vertex_map"]
        }
        expected_map = dict(parent_map)
        expected_map[inserted["source"][0]] = inserted["target"][0]
        expected_map[inserted["source"][1]] = inserted["target"][1]
        assert parsed_vertex_map(transports[row["transport_id"]]) == expected_map
        restriction_checks = {}
        for side in ("source", "target"):
            record_id = row[f"{side}_parent_restriction_id"]
            restriction_checks[side] = validate_restriction(
                children[side][1], children[side][0], row["inserted_label"], restrictions[record_id]
            )
        equality_results.append({
            "ledger_index_zero_based": row_number,
            "claimed_and_reconstructed_relation": row["status"],
            "anchor_id": row["parent_anchor_id"],
            "transport_id": row["transport_id"],
            "source_child_graph_sha256": sha(graph_payload(children["source"][1])),
            "target_child_graph_sha256": sha(graph_payload(children["target"][1])),
            "semantic_transport": semantic,
            "parent_map_plus_inserted_stem_and_leaf": True,
            "restrictions": restriction_checks,
        })

    quartet_row = one[1]
    quartet_children, _ = sample_children(anchors[quartet_row["parent_anchor_id"]], quartet_row)
    quartet = (0, 1, 2, 4)
    source_splits = displayed_splits(quartet_children["source"][1], quartet)
    target_splits = displayed_splits(quartet_children["target"][1], quartet)
    assert source_splits != target_splits
    with gzip.open(probes / "separation_proof_registry.json.gz", "rt", encoding="utf-8") as handle:
        proof_registry = json.load(handle)
    quartet_proof = proof_registry["separation_proof_registry"][quartet_row["proof_id"]]
    source_payload = [[list(left), list(right)] for left, right in source_splits]
    target_payload = [[list(left), list(right)] for left, right in target_splits]
    assert quartet_proof["quartet"] == list(quartet)
    assert quartet_proof["source_displayed_splits"] == source_payload
    assert quartet_proof["target_displayed_splits"] == target_payload
    quartet_result = {
        "ledger_index_zero_based": 1,
        "proof_id": quartet_row["proof_id"],
        "quartet": list(quartet),
        "source_displayed_splits": source_payload,
        "target_displayed_splits": target_payload,
        "semantic_mismatch_reconstructed": True,
    }

    sunlet_row = one[122]
    sunlet_children, _ = sample_children(anchors[sunlet_row["parent_anchor_id"]], sunlet_row)
    triple = (0, 1, 4)
    source_restricted = restrict_rooted(sunlet_children["source"][1], set(triple))
    target_restricted = restrict_rooted(sunlet_children["target"][1], set(triple))
    source_mixed, target_mixed = to_mixed(source_restricted), to_mixed(target_restricted)
    source_triangle, target_triangle = actual_triangle(source_mixed), actual_triangle(target_mixed)
    source_tree = source_triangle is None and not any(
        data["role"] == "retic" for data in source_restricted.attributes.values()
    )
    target_degrees = sorted(sum(node in edge for edge in target_mixed.edges) for node in target_mixed.attributes)
    target_sunlet = (
        target_triangle is not None
        and len(target_mixed.attributes) == len(target_mixed.edges) == 6
        and target_degrees == [1, 1, 1, 3, 3, 3]
    )
    assert source_tree and target_sunlet
    source_outputs, source_width, source_edges, source_reticulations = compile_three_leaf(source_restricted, triple)
    target_outputs, target_width, target_edges, target_reticulations = compile_three_leaf(target_restricted, triple)
    source_circuits = circuit_deck(source_outputs, source_width)
    target_circuits = circuit_deck(target_outputs, target_width)
    assert not any(source_circuits) and all(target_circuits)
    target_point = [Q(1, 2)] * (3*target_edges) + [Q(1, 3)] * target_reticulations
    target_values = [evaluate(polynomial, target_point) for polynomial in target_circuits]
    target_sum_squares = sum(value*value for value in target_values)
    assert target_sum_squares > 0
    sunlet_proof = proof_registry["k3p_tree_sunlet_registry"]["certificates"][sunlet_row["proof_id"]]
    assert sunlet_proof["triple"] == list(triple)
    assert sunlet_proof["tree_on"] == "source" and sunlet_proof["sunlet_on"] == "target"
    assert sunlet_proof["sunlet_nonzero_circuit_count"] == 6
    sunlet_result = {
        "ledger_index_zero_based": 122,
        "proof_id": sunlet_row["proof_id"],
        "triple": list(triple),
        "source_type": "tree",
        "target_type": "ordinary_sunlet",
        "target_degree_sequence": target_degrees,
        "source_nonzero_circuit_count": sum(bool(polynomial) for polynomial in source_circuits),
        "target_nonzero_circuit_count": sum(bool(polynomial) for polynomial in target_circuits),
        "fresh_isotropic_ct_values": [str(value) for value in target_values],
        "fresh_isotropic_ct_sum_of_squares": str(target_sum_squares),
        "source_edge_reticulation_counts": [source_edges, source_reticulations],
        "target_edge_reticulation_counts": [target_edges, target_reticulations],
    }

    base_anchor = anchors[parent_inventory["base_anchor_id"]]
    assert parent_inventory["one_port_parent_id"] == two_row["one_port_parent_id"]
    assert parent_inventory["base_anchor_id"] == two_row["base_anchor_id"]
    first_children = cached_children[0][0]
    two_parents = {}
    source_labels, target_labels = anchor_label_maps(base_anchor)
    for side, labels in (("source", source_labels), ("target", target_labels)):
        parent = build_from_profile(parent_inventory[f"{side}_candidate_profile"], labels)
        assert sha(graph_payload(parent)) == parent_inventory[f"{side}_graph_sha256"]
        assert graph_payload(parent) == graph_payload(first_children[side][1])
        two_parents[side] = parent
    two_children, two_inserted = {}, {}
    for side in ("source", "target"):
        profile = parent_inventory[f"{side}_candidate_profile"]
        index = two_row[f"second_{side}_site_index"]
        assert profile["sites"][index]["site_id"] == two_row[f"second_{side}_site_id"]
        child, subdivision, leaf = insert_at_site(
            two_parents[side],
            profile["sites"][index],
            two_row["second_label"],
            "P2:" + two_row["one_port_parent_id"],
            side,
            index,
        )
        assert sha(graph_payload(child)) == two_row[f"{side}_child_graph_sha256"]
        two_children[side] = child
        two_inserted[side] = (subdivision, leaf)
    two_semantic = semantic_transport(
        two_children["source"], two_children["target"], transports[two_row["transport_id"]]
    )
    two_restrictions = {}
    for side in ("source", "target"):
        record_id = two_row[f"{side}_parent_restriction_id"]
        two_restrictions[side] = validate_restriction(
            two_children[side], two_parents[side], two_row["second_label"], restrictions[record_id]
        )
    child_map = parsed_vertex_map(transports[two_row["transport_id"]])
    restricted_map = {
        source: target for source, target in child_map.items()
        if source not in set(two_inserted["source"])
        and target not in set(two_inserted["target"])
    }
    assert restricted_map == parsed_vertex_map(transports[two_row["parent_transport_id"]])
    raw_pairs = (
        parent_inventory["source_candidate_profile"]["site_count"]
        * parent_inventory["target_candidate_profile"]["site_count"]
    )
    assert raw_pairs == parent_inventory["raw_second_probe_pairs"] == 169
    two_result = {
        "parent_inventory_index_zero_based": 0,
        "two_port_ledger_index_zero_based": 0,
        "one_port_parent_id": two_row["one_port_parent_id"],
        "raw_second_probe_pairs": raw_pairs,
        "semantic_transport": two_semantic,
        "remove_second_label_recovers_one_port_parent": True,
        "child_transport_restricts_to_parent_transport": True,
        "restrictions": two_restrictions,
    }

    result = {
        "scope": {
            "semantic_rows_checked": 5,
            "one_port_rows_total": 29964,
            "two_port_rows_total": 544571,
            "all_probe_rows_total": 574535,
            "completeness_claim": False,
        },
        "one_port_equality_samples": equality_results,
        "one_port_quartet_sample": quartet_result,
        "one_port_tree_sunlet_sample": sunlet_result,
        "two_port_equality_restriction_sample": two_result,
        "independence_boundary": (
            "Five rows are semantically rebuilt from public literal profiles without package code. "
            "The sample exercises all four one-port statuses plus a two-port equality/restriction, "
            "but does not independently establish all-row semantic completeness."
        ),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (args.output_dir / "probe_semantic_samples.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
