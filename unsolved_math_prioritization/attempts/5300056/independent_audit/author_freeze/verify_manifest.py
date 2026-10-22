#!/usr/bin/env python3
"""Verify only the present sanitized payload. Omitted sources are not checked."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={e['path']:e for e in manifest['files']}
actual={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
assert set(actual)==set(expected),('payload_file_set_mismatch',sorted(set(actual)^set(expected)))
for name,p in sorted(actual.items()):
    assert p.suffix in {'.md','.json','.py'},('disallowed_extension',name)
    assert '/' not in name,('unexpected_subdirectory',name)
    blob=p.read_bytes()
    assert len(blob)==expected[name]['bytes'],('size_mismatch',name)
    assert hashlib.sha256(blob).hexdigest()==expected[name]['sha256'],('hash_mismatch',name)
print(json.dumps({'status':'PASS','payload_files':len(actual),'scope':'Only the present sanitized authored payload was checked; omitted sources and mathematical validity are not certified.'},sort_keys=True))
