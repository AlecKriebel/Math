#!/usr/bin/env python3
"""Verify the audit's plain-file allowlist, sizes and SHA-256 hashes."""
from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
m=json.loads((p/'MANIFEST.json').read_text())
expected={row['path'] for row in m['files']}|{'MANIFEST.json'}
assert {f.name for f in p.iterdir()}==expected
for row in m['files']:
    assert Path(row['path']).name==row['path']
    f=p/row['path'];assert f.is_file() and not f.is_symlink()
    data=f.read_bytes()
    assert len(data)==row['bytes']
    assert hashlib.sha256(data).hexdigest()==row['sha256']
assert json.loads(subprocess.check_output([sys.executable,str(p/'independent_controls.py')]))==json.loads((p/'INDEPENDENT_RESULTS.json').read_text())
print(json.dumps({'audit_manifest_verified':True,'files_verified':len(m['files']),'independent_controls_reproduced':True,'original_problem_solved':False},sort_keys=True))
