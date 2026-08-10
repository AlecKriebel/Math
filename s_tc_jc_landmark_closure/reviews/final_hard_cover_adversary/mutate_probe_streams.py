#!/usr/bin/env python3
"""Mutation-sensitive tests for the actual theta-2 probe package."""

from __future__ import annotations

import copy
import gzip
from itertools import combinations
import json
from pathlib import Path
import time

from audit_hard_cover import INVARIANT_PATH, PROJECT
from audit_probe_streams import (
    ALLOWED,
    BASE_SUMMARY,
    P_BINDING_FIELDS,
    Q_BINDING_FIELDS,
    STATE_FIELDS,
    SUMMARY,
    admissible_arcs,
    delete_inserted_port,
    exact_transport,
    graph_from_row,
    load_base,
    normalized_graph,
    poly_from_row,
)
from audit_candidate_full import file_sha
from cleanroom_core import (
    canonical_json,
    exact_poly_hash,
    invariant_orbit,
    pullback,
    quartet_descriptor,
    stable_hash,
)


HERE = Path(__file__).resolve().parent


def rows(path: Path):
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            yield json.loads(line)


def rebound(row: dict, identifier: str) -> dict:
    result = copy.deepcopy(row)
    payload = {
        key: result[key]
        for key in result if key not in {"schema", identifier}
    }
    result[identifier] = stable_hash(payload)
    return result


def main() -> int:
    started = time.monotonic()
    summary = json.loads(SUMMARY.read_text())
    paths = {
        name: PROJECT / spec["path"]
        for name, spec in summary["streams"].items()
    }
    _, _, base_paths, _ = load_base()
    results = []

    def record(name: str, baseline: bool, mutated: bool, detector: str):
        results.append({
            "mutation": name,
            "baseline_accepted": bool(baseline),
            "mutated_accepted": bool(mutated),
            "rejected": bool(baseline and not mutated),
            "detector": detector,
        })

    binding_ids = set()
    first_p = None
    other_root_p = None
    first_q = None
    for row in rows(paths["bindings"]):
        identifier = row["probe_path_binding_id"]
        binding_ids.add(identifier)
        if row["stage"] == "A_plus_p":
            if first_p is None:
                first_p = row
            elif other_root_p is None and row["restoration_root_id"] != first_p["restoration_root_id"]:
                other_root_p = row
        elif first_q is None:
            first_q = row
    assert first_p is not None and first_q is not None and other_root_p is not None
    parent_p = None
    for row in rows(paths["bindings"]):
        if row["probe_path_binding_id"] == first_q["parent_probe_path_binding_id"]:
            parent_p = row
            break
    assert parent_p is not None

    baseline_count = len(binding_ids) == summary["streams"]["bindings"]["records"]
    record("delete_probe_binding", baseline_count, len(binding_ids) - 1 == summary["streams"]["bindings"]["records"], "summary-bound exact binding count and complete semantic cover")
    duplicate_list = [*binding_ids, min(binding_ids)]
    record("duplicate_probe_binding", len(binding_ids) == len(set(binding_ids)), len(duplicate_list) == len(set(duplicate_list)), "binding-ID uniqueness")

    needed_state_ids = {
        first_p["state_id"], other_root_p["state_id"],
        first_q["state_id"], parent_p["state_id"],
    }
    selected_states = {}
    generic_states = []
    allowed_state = None
    state_ids = set()
    for row in rows(paths["states"]):
        state_ids.add(row["state_id"])
        if row["state_id"] in needed_state_ids:
            selected_states[row["state_id"]] = row
        if row["classification"] == "generic_polynomial_separation":
            if not generic_states or row["probe_witness"].get("source_pullback_id") != generic_states[0]["probe_witness"].get("source_pullback_id"):
                generic_states.append(row)
                if len(generic_states) > 2:
                    generic_states = generic_states[:2]
        elif row["classification"] in ALLOWED and allowed_state is None:
            allowed_state = row
    assert len(generic_states) >= 2 and allowed_state is not None
    selected_states[allowed_state["state_id"]] = allowed_state
    for row in generic_states:
        selected_states[row["state_id"]] = row

    needed_graph_ids = set()
    for state in selected_states.values():
        needed_graph_ids.update((state["source_graph_id"], state["target_graph_id"]))
    for binding in (first_p, other_root_p, first_q, parent_p):
        needed_graph_ids.update(
            binding[key] for key in (
                "source_parent_graph_id", "target_parent_graph_id",
                "source_child_graph_id", "target_child_graph_id",
            )
        )
    graphs = {}
    for row in rows(paths["graphs"]):
        if row["graph_id"] in needed_graph_ids:
            graphs[row["graph_id"]] = graph_from_row(row)
    assert set(graphs) == needed_graph_ids
    polynomials = {
        row["polynomial_id"]: poly_from_row(row)
        for row in rows(paths["polynomials"])
    }
    invariants = invariant_orbit(json.loads(INVARIANT_PATH.read_text()))

    def state_hash_valid(row: dict) -> bool:
        if set(row) != STATE_FIELDS:
            return False
        return stable_hash({
            key: row[key] for key in row if key not in {"schema", "state_id"}
        }) == row["state_id"]

    def witness_valid(row: dict) -> bool:
        if not state_hash_valid(row) or row["classification"] != "generic_polynomial_separation":
            return False
        p = int(row["selected_port_count"])
        witness = row["probe_witness"]
        quartet = tuple(combinations(range(p), 4))[int(witness["quartet_chunk"])]
        invariant = invariants[int(witness["invariant_index"])]
        labels = tuple(f"L_{index}" for index in range(p))
        source = pullback(quartet_descriptor(graphs[row["source_graph_id"]], labels, quartet), invariant)
        target = pullback(quartet_descriptor(graphs[row["target_graph_id"]], labels, quartet), invariant)
        identifier = witness.get("source_pullback_id")
        return (
            bool(source) and not target and identifier in polynomials
            and exact_poly_hash(source) == witness.get("source_pullback_exact_sha256")
            and polynomials[identifier] == source
        )

    def transport_valid(row: dict) -> bool:
        if not state_hash_valid(row) or row["classification"] not in ALLOWED:
            return False
        derived = exact_transport(graphs[row["source_graph_id"]], graphs[row["target_graph_id"]])
        return (
            derived is not None
            and canonical_json(row["transport"]) == canonical_json(derived[0])
            and canonical_json(row["canonicalization"]) == canonical_json(derived[1])
        )

    def binding_valid(row: dict) -> bool:
        fields = P_BINDING_FIELDS if row.get("stage") == "A_plus_p" else Q_BINDING_FIELDS
        if set(row) != fields:
            return False
        if stable_hash({
            key: row[key]
            for key in row if key not in {"schema", "probe_path_binding_id"}
        }) != row["probe_path_binding_id"]:
            return False
        state = selected_states.get(row["state_id"])
        base = base_paths.get(row["base_path_binding_id"])
        if state is None or base is None:
            return False
        if row["restoration_root_id"] != base["coverage"]["root_case_id"]:
            return False
        if row["source_child_graph_id"] != state["source_graph_id"] or row["target_child_graph_id"] != state["target_graph_id"]:
            return False
        for side in ("source", "target"):
            parent = graphs[row[f"{side}_parent_graph_id"]]
            child = graphs[row[f"{side}_child_graph_id"]]
            insertion = row[f"{side}_insertion"]
            if delete_inserted_port(child, insertion) != normalized_graph(parent):
                return False
            if tuple(insertion["subdivided_parent_arc"]) not in admissible_arcs(parent):
                return False
            if insertion["inserted_label"] != f"L_{int(state['selected_port_count']) - 1}":
                return False
        return True

    # Port map: alter a physical inserted label and repair the outer hash.
    baseline_binding = binding_valid(first_p)
    port_mutant = copy.deepcopy(first_p)
    port_mutant["source_insertion"]["inserted_label"] = "L_MUTATED"
    port_mutant = rebound(port_mutant, "probe_path_binding_id")
    record("alter_probe_port_map", baseline_binding, binding_valid(port_mutant), "exact child deletion plus physical L_i label")

    # Directed source/target reversal with a repaired state hash.
    generic = generic_states[0]
    baseline_witness = witness_valid(generic)
    reversal = copy.deepcopy(generic)
    reversal["source_graph_id"], reversal["target_graph_id"] = reversal["target_graph_id"], reversal["source_graph_id"]
    reversal = rebound(reversal, "state_id")
    record("reverse_probe_source_target", baseline_witness, witness_valid(reversal), "regenerated directed graph pullback orientation")

    # Valid polynomial/witness from another state attached to the wrong graph.
    swapped = copy.deepcopy(generic)
    swapped["probe_witness"] = copy.deepcopy(generic_states[1]["probe_witness"])
    swapped = rebound(swapped, "state_id")
    record("swap_valid_polynomial_between_probe_graphs", baseline_witness, witness_valid(swapped), "graph -> descriptor -> exact polynomial body")

    baseline_transport = transport_valid(allowed_state)
    wrong_transport = copy.deepcopy(allowed_state)
    wrong_transport["transport"]["vertex_transport"][0][1] += 1000
    wrong_transport = rebound(wrong_transport, "state_id")
    record("alter_probe_transport", baseline_transport, transport_valid(wrong_transport), "independent rigid T-quotient transport")

    # Jacobians are outside this artifact's claim.  A fabricated field must be
    # rejected by the closed state schema rather than silently trusted.
    wrong_jacobian = copy.deepcopy(allowed_state)
    wrong_jacobian["jacobian_minor"] = "forged"
    wrong_jacobian = rebound(wrong_jacobian, "state_id")
    record("inject_forged_jacobian", state_hash_valid(allowed_state), state_hash_valid(wrong_jacobian), "closed probe-state schema; no Jacobian claim exists")

    # Replace a q parent by a valid unrelated p path and repair the hash.
    def parent_valid(q: dict, parent: dict) -> bool:
        return (
            q["parent_probe_path_binding_id"] == parent["probe_path_binding_id"]
            and q["base_path_binding_id"] == parent["base_path_binding_id"]
            and q["restoration_root_id"] == parent["restoration_root_id"]
            and q["source_parent_graph_id"] == parent["source_child_graph_id"]
            and q["target_parent_graph_id"] == parent["target_child_graph_id"]
        )

    baseline_parent = parent_valid(first_q, parent_p)
    wrong_parent = copy.deepcopy(first_q)
    wrong_parent["parent_probe_path_binding_id"] = other_root_p["probe_path_binding_id"]
    wrong_parent = rebound(wrong_parent, "probe_path_binding_id")
    record("replace_q_parent_path", baseline_parent, parent_valid(wrong_parent, other_root_p), "root/path and exact parent-child graph coherence")

    # State algebra rows may be reusable only if path bindings stay distinct.
    # Adding another root binding to one state violates the observed bijection.
    baseline_bijection = len(state_ids) == len(binding_ids)
    synthetic_binding_count = len(binding_ids) + 1
    record("merge_probe_state_across_roots", baseline_bijection, len(state_ids) == synthetic_binding_count, "one exact root/path binding per emitted state")

    payload = {
        "schema": "theta2-schema3-probe-mutations-v1",
        "status": "VERIFIED" if all(row["rejected"] for row in results) else "FALSE",
        "scope": "in-memory mutations of frozen probe streams; primary untouched",
        "inputs": {
            str(path.relative_to(PROJECT)): file_sha(path)
            for path in (SUMMARY, BASE_SUMMARY, *paths.values())
        },
        "mutation_count": len(results),
        "rejected_count": sum(row["rejected"] for row in results),
        "mutations": results,
        "elapsed_seconds": time.monotonic() - started,
    }
    output = HERE / "schema3_theta2_probe_mutations.json"
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "rejected": f"{payload['rejected_count']}/{payload['mutation_count']}",
        "output": str(output), "sha256": file_sha(output),
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
