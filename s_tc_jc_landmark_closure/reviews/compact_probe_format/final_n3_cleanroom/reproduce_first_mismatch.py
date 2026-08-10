#!/usr/bin/env python3
"""Minimal standalone reproduction of the first sequential n=3 mismatch.

This checker fixes one path/cell and independently reconstructs the inserted
graphs and both selected strict witnesses.  It imports no primary module.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
N4 = HERE.parent / "final_n4_cleanroom"
sys.path[:0] = [str(HERE), str(N4)]

import audit_final_n3 as audit  # noqa: E402
import audit_final_n4 as common  # noqa: E402
from engine import (  # noqa: E402
    admissible_internal_arcs,
    exact_poly_hash,
    file_sha256,
    insert_port,
    load_invariants,
    polynomial_record,
    pullback,
    quartet_descriptor,
    require,
    stable_hash,
)
from engine_n3 import prove_strict_open_cube_sign  # noqa: E402


PROJECT = HERE.parents[2]
CERT = PROJECT / "primary/certificates"
COMPACT_SUMMARY = CERT / "compact_probe_schema3_n3_compact_s1_summary.json"
VERBOSE_SUMMARY = CERT / "probe_extension_schema3_n3_final_summary.json"
PATH_INDEX = 59
P_FLAT = 45
Q_LOCAL = 47


def witness_replay(name, witness, source, target, port_count, invariants,
                   library):
    chunk = int(witness["quartet_chunk"])
    invariant_index = int(witness["invariant_index"])
    source_descriptor = quartet_descriptor(source, port_count, chunk)
    target_descriptor = quartet_descriptor(target, port_count, chunk)
    source_poly = pullback(source_descriptor, invariants[invariant_index])
    target_poly = pullback(target_descriptor, invariants[invariant_index])
    require(not source_poly and bool(target_poly),
            "not_a_strict_separator", witness=name)
    exact_sha = exact_poly_hash(target_poly)
    identifier, body = polynomial_record(target_poly)
    require(exact_sha == witness["target_pullback_exact_sha256"],
            "exact_polynomial_hash", witness=name)
    require(identifier == witness["target_pullback_id"],
            "polynomial_content_id", witness=name)
    require(identifier in library, "polynomial_not_in_library", witness=name)
    require({key: library[identifier][key] for key in body} ==
            json.loads(json.dumps(body)), "polynomial_body", witness=name)
    sign = prove_strict_open_cube_sign(target_poly)
    require(sign["strict_open_sign"] == int(witness["target_strict_sign"]),
            "strict_sign", witness=name)
    return {
        "name": name,
        "quartet_chunk": chunk,
        "invariant_index": invariant_index,
        "source_pullback_zero": True,
        "target_pullback_zero": False,
        "target_pullback_exact_sha256": exact_sha,
        "target_pullback_id": identifier,
        "descriptor_pair_sha256": stable_hash(
            [source_descriptor, target_descriptor]),
        "independent_sign_proof": sign,
        "stored_witness": witness,
    }


def main():
    compact = common.load_compact(
        COMPACT_SUMMARY, audit.EXPECTED_COMPACT["s1"])
    inventory, commitment, inputs = common.build_inventory([
        common.resolve(path, COMPACT_SUMMARY)
        for path in compact["summary"]["base_summaries"]
    ])
    require(common.inventory_commitment(commitment) ==
            compact["summary"]["path_inventory_sha256"],
            "inventory_commitment")
    require(inputs == compact["summary"]["input_sha256"],
            "inventory_inputs")
    verbose = audit.load_verbose(VERBOSE_SUMMARY)
    invariants = load_invariants(
        PROJECT.parent /
        "strong_level2_phylo_identifiability/src/jc_root_spanning_atlas_data.py",
        PROJECT / "primary/seventh_invariant.json")

    row = next(item for item in compact["paths"]
               if int(item["path_index"]) == PATH_INDEX)
    entry = inventory[PATH_INDEX]
    p_keys = tuple((tuple(source), tuple(target))
                   for source in row["source_p_arcs"]
                   for target in row["target_p_arcs"])
    source_p_arc, target_p_arc = p_keys[P_FLAT]
    p0 = int(row["selected_port_count"])
    source_p, source_p_meta = insert_port(
        entry["source"], source_p_arc, f"L_{p0}")
    target_p, target_p_meta = insert_port(
        entry["target"], target_p_arc, f"L_{p0}")
    q_keys = tuple((source, target)
                   for source in admissible_internal_arcs(source_p)
                   for target in admissible_internal_arcs(target_p))
    source_q_arc, target_q_arc = q_keys[Q_LOCAL]
    source_q, source_q_meta = insert_port(
        source_p, source_q_arc, f"L_{p0 + 1}")
    target_q, target_q_meta = insert_port(
        target_p, target_q_arc, f"L_{p0 + 1}")

    block = row["allowed_p_flat_indices"].index(P_FLAT)
    q_cursor = sum(int(a) * int(b) for a, b in row["q_shapes"][:block]) + Q_LOCAL
    word = common.decode_words(
        row["q_words_base64_le_u32"], int(row["q_word_count"]))[q_cursor]
    require(word >> 29 == 1, "not_strict_word")
    witness_index = word & audit.INDEX_MASK
    compact_record = compact["witnesses"][witness_index]

    path_bindings = verbose["bindings_by_base"][row["base_path_binding_id"]]
    p_binding = next(binding for binding in path_bindings
                     if binding["stage"] == "A_plus_p"
                     and tuple(binding["source_insertion"]
                               ["subdivided_parent_arc"]) == source_p_arc
                     and tuple(binding["target_insertion"]
                               ["subdivided_parent_arc"]) == target_p_arc)
    q_binding = next(binding for binding in path_bindings
                     if binding["stage"] == "A_plus_p_plus_q"
                     and binding["parent_probe_path_binding_id"] ==
                     p_binding["probe_path_binding_id"]
                     and tuple(binding["source_insertion"]
                               ["subdivided_parent_arc"]) == source_q_arc
                     and tuple(binding["target_insertion"]
                               ["subdivided_parent_arc"]) == target_q_arc)
    state = verbose["states"][q_binding["state_id"]]
    require(source_q.graph_id == q_binding["source_child_graph_id"] and
            target_q.graph_id == q_binding["target_child_graph_id"],
            "graph_direction")
    require(source_p_meta == p_binding["source_insertion"] and
            target_p_meta == p_binding["target_insertion"] and
            source_q_meta == q_binding["source_insertion"] and
            target_q_meta == q_binding["target_insertion"],
            "insertion_body")
    require(compact_record["classification"] ==
            state["classification"] == "strict_open_cube_separation",
            "classification")

    compact_result = witness_replay(
        "compact", compact_record["probe_witness"], source_q, target_q,
        p0 + 2, invariants, compact["polynomials"])
    verbose_result = witness_replay(
        "verbose", state["probe_witness"], source_q, target_q,
        p0 + 2, invariants, verbose["polynomials"])
    exact_body_equal = (compact_record["probe_witness"] ==
                        state["probe_witness"])
    require(not exact_body_equal, "expected_mismatch_disappeared")

    payload = {
        "schema": "compact-probe-n3-first-mismatch-reproduction-v1",
        "status": "LOCALIZED",
        "compact_summary": common.normalized(COMPACT_SUMMARY),
        "compact_summary_sha256": file_sha256(COMPACT_SUMMARY),
        "verbose_summary": common.normalized(VERBOSE_SUMMARY),
        "verbose_summary_sha256": file_sha256(VERBOSE_SUMMARY),
        "relation": {
            "path_index": PATH_INDEX,
            "stage": "A_plus_p_plus_q",
            "p_flat_index": P_FLAT,
            "q_local_index": Q_LOCAL,
            "q_global_index": q_cursor,
            "packed_word": word,
            "witness_index": witness_index,
            "base_path_binding_id": row["base_path_binding_id"],
            "p_binding_id": p_binding["probe_path_binding_id"],
            "verbose_binding_id": q_binding["probe_path_binding_id"],
            "verbose_state_id": state["state_id"],
            "source_parent_graph_id": source_p.graph_id,
            "target_parent_graph_id": target_p.graph_id,
            "source_child_graph_id": source_q.graph_id,
            "target_child_graph_id": target_q.graph_id,
            "source_p_arc": source_p_arc,
            "target_p_arc": target_p_arc,
            "source_q_arc": source_q_arc,
            "target_q_arc": target_q_arc,
            "classification": state["classification"],
        },
        "exact_selected_witness_bodies_equal": exact_body_equal,
        "compact_witness_replay": compact_result,
        "verbose_witness_replay": verbose_result,
        "diagnosis": {
            "cleanroom_graph_decoder_defect": False,
            "compact_primary_mathematical_witness_defect": False,
            "verbose_package_mathematical_witness_defect": False,
            "exact_body_comparator_too_strict_for_semantic_equivalence": True,
            "explanation": (
                "The same exact directed graph relation and classification "
                "has two distinct independently valid strict separators. "
                "The compact and verbose packages are semantically equal at "
                "this relation but are not lossless copies of the selected "
                "witness body."),
        },
        "implementation": common.normalized(Path(__file__)),
        "implementation_sha256": file_sha256(Path(__file__)),
        "dependencies": {
            common.normalized(HERE / "audit_final_n3.py"):
                file_sha256(HERE / "audit_final_n3.py"),
            common.normalized(HERE / "engine_n3.py"):
                file_sha256(HERE / "engine_n3.py"),
            common.normalized(N4 / "audit_final_n4.py"):
                file_sha256(N4 / "audit_final_n4.py"),
            common.normalized(N4 / "engine.py"):
                file_sha256(N4 / "engine.py"),
        },
    }
    output = (HERE / "history/sequential_first_failure/"
              "FIRST_MISMATCH_CERTIFICATE.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "exact_selected_witness_bodies_equal": exact_body_equal,
        "compact_target_sha": compact_result["target_pullback_exact_sha256"],
        "verbose_target_sha": verbose_result["target_pullback_exact_sha256"],
        "output": common.normalized(output),
        "output_sha256": file_sha256(output),
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FALSE", "error": str(exc)},
                         sort_keys=True), file=sys.stderr)
        raise
