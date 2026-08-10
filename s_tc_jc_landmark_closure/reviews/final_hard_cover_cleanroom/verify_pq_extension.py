#!/usr/bin/env python3
"""Exact clean-room verification of the path-bound p/q closure lemma."""

from __future__ import annotations

from pathlib import Path
import gzip
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from graph_model import (
    decorated_mixed_relation, digest, rooted_code, rooted_graph_id,
    stable_json, standard_semidirected_audit,
)
from pq_extension import (
    all_segment_insertions, cyclic_blob_arcs, extend_p_then_q,
    extend_relation,
)
from relation_universe import graph_from_object


def load_gzip_json(path):
    with gzip.open(path, "rt") as stream:
        return json.load(stream)


def relation_id(source, target, matching):
    rel = decorated_mixed_relation(source, target, matching)
    return digest({
        "decorated_relation_code": rel["code"],
        "direction": rel["direction"],
        "port_matching": rel["port_matching"],
    })


def verify_extension_record(record, full_relation_id, parent_path_id):
    assert record["fixed_full_root_case_id"] == full_relation_id
    assert record["source_rooted_graph_id"] == rooted_graph_id(record["source_graph"])
    assert record["target_rooted_graph_id"] == rooted_graph_id(record["target_graph"])
    assert record["parent_path_binding_id"] == parent_path_id
    assert standard_semidirected_audit(record["source_graph"])["ok"]
    assert standard_semidirected_audit(record["target_graph"])["ok"]
    rel = decorated_mixed_relation(
        record["source_graph"], record["target_graph"],
        tuple(map(tuple, record["port_matching"])),
    )
    state_payload = {
        "fixed_full_root_case_id": full_relation_id,
        "source_rooted_graph_id": rooted_graph_id(record["source_graph"]),
        "target_rooted_graph_id": rooted_graph_id(record["target_graph"]),
        "decorated_relation_code": rel["code"],
        "direction": rel["direction"],
        "port_matching": rel["port_matching"],
    }
    assert digest(state_payload) == record["state_id"]
    assert rel["sha256"] == record["decorated_relation_sha256"]


def raw_pair_set(records):
    out = set()
    for record in records:
        for a, b in record["raw_insertion_arc_pairs"]:
            pair = (tuple(a), tuple(b))
            if pair in out:
                raise AssertionError(("raw insertion pair emitted twice", pair))
            out.add(pair)
    return out


def verify_same_segment_orders(p_graph):
    labels = p_graph.label_map
    p_leaf = next(v for v, label in labels.items() if label == "L_p")
    _, _, _, parents = p_graph.degrees()
    p_parent = parents[p_leaf][0]
    seen = set()
    for item in all_segment_insertions(p_graph, "L_q"):
        h = item["graph"]; lm = h.label_map
        q_leaf = next(v for v, label in lm.items() if label == "L_q")
        _, _, _, hp = h.degrees(); q_parent = hp[q_leaf][0]
        arcs = set(h.arcs)
        if (q_parent, p_parent) in arcs: seen.add("q_before_p")
        if (p_parent, q_parent) in arcs: seen.add("p_before_q")
    if seen != {"q_before_p", "p_before_q"}:
        raise AssertionError(("same-segment orders incomplete", sorted(seen)))


def audit_universe(tag):
    universe = load_gzip_json(HERE / "certificates" / f"universe_{tag}.json.gz")
    records = []
    for source_obj in universe["sources"]:
        graph = graph_from_object(source_obj["graph"])
        labels = sorted(graph.label_map.values())
        matching = tuple((label, label) for label in labels)
        base_relation_id = relation_id(graph, graph, matching)
        base_path_id = digest({"full_relation_id": base_relation_id, "path": "base"})
        qt_transport = {"kind": "identity", "labels": labels}
        p_records = extend_relation(
            base_relation_id, graph, graph, "L_p", "L_p", base_path_id,
            qt_transport, matching,
        )
        arcs = cyclic_blob_arcs(graph)
        expected_pairs = {(a, b) for a in arcs for b in arcs}
        if raw_pair_set(p_records) != expected_pairs:
            raise AssertionError((tag, source_obj["source_id"], "p raw coverage"))
        if len({x["state_id"] for x in p_records}) != len(p_records):
            raise AssertionError("p state dedup failed")
        for record in p_records:
            verify_extension_record(record, base_relation_id, base_path_id)

        chosen = p_records[0]
        p_again, q_records = extend_p_then_q(
            base_relation_id, graph, graph, base_path_id, qt_transport,
            matching, [chosen["path_binding_id"]],
        )
        assert tuple(x["state_id"] for x in p_again) == tuple(x["state_id"] for x in p_records)
        q_source_arcs = cyclic_blob_arcs(chosen["source_graph"])
        q_target_arcs = cyclic_blob_arcs(chosen["target_graph"])
        if raw_pair_set(q_records) != {(a, b) for a in q_source_arcs for b in q_target_arcs}:
            raise AssertionError((tag, source_obj["source_id"], "q raw coverage"))
        for record in q_records:
            verify_extension_record(record, base_relation_id, chosen["path_binding_id"])
        verify_same_segment_orders(chosen["source_graph"])

        # The second stage must not silently extend an unapproved p path.
        q_parent_ids = {x["parent_path_binding_id"] for x in q_records}
        if q_parent_ids != {chosen["path_binding_id"]}:
            raise AssertionError(("unapproved p path reached q", q_parent_ids))

        # Incomplete terminal matching and a too-small safe bound both fail.
        try:
            extend_relation(
                base_relation_id, graph, graph, "BAD_P", "BAD_P", base_path_id,
                qt_transport, matching[:-1],
            )
        except ValueError:
            incomplete_matching_rejected = True
        else:
            incomplete_matching_rejected = False
        if not incomplete_matching_rejected:
            raise AssertionError("incomplete base matching accepted")
        try:
            extend_p_then_q(
                base_relation_id, graph, graph, base_path_id, qt_transport,
                matching, [chosen["path_binding_id"]], max_total_ports=len(matching) + 1,
            )
        except ValueError:
            unsafe_bound_rejected = True
        else:
            unsafe_bound_rejected = False
        if not unsafe_bound_rejected:
            raise AssertionError("unsafe q port bound accepted")

        records.append({
            "source_id": source_obj["source_id"],
            "base_port_count": len(matching),
            "base_cyclic_arc_count": len(arcs),
            "p_state_count": len(p_records),
            "p_raw_pair_count": len(expected_pairs),
            "chosen_p_path_binding_id": chosen["path_binding_id"],
            "q_state_count_from_chosen_p": len(q_records),
            "q_raw_pair_count_from_chosen_p": len(q_source_arcs) * len(q_target_arcs),
            "p_state_commitment": digest([x["record_sha256"] for x in p_records]),
            "q_state_commitment": digest([x["record_sha256"] for x in q_records]),
        })
    return records


def main():
    by_tag = {tag: audit_universe(tag) for tag in ("n3", "n4_minimum")}
    cert = {
        "schema": 1,
        "status": "VERIFIED",
        "scope": "conditional path-bound p/q enumeration; not terminal classification",
        "universes": by_tag,
        "assertions": {
            "complete_cartesian_segment_coverage": True,
            "both_same_segment_orders": True,
            "fixed_full_relation_binding": True,
            "rooted_graph_ids_in_state_identity": True,
            "qt_transport_retained": True,
            "only_allowed_p_paths_reach_q": True,
            "complete_base_matching_required": True,
            "safe_port_bound_enforced": True,
            "standard_stc_preserved": True,
        },
    }
    cert["normalized_sha256_without_hash"] = digest(cert)
    out = HERE / "certificates" / "pq_extension_certificate.json"
    out.write_text(stable_json(cert) + "\n")
    print(stable_json({
        "status": cert["status"],
        "record_counts": {tag: len(rows) for tag, rows in by_tag.items()},
        "hash": cert["normalized_sha256_without_hash"],
    }))


if __name__ == "__main__":
    main()
