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
from collections import Counter
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
    restoration_ledger_path = restoration_dir / "restoration_ledger.jsonl.gz"
    assert sha_file(restoration_ledger_path) == restoration_manifest["ledger"]["sha256"]
    with gzip.open(restoration_dir / "restoration_proof_registry.json.gz", "rt", encoding="utf-8") as handle:
        registry = json.load(handle)
    logical_registry = dict(registry)
    claimed_registry_hash = logical_registry.pop("payload_sha256")
    assert claimed_registry_hash == sha(logical_registry)
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

    layer_counts, proof_use, roots, used_proofs = Counter(), Counter(), set(), set()
    row_hashes, first_layer_hashes, second_parent_counts, restoration_samples = [], set(), Counter(), []
    restoration_rows = 0
    for index, row in enumerate(iter_gzip_jsonl(restoration_ledger_path)):
        public = dict(row)
        claimed = public.pop("row_sha256")
        assert claimed == sha(public)
        assert row["edge_index"] == index
        row_hashes.append(claimed)
        layer_counts[row["layer"]] += 1
        proof_use[row["proof_kind"]] += 1
        roots.add(row["root_id"])
        used_proofs.add(row["proof_id"])
        assert row["proof_id"] in proof_ids
        assert proof_kinds_by_id[row["proof_id"]] == row["proof_kind"]
        if row["layer"] == 1:
            first_layer_hashes.add(claimed)
        if row["layer"] == 2:
            second_parent_counts[row["parent_first_row_sha256"]] += 1
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
    assert len(second_parent_counts) == 32 and set(second_parent_counts.values()) == {8}
    assert set(second_parent_counts) <= first_layer_hashes
    assert used_proofs == proof_ids

    coherence = json.loads((probe_dir / "K3P_PROBE_COHERENCE_CERTIFICATE.json").read_text(encoding="utf-8"))
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

    with gzip.open(probe_dir / "separation_proof_registry.json.gz", "rt", encoding="utf-8") as handle:
        separation = json.load(handle)
    topological = separation["separation_proof_registry"]
    tree_sunlet = separation["k3p_tree_sunlet_registry"]["certificates"]
    assert all(proof_id == "Q:" + sha(certificate) for proof_id, certificate in topological.items())
    assert all(proof_id == "K3P-TS:" + sha(certificate) for proof_id, certificate in tree_sunlet.items())

    one_counts, one_origin, one_samples = Counter(), Counter(), {}
    one_root = sha([])
    one_equalities = []
    one_path = probe_dir / "one_port_ledger.jsonl.gz"
    assert sha_file(one_path) == coherence["one_port"]["ledger_sha256"]
    for index, row in enumerate(iter_gzip_jsonl(one_path)):
        one_root = ordered_add(one_root, row)
        status = row["status"]
        assert status in {"isomorphic", "triangle", "displayed_quartet_mismatch", "k3p_tree_sunlet_sos"}
        one_counts[status] += 1
        one_origin[(row["origin"], status)] += 1
        assert row["source_parent_restriction_id"] in restrictions
        assert row["target_parent_restriction_id"] in restrictions
        if status in ("isomorphic", "triangle"):
            assert transports[row["transport_id"]] == status
            one_equalities.append(f"P1:{row['parent_anchor_id']}:{row['source_site_index']}:{row['target_site_index']}")
        else:
            assert row["proof_id"] in (topological if status == "displayed_quartet_mismatch" else tree_sunlet)
        one_samples.setdefault(status, {"row": index, "digest": sha(row), "parent": row["parent_anchor_id"]})
    assert one_root == coherence["one_port"]["ordered_ledger"]["ordered_hash_root"]
    assert dict(one_counts) == coherence["one_port"]["counts"]
    assert len(one_equalities) == 2107

    parent_root = sha([])
    parent_ids = []
    raw_second_pairs = 0
    parent_path = probe_dir / "two_port_parent_inventory.jsonl.gz"
    assert sha_file(parent_path) == coherence["two_port"]["parent_inventory_sha256"]
    for index, row in enumerate(iter_gzip_jsonl(parent_path)):
        parent_root = ordered_add(parent_root, row)
        parent_id = row["one_port_parent_id"]
        parent_ids.append(parent_id)
        assert parent_id == one_equalities[index]
        for side in ("source_candidate_profile", "target_candidate_profile"):
            profile = row[side]
            assert profile["site_count"] == 2*profile["port_count"] + 3*profile["reticulation_count"] - 3
            assert profile["site_count"] == len(profile["sites"])
            assert profile["ordered_site_hash_root"] == sha([sha(site) for site in profile["sites"]])
        pairs = row["source_candidate_profile"]["site_count"] * row["target_candidate_profile"]["site_count"]
        assert pairs == row["raw_second_probe_pairs"]
        raw_second_pairs += pairs
    parent_manifest = coherence["two_port"]["ordered_parent_inventory"]
    assert parent_root == parent_manifest["ordered_hash_root"]
    assert len(parent_ids) == parent_manifest["rows"] == 2107
    assert len(set(parent_ids)) == len(parent_ids)
    assert raw_second_pairs == 544571

    two_counts, reverse_counts, two_samples = Counter(), Counter(), {}
    two_root = sha([])
    two_path = probe_dir / "two_port_ledger.jsonl.gz"
    assert sha_file(two_path) == coherence["two_port"]["ledger_sha256"]
    for index, row in enumerate(iter_gzip_jsonl(two_path)):
        two_root = ordered_add(two_root, row)
        status = row["status"]
        assert status in {"isomorphic", "triangle", "displayed_quartet_mismatch", "k3p_tree_sunlet_sos"}
        two_counts[status] += 1
        assert row["source_parent_restriction_id"] in restrictions
        assert row["target_parent_restriction_id"] in restrictions
        if status in ("isomorphic", "triangle"):
            assert transports[row["transport_id"]] == status
            reverse = row["reverse_order_certificate"]
            assert reverse["reverse_parent_transport_id"] in transports
            assert transports[reverse["reverse_parent_transport_id"]] == reverse["reverse_parent_relation"]
            assert reverse["same_base_anchor_id"] == row["base_anchor_id"]
            reverse_counts[reverse["reverse_parent_relation"]] += 1
        else:
            assert row["proof_id"] in (topological if status == "displayed_quartet_mismatch" else tree_sunlet)
        two_samples.setdefault(status, {"row": index, "digest": sha(row), "parent": row["one_port_parent_id"]})
    assert two_root == coherence["two_port"]["ordered_ledger"]["ordered_hash_root"]
    assert dict(two_counts) == coherence["two_port"]["counts"]
    assert sum(two_counts.values()) == 544571

    result = {
        "restoration": {
            "rows": restoration_rows,
            "layers": dict(layer_counts),
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
            "All stored rows are streamed and checked for hashes, counts, references, and literal endpoint-map "
            "compatibility.  This census does not regenerate the restoration forest or all candidate graphs; "
            "the companion semantic-sample script reconstructs selected rows from public profiles."
        ),
    }
    assert result["probes"]["total_probe_rows"] == 574535
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (args.output_dir / "restoration_probe_census.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
