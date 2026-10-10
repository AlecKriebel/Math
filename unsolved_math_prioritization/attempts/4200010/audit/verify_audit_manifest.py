#!/usr/bin/env python3
"""Validate the portable audit allowlist and exact bytes."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
rows={r['path']:r for r in manifest['files']}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() or p.is_symlink()}
assert actual==set(rows)|{'AUDIT_MANIFEST.json'},'Audit inventory differs'
for name,row in rows.items():
    p=root/name
    assert not p.is_symlink(),name
    b=p.read_bytes()
    assert len(b)==row['bytes'],name
    assert hashlib.sha256(b).hexdigest()==row['sha256'],name
print(json.dumps({'result':'PASS','audit_manifest_sha256':hashlib.sha256((root/'AUDIT_MANIFEST.json').read_bytes()).hexdigest(),'verified_audit_files':len(rows)},sort_keys=True))
