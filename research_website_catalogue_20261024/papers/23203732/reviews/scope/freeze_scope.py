#!/usr/bin/env python3
"""Explicit new-folder custody freeze; no source or native scientific execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import subprocess
import sys

A = Path(__file__).resolve().parent
TERMINALS = ["CLOSURE.json", "FINAL_SEAL.json", "OWNED_MANIFEST.json"]


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def pin(p):
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "SHA256": hashlib.sha256(b).hexdigest()}


def write_new(name, obj):
    p = A / name
    require(not p.exists(), "exact new terminal only: " + name)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def freeze():
    require(not any((A / name).exists() for name in TERMINALS), "no terminal overwrite")
    code = json.loads((A / "CODE_AND_EXECUTION_LEDGER.json").read_bytes())
    code["current_freeze_orchestrator_fully_read_before_execution"] = pin(Path(__file__))
    (A / "CODE_AND_EXECUTION_LEDGER.json").write_text(json.dumps(code, indent=2, ensure_ascii=False) + "\n")
    with (A / "RESEARCH_LOG.md").open("a") as f:
        f.write("\n" + datetime.now(timezone.utc).isoformat() + " —95%: All scientific reading, bounded own controls, derivations, literal data/exposure/failure records and full current custody/freeze source reading complete. Exact owned manifest and actual normal/optimized offline custody closure are now attempted. Completion100% exists only in a successful immutable FINAL terminal; failed attempts remain preserved. Root137 CLOSED, findings withheld.\n")
    files, dirs = [], []
    for p in sorted(A.rglob("*")):
        mode = p.lstat().st_mode
        rel = p.relative_to(A).as_posix()
        require(not stat.S_ISLNK(mode), "no symlinks")
        if stat.S_ISDIR(mode):
            dirs.append(rel)
        else:
            require(stat.S_ISREG(mode), "only regular owned files")
            item = pin(p)
            item["path"] = rel
            files.append(item)
    write_new("OWNED_MANIFEST.json", {"schema": "scope_23203732_strict_owned_whole_namespace_v1", "UTC": datetime.now(timezone.utc).isoformat(), "files": files, "directories": dirs, "exact_root_terminal_controls": TERMINALS, "recursive_basename_exclusions": False, "future_output_exclusions": [], "root137_gate": "CLOSED"})
    runs = []
    for options in ([], ["-O"]):
        command = [sys.executable, "-B", *options, str(A / "verify_custody.py"), "--preseal"]
        started = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(command, capture_output=True, text=True)
        run = {"actual_command": command, "UTC_started": started, "UTC_completed": datetime.now(timezone.utc).isoformat(), "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr, "whole_result": json.loads(result.stdout) if result.returncode == 0 else None}
        runs.append(run)
        if result.returncode != 0 or result.stderr:
            path = A / "failures" / ("CLOSURE_FAILURE_" + str(len(runs)) + ".json")
            require(not path.exists(), "retain first closure failure")
            path.write_text(json.dumps({"actual_runs": runs, "no_FINAL_written": True}, indent=2) + "\n")
            raise RuntimeError("Custody closure failed; full actual streams preserved, no FINAL")
    write_new("CLOSURE.json", {"schema": "scope_23203732_actual_preseal_closure_v1", "UTC": datetime.now(timezone.utc).isoformat(), "actual_runs": runs, "fully_read_current_pure_helper": pin(A / "verify_custody.py"), "fully_read_current_freeze_orchestrator": pin(Path(__file__)), "whole_manifest_checked": pin(A / "OWNED_MANIFEST.json"), "custody_only_not_scientific_proof": True, "no_native_or_source_scientific_execution": True, "root137_gate": "CLOSED"})
    write_new("FINAL_SEAL.json", {"schema": "scope_23203732_immutable_final_v1", "UTC": datetime.now(timezone.utc).isoformat(), "record_id": 23203732, "sheet_row": 137, "status": "INDEPENDENT_SCOPE_FINAL_FINDINGS_WITHHELD_ROOT137_CLOSED", "completion_percent": 100, "MANIFEST_SHA256": pin(A / "OWNED_MANIFEST.json")["SHA256"], "CLOSURE_SHA256": pin(A / "CLOSURE.json")["SHA256"], "owned_payload_count": len(files), "complete_actual_files": len(files) + 3, "complete_directories": len(dirs), "exact_root_terminal_controls": TERMINALS, "recursive_basename_exclusions": False, "future_output_exclusions": [], "source_files_unchanged": 101, "source_directories_unchanged": 18, "native_asset_order": ["paper.pdf", "cost-betti-source-and-verification.zip"], "PDF_pages": 6, "controlling_TeX_lines": 198, "own_manuscript_rasters_read": 6, "own_primary_rasters_read": 8, "archive_containers": 1, "ZIP_regular_occurrences": 35, "raw_primary_handoff_files": 56, "own_primary_GETs": 0, "source_READY_SHA256": "bd5708d6fa77da017786d34952a3d689b5b5fb2703086bc4d33a1093430ed4cb", "source_SEAL_SHA256": "cf9ffb0b5f509af974aa3e7a368c2672e000f2665aecf772a0df57f658145287", "initial_SEAL_SHA256": "087144bfa352a5236528c552ea4c31650da8a0b7ac0aa4fae746769b56717101", "own_PROOF_CONTROL_SEAL_SHA256": "70820956f8fc2da8d8790b2ee01bf83221d6e37ee5d5fb5ad4e6dc627113c34d", "native_version_field_present": False, "native_version_original": None, "source_historical_UNREAD_flags_unchanged": True, "root137_gate": "CLOSED", "scientific_findings_sent_to_root": False, "source_scientific_programmes_executed": [], "current_peer_or_root_findings_read": False, "publication_authority": False, "production_authority": False, "canonical_url": None, "AA": None, "no_postseal_writes_authorized": True})
    print(json.dumps({"FINAL_SEAL": pin(A / "FINAL_SEAL.json"), "MANIFEST": pin(A / "OWNED_MANIFEST.json"), "complete_files": len(files) + 3, "complete_directories": len(dirs), "normal_and_optimized_preseal_checks": [r["whole_result"]["checks"] for r in runs], "root137_gate": "CLOSED"}, sort_keys=True))


if __name__ == "__main__":
    if sys.argv[1:] != ["--freeze"]:
        raise SystemExit("Inert by default; --freeze creates exact new scope terminals only")
    freeze()
