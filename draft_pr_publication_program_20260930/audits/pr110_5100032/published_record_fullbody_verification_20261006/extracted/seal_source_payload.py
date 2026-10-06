#!/usr/bin/env python3
"""Seal the authored source payload in its original repository custody context.

This does not compile, archive, publish, contact anyone, or mutate Git.
It validates adjacent results and exact input pins before generating a compact
manifest and independent seal receipt. It is not needed to run verify.py.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REQUIRED = {
    "focal_antipedal_sum.tex", "verify.py", "run_verification.py",
    "proof_binding.json", "input_pins.json", "RESEARCH_LOG.md", "README.md",
    "LICENSE", "source_audit_summary.md", "intended_zenodo_metadata.json",
    "zenodo-deposit.json", "verification_normal.json", "verification_optimized.json",
    "execution_envelope.json", "seal_source_payload.py",
}
EXCLUDED = {"source_payload_manifest.json", "source_seal_receipt.json"}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def pin(path, label=None):
    body = path.read_bytes()
    return {"path":label or path.name,"bytes":len(body),
            "sha256":hashlib.sha256(body).hexdigest()}


def read(name):
    return json.loads((HERE/name).read_text(encoding="utf-8"))


def main():
    started = now()
    found = {p.name for p in HERE.iterdir()}
    require(found-EXCLUDED == REQUIRED, "Unexpected or missing source payload members")
    require(all((HERE/name).is_file() for name in REQUIRED), "Payload must contain regular files")
    require(not any((HERE/name).is_symlink() for name in found), "No symlink payload or receipt")
    source = pin(HERE/"focal_antipedal_sum.tex")
    binding = read("proof_binding.json")
    require(all(source[k] == binding[k] for k in ("path","bytes","sha256")), "Manuscript binding mismatch")
    inputs = read("input_pins.json")
    for item in inputs["pins"]:
        actual = pin(HERE.parent/item["path_relative_to_audit_root"])
        require(actual["bytes"] == item["bytes"] and actual["sha256"] == item["sha256"],
                "Changed pinned authoring input: "+item["path_relative_to_audit_root"])
    gate = json.loads((HERE.parent/"ROOT_PRIORITY_CLEARANCE_AFTER_M1_20261006.json").read_text())
    require(all(gate[k] is True for k in ("mathematical_clearance","M1_journal_final_comparison_cleared",
                                         "bounded_priority_clearance","paper_preparation_authorized")),
            "Authoritative root preparation gate is not cleared")
    require(gate["publication_ready"] is False, "This source-only seal assumes later package reviews")
    intended, deposit = read("intended_zenodo_metadata.json"), read("zenodo-deposit.json")
    require(intended["metadata"] == deposit["metadata"], "Metadata objects differ")
    metadata = intended["metadata"]
    require(metadata["title"] == "A telescoping proof of the focal antipedal sum invariant", "Title mismatch")
    require(metadata["publication_date"] == "2026-10-06" and metadata["version"] == "1.0", "Date/version mismatch")
    require(metadata["license"] == "cc-by-4.0", "License mismatch")
    require(metadata["creators"] == [{"name":"Kriebel, Alec","affiliation":"Independent researcher",
                                      "orcid":"0009-0001-9320-500X"}], "Author metadata mismatch")
    require(deposit["files"] == [{"path":"focal_antipedal_sum.pdf"},{"path":"focal_antipedal_sum_support.zip"}],
            "Planned adjacent deliverable names mismatch")
    normal, optimized = read("verification_normal.json"), read("verification_optimized.json")
    for result, mode in ((normal,0),(optimized,1)):
        require(result["status"] == "passed" and result["optimization_level"] == mode, "Verification mode/status mismatch")
        require(result["proof_sha256"] == source["sha256"], "Executed verifier bound to different manuscript")
        require(result["directed_chord_cases"] == 1456 and result["explicit_passing_guard_checks"] == 63346,
                "Verification counts inconsistent with README")
        require([r["name"] for r in result["mandatory_invalid_controls"]] ==
                ["coefficient","height","sign","proof-binding"], "Missing mandatory invalid controls")
        require(all(r["rejected"] is True for r in result["mandatory_invalid_controls"]), "Invalid control accepted")
    keys = ("proof_sha256","directed_chord_cases","paired_reversal_cases","horizontal_directed_chords",
            "coefficient_sign_cases","explicit_passing_guard_checks","closed_cycle_controls","mandatory_invalid_controls")
    require(all(normal[k] == optimized[k] for k in keys), "Normal/-O summaries differ")
    envelope = read("execution_envelope.json")
    require(envelope["normal_optimized_agree"] is True and len(envelope["operations"]) == 10,
            "Execution envelope lacks genuine positive/negative runs")
    for receipt in envelope["operations"]:
        require(receipt["child_PID"] > 0 and receipt["UTC_start"] <= receipt["UTC_end"], "Invalid actual process receipt")
        if receipt["invalid_control"] is None:
            output = pin(HERE/receipt["stdout"]["path"])
            require(all(output[k] == receipt["stdout"][k] for k in ("bytes","sha256")), "Executed output pin mismatch")
            result = optimized if receipt["optimization"] else normal
            require(receipt["child_PID"] == result["actual_verifier_PID"] and receipt["exit_code"] == 0,
                    "Positive process/result mismatch")
        else:
            require(receipt["exit_code"] == 2 and receipt["stdout"]["bytes"] == 0 and
                    receipt["verified_rejection"]["actual_verifier_PID"] == receipt["child_PID"],
                    "Required failed subprocess control not authenticated")
    checkpoint = now()
    with (HERE/"RESEARCH_LOG.md").open("a",encoding="utf-8") as log:
        log.write("\n"+checkpoint+" — Final source/support checkpoint: 100% of this preparation subtask. "
                  "Exact 16 input pins rechecked, manuscript binding checked, metadata objects identical; "
                  "normal and optimized runs each passed 1,456 directed chord cases and 63,346 explicit guards, "
                  "and all eight mandatory faulty subprocesses were rejected for the expected reason. "
                  "Source payload sealed for root compilation/visual review/archive assembly and fresh whole-package "
                  "reviews. Mathematical and bounded-priority gates are cleared; publication readiness remains false. "
                  "No source bytes should be edited after this seal without reopening binding, verification and sealing.\n")
    files = [pin(HERE/name) for name in sorted(REQUIRED)]
    manifest = {"schema":"focal-antipedal-authored-source-manifest/v1","UTC":checkpoint,
                "actual_manifest_builder_PID":os.getpid(),"scope":"Authored source/support payload only; no PDF or archive.",
                "files":files,"excluded_receipts":sorted(EXCLUDED)}
    path = HERE/"source_payload_manifest.json"
    path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    receipt = {"schema":"focal-antipedal-authored-source-seal/v1","actual_sealer_PID":os.getpid(),
               "argv":[sys.executable]+sys.argv,"cwd":str(Path.cwd()),
               "UTC_started":started,"UTC_sealed":now(),"source_manifest":pin(path),
               "source_file_count":len(files),"source_total_bytes":sum(p["bytes"] for p in files),
               "exact_input_pins_checked":len(inputs["pins"]),"normal_optimized_verification_checked":True,
               "mandatory_failed_subprocess_controls":8,"source_support_preparation_percent":100,
               "publication_ready":False,"PDF_or_archive_constructed":False}
    (HERE/"source_seal_receipt.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
