#!/usr/bin/env python3
"""Primary-side reconstruction and exact K3P algebra helpers.

The release producer imports this module.  The independent verifier does not:
it reconstructs the graph universe and Fourier maps through a separate code
path.
"""
from __future__ import annotations

import ast
import collections
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ATLAS_PATH = PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py"
FOREST_PATH = (
    PROJECT
    / "input_frozen/model_independent_topology_package/anchor_inputs/corrected_restoration_forest.json"
)
POLYNOMIAL_PATHS = (
    PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_h14_marginal_orbit_certificates.json",
    PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_remaining_quartic_separators.json",
    PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_prelock_source5_quartic.json",
)


def load_atlas():
    spec = importlib.util.spec_from_file_location("restoration_discovery_k3p_atlas", ATLAS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {ATLAS_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def exact_labelled_mixed_payload(atlas, graph):
    mixed = atlas.sd0_mixed(graph)
    nodes = [
        [repr(node), data.get("label"), data.get("role")]
        for node, data in sorted(mixed.nodes(data=True), key=lambda row: repr(row[0]))
    ]
    edges = []
    for left, right, data in mixed.edges(data=True):
        if repr(right) < repr(left):
            left, right = right, left
        edges.append(
            [
                repr(left),
                repr(right),
                sorted(repr(node) for node in data.get("heads", frozenset())),
            ]
        )
    edges.sort()
    return {"nodes": nodes, "edges": edges}


def source_insertion_candidates(graph):
    rows = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        if graph.nodes[head].get("role") == "leaf":
            continue
        if graph.nodes[tail].get("role") == "root":
            continue
        rows.append(
            {"tail": repr(tail), "head": repr(head), "edge_role": data.get("edge_role")}
        )
    return rows


def insert_source_leaf(atlas, graph, candidate, label):
    result = graph.copy()
    tail = ast.literal_eval(candidate["tail"])
    head = ast.literal_eval(candidate["head"])
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = ("restoration_subdivision", label, repr(tail), repr(head))
    leaf = ("leaf", "restoration", label)
    result.add_node(subdivision, role="tree", label=None, dummy=False)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    atlas.validate_graph(result)
    return result


def parse_root_id(root_id):
    fields = root_id.split(":")
    return (
        int(fields[0][1:]),
        int(fields[1][1:]),
        int(fields[2][1:]),
        tuple(map(int, fields[3][1:])),
    )


def promoted_target(atlas, targets, target_index, permutation, roles):
    result = atlas.relabel_record(targets[target_index], permutation).graph.copy()
    for role, label in roles:
        nodes = [n for n, data in result.nodes(data=True) if data.get("dummy_name") == role]
        assert len(nodes) == 1, (target_index, permutation, role, nodes)
        data = result.nodes[nodes[0]]
        data["label"] = label
        data["dummy"] = False
        data["dummy_name"] = None
    selected = atlas.restrict_rooted(result, set(range(4 + len(roles))))
    return result, selected


def labels_of(graph):
    return tuple(
        sorted(
            data["label"]
            for _, data in graph.nodes(data=True)
            if isinstance(data.get("label"), int)
        )
    )


def ordinary_triangles(atlas, graph):
    try:
        mixed = atlas.sd0_mixed(graph)
    except (ValueError, KeyError):
        return []
    undirected = atlas.nx.Graph()
    undirected.add_nodes_from(mixed.nodes())
    undirected.add_edges_from(mixed.edges())
    rows = []
    for triangle in itertools.combinations(undirected.nodes(), 3):
        edges = [frozenset(pair) for pair in itertools.combinations(triangle, 2)]
        if not all(undirected.has_edge(*tuple(edge)) for edge in edges):
            continue
        headed = []
        valid = True
        for edge in edges:
            heads = mixed.edges[tuple(edge)].get("heads", frozenset())
            if len(heads) > 1 or any(head not in edge for head in heads):
                valid = False
                break
            if heads:
                headed.append(next(iter(heads)))
        if valid and len(headed) == 2 and headed[0] == headed[1]:
            rows.append((triangle, tuple(edges), headed[0]))
    return rows


def is_exact_ordinary_sunlet(atlas, graph):
    try:
        mixed = atlas.sd0_mixed(graph)
    except (ValueError, KeyError):
        return False
    triangles = ordinary_triangles(atlas, graph)
    labels = [data.get("label") for _, data in mixed.nodes(data=True)]
    degree_census = sorted(dict(mixed.degree()).values())
    return (
        len(triangles) == 1
        and len(mixed.nodes()) == 6
        and len(mixed.edges()) == 6
        and len([label for label in labels if isinstance(label, int)]) == 3
        and degree_census == [1, 1, 1, 3, 3, 3]
    )


def normalized_restriction(atlas, graph, triple):
    restricted = atlas.restrict_rooted(graph, set(triple))
    relabel = {old: new for new, old in enumerate(sorted(triple))}
    normalized = restricted.copy()
    for _, data in normalized.nodes(data=True):
        label = data.get("label")
        if label in relabel:
            data["label"] = relabel[label]
    return restricted, normalized


CIRCUITS = (
    (("000", "CGT", "GTC"), ("0TT", "C0C", "GG0")),
    (("000", "CTG", "TGC"), ("0GG", "C0C", "TT0")),
    (("000", "GCT", "TGC"), ("0CC", "GG0", "T0T")),
    (("000", "GTC", "TCG"), ("0CC", "G0G", "TT0")),
    (("000", "CTG", "GCT"), ("0TT", "CC0", "G0G")),
    (("000", "CGT", "TCG"), ("0GG", "CC0", "T0T")),
)


def circuit_pullbacks(atlas, descriptor):
    outputs = atlas.output_sparse_polynomials(descriptor)
    assignments = atlas.k3p_assignments(3)
    index = {assignment: number for number, assignment in enumerate(assignments)}
    code = {"0": 0, "C": 1, "G": 2, "T": 3}

    def coordinate(label):
        return outputs[index[tuple(code[value] for value in label)]]

    rows = []
    for left, right in CIRCUITS:
        rows.append(
            atlas.sparse_lincomb(
                [
                    atlas.sparse_mul_many([coordinate(label) for label in left]),
                    atlas.sparse_mul_many([coordinate(label) for label in right]),
                ],
                [1, -1],
            )
        )
    return rows


def tree_sunlet_certificate(atlas, source, target):
    labels = labels_of(source)
    assert labels == labels_of(target)
    for triple in itertools.combinations(labels, 3):
        source_type = atlas.triple_type(source, triple)
        target_type = atlas.triple_type(target, triple)
        if {source_type, target_type} != {"tree", "sunlet"}:
            continue
        source_restricted, source_normalized = normalized_restriction(atlas, source, triple)
        target_restricted, target_normalized = normalized_restriction(atlas, target, triple)
        source_descriptor = atlas.model_descriptor(source_normalized)
        target_descriptor = atlas.model_descriptor(target_normalized)
        source_circuits = circuit_pullbacks(atlas, source_descriptor)
        target_circuits = circuit_pullbacks(atlas, target_descriptor)
        if source_type == "tree":
            tree_desc, sun_desc = source_descriptor, target_descriptor
            tree_circuits, sun_circuits = source_circuits, target_circuits
            sun_graph = target_normalized
            tree_on, sunlet_on = "source", "target"
        else:
            tree_desc, sun_desc = target_descriptor, source_descriptor
            tree_circuits, sun_circuits = target_circuits, source_circuits
            sun_graph = source_normalized
            tree_on, sunlet_on = "target", "source"
        if tree_desc.retic_count != 0 or sun_desc.retic_count != 1:
            continue
        if not is_exact_ordinary_sunlet(atlas, sun_graph):
            continue
        if any(tree_circuits) or not any(sun_circuits):
            continue
        return {
            "triple": list(triple),
            "tree_on": tree_on,
            "sunlet_on": sunlet_on,
            "tree_zero": [not row for row in tree_circuits],
            "sunlet_nonzero": [bool(row) for row in sun_circuits],
        }
    return None


def polynomial_pullback(atlas, descriptor, terms):
    outputs = atlas.output_sparse_polynomials(descriptor)
    return atlas.sparse_lincomb(
        [
            atlas.sparse_mul_many([outputs[index] for index in term["coordinate_indices"]])
            for term in terms
        ],
        [term["coefficient"] for term in terms],
    )


def transported_terms(atlas, terms, permutation):
    assignments = atlas.k3p_assignments(4)
    index = {assignment: number for number, assignment in enumerate(assignments)}
    mapping = tuple(
        index[tuple(assignment[permutation[position]] for position in range(4))]
        for assignment in assignments
    )
    return [
        {
            "coefficient": term["coefficient"],
            "coordinate_indices": sorted(mapping[value] for value in term["coordinate_indices"]),
        }
        for term in terms
    ]


def load_polynomial_templates():
    rows = []
    for path in POLYNOMIAL_PATHS:
        payload = json.loads(path.read_text())
        for record in payload["records"]:
            if "terms" in record:
                rows.append((path.name, record.get("orbit_id", "prelock"), record["terms"]))
    return rows


def k3p_four_port_polynomial(atlas, source, target):
    source_descriptor = atlas.model_descriptor_fast2(source)
    target_descriptor = atlas.model_descriptor_fast2(target)
    for filename, orbit_id, base_terms in load_polynomial_templates():
        for permutation in itertools.permutations(range(4)):
            terms = transported_terms(atlas, base_terms, permutation)
            if polynomial_pullback(atlas, target_descriptor, terms):
                continue
            source_pullback = polynomial_pullback(atlas, source_descriptor, terms)
            if not source_pullback:
                continue
            return {
                "template_file": filename,
                "template_orbit_id": orbit_id,
                "port_permutation": list(permutation),
                "source_pullback_terms": len(source_pullback),
            }
    return None


def reconstruct_rows():
    atlas = load_atlas()
    forest = json.loads(FOREST_PATH.read_text())
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    first_cache = {}
    target_cache = {}
    first_graphs = {}
    rows = []
    for row in forest["first_coverage"]:
        source_index, _, target_index, permutation = parse_root_id(row["root_id"])
        source_key = (source_index, row["source_insertion_index"])
        if source_key not in first_cache:
            candidates = source_insertion_candidates(sources[source_index].graph)
            first_cache[source_key] = insert_source_leaf(
                atlas,
                sources[source_index].graph,
                candidates[row["source_insertion_index"]],
                4,
            )
        target_key = (target_index, permutation, row["restored_role"])
        if target_key not in target_cache:
            target_cache[target_key] = promoted_target(
                atlas, targets, target_index, permutation, ((row["restored_role"], 4),)
            )
        source_graph = first_cache[source_key]
        target_full, target_selected = target_cache[target_key]
        first_graphs[row["row_sha256"]] = (source_graph, target_full, target_selected)
        rows.append(("first", row, source_graph, target_full, target_selected))
    for row in forest["second_coverage"]:
        first_source, first_target_full, first_target_selected = first_graphs[
            row["parent_first_row_sha256"]
        ]
        candidates = source_insertion_candidates(first_source)
        source_graph = insert_source_leaf(
            atlas,
            first_source,
            candidates[row["second_source_insertion_index"]],
            5,
        )
        target_full = first_target_full.copy()
        role = row["second_restored_role"]
        nodes = [n for n, data in target_full.nodes(data=True) if data.get("dummy_name") == role]
        assert len(nodes) == 1
        data = target_full.nodes[nodes[0]]
        data["label"] = 5
        data["dummy"] = False
        data["dummy_name"] = None
        target_selected = atlas.restrict_rooted(target_full, set(range(6)))
        rows.append(("second", row, source_graph, target_full, target_selected))
    return atlas, forest, rows


def main():
    atlas, forest, rows = reconstruct_rows()
    ti_counts = collections.Counter()
    algebra_pairs = {}
    transport_failures = []
    for layer, row, source, target_full, target_selected in rows:
        if labels_of(source) != labels_of(target_selected):
            raise AssertionError((layer, row["row_sha256"], "labels"))
        if layer == "first":
            sid = row["source_parent_transport_id"]
            tid = row["target_parent_transport_id"]
            s_transport = forest["first_source_transport_certificates"][sid]
            t_transport = forest["first_target_transport_certificates"][tid]
            source_parent = atlas.restrict_rooted(source, set(range(4)))
            target_parent = atlas.restrict_rooted(target_full, set(range(4)))
            if sha(exact_labelled_mixed_payload(atlas, source_parent)) != s_transport["parent_mixed_graph_sha256"]:
                transport_failures.append((row["row_sha256"], "source"))
            if sha(exact_labelled_mixed_payload(atlas, target_parent)) != t_transport["parent_mixed_graph_sha256"]:
                transport_failures.append((row["row_sha256"], "target"))
        if row["proof"] == "full_map_Ti_zero_strict_sign":
            cert = tree_sunlet_certificate(atlas, source, target_selected)
            ti_counts["certified" if cert else "unresolved"] += 1
            if not cert:
                print("UNRESOLVED_TI", layer, row["row_sha256"], row.get("certificate"))
        elif row["proof"] in {
            "exact_multihomogeneous_quadratic",
            "inherited_exact_F_2_112_quartic",
        }:
            source_descriptor = atlas.model_descriptor_fast2(source)
            target_descriptor = atlas.model_descriptor_fast2(target_full)
            key = (source_descriptor, target_descriptor)
            algebra_pairs.setdefault(key, []).append((layer, row))
    print(
        json.dumps(
            {
                "rows": len(rows),
                "transport_failures": transport_failures[:10],
                "transport_failure_count": len(transport_failures),
                "ti_counts": dict(ti_counts),
                "algebra_rows": sum(map(len, algebra_pairs.values())),
                "algebra_descriptor_pairs": len(algebra_pairs),
            },
            sort_keys=True,
        )
    )
    for number, (key, members) in enumerate(algebra_pairs.items()):
        source_descriptor, target_descriptor = key
        proof = atlas.quadratic_separator_fast(source_descriptor, target_descriptor, max_block_size=64)
        print(
            "ALGEBRA_PAIR",
            number,
            len(members),
            members[0][1]["proof"],
            "K3P_QUADRATIC" if proof else "NONE",
            (len(proof["source_pullback"]) if proof else None),
        )
        if proof is None:
            layer, row = members[0]
            source = next(item[2] for item in rows if item[1]["row_sha256"] == row["row_sha256"])
            target_selected = next(item[4] for item in rows if item[1]["row_sha256"] == row["row_sha256"])
            source4 = atlas.restrict_rooted(source, set(range(4)))
            target4 = atlas.restrict_rooted(target_selected, set(range(4)))
            cert = k3p_four_port_polynomial(atlas, source4, target4)
            print("FOUR_PORT_CERT", number, cert)


if __name__ == "__main__":
    main()
