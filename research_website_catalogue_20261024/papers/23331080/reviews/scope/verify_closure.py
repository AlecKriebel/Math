#!/usr/bin/env python3
"""Read-only packet/custody closure; stdout only, no scientific campaign.

Checks all original bytes, all40 ZIP payloads and complete native copies;
reuses bound fresh support outputs; reruns only own small exact verifier.
Can run once before FINAL_SEAL creation, then verifies the seal on later runs.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile
import zlib

OWN = Path(__file__).resolve().parent
PAPER = OWN.parent.parent
SOURCES = PAPER / "sources"
EXCLUSIONS = {"OWNED_MANIFEST.json", "FINAL_SEAL.json", "CLOSURE_RESULTS.json"}


def read_json(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def check_file(path, n, h):
    require(path.is_file() and not path.is_symlink(), "Missing/nonregular file: "+str(path))
    require(path.stat().st_size == n and sha(path) == h, "Byte mismatch: "+str(path))


manifest_path = OWN / "OWNED_MANIFEST.json"
manifest = read_json(manifest_path)
actual_owned = {str(f.relative_to(OWN)) for f in OWN.rglob("*") if f.is_file() and str(f.relative_to(OWN)) not in EXCLUSIONS}
expected_owned = {r["relative_path"] for r in manifest["files"]}
require(actual_owned == expected_owned, "Owned file inventory mismatch")
for item in manifest["files"]:
    check_file(OWN/item["relative_path"], item["bytes"], item["sha256"])

inputs = read_json(OWN/"INPUT_MANIFEST.json")
require(len(inputs["input_files"]) == 51, "Unexpected native source count")
actual_sources = {str(f) for f in SOURCES.rglob("*") if f.is_file()}
expected_sources = {r["absolute_path"] for r in inputs["input_files"]}
require(actual_sources == expected_sources, "Native source inventory mismatch")
for item in inputs["input_files"]:
    check_file(Path(item["absolute_path"]), item["bytes"], item["sha256"])
require(sha(SOURCES/"SOURCE_READY_MANIFEST.json") == "116c685e1dcfcc58e8b96c92f93174633106ff690323ac5af512a7c804618381", "Original acquisition manifest mismatch")
require(sha(SOURCES/"SOURCE_READY_SEAL.json") == "04aeb3a92833a1888c083f27788f96bcbb8d9da37e414a42a0ac7ebf3a3a02ac", "Original acquisition seal mismatch")
original_manifest = read_json(SOURCES/"SOURCE_READY_MANIFEST.json")
for item in original_manifest["files"]:
    check_file(Path(item["path"]), item["bytes"], item["sha256"])
for native_copy in (OWN/"native_objects").iterdir():
    require(native_copy.read_bytes() == (SOURCES/native_copy.name).read_bytes(), "Native copy was transformed")
    read_json(native_copy)

archive = read_json(SOURCES/"archive-members.json")
members = archive["members"]
require(len(members) == 40, "Unexpected archive payload count")
with zipfile.ZipFile(SOURCES/"verification_package.zip") as z:
    require(z.testzip() is None, "ZIP CRC failure")
    infos = z.infolist()
    require(len(infos) == 40, "ZIP inventory count changed")
    for item in members:
        zi = infos[item["ordinal_zero_based"]]
        require(zi.filename == item["original_member_name"], "Native ZIP order/name mismatch")
        require(zi.file_size == item["bytes"] and zi.compress_size == item["compressed_bytes"], "Native ZIP size mismatch")
        require(zi.flag_bits == item["zip_flags"] and zi.external_attr == item["native_external_attr"], "Native ZIP attributes mismatch")
        body = z.read(zi)
        require(format(zi.CRC, "08x") == item["CRC32"] == format(zlib.crc32(body)&0xffffffff, "08x"), "Native ZIP CRC mismatch")
        require(hashlib.sha256(body).hexdigest() == item["sha256"], "ZIP body SHA-256 mismatch")
        require(body == Path(item["extracted_path"]).read_bytes(), "Immutable extracted payload mismatch")

initial = read_json(OWN/"INITIAL_SEAL.json")
require(sha(OWN/"INITIAL_SEAL.json") == "1efb2c65967ba22501510552befaa49ed59617ffc5708facb32f28ec3564e125", "Initial seal changed")
require(sha(OWN/"INITIAL_RECONSTRUCTION.md") == initial["initial_reconstruction_sha256"], "Initial reconstruction changed")
require(initial["foreign_primary_code_results_reviews_opinions_before_seal"] is False, "Initial independence field changed")

binding = read_json(OWN/"replay/PROGRAM_COPY_BINDINGS.json")
require(len(binding["bindings"]) == 4, "Unexpected support copy count")
for item in binding["bindings"]:
    check_file(OWN/item["copy"], item["bytes"], item["sha256"])
    check_file(Path(item["source"]), item["bytes"], item["sha256"])
summary = read_json(OWN/"SUPPLIED_REPLAY_SUMMARY.json")
counts = []
for item in summary["fresh_bounded_owned_copy_replays"]:
    name = item["program"]
    stdout = OWN/"replay"/(name+".stdout.json")
    stderr = OWN/"replay"/(name+".stderr.txt")
    receipt_file = OWN/"replay"/(name+".receipt.json")
    receipt = read_json(receipt_file)
    require(sha(stdout) == item["fresh_stdout_sha256"] == receipt["stdout_sha256"], "Fresh support stdout mismatch")
    require(sha(receipt_file) == item["receipt_sha256"] and sha(stderr) == receipt["stderr_sha256"], "Fresh support receipt mismatch")
    require(receipt["exit_code"] == 0 and receipt["python_optimization"] is False, "Invalid support execution")
    result = read_json(stdout)
    status = result.get("status", result.get("verdict", ""))
    require(status.startswith("PASS") or status == "all exact algebraic checks passed", "Support check did not pass")
    counts.append(item["checks"])
require(counts == [40, 43, 17, 57], "Support check counts changed")

exact = read_json(OWN/"EXACT_RESULTS.json")
exact_receipt = read_json(OWN/"EXACT_RUN_RECEIPT.json")
require(sha(OWN/"EXACT_RESULTS.json") == exact_receipt["stdout_sha256"], "Own result/receipt mismatch")
python = Path("/Users/alec/Documents/Math/.venv/bin/python")
require(python.is_file(), "Recorded existing SymPy environment unavailable")
result = subprocess.run([str(python), "-B", str(OWN/"verify_exact.py")], cwd=OWN,
                        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                        text=True, capture_output=True, timeout=30, check=True)
require(json.loads(result.stdout) == exact, "Own exact verifier disagrees with bound results")
require(exact["exact_checks"] == 49 and exact["negative_controls_rejected"] == 7, "Own diagnostic coverage changed")
verdict = read_json(OWN/"VERDICT.json")
require(verdict["literal_custom_verdict"] == "PASS_FULL_STATED_COUNTEREXAMPLE_AT_DECLARED_PROBABILITY_FLOW_WITH_EXPLICIT_CLASSICAL_INPUT_CONVENTION_AND_PRIORITY_LIMITS", "Literal custom verdict changed")
require(verdict["full_original_claim_supported"] is True and verdict["priority"]["firstness_certified"] is False, "Scope/priority fields changed")
require(verdict["public_adoption_or_release_authority"] is False, "No publication authority exists")

seal_path = OWN/"FINAL_SEAL.json"
if seal_path.exists():
    seal = read_json(seal_path)
    require(seal["owned_manifest_sha256"] == sha(manifest_path), "Final owned manifest seal mismatch")
    require(seal["input_manifest_sha256"] == sha(OWN/"INPUT_MANIFEST.json"), "Final input seal mismatch")
    require(seal["report_sha256"] == sha(OWN/"REPORT.md") and seal["literal_verdict_file_sha256"] == sha(OWN/"VERDICT.json"), "Final scientific report/verdict seal mismatch")
    require(seal["closure_result_sha256"] == sha(OWN/"CLOSURE_RESULTS.json"), "Final closure result seal mismatch")

print(json.dumps({"status":"PASS_READ_ONLY_CLOSURE", "record_id":23331080,
                  "owned_manifest_files_checked":len(manifest["files"]),
                  "whole_native_source_files_checked":len(inputs["input_files"]),
                  "original_acquisition_manifest_entries_checked":len(original_manifest["files"]),
                  "whole_source_JSON_objects_copied_verbatim":9,
                  "native_ZIP_payloads_CRC_sizes_SHA256_and_order_checked":len(members),
                  "fresh_support_evidence_reused_checks":counts,
                  "own_exact_checks_replayed":49,"own_negative_controls_rejected":7,
                  "original_writes":False,"network":False,"old_wrapper_or_campaign_run":False,
                  "publication_authority":False}, indent=2))
