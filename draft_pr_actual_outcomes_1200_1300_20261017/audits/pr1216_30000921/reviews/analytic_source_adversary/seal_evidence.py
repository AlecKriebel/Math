#!/usr/bin/env python3
"""Seal current local review artifacts, excluding ignored source bodies and self-manifest."""
from pathlib import Path
from hashlib import sha256
import json

BASE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok: raise RuntimeError(message)

def main():
    receipts = [(BASE/name).read_bytes() for name in ["exact_normal.json","exact_optimized.json","exact_optimized_docstrings.json"]]
    require(receipts[0] == receipts[1] == receipts[2],"interpreter receipts differ")
    exact = json.loads(receipts[0])
    require(exact["program_sha256"] == sha256((BASE/"exact_checks.py").read_bytes()).hexdigest(),"exact program changed")
    require(exact["status"] == "PASS","exact check failed")
    require(json.loads((BASE/"integrity_receipt.json").read_text())["status"] == "PASS","integrity check failed")
    require(json.loads((BASE/"VERDICT.json").read_text())["status"] == "PASS_ANALYTIC_AND_SOURCE_SCOPE","verdict mismatch")
    for source in json.loads((BASE/"source_receipt.json").read_text())["sources"]:
        body = (BASE/"sources"/(source["name"]+".pdf")).read_bytes()
        require(len(body) == source["bytes"] and sha256(body).hexdigest() == source["sha256"],"fresh source body changed")
        require(source["matches_submitted_historical_pdf_hash"],"source identity mismatch")
        for page in source["text_pages_extracted"]:
            require((BASE/"sources"/(source["name"]+"_p"+str(page)+".txt")).is_file(),"source text missing")
        for page in source["pages_rendered"]:
            require((BASE/"sources"/(source["name"]+"_p"+str(page)+".png")).is_file(),"source render missing")
    entries = []
    for path in sorted(BASE.iterdir()):
        if path.name in {"sources","__pycache__","EVIDENCE.json"}: continue
        require(path.is_file() and not path.is_symlink(),"unexpected nonregular artifact")
        body = path.read_bytes()
        if path.suffix == ".json": json.loads(body)
        entries.append({"file":path.name,"bytes":len(body),"sha256":sha256(body).hexdigest()})
    evidence = {"schema":"analytic-source-review-evidence-v1","status":"PASS","scope":"Local non-source artifact bindings, not an outside seal or historical receipt replay.","excluded":["sources/","__pycache__/","EVIDENCE.json"],"exact_receipts_byte_identical":True,"entries":entries}
    (BASE/"EVIDENCE.json").write_text(json.dumps(evidence,indent=2)+"\n")
    print(json.dumps({"status":"PASS","non_source_members":len(entries),"evidence_sha256":sha256((BASE/"EVIDENCE.json").read_bytes()).hexdigest()},sort_keys=True))

if __name__ == "__main__": main()
