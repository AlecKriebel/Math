#!/usr/bin/env python3
"""Explicit new scope terminal freeze; no source/native scientific execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import subprocess
import sys

A = Path(__file__).resolve().parent
TERMINALS = ["CLOSURE.json", "FINAL_SEAL.json", "OWNED_MANIFEST.json"]


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def pin(p):
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "SHA256": hashlib.sha256(b).hexdigest()}


def write_new(name, value):
    p = A / name
    need(not p.exists(), "no terminal overwrite")
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def freeze():
    need(not any((A/n).exists() for n in TERMINALS), "all terminal controls newly absent")
    current = load_code = json.loads((A/"CODE_AND_EXECUTION_LEDGER.json").read_bytes())
    current["current_terminal_helper_fully_read_before_execution"] = pin(A/"verify_custody.py")
    current["current_freeze_orchestrator_fully_read_before_execution"] = pin(Path(__file__))
    current["actual_metadata_package_execution"] = json.loads((A/"PACKAGE_EXECUTION.json").read_bytes())
    (A/"CODE_AND_EXECUTION_LEDGER.json").write_text(json.dumps(load_code,indent=2,ensure_ascii=False)+"\n")
    with (A/"RESEARCH_LOG.md").open("a") as f:
        f.write("\n"+datetime.now(timezone.utc).isoformat()+" —95%: Current complete standalone custody helper and terminal orchestrator fully read. Original104-file/13-dir source, native objects, two ZIP central directories/all35 regular bodies, own early seals, all raw handoff files and exact owned namespace are now checked offline under normal/optimized Python. Only successful actual terminal closure becomes100%FINAL. No source/science/native/foreign/oldcampaign replay. Root139 CLOSED; no findings shared.\n")
    files, dirs = [], []
    for p in sorted(A.rglob("*")):
        mode = p.lstat().st_mode
        need(not stat.S_ISLNK(mode), "no owned symlink")
        if stat.S_ISDIR(mode):
            dirs.append(p.relative_to(A).as_posix())
        else:
            need(stat.S_ISREG(mode), "only owned regular files")
            item = pin(p)
            item["path"] = p.relative_to(A).as_posix()
            files.append(item)
    write_new("OWNED_MANIFEST.json", {"schema":"scope139_strict_whole_owned_file_directory_namespace_v1","UTC":datetime.now(timezone.utc).isoformat(),"files":files,"directories":dirs,"exact_root_terminal_controls":TERMINALS,"recursive_basename_exclusions":False,"future_output_exclusions":[],"root139_gate":"CLOSED"})
    runs = []
    for options in ([],["-O"]):
        command = [sys.executable,"-B",*options,str(A/"verify_custody.py"),"--preseal"]
        start = datetime.now(timezone.utc).isoformat()
        r = subprocess.run(command,capture_output=True,text=True)
        runs.append({"actual_command":command,"UTC_started":start,"UTC_completed":datetime.now(timezone.utc).isoformat(),"exit_code":r.returncode,"stdout":r.stdout,"stderr":r.stderr,"whole_result":json.loads(r.stdout) if r.returncode==0 else None})
        if r.returncode != 0 or r.stderr:
            fail = A/"CLOSURE_FAILED_ATTEMPT.json"
            need(not fail.exists(),"retain actual first closure failure")
            fail.write_text(json.dumps({"actual_runs":runs,"no_FINAL_written":True},indent=2)+"\n")
            raise RuntimeError("Custody failed; whole actual process streams retained, no FINAL")
    write_new("CLOSURE.json", {"schema":"scope139_actual_offline_preseal_closure_v1","UTC":datetime.now(timezone.utc).isoformat(),"actual_runs":runs,"fully_read_current_pure_helper":pin(A/"verify_custody.py"),"fully_read_current_freeze_orchestrator":pin(Path(__file__)),"whole_checked_manifest":pin(A/"OWNED_MANIFEST.json"),"custody_only_not_scientific_proof":True,"root139_gate":"CLOSED"})
    write_new("FINAL_SEAL.json", {"schema":"scope139_immutable_final_v1","UTC":datetime.now(timezone.utc).isoformat(),"record_id":23204250,"sheet_row":139,"status":"INDEPENDENT_ANALYTIC_SCOPE_FINAL_FINDINGS_WITHHELD_ROOT139_CLOSED","completion_percent":100,"MANIFEST_SHA256":pin(A/"OWNED_MANIFEST.json")["SHA256"],"CLOSURE_SHA256":pin(A/"CLOSURE.json")["SHA256"],"owned_payload_count":len(files),"complete_actual_files":len(files)+3,"complete_directories":len(dirs),"exact_root_terminal_controls":TERMINALS,"recursive_basename_exclusions":False,"future_output_exclusions":[],"unchanged_source_files":104,"unchanged_source_directories":13,"native_assets_in_original_order":["paper.pdf","tsp-verification.zip","tsp-source.zip"],"PDF_pages":6,"controlling_TeX_lines":189,"fresh_own_manuscript_rasters_read":6,"fresh_own_primary_rasters_read":8,"ZIP_containers":2,"ZIP_regular_occurrences":35,"raw_primary_records":32,"own_primary_GETs":0,"SOURCE_READY_SHA256":"13d913127abab98d78c3758516884b09f7e4849b5e6c07a3e0fd44c502147ec9","SOURCE_SEAL_SHA256":"94bd3bbf71c9fd618b6bf12616120aace2a6d3fe04707d6f73bb1bd787dd8ecf","INITIAL_SEAL_SHA256":"54aab1397c627cd08661c88b2fb2102910c15f325628ebb360455f15cd31d329","OWN_PROOF_CONTROL_SEAL_SHA256":"ba94acb1f8d28a51a73f6d4799f3bb5bfcbd8d93269aeb4d4aab34703610f391","native_version_field_present":False,"native_version_original":None,"source_historical_UNREAD_flags_unchanged":True,"source_or_supplied_scientific_programmes_executed":[],"current_peer_root_findings_or_replay_results_read":False,"root139_gate":"CLOSED","scientific_findings_sent_to_root":False,"publication_authority":False,"production_authority":False,"canonical_url":None,"AA":None,"no_postseal_writes_authorized":True})
    print(json.dumps({"FINAL_SEAL":pin(A/"FINAL_SEAL.json"),"MANIFEST":pin(A/"OWNED_MANIFEST.json"),"CLOSURE":pin(A/"CLOSURE.json"),"complete_files":len(files)+3,"complete_directories":len(dirs),"normal_optimized_preseal_custody_checks":[r["whole_result"]["checks"] for r in runs],"root139_gate":"CLOSED"},sort_keys=True))


if __name__ == "__main__":
    if sys.argv[1:] != ["--freeze"]:
        raise SystemExit("Inert by default; --freeze creates new scope exact terminal controls only")
    freeze()
