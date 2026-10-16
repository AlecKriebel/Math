#!/usr/bin/env python3
"""Freeze complete first-candidate-stage namespace; final receipt goes to stdout.

The on-disk manifest cannot contain its own stable hash. This program makes that
boundary explicit, then emits a second, self-inclusive native inventory after the
last namespace write. The parent must retain that final stdout as external evidence.
"""
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import time

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "FIRST_CANDIDATE_FREEZE.json"
CLOCK = ["/bin/date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]

def utc():
    p = subprocess.run(CLOCK, capture_output=True, check=True)
    return p.stdout.decode().strip()

def native(argv):
    start = utc()
    before = time.monotonic_ns()
    p = subprocess.run(argv, cwd=ROOT, capture_output=True, check=False)
    end = utc()
    receipt = {"argv": argv, "cwd": str(ROOT), "utc_start": start, "utc_end": end,
               "clock_argv": CLOCK, "elapsed_monotonic_ns": time.monotonic_ns()-before,
               "exit_status": p.returncode, "stdout": p.stdout.decode(errors="replace"),
               "stderr": p.stderr.decode(errors="replace")}
    if p.returncode:
        print(json.dumps(receipt, indent=2))
        raise SystemExit(p.returncode)
    return receipt

if MANIFEST.exists():
    raise SystemExit("Refusing to overwrite an existing first-candidate freeze.")

checkpoint = utc()
with (ROOT / "RESEARCH_LOG.md").open("a") as log:
    log.write(f"\n- {checkpoint}: First-candidate full-namespace freeze initiated. Initial candidate-reading stage 100%; complete requested audit 35%; original-problem resolution not independently certified. Source-only preservation was checked, with the exact frozen log prefix retained and later log entries appended. All current bodies/modes/directory modes, including failures and candidate copies, are inventoried by native stat and SHA-256 receipts. This is an exposure/assessment checkpoint only, not a clean verdict, self-seal or publication approval. HOLD: no ZIP, supporting packet or earlier review access until explicit parent release.\n")

paths = sorted([ROOT] + list(ROOT.rglob("*")), key=lambda p: str(p.relative_to(ROOT)))
for p in paths:
    if p.is_symlink() or not (p.is_file() or p.is_dir()):
        raise SystemExit("Unexpected nonregular or symlink object: " + str(p))
files = [p for p in paths if p.is_file()]
hash_receipt = native(["/usr/bin/shasum", "-a", "256"] + [str(p.relative_to(ROOT)) for p in files])
mode_receipt = native(["/usr/bin/stat", "-f", "%N|%HT|%OLp|%z"] + ["." if p==ROOT else str(p.relative_to(ROOT)) for p in paths])
rows = []
for p in paths:
    s = p.stat()
    row = {"path": "." if p==ROOT else str(p.relative_to(ROOT)),
           "type": "directory" if p.is_dir() else "file", "mode_octal": format(stat.S_IMODE(s.st_mode), "04o")}
    if p.is_file():
        row.update({"bytes": s.st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    rows.append(row)
manifest = {"stage": "first-candidate-assessment", "namespace": str(ROOT), "freeze_checkpoint_utc": checkpoint,
            "candidate_exposure": ["released manuscript.tex", "released manuscript.pdf", "released zenodo-deposit.json"], "initial_candidate_stage_complete_percent": 100,
            "whole_requested_audit_complete_percent": 35, "publication_approval": False,
            "self_reference_boundary": "This on-disk manifest inventories every object existing before its creation. Its own body/mode is included in the final self-inclusive native stdout receipt emitted after the last write. Retain that stdout externally; no manifest claims to hash itself.",
            "objects_before_manifest_creation": rows,
            "native_file_hash_receipt": hash_receipt, "native_modes_receipt": mode_receipt}
MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")

# From here onward no namespace write is permitted in this invocation.
all_paths = sorted([ROOT] + list(ROOT.rglob("*")), key=lambda p: str(p.relative_to(ROOT)))
all_files = [p for p in all_paths if p.is_file()]
final_hash = native(["/usr/bin/shasum", "-a", "256"] + [str(p.relative_to(ROOT)) for p in all_files])
final_mode = native(["/usr/bin/stat", "-f", "%N|%HT|%OLp|%z"] + ["." if p==ROOT else str(p.relative_to(ROOT)) for p in all_paths])
final_rows = []
for p in all_paths:
    s = p.stat()
    row = {"path": "." if p==ROOT else str(p.relative_to(ROOT)),
           "type": "directory" if p.is_dir() else "file", "mode_octal": format(stat.S_IMODE(s.st_mode), "04o")}
    if p.is_file():
        row.update({"bytes": s.st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    final_rows.append(row)
canonical = (json.dumps(final_rows, sort_keys=True, separators=(",", ":")) + "\n").encode()
final = {"namespace": str(ROOT), "all_namespace_files_included": True,
         "files": len(all_files), "directories": len(all_paths)-len(all_files),
         "canonical_inventory_encoding": "json.dumps(object_rows, sort_keys=True, separators=(',',':')) plus LF, UTF-8",
         "canonical_inventory_sha256": hashlib.sha256(canonical).hexdigest(),
         "objects": final_rows, "native_file_hash_receipt": final_hash,
         "native_modes_receipt": final_mode, "hold_utc": utc(),
         "candidate_exposure": ["released manuscript.tex", "released manuscript.pdf", "released zenodo-deposit.json"], "publication_approval": False}
print("FINAL_SELF_INCLUSIVE_NATIVE_FREEZE_BEGIN")
print(json.dumps(final, indent=2))
print("FINAL_SELF_INCLUSIVE_NATIVE_FREEZE_END")
