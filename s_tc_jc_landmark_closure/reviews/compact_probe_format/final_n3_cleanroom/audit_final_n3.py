#!/usr/bin/env python3
"""Clean-room semantic audit of one final n=3 compact probe shard.

The implementation reuses only the already committed independent n=4 review
utilities and graph/Fourier engine (commit 35c0116d), plus ``engine_n3`` in
this directory.  It imports no module under ``primary`` and never accepts a
producer graph identifier, classification, witness, or transport without
regenerating the corresponding object from the encoded rooted graphs.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
N4 = HERE.parent / "final_n4_cleanroom"
sys.path.insert(0, str(N4))

import audit_final_n4 as common  # noqa: E402
from engine import (  # noqa: E402
    RootedGraph,
    admissible_internal_arcs,
    class_audit,
    exact_poly_hash,
    file_sha256,
    insert_port,
    load_invariants,
    polynomial_record,
    pullback,
    quartet_descriptor,
    require,
    stable_hash,
    transport_restricts,
)
from engine_n3 import (  # noqa: E402
    derive_and_validate_transport,
    prove_strict_open_cube_sign,
)


PROJECT = HERE.parents[2]
PRIMARY = PROJECT / "primary"
CERT = PRIMARY / "certificates"

EXPECTED_COMPACT = {
    "s0": "dc7b806f9afc1af9909682f47ea4bdc9ac5a8631d78ce3a6b15d41c4f171ad73",
    "s1": "996084af49c3e4ddf63b62cfa951be652a886e3424674f6e34d664b5a4901a37",
    "s2": "a8162d2bb136668ce2f204ce2012c85eb4dbb5e42c7037307d974b5f9ebf2286",
    "s3": "b246614dafc669784f8ef5e16ef62db79f08929b2afc2a6d14ce7f50bd7b7942",
}
EXPECTED_VERBOSE = "c8aa65474844276bc4d123152c6fd1b85276a38ee410ef61a4a64488f7886108"
CLASS_BY_CODE = common.CLASS_BY_CODE
INDEX_MASK = common.INDEX_MASK
SEPARATED = {
    "generic_polynomial_separation", "strict_open_cube_separation",
}
ALLOWED_CHILD = {"labelled_isomorphism", "ordinary_T"}
ALLOWED_BASE = common.ALLOWED_BASE


def load_verbose(summary_path: Path):
    """Load and content-address every verbose stream independently."""
    require(file_sha256(summary_path) == EXPECTED_VERBOSE,
            "verbose_summary_sha256")
    summary = json.loads(summary_path.read_text())
    require(summary["schema"] == "path-bound-common-anchor-probe-extension-v1",
            "verbose_schema")
    require(summary["status"] == "EXACTLY_COMPUTED", "verbose_status")
    loaded = {}; digests = {}; paths = {}
    for name, key in (("bindings", "probe_path_binding_id"),
                      ("states", "state_id"),
                      ("graphs", "graph_id"),
                      ("polynomials", "polynomial_id")):
        rows, digest, path = common.verify_verbose_stream(
            summary_path, summary, name, key)
        loaded[name] = rows; digests[name] = digest; paths[name] = path

    bindings = loaded["bindings"]
    states = {str(row["state_id"]): row for row in loaded["states"]}
    graphs = {str(row["graph_id"]): row for row in loaded["graphs"]}
    polynomials = {str(row["polynomial_id"]): row
                   for row in loaded["polynomials"]}
    for binding in bindings:
        body = {key: value for key, value in binding.items()
                if key not in {"schema", "probe_path_binding_id"}}
        require(stable_hash(body) == binding["probe_path_binding_id"],
                "verbose_binding_content_id")
    for identifier, state in states.items():
        body = {key: value for key, value in state.items()
                if key not in {"schema", "state_id"}}
        require(stable_hash(body) == identifier,
                "verbose_state_content_id", state_id=identifier)
    for identifier, row in graphs.items():
        require(common.graph_original_id(row["rooted_graph"]) == identifier,
                "verbose_graph_content_id", graph_id=identifier)
    for identifier, row in polynomials.items():
        body = {key: row[key]
                for key in ("schema", "variable_count", "terms")}
        require(stable_hash(body) == identifier,
                "verbose_polynomial_content_id", polynomial_id=identifier)
    by_base = defaultdict(list)
    for binding in bindings:
        by_base[str(binding["base_path_binding_id"])].append(binding)
    return {
        "summary": summary, "summary_path": summary_path,
        "summary_sha256": EXPECTED_VERBOSE,
        "bindings": bindings, "bindings_by_base": by_base,
        "states": states, "graphs": graphs, "polynomials": polynomials,
        "stream_sha256": digests, "stream_paths": paths,
    }


def audit_graph(caches, graph: RootedGraph, context):
    """Independently validate the locked graph class and cache its audit."""
    if graph.graph_id not in caches["graph_audits"]:
        result = class_audit(graph)
        require(result["triangle_count"] in (0, 1),
                "more_than_one_triangle", context=context,
                graph_id=graph.graph_id, audit=result)
        caches["graph_audits"][graph.graph_id] = result
    return caches["graph_audits"][graph.graph_id]


def graph_library_check(verbose, identifier: str, expected: RootedGraph,
                        caches, context, arcs=None):
    require(identifier == expected.graph_id, "generated_child_graph_id",
            context=context)
    require(identifier in verbose["graphs"], "verbose_graph_missing",
            graph_id=identifier, context=context)
    row = verbose["graphs"][identifier]
    require(RootedGraph.from_payload(row["rooted_graph"]) == expected,
            "verbose_graph_body", graph_id=identifier, context=context)
    independent = audit_graph(caches, expected, context)
    require(row["rooted_valid"] is True and
            row["standard_strong_local"] is True,
            "verbose_graph_flags", graph_id=identifier, context=context)
    if arcs is not None:
        require(tuple(tuple(x) for x in row["admissible_internal_arcs"]) == arcs,
                "verbose_admissible_arcs", graph_id=identifier,
                context=context)
    return independent


def _descriptor(caches, graph, port_count, chunk):
    key = (graph.graph_id, port_count, chunk)
    if key not in caches["descriptors"]:
        caches["descriptors"][key] = quartet_descriptor(
            graph, port_count, chunk)
    return caches["descriptors"][key]


def _pullback(caches, descriptor, invariant_index, invariants):
    key = (descriptor, invariant_index)
    if key not in caches["pullbacks"]:
        caches["pullbacks"][key] = pullback(
            descriptor, invariants[invariant_index])
    return caches["pullbacks"][key]


def _replay_witness(*, label, classification, witness, polynomial_library,
                    source, target, port_count, invariants, caches, context):
    """Independently replay one selected witness against the exact graphs."""
    chunk = int(witness["quartet_chunk"])
    invariant_index = int(witness["invariant_index"])
    require(0 <= invariant_index < len(invariants), "invariant_index",
            context=context, evidence=label, invariant_index=invariant_index)
    source_descriptor = _descriptor(caches, source, port_count, chunk)
    target_descriptor = _descriptor(caches, target, port_count, chunk)
    source_poly = _pullback(
        caches, source_descriptor, invariant_index, invariants)
    target_poly = _pullback(
        caches, target_descriptor, invariant_index, invariants)

    if classification == "generic_polynomial_separation":
        require(bool(source_poly) and not target_poly,
                "generic_separator_orientation", context=context,
                evidence=label)
        require(exact_poly_hash(source_poly) ==
                witness["source_pullback_exact_sha256"],
                "source_exact_pullback_sha256", context=context,
                evidence=label)
        polynomial_id, body = polynomial_record(source_poly)
        require(polynomial_id == witness["source_pullback_id"],
                "source_pullback_polynomial_id", context=context,
                evidence=label)
        require(witness["target_pullback"] == "0",
                "target_pullback_marker", context=context, evidence=label)
        sign_proof = None
    else:
        require(classification == "strict_open_cube_separation",
                "unexpected_separator_class", context=context, evidence=label)
        require(not source_poly and bool(target_poly),
                "strict_separator_orientation", context=context,
                evidence=label)
        require(witness["source_pullback"] == "0",
                "source_pullback_marker", context=context, evidence=label)
        require(exact_poly_hash(target_poly) ==
                witness["target_pullback_exact_sha256"],
                "target_exact_pullback_sha256", context=context,
                evidence=label)
        polynomial_id, body = polynomial_record(target_poly)
        require(polynomial_id == witness["target_pullback_id"],
                "target_pullback_polynomial_id", context=context,
                evidence=label)
        proof_key = exact_poly_hash(target_poly)
        if proof_key not in caches["sign_proofs"]:
            caches["sign_proofs"][proof_key] = (
                prove_strict_open_cube_sign(target_poly))
        sign_proof = caches["sign_proofs"][proof_key]
        require(sign_proof["strict_open_sign"] ==
                int(witness["target_strict_sign"]),
                "independent_strict_sign", context=context, evidence=label,
                independent=sign_proof["strict_open_sign"],
                stored=witness["target_strict_sign"])
        require(witness["target_sign_certificate"]["certified"] is True and
                int(witness["target_sign_certificate"]["strict_sign"]) ==
                int(witness["target_strict_sign"]),
                "stored_strict_sign_certificate", context=context,
                evidence=label)

    require(polynomial_id in polynomial_library,
            "pullback_body_missing", context=context, evidence=label,
            polynomial_id=polynomial_id)
    stored = polynomial_library[polynomial_id]
    require({key: stored[key] for key in body} == json.loads(json.dumps(body)),
            "pullback_polynomial_body", context=context, evidence=label)
    return {
        "polynomial_id": polynomial_id,
        "descriptor_pair_sha256": stable_hash(
            [source_descriptor, target_descriptor]),
        "sign_proof": sign_proof,
    }


def evidence_check(word, compact, verbose_state, verbose_polynomials,
                   source: RootedGraph, target: RootedGraph, port_count: int,
                   parent_transport, invariants, caches, used, context):
    """Regenerate both compact and verbose evidence for one exact relation."""
    code = int(word) >> 29
    index = int(word) & INDEX_MASK
    require(code in CLASS_BY_CODE, "reserved_class_code",
            context=context, code=code)
    classification = CLASS_BY_CODE[code]
    require(classification == verbose_state["classification"],
            "compact_verbose_classification", context=context)
    audit_graph(caches, source, context)
    audit_graph(caches, target, context)

    if classification in SEPARATED:
        require(index in compact["witnesses"], "witness_index",
                context=context, index=index)
        record = compact["witnesses"][index]
        verbose_record = {
            "classification": verbose_state["classification"],
            "probe_classification": verbose_state["probe_classification"],
            "probe_witness": verbose_state["probe_witness"],
        }
        require(record["classification"] == classification and
                record["probe_classification"] ==
                verbose_state["probe_classification"] == classification,
                "witness_classification", context=context)
        compact_replay = _replay_witness(
            label="compact", classification=classification,
            witness=record["probe_witness"],
            polynomial_library=compact["polynomials"], source=source,
            target=target, port_count=port_count, invariants=invariants,
            caches=caches, context=context)
        verbose_replay = _replay_witness(
            label="verbose", classification=classification,
            witness=verbose_state["probe_witness"],
            polynomial_library=verbose_polynomials, source=source,
            target=target, port_count=port_count, invariants=invariants,
            caches=caches, context=context)
        body_equal = ({key: record[key] for key in verbose_record} ==
                      verbose_record)
        caches["evidence_body_comparison"][(classification, body_equal)] += 1
        used["witnesses"].add(index)
        used["polynomials"].add(compact_replay["polynomial_id"])
        used["verbose_polynomials"].add(verbose_replay["polynomial_id"])
        compact_evidence_id = record["witness_id"]
        verbose_evidence_id = stable_hash(verbose_record)
        mapping = None
        compact_descriptor_pair = compact_replay["descriptor_pair_sha256"]
        verbose_descriptor_pair = verbose_replay["descriptor_pair_sha256"]
        compact_sign_proof = compact_replay["sign_proof"]
        verbose_sign_proof = verbose_replay["sign_proof"]
    else:
        require(classification in ALLOWED_CHILD,
                "unknown_transport_classification", context=context)
        require(index in compact["transports"], "transport_index",
                context=context, index=index)
        record = compact["transports"][index]
        verbose_record = {
            "classification": verbose_state["classification"],
            "transport": verbose_state["transport"],
            "canonicalization": verbose_state["canonicalization"],
            "fourier_coordinate_transport": "identity_on_fixed_port_labels",
        }
        mapping, independent_class = derive_and_validate_transport(
            source, target, record)
        verbose_mapping, verbose_independent_class = derive_and_validate_transport(
            source, target, verbose_record)
        require(independent_class == classification,
                "independent_transport_classification", context=context)
        require(verbose_independent_class == classification and
                verbose_mapping == mapping,
                "verbose_transport_semantics", context=context)
        require(transport_restricts(mapping, parent_transport),
                "incoherent_child_transport", context=context)

        # Regenerate displayed switchings, descendant masks, and
        # complement-normalized Fourier signatures for every transport cell.
        source_descriptor = _descriptor(caches, source, port_count, 0)
        target_descriptor = _descriptor(caches, target, port_count, 0)
        if classification == "labelled_isomorphism":
            require(source_descriptor == target_descriptor,
                    "isomorphism_descriptor_mismatch", context=context)
        body_equal = ({key: record[key] for key in verbose_record} ==
                      verbose_record)
        caches["evidence_body_comparison"][(classification, body_equal)] += 1
        used["transports"].add(index)
        compact_evidence_id = record["transport_id"]
        verbose_evidence_id = stable_hash(verbose_record)
        compact_descriptor_pair = stable_hash(
            [source_descriptor, target_descriptor])
        verbose_descriptor_pair = compact_descriptor_pair
        compact_sign_proof = None; verbose_sign_proof = None
    return {
        "classification": classification,
        "mapping": mapping,
        "compact_evidence_id": compact_evidence_id,
        "verbose_evidence_id": verbose_evidence_id,
        "evidence_body_equal": body_equal,
        "compact_descriptor_pair_sha256": compact_descriptor_pair,
        "verbose_descriptor_pair_sha256": verbose_descriptor_pair,
        "compact_sign_proof": compact_sign_proof,
        "verbose_sign_proof": verbose_sign_proof,
    }


def audit_shard(compact, inventory, verbose, invariants, writer):
    summary = compact["summary"]
    start, stop = map(int, summary["path_range"])
    require(len(inventory) == int(summary["path_inventory_count"]),
            "inventory_count")
    used = {"witnesses": set(), "transports": set(), "polynomials": set(),
            "verbose_polynomials": set(), "bindings": set()}
    caches = {"descriptors": {}, "pullbacks": {}, "sign_proofs": {},
              "graph_audits": {},
              "evidence_body_comparison": Counter()}
    counts = Counter(); stage_counts = Counter(); triangle_cells = Counter()
    inventory_fields = (
        "base_summary", "base_run_index", "base_state_id",
        "base_path_binding_id", "fixed_full_root_case_id",
        "selected_port_count", "source_parent_graph_id",
        "target_parent_graph_id", "source_parent_normalized_graph_id",
        "target_parent_normalized_graph_id", "base_dummy_order",
        "base_restored_role_to_label",
    )
    total_verbose = set()
    for path_offset, row in enumerate(compact["paths"]):
        path_index = start + path_offset
        require(int(row["path_index"]) == path_index, "path_index")
        require(stable_hash({key: value for key, value in row.items()
                             if key != "path_record_id"}) ==
                row["path_record_id"], "path_record_id",
                path_index=path_index)
        entry = inventory[path_index]
        for key in inventory_fields:
            require(row[key] == entry[key], "path_inventory_binding",
                    path_index=path_index, key=key)
        source_parent = entry["source"]; target_parent = entry["target"]
        require(source_parent.graph_id ==
                row["source_parent_normalized_graph_id"],
                "source_parent_normalized_id")
        require(target_parent.graph_id ==
                row["target_parent_normalized_graph_id"],
                "target_parent_normalized_id")
        audit_graph(caches, source_parent, [path_index, "source_parent"])
        audit_graph(caches, target_parent, [path_index, "target_parent"])

        base_index = int(row["base_transport_index"])
        require(base_index in compact["transports"], "base_transport_index")
        base_record = compact["transports"][base_index]
        expected_base = ALLOWED_BASE[entry["base_terminal_classification"]]
        require(base_record["classification"] == expected_base,
                "base_transport_classification", path_index=path_index)
        base_mapping, base_class = derive_and_validate_transport(
            source_parent, target_parent, base_record)
        require(base_class == expected_base,
                "independent_base_transport_classification",
                path_index=path_index)
        used["transports"].add(base_index)

        source_p_arcs = admissible_internal_arcs(source_parent)
        target_p_arcs = admissible_internal_arcs(target_parent)
        require(tuple(tuple(x) for x in row["source_p_arcs"]) == source_p_arcs,
                "source_p_arc_order", path_index=path_index)
        require(tuple(tuple(x) for x in row["target_p_arcs"]) == target_p_arcs,
                "target_p_arc_order", path_index=path_index)
        p_keys = tuple((s, t) for s in source_p_arcs for t in target_p_arcs)
        require(len(p_keys) == int(row["p_word_count"]), "p_word_count",
                path_index=path_index)
        p_words = common.decode_words(
            row["p_words_base64_le_u32"], len(p_keys))
        q_words = common.decode_words(
            row["q_words_base64_le_u32"], int(row["q_word_count"]))

        path_bindings = verbose["bindings_by_base"][
            row["base_path_binding_id"]]
        total_verbose.update(b["probe_path_binding_id"] for b in path_bindings)
        p_bindings = [b for b in path_bindings if b["stage"] == "A_plus_p"]
        q_bindings = [b for b in path_bindings
                      if b["stage"] == "A_plus_p_plus_q"]
        p_by_arcs = {}
        for binding in p_bindings:
            key = (tuple(binding["source_insertion"]["subdivided_parent_arc"]),
                   tuple(binding["target_insertion"]["subdivided_parent_arc"]))
            require(key not in p_by_arcs, "duplicate_verbose_p_relation",
                    path_index=path_index)
            p_by_arcs[key] = binding
        require(set(p_by_arcs) == set(p_keys), "p_relation_bijection",
                path_index=path_index, expected=len(p_keys),
                actual=len(p_by_arcs))

        allowed = []; q_shapes = []; q_cursor = 0
        p0 = int(row["selected_port_count"])
        for p_flat, (source_arc, target_arc) in enumerate(p_keys):
            source_p, source_meta = insert_port(
                source_parent, source_arc, f"L_{p0}")
            target_p, target_meta = insert_port(
                target_parent, target_arc, f"L_{p0}")
            binding = p_by_arcs[(source_arc, target_arc)]
            state = verbose["states"][binding["state_id"]]
            common.binding_common(
                binding, state, row, stage="A_plus_p",
                selected_count=p0 + 1,
                source_parent=source_parent.graph_id,
                target_parent=target_parent.graph_id,
                source_child=source_p.graph_id,
                target_child=target_p.graph_id,
                source_insertion=source_meta, target_insertion=target_meta)
            require(binding["parent_probe_path_binding_id"] is None,
                    "p_parent_binding", path_index=path_index, p_flat=p_flat)
            require(binding["base_transport"] == base_record["transport"] and
                    binding["base_canonicalization"] ==
                    base_record["canonicalization"],
                    "verbose_base_transport", path_index=path_index,
                    p_flat=p_flat)
            graph_library_check(
                verbose, source_p.graph_id, source_p, caches,
                [path_index, "p", p_flat, "source"],
                admissible_internal_arcs(source_p))
            graph_library_check(
                verbose, target_p.graph_id, target_p, caches,
                [path_index, "p", p_flat, "target"],
                admissible_internal_arcs(target_p))
            evidence = evidence_check(
                p_words[p_flat], compact, state, verbose["polynomials"],
                source_p, target_p, p0 + 1, base_mapping, invariants,
                caches, used,
                [path_index, "p", p_flat])
            classification = evidence["classification"]
            child_mapping = evidence["mapping"]
            used["bindings"].add(binding["probe_path_binding_id"])
            counts[classification] += 1; stage_counts["A_plus_p"] += 1
            triangle_cells[(classification,
                            class_audit(source_p)["triangle_count"],
                            class_audit(target_p)["triangle_count"])] += 1
            writer.write({
                "path_index": path_index, "stage": "A_plus_p",
                "flat_index": p_flat,
                "source_parent_graph_id": source_parent.graph_id,
                "target_parent_graph_id": target_parent.graph_id,
                "source_arc": source_arc, "target_arc": target_arc,
                "source_child_graph_id": source_p.graph_id,
                "target_child_graph_id": target_p.graph_id,
                "classification": classification,
                "compact_evidence_id": evidence["compact_evidence_id"],
                "verbose_evidence_id": evidence["verbose_evidence_id"],
                "evidence_body_equal": evidence["evidence_body_equal"],
                "compact_descriptor_pair_sha256":
                    evidence["compact_descriptor_pair_sha256"],
                "verbose_descriptor_pair_sha256":
                    evidence["verbose_descriptor_pair_sha256"],
                "compact_independent_sign_proof_sha256": (
                    stable_hash(evidence["compact_sign_proof"])
                    if evidence["compact_sign_proof"] else None),
                "verbose_independent_sign_proof_sha256": (
                    stable_hash(evidence["verbose_sign_proof"])
                    if evidence["verbose_sign_proof"] else None),
                "verbose_binding_id": binding["probe_path_binding_id"],
                "verbose_state_id": state["state_id"],
            })
            if classification not in ALLOWED_CHILD:
                require(not any(q["parent_probe_path_binding_id"] ==
                                binding["probe_path_binding_id"]
                                for q in q_bindings),
                        "q_under_separated_p", path_index=path_index,
                        p_flat=p_flat)
                continue
            allowed.append(p_flat)
            source_q_arcs = admissible_internal_arcs(source_p)
            target_q_arcs = admissible_internal_arcs(target_p)
            q_shapes.append([len(source_q_arcs), len(target_q_arcs)])
            q_keys = tuple((s, t) for s in source_q_arcs
                           for t in target_q_arcs)
            q_group = [q for q in q_bindings
                       if q["parent_probe_path_binding_id"] ==
                       binding["probe_path_binding_id"]]
            q_by_arcs = {}
            for q_binding in q_group:
                key = (tuple(q_binding["source_insertion"]
                             ["subdivided_parent_arc"]),
                       tuple(q_binding["target_insertion"]
                             ["subdivided_parent_arc"]))
                require(key not in q_by_arcs, "duplicate_verbose_q_relation",
                        path_index=path_index, p_flat=p_flat)
                q_by_arcs[key] = q_binding
            require(set(q_by_arcs) == set(q_keys), "q_relation_bijection",
                    path_index=path_index, p_flat=p_flat,
                    expected=len(q_keys), actual=len(q_by_arcs))
            for q_local, (source_q_arc, target_q_arc) in enumerate(q_keys):
                require(q_cursor < len(q_words), "truncated_q_words",
                        path_index=path_index)
                source_q, source_q_meta = insert_port(
                    source_p, source_q_arc, f"L_{p0 + 1}")
                target_q, target_q_meta = insert_port(
                    target_p, target_q_arc, f"L_{p0 + 1}")
                q_binding = q_by_arcs[(source_q_arc, target_q_arc)]
                q_state = verbose["states"][q_binding["state_id"]]
                common.binding_common(
                    q_binding, q_state, row, stage="A_plus_p_plus_q",
                    selected_count=p0 + 2,
                    source_parent=source_p.graph_id,
                    target_parent=target_p.graph_id,
                    source_child=source_q.graph_id,
                    target_child=target_q.graph_id,
                    source_insertion=source_q_meta,
                    target_insertion=target_q_meta)
                require(q_binding["parent_transport"] == state["transport"],
                        "verbose_q_parent_transport", path_index=path_index,
                        p_flat=p_flat, q_local=q_local)
                graph_library_check(
                    verbose, source_q.graph_id, source_q, caches,
                    [path_index, "q", p_flat, q_local, "source"],
                    admissible_internal_arcs(source_q))
                graph_library_check(
                    verbose, target_q.graph_id, target_q, caches,
                    [path_index, "q", p_flat, q_local, "target"],
                    admissible_internal_arcs(target_q))
                q_evidence = evidence_check(
                    q_words[q_cursor], compact, q_state,
                    verbose["polynomials"], source_q, target_q,
                    p0 + 2, child_mapping, invariants, caches, used,
                    [path_index, "q", p_flat, q_local])
                q_class = q_evidence["classification"]
                used["bindings"].add(q_binding["probe_path_binding_id"])
                counts[q_class] += 1
                stage_counts["A_plus_p_plus_q"] += 1
                triangle_cells[(q_class,
                                class_audit(source_q)["triangle_count"],
                                class_audit(target_q)["triangle_count"])] += 1
                writer.write({
                    "path_index": path_index,
                    "stage": "A_plus_p_plus_q",
                    "parent_p_flat_index": p_flat,
                    "local_flat_index": q_local,
                    "global_q_flat_index": q_cursor,
                    "source_parent_graph_id": source_p.graph_id,
                    "target_parent_graph_id": target_p.graph_id,
                    "source_arc": source_q_arc, "target_arc": target_q_arc,
                    "source_child_graph_id": source_q.graph_id,
                    "target_child_graph_id": target_q.graph_id,
                    "classification": q_class,
                    "compact_evidence_id":
                        q_evidence["compact_evidence_id"],
                    "verbose_evidence_id":
                        q_evidence["verbose_evidence_id"],
                    "evidence_body_equal":
                        q_evidence["evidence_body_equal"],
                    "compact_descriptor_pair_sha256":
                        q_evidence["compact_descriptor_pair_sha256"],
                    "verbose_descriptor_pair_sha256":
                        q_evidence["verbose_descriptor_pair_sha256"],
                    "compact_independent_sign_proof_sha256": (
                        stable_hash(q_evidence["compact_sign_proof"])
                        if q_evidence["compact_sign_proof"] else None),
                    "verbose_independent_sign_proof_sha256": (
                        stable_hash(q_evidence["verbose_sign_proof"])
                        if q_evidence["verbose_sign_proof"] else None),
                    "verbose_binding_id": q_binding["probe_path_binding_id"],
                    "verbose_state_id": q_state["state_id"],
                })
                q_cursor += 1
        require(row["allowed_p_flat_indices"] == allowed,
                "allowed_p_flat_indices", path_index=path_index)
        require(row["q_shapes"] == q_shapes, "q_shape_blocks",
                path_index=path_index)
        require(q_cursor == len(q_words), "q_word_exhaustion",
                path_index=path_index)
        require(len(path_bindings) == len(p_bindings) + len(q_bindings),
                "unknown_verbose_stage", path_index=path_index)
        require(set(b["probe_path_binding_id"] for b in path_bindings) <=
                used["bindings"], "unconsumed_verbose_path_binding",
                path_index=path_index)

    require(used["bindings"] == total_verbose, "verbose_binding_bijection",
            used=len(used["bindings"]), expected=len(total_verbose))
    require(dict(sorted(counts.items())) == summary["counts"],
            "classification_counts", actual=dict(sorted(counts.items())),
            expected=summary["counts"])
    require(used["witnesses"] == set(compact["witnesses"]),
            "orphan_witnesses")
    require(used["transports"] == set(compact["transports"]),
            "orphan_transports")
    require(used["polynomials"] == set(compact["polynomials"]),
            "orphan_polynomials")
    graph_triangle_counts = Counter(
        result["triangle_count"] for result in caches["graph_audits"].values())
    return {
        "counts": dict(sorted(counts.items())),
        "stage_counts": dict(sorted(stage_counts.items())),
        "verbose_bindings_compared": len(used["bindings"]),
        "witnesses_replayed": len(used["witnesses"]),
        "transports_replayed": len(used["transports"]),
        "polynomials_replayed": len(used["polynomials"]),
        "verbose_selected_polynomials_replayed":
            len(used["verbose_polynomials"]),
        "selected_polynomial_library_overlap":
            len(used["polynomials"] & used["verbose_polynomials"]),
        "compact_only_selected_polynomials":
            len(used["polynomials"] - used["verbose_polynomials"]),
        "verbose_only_selected_polynomials":
            len(used["verbose_polynomials"] - used["polynomials"]),
        "unique_exact_rooted_graphs_audited": len(caches["graph_audits"]),
        "rooted_graph_triangle_counts": {
            str(key): value for key, value in sorted(graph_triangle_counts.items())},
        "zero_sum_descriptors_regenerated": len(caches["descriptors"]),
        "exact_pullbacks_regenerated": len(caches["pullbacks"]),
        "independent_strict_sign_proofs": len(caches["sign_proofs"]),
        "evidence_body_comparison": [
            {"classification": key[0], "exact_body_equal": key[1],
             "count": value}
            for key, value in sorted(
                caches["evidence_body_comparison"].items())
        ],
        "nonidentical_but_semantically_valid_evidence_selections": sum(
            value for (classification, equal), value in
            caches["evidence_body_comparison"].items() if not equal),
        "ordinary_T_cells": counts.get("ordinary_T", 0),
        "strict_open_cube_cells": counts.get(
            "strict_open_cube_separation", 0),
        "triangle_cell_counts": [
            {"classification": key[0], "source_triangles": key[1],
             "target_triangles": key[2], "count": value}
            for key, value in sorted(triangle_cells.items())
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", choices=tuple(EXPECTED_COMPACT), required=True)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--verbose", type=Path,
                        default=CERT /
                        "probe_extension_schema3_n3_final_summary.json")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--relations", type=Path)
    args = parser.parse_args()
    summary_path = (args.summary or CERT /
                    f"compact_probe_schema3_n3_compact_{args.shard}_summary.json").resolve()
    output = (args.output or HERE / "certificates" /
              f"independent_{args.shard}.json").resolve()
    relation_path = (args.relations or HERE / "certificates" /
                     f"normalized_relations_{args.shard}.jsonl.gz").resolve()

    compact = common.load_compact(summary_path, EXPECTED_COMPACT[args.shard])
    base_paths = [common.resolve(path, summary_path)
                  for path in compact["summary"]["base_summaries"]]
    inventory, commitment_rows, input_hashes = common.build_inventory(base_paths)
    require(len(inventory) == int(compact["summary"]["path_inventory_count"]),
            "inventory_count")
    require(common.inventory_commitment(commitment_rows) ==
            compact["summary"]["path_inventory_sha256"],
            "inventory_commitment")
    require(input_hashes == compact["summary"]["input_sha256"],
            "inventory_input_commitments")
    verbose = load_verbose(args.verbose.resolve())
    invariants = load_invariants(
        PROJECT.parent /
        "strong_level2_phylo_identifiability/src/jc_root_spanning_atlas_data.py",
        PRIMARY / "seventh_invariant.json")

    writer = common.RelationWriter(relation_path)
    try:
        audit = audit_shard(compact, inventory, verbose, invariants, writer)
    except Exception:
        writer.gz.close(); writer.raw.close()
        raise
    relation_metadata = writer.close()
    require(relation_metadata["records"] ==
            audit["verbose_bindings_compared"],
            "normalized_relation_record_count")
    payload = {
        "schema": "compact-probe-final-n3-cleanroom-replay-v1",
        "status": "VERIFIED",
        "scope": "one exact final complement-normalized n=3 compact shard",
        "shard": args.shard,
        "summary": common.normalized(summary_path),
        "summary_sha256": EXPECTED_COMPACT[args.shard],
        "path_range": compact["summary"]["path_range"],
        "path_inventory_count": len(inventory),
        "path_inventory_sha256":
            compact["summary"]["path_inventory_sha256"],
        "schema_specification_sha256":
            compact["summary"]["schema_specification_sha256"],
        "verbose_summary": common.normalized(args.verbose.resolve()),
        "verbose_summary_sha256": EXPECTED_VERBOSE,
        "compact_stream_sha256": compact["stream_sha256"],
        "verbose_stream_sha256": verbose["stream_sha256"],
        "semantic_comparison": audit,
        "counts": audit["counts"],
        "normalized_relation_stream": relation_metadata,
        "independent_implementation": {
            "audit_script": common.normalized(Path(__file__)),
            "audit_script_sha256": file_sha256(Path(__file__)),
            "n3_engine": common.normalized(HERE / "engine_n3.py"),
            "n3_engine_sha256": file_sha256(HERE / "engine_n3.py"),
            "committed_n4_engine": common.normalized(N4 / "engine.py"),
            "committed_n4_engine_sha256": file_sha256(N4 / "engine.py"),
            "committed_n4_audit_utilities":
                common.normalized(N4 / "audit_final_n4.py"),
            "committed_n4_audit_utilities_sha256":
                file_sha256(N4 / "audit_final_n4.py"),
            "imports_primary_modules": False,
            "descriptor_normalization": (
                "minimum of quartet side and complement after zero-sum "
                "restriction"),
            "strict_sign_method": (
                "independent exact factorization and affine endpoint signs"),
        },
        "scope_limitations": {
            "ordinary_T_cells_present": audit["ordinary_T_cells"] > 0,
            "strict_open_cube_cells_present":
                audit["strict_open_cube_cells"] > 0,
            "claim": (
                "This verifies the evidence format and exact n=3 shard, not "
                "the landmark global identifiability theorem."),
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"], "shard": args.shard,
        "summary_sha256": payload["summary_sha256"],
        "path_range": payload["path_range"], "counts": payload["counts"],
        "relations": relation_metadata["records"],
        "output": common.normalized(output),
        "output_sha256": file_sha256(output),
    }, sort_keys=True), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FALSE", "error": str(exc)},
                         sort_keys=True), file=sys.stderr, flush=True)
        raise
