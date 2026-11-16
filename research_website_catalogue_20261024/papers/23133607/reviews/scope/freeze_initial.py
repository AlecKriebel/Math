#!/usr/bin/env python3
"""Explicit source/scope paper-first initial custody freeze, no science execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import sys

A = Path(__file__).resolve().parent


def pin(p):
    b=p.read_bytes()
    return {"path":str(p),"bytes":len(b),"SHA256":hashlib.sha256(b).hexdigest()}


def need(ok,why):
    if not ok:
        raise RuntimeError(why)


def freeze():
    need(not(A/"INITIAL_MANIFEST.json").exists() and not(A/"INITIAL_SEAL.json").exists(),"new initial only")
    now=datetime.now(timezone.utc).isoformat()
    r=json.loads((A/"MANUSCRIPT_DERIVATION_RECEIPTS.json").read_bytes())
    ledger={"UTC":now,"record_id":23133607,"sheet_row":140,"actual_PDF":r["actual_PDF"],"actual_controlling_TeX":r["actual_controlling_TeX"],"all4_actual_PDF_pages_personally_read":True,"all267_actual_TeX_lines_personally_read":True,"all4_fresh_own_individual_rasters_personally_viewed":True,"fresh_own_rasters":r["fresh_own_rasters"],"additional_controlling_manuscripts":[],"whole_source_files_authenticated":97,"whole_source_directories_authenticated":9,"qualified_core_byreference_binding":pin(A/"CORE_BINDINGS.json"),"qualified_core_originals":17,"separately_authorized_checkpoint_helper_SHA256":"405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0","all18_original_unchanged_claim":False,"generated_caches_opaque_no_immutability_claim":True,"native_version_field_present":True,"native_version_original":"1.0","printed_date":"4 October 2026","printed_version_line_present":False,"printed_version":None,"historical_source_UNREAD_and_Queued_flags_modified":False,"root_current_native_InReview_status_report_only_not_independently_requeried":True,"prior_background":"General algebra/linear duality/perfect-field knowledge and prior unrelated programme reviews; no record140 scientific opinion read","older_excluded_row134_opinion_exposure_disclosed_not_imported_or_reread":True,"manuscript_author_automated_validation_and_classical_credit_assertions_seen_not_used_as_proof":True,"supplied_scientific_code_results_archive_or_current_peer_root_opinions_read":False,"new_foreign_scientific_bodies_read":False,"scientific_programmes_imported_or_executed":[],"primary_GETs":0,"only_executed_derivation":"Own metadata/source/core byte checks and ordinary Poppler PDF derivatives","root140_gate":"CLOSED","scientific_findings_sent_to_root":False,"publication_authority":False}
    (A/"INITIAL_READ_LEDGER.json").write_text(json.dumps(ledger,indent=2)+"\n")
    with(A/"RESEARCH_LOG.md").open("a")as f:
        f.write("\n"+now+" —20%: Resumed after checkpoint0746661d1a5b45f6a67084ab5572bc6b34a9886b from honest15files/1dir/18%partial/noINITIAL. Actual4PDF/267TeX/4freshownrasters fully personally read. Substantial14-family independent module/duality/Honda/scope reconstruction now frozen before suppliedcode/results/archive/currentopinions/foreign bodies or scientific execution. SourceQueued remains historical despite root-reported currentInReview. No primaryGET; root140 CLOSED.\n")
    (A/"RESEARCH_LOG.md").rename(A/"INITIAL_RESEARCH_LOG.md")
    files,dirs=[],[]
    for p in sorted(A.rglob("*")):
        mode=p.lstat().st_mode
        need(not stat.S_ISLNK(mode),"no symlinks")
        if stat.S_ISDIR(mode):dirs.append(p.relative_to(A).as_posix())
        else:
            need(stat.S_ISREG(mode),"only regular payloads")
            files.append(pin(p))
    (A/"INITIAL_MANIFEST.json").write_text(json.dumps({"schema":"scope140_paper_first_initial_manifest_v1","UTC":now,"files":files,"complete_directories_at_initial":dirs,"no_initial_payload_overwrite_authorized":True},indent=2)+"\n")
    (A/"INITIAL_SEAL.json").write_text(json.dumps({"schema":"scope140_paper_first_initial_seal_v1","UTC":datetime.now(timezone.utc).isoformat(),"record_id":23133607,"sheet_row":140,"status":"SUBSTANTIAL_INDEPENDENT_SCOPE_INITIAL_FROZEN_ROOT140_CLOSED","manifest":pin(A/"INITIAL_MANIFEST.json"),"substantive_reconstruction":pin(A/"INITIAL_DERIVATIONS.md"),"read_ledger":pin(A/"INITIAL_READ_LEDGER.json"),"complete_PDF_pages":4,"complete_TeX_lines":267,"fresh_own_rasters_viewed":4,"materially_distinct_reconstruction_families":14,"supplied_code_results_archive_foreign_or_current_opinion_exposure":False,"scientific_programmes_executed":[],"primary_GETs":0,"completion_percent":20,"root140_gate":"CLOSED","scientific_findings_sent_to_root":False,"not_final_disposition":True,"follow_up":None,"publication_authority":False},indent=2)+"\n")
    print(json.dumps({"INITIAL_SEAL":pin(A/"INITIAL_SEAL.json"),"MANIFEST":pin(A/"INITIAL_MANIFEST.json"),"initial_payloads":len(files),"root140_gate":"CLOSED"}))


if __name__=="__main__":
    if sys.argv[1:]!=["--freeze"]:
        raise SystemExit("Inert by default; --freeze records only new paper-first initial custody")
    freeze()
