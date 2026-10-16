#!/usr/bin/env python3
"""Seal a first independent record exactly once, retaining clean provenance."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import platform
import sys

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "FIRST_MANIFEST.json"
if MANIFEST.exists():
    raise RuntimeError("First manifest exists; preserve it unchanged")

def identity(path):
    body = path.read_bytes()
    return {"path": str(path), "bytes": len(body), "sha256": sha256(body).hexdigest()}

now = datetime.now(timezone.utc).isoformat()
ledger_path = ROOT / "source_ledger.json"
ledger = json.loads(ledger_path.read_text())
ledger["section_coverage_checked_utc"] = now
ledger["primary_sources"][0]["actual_coverage"] = (
    "Full body acquired, not fully read. Complete printed pp.398 and 422 (PDF indices 25 and 49) "
    "were read as text and rendered/visually inspected, including headings, figure convention, "
    "problem, adjoining example/remark and visible footnotes. No other page was inspected locally; "
    "web returned front matter during opening and context in targeted finds. Author archive not acquired."
)
ledger["private_source_derivatives"] = [
    {**identity(path), "path": str(path.relative_to(ROOT)), "private_third_party_body": True,
     "coverage": "one complete inspected page"}
    for path in sorted((ROOT / "private_sources").iterdir()) if path.suffix in (".txt", ".png")
]
skill = Path("/Users/alec/.codex/plugins/cache/openai-primary-runtime/pdf/26.1009.11318/skills/pdf/SKILL.md")
ledger["additional_consumed_instruction"] = {**identity(skill), "read_scope": "complete body", "purpose": "read-only PDF rendering and inspection"}
ledger["runtime_binary_identities"] = [identity(Path(sys.executable).resolve()), identity(Path("/opt/homebrew/bin/pdftotext").resolve()), identity(Path("/opt/homebrew/bin/pdftoppm").resolve())]
ledger["renderer"] = {"pdftotext_version": "26.08.0", "pdftoppm_version": "26.08.0", "page_range_commands": ["-f 26 -l 26", "-f 50 -l 50"], "image_scale": 1500}
ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")

normal=json.loads((ROOT / "controls_normal.json").read_text())
optimized=json.loads((ROOT / "controls_optimized.json").read_text())
for receipt, optimization in ((normal,0),(optimized,1)):
    if receipt["status"]!="pass" or receipt["runtime"]["optimization"]!=optimization:
        raise RuntimeError("Control receipt status or optimization mismatch")
    if receipt["script_sha256"] != sha256((ROOT / "exact_controls.py").read_bytes()).hexdigest():
        raise RuntimeError("Receipt does not identify current control script")
if normal["positive_controls"] != optimized["positive_controls"] or normal["negative_mutations"] != optimized["negative_mutations"]:
    raise RuntimeError("Normal and optimized control coverage differ")
execution={"checked_utc":now,"normal_exit_code":0,"optimized_exit_code":0,
           "normal_receipt":identity(ROOT / "controls_normal.json"),
           "optimized_receipt":identity(ROOT / "controls_optimized.json"),
           "positive_control_families":len(normal["positive_controls"]),"rejected_mutations":len(normal["negative_mutations"]),
           "raw_stderr_or_headers_retained":False,"diagnostics_are_proof":False}
(ROOT / "execution_receipt.json").write_text(json.dumps(execution,indent=2)+"\n")

with (ROOT / "WORK_LOG.md").open("a") as log:
    log.write(f"\nUTC checkpoint {now}: independent universal proof completed; no full-algebra defect found. "
              f"Normal and -O controls pass with {len(normal['positive_controls'])} positive families and {len(normal['negative_mutations'])} rejected mutations. "
              "Source full-page checks complete. First assessment sealing occurs now before feedback. "
              "Audit completion estimate: 95%; overall case estimate: 15%, not accepted. "
              "No priority verdict; separate linking-number example remains unresolved.\n")

files = sorted(p for p in ROOT.rglob("*") if p.is_file())
entries=[]
for path in files:
    os.chmod(path,0o444)
    entries.append({**identity(path), "path": str(path.relative_to(ROOT)),"mode":"0444",
                    "public_eligible": "private_sources" not in path.relative_to(ROOT).parts})
manifest={"sealed_utc":now,"scope":"independent first record before feedback","files":entries,
          "self_reference":"This manifest excludes itself and its subsequent seal receipt. Their hashes and bytes are in the receipt and final inventory.",
          "overall_case_estimate_percent":15,"case_accepted":False,"audit_completion_estimate_percent":95}
MANIFEST.write_text(json.dumps(manifest,indent=2)+"\n")
os.chmod(MANIFEST,0o444)
assessment=identity(ROOT / "FIRST_ASSESSMENT.md")
receipt={"sealed_utc":now,"first_assessment":{**assessment,"mode":"0444"},
         "first_manifest":{**identity(MANIFEST),"mode":"0444"},
         "first_records_preserved":True,"feedback_sent_before_seal":False}
receipt_path=ROOT / "FIRST_SEAL_RECEIPT.json"
receipt_path.write_text(json.dumps(receipt,indent=2)+"\n")
os.chmod(receipt_path,0o444)
print(json.dumps(receipt,indent=2))
