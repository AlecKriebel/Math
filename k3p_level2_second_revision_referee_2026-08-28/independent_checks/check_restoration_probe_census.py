#!/usr/bin/env python3
"""Independent streaming census of restoration and probe evidence.

Every stored row is streamed.  The script recomputes file hashes, canonical
self-hashes, ordered roots, counts, cross-references, and strict witness
margins.  It imports no package module and does not invoke a package verifier.
Semantic reconstruction of selected rows is performed by the companion
``check_probe_semantic_samples.py``.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("run without -O so fail-closed assertions remain active")


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def locate_proof_root(package_root):
    for candidate in (package_root / "proof_package", package_root):
        if (candidate / "restoration/RESTORATION_MANIFEST.json").is_file():
            return candidate
    raise FileNotFoundError("could not locate proof_package beneath --package-root")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def ordered_add(root, row):
    return sha({"previous": root, "row_sha256": sha(row)})


def iter_gzip_jsonl(path):
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            yield json.loads(line)


def ct_margin(triple):
    c, g, t = map(Q, triple)
    return min(
        c, g, t, 1-c, 1-g, 1-t,
        1+c-g-t, 1-c+g-t, 1-c-g+t,
        c-g*t, g-c*t, t-c*g,
    )


def validate_transport_binding(row):
    record_id, record = row["record_id"], row["record"]
    public = dict(record)
    ordinary = public.pop("ordinary_triangle_arrowhead_witness", None)
    claimed = public.pop("transport_sha256")
    assert record_id == claimed == sha(public)
    vertex_map = dict(record["vertex_map"])
    assert len(vertex_map) == len(record["vertex_map"]) == len(set(vertex_map.values()))
    source_edges, target_edges = set(), set()
    for source, target in record["mixed_edge_map"]:
        source_edges.add(tuple(source))
        target_edges.add(tuple(target))
        assert {vertex_map[source[0]], vertex_map[source[1]]} == set(target)
    assert len(source_edges) == len(target_edges) == len(record["mixed_edge_map"])
    relation = record["relation"]
    if relation == "isomorphic":
        assert record["source_triangle_edges"] is None
        assert record["target_triangle_edges"] is None
        assert ordinary is None
    else:
        assert relation == "triangle" and ordinary is not None
        for side in ("source", "target"):
            triangle = record[f"{side}_triangle_edges"]
            headed = ordinary[f"{side}_headed_edges"]
            common = ordinary[f"{side}_common_reticulation"]
            assert len(triangle) == 3 and len(headed) == 2
            assert all(common in edge and edge in triangle for edge in headed)
    return relation


def main():
    args = arguments()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    proof_root = locate_proof_root(args.package_root)
    restoration_dir = proof_root / "restoration"
    probe_dir = proof_root / "probes"

    restoration_manifest = json.loads((restoration_dir / "RESTORATION_MANIFEST.json").read_text(encoding="utf-8"))
    logical_restoration_manifest = dict(restoration_manifest)
    claimed_restoration_manifest_hash = logical_restoration_manifest.pop("payload_sha256")
    assert claimed_restoration_manifest_hash == sha(logical_restoration_manifest)
    assert restoration_manifest["status"] == "PASS"
    frozen_forest_path = (
        proof_root
        / "input_frozen/model_independent_topology_package/anchor_inputs/corrected_restoration_forest.json"
    )
    assert sha_file(frozen_forest_path) == restoration_manifest["inputs"]["frozen_restoration_forest_sha256"]
    frozen_forest = json.loads(frozen_forest_path.read_text(encoding="utf-8"))
    assert len(frozen_forest["first_coverage"]) == 36568
    assert len(frozen_forest["second_coverage"]) == 256
    restoration_ledger_path = restoration_dir / "restoration_ledger.jsonl.gz"
    assert sha_file(restoration_ledger_path) == restoration_manifest["ledger"]["sha256"]
    restoration_registry_path = restoration_dir / "restoration_proof_registry.json.gz"
    assert sha_file(restoration_registry_path) == restoration_manifest["proof_registry"]["sha256"]
    with gzip.open(restoration_registry_path, "rt", encoding="utf-8") as handle:
        registry = json.load(handle)
    logical_registry = dict(registry)
    claimed_registry_hash = logical_registry.pop("payload_sha256")
    assert claimed_registry_hash == sha(logical_registry) == restoration_manifest["proof_registry"]["payload_sha256"]
    prefixes = {
        "displayed_quartet_mismatch": "Q:",
        "k3p_tree_sunlet_sos": "K3P-TS:",
        "k3p_exact_multihomogeneous_quadratic": "K3P-Q2:",
        "k3p_direct_marginal_quartic": "K3P-M4:",
    }
    proof_ids = set()
    proof_kinds_by_id = {}
    registry_counts = Counter()
    minimum_witness_margin = None
    for proof_kind, proofs in registry["proofs"].items():
        assert proof_kind in prefixes
        for proof_id, certificate in proofs.items():
            assert proof_id == prefixes[proof_kind] + sha(certificate)
            assert proof_id not in proof_kinds_by_id
            proof_ids.add(proof_id)
            proof_kinds_by_id[proof_id] = proof_kind
            registry_counts[proof_kind] += 1
            if proof_kind == "displayed_quartet_mismatch":
                assert certificate["source_splits"] != certificate["target_splits"]
            elif proof_kind == "k3p_tree_sunlet_sos":
                assert {certificate["tree_on"], certificate["sunlet_on"]} == {"source", "target"}
                assert certificate["sunlet_nonzero_circuit_count"] == 6
            else:
                assert certificate["target_pullback_term_count"] == 0
                assert certificate["source_pullback_term_count"] > 0
                witness = certificate["strict_source_witness"]
                margin = min(
                    [ct_margin(triple) for triple in witness["edge_triples"]]
                    + [min(Q(value), 1-Q(value)) for value in witness["inheritance"]]
                )
                assert margin > 0 and Q(witness["evaluation"]) != 0
                minimum_witness_margin = margin if minimum_witness_margin is None else min(minimum_witness_margin, margin)
    assert dict(registry_counts) == restoration_manifest["proof_registry"]["certificate_counts"]

    layer_counts, proof_use, roots, used_proofs = Counter(), Counter(), set(), set()
    legacy_status_counts, active_status_counts = Counter(), Counter()
    row_hashes, restoration_samples = [], []
    first_by_legacy_hash = {}
    legacy_hashes_by_layer = {1: set(), 2: set()}
    continuation_legacy_hashes = set()
    second_parent_counts = Counter()
    second_parent_indices = defaultdict(set)
    early_termination_count = 0
    legacy_full_forest_rows = 0
    restoration_rows = 0
    for index, row in enumerate(iter_gzip_jsonl(restoration_ledger_path)):
        public = dict(row)
        claimed = public.pop("row_sha256")
        assert claimed == sha(public)
        assert row["edge_index"] == index
        row_hashes.append(claimed)
        layer = row["layer"]
        assert layer in (1, 2)
        layer_counts[layer] += 1
        legacy_status_counts[(layer, row["legacy_structural_status"])] += 1
        active_status_counts[(layer, row["active_k3p_status"])] += 1
        proof_use[row["proof_kind"]] += 1
        roots.add(row["root_id"])
        used_proofs.add(row["proof_id"])
        assert row["proof_id"] in proof_ids
        assert proof_kinds_by_id[row["proof_id"]] == row["proof_kind"]
        legacy_hash = row["legacy_row_sha256"]
        assert legacy_hash not in legacy_hashes_by_layer[layer]
        legacy_hashes_by_layer[layer].add(legacy_hash)
        if layer == 1:
            assert index < 36568
            frozen = frozen_forest["first_coverage"][index]
            assert legacy_hash == frozen["row_sha256"]
            assert row["legacy_structural_status"] == frozen["status"]
            assert row["root_id"] == frozen["root_id"]
            assert row["restored_role"] == frozen["restored_role"]
            assert row["restored_label"] == frozen["restored_label"]
            assert row["source_insertion_index"] == frozen["source_insertion_index"]
            assert row["remaining_roles"] == frozen["remaining_roles"]
            assert row["source_parent_transport_id"] == frozen["source_parent_transport_id"]
            assert row["target_parent_transport_id"] == frozen["target_parent_transport_id"]
            assert row["active_k3p_status"] == "separated"
            assert row["restored_label"] == 4
            assert legacy_hash not in first_by_legacy_hash
            first_by_legacy_hash[legacy_hash] = row
            if row["legacy_structural_status"] == "continuation":
                assert row.get("k3p_refinement") == "early_termination_before_redundant_depth2"
                assert row["proof_kind"] == "k3p_direct_marginal_quartic"
                assert len(row["remaining_roles"]) == 1
                continuation_legacy_hashes.add(legacy_hash)
                early_termination_count += 1
            else:
                assert row["legacy_structural_status"] == "separated"
                assert "k3p_refinement" not in row
        else:
            assert 36568 <= index < 36824
            frozen = frozen_forest["second_coverage"][index - 36568]
            assert legacy_hash == frozen["row_sha256"]
            assert row["parent_first_row_sha256"] == frozen["parent_first_row_sha256"]
            assert row["legacy_structural_status"] == frozen["status"]
            assert row["root_id"] == frozen["root_id"]
            assert row["restored_role"] == frozen["second_restored_role"]
            assert row["restored_label"] == frozen["second_restored_label"]
            assert row["source_insertion_index"] == frozen["second_source_insertion_index"]
            assert row["legacy_structural_status"] == "separated"
            assert row["active_k3p_status"] == "redundant_verified"
            assert row.get("legacy_full_forest_only") is True
            assert row["restored_label"] == 5
            parent_hash = row["parent_first_row_sha256"]
            assert parent_hash in first_by_legacy_hash
            parent = first_by_legacy_hash[parent_hash]
            assert parent["legacy_structural_status"] == "continuation"
            assert parent["active_k3p_status"] == "separated"
            assert row["root_id"] == parent["root_id"]
            assert row["restored_role"] == parent["remaining_roles"][0]
            second_parent_counts[parent_hash] += 1
            second_parent_indices[parent_hash].add(row["source_insertion_index"])
            legacy_full_forest_rows += 1
        if index in (0, 36567, 36568, 36823):
            restoration_samples.append({
                "edge_index": index,
                "row_sha256": claimed,
                "proof_id": row["proof_id"],
                "layer": row["layer"],
            })
        restoration_rows += 1
    assert restoration_rows == restoration_manifest["ledger"]["rows"]
    assert sha(row_hashes) == restoration_manifest["ledger"]["ordered_row_hash_root"]
    assert layer_counts == Counter({1: 36568, 2: 256})
    assert legacy_status_counts == Counter({
        (1, "separated"): 36536,
        (1, "continuation"): 32,
        (2, "separated"): 256,
    })
    assert active_status_counts == Counter({
        (1, "separated"): 36568,
        (2, "redundant_verified"): 256,
    })
    assert len(first_by_legacy_hash) == len(legacy_hashes_by_layer[1]) == 36568
    assert len(legacy_hashes_by_layer[2]) == 256
    assert early_termination_count == len(continuation_legacy_hashes) == 32
    assert set(second_parent_counts) == continuation_legacy_hashes
    assert set(second_parent_counts.values()) == {8}
    assert set(second_parent_indices) == continuation_legacy_hashes
    assert all(indices == set(range(8)) for indices in second_parent_indices.values())
    assert legacy_full_forest_rows == 256
    assert used_proofs == proof_ids

    coherence = json.loads((probe_dir / "K3P_PROBE_COHERENCE_CERTIFICATE.json").read_text(encoding="utf-8"))
    logical_coherence = dict(coherence)
    claimed_coherence_hash = logical_coherence.pop("payload_sha256")
    assert claimed_coherence_hash == sha(logical_coherence)
    assert coherence["status"] == "PASS"
    transports, transport_counts = {}, Counter()
    transport_root = sha([])
    transport_samples = {}
    transport_path = probe_dir / "exact_transport_ledger.jsonl.gz"
    assert sha_file(transport_path) == coherence["registries"]["exact_transports"]["sha256"]
    for index, row in enumerate(iter_gzip_jsonl(transport_path)):
        relation = validate_transport_binding(row)
        record_id = row["record_id"]
        assert record_id not in transports
        transports[record_id] = relation
        transport_counts[relation] += 1
        transport_root = ordered_add(transport_root, row)
        transport_samples.setdefault(relation, {
            "record_index": index,
            "record_id": record_id,
            "vertices": len(row["record"]["vertex_map"]),
            "edges": len(row["record"]["mixed_edge_map"]),
        })
    exact_manifest = coherence["registries"]["exact_transports"]["ordered_records"]
    assert len(transports) == exact_manifest["rows"] == coherence["registries"]["exact_transports"]["unique_records"]
    assert transport_root == exact_manifest["ordered_hash_root"]

    restrictions = set()
    restriction_root = sha([])
    restriction_path = probe_dir / "parent_restriction_ledger.jsonl.gz"
    assert sha_file(restriction_path) == coherence["registries"]["parent_restrictions"]["sha256"]
    for row in iter_gzip_jsonl(restriction_path):
        record_id = row["record_id"]
        assert record_id == "R:" + sha(row["record"])
        assert record_id not in restrictions
        restrictions.add(record_id)
        restriction_root = ordered_add(restriction_root, row)
    restriction_manifest = coherence["registries"]["parent_restrictions"]["ordered_records"]
    assert len(restrictions) == restriction_manifest["rows"]
    assert restriction_root == restriction_manifest["ordered_hash_root"]

    separation_path = probe_dir / "separation_proof_registry.json.gz"
    assert sha_file(separation_path) == coherence["registries"]["separation"]["sha256"]
    with gzip.open(separation_path, "rt", encoding="utf-8") as handle:
        separation = json.load(handle)
    logical_separation = dict(separation)
    claimed_separation_hash = logical_separation.pop("payload_sha256")
    assert claimed_separation_hash == sha(logical_separation) == coherence["registries"]["separation"]["payload_sha256"]
    topological = separation["separation_proof_registry"]
    tree_sunlet = separation["k3p_tree_sunlet_registry"]["certificates"]
    assert len(topological) == coherence["registries"]["separation"]["topological_proofs"]
    assert len(tree_sunlet) == coherence["registries"]["separation"]["k3p_tree_sunlet_relation_certificates"]
    assert all(proof_id == "Q:" + sha(certificate) for proof_id, certificate in topological.items())
    assert all(proof_id == "K3P-TS:" + sha(certificate) for proof_id, certificate in tree_sunlet.items())

    public_anchors = coherence["anchor_inventory"]["public_anchors"]
    anchors = {}
    for anchor in public_anchors:
        anchor_id = anchor["anchor_id"]
        assert anchor_id not in anchors
        assert transports[anchor["transport_id"]] == anchor["relation"]
        anchors[anchor_id] = anchor
    assert len(anchors) == coherence["anchor_inventory"]["anchors"] == 176
    assert sha([sha(anchor) for anchor in public_anchors]) == coherence["anchor_inventory"]["ordered_public_anchor_hash_root"]

    one_counts, one_origin, one_samples = Counter(), Counter(), {}
    one_root = sha([])
    one_equalities = []
    one_equality_rows = {}
    expected_one = iter(
        (anchor["anchor_id"], source_index, target_index)
        for anchor in public_anchors
        for source_index in range(anchor["source_site_count"])
        for target_index in range(anchor["target_site_count"])
    )
    one_path = probe_dir / "one_port_ledger.jsonl.gz"
    assert sha_file(one_path) == coherence["one_port"]["ledger_sha256"]
    for index, row in enumerate(iter_gzip_jsonl(one_path)):
        one_root = ordered_add(one_root, row)
        assert row["stage"] == "A+p"
        anchor = anchors[row["parent_anchor_id"]]
        assert row["origin"] == anchor["origin"]
        assert (
            row["parent_anchor_id"], row["source_site_index"], row["target_site_index"]
        ) == next(expected_one, None)
        status = row["status"]
        assert status in {"isomorphic", "triangle", "displayed_quartet_mismatch", "k3p_tree_sunlet_sos"}
        one_counts[status] += 1
        one_origin[(row["origin"], status)] += 1
        assert row["source_parent_restriction_id"] in restrictions
        assert row["target_parent_restriction_id"] in restrictions
        if status in ("isomorphic", "triangle"):
            assert transports[row["transport_id"]] == status
            assert row["parent_transport_id"] == anchor["transport_id"]
            expected_triangle = None if anchor["global_triangle"] is None else sha(anchor["global_triangle"])
            assert row["global_triangle_sha256"] == expected_triangle
            parent_id = f"P1:{row['parent_anchor_id']}:{row['source_site_index']}:{row['target_site_index']}"
            assert parent_id not in one_equality_rows
            one_equalities.append(parent_id)
            one_equality_rows[parent_id] = row
        else:
            assert row["proof_id"] in (topological if status == "displayed_quartet_mismatch" else tree_sunlet)
        one_samples.setdefault(status, {"row": index, "digest": sha(row), "parent": row["parent_anchor_id"]})
    assert one_root == coherence["one_port"]["ordered_ledger"]["ordered_hash_root"]
    assert dict(one_counts) == coherence["one_port"]["counts"]
    assert {
        f"{origin}:{status}": count for (origin, status), count in one_origin.items()
    } == coherence["one_port"]["counts_by_origin"]
    assert len(one_equalities) == 2107
    assert next(expected_one, None) is None

    parent_root = sha([])
    parent_ids = []
    parents = {}
    one_classes_by_base = defaultdict(set)
    raw_second_pairs = 0
    parent_path = probe_dir / "two_port_parent_inventory.jsonl.gz"
    assert sha_file(parent_path) == coherence["two_port"]["parent_inventory_sha256"]
    for index, row in enumerate(iter_gzip_jsonl(parent_path)):
        parent_root = ordered_add(parent_root, row)
        parent_id = row["one_port_parent_id"]
        parent_ids.append(parent_id)
        assert parent_id == one_equalities[index]
        assert parent_id not in parents
        one_row = one_equality_rows[parent_id]
        assert row["base_anchor_id"] == one_row["parent_anchor_id"]
        assert row["origin"] == one_row["origin"]
        assert row["relation"] == one_row["status"]
        assert row["first_label"] == one_row["inserted_label"]
        assert row["first_source_site_index"] == one_row["source_site_index"]
        assert row["first_target_site_index"] == one_row["target_site_index"]
        assert row["source_graph_sha256"] == one_row["source_child_graph_sha256"]
        assert row["target_graph_sha256"] == one_row["target_child_graph_sha256"]
        for side in ("source_candidate_profile", "target_candidate_profile"):
            profile = row[side]
            assert profile["site_count"] == 2*profile["port_count"] + 3*profile["reticulation_count"] - 3
            assert profile["site_count"] == len(profile["sites"])
            assert profile["ordered_site_hash_root"] == sha([sha(site) for site in profile["sites"]])
        pairs = row["source_candidate_profile"]["site_count"] * row["target_candidate_profile"]["site_count"]
        assert pairs == row["raw_second_probe_pairs"]
        raw_second_pairs += pairs
        parents[parent_id] = row
        one_classes_by_base[row["base_anchor_id"]].add(row["canonical_one_port_relation_class_id"])
    parent_manifest = coherence["two_port"]["ordered_parent_inventory"]
    assert parent_root == parent_manifest["ordered_hash_root"]
    assert len(parent_ids) == parent_manifest["rows"] == 2107
    assert len(set(parent_ids)) == len(parent_ids)
    assert raw_second_pairs == 544571

    two_counts, two_origin, reverse_counts, two_samples = Counter(), Counter(), Counter(), {}
    two_root = sha([])
    expected_two = iter(
        (parent_id, source_index, target_index)
        for parent_id in parent_ids
        for source_index in range(parents[parent_id]["source_candidate_profile"]["site_count"])
        for target_index in range(parents[parent_id]["target_candidate_profile"]["site_count"])
    )
    two_path = probe_dir / "two_port_ledger.jsonl.gz"
    assert sha_file(two_path) == coherence["two_port"]["ledger_sha256"]
    for index, row in enumerate(iter_gzip_jsonl(two_path)):
        two_root = ordered_add(two_root, row)
        assert row["stage"] == "A+p+q"
        status = row["status"]
        assert status in {"isomorphic", "triangle", "displayed_quartet_mismatch", "k3p_tree_sunlet_sos"}
        two_counts[status] += 1
        two_origin[(row["origin"], status)] += 1
        parent_id = row["one_port_parent_id"]
        assert parent_id in parents
        parent = parents[parent_id]
        assert row["base_anchor_id"] == parent["base_anchor_id"]
        assert row["origin"] == parent["origin"]
        assert row["first_label"] == parent["first_label"]
        assert row["first_source_site_index"] == parent["first_source_site_index"]
        assert row["first_target_site_index"] == parent["first_target_site_index"]
        source_index = row["second_source_site_index"]
        target_index = row["second_target_site_index"]
        assert (parent_id, source_index, target_index) == next(expected_two, None)
        source_sites = parent["source_candidate_profile"]["sites"]
        target_sites = parent["target_candidate_profile"]["sites"]
        assert row["second_source_site_id"] == source_sites[source_index]["site_id"]
        assert row["second_target_site_id"] == target_sites[target_index]["site_id"]
        assert row["source_parent_restriction_id"] in restrictions
        assert row["target_parent_restriction_id"] in restrictions
        if status in ("isomorphic", "triangle"):
            assert transports[row["transport_id"]] == status
            assert row["parent_transport_id"] == one_equality_rows[parent_id]["transport_id"]
            assert row["global_triangle_sha256"] == one_equality_rows[parent_id]["global_triangle_sha256"]
            reverse = row["reverse_order_certificate"]
            assert reverse["reverse_parent_transport_id"] in transports
            assert transports[reverse["reverse_parent_transport_id"]] == reverse["reverse_parent_relation"]
            assert reverse["same_base_anchor_id"] == row["base_anchor_id"]
            assert reverse["reverse_parent_canonical_one_port_class_id"] in one_classes_by_base[row["base_anchor_id"]]
            reverse_counts[reverse["reverse_parent_relation"]] += 1
        else:
            assert row["proof_id"] in (topological if status == "displayed_quartet_mismatch" else tree_sunlet)
            assert "reverse_order_certificate" not in row
        two_samples.setdefault(status, {"row": index, "digest": sha(row), "parent": row["one_port_parent_id"]})
    assert two_root == coherence["two_port"]["ordered_ledger"]["ordered_hash_root"]
    assert dict(two_counts) == coherence["two_port"]["counts"]
    assert {
        f"{origin}:{status}": count for (origin, status), count in two_origin.items()
    } == coherence["two_port"]["counts_by_origin"]
    assert dict(reverse_counts) == coherence["two_port"]["reverse_order_parent_relation_counts"]
    assert sum(two_counts.values()) == 544571
    assert next(expected_two, None) is None

    result = {
        "restoration": {
            "rows": restoration_rows,
            "layers": dict(layer_counts),
            "legacy_statuses": {
                f"layer_{layer}:{status}": count
                for (layer, status), count in legacy_status_counts.items()
            },
            "active_k3p_statuses": {
                f"layer_{layer}:{status}": count
                for (layer, status), count in active_status_counts.items()
            },
            "legacy_continuation_parents": len(continuation_legacy_hashes),
            "redundant_depth_two_rows": legacy_full_forest_rows,
            "depth_two_source_insertion_indices": list(range(8)),
            "proof_use": dict(proof_use),
            "proof_registry_counts": dict(registry_counts),
            "unique_proofs_used": len(used_proofs),
            "unique_roots": len(roots),
            "ordered_root": sha(row_hashes),
            "minimum_exact_checked_ct_witness_margin": str(minimum_witness_margin),
            "samples": restoration_samples,
        },
        "probes": {
            "one_counts": dict(one_counts),
            "one_ordered_root": one_root,
            "one_samples": one_samples,
            "two_counts": dict(two_counts),
            "two_ordered_root": two_root,
            "two_samples": two_samples,
            "total_probe_rows": sum(one_counts.values()) + sum(two_counts.values()),
            "one_equality_survivors": len(one_equalities),
            "parent_inventory_rows": len(parent_ids),
            "raw_second_probe_pairs": raw_second_pairs,
            "transport_records": len(transports),
            "transport_relations": dict(transport_counts),
            "transport_ordered_root": transport_root,
            "restriction_records": len(restrictions),
            "restriction_ordered_root": restriction_root,
            "transport_samples": transport_samples,
            "reverse_relation_counts": dict(reverse_counts),
        },
        "independence_boundary": (
            "All stored rows are streamed and checked for hashes, counts, references, frozen-forest identity, "
            "Cartesian probe coverage, and literal endpoint-map compatibility.  This census does not regenerate "
            "the restoration forest or all candidate graphs; the companion semantic-sample script reconstructs "
            "selected rows from public profiles."
        ),
    }
    assert result["probes"]["total_probe_rows"] == 574535
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (args.output_dir / "restoration_probe_census.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
