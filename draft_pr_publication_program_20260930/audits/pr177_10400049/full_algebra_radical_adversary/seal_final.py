#!/usr/bin/env python3
"""Verify preservation, record an exact public allowlist, and seal an inventory.

The inventory includes its own name/mode/bytes. Its SHA256 is reported externally
because embedding a file's own SHA256 would create a self-reference problem.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import stat

ROOT=Path(__file__).resolve().parent
inventory_path=ROOT / "FINAL_INVENTORY.json"
if inventory_path.exists():
    raise RuntimeError("Final inventory already exists; preserve it")

def data(path):
    body=path.read_bytes()
    return {"path":str(path.relative_to(ROOT)),"bytes":len(body),"sha256":sha256(body).hexdigest(),"mode":f"{stat.S_IMODE(path.stat().st_mode):04o}"}

first=json.loads((ROOT / "FIRST_MANIFEST.json").read_text())
for record in first["files"]:
    actual=data(ROOT / record["path"])
    for key in ("bytes","sha256","mode"):
        if actual[key]!=record[key]: raise RuntimeError("First record changed: "+record["path"])
seal=json.loads((ROOT / "FIRST_SEAL_RECEIPT.json").read_text())
for key in ("first_assessment","first_manifest"):
    path=Path(seal[key]["path"])
    actual=data(path)
    for field in ("bytes","sha256","mode"):
        if actual[field]!=seal[key][field]: raise RuntimeError("First seal identity changed")

public_names=["FIRST_ASSESSMENT.md","FIRST_MANIFEST.json","FIRST_SEAL_RECEIPT.json","WORK_LOG.md",
              "source_ledger.json","exact_controls.py","controls_normal.json","controls_optimized.json",
              "execution_receipt.json","acquire_sources.py","seal_first.py","FINAL_NOTES.md","seal_final.py"]
for name in public_names:
    path=ROOT/name
    if not path.is_file() or "private_sources" in path.parts: raise RuntimeError("Invalid public allowlist entry")
    os.chmod(path,0o444)
now=datetime.now(timezone.utc).isoformat()
allowlist={"created_utc":now,"kind":"exact paths with immutable content identities",
           "files":[data(ROOT/name) for name in public_names],
           "private_third_party_bodies_excluded":True,
           "exclusions":[str(path.relative_to(ROOT)) for path in sorted((ROOT/"private_sources").iterdir()) if path.is_file()],
           "gate":"Math only; root mathematics/publication gate remains responsible. Case 15%, not accepted."}
allowlist_path=ROOT/"PUBLIC_ALLOWLIST.json"
allowlist_path.write_text(json.dumps(allowlist,indent=2)+"\n")
os.chmod(allowlist_path,0o444)

entries=[]
for path in sorted(ROOT.rglob("*")):
    if path.is_file():
        os.chmod(path,0o444)
        entries.append(data(path))
entries.append({"path":"FINAL_INVENTORY.json","bytes":0,"sha256":None,"mode":"0444",
                "sha256_location":"External final audit message; embedding the digest of this file in itself is not attempted."})
inventory={"sealed_utc":now,"all_retained_files":sorted(entries,key=lambda x:x["path"]),
           "first_records_verified_unchanged":True,"public_allowlist":data(allowlist_path),
           "audit_completion_percent":100,"case_completion_percent":15,"case_accepted":False,
           "raw_stderr_or_headers_retained":False}
for _ in range(10):
    body=(json.dumps(inventory,indent=2)+"\n").encode()
    self_entry=next(x for x in inventory["all_retained_files"] if x["path"]=="FINAL_INVENTORY.json")
    if self_entry["bytes"]==len(body): break
    self_entry["bytes"]=len(body)
else: raise RuntimeError("Inventory byte-count did not stabilize")
inventory_path.write_bytes(body)
os.chmod(inventory_path,0o444)

actual_names={str(path.relative_to(ROOT)) for path in ROOT.rglob("*") if path.is_file()}
inventory_names={entry["path"] for entry in inventory["all_retained_files"]}
if actual_names!=inventory_names: raise RuntimeError("Incomplete retained-file inventory")
for path in ROOT.rglob("*"):
    if path.is_file() and stat.S_IMODE(path.stat().st_mode)!=0o444: raise RuntimeError("Unsealed file")
print(json.dumps({"status":"sealed","inventory":data(inventory_path),"public_allowlist":data(allowlist_path),
                  "retained_file_count":len(actual_names),"first_records_verified_unchanged":True},indent=2))
