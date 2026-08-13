#!/usr/bin/env python3
"""Mutation-sensitive checks for the independently audited p/q probe gate."""

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

from audit_probe_extension_structure import exact_insert
from derived_invariants import exact_relation_pullback
from graph_model import digest, stable_json
from jc_exact import INVARIANTS, descriptor_from_graph, p_hash
from relation_universe import graph_from_object


STATES = ROOT / "primary/certificates/probe_extension_states_theta2_schema3.jsonl.gz"
BINDINGS = ROOT / "primary/certificates/probe_extension_bindings_theta2_schema3.jsonl.gz"
GRAPHS = ROOT / "primary/certificates/probe_extension_graphs_theta2_schema3.jsonl.gz"
EVIDENCE = HERE / "certificates/schema3_n4_theta2_probe_algebra_records.jsonl.gz"
ALGEBRA = HERE / "certificates/schema3_n4_theta2_probe_algebra_audit.json"
FAMILY = HERE / "certificates/family_n4_minimum.json.gz"
OUT = HERE / "certificates/schema3_n4_theta2_probe_mutation_certificate.json"


def jsonl(path):
    with gzip.open(path, "rt") as stream:
        for line in stream:
            if line.strip(): yield json.loads(line)


def load_family():
    with gzip.open(FAMILY, "rt") as stream: obj = json.load(stream)
    return tuple(
        tuple((int(c), tuple(int(i) for i in mon)) for c, mon in relation)
        for relation in obj["relations"]
    )


def quadratic_family():
    return tuple(((1, tuple(a)), (-1, tuple(b))) for a, b in INVARIANTS)


def expect_rejection(name, callback, results):
    try:
        callback()
    except Exception as exc:
        results[name] = {"rejected": True, "reason": str(exc)}
    else:
        results[name] = {"rejected": False, "reason": "mutation passed"}


def require(condition, message):
    if not condition: raise ValueError(message)


def validate_id_universe(records, expected_ids, key):
    ids = [x[key] for x in records]
    require(len(ids) == len(set(ids)), "duplicate relation")
    require(set(ids) == expected_ids, "missing or extra relation")


def validate_direction(record):
    require(record.get("direction", "source_to_target") == "source_to_target", "reversed direction")


def validate_port_transport(record):
    p = int(record["selected_port_count"])
    expected = [[f"L_{i}", f"L_{i}"] for i in range(p)]
    require(record["transport"]["port_transport"] == expected, "altered port matching")


def validate_binding(record, states, graphs, p_paths):
    state = states[record["state_id"]]
    require(state["source_graph_id"] == record["source_child_graph_id"], "source child/state mismatch")
    require(state["target_graph_id"] == record["target_child_graph_id"], "target child/state mismatch")
    if record["stage"] == "A_plus_p_plus_q":
        parent = p_paths[record["parent_probe_path_binding_id"]]
        require(parent["base_path_binding_id"] == record["base_path_binding_id"], "inconsistent path binding")
        require(parent["source_child_graph_id"] == record["source_parent_graph_id"], "wrong source parent graph ID")
        require(parent["target_child_graph_id"] == record["target_parent_graph_id"], "wrong target parent graph ID")
    for side in ("source", "target"):
        parent = graphs[record[f"{side}_parent_graph_id"]]
        child = graphs[record[f"{side}_child_graph_id"]]
        require(exact_insert(parent, record[f"{side}_insertion"]) == child, "wrong insertion child")


def validate_algebra(row, state, descriptors, families):
    require(row["state_id"] == state["state_id"], "evidence assigned to wrong relation")
    require(row["classification"] == "generic_identity_separation", "wrong algebra class")
    source = descriptors[state["source_graph_id"]]; target = descriptors[state["target_graph_id"]]
    require(row["source_descriptor_sha256"] == digest({"reticulation_count": source.reticulation_count, "switching_mask_rows": source.rows}), "wrong source descriptor")
    require(row["target_descriptor_sha256"] == digest({"reticulation_count": target.reticulation_count, "switching_mask_rows": target.rows}), "wrong target descriptor")
    family = families[row["family"]]
    relation = family[int(row["family_relation_index"])]
    quartet = tuple(row["quartet"])
    sp = exact_relation_pullback(source, quartet, relation)
    tp = exact_relation_pullback(target, quartet, relation)
    require(bool(sp) and not tp, "polynomial is invalid for this directed relation")
    require(p_hash(sp) == row["source_pullback_sha256"], "wrong source polynomial")
    require(p_hash(tp) == row["target_pullback_sha256"], "wrong target polynomial")
    require(len(sp) == row["source_pullback_term_count"] and not row["target_pullback_term_count"], "wrong polynomial term counts")


def main():
    algebra = json.loads(ALGEBRA.read_text())
    require(algebra["status"] == "VERIFIED", "algebra baseline is not verified")
    states = []
    state_by_id = {}
    chosen_iso_state = None
    for record in jsonl(STATES):
        states.append({"state_id": record["state_id"]})
        state_by_id[record["state_id"]] = {
            "state_id": record["state_id"],
            "source_graph_id": record["source_graph_id"],
            "target_graph_id": record["target_graph_id"],
            "stage": record["stage"],
            "classification": record["classification"],
            "selected_port_count": record["selected_port_count"],
        }
        if chosen_iso_state is None and record["classification"] == "labelled_isomorphism":
            chosen_iso_state = record
    expected_state_ids = set(state_by_id)

    binding_ids = []; p_paths = {}; chosen_p = None; chosen_q = None
    for record in jsonl(BINDINGS):
        binding_ids.append(record["probe_path_binding_id"])
        if record["stage"] == "A_plus_p":
            p_paths[record["probe_path_binding_id"]] = {
                "base_path_binding_id": record["base_path_binding_id"],
                "source_child_graph_id": record["source_child_graph_id"],
                "target_child_graph_id": record["target_child_graph_id"],
            }
            if chosen_p is None: chosen_p = record
        elif chosen_q is None:
            chosen_q = record
    expected_binding_ids = set(binding_ids)
    require(len(expected_binding_ids) == len(binding_ids), "baseline duplicate bindings")

    chosen_sep = [] ; evidence_count = 0
    for row in jsonl(EVIDENCE):
        evidence_count += 1
        if row["classification"] == "generic_identity_separation" and len(chosen_sep) < 2:
            chosen_sep.append(row)
    graph_ids = {
        gid for rec in (chosen_p, chosen_q)
        for gid in (rec["source_parent_graph_id"], rec["target_parent_graph_id"], rec["source_child_graph_id"], rec["target_child_graph_id"])
    }
    graph_ids |= {
        gid for row in chosen_sep
        for gid in (state_by_id[row["state_id"]]["source_graph_id"], state_by_id[row["state_id"]]["target_graph_id"])
    }
    graphs = {}
    for rec in jsonl(GRAPHS):
        if rec["graph_id"] in graph_ids: graphs[rec["graph_id"]] = graph_from_object(rec["rooted_graph"])
    descriptors = {gid: descriptor_from_graph(graph) for gid, graph in graphs.items()}
    families = {"quadratic162": quadratic_family(), "source-derived-degree3": load_family()}

    # Baseline semantic checks on the selected records.
    validate_binding(chosen_p, state_by_id, graphs, p_paths)
    validate_binding(chosen_q, state_by_id, graphs, p_paths)
    for row in chosen_sep: validate_algebra(row, state_by_id[row["state_id"]], descriptors, families)
    validate_port_transport(chosen_iso_state)

    mutations = {}
    expect_rejection("missing_state", lambda: validate_id_universe(states[:-1], expected_state_ids, "state_id"), mutations)
    expect_rejection("duplicate_state", lambda: validate_id_universe(states + [deepcopy(states[0])], expected_state_ids, "state_id"), mutations)
    binding_stub = [{"probe_path_binding_id": x} for x in binding_ids]
    expect_rejection("missing_binding", lambda: validate_id_universe(binding_stub[:-1], expected_binding_ids, "probe_path_binding_id"), mutations)
    expect_rejection("duplicate_binding", lambda: validate_id_universe(binding_stub + [deepcopy(binding_stub[0])], expected_binding_ids, "probe_path_binding_id"), mutations)

    changed = deepcopy(chosen_iso_state); changed["transport"]["port_transport"][0][1] = "L_MUTATED"
    expect_rejection("altered_port_matching", lambda: validate_port_transport(changed), mutations)
    changed = deepcopy(chosen_sep[0]); changed["direction"] = "target_to_source"
    expect_rejection("reversed_direction", lambda: validate_direction(changed), mutations)

    changed = deepcopy(chosen_q); changed["parent_probe_path_binding_id"] = next(pid for pid, item in p_paths.items() if item["base_path_binding_id"] != chosen_q["base_path_binding_id"])
    expect_rejection("inconsistent_path_binding", lambda: validate_binding(changed, state_by_id, graphs, p_paths), mutations)
    changed = deepcopy(chosen_p); changed["source_child_graph_id"] = chosen_p["source_parent_graph_id"]
    expect_rejection("altered_exact_graph_id", lambda: validate_binding(changed, state_by_id, graphs, p_paths), mutations)

    changed = deepcopy(chosen_sep[0]); changed["source_pullback_sha256"] = "0" * 64
    expect_rejection("wrong_polynomial", lambda: validate_algebra(changed, state_by_id[changed["state_id"]], descriptors, families), mutations)
    changed = deepcopy(chosen_sep[0])
    for key in ("family", "family_relation_index", "family_relation_sha256", "quartet", "source_pullback_sha256", "source_pullback_term_count", "target_pullback_sha256", "target_pullback_term_count"):
        changed[key] = deepcopy(chosen_sep[1][key])
    expect_rejection("valid_polynomial_assigned_to_wrong_relation", lambda: validate_algebra(changed, state_by_id[changed["state_id"]], descriptors, families), mutations)

    require(all(item["rejected"] for item in mutations.values()), "one or more mutations passed")
    cert = {
        "schema": 1,
        "status": "VERIFIED",
        "algebra_audit_sha256": algebra["normalized_sha256_without_hash"],
        "baseline_state_count": len(states),
        "baseline_binding_count": len(binding_ids),
        "baseline_evidence_count": evidence_count,
        "mutations": mutations,
    }
    cert["normalized_sha256_without_hash"] = digest(cert)
    OUT.write_text(stable_json(cert) + "\n")
    print(stable_json({"status": cert["status"], "mutations": len(mutations), "hash": cert["normalized_sha256_without_hash"]}))


if __name__ == "__main__":
    main()
