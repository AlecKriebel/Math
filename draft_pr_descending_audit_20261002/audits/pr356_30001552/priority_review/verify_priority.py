#!/usr/bin/env python3
"""Read-only evidence/inventory verification, without mathematical comparison loops."""
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
VERSION = 2
GATE_SHA = "a39f2c1a81d3194f645976fbe09fbbedb0ebc030ee561fe6b3b5842dd03489f8"
BASELINE_SHA = "bd440890c348616ba7afbf378ca550d1f7dd9fe4b733d074a7cf320c8d02899a"
PRIVATE_DIRS = {"sources_private", "metadata_private", "search_private", "verification_private"}
PUBLIC_MANIFEST = "PUBLIC_MANIFEST.json"
PRIVATE_MANIFEST = "verification_private/PRIVATE_MANIFEST.json"
NATIVE_DIR = "verification_private/integrity_runs"
NATIVE_PATHS = {f"{NATIVE_DIR}/{mode}.{suffix}" for mode in ("full", "public")
                for suffix in ("stdout", "stderr", "receipt.json")}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((BASE / name).read_text())


def check_binding(name, expected):
    relative = Path(name)
    assert not relative.is_absolute() and ".." not in relative.parts, name
    path = BASE / relative
    assert path.is_file() and not path.is_symlink(), name
    assert path.stat().st_size == expected["bytes"], name
    assert digest(path) == expected["sha256"], name


def actual_files():
    return {str(p.relative_to(BASE)) for p in BASE.rglob("*") if p.is_file()}


def comparison_evidence():
    pins = read("comparison_preexecution_pins.json")
    assert set(pins["files"]) == {"comparison_check.py", "mechanism_comparison.md"}
    for name, binding in pins["files"].items():
        check_binding(name, binding)
    receipt = read("comparison_receipt.json")
    assert receipt["exit_code"] == 0
    assert receipt["checker_sha256"] == digest(BASE / "comparison_check.py")
    assert receipt["preexecution_pins_sha256"] == digest(BASE / "comparison_preexecution_pins.json")
    assert datetime.fromisoformat(pins["created_utc"]) <= datetime.fromisoformat(receipt["started_utc"])
    assert receipt["checker_changed_priority_tree"] is False
    for stream in receipt["native_streams"].values():
        check_binding(stream["path"], stream)
    assert (BASE / "comparison.stderr").read_bytes() == b""
    saved = read("comparison.stdout")
    assert saved == receipt["result"] and saved["status"] == "PASS"
    assert saved["comparison_checks"] == {
        "words_permutations": 13116,
        "period_equivalences_each": 85296,
        "numeric_prior_bound_substitutions": 2500,
        "uniform_sharpness_witness": "abb; reversal; p=2,q=3"}
    return saved["comparison_checks"]


def verify_private_comparison():
    receipt = read("verification_private/comparison_receipt_private.json")
    public = read("comparison_receipt.json")
    assert receipt["result"] == public["result"]
    assert receipt["native_streams"] == public["native_streams"]
    assert receipt["tree_before"] == receipt["tree_after"]
    for key in ("orchestrator", "private_preexecution", "public_receipt"):
        item = receipt[key]
        check_binding(item["path"], item)
    pre = read(receipt["private_preexecution"]["path"])
    assert pre["checker"] == read("comparison_preexecution_pins.json")["files"]["comparison_check.py"]
    assert pre["public_pins"]["sha256"] == digest(BASE / "comparison_preexecution_pins.json")
    assert pre["orchestrator"]["sha256"] == receipt["orchestrator"]["sha256"]
    source_readbacks = 0
    for name, binding in pre["tree_before"].items():
        if Path(name).parts[0] in {"sources_private", "metadata_private", "search_private"}:
            check_binding(name, binding)
            source_readbacks += 1
    historical = read("verification_private/historical_v1/preservation_index.json")
    assert len(historical["files"]) == 8
    for item in historical["files"]:
        check_binding(item["preserved_path"], item)
        if item["original_path"] == "verify_priority.py":
            assert pre["tree_before"]["verify_priority.py"]["sha256"] == item["sha256"]
    return source_readbacks


def native_integrity_receipts():
    count = 0
    for mode in ("full", "public"):
        name = f"{NATIVE_DIR}/{mode}.receipt.json"
        if not (BASE / name).exists():
            continue
        receipt = read(name)
        assert receipt["exit_code"] == 0
        assert receipt["verifier_changed_priority_tree"] is False
        assert receipt["verifier_version"] == VERSION
        assert receipt["tree_before"] == receipt["tree_after"]
        for path, binding in receipt["tree_before"].items():
            if path not in NATIVE_PATHS:
                check_binding(path, binding)
        for item in receipt["preexecution_inputs"].values():
            check_binding(item["path"], item)
        for item in receipt["native_streams"].values():
            check_binding(item["path"], item)
        assert receipt["verifier_sha256"] == digest(BASE / "verify_priority.py")
        assert receipt["orchestrator_sha256"] == digest(BASE / "verification_private/run_integrity.py")
        stdout_path = receipt["native_streams"]["stdout"]["path"]
        result = read(stdout_path)
        assert result == receipt["result"] and result["status"] == "PASS"
        assert result["comparison_execution_replayed"] is False
        assert (BASE / receipt["native_streams"]["stderr"]["path"]).read_bytes() == b""
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-only", action="store_true",
                        help="Require the exact curated public inventory; omit all private provenance.")
    parser.add_argument("--include-external", action="store_true",
                        help="Also read the pinned candidate16 files and root original PDF.")
    args = parser.parse_args()
    assert not (args.public_only and args.include_external), "External bindings are outside public-only scope"
    assert digest(BASE / "source_first_gate.json") == GATE_SHA
    assert digest(BASE / "source_first_baseline.md") == BASELINE_SHA
    gate, release = read("source_first_gate.json"), read("candidate_release.json")
    assert gate["candidate_or_previous_priority_material_seen"] is False
    assert gate["candidate_release_received"] is False
    assert release["source_gate_sha256"] == GATE_SHA
    assert datetime.fromisoformat(gate["created_utc"]) < datetime.fromisoformat(release["candidate_release_received_utc"])
    assert gate["baseline_sha256"] == BASELINE_SHA
    queries = [json.loads(line) for line in (BASE / "query_log.jsonl").read_text().splitlines()]
    assert len(queries) == 53 and all(q.get("query") and q.get("recorded_utc") for q in queries)
    public = read(PUBLIC_MANIFEST)
    assert set(public["excluded_private_directories"]) == PRIVATE_DIRS
    public_expected = set(public["files"]) | {PUBLIC_MANIFEST}
    all_files = actual_files()
    public_actual = {name for name in all_files if Path(name).parts[0] not in PRIVATE_DIRS and name != "CLOSURE.json"}
    assert public_actual == public_expected, "Curated public inventory differs from actual public files"
    assert set(read("AUDIT_PLAN.json")["public_artifacts"]) == public_expected
    for name, binding in public["files"].items():
        assert Path(name).parts[0] not in PRIVATE_DIRS
        check_binding(name, binding)
    comparisons = comparison_evidence()
    source_checks = external_checks = receipt_checks = private_checks = source_readbacks = native_receipts = 0
    if not args.public_only:
        private = read(PRIVATE_MANIFEST)
        private_actual = {name for name in all_files if Path(name).parts[0] in PRIVATE_DIRS}
        static_expected = set(private["files"]) | {PRIVATE_MANIFEST}
        assert set(private["terminal_native_paths"]) == NATIVE_PATHS
        extras = private_actual - static_expected
        assert static_expected <= private_actual and extras <= NATIVE_PATHS, "Private inventory differs from actual files"
        for name, binding in private["files"].items():
            assert Path(name).parts[0] in PRIVATE_DIRS
            check_binding(name, binding)
            private_checks += 1
        assert digest(BASE / "sources_private/official_nowotka_bischoff_2010_pages25-28.txt") == gate["private_extract_sha256"]
        inventory = read("sources_private/inspection_inventory.json")
        assert len(inventory["entries"]) == 17
        for artifact in inventory["raw_private_artifact_inventory"]:
            check_binding(artifact["file"], artifact)
            source_checks += 1
        recent = read("metadata_private/verified_recent_records.json")
        assert len(recent["records"]) == 3
        for record in recent["records"]:
            assert record["state"] == "published"
            assert record["doi"] == "10.5281/zenodo." + record["record_id"]
            for receipt in record["receipts"].values():
                assert digest(BASE / receipt["path"]) == receipt["sha256"]
                receipt_checks += 1
        releases = read("metadata_private/github_release_metadata.json")
        assert len(releases) == 28 and all(not r["isDraft"] and not r["isPrerelease"] for r in releases)
        assert recent["matching_record_ids"] == []
        source_readbacks = verify_private_comparison()
        native_receipts = native_integrity_receipts()
    if args.include_external:
        root = Path(gate["original_source"]["path"])
        assert digest(root) == gate["original_source"]["sha256"]
        external_checks += 1
        pins = read("candidate_pins.json")
        candidate = Path(pins["candidate_root"])
        assert len(pins["files"]) == 16
        actual = {str(p.relative_to(candidate)) for p in candidate.rglob("*") if p.is_file()}
        assert actual == set(pins["files"])
        for name, expected in pins["files"].items():
            path = candidate / name
            assert path.stat().st_size == expected["bytes"] and digest(path) == expected["sha256"]
            external_checks += 1
    closure = BASE / "CLOSURE.json"
    closure_checks = 0
    if closure.exists():
        sealed = read("CLOSURE.json")
        assert sealed["root_approval_received"] is True
        assert sealed["public_manifest_sha256"] == digest(BASE / PUBLIC_MANIFEST)
        closure_public = {name for name in sealed["files"] if Path(name).parts[0] not in PRIVATE_DIRS}
        assert closure_public == public_expected
        if not args.public_only:
            assert sealed["private_manifest_sha256"] == digest(BASE / PRIVATE_MANIFEST)
            assert all_files - {"CLOSURE.json"} == set(sealed["files"])
            assert NATIVE_PATHS <= all_files and native_receipts == 2
        for name, binding in sealed["files"].items():
            if args.public_only and Path(name).parts[0] in PRIVATE_DIRS:
                continue
            check_binding(name, binding)
            closure_checks += 1
    print(json.dumps({"status": "PASS", "verifier_version": VERSION,
                      "scope": "Read-only file inventory and saved evidence integrity; no mathematical comparison loops, global priority certificate, or universal proof certification",
                      "source_first_gate": "PASS", "query_rows": len(queries),
                      "public_inventory_files": len(public_expected),
                      "private_inventory_files": private_checks,
                      "private_source_artifacts": source_checks,
                      "published_metadata_receipts": receipt_checks,
                      "comparison_source_readbacks": source_readbacks,
                      "native_integrity_receipts": native_receipts,
                      "external_bindings": external_checks,
                      "closure_state": "sealed" if closure.exists() else "awaiting root authorization",
                      "closure_files_checked": closure_checks,
                      "comparison_execution_replayed": False,
                      "saved_comparison_checks": comparisons,
                      "public_provenance_omissions": ["Raw source PDFs, extracts, renders and access captures", "Native search response payloads and publication-status metadata receipts", "Private orchestration code, full-tree execution inventories and final native integrity captures", "External original-source and candidate-file readbacks"] if args.public_only else []}, indent=2))


if __name__ == "__main__":
    main()
