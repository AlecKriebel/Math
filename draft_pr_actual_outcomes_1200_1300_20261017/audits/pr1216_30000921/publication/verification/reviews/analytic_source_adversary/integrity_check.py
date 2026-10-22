#!/usr/bin/env python3
"""Current submitted bindings only; historical omitted packets not replayed."""
from hashlib import sha256
from pathlib import Path, PurePosixPath
import json

BASE = Path(__file__).resolve().parent
SUBMITTED = BASE.parent.parent / "submitted"

def require(value, message):
    if not value: raise RuntimeError(message)

def no_duplicate_keys(pairs):
    result = {}
    for k,v in pairs:
        require(k not in result, "duplicate JSON key: "+k)
        result[k] = v
    return result

def read_json(path): return json.loads(path.read_text(),object_pairs_hook=no_duplicate_keys)

def main():
    manifest = read_json(SUBMITTED / "MANIFEST.json")
    members = manifest["members"]
    require(len(members) == len(set(members)),"duplicate member")
    require(set(members) == {p.name for p in SUBMITTED.iterdir()},"closed inventory mismatch")
    require(manifest["self_hash_excluded"] == "MANIFEST.json","unexpected self-exclusion")
    entries = manifest["entries"]
    require({e["file"] for e in entries} == set(members)-{"MANIFEST.json"},"entry coverage")
    require(len(entries) == len({e["file"] for e in entries}),"duplicate entry")
    receipts = {}
    for name in members:
        require(PurePosixPath(name).parts == (name,),"unsafe member")
        p = SUBMITTED / name
        require(not p.is_symlink() and p.is_file(),"member not a regular file")
        for parent in [SUBMITTED, SUBMITTED.parent]: require(not parent.is_symlink(),"submitted parent symlink")
        body = p.read_bytes()
        receipts[name] = {"bytes":len(body),"sha256":sha256(body).hexdigest()}
    for entry in entries:
        require(receipts[entry["file"]] == {"bytes":entry["bytes"],"sha256":entry["sha256"]},"manifest binding mismatch")
    acceptance = read_json(SUBMITTED / "ACCEPTANCE.json")
    for name,binding in acceptance["distributed_document_bindings"].items():
        require(receipts[name] == binding,"distributed binding mismatch")
    require(receipts["PROOF.md"]["sha256"] == "3479117bbe24e0829a31a9ac616c305028ad571aa41647d28b3e7016311f8fe6","assigned proof identity mismatch")
    print(json.dumps({"schema":"current-submitted-integrity-v1","status":"PASS","files":receipts,"current_manifest_closed_set":True,"current_acceptance_distributed_bindings":True,"historical_original_documents_and_omitted_receipts_replayed":False,"scope":"Fresh verification of the eight submitted files. Historical receipt counts and omitted packet hashes are reported metadata only, not reproduced by this check."},sort_keys=True,indent=2))

if __name__ == "__main__": main()
