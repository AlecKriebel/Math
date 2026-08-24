#!/usr/bin/env python3
"""Independent fail-closed replay of the three-port cycle closure."""

from __future__ import annotations

import argparse
import ast
import collections
import gzip
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

from cycle_common import (
    DEFAULT_ARTIFACT_ROOT,
    DEFAULT_PACKAGE_ROOT,
    canonical_data,
    canonical_json_bytes,
    descriptor_sha256,
    load_atlas,
    read_json,
    sha_file,
    sha_object,
)


class ReplayFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ReplayFailure(message)


def audit_candidates(graph):
    answer = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        if graph.nodes[head].get("role") == "leaf":
            continue
        if graph.nodes[tail].get("role") == "root":
            continue
        answer.append(
            {"tail": repr(tail), "head": repr(head), "edge_role": data.get("edge_role")}
        )
    return answer


def audit_insert(atlas, graph, candidate, label):
    answer = graph.copy()
    tail, head = ast.literal_eval(candidate["tail"]), ast.literal_eval(candidate["head"])
    require(answer.has_edge(tail, head), "REPLAY_INSERTION_EDGE_MISSING")
    edge_data = dict(answer.edges[tail, head])
    answer.remove_edge(tail, head)
    subdivision = ("cycle_restoration_subdivision", label, repr(tail), repr(head))
    leaf = ("leaf", "cycle_restoration", label)
    require(subdivision not in answer and leaf not in answer, "REPLAY_NODE_COLLISION")
    answer.add_node(subdivision, role="tree", label=None, dummy=False)
    answer.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    answer.add_edge(tail, subdivision, **edge_data)
    answer.add_edge(subdivision, head, **edge_data)
    answer.add_edge(subdivision, leaf, edge_role="arm")
    atlas.validate_graph(answer)
    return answer


def audit_promote(atlas, record, permutation, roles):
    answer = atlas.relabel_record(record, tuple(permutation)).graph
    for offset, role in enumerate(roles):
        matches = [
            node for node, data in answer.nodes(data=True) if data.get("dummy_name") == role
        ]
        require(len(matches) == 1, "REPLAY_TARGET_ROLE_MULTIPLICITY")
        data = answer.nodes[matches[0]]
        data["label"], data["dummy"], data["dummy_name"] = 3 + offset, False, None
    labels = sorted(
        data["label"]
        for _, data in answer.nodes(data=True)
        if isinstance(data.get("label"), int)
    )
    require(labels == list(range(3 + len(roles))), "REPLAY_PROMOTED_LABEL_SET")
    atlas.validate_graph(answer)
    return answer


def audit_split_json(values):
    rows = []
    for split in values:
        require(split != ("star",), "REPLAY_STAR_QUARTET")
        rows.append([list(split[0]), list(split[1])])
    return sorted(rows)


def audit_topology(source_signature, target_signature):
    source_labels, source_quartets, source_triples = source_signature
    target_labels, target_quartets, target_triples = target_signature
    require(source_labels == target_labels, "REPLAY_LABEL_SET_MISMATCH")
    for source_row, target_row in zip(source_quartets, target_quartets):
        quartet, source_values = source_row
        other, target_values = target_row
        require(quartet == other, "REPLAY_QUARTET_ALIGNMENT")
        if source_values == target_values:
            continue
        source_set, target_set = set(source_values), set(target_values)
        require(source_set and target_set, "REPLAY_EMPTY_DISPLAYED_SET")
        if len(source_set) == 1:
            split = min(source_set, key=repr)
            zero_on, positive_on, kind = "source", "target", "I_singleton"
        elif len(target_set) == 1:
            split = min(target_set, key=repr)
            zero_on, positive_on, kind = "target", "source", "I_singleton"
        elif target_set - source_set:
            split = min(target_set - source_set, key=repr)
            zero_on, positive_on, kind = "source", "target", "J_membership"
        else:
            split = min(source_set - target_set, key=repr)
            zero_on, positive_on, kind = "target", "source", "J_membership"
        return {
            "reason": "displayed_quartet_mismatch",
            "quartet": list(quartet),
            "source_displayed_splits": audit_split_json(source_set),
            "target_displayed_splits": audit_split_json(target_set),
            "invariant_kind": kind,
            "distinguished_split": [list(split[0]), list(split[1])],
            "zero_on": zero_on,
            "strictly_positive_on": positive_on,
            "theorem": "Englander-et-al-v4-Propositions-2.9-2.10-Theorem-2.11",
        }
    source_types, target_types = dict(source_triples), dict(target_triples)
    for triple in sorted(source_types):
        if {source_types[triple], target_types[triple]} != {"tree", "sunlet"}:
            continue
        source_type, target_type = source_types[triple], target_types[triple]
        return {
            "reason": "tree_sunlet_strict_sign",
            "triple": list(triple),
            "source_type": source_type,
            "target_type": target_type,
            "zero_on": "source" if source_type == "tree" else "target",
            "strictly_negative_on": "source" if source_type == "sunlet" else "target",
            "invariant": "T3=V^2*X_g-X_s^2*Y_g*Z_g",
            "sunlet_pullback": "-a_s^2*b_s^2*a_g*b_g*c_g^2*f_s^2*delta*(1-delta)*d_g*e_g*(1-f_g)^2",
        }
    return None


def audit_witness_id(content):
    prefix = "QW" if content["reason"] == "displayed_quartet_mismatch" else "TS"
    return f"{prefix}:{sha_object(content)}"


def audit_transports(atlas, source_graph, target_graph, relation):
    source_mixed, target_mixed = atlas.sd0_mixed(source_graph), atlas.sd0_mixed(target_graph)
    if relation == "isomorphic":
        pairs = [(None, None)]
    else:
        require(relation == "triangle", "REPLAY_BAD_TRANSPORT_RELATION")
        pairs = [
            (left, right)
            for left in atlas._mixed_triangle_edges(source_mixed)
            for right in atlas._mixed_triangle_edges(target_mixed)
        ]
    node_match = lambda x, y: x.get("kind") == y.get("kind") and x.get("label") == y.get("label")
    edge_match = lambda x, y: x.get("head") == y.get("head")
    records = {}
    for left_triangle, right_triangle in pairs:
        left = atlas.mixed_incidence_graph(source_mixed, left_triangle)
        right = atlas.mixed_incidence_graph(target_mixed, right_triangle)
        matcher = atlas.nx.algorithms.isomorphism.GraphMatcher(
            left, right, node_match=node_match, edge_match=edge_match
        )
        for mapping in matcher.isomorphisms_iter():
            ordered_mapping = sorted(
                mapping.items(), key=lambda pair: canonical_json_bytes(pair[0])
            )
            record = {
                "relation": relation,
                "incidence_node_mapping_source_to_target": [
                    [canonical_data(a), canonical_data(b)]
                    for a, b in ordered_mapping
                ],
                "source_triangle_edges": None,
                "target_triangle_edges": None,
            }
            if left_triangle is not None:
                record["source_triangle_edges"] = sorted(
                    [
                        sorted(
                            [canonical_data(a), canonical_data(b)],
                            key=lambda item: canonical_json_bytes(item),
                        )
                        for a, b in left_triangle
                    ],
                    key=lambda item: canonical_json_bytes(item),
                )
                record["target_triangle_edges"] = sorted(
                    [
                        sorted(
                            [canonical_data(a), canonical_data(b)],
                            key=lambda item: canonical_json_bytes(item),
                        )
                        for a, b in right_triangle
                    ],
                    key=lambda item: canonical_json_bytes(item),
                )
            records[sha_object(record)] = record
    return [records[key] for key in sorted(records)]


class Ledger:
    def __init__(self, path, metadata):
        self.path, self.metadata = path, metadata
        self.digest = hashlib.sha256()
        self.byte_count = 0
        self.row_count = 0
        self.handle = gzip.open(path, "rb")

    def next(self):
        line = self.handle.readline()
        require(line, f"REPLAY_LEDGER_EARLY_EOF:{self.path.name}")
        self.digest.update(line)
        self.byte_count += len(line)
        self.row_count += 1
        row = json.loads(line)
        require(line == canonical_json_bytes(row) + b"\n", "REPLAY_NONCANONICAL_LEDGER_ROW")
        return row

    def finish(self):
        require(not self.handle.readline(), f"REPLAY_LEDGER_TRAILING_ROW:{self.path.name}")
        self.handle.close()
        require(self.row_count == self.metadata["rows"], "REPLAY_LEDGER_ROW_COUNT")
        require(self.byte_count == self.metadata["plain_bytes"], "REPLAY_LEDGER_BYTE_COUNT")
        require(self.digest.hexdigest() == self.metadata["plain_sha256"], "REPLAY_LEDGER_PLAIN_HASH")


def build_audit_configurations(atlas, sources):
    answer = {}
    for source_index, source in enumerate(sources):
        states = [([], source.graph)]
        for depth in range(1, 5):
            children = []
            for path, graph in states:
                candidates = audit_candidates(graph)
                require(len(candidates) == depth + 2, "REPLAY_CANDIDATE_CENSUS")
                for insertion_index, candidate in enumerate(candidates):
                    child = audit_insert(atlas, graph, candidate, depth + 2)
                    children.append((path + [insertion_index], child))
            states = children
            answer[(source_index, depth)] = [
                (path, graph, atlas.topology_signature(graph)) for path, graph in states
            ]
    return answer


def sparse_hash(polynomial):
    return sha_object(
        [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())]
    )


def replay_quadratic(atlas, source_descriptor, target_descriptor, certificate, rank_witnesses):
    require(certificate["source_descriptor_sha256"] == descriptor_sha256(source_descriptor), "REPLAY_QUADRATIC_SOURCE_DIGEST")
    require(certificate["target_descriptor_sha256"] == descriptor_sha256(target_descriptor), "REPLAY_QUADRATIC_TARGET_DIGEST")
    pairs = [tuple(pair) for pair in certificate["coordinate_pairs"]]
    coefficients = tuple(certificate["coefficients"])
    source_outputs = atlas.output_sparse_polynomials(source_descriptor)
    target_outputs = atlas.output_sparse_polynomials(target_descriptor)
    source_columns = [atlas.sparse_mul(source_outputs[i], source_outputs[j]) for i, j in pairs]
    target_columns = [atlas.sparse_mul(target_outputs[i], target_outputs[j]) for i, j in pairs]
    target_pullback = atlas.sparse_lincomb(target_columns, coefficients)
    source_pullback = atlas.sparse_lincomb(source_columns, coefficients)
    require(not target_pullback, "REPLAY_QUADRATIC_NONZERO_TARGET")
    require(source_pullback, "REPLAY_QUADRATIC_ZERO_SOURCE")
    require(sparse_hash(source_pullback) == certificate["source_pullback_sha256"], "REPLAY_QUADRATIC_PULLBACK_HASH")
    witness = certificate["strict_D_plus_witness"]
    edge_pairs = tuple((Fraction(a), Fraction(b)) for a, b in witness["edge_pairs"])
    lambdas = tuple(Fraction(value) for value in witness["lambdas"])
    require(all(0 < s < 1 and 0 < g < 1 and g > 2 * s - 1 for s, g in edge_pairs), "REPLAY_WITNESS_OUTSIDE_D_PLUS")
    require(all(0 < value < 1 for value in lambdas), "REPLAY_INHERITANCE_OUTSIDE_OPEN_INTERVAL")
    point = tuple(value for pair in edge_pairs for value in pair) + lambdas
    value = Fraction(0)
    for exponent, coefficient in source_pullback.items():
        term = Fraction(coefficient)
        for coordinate, power in zip(point, exponent):
            if power:
                term *= coordinate**power
        value += term
    require(value == Fraction(witness["value"]) and value, "REPLAY_STRICT_WITNESS_VALUE")
    deterministic = atlas.quadratic_separator_fast(source_descriptor, target_descriptor, max_block_size=16)
    require(deterministic is not None, "REPLAY_EXHAUSTIVE_QUADRATIC_SEARCH_MISSED")
    require([list(pair) for pair in deterministic["coordinate_pairs"]] == certificate["coordinate_pairs"], "REPLAY_QUADRATIC_PAIR_REASSIGNMENT")
    require(list(deterministic["coefficients"]) == certificate["coefficients"], "REPLAY_QUADRATIC_COEFFICIENT_REASSIGNMENT")
    for descriptor, field, label in (
        (source_descriptor, "source_descriptor_sha256", "source_witnessed_jacobian_rank"),
        (target_descriptor, "target_descriptor_sha256", "target_witnessed_jacobian_rank"),
    ):
        digest = certificate[field]
        rank_row = rank_witnesses[digest]
        candidates = [atlas.rank_certificate(descriptor, salt=salt) for salt in range(8)]
        best = max(candidates, key=lambda row: int(row["rank"]))
        require(canonical_data(best) == rank_row["lower_certificate"], "REPLAY_RANK_LOWER_CERTIFICATE")
        require(int(best["rank"]) == certificate[label], "REPLAY_RANK_WITNESS_ASSIGNMENT")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=DEFAULT_PACKAGE_ROOT)
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    args = parser.parse_args()
    atlas = load_atlas(args.package_root)
    root = args.artifact_root
    summary = read_json(root / "cycle_three_port_summary.json")
    payload = summary.pop("payload_sha256")
    require(sha_object(summary) == payload, "REPLAY_SUMMARY_PAYLOAD_HASH")
    summary["payload_sha256"] = payload
    require(summary["status"] == "PASS", "REPLAY_SUMMARY_NOT_PASS")
    for name, metadata in summary["artifacts"].items():
        path = root / name
        require(path.exists(), f"REPLAY_MISSING_ARTIFACT:{name}")
        require(sha_file(path) == metadata["sha256"], f"REPLAY_ARTIFACT_HASH:{name}")

    topology_payload = read_json(root / "topology_witnesses.json")
    transport_payload = read_json(root / "transport_certificates.json")
    quadratic_payload = read_json(root / "quadratic_certificates.json")
    rank_payload = read_json(root / "rank_witnesses.json")
    anchor_payload = read_json(root / "physical_anchors.json")
    topology_certificates = topology_payload["witnesses"]
    transport_certificates = transport_payload["certificates"]
    quadratic_certificates = quadratic_payload["certificates"]
    rank_witnesses = rank_payload["certificates"]
    for identifier, content in topology_certificates.items():
        require(audit_witness_id(content) == identifier, "REPLAY_TOPOLOGY_CERTIFICATE_ID")
    for identifier, content in transport_certificates.items():
        require(f"TR:{sha_object(content)}" == identifier, "REPLAY_TRANSPORT_CERTIFICATE_ID")
    for identifier, content in quadratic_certificates.items():
        expected = f"QD:{sha_object({'source_descriptor_sha256': content['source_descriptor_sha256'], 'target_descriptor_sha256': content['target_descriptor_sha256']})}"
        require(expected == identifier == content["certificate_id"], "REPLAY_QUADRATIC_CERTIFICATE_ID")

    sources = tuple(atlas.source_supports(core_ids=("cycle",)))
    targets = tuple(atlas.target_completions(3, True) + atlas.target_completions(3, False))
    permutations = tuple(itertools.permutations(range(3)))
    require((len(sources), len(targets), len(permutations)) == (2, 1120, 6), "REPLAY_PRIMITIVE_CENSUS")
    source_signatures = [atlas.topology_signature(source.graph) for source in sources]
    target_signatures = [atlas.topology_signature(atlas.selected_graph_from_completion(target)) for target in targets]
    base_ledger = Ledger(root / "base_raw_ledger.jsonl.gz", summary["artifacts"]["base_raw_ledger.jsonl.gz"])
    root_rows = []
    expected_anchors = []
    seen_topology = set()
    seen_transports = set()
    base_counts = collections.Counter()
    raw_id = 0
    for source_index, source in enumerate(sources):
        for target_index, target in enumerate(targets):
            for permutation_index, permutation in enumerate(permutations):
                permuted = atlas.permute_signature(target_signatures[target_index], permutation)
                content = audit_topology(source_signatures[source_index], (source_signatures[source_index][0], permuted[0], permuted[1]))
                certificate_id = None
                if content is not None:
                    require(content["reason"] == "tree_sunlet_strict_sign", "REPLAY_BASE_QUARTET")
                    category = "tree_sunlet_pointwise_excluded"
                    certificate_id = audit_witness_id(content)
                    require(topology_certificates[certificate_id] == content, "REPLAY_BASE_TOPOLOGY_CERTIFICATE")
                    seen_topology.add(certificate_id)
                elif target.dummy_labels:
                    category = "restoration_root"
                else:
                    target_graph = atlas.relabel_record(target, permutation).graph
                    category = atlas.mixed_relation_exact(source.graph, target_graph)
                    require(category in {"isomorphic", "triangle"}, "REPLAY_BASE_NONTERMINAL")
                    transports = audit_transports(atlas, source.graph, target_graph, category)
                    require(len(transports) == 1, "REPLAY_BASE_TRANSPORT_MULTIPLICITY")
                    certificate_id = f"TR:{sha_object(transports[0])}"
                    require(transport_certificates[certificate_id] == transports[0], "REPLAY_BASE_TRANSPORT")
                    seen_transports.add(certificate_id)
                    expected_anchors.append({
                        "anchor_id": f"A3:{raw_id}", "origin": "base_no_dummy", "port_count": 3,
                        "base_raw_id": raw_id, "source_index": source_index, "target_index": target_index,
                        "permutation_index": permutation_index, "port_permutation": list(permutation),
                        "relation": category, "transport_certificate_id": certificate_id,
                    })
                expected = {
                    "raw_id": raw_id, "source_index": source_index, "target_index": target_index,
                    "permutation_index": permutation_index, "port_permutation": list(permutation),
                    "dummy_roles": list(target.dummy_labels), "category": category,
                    "certificate_id": certificate_id,
                }
                require(base_ledger.next() == expected, f"REPLAY_BASE_ROW:{raw_id}")
                if category == "restoration_root":
                    root_content = {
                        "base_raw_id": raw_id, "source_index": source_index, "target_index": target_index,
                        "permutation_index": permutation_index, "port_permutation": list(permutation),
                        "dummy_roles": list(target.dummy_labels),
                    }
                    root_content["root_id"] = f"R:{sha_object(root_content)}"
                    root_rows.append(root_content)
                base_counts[category] += 1
                raw_id += 1
    base_ledger.finish()
    require(base_counts == collections.Counter(summary["base"]["categories"]), "REPLAY_BASE_COUNTS")
    roots_ledger = Ledger(root / "restoration_roots.jsonl.gz", summary["artifacts"]["restoration_roots.jsonl.gz"])
    for index, expected in enumerate(root_rows):
        require(roots_ledger.next() == expected, f"REPLAY_ROOT_ROW:{index}")
    roots_ledger.finish()

    configurations = build_audit_configurations(atlas, sources)
    full_ledger = Ledger(root / "full_completion_ledger.jsonl.gz", summary["artifacts"]["full_completion_ledger.jsonl.gz"])
    full_counts = collections.Counter()
    quadratic_multiplicity = collections.Counter()
    replayed_quadratics = set()
    raw_id = 0
    for root_row in root_rows:
        roles = tuple(root_row["dummy_roles"])
        depth = len(roles)
        source_index = root_row["source_index"]
        target_graph = audit_promote(atlas, targets[root_row["target_index"]], permutations[root_row["permutation_index"]], roles)
        target_signature = atlas.topology_signature(target_graph)
        target_descriptor = None
        for placement_path, source_graph, source_signature in configurations[(source_index, depth)]:
            content = audit_topology(source_signature, target_signature)
            if content is not None:
                category = "quartet_pointwise_excluded" if content["reason"] == "displayed_quartet_mismatch" else "tree_sunlet_pointwise_excluded"
                certificate_id = audit_witness_id(content)
                require(topology_certificates[certificate_id] == content, "REPLAY_FULL_TOPOLOGY_CERTIFICATE")
                seen_topology.add(certificate_id)
            else:
                relation = atlas.mixed_relation_exact(source_graph, target_graph)
                if relation == "isomorphic":
                    category = "isomorphic"
                    transports = audit_transports(atlas, source_graph, target_graph, relation)
                    require(len(transports) == 1, "REPLAY_FULL_TRANSPORT_MULTIPLICITY")
                    certificate_id = f"TR:{sha_object(transports[0])}"
                    require(transport_certificates[certificate_id] == transports[0], "REPLAY_FULL_TRANSPORT")
                    seen_transports.add(certificate_id)
                    expected_anchors.append({
                        "anchor_id": f"AF:{raw_id}", "origin": "fixed_full_restoration",
                        "port_count": 3 + depth, "full_raw_id": raw_id,
                        "root_id": root_row["root_id"], "base_raw_id": root_row["base_raw_id"],
                        "source_index": source_index, "target_index": root_row["target_index"],
                        "permutation_index": root_row["permutation_index"],
                        "port_permutation": list(permutations[root_row["permutation_index"]]),
                        "dummy_roles_in_label_order": list(roles),
                        "source_placement_path": placement_path, "relation": relation,
                        "transport_certificate_id": certificate_id,
                    })
                else:
                    require(relation in {None, "none"}, "REPLAY_FULL_UNEXPECTED_RELATION")
                    category = "quadratic_separated"
                    source_descriptor = atlas.model_descriptor_fast2(source_graph)
                    if target_descriptor is None:
                        target_descriptor = atlas.model_descriptor_fast2(target_graph)
                    pair = {
                        "source_descriptor_sha256": descriptor_sha256(source_descriptor),
                        "target_descriptor_sha256": descriptor_sha256(target_descriptor),
                    }
                    certificate_id = f"QD:{sha_object(pair)}"
                    certificate = quadratic_certificates[certificate_id]
                    if certificate_id not in replayed_quadratics:
                        replay_quadratic(atlas, source_descriptor, target_descriptor, certificate, rank_witnesses)
                        replayed_quadratics.add(certificate_id)
                    quadratic_multiplicity[certificate_id] += 1
            expected = {
                "raw_id": raw_id, "root_id": root_row["root_id"], "base_raw_id": root_row["base_raw_id"],
                "source_index": source_index, "target_index": root_row["target_index"],
                "permutation_index": root_row["permutation_index"],
                "dummy_roles_in_label_order": list(roles), "port_count": 3 + depth,
                "source_placement_path": placement_path, "category": category,
                "certificate_id": certificate_id,
            }
            require(full_ledger.next() == expected, f"REPLAY_FULL_ROW:{raw_id}")
            full_counts[category] += 1
            raw_id += 1
    full_ledger.finish()
    require(full_counts == collections.Counter(summary["restoration"]["categories"]), "REPLAY_FULL_COUNTS")
    require(set(quadratic_certificates) == replayed_quadratics, "REPLAY_QUADRATIC_COVERAGE")
    require({key: quadratic_multiplicity[key] for key in sorted(quadratic_multiplicity)} == quadratic_payload["raw_multiplicity"], "REPLAY_QUADRATIC_MULTIPLICITY")
    require(set(topology_certificates) == seen_topology, "REPLAY_TOPOLOGY_CERTIFICATE_COVERAGE")
    require(set(transport_certificates) == seen_transports, "REPLAY_TRANSPORT_CERTIFICATE_COVERAGE")
    require(anchor_payload["anchors"] == expected_anchors, "REPLAY_PHYSICAL_ANCHOR_LEDGER")
    require(len(expected_anchors) == 36, "REPLAY_PHYSICAL_ANCHOR_CENSUS")
    result = {
        "schema": "k2p-cycle-three-port-independent-replay-v1",
        "status": "PASS",
        "optimized_mode": not __debug__,
        "base_raw_relations": sum(base_counts.values()),
        "restoration_roots": len(root_rows),
        "physical_completions": sum(full_counts.values()),
        "quadratic_raw_relations": sum(quadratic_multiplicity.values()),
        "quadratic_descriptor_pair_classes": len(replayed_quadratics),
        "physical_anchors": len(expected_anchors),
        "unresolved": 0,
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ReplayFailure, KeyError, ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"CYCLE_REPLAY_FAIL:{exc}") from exc
