#!/usr/bin/env python3
"""Aggregate and verify the four final n=3 clean-room shard certificates."""

from __future__ import annotations

from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
CERT = HERE / "certificates"
EXPECTED = [
    "dc7b806f9afc1af9909682f47ea4bdc9ac5a8631d78ce3a6b15d41c4f171ad73",
    "996084af49c3e4ddf63b62cfa951be652a886e3424674f6e34d664b5a4901a37",
    "a8162d2bb136668ce2f204ce2012c85eb4dbb5e42c7037307d974b5f9ebf2286",
    "b246614dafc669784f8ef5e16ef62db79f08929b2afc2a6d14ce7f50bd7b7942",
]
VERBOSE_SHA = "c8aa65474844276bc4d123152c6fd1b85276a38ee410ef61a4a64488f7886108"
EXPECTED_COUNTS = {
    "generic_polynomial_separation": 90008,
    "labelled_isomorphism": 9676,
    "ordinary_T": 840,
    "strict_open_cube_separation": 624,
}
EXPECTED_STAGES = {
    "A_plus_p": 9316,
    "A_plus_p_plus_q": 91832,
}


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def logical_rows(path):
    digest = hashlib.sha256(); rows = 0
    with gzip.open(path, "rb") as handle:
        for raw in handle:
            digest.update(raw); rows += 1
    return rows, digest.hexdigest()


def normalized(path):
    return str(path.resolve().relative_to(PROJECT))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    counts = Counter(); stages = Counter(); body_comparison = Counter()
    cursor = 0; all_bindings = set(); shard_rows = []
    total_graphs = 0; total_descriptors = 0; total_pullbacks = 0
    unique_sign_proof_counts = []
    for index, expected in enumerate(EXPECTED):
        path = CERT / f"independent_s{index}.json"
        payload = json.loads(path.read_text())
        require(payload["status"] == "VERIFIED", f"s{index} status")
        require(payload["summary_sha256"] == expected, f"s{index} summary")
        start, stop = map(int, payload["path_range"])
        require(start == cursor and stop >= start, f"s{index} range")
        require(payload["verbose_summary_sha256"] == VERBOSE_SHA,
                f"s{index} verbose binding")
        comparison = payload["semantic_comparison"]
        require(comparison["ordinary_T_cells"] > 0, f"s{index} T branch")
        require(comparison["strict_open_cube_cells"] > 0,
                f"s{index} strict branch")
        relation = payload["normalized_relation_stream"]
        relation_path = PROJECT / relation["path"]
        require(sha(relation_path) == relation["file_sha256"],
                f"s{index} relation file hash")
        records, logical = logical_rows(relation_path)
        require(records == int(relation["records"]),
                f"s{index} relation count")
        require(logical == relation["sha256"],
                f"s{index} relation logical hash")
        local_bindings = set(); local_classes = Counter()
        local_body = Counter()
        with gzip.open(relation_path, "rt") as handle:
            for line in handle:
                row = json.loads(line)
                binding = str(row["verbose_binding_id"])
                require(binding not in local_bindings,
                        f"s{index} duplicate binding")
                local_bindings.add(binding)
                classification = row["classification"]
                require(classification in EXPECTED_COUNTS,
                        f"s{index} unexpected class")
                require(row["source_child_graph_id"] and
                        row["target_child_graph_id"],
                        f"s{index} missing directed graph relation")
                require(row["compact_evidence_id"] and
                        row["verbose_evidence_id"],
                        f"s{index} missing evidence binding")
                equal = bool(row["evidence_body_equal"])
                local_classes[classification] += 1
                local_body[(classification, equal)] += 1
                if classification == "strict_open_cube_separation":
                    require(row["compact_independent_sign_proof_sha256"] and
                            row["verbose_independent_sign_proof_sha256"],
                            f"s{index} missing strict proof")
                else:
                    require(row["compact_independent_sign_proof_sha256"] is None
                            and row["verbose_independent_sign_proof_sha256"] is None,
                            f"s{index} unexpected sign proof")
        require(len(local_bindings) == records, f"s{index} binding count")
        require(dict(sorted(local_classes.items())) == payload["counts"],
                f"s{index} relation class replay")
        require(not (all_bindings & local_bindings),
                "cross-shard binding duplicate")
        all_bindings.update(local_bindings)
        declared_body = Counter()
        for row in comparison["evidence_body_comparison"]:
            declared_body[(row["classification"],
                           bool(row["exact_body_equal"]))] += int(row["count"])
        require(local_body == declared_body,
                f"s{index} evidence-body comparison")
        counts.update(payload["counts"])
        stages.update(comparison["stage_counts"])
        body_comparison.update(local_body)
        total_graphs += int(comparison["unique_exact_rooted_graphs_audited"])
        total_descriptors += int(comparison["zero_sum_descriptors_regenerated"])
        total_pullbacks += int(comparison["exact_pullbacks_regenerated"])
        unique_sign_proof_counts.append(
            int(comparison["independent_strict_sign_proofs"]))
        shard_rows.append({
            "shard": f"s{index}", "summary_sha256": expected,
            "path_range": [start, stop], "certificate": normalized(path),
            "certificate_sha256": sha(path),
            "normalized_relation_stream": relation,
            "nonidentical_but_semantically_valid_evidence_selections":
                int(comparison[
                    "nonidentical_but_semantically_valid_evidence_selections"]),
        })
        cursor = stop

    require(cursor == 144, "incomplete path inventory")
    require(len(all_bindings) == 101148, "aggregate binding count")
    require(dict(sorted(counts.items())) == EXPECTED_COUNTS,
            "aggregate classification counts")
    require(dict(sorted(stages.items())) == EXPECTED_STAGES,
            "aggregate stage counts")
    unequal = Counter({classification: value
                       for (classification, equal), value
                       in body_comparison.items() if not equal})
    require(dict(unequal) == {"strict_open_cube_separation": 56},
            "unexpected evidence normalization differences")

    verbose_summary_path = (PROJECT / "primary/certificates/"
                            "probe_extension_schema3_n3_final_summary.json")
    require(sha(verbose_summary_path) == VERBOSE_SHA,
            "verbose summary hash")
    verbose_summary = json.loads(verbose_summary_path.read_text())
    require(int(verbose_summary["streams"]["bindings"]["records"]) == 101148,
            "verbose binding declaration")
    verbose_binding_path = PROJECT / verbose_summary["streams"]["bindings"]["path"]
    verbose_ids = set(); digest = hashlib.sha256(); verbose_count = 0
    with gzip.open(verbose_binding_path, "rb") as handle:
        for raw in handle:
            digest.update(raw); verbose_count += 1
            identifier = str(json.loads(raw)["probe_path_binding_id"])
            require(identifier not in verbose_ids,
                    "duplicate verbose binding")
            verbose_ids.add(identifier)
    require(verbose_count == 101148, "verbose binding count")
    require(digest.hexdigest() ==
            verbose_summary["streams"]["bindings"]["sha256"],
            "verbose logical binding hash")
    require(all_bindings == verbose_ids,
            "global compact/verbose binding bijection")

    mutation_path = CERT / "mutation_tests.json"
    merger_mutation_path = CERT / "merger_mutations.json"
    merge_path = CERT / "hardened_merge_manifest.json"
    adversarial_path = CERT / "adversarial_release_review.json"
    mismatch_path = (HERE / "history/sequential_first_failure/"
                     "FIRST_MISMATCH_CERTIFICATE.json")
    false_claim_path = (HERE / "history/sequential_first_failure/"
                        "LOSSLESS_WITNESS_BODY_CLAIM_FALSE.json")
    mutation = json.loads(mutation_path.read_text())
    merger_mutation = json.loads(merger_mutation_path.read_text())
    merge = json.loads(merge_path.read_text())
    adversarial = json.loads(adversarial_path.read_text())
    mismatch = json.loads(mismatch_path.read_text())
    false_claim = json.loads(false_claim_path.read_text())
    require(mutation["status"] == "VERIFIED", "semantic mutations")
    require(merger_mutation["status"] == "VERIFIED", "merger mutations")
    require(merge["status"] == "EXACTLY_VERIFIED", "hardened merger")
    require(merge["path_range"] == [0, 144], "merged range")
    require(merge["counts"] == EXPECTED_COUNTS, "merged counts")
    require(adversarial["status"] == "VERIFIED_AFTER_CORRECTION" and
            int(adversarial["relations"]) == 101148 and
            adversarial["global_verbose_binding_bijection"] is True,
            "adversarial release review")
    require(mismatch["status"] == "LOCALIZED" and
            mismatch["diagnosis"]
            ["exact_body_comparator_too_strict_for_semantic_equivalence"] is True,
            "first mismatch diagnosis")
    require(false_claim["status"] == "FALSE", "withdrawn lossless claim")
    require(false_claim["preserved_certificate_sha256"] == sha(mismatch_path),
            "withdrawn claim mismatch-certificate binding")

    implementation = {}
    for name in ("engine_n3.py", "audit_final_n3.py",
                 "reproduce_first_mismatch.py", "mutation_tests.py",
                 "merger_mutations.py", "adversarial_release_review.py",
                 "finalize_certificate.py"):
        path = HERE / name
        implementation[name] = sha(path)
    for name in ("engine.py", "audit_final_n4.py"):
        path = HERE.parent / "final_n4_cleanroom" / name
        implementation[f"committed_n4_dependency/{name}"] = sha(path)
    payload = {
        "schema": "compact-probe-final-n3-evidence-gate-v1",
        "status": "VERIFIED_AFTER_CORRECTION",
        "scope": (
            "Evidence-format gate for the final complement-normalized n=3 "
            "compact shards; not a global identifiability theorem."),
        "correction": (
            "The lossless selected-witness-body claim is FALSE. Record-level "
            "semantic equivalence instead requires exact graph relation, "
            "direction, insertion, class, and transport, plus independent "
            "validity of each package's selected witness."),
        "path_inventory_count": 144,
        "path_range": [0, 144],
        "total_relations": 101148,
        "classification_counts": EXPECTED_COUNTS,
        "stage_counts": EXPECTED_STAGES,
        "evidence_body_comparison": [
            {"classification": key[0], "exact_body_equal": key[1],
             "count": value}
            for key, value in sorted(body_comparison.items())
        ],
        "nonidentical_but_semantically_valid_evidence_selections": 56,
        "nonidentical_evidence_classes": {
            "strict_open_cube_separation": 56},
        "all_four_classification_branches_exercised": True,
        "ordinary_T_cells": 840,
        "strict_open_cube_cells": 624,
        "verbose_summary": normalized(verbose_summary_path),
        "verbose_summary_sha256": VERBOSE_SHA,
        "verbose_binding_stream_sha256": digest.hexdigest(),
        "global_verbose_binding_bijection": True,
        "aggregate_regeneration_work": {
            "per_shard_unique_graph_audits_sum": total_graphs,
            "per_shard_descriptor_regenerations_sum": total_descriptors,
            "per_shard_pullback_regenerations_sum": total_pullbacks,
            "unique_strict_sign_proofs_by_shard": unique_sign_proof_counts,
        },
        "shards": shard_rows,
        "hardened_merge_manifest": normalized(merge_path),
        "hardened_merge_manifest_sha256": sha(merge_path),
        "semantic_mutation_certificate": normalized(mutation_path),
        "semantic_mutation_certificate_sha256": sha(mutation_path),
        "merger_mutation_certificate": normalized(merger_mutation_path),
        "merger_mutation_certificate_sha256": sha(merger_mutation_path),
        "adversarial_release_review": normalized(adversarial_path),
        "adversarial_release_review_sha256": sha(adversarial_path),
        "first_mismatch_certificate": normalized(mismatch_path),
        "first_mismatch_certificate_sha256": sha(mismatch_path),
        "withdrawn_lossless_claim": normalized(false_claim_path),
        "withdrawn_lossless_claim_sha256": sha(false_claim_path),
        "independent_implementation_sha256": implementation,
        "limitations": [
            "This gate certifies the evidence format and exact n=3 family only.",
            "It does not by itself certify the landmark global identifiability theorem.",
            "Compact and verbose selected witness identities are not lossless: 56 strict relations select distinct valid witnesses.",
            "All path, graph, direction, insertion, classification, and unique transport semantics agree exactly.",
        ],
    }
    output = CERT / "final_gate_certificate.json"
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"], "relations": payload["total_relations"],
        "counts": payload["classification_counts"],
        "alternate_valid_witness_selections": 56,
        "output": normalized(output), "output_sha256": sha(output),
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FALSE", "error": str(exc)},
                         sort_keys=True), file=sys.stderr)
        raise
