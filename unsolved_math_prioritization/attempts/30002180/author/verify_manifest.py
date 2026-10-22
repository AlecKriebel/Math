#!/usr/bin/env python3
"""Verify a frozen plain-file allowlist, sizes, and SHA-256 hashes."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
m=json.loads((p/'MANIFEST.json').read_text())
expected={x['path'] for x in m['files']}|{'MANIFEST.json'}
actual={x.name for x in p.iterdir()}
assert actual==expected, {'unexpected':sorted(actual-expected),'missing':sorted(expected-actual)}
for item in m['files']:
 f=p/item['path']
 assert f.is_file() and not f.is_symlink(),f
 b=f.read_bytes()
 assert len(b)==item['bytes'],f
 assert hashlib.sha256(b).hexdigest()==item['sha256'],f
print(json.dumps({'manifest_verified':True,'files_verified':len(m['files']),'original_problem_solved':False},sort_keys=True))
