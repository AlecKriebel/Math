#!/usr/bin/env python3
"""Verify both prior seals and create an additive exact allowlist/inventory."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import stat

ROOT=Path(__file__).resolve().parent
TARGET=ROOT/"FINAL_INVENTORY_ADDITIVE.json"
if TARGET.exists(): raise RuntimeError("Additive inventory exists; preserve it")

def identity(path):
    body=path.read_bytes()
    return {"path":str(path.relative_to(ROOT)),"bytes":len(body),"sha256":sha256(body).hexdigest(),"mode":f"{stat.S_IMODE(path.stat().st_mode):04o}"}

first=json.loads((ROOT/"FIRST_MANIFEST.json").read_text())
for item in first["files"]:
    actual=identity(ROOT/item["path"])
    for field in ("bytes","sha256","mode"):
        if actual[field]!=item[field]: raise RuntimeError("Changed first record: "+item["path"])
old=json.loads((ROOT/"FINAL_INVENTORY.json").read_text())
for item in old["all_retained_files"]:
    actual=identity(ROOT/item["path"])
    for field in ("bytes","mode"):
        if actual[field]!=item[field]: raise RuntimeError("Changed initial final record")
    if item["sha256"] is not None and actual["sha256"]!=item["sha256"]: raise RuntimeError("Changed initial final digest")
if identity(ROOT/"FINAL_INVENTORY.json")["sha256"]!="7910498b9cd7e7efb914ef8e2dee842b0fca8f0e833d0b3d39f6665d65c1216f": raise RuntimeError("Initial final inventory changed")
if identity(ROOT/"PUBLIC_ALLOWLIST.json")["sha256"]!="8c853b9cf25bb2bf822b8c499fbdf26d0366704b082cd9519cde55bc3b873a19": raise RuntimeError("Initial allowlist changed")

now=datetime.now(timezone.utc).isoformat()
ledger_path=ROOT/"REPAIR_SOURCE_LEDGER.json"
ledger=json.loads(ledger_path.read_text())
ledger["visual_source_check_completed_utc"]=now
ledger["acquired_primary_bodies"][1]["actual_coverage"]="Complete one-page question extracted, rendered and visually read: header/date, posting label, question, example, remark, references and footer."
ledger["source_derivatives"]=[identity(ROOT/"private_sources"/name) for name in ("author_question.txt","author_question.png")]
ledger["observed_date_evidence"]={"posting_label":"June 2001","displayed_PDF_header":"July 24, 2011, 12:42 PM","archive_listing_creation_UTC":"2011-07-24 16:42:55","archive_listing_modification_UTC":"2011-07-24 16:50:00","interpretation":"Displayed provenance labels only, no priority conclusion."}
ledger["checkpoint"]={"audit_completion_percent":100,"case_completion_percent":15,"accepted":False}
ledger_path.write_text(json.dumps(ledger,indent=2)+"\n")

old_allow=json.loads((ROOT/"PUBLIC_ALLOWLIST.json").read_text())
names=[entry["path"] for entry in old_allow["files"]]
names += ["PUBLIC_ALLOWLIST.json","FINAL_INVENTORY.json","REPAIR_ADDITIVE_NOTE.md","repair_recheck.py","REPAIR_SOURCE_LEDGER.json","REPAIR_EXECUTION_RECEIPT.json","seal_additive.py"]
for name in names: os.chmod(ROOT/name,0o444)
excluded=[str(path.relative_to(ROOT)) for folder in (ROOT/"private_sources",ROOT/"repair_inputs") for path in sorted(folder.rglob("*")) if path.is_file()]
allow={"sealed_utc":now,"supersedes_for_package_selection":"PUBLIC_ALLOWLIST.json (preserved)",
       "exact_files":[identity(ROOT/name) for name in names],"exact_excluded_body_paths":excluded,
       "private_third_party_bodies_excluded":True,"consumed_repaired_input_snapshots_excluded":True,
       "scope":"Math only; case 15%, not accepted; no priority/publication verdict."}
allow_path=ROOT/"PUBLIC_ALLOWLIST_ADDITIVE.json"
allow_path.write_text(json.dumps(allow,indent=2)+"\n")
os.chmod(allow_path,0o444)
records=[]
for path in sorted(ROOT.rglob("*")):
    if path.is_file():
        os.chmod(path,0o444)
        records.append(identity(path))
records.append({"path":TARGET.name,"bytes":0,"sha256":None,"mode":"0444","sha256_location":"External final audit message, avoiding self digest embedding."})
inventory={"sealed_utc":now,"all_retained_files":sorted(records,key=lambda x:x["path"]),
           "first_and_initial_final_records_verified_unchanged":True,"public_allowlist":identity(allow_path),
           "audit_completion_percent":100,"case_completion_percent":15,"case_accepted":False,
           "raw_stderr_or_headers_retained":False}
for _ in range(10):
    body=(json.dumps(inventory,indent=2)+"\n").encode()
    entry=next(item for item in inventory["all_retained_files"] if item["path"]==TARGET.name)
    if entry["bytes"]==len(body): break
    entry["bytes"]=len(body)
else: raise RuntimeError("Self byte count did not stabilize")
TARGET.write_bytes(body); os.chmod(TARGET,0o444)
actual={str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()}
if actual!={x["path"] for x in inventory["all_retained_files"]}: raise RuntimeError("Incomplete additive inventory")
if any(stat.S_IMODE(p.stat().st_mode)!=0o444 for p in ROOT.rglob("*") if p.is_file()): raise RuntimeError("Unsealed retained file")
print(json.dumps({"status":"sealed","final_inventory":identity(TARGET),"public_allowlist":identity(allow_path),"retained_file_count":len(actual),"first_and_initial_final_records_verified_unchanged":True},indent=2))
