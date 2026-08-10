#!/usr/bin/env python3
"""Independent release-layer adversarial check for the n=3 audit.

This program imports no review decoder or primary module.  It independently
checks the locked summaries, normalized relation streams, global verbose
binding bijection, class/evidence normalization counts, implementation import
surface, mutation certificates, and preserved FALSE claim.
"""

from __future__ import annotations

import ast
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
CERT = HERE / "certificates"
SUMMARY_SHA = [
    "dc7b806f9afc1af9909682f47ea4bdc9ac5a8631d78ce3a6b15d41c4f171ad73",
    "996084af49c3e4ddf63b62cfa951be652a886e3424674f6e34d664b5a4901a37",
    "a8162d2bb136668ce2f204ce2012c85eb4dbb5e42c7037307d974b5f9ebf2286",
    "b246614dafc669784f8ef5e16ef62db79f08929b2afc2a6d14ce7f50bd7b7942",
]
VERBOSE_SHA = "c8aa65474844276bc4d123152c6fd1b85276a38ee410ef61a4a64488f7886108"
EXPECTED = Counter({
    "generic_polynomial_separation": 90008,
    "labelled_isomorphism": 9676,
    "ordinary_T": 840,
    "strict_open_cube_separation": 624,
})


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def relative(path):
    return str(path.resolve().relative_to(PROJECT))


def forbidden_imports(path):
    tree = ast.parse(path.read_text(), filename=str(path))
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            bad.extend(alias.name for alias in node.names
                       if alias.name == "primary" or
                       alias.name.startswith("primary."))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module == "primary" or module.startswith("primary."):
                bad.append(module)
    return bad


def main():
    relation_ids = set(); relation_keys = set(); counts = Counter()
    evidence = Counter(); cursor = 0; shard_rows = []
    for index, expected_sha in enumerate(SUMMARY_SHA):
        summary_path = (PROJECT / "primary/certificates" /
                        f"compact_probe_schema3_n3_compact_s{index}_summary.json")
        require(sha(summary_path) == expected_sha, f"s{index} summary hash")
        certificate_path = CERT / f"independent_s{index}.json"
        certificate = json.loads(certificate_path.read_text())
        require(certificate["status"] == "VERIFIED", f"s{index} status")
        require(certificate["summary_sha256"] == expected_sha,
                f"s{index} summary binding")
        start, stop = map(int, certificate["path_range"])
        require(start == cursor, f"s{index} gap/overlap")
        relation = certificate["normalized_relation_stream"]
        relation_path = PROJECT / relation["path"]
        require(sha(relation_path) == relation["file_sha256"],
                f"s{index} relation file hash")
        logical = hashlib.sha256(); local = 0
        local_counts = Counter(); local_evidence = Counter()
        with gzip.open(relation_path, "rb") as handle:
            for raw in handle:
                logical.update(raw); local += 1
                row = json.loads(raw)
                binding = str(row["verbose_binding_id"])
                require(binding not in relation_ids,
                        "duplicate global verbose binding")
                relation_ids.add(binding)
                key = (
                    int(row["path_index"]), row["stage"],
                    row.get("flat_index"), row.get("parent_p_flat_index"),
                    row.get("local_flat_index"),
                )
                require(key not in relation_keys, "duplicate relation index")
                relation_keys.add(key)
                classification = row["classification"]
                require(classification in EXPECTED, "unknown classification")
                require(row["source_child_graph_id"] !=
                        row["target_child_graph_id"] or
                        classification in EXPECTED,
                        "malformed graph relation")
                require(bool(row["compact_evidence_id"]) and
                        bool(row["verbose_evidence_id"]),
                        "missing evidence identifiers")
                equal = bool(row["evidence_body_equal"])
                local_counts[classification] += 1
                local_evidence[(classification, equal)] += 1
                if not equal:
                    require(classification == "strict_open_cube_separation",
                            "non-strict evidence mismatch")
                if classification == "strict_open_cube_separation":
                    require(row["compact_independent_sign_proof_sha256"] and
                            row["verbose_independent_sign_proof_sha256"],
                            "missing strict sign proof")
        require(local == int(relation["records"]), f"s{index} relation count")
        require(logical.hexdigest() == relation["sha256"],
                f"s{index} logical relation hash")
        require(dict(sorted(local_counts.items())) == certificate["counts"],
                f"s{index} class count")
        declared = Counter()
        for row in (certificate["semantic_comparison"]
                    ["evidence_body_comparison"]):
            declared[(row["classification"],
                      bool(row["exact_body_equal"]))] += int(row["count"])
        require(declared == local_evidence,
                f"s{index} evidence normalization")
        counts.update(local_counts); evidence.update(local_evidence)
        shard_rows.append({
            "shard": f"s{index}", "path_range": [start, stop],
            "summary_sha256": expected_sha,
            "independent_certificate_sha256": sha(certificate_path),
            "relation_file_sha256": sha(relation_path),
            "relations": local,
        })
        cursor = stop
    require(cursor == 144, "path coverage")
    require(counts == EXPECTED, "aggregate counts")
    require(evidence[("strict_open_cube_separation", False)] == 56,
            "alternate strict witness count")
    require(sum(value for (classification, equal), value in evidence.items()
                if not equal) == 56, "unexpected evidence differences")

    verbose_summary_path = (PROJECT / "primary/certificates/"
                            "probe_extension_schema3_n3_final_summary.json")
    require(sha(verbose_summary_path) == VERBOSE_SHA, "verbose summary hash")
    verbose = json.loads(verbose_summary_path.read_text())
    binding_path = PROJECT / verbose["streams"]["bindings"]["path"]
    verbose_ids = set(); logical = hashlib.sha256(); records = 0
    with gzip.open(binding_path, "rb") as handle:
        for raw in handle:
            logical.update(raw); records += 1
            identifier = str(json.loads(raw)["probe_path_binding_id"])
            require(identifier not in verbose_ids,
                    "duplicate verbose binding stream ID")
            verbose_ids.add(identifier)
    require(records == 101148, "verbose count")
    require(logical.hexdigest() ==
            verbose["streams"]["bindings"]["sha256"],
            "verbose logical hash")
    require(relation_ids == verbose_ids, "global relation/binding bijection")

    implementation_paths = [
        HERE / "engine_n3.py", HERE / "audit_final_n3.py",
        HERE.parent / "final_n4_cleanroom/engine.py",
        HERE.parent / "final_n4_cleanroom/audit_final_n4.py",
    ]
    import_audit = {relative(path): forbidden_imports(path)
                    for path in implementation_paths}
    require(not any(import_audit.values()), "primary module import detected")

    mutation_path = CERT / "mutation_tests.json"
    merger_mutation_path = CERT / "merger_mutations.json"
    mismatch_path = (HERE / "history/sequential_first_failure/"
                     "FIRST_MISMATCH_CERTIFICATE.json")
    false_path = (HERE / "history/sequential_first_failure/"
                  "LOSSLESS_WITNESS_BODY_CLAIM_FALSE.json")
    require(json.loads(mutation_path.read_text())["status"] == "VERIFIED",
            "semantic mutations")
    require(json.loads(merger_mutation_path.read_text())["status"] ==
            "VERIFIED", "merger mutations")
    mismatch = json.loads(mismatch_path.read_text())
    false_claim = json.loads(false_path.read_text())
    require(mismatch["status"] == "LOCALIZED", "mismatch localization")
    require(false_claim["status"] == "FALSE", "false claim status")
    require(false_claim["preserved_certificate_sha256"] == sha(mismatch_path),
            "false-claim certificate binding")

    payload = {
        "schema": "compact-probe-final-n3-adversarial-release-review-v1",
        "status": "VERIFIED_AFTER_CORRECTION",
        "scope": "Independent release-layer audit; no decoder imports.",
        "path_range": [0, 144],
        "relations": len(relation_ids),
        "classification_counts": dict(sorted(counts.items())),
        "nonidentical_valid_strict_witness_selections": 56,
        "global_verbose_binding_bijection": True,
        "forbidden_primary_import_audit": import_audit,
        "shards": shard_rows,
        "mutation_certificate_sha256": sha(mutation_path),
        "merger_mutation_certificate_sha256": sha(merger_mutation_path),
        "first_mismatch_certificate_sha256": sha(mismatch_path),
        "withdrawn_lossless_claim_sha256": sha(false_path),
        "implementation": relative(Path(__file__)),
        "implementation_sha256": sha(Path(__file__)),
        "limitation": (
            "This is an adversarial release-layer cross-check of the full "
            "clean-room semantic certificates, not a second graph/Fourier "
            "engine and not a global theorem certificate."),
    }
    output = CERT / "adversarial_release_review.json"
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"], "relations": payload["relations"],
        "output": relative(output), "output_sha256": sha(output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
