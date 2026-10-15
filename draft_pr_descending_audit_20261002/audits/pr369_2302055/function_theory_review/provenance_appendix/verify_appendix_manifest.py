#!/usr/bin/env python3
"""Verify exact appendix inventory and unchanged original bindings; read only."""
from pathlib import Path
import hashlib,json
own=Path(__file__).resolve().parent
original=own.parent
m=json.loads((own/"PUBLIC_MANIFEST.json").read_text())
assert m["own_root"]==str(own)
assert m["manifest_self_excluded"] is True
listed=set()
for f in m["files"]:
    rel=Path(f["path"])
    assert not rel.is_absolute() and ".." not in rel.parts
    assert str(rel)!="PUBLIC_MANIFEST.json"
    raw=(own/rel).read_bytes()
    assert len(raw)==f["bytes"] and hashlib.sha256(raw).hexdigest()==f["sha256"]
    assert str(rel) not in listed
    listed.add(str(rel))
actual={str(f.relative_to(own)) for f in own.rglob("*")
        if f.is_file() and f.name!="PUBLIC_MANIFEST.json" and "__pycache__" not in f.parts}
assert actual==listed
receipt=json.loads((own/"ORIGINAL_BINDINGS_RECEIPT.json").read_text())
orig_m_raw=(original/"PUBLIC_MANIFEST.json").read_bytes()
assert hashlib.sha256(orig_m_raw).hexdigest()==receipt["original_public_manifest_sha256"]
orig_m=json.loads(orig_m_raw)
orig_listed=set()
for f in orig_m["files"]:
    raw=(original/f["path"]).read_bytes()
    assert len(raw)==f["bytes"] and hashlib.sha256(raw).hexdigest()==f["sha256"]
    orig_listed.add(f["path"])
orig_actual={str(f.relative_to(original)) for f in original.rglob("*")
             if f.is_file() and "private" not in f.relative_to(original).parts
             and "provenance_appendix" not in f.relative_to(original).parts
             and f.name!="PUBLIC_MANIFEST.json" and "__pycache__" not in f.parts}
assert orig_actual==orig_listed
seal_raw=(original/"MATHEMATICAL_SEAL.json").read_bytes()
assert hashlib.sha256(seal_raw).hexdigest()==receipt["original_mathematical_seal_sha256"]
for name,digest in json.loads(seal_raw)["own_files"].items():
    assert hashlib.sha256((original/name).read_bytes()).hexdigest()==digest
print(json.dumps({"status":"PASS","appendix_bound_files":len(listed),"original_bound_files_unchanged":len(orig_listed),"exact_separate_inventories":True,"manifest_self_excluded":True},indent=2))
