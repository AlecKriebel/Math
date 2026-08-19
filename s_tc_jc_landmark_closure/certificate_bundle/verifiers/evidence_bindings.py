#!/usr/bin/env python3
"""Reconstruct the record-level evidence map for the bounded atlas.

The resulting rows are not a filename index.  Every row binds one canonical
directed relation/presentation to the exact graph, polynomial, transport,
root, and verifier records that discharge it.  The bundle verifier rebuilds
these rows from the underlying proof records and compares them byte-for-byte
with the frozen map.
"""

from __future__ import annotations

from collections import defaultdict
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Iterable


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


def load_canonicalizer(root: Path):
    path = root / "reviews/theta2_signature_gate/canonicalize_relations.py"
    spec = importlib.util.spec_from_file_location("bundle_theta2_canonicalizer", path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load theta-2 canonicalizer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def n3_rows(root: Path) -> list[dict]:
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
                })
            if not bindings:
                raise AssertionError((relation_id, "pending relation lacks hard-cover root"))
            evidence["restoration_roots"] = bindings
            base_verifier = "reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py"
            closure_verifier = "reviews/compact_probe_clean_clone_gate/semantic_gate.py"
        elif classification == "isomorphism_or_T":
            evidence["quotient"] = {
                "t_quotient_code_sha256": str(relation["t_quotient_code_sha256"]),
                "source_selected_graph_id": relation.get("source_graph_id"),
                "target_selected_graph_id": relation.get("target_selected_graph_id"),
            }
            base_verifier = "reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py"
            closure_verifier = ""
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


def n4_rows(root: Path) -> list[dict]:
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


def reconstruct_rows(root: Path) -> list[dict]:
    rows = [*n3_rows(root), *n4_rows(root)]
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
    path = root / "atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz"
    frozen = read_rows(path)
    regenerated = reconstruct_rows(root)
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
    }
