#!/usr/bin/env python3
"""Verify exact author file set, byte sizes, hashes, and stored control replay."""
import hashlib,json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'SHA256SUMS.json').read_text())
paths=[x['path'] for x in m['files']]
assert len(paths)==len(set(paths)), 'duplicate manifest paths'
assert all(Path(n).name==n and n!='SHA256SUMS.json' for n in paths)
assert not any(p.is_symlink() for p in root.iterdir()),'symlink in packet'
expected=set(paths)
actual={p.name for p in root.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'}
assert expected==actual, (sorted(expected-actual),sorted(actual-expected))
assert not any(p.is_dir() for p in root.iterdir()),'unmanifested subdirectory'
for row in m['files']:
    b=(root/row['path']).read_bytes()
    assert len(b)==row['bytes'],row['path']
    assert hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
replay=json.loads(subprocess.check_output([sys.executable,str(root/'verify.py')],text=True))
assert replay==json.loads((root/'CONTROL_RESULTS.json').read_text()),'control replay differs'
assert json.loads((root/'STATUS.json').read_text())['status']=='already_solved'
print('Verified %d frozen files and exact control replay.'%len(expected))
