#!/usr/bin/env python3
from pathlib import Path
import datetime,hashlib,json,os,stat
D=Path(__file__).resolve().parent
excluded={"OUTPUT_MANIFEST.json","SEAL_RECEIPT.json"}
private=("private_sources/","private_review_materials/","actual_operations/final_seal/")
def pin(p):
    data=p.read_bytes()
    return {"path":p.relative_to(D).as_posix(),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
verdict=json.loads((D/"VERDICT.json").read_text())
if verdict["required_findings"] or verdict["optional_findings"]:raise ValueError("findings not reflected")
if verdict["publication_ready"] or verdict["novelty_established"] or verdict["combined_priority_clearance"]:raise ValueError("scope")
files=[]
for p in sorted(D.rglob("*")):
    rel=p.relative_to(D).as_posix()
    if rel in excluded or rel.startswith(private):continue
    if p.is_symlink():raise ValueError("symlink "+rel)
    if p.is_file():
        if not stat.S_ISREG(p.stat().st_mode):raise ValueError("mode")
        files.append(pin(p))
if not {"REPORT.md","VERDICT.json","INPUT_AUTHENTICATION.json","PRIVATE_SOURCE_CUSTODY.json","WEB_QUERY_LEDGER.json","quantity_transfer_controls.py"}<=set(r["path"] for r in files):raise ValueError("missing")
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest={"schema":"pr110-classical-priority-public-manifest/v1","UTC":utc,"actual_sealer_PID":os.getpid(),"payload":files,"payload_file_count":len(files),"payload_bytes":sum(r["bytes"] for r in files),"excluded_private_prefixes":list(private[:2]),"closing_process_envelope_excluded_prefix":private[2],"required_findings":[],"optional_findings":[]}
(D/"OUTPUT_MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
seal={"schema":"pr110-classical-priority-seal/v1","UTC":utc,"actual_sealer_PID":os.getpid(),"REPORT":pin(D/"REPORT.md"),"VERDICT":pin(D/"VERDICT.json"),"OUTPUT_MANIFEST":pin(D/"OUTPUT_MANIFEST.json"),"payload_file_count":len(files),"required_findings":[],"optional_findings":[],"family_clearance":True,"novelty_established":False,"publication_ready":False,"closing_actual_process_receipt":"actual_operations/final_seal/execution.json","closing_receipt_will_be_written_after_this_process_returns":True}
(D/"SEAL_RECEIPT.json").write_text(json.dumps(seal,indent=2,sort_keys=True)+"\n")
print(json.dumps(seal,sort_keys=True))

