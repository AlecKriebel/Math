#!/usr/bin/env python3
"""Mutation tests bound to the independently verified schema-3 n=4 stream."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import gzip
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from jc_exact import canonical_descriptor_key, descriptor_from_graph
from relation_universe import graph_from_object


def stable(obj): return json.dumps(obj, sort_keys=True, separators=(",", ":"))
def digest(obj): return hashlib.sha256(stable(obj).encode()).hexdigest()


def load_jsonl(path):
    with gzip.open(path, "rt") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def record_hashes(records, key): return {record[key]: digest(record) for record in records}


def validate_states(records, expected_ids, expected_hashes):
    ids = [record["state_id"] for record in records]
    if len(ids) != len(set(ids)): raise ValueError("duplicate relation")
    if set(ids) != expected_ids: raise ValueError("missing or extra relation")
    by_id = {record["state_id"]: record for record in records}
    for sid, record in by_id.items():
        if record.get("direction", "source_to_target") != "source_to_target":
            raise ValueError("reversed direction")
        fixed = record.get("fixed_full_root_case_id")
        if not fixed: raise ValueError("missing fixed full root case")
        declared = set(record["children"])
        for coverage in record["raw_coverage"]:
            if coverage["root_case_id"] != fixed:
                raise ValueError("merge across fixed full root cases")
            if coverage["source_graph_id"] != record["source_graph_id"]:
                raise ValueError("merge across source rooted graph IDs")
            if coverage["target_graph_id"] != record["target_graph_id"]:
                raise ValueError("merge across target rooted graph IDs")
            if set(coverage["child_state_ids"]) != declared:
                raise ValueError("inconsistent per-path child set")
        if digest(record) != expected_hashes[sid]:
            raise ValueError("normalized relation commitment changed")


def validate_terminals(records, expected_ids, expected_hashes):
    ids = [record["state_id"] for record in records]
    if len(ids) != len(set(ids)): raise ValueError("duplicate terminal evidence")
    if set(ids) != expected_ids: raise ValueError("missing or extra terminal evidence")
    for record in records:
        sid = record["state_id"]
        if record["classification"] == "generic_identity_separation":
            if not record["source_pullback_term_count"] or record["target_pullback_term_count"]:
                raise ValueError("invalid identity-separator term counts")
            if not record.get("independent_witness_uses_primary_quartet"):
                raise ValueError("separator moved away from the bound primary quartet")
            if not record.get("primary_polynomial_id"):
                raise ValueError("missing primary polynomial binding")
        if digest(record) != expected_hashes[sid]:
            raise ValueError("wrong independently regenerated polynomial or topology record")


def validate_split_complement_normalization(graph_records, mode):
    groups = {}
    for record in graph_records:
        graph = graph_from_object(record["rooted_graph"])
        key = canonical_descriptor_key(descriptor_from_graph(graph, mode))
        groups.setdefault(record["standard_mixed_code_sha256"], set()).add(key)
    failures = [group for group, keys in groups.items() if len(keys) != 1]
    if failures:
        raise ValueError(
            f"split-complement normalization is not root invariant: {len(failures)} groups"
        )


def expect_rejection(name, callback, mutations):
    try:
        callback()
    except Exception as exc:
        mutations[name] = {"rejected": True, "reason": str(exc)}
    else:
        mutations[name] = {"rejected": False, "reason": "mutation passed"}


def main():
    relations_path = ROOT / "primary/certificates/hard_cover_n4_schema3_theta2_full.jsonl.gz"
    graphs_path = ROOT / "primary/certificates/hard_cover_graphs_n4_schema3_theta2_full.jsonl.gz"
    terminal_path = HERE / "certificates/schema3_n4_theta2_terminal_records.jsonl.gz"
    audit_path = HERE / "certificates/schema3_n4_theta2_full_audit.json"
    audit = json.loads(audit_path.read_text())
    if audit["status"] != "VERIFIED": raise ValueError("full independent audit is not verified")
    states = load_jsonl(relations_path); terminals = load_jsonl(terminal_path)
    graph_records = load_jsonl(graphs_path)
    expected_state_hashes = record_hashes(states, "state_id")
    expected_terminal_hashes = record_hashes(terminals, "state_id")
    expected_state_ids = set(expected_state_hashes); expected_terminal_ids = set(expected_terminal_hashes)
    validate_states(states, expected_state_ids, expected_state_hashes)
    validate_terminals(terminals, expected_terminal_ids, expected_terminal_hashes)
    validate_split_complement_normalization(graph_records, "minimum")

    mutations = {}
    expect_rejection("missing_relation", lambda: validate_states(states[:-1], expected_state_ids, expected_state_hashes), mutations)
    expect_rejection("duplicate_relation", lambda: validate_states(states + [deepcopy(states[0])], expected_state_ids, expected_state_hashes), mutations)

    changed = deepcopy(states); changed[0]["port_matching"][0][1] = "L_MUTATED"
    expect_rejection("altered_port_matching", lambda: validate_states(changed, expected_state_ids, expected_state_hashes), mutations)
    changed = deepcopy(states); changed[0]["direction"] = "target_to_source"
    expect_rejection("reversed_direction", lambda: validate_states(changed, expected_state_ids, expected_state_hashes), mutations)

    refined_index = next(i for i, record in enumerate(states) if record["terminal_classification"] == "refined_by_next_restoration")
    changed = deepcopy(states); changed[refined_index]["raw_coverage"][0]["child_state_ids"] = []
    expect_rejection("inconsistent_path_binding", lambda: validate_states(changed, expected_state_ids, expected_state_hashes), mutations)
    changed = deepcopy(states); changed[0]["raw_coverage"][0]["root_case_id"] = "MUTATED_ROOT"
    expect_rejection("cross_root_case_merge", lambda: validate_states(changed, expected_state_ids, expected_state_hashes), mutations)
    changed = deepcopy(states); changed[0]["raw_coverage"][0]["source_graph_id"] = "MUTATED_SOURCE_GRAPH"
    expect_rejection("cross_source_rooted_graph_merge", lambda: validate_states(changed, expected_state_ids, expected_state_hashes), mutations)
    changed = deepcopy(states); changed[0]["raw_coverage"][0]["target_graph_id"] = "MUTATED_TARGET_GRAPH"
    expect_rejection("cross_target_rooted_graph_merge", lambda: validate_states(changed, expected_state_ids, expected_state_hashes), mutations)
    changed = deepcopy(states); changed[0]["source_graph_id"] = "MUTATED_EXACT_GRAPH"
    expect_rejection("altered_exact_graph_id", lambda: validate_states(changed, expected_state_ids, expected_state_hashes), mutations)

    polynomial_index = next(i for i, record in enumerate(terminals) if record["classification"] == "generic_identity_separation")
    changed_terminals = deepcopy(terminals)
    changed_terminals[polynomial_index]["source_pullback_sha256"] = "0" * 64
    expect_rejection(
        "wrong_polynomial",
        lambda: validate_terminals(changed_terminals, expected_terminal_ids, expected_terminal_hashes),
        mutations,
    )
    other_polynomial_index = next(
        i for i, record in enumerate(terminals)
        if record["classification"] == "generic_identity_separation"
        and record["source_pullback_sha256"]
        != terminals[polynomial_index]["source_pullback_sha256"]
    )
    changed_terminals = deepcopy(terminals)
    changed_terminals[polynomial_index]["source_pullback_sha256"] = (
        terminals[other_polynomial_index]["source_pullback_sha256"]
    )
    changed_terminals[polynomial_index]["independent_relation_sha256"] = (
        terminals[other_polynomial_index]["independent_relation_sha256"]
    )
    expect_rejection(
        "valid_polynomial_assigned_to_wrong_relation",
        lambda: validate_terminals(
            changed_terminals, expected_terminal_ids, expected_terminal_hashes,
        ),
        mutations,
    )
    expect_rejection(
        "removed_split_complement_normalization",
        lambda: validate_split_complement_normalization(graph_records, "none"),
        mutations,
    )
    expect_rejection(
        "wrong_split_complement_normalization",
        lambda: validate_split_complement_normalization(
            graph_records, "wrong_four_port_universe",
        ),
        mutations,
    )
    if not all(result["rejected"] for result in mutations.values()):
        raise AssertionError(mutations)
    cert = {
        "schema": 1,
        "status": "VERIFIED",
        "full_audit_sha256": audit["normalized_sha256_without_hash"],
        "baseline_state_count": len(states),
        "baseline_terminal_count": len(terminals),
        "baseline_graph_count": len(graph_records),
        "split_complement_normalization": "minimum",
        "baseline_state_commitment": digest(sorted(expected_state_hashes.items())),
        "baseline_terminal_commitment": digest(sorted(expected_terminal_hashes.items())),
        "mutations": mutations,
    }
    cert["normalized_sha256_without_hash"] = digest(cert)
    out = HERE / "certificates/schema3_n4_theta2_mutation_certificate.json"
    out.write_text(stable(cert) + "\n")
    print(stable({
        "status": cert["status"], "mutation_count": len(mutations),
        "hash": cert["normalized_sha256_without_hash"],
    }))


if __name__ == "__main__":
    main()
