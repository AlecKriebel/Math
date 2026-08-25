#!/usr/bin/env python3
"""Independent cross-artifact binding checks for the submitted referee package.

This intentionally does not import any submitted module or reuse its checker.
It compares bytes and declared relationships directly from the sealed files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_payload_hash(obj: dict) -> str:
    payload = dict(obj)
    payload.pop("payload_sha256", None)
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(raw)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object: {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()

    rels = {
        "manifest": "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json",
        "crosswalk": "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json",
        "pdf_report": "proof_compression_submission/PDF_BUILD_REPORT.json",
        "static_audit": "proof_compression_submission/adversarial_review/STATIC_AUDIT_RESULT.json",
        "full_report": "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json",
        "telemetry": "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json",
        "release_lock": "work/final_theorem_release/RELEASE_LOCK.json",
    }
    docs = {name: load_json(project / rel) for name, rel in rels.items()}
    checks: list[dict] = []

    def check(name: str, condition: bool, detail: object) -> None:
        checks.append({"name": name, "pass": bool(condition), "detail": detail})

    for name in ("manifest", "crosswalk", "pdf_report", "static_audit", "release_lock"):
        actual = canonical_payload_hash(docs[name])
        expected = docs[name].get("payload_sha256")
        check(f"canonical_payload:{name}", actual == expected, {"actual": actual, "expected": expected})

    manifest = docs["manifest"]
    frozen = manifest["frozen_evidence"]["files"]
    submission = manifest["submission_sources"]["files"]
    declared = {**frozen, **submission}
    check("manifest_disjoint_layers", not (set(frozen) & set(submission)), sorted(set(frozen) & set(submission)))
    manifest_mismatches = []
    for rel, row in declared.items():
        path = project / rel
        actual = {"bytes": path.stat().st_size, "sha256": sha256_file(path)} if path.is_file() else None
        expected = {"bytes": row["bytes"], "sha256": row["sha256"]}
        if actual != expected:
            manifest_mismatches.append({"path": rel, "expected": expected, "actual": actual})
    check("all_479_manifest_rows_match_disk", not manifest_mismatches, manifest_mismatches)

    crosswalk = docs["crosswalk"]
    references = []
    schema_mismatches = []
    binding_mismatches = []
    for claim in crosswalk["claims"]:
        for field in ("authoritative_artifacts", "producer_artifacts", "replay_artifacts", "mutation_artifacts"):
            for row in claim[field]:
                rel = row["path"]
                references.append((claim["claim_id"], field, rel))
                expected_layer = frozen if row["frozen"] else submission
                bound = expected_layer.get(rel)
                if bound != {"bytes": row["bytes"], "sha256": row["sha256"]}:
                    binding_mismatches.append(
                        {"claim": claim["claim_id"], "field": field, "path": rel, "crosswalk": row, "manifest": bound}
                    )
                if row.get("declared_schema"):
                    value = load_json(project / rel)
                    if value.get("schema") != row["declared_schema"]:
                        schema_mismatches.append(
                            {"path": rel, "expected": row["declared_schema"], "actual": value.get("schema")}
                        )
    check("crosswalk_13_claims", len(crosswalk["claims"]) == 13, len(crosswalk["claims"]))
    check("crosswalk_all_artifacts_bound_to_correct_ledger", not binding_mismatches, binding_mismatches)
    check("crosswalk_declared_json_schemas", not schema_mismatches, schema_mismatches)

    telemetry = docs["telemetry"]
    full = docs["full_report"]
    lock = docs["release_lock"]
    runtime = manifest["runtime_boundary"]
    report_rel = telemetry["report"]["path"]
    lock_rel = telemetry["release_lock"]["path"]
    check(
        "telemetry_report_bytes_and_semantics",
        sha256_file(project / report_rel) == telemetry["report"]["sha256"]
        and full["status"] == telemetry["status"] == "PASS"
        and full["mode"] == "full"
        and not full["optimized_mode"]
        and len(full["layer_replays"]) == telemetry["report"]["layer_count"] == 40
        and full["elapsed_seconds"] == telemetry["report"]["internal_elapsed_seconds"],
        {
            "report_sha256": sha256_file(project / report_rel),
            "layer_count": len(full["layer_replays"]),
            "elapsed_seconds": full["elapsed_seconds"],
        },
    )
    layer_names = [row["name"] for row in full["layer_replays"]]
    bad_layer_rows = [
        row
        for row in full["layer_replays"]
        if row["status"] != "PASS"
        or not (
            row.get("returncode") == 0
            or (isinstance(row.get("observed_nonzero_returncode"), int) and row["observed_nonzero_returncode"] != 0)
        )
    ]
    check(
        "stored_full_replay_layer_rows",
        len(layer_names) == len(set(layer_names)) == 40
        and not bad_layer_rows,
        {"unique_names": len(set(layer_names)), "nonpass_or_bad_exit": bad_layer_rows},
    )
    check(
        "telemetry_release_lock_bytes_and_payload",
        sha256_file(project / lock_rel) == telemetry["release_lock"]["sha256"]
        and (project / lock_rel).stat().st_size == telemetry["release_lock"]["bytes"]
        and lock["payload_sha256"] == telemetry["release_lock"]["payload_sha256"]
        and full["lock_payload_sha256"] == lock["payload_sha256"],
        {
            "lock_sha256": sha256_file(project / lock_rel),
            "lock_payload_sha256": lock["payload_sha256"],
        },
    )
    check(
        "manifest_runtime_boundary_matches_telemetry",
        runtime["report_sha256"] == telemetry["report"]["sha256"]
        and runtime["telemetry_sha256"] == sha256_file(project / rels["telemetry"])
        and runtime["git_commit"] == telemetry["git_commit"]
        and runtime["end_to_end_full_runtime_seconds"] == telemetry["time_l"]["real_seconds"]
        and runtime["maximum_resident_set_size_bytes"] == telemetry["time_l"]["maximum_resident_set_size_bytes"]
        and runtime["peak_memory_footprint_bytes"] == telemetry["time_l"]["peak_memory_footprint_bytes"],
        runtime,
    )

    source_mismatches = []
    static_sources = docs["static_audit"]["source_sha256"]
    for rel, row in telemetry["submission_sources"].items():
        path = project / rel
        actual = {"bytes": path.stat().st_size, "sha256": sha256_file(path)}
        static_key = rel.removeprefix("proof_compression_submission/")
        static_hash = static_sources.get(static_key)
        if actual != row or static_hash != row["sha256"]:
            source_mismatches.append(
                {"path": rel, "telemetry": row, "actual": actual, "static_audit_sha256": static_hash}
            )
    check("five_sources_match_telemetry_and_static_audit", not source_mismatches, source_mismatches)

    pdf = docs["pdf_report"]
    pdf_mismatches = []
    for label in ("article", "supplement"):
        row = pdf[label]
        pdf_path = project / row["pdf_path"]
        source_path = project / row["source_path"]
        log_path = project / f"proof_compression_submission/output/logs/{label}.log"
        actual = {
            "pdf_sha256": sha256_file(pdf_path),
            "bytes": pdf_path.stat().st_size,
            "source_sha256": sha256_file(source_path),
            "log_sha256": sha256_file(log_path),
        }
        expected = {key: row[key] for key in actual}
        if actual != expected:
            pdf_mismatches.append({"document": label, "expected": expected, "actual": actual})
    check("pdf_report_source_pdf_log_bytes", not pdf_mismatches, pdf_mismatches)
    source_set = {f"proof_compression_submission/{rel}" for rel in pdf["source_set"]}
    check(
        "pdf_report_exact_five_sources",
        source_set == set(telemetry["submission_sources"]),
        {"pdf_report": sorted(source_set), "telemetry": sorted(telemetry["submission_sources"])},
    )
    article_tex = (project / "proof_compression_submission/article/main.tex").read_text(encoding="utf-8")
    supplement_tex = (project / "proof_compression_submission/supplement/supplement.tex").read_text(encoding="utf-8")
    check("article_bibliography_is_literal_input", "\\bibliography{references}" in article_tex, None)
    check(
        "supplement_generated_inputs_are_literal",
        "\\input{compression_tables.tex}" in supplement_tex and "\\input{certificate_appendix.tex}" in supplement_tex,
        None,
    )

    key_hashes = {
        name: {"path": rel, "bytes": (project / rel).stat().st_size, "sha256": sha256_file(project / rel)}
        for name, rel in rels.items()
    }
    result = {
        "schema": "independent-k2p-artifact-consistency-audit-v1",
        "status": "PASS" if all(row["pass"] for row in checks) else "FAIL",
        "project": str(project),
        "checks": checks,
        "summary": {
            "check_count": len(checks),
            "failed": [row["name"] for row in checks if not row["pass"]],
            "crosswalk_artifact_references": len(references),
            "manifest_declared_files": len(declared),
        },
        "key_artifacts": key_hashes,
    }
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], **result["summary"]}, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
