#!/usr/bin/env python3
"""Reconstruct the record-level evidence map for the bounded atlas.

The resulting rows are not a filename index.  Every row binds one canonical
directed relation/presentation to the exact graph, polynomial, transport,
root, and verifier records that discharge it.  The bundle verifier rebuilds
these rows from the underlying proof records and compares them byte-for-byte
with the frozen map.
"""

from __future__ import annotations

import base64
from collections import Counter, defaultdict
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
from typing import Iterable


INDEX_MASK = (1 << 29) - 1
SEPARATED_WORD_CODES = {0, 1}
TRANSPORT_WORD_CODES = {2, 3}

COMPACT_CLOSURE_REL = "atlas/COMPACT_PATH_CLOSURE_BINDINGS.jsonl.gz"
RESTORATION_CLOSURE_REL = "atlas/RESTORATION_CLOSURE_BINDINGS.jsonl.gz"
DIRECT_CLOSURE_REL = "atlas/DIRECT_ANCHOR_CLOSURE_BINDINGS.jsonl.gz"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def stable_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_jsonl(path: Path, key: str | None = None) -> list[dict] | dict[str, dict]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle]
    if key is None:
        return rows
    result: dict[str, dict] = {}
    for row in rows:
        identifier = str(row[key])
        if identifier in result:
            raise AssertionError((path, "duplicate record identifier", identifier))
        result[identifier] = row
    return result


def record_ref(path: str, key: str, identifier: str, row: dict) -> dict:
    return {
        "path": path,
        "key": key,
        "id": str(identifier),
        "record_sha256": stable_hash(row),
    }


def decode_words(encoded: str, expected: int) -> tuple[int, ...]:
    raw = base64.b64decode(encoded)
    if len(raw) != 4 * expected:
        raise AssertionError(("packed compact word length", len(raw), expected))
    if not raw:
        return ()
    return struct.unpack(f"<{expected}I", raw)


def compact_path_closure_rows(root: Path) -> list[dict]:
    """Bind every restoration terminal to all compact probe evidence it uses."""

    families = {
        "three_outgoing": "schema3_n3_compact_s",
        "four_outgoing": "theta2_compact_n4_s",
    }
    result: list[dict] = []
    seen_states: set[tuple[str, str]] = set()
    for family, prefix in families.items():
        for shard in range(4):
            base = "primary/certificates"
            path_rel = f"{base}/compact_probe_paths_{prefix}{shard}.jsonl.gz"
            witness_rel = f"{base}/compact_probe_witnesses_{prefix}{shard}.jsonl.gz"
            transport_rel = f"{base}/compact_probe_transports_{prefix}{shard}.jsonl.gz"
            polynomial_rel = f"{base}/compact_probe_polynomials_{prefix}{shard}.jsonl.gz"
            paths = load_jsonl(root / path_rel)
            witnesses = load_jsonl(root / witness_rel, "witness_index")
            transports = load_jsonl(root / transport_rel, "transport_index")
            polynomials = load_jsonl(root / polynomial_rel, "polynomial_id")
            for path in paths:
                state_id = str(path["base_state_id"])
                state_key = (family, state_id)
                if state_key in seen_states:
                    raise AssertionError(("duplicate compact terminal state", state_key))
                seen_states.add(state_key)
                words = (
                    *decode_words(path["p_words_base64_le_u32"], int(path["p_word_count"])),
                    *decode_words(path["q_words_base64_le_u32"], int(path["q_word_count"])),
                )
                witness_indices = sorted({
                    word & INDEX_MASK for word in words
                    if word >> 29 in SEPARATED_WORD_CODES
                })
                transport_indices = sorted({
                    int(path["base_transport_index"]),
                    *(
                        word & INDEX_MASK for word in words
                        if word >> 29 in TRANSPORT_WORD_CODES
                    ),
                })
                if any(word >> 29 not in (SEPARATED_WORD_CODES | TRANSPORT_WORD_CODES)
                       for word in words):
                    raise AssertionError((state_id, "reserved compact word code"))
                witness_refs = []
                polynomial_ids: set[str] = set()
                for index in witness_indices:
                    witness = witnesses.get(str(index))
                    if witness is None:
                        raise AssertionError((state_id, "missing compact witness", index))
                    witness_refs.append(record_ref(
                        witness_rel, "witness_index", str(index), witness
                    ))
                    probe = witness["probe_witness"]
                    candidates = [
                        str(probe[key]) for key in ("source_pullback_id", "target_pullback_id")
                        if key in probe
                    ]
                    if len(candidates) != 1:
                        raise AssertionError((state_id, "compact witness polynomial", index))
                    polynomial_ids.add(candidates[0])
                transport_refs = []
                for index in transport_indices:
                    transport = transports.get(str(index))
                    if transport is None:
                        raise AssertionError((state_id, "missing compact transport", index))
                    transport_refs.append(record_ref(
                        transport_rel, "transport_index", str(index), transport
                    ))
                polynomial_refs = []
                for identifier in sorted(polynomial_ids):
                    polynomial = polynomials.get(identifier)
                    if polynomial is None:
                        raise AssertionError((state_id, "missing compact polynomial", identifier))
                    polynomial_refs.append(record_ref(
                        polynomial_rel, "polynomial_id", identifier, polynomial
                    ))
                closure_id = stable_hash({
                    "family": family,
                    "base_state_id": state_id,
                    "path_record_id": path["path_record_id"],
                })
                row = {
                    "schema": "stc-jc-compact-path-closure-v1",
                    "closure_id": closure_id,
                    "family": family,
                    "base_state_id": state_id,
                    "fixed_full_root_case_id": str(path["fixed_full_root_case_id"]),
                    "path": record_ref(
                        path_rel, "path_record_id", str(path["path_record_id"]), path
                    ),
                    "probe_relation_counts": {
                        "one_port": int(path["p_word_count"]),
                        "two_port": int(path["q_word_count"]),
                    },
                    "witnesses": witness_refs,
                    "transports": transport_refs,
                    "polynomials": polynomial_refs,
                }
                row["closure_binding_sha256"] = stable_hash(row)
                result.append(row)
    result.sort(key=lambda row: (row["family"], row["base_state_id"]))
    return result


def restoration_closure_rows(root: Path, compact_rows: list[dict]) -> list[dict]:
    """Bind every hard-cover root to its complete restoration tree and probes."""

    compact_by_state = {
        (row["family"], row["base_state_id"]): row for row in compact_rows
    }
    specs = {
        "three_outgoing": (
            "primary/certificates/hard_cover_root_cases_n3_schema3_n3_full.jsonl.gz",
            "primary/certificates/hard_cover_n3_schema3_n3_full.jsonl.gz",
            "primary/certificates/hard_cover_polynomials_n3_schema3_n3_full.jsonl.gz",
        ),
        "four_outgoing": (
            "primary/certificates/hard_cover_root_cases_n4_schema3_theta2_full.jsonl.gz",
            "primary/certificates/hard_cover_n4_schema3_theta2_full.jsonl.gz",
            "primary/certificates/hard_cover_polynomials_n4_schema3_theta2_full.jsonl.gz",
        ),
    }
    result: list[dict] = []
    used_compact: set[tuple[str, str]] = set()
    for family, (root_rel, state_rel, polynomial_rel) in specs.items():
        roots = load_jsonl(root / root_rel, "root_case_id")
        states = load_jsonl(root / state_rel, "state_id")
        polynomials = load_jsonl(root / polynomial_rel, "polynomial_id")
        for root_id in sorted(roots):
            root_row = roots[root_id]
            stack = [str(value) for value in root_row["entry_state_ids"]]
            reachable: set[str] = set()
            while stack:
                state_id = stack.pop()
                if state_id in reachable:
                    continue
                state = states.get(state_id)
                if state is None:
                    raise AssertionError((root_id, "missing restoration state", state_id))
                if str(state["fixed_full_root_case_id"]) != root_id:
                    raise AssertionError((root_id, "cross-root restoration edge", state_id))
                reachable.add(state_id)
                stack.extend(str(value) for value in state["children"])

            state_refs = []
            polynomial_bindings = []
            compact_bindings = []
            terminal_counts: Counter[str] = Counter()
            for state_id in sorted(reachable):
                state = states[state_id]
                classification = str(state["terminal_classification"])
                terminal_counts[classification] += 1
                state_refs.append({
                    **record_ref(state_rel, "state_id", state_id, state),
                    "terminal_classification": classification,
                })
                if classification == "refined_by_next_restoration":
                    if not state["children"]:
                        raise AssertionError((state_id, "refinement state has no children"))
                    continue
                if state["children"]:
                    raise AssertionError((state_id, "terminal state has children"))
                if classification in {
                    "generic_polynomial_separation", "strict_open_cube_separation"
                }:
                    witness = state.get("probe_witness") or {}
                    keys = [key for key in ("source_pullback_id", "target_pullback_id")
                            if key in witness]
                    if len(keys) != 1:
                        raise AssertionError((state_id, "hard-cover polynomial witness"))
                    polynomial_id = str(witness[keys[0]])
                    polynomial = polynomials.get(polynomial_id)
                    if polynomial is None:
                        raise AssertionError((state_id, "missing hard-cover polynomial"))
                    polynomial_bindings.append({
                        "state_id": state_id,
                        "classification": classification,
                        "polynomial": record_ref(
                            polynomial_rel, "polynomial_id", polynomial_id, polynomial
                        ),
                    })
                elif classification in {
                    "support_prefix_labelled_isomorphism",
                    "support_prefix_ordinary_T",
                }:
                    compact = compact_by_state.get((family, state_id))
                    if compact is None:
                        raise AssertionError((state_id, "missing compact closure"))
                    if compact["fixed_full_root_case_id"] != root_id:
                        raise AssertionError((state_id, "compact/root mismatch"))
                    used_compact.add((family, state_id))
                    compact_bindings.append({
                        "state_id": state_id,
                        "classification": classification,
                        "compact_closure": record_ref(
                            COMPACT_CLOSURE_REL, "closure_id",
                            str(compact["closure_id"]), compact,
                        ),
                    })
                else:
                    raise AssertionError((state_id, "unknown hard-cover classification",
                                          classification))
            closure_id = stable_hash({"family": family, "root_case_id": root_id})
            row = {
                "schema": "stc-jc-restoration-root-closure-v1",
                "closure_id": closure_id,
                "family": family,
                "root_case_id": root_id,
                "root": record_ref(root_rel, "root_case_id", root_id, root_row),
                "reachable_state_count": len(reachable),
                "terminal_counts": dict(sorted(terminal_counts.items())),
                "states": state_refs,
                "terminal_polynomials": polynomial_bindings,
                "compact_terminals": compact_bindings,
            }
            row["closure_binding_sha256"] = stable_hash(row)
            result.append(row)
    if used_compact != set(compact_by_state):
        raise AssertionError(("orphan compact closures",
                              len(set(compact_by_state) - used_compact)))
    result.sort(key=lambda row: (row["family"], row["root_case_id"]))
    return result


def direct_anchor_closure_rows(root: Path) -> list[dict]:
    """Bind all 62 residual anchors to every one/two-port child certificate."""

    base = "reviews/direct_anchor_probe_closure/certificates"
    anchor_rel = f"{base}/anchors.jsonl.gz"
    graph_rel = f"{base}/graphs.jsonl.gz"
    p_rel = f"{base}/p_relations.jsonl.gz"
    q_rel = f"{base}/q_relations.jsonl.gz"
    witness_rel = f"{base}/witnesses.jsonl.gz"
    anchors = load_jsonl(root / anchor_rel, "direct_anchor_id")
    graphs = load_jsonl(root / graph_rel, "graph_sha256")
    p_rows = load_jsonl(root / p_rel, "relation_id")
    q_rows = load_jsonl(root / q_rel, "relation_id")
    witnesses = load_jsonl(root / witness_rel, "witness_id")
    p_by_anchor: dict[str, list[dict]] = defaultdict(list)
    q_by_anchor: dict[str, list[dict]] = defaultdict(list)
    for row in p_rows.values():
        p_by_anchor[str(row["direct_anchor_id"])].append(row)
    for row in q_rows.values():
        q_by_anchor[str(row["direct_anchor_id"])].append(row)

    result = []
    used_p: set[str] = set()
    used_q: set[str] = set()
    used_witnesses: set[str] = set()
    for anchor_id in sorted(anchors):
        anchor = anchors[anchor_id]
        children_p = sorted(p_by_anchor.get(anchor_id, []),
                            key=lambda row: row["relation_id"])
        children_q = sorted(q_by_anchor.get(anchor_id, []),
                            key=lambda row: row["relation_id"])
        p_ids = {str(row["relation_id"]) for row in children_p}
        if any(str(row["parent_relation_id"]) not in p_ids for row in children_q):
            raise AssertionError((anchor_id, "two-port child lacks one-port parent"))
        graph_ids = {
            str(anchor["source_graph_sha256"]), str(anchor["target_graph_sha256"]),
        }
        witness_ids: set[str] = set()
        for row in (*children_p, *children_q):
            graph_ids.update((str(row["source_graph_sha256"]),
                              str(row["target_graph_sha256"])))
            if row.get("witness_id"):
                witness_ids.add(str(row["witness_id"]))
        for graph_id in graph_ids:
            if graph_id not in graphs:
                raise AssertionError((anchor_id, "missing direct-anchor graph", graph_id))
        for witness_id in witness_ids:
            if witness_id not in witnesses:
                raise AssertionError((anchor_id, "missing direct-anchor witness", witness_id))
        used_p.update(p_ids)
        used_q.update(str(row["relation_id"]) for row in children_q)
        used_witnesses.update(witness_ids)
        closure_id = stable_hash({"direct_anchor_id": anchor_id})
        row = {
            "schema": "stc-jc-direct-anchor-closure-v1",
            "closure_id": closure_id,
            "direct_anchor_id": anchor_id,
            "anchor": record_ref(anchor_rel, "direct_anchor_id", anchor_id, anchor),
            "classification": str(anchor["classification"]),
            "one_port_relations": [
                record_ref(p_rel, "relation_id", str(child["relation_id"]), child)
                for child in children_p
            ],
            "two_port_relations": [
                record_ref(q_rel, "relation_id", str(child["relation_id"]), child)
                for child in children_q
            ],
            "graphs": [
                record_ref(graph_rel, "graph_sha256", graph_id, graphs[graph_id])
                for graph_id in sorted(graph_ids)
            ],
            "witnesses": [
                record_ref(witness_rel, "witness_id", witness_id,
                           witnesses[witness_id])
                for witness_id in sorted(witness_ids)
            ],
            "classification_counts": {
                "one_port": dict(sorted(Counter(
                    child["classification"] for child in children_p
                ).items())),
                "two_port": dict(sorted(Counter(
                    child["classification"] for child in children_q
                ).items())),
            },
        }
        row["closure_binding_sha256"] = stable_hash(row)
        result.append(row)
    if used_p != set(p_rows) or used_q != set(q_rows):
        raise AssertionError(("orphan direct-anchor relations",
                              len(set(p_rows) - used_p), len(set(q_rows) - used_q)))
    if used_witnesses != set(witnesses):
        raise AssertionError(("orphan direct-anchor witnesses",
                              len(set(witnesses) - used_witnesses)))
    return result


def load_canonicalizer(root: Path):
    path = root / "reviews/theta2_signature_gate/canonicalize_relations.py"
    spec = importlib.util.spec_from_file_location("bundle_theta2_canonicalizer", path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load theta-2 canonicalizer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def n3_rows(
    root: Path,
    restoration_closures: dict[tuple[str, str], dict],
    direct_closures: dict[str, dict],
) -> list[dict]:
    cert = root / "primary/certificates"
    relation_rel = "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_relations.jsonl.gz"
    graph_rel = "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_graphs.jsonl.gz"
    polynomial_rel = "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_polynomials.jsonl.gz"
    sign_rel = "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_signs.json"
    crosswalk_rel = "primary/certificates/bounded_relation_n3_hard_cover_crosswalk.jsonl.gz"
    root_rel = "primary/certificates/hard_cover_root_cases_n3_schema3_n3_full.jsonl.gz"
    state_rel = "primary/certificates/hard_cover_n3_schema3_n3_full.jsonl.gz"

    relations = load_jsonl(root / relation_rel, "relation_id")
    graphs = load_jsonl(root / graph_rel, "graph_id")
    polynomials = load_jsonl(root / polynomial_rel, "polynomial_id")
    signs = json.loads((root / sign_rel).read_text(encoding="utf-8"))
    roots = load_jsonl(root / root_rel, "root_case_id")
    states = load_jsonl(root / state_rel, "state_id")
    crosswalk = load_jsonl(root / crosswalk_rel)
    by_relation: dict[str, list[tuple[int, dict]]] = defaultdict(list)
    for ordinal, row in enumerate(crosswalk):
        by_relation[str(row["relation_id"])].append((ordinal, row))
    direct_anchor_rel = "reviews/direct_anchor_probe_closure/certificates/anchors.jsonl.gz"
    direct_anchors = load_jsonl(root / direct_anchor_rel, "direct_anchor_id")
    direct_by_graphs = {}
    for anchor_id, anchor in direct_anchors.items():
        key = (
            str(anchor["source_input_graph_id"]),
            str(anchor["target_completion_input_graph_id"]),
            str(anchor["target_selected_input_graph_id"]),
        )
        if key in direct_by_graphs:
            raise AssertionError(("duplicate direct-anchor graph triple", key))
        direct_by_graphs[key] = anchor_id

    result = []
    for relation_id in sorted(relations):
        relation = relations[relation_id]
        source_id = str(relation["source_graph_id"])
        target_id = str(relation["target_completion_graph_id"])
        evidence: dict[str, object] = {
            "relation": record_ref(relation_rel, "relation_id", relation_id, relation),
            "source_graph": record_ref(graph_rel, "graph_id", source_id, graphs[source_id]),
            "target_graph": record_ref(graph_rel, "graph_id", target_id, graphs[target_id]),
        }
        classification = str(relation["classification"])
        if classification == "strict_open_cube_separation":
            witness = relation["witness"]
            polynomial_id = str(witness["target_pullback_id"])
            exact_hash = str(witness["target_pullback_exact_sha256"])
            polynomial = polynomials[polynomial_id]
            sign = signs[exact_hash]
            if polynomial.get("exact_polynomial_sha256") != exact_hash:
                raise AssertionError((relation_id, "polynomial exact hash"))
            if sign.get("polynomial_id") != polynomial_id:
                raise AssertionError((relation_id, "sign/polynomial binding"))
            evidence["strict_witness"] = {
                "quartet_chunk": int(witness["quartet_chunk"]),
                "invariant_index": int(witness["invariant_index"]),
                "strict_sign": int(witness["strict_sign"]),
                "exact_pullback_sha256": exact_hash,
                "polynomial": record_ref(
                    polynomial_rel, "polynomial_id", polynomial_id, polynomial
                ),
                "sign_record": {
                    "path": sign_rel,
                    "key": "exact_polynomial_sha256",
                    "id": exact_hash,
                    "record_sha256": stable_hash(sign),
                },
            }
            base_verifier = "reviews/base_gate_adversarial_referee_n3/referee_n3.py"
            closure_verifier = ""
        elif classification == "pending_support_completion":
            bindings = []
            for ordinal, cross in sorted(by_relation.get(relation_id, [])):
                root_id = str(cross["root_case_id"])
                root_row = roots[root_id]
                entries = []
                for state_id in root_row["entry_state_ids"]:
                    state = states[str(state_id)]
                    entries.append({
                        **record_ref(state_rel, "state_id", str(state_id), state),
                        "terminal_classification": state["terminal_classification"],
                    })
                bindings.append({
                    "crosswalk_ordinal": ordinal,
                    "crosswalk_record_sha256": stable_hash(cross),
                    "raw_coverage_ordinal": int(cross["raw_coverage_ordinal"]),
                    "raw_coverage_sha256": str(cross["raw_coverage_sha256"]),
                    "root": record_ref(root_rel, "root_case_id", root_id, root_row),
                    "entry_states": entries,
                    "closure": record_ref(
                        RESTORATION_CLOSURE_REL,
                        "closure_id",
                        str(restoration_closures[("three_outgoing", root_id)]["closure_id"]),
                        restoration_closures[("three_outgoing", root_id)],
                    ),
                })
            if not bindings:
                raise AssertionError((relation_id, "pending relation lacks hard-cover root"))
            evidence["restoration_roots"] = bindings
            base_verifier = "reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py"
            closure_verifier = "reviews/compact_probe_clean_clone_gate/semantic_gate.py"
        elif classification == "isomorphism_or_T":
            graph_key = (
                source_id,
                str(relation["target_completion_graph_id"]),
                str(relation["target_selected_graph_id"]),
            )
            anchor_id = direct_by_graphs.get(graph_key)
            if anchor_id is None:
                raise AssertionError((relation_id, "missing direct-anchor closure"))
            closure = direct_closures.get(anchor_id)
            if closure is None:
                raise AssertionError((relation_id, "unknown direct-anchor closure", anchor_id))
            evidence["quotient"] = {
                "t_quotient_code_sha256": str(relation["t_quotient_code_sha256"]),
                "source_selected_graph_id": relation.get("source_graph_id"),
                "target_selected_graph_id": relation.get("target_selected_graph_id"),
            }
            evidence["direct_anchor_closure"] = record_ref(
                DIRECT_CLOSURE_REL, "closure_id", str(closure["closure_id"]), closure
            )
            base_verifier = "reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py"
            closure_verifier = "reviews/direct_anchor_probe_closure/verify_direct_anchor_probes.py"
        else:
            raise AssertionError((relation_id, "unknown n3 classification", classification))

        row = {
            "schema": "stc-jc-record-evidence-binding-v2",
            "universe": "three_outgoing",
            "relation_id": relation_id,
            "direction": str(relation["direction"]),
            "source_graph_id": source_id,
            "target_graph_id": target_id,
            "disposition": classification,
            "base_verifier": base_verifier,
            "closure_verifier": closure_verifier,
            "evidence": evidence,
        }
        row["evidence_binding_sha256"] = stable_hash(row)
        result.append(row)
    return result


def n4_rows(
    root: Path,
    restoration_closures: dict[tuple[str, str], dict],
) -> list[dict]:
    presentation_rel = "reviews/theta2_signature_gate/presentation_crosswalk.jsonl"
    duplicate_rel = "reviews/theta2_signature_gate/canonical_duplicate_transports.jsonl"
    frozen_transport_rel = "reviews/theta2_signature_gate/frozen_presentation_transports.jsonl"
    quotient_rel = "reviews/theta2_signature_gate/canonical_quotient_certificate.json"
    root_rel = "primary/certificates/hard_cover_root_cases_n4_schema3_theta2_full.jsonl.gz"
    state_rel = "primary/certificates/hard_cover_n4_schema3_theta2_full.jsonl.gz"
    audit_rel = "reviews/final_hard_cover_cleanroom/certificates/schema3_n4_theta2_terminal_records.jsonl.gz"

    presentations = load_jsonl(root / presentation_rel)
    duplicate_transports = load_jsonl(root / duplicate_rel)
    frozen_transports = load_jsonl(root / frozen_transport_rel)
    quotient = json.loads((root / quotient_rel).read_text(encoding="utf-8"))
    roots_list = load_jsonl(root / root_rel)
    roots = {str(row["root_case_id"]): row for row in roots_list}
    states = load_jsonl(root / state_rel, "state_id")
    audit = load_jsonl(root / audit_rel, "state_id")
    canonicalizer = load_canonicalizer(root)

    normalized = [row["normalized_relation"] for row in presentations]
    frozen_normalized = []
    for root_row in roots_list:
        case = root_row["root_case"]
        frozen_normalized.append({
            "direction": "source_precedes_target",
            "selected_outgoing": case["selected_outgoing"],
            "selected_signature_sha256": case["selected_signature_sha256"],
            "source_position_to_label": case["source_position_to_label"],
            "source_provenance": case["source_provenance"],
            "target_provenance": case["target_provenance"],
            "target_dummy_roles": case["target_dummy_roles"],
            "target_position_to_label": case["target_position_to_label"],
        })

    canonical_by_raw: dict[int, tuple[str, str, str]] = {}
    raw_by_digest: dict[str, list[int]] = defaultdict(list)
    frozen_by_digest: dict[str, list[int]] = defaultdict(list)
    for index, value in enumerate(normalized):
        code, _transport = canonicalizer.relation_from_normalized(value)
        parsed = json.loads(code)
        digest = hashlib.sha256(code.encode()).hexdigest()
        canonical_by_raw[index] = (
            digest,
            hashlib.sha256(parsed["source"].encode()).hexdigest(),
            hashlib.sha256(parsed["target"].encode()).hexdigest(),
        )
        raw_by_digest[digest].append(index)
    for index, value in enumerate(frozen_normalized):
        code, _transport = canonicalizer.relation_from_normalized(value)
        frozen_by_digest[hashlib.sha256(code.encode()).hexdigest()].append(index)

    # Reconstruct the exact pairings used by canonicalize_relations.py.
    marginalized_pair: dict[int, tuple[int, int]] = {}
    transport_cursor = 0
    for digest in sorted(set(raw_by_digest) & set(frozen_by_digest)):
        left = [i for i in raw_by_digest[digest]
                if normalized[i]["target_dummy_roles"]
                and not normalized[i]["target_provenance"][-1]]
        right = frozen_by_digest[digest]
        if len(left) != len(right):
            continue
        for raw_index, frozen_index in zip(left, right):
            marginalized_pair[raw_index] = (frozen_index, transport_cursor)
            transport_cursor += 1
    if transport_cursor != len(frozen_transports):
        raise AssertionError("n4 frozen transport pairing count")

    selected_indices = [i for i, value in enumerate(normalized)
                        if value["target_dummy_roles"] and value["target_provenance"][-1]]
    selected_pair: dict[int, tuple[int, int]] = {}
    if len(selected_indices) != len(duplicate_transports):
        raise AssertionError("n4 duplicate transport count")
    for transport_index, raw_index in enumerate(selected_indices):
        digest = canonical_by_raw[raw_index][0]
        candidates = frozen_by_digest.get(digest, [])
        if not candidates:
            raise AssertionError((raw_index, "selected duplicate lacks frozen root"))
        selected_pair[raw_index] = (candidates[0], transport_index)

    direct_rows = quotient["direct_classifications"]
    direct_indices = [i for i, value in enumerate(normalized) if not value["target_dummy_roles"]]
    if len(direct_indices) != len(direct_rows):
        raise AssertionError("n4 direct classification count")
    direct_by_raw = {raw_index: direct_rows[j] for j, raw_index in enumerate(direct_indices)}

    result = []
    for raw_index, presentation in enumerate(presentations):
        value = presentation["normalized_relation"]
        relation_id = str(presentation["normalized_relation_sha256"])
        if stable_hash(value) != relation_id:
            raise AssertionError((raw_index, "normalized relation content address"))
        canonical_digest, source_graph_id, target_graph_id = canonical_by_raw[raw_index]
        evidence: dict[str, object] = {
            "presentation": {
                "path": presentation_rel,
                "ordinal": raw_index,
                "record_sha256": stable_hash(presentation),
                "canonical_relation_sha256": canonical_digest,
            }
        }
        if raw_index in direct_by_raw:
            direct = direct_by_raw[raw_index]
            if direct["classification"] != "labelled_mixed_graph_isomorphism":
                raise AssertionError((raw_index, "unresolved direct n4 relation"))
            disposition = "direct_labelled_isomorphism"
            evidence["direct_classification"] = {
                "path": quotient_rel,
                "record_index": int(direct["record_index"]),
                "record_sha256": stable_hash(direct),
            }
            base_verifier = "reviews/theta2_signature_gate/canonicalize_relations.py"
            closure_verifier = ""
        else:
            if raw_index in selected_pair:
                frozen_index, transport_index = selected_pair[raw_index]
                transport = duplicate_transports[transport_index]
                disposition = "selected_incoming_rooting_duplicate"
                transport_path = duplicate_rel
                base_verifier = "reviews/theta2_signature_gate/canonicalize_relations.py"
                closure_verifier = ""
            elif raw_index in marginalized_pair:
                frozen_index, transport_index = marginalized_pair[raw_index]
                transport = frozen_transports[transport_index]
                disposition = "fixed_full_restoration_root"
                transport_path = frozen_transport_rel
                base_verifier = "reviews/final_hard_cover_cleanroom/audit_candidate_stream.py"
                closure_verifier = "reviews/compact_probe_clean_clone_gate/semantic_gate.py"
            else:
                raise AssertionError((raw_index, "unclassified n4 presentation"))
            frozen_root = roots_list[frozen_index]
            root_id = str(frozen_root["root_case_id"])
            if transport["canonical_relation_sha256"] != canonical_digest:
                raise AssertionError((raw_index, "n4 transport canonical relation"))
            entries = []
            for state_id in frozen_root["entry_state_ids"]:
                state_id = str(state_id)
                state = states[state_id]
                entry = {
                    **record_ref(state_rel, "state_id", state_id, state),
                    "terminal_classification": state["terminal_classification"],
                }
                if state_id in audit:
                    entry["exact_audit"] = record_ref(
                        audit_rel, "state_id", state_id, audit[state_id]
                    )
                entries.append(entry)
            evidence["presentation_transport"] = {
                "path": transport_path,
                "ordinal": transport_index,
                "record_sha256": stable_hash(transport),
            }
            evidence["frozen_root"] = record_ref(
                root_rel, "root_case_id", root_id, frozen_root
            )
            evidence["entry_states"] = entries
            closure = restoration_closures[("four_outgoing", root_id)]
            evidence["restoration_closure"] = record_ref(
                RESTORATION_CLOSURE_REL, "closure_id",
                str(closure["closure_id"]), closure,
            )
            closure_verifier = "reviews/compact_probe_clean_clone_gate/semantic_gate.py"

        row = {
            "schema": "stc-jc-record-evidence-binding-v2",
            "universe": "four_outgoing_survivor",
            "relation_id": relation_id,
            "presentation_ordinal": raw_index,
            "direction": str(value["direction"]),
            "source_graph_id": source_graph_id,
            "target_graph_id": target_graph_id,
            "disposition": disposition,
            "base_verifier": base_verifier,
            "closure_verifier": closure_verifier,
            "evidence": evidence,
        }
        row["evidence_binding_sha256"] = stable_hash(row)
        result.append(row)
    return result


def reconstruct_closure_rows(root: Path) -> tuple[list[dict], list[dict], list[dict]]:
    compact = compact_path_closure_rows(root)
    restoration = restoration_closure_rows(root, compact)
    direct = direct_anchor_closure_rows(root)
    return compact, restoration, direct


def reconstruct_rows(
    root: Path,
    closures: tuple[list[dict], list[dict], list[dict]] | None = None,
) -> list[dict]:
    compact, restoration, direct = closures or reconstruct_closure_rows(root)
    restoration_map = {
        (row["family"], row["root_case_id"]): row for row in restoration
    }
    direct_map = {row["direct_anchor_id"]: row for row in direct}
    rows = [
        *n3_rows(root, restoration_map, direct_map),
        *n4_rows(root, restoration_map),
    ]
    rows.sort(key=lambda row: (
        row["universe"], row["relation_id"], int(row.get("presentation_ordinal", -1))
    ))
    return rows


def write_rows(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as out:
            for row in rows:
                out.write(canonical_bytes(row) + b"\n")


def read_rows(path: Path) -> list[dict]:
    return list(load_jsonl(path))


def assert_rows_equal(frozen: list[dict], regenerated: list[dict]) -> None:
    if frozen != regenerated:
        for index, (left, right) in enumerate(zip(frozen, regenerated)):
            if left != right:
                raise AssertionError(("evidence binding mismatch", index,
                                      left.get("relation_id"), right.get("relation_id")))
        raise AssertionError(("evidence binding length", len(frozen), len(regenerated)))


def verify_frozen(root: Path) -> dict:
    closure_specs = (
        (COMPACT_CLOSURE_REL, compact_path_closure_rows(root)),
        (RESTORATION_CLOSURE_REL, None),
        (DIRECT_CLOSURE_REL, direct_anchor_closure_rows(root)),
    )
    compact_regenerated = closure_specs[0][1]
    assert compact_regenerated is not None
    restoration_regenerated = restoration_closure_rows(root, compact_regenerated)
    regenerated_closures = (
        compact_regenerated,
        restoration_regenerated,
        closure_specs[2][1],
    )
    closure_counts = {}
    for relative, regenerated in (
        (COMPACT_CLOSURE_REL, regenerated_closures[0]),
        (RESTORATION_CLOSURE_REL, regenerated_closures[1]),
        (DIRECT_CLOSURE_REL, regenerated_closures[2]),
    ):
        assert regenerated is not None
        frozen_closure = read_rows(root / relative)
        assert_rows_equal(frozen_closure, regenerated)
        closure_counts[Path(relative).name] = len(frozen_closure)
    path = root / "atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz"
    frozen = read_rows(path)
    regenerated = reconstruct_rows(root, regenerated_closures)
    assert_rows_equal(frozen, regenerated)
    return {
        "records": len(frozen),
        "three_outgoing": sum(row["universe"] == "three_outgoing" for row in frozen),
        "four_outgoing_survivor": sum(
            row["universe"] == "four_outgoing_survivor" for row in frozen
        ),
        "logical_sha256": hashlib.sha256(
            b"".join(canonical_bytes(row) + b"\n" for row in frozen)
        ).hexdigest(),
        "closure_counts": closure_counts,
    }
