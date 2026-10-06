#!/usr/bin/env python3
"""Verify this own-root, self-excluded review manifest without modifying files."""
from pathlib import Path
import json,hashlib
own=Path(__file__).resolve().parent
manifest=json.loads((own/"PUBLIC_MANIFEST.json").read_text())
assert manifest["own_root"]==str(own)
assert manifest["manifest_self_excluded"] is True
listed=set()
for entry in manifest["files"]:
    rel=Path(entry["path"])
    assert not rel.is_absolute() and ".." not in rel.parts
    assert rel.parts[0]!="private" and str(rel)!="PUBLIC_MANIFEST.json"
    raw=(own/rel).read_bytes()
    assert len(raw)==entry["bytes"]
    assert hashlib.sha256(raw).hexdigest()==entry["sha256"]
    assert str(rel) not in listed
    listed.add(str(rel))
expected={str(p.relative_to(own)) for p in own.rglob("*")
          if p.is_file() and "private" not in p.relative_to(own).parts
          and p.name!="PUBLIC_MANIFEST.json" and "__pycache__" not in p.parts}
assert listed==expected,(listed^expected)
print(json.dumps({"status":"PASS","public_bound_files":len(listed),"self_excluded":True,"private_excluded":True},indent=2))
