#!/usr/bin/env python3
"""Strict, read-only publication verification, including exact file sets."""
import hashlib,json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'PUBLICATION_MANIFEST.json').read_text())
expected={r['path'] for r in manifest['files']}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name!='PUBLICATION_MANIFEST.json'}
assert len(expected)==len(manifest['files'])
assert actual==expected,(sorted(actual-expected),sorted(expected-actual))
for row in manifest['files']:
    b=(root/row['path']).read_bytes()
    assert len(b)==row['bytes'],row['path']
    assert hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
subprocess.run([sys.executable,str(root/'submission/verify_manifest.py')],check=True)
subprocess.run([sys.executable,str(root/'audit/verify_audit_manifest.py')],check=True)
print('Verified %d bound publication files.'%len(expected))
