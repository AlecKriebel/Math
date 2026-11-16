#!/usr/bin/env python3
"""Explicit custody freeze of personally read paper-first analytic reconstruction."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import sys

A = Path(__file__).resolve().parent


def pin(p):
    body = p.read_bytes()
    return {"path": str(p), "bytes": len(body), "SHA256": hashlib.sha256(body).hexdigest()}


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def freeze():
    now = datetime.now(timezone.utc).isoformat()
    require(not (A / "INITIAL_SEAL.json").exists() and not (A / "INITIAL_MANIFEST.json").exists(), "new initial only")
    receipt = json.loads((A / "MANUSCRIPT_DERIVATION_RECEIPTS.json").read_bytes())
    ledger = {"UTC": now, "record_id": 23204250, "sheet_row": 139, "actual_whole_PDF": receipt["actual_PDF"], "actual_whole_controlling_TeX": receipt["actual_controlling_TeX"], "full_PDF_pages_personally_read": 6, "all_controlling_TeX_lines_personally_read": 189, "fresh_own_rasters_personally_viewed": receipt["fresh_own_rasters"], "all6_own_individual_rasters_personally_viewed": True, "other_distinct_controlling_manuscripts": [], "complete_source_files_authenticated": 104, "complete_source_directories_authenticated": 13, "source_custody_document_read_first": "SOURCE_CUSTODY_PROOF.md", "prior_related_background": "General PSD-cone/finite-dimensional convex and linear algebra/graph polytope knowledge; prior unrelated programme work and row137 group/cost review; no prior record139 scientific opinion", "older_unrelated_excluded_row134_opinion_exposure_disclosed": True, "prior_record139_scientific_opinion": False, "actual_manuscript_author_audit_and_finite_counts_seen_not_used_as_proof": True, "supplied_scientific_code_results_archived_reviews_triage_or_current_peer_root_findings_read": False, "new_foreign_scientific_bodies_read": False, "source_or_supplied_scientific_programmes_imported_or_executed": [], "own_scientific_programmes_executed": [], "only_actual_derivation_execution": "Own whole-byte metadata authentication and ordinary Poppler PDF text/metadata/rasters", "native_version_field_present": False, "native_version_original": None, "printed_date": "October 6, 2026", "printed_version_line_present": False, "printed_version": None, "historical_source_UNREAD_flags_modified": False, "root139_gate": "CLOSED", "scientific_findings_sent_to_root": False, "publication_authority": False}
    (A / "INITIAL_READ_LEDGER.json").write_text(json.dumps(ledger, indent=2) + "\n")
    with (A / "RESEARCH_LOG.md").open("a") as f:
        f.write("\n" + now + " —20%: Resumed after checkpointaaa444c09a321e9763eef6868599a03dcff8c594 from honest18%13files/1dir/noINITIAL. Actual full6PDF/189TeX/6freshownrasters personally read. Substantial14-family independent uniform analytic reconstruction/claims/boundaries/falsifiers now frozen before native code/results, archived or current opinions, and new foreign scientific bodies. No own or supplied scientific execution yet. Root139 CLOSED; no findings sent.\n")
    (A / "RESEARCH_LOG.md").rename(A / "INITIAL_RESEARCH_LOG.md")
    files, dirs = [], []
    for p in sorted(A.rglob("*")):
        mode = p.lstat().st_mode
        require(not stat.S_ISLNK(mode), "no initial symlinks")
        if stat.S_ISDIR(mode):
            dirs.append(p.relative_to(A).as_posix())
        else:
            require(stat.S_ISREG(mode), "only regular initial files")
            files.append(pin(p))
    (A / "INITIAL_MANIFEST.json").write_text(json.dumps({"schema": "paper_first_scope139_initial_manifest_v1", "UTC": now, "files": files, "complete_directories_at_initial": dirs, "future_phases_not_part_of_initial_payload": True, "no_initial_payload_overwrite_authorized": True}, indent=2) + "\n")
    (A / "INITIAL_SEAL.json").write_text(json.dumps({"schema": "paper_first_scope139_initial_seal_v1", "UTC": datetime.now(timezone.utc).isoformat(), "record_id": 23204250, "sheet_row": 139, "status": "SUBSTANTIAL_INDEPENDENT_ANALYTIC_INITIAL_FROZEN_ROOT139_CLOSED", "manifest": pin(A / "INITIAL_MANIFEST.json"), "substantive_reconstruction": pin(A / "INITIAL_DERIVATIONS.md"), "full_read_ledger": pin(A / "INITIAL_READ_LEDGER.json"), "complete_PDF_pages": 6, "complete_TeX_lines": 189, "own_individual_fresh_rasters_viewed": 6, "materially_distinct_reconstruction_families": 14, "supplied_scientific_code_results_archive_current_opinion_or_new_foreign_exposure": False, "scientific_programmes_executed": [], "completion_percent": 20, "root139_gate": "CLOSED", "scientific_findings_sent_to_root": False, "not_a_final_scientific_disposition": True, "follow_up": None, "publication_authority": False}, indent=2) + "\n")
    print(json.dumps({"INITIAL_SEAL": pin(A / "INITIAL_SEAL.json"), "INITIAL_MANIFEST": pin(A / "INITIAL_MANIFEST.json"), "initial_payloads": len(files), "root139_gate": "CLOSED"}))


if __name__ == "__main__":
    if sys.argv[1:] != ["--freeze"]:
        raise SystemExit("Inert by default; --freeze creates paper-first initial only")
    freeze()
