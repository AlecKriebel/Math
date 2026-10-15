"""Bound only this family's files; foreign primary evidence is excluded individually."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

here = Path(__file__).resolve().parent
entries = []
for path in sorted(here.rglob("*")):
    if not path.is_file() or path.name == "SELF_MANIFEST.json":
        continue
    relative = path.relative_to(here).as_posix()
    data = path.read_bytes()
    if len(data) >= 100 * 1024 * 1024:
        raise RuntimeError("File reaches 100 MiB cap: " + relative)
    digest = hashlib.sha256(data).hexdigest()
    if relative.startswith("foreign/"):
        if relative.endswith(".extracted.txt"):
            purpose = "Mechanically extracted primary source text, foreign content, not authored science."
        elif relative.endswith(".png"):
            purpose = "Rendered primary-source page for visual inspection, foreign content, not an authored figure."
        elif relative.endswith(".pdf"):
            purpose = "Individually preserved downloaded primary scientific publication, not authored or copied project science."
        elif relative.endswith("kp_publisher.html"):
            purpose = "Foreign publisher anti-bot access response; not inspected journal science."
        elif relative.endswith("jkp_publisher_download.response"):
            purpose = "Foreign HTML access response, not a journal PDF or a journal-proof capture."
        else:
            purpose = "Individually preserved primary landing/version metadata HTML, foreign content."
        classification = "foreign_primary_or_access_evidence"
        exclusion = "Excluded from first-party scientific and novelty claims; retained only as hash-bound source/access evidence."
    else:
        classification = "first_party_audit_artifact"
        purpose = ("Own audit program, mathematical derivation, research note or genuine process/source-inspection receipt. "
                   "No candidate helper execution is represented by this classification.")
        exclusion = None
    entries.append({"path": relative, "bytes": len(data), "sha256": digest,
                    "classification": classification, "purpose": purpose,
                    "individual_exclusion": exclusion, "novelty_claim": False})

for name in ["INITIAL_SEAL", "SOURCE_VERDICT_SEAL"]:
    expected = (here / (name + ".sha256")).read_text().split()[0]
    actual = hashlib.sha256((here / (name + ".md")).read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError("Independent seal changed: " + name)

for label, source_path in [("source_inspection", "captures/first_source_reconstructed_after_execution.py"),
                           ("source_inspection_corrected", "inspect_sources_and_snapshot.py")]:
    receipt = json.loads((here / "captures" / (label + "_capture.json")).read_text())
    if receipt["returncode"] != 0:
        raise RuntimeError("Source predicate process did not complete: " + label)
    for stream in ["stdout", "stderr"]:
        data = (here / "captures" / (label + "." + stream + ".txt")).read_bytes()
        if hashlib.sha256(data).hexdigest() != receipt[stream + "_sha256"]:
            raise RuntimeError("Full stream changed: " + label + "." + stream)
    if hashlib.sha256((here / source_path).read_bytes()).hexdigest() != receipt["prelaunch_source_sha256"]:
        raise RuntimeError("Source bytes are not bound to their process: " + label)

corrected = json.loads((here / "captures/source_inspection_corrected.stdout.txt").read_text())
if not corrected["all_finite_source_predicates_passed"]:
    raise RuntimeError("Corrected source predicates do not all pass")

manifest = {"schema": "probability-source-family-self-only-closure/v1",
            "utc": datetime.now(timezone.utc).isoformat(), "manifest_process_pid": os.getpid(),
            "root": str(here), "scope": "This family only; no sibling, parent or candidate artifact is included as first-party science.",
            "files": entries,
            "manifest_self_exclusion": "SELF_MANIFEST.json is this hash-list control and is excluded only to avoid a self-hash cycle.",
            "first_party_file_count": sum(row["classification"] == "first_party_audit_artifact" for row in entries),
            "individual_foreign_file_count": sum(row["classification"] == "foreign_primary_or_access_evidence" for row in entries),
            "all_files_below_100MiB": True, "own_readonly_source_predicates": 44,
            "own_candidate_helper_import_compile_execution": False,
            "own_native_git_or_remote_writes": False, "novelty_claim": False,
            "whole_PR_or_future_scope_certified": False,
            "pending_parent_work": "Current provenance precision repairs, cross-family reconciliation and whole-scope publication review."}
(here / "SELF_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"scope": manifest["scope"], "files": len(entries),
                  "first_party": manifest["first_party_file_count"], "individual_foreign": manifest["individual_foreign_file_count"],
                  "total_bytes": sum(row["bytes"] for row in entries),
                  "largest_file_bytes": max(row["bytes"] for row in entries),
                  "final_report_sha256": hashlib.sha256((here / "FINAL_REPORT.md").read_bytes()).hexdigest(),
                  "manifest_sha256": hashlib.sha256((here / "SELF_MANIFEST.json").read_bytes()).hexdigest(),
                  "both_independent_seals_unchanged": True, "corrected_own_source_predicates_all_passed": True}, indent=2))
