#!/usr/bin/env python3
"""Verify bound author and audit bytes without network or mutation."""
import hashlib,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
source=Path(sys.argv[1]) if len(sys.argv)>1 else root.parent/'submission'
m=json.loads((root/'AUDIT_MANIFEST.json').read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert sha(source/'SHA256SUMS.json')==m['reviewed_author_manifest_sha256']
assert sha(source/'PARTIAL.md')==m['reviewed_partial_sha256']
a=json.loads((source/'SHA256SUMS.json').read_text())
assert {r['path'] for r in a['files']}=={p.name for p in source.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'}
assert {r['path'] for r in m['files']}=={p.name for p in root.iterdir() if p.is_file() and p.name!='AUDIT_MANIFEST.json'}
for directory,rows in [(source,a['files']),(root,m['files'])]:
    for row in rows:
        p=directory/row['path']
        assert p.stat().st_size==row['bytes'],p.name
        assert sha(p)==row['sha256'],p.name
print('Verified bound author manifest, 11 author files, and %s audit files.'%len(m['files']))
