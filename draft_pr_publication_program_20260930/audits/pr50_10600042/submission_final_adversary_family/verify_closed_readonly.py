#!/usr/bin/env python3
"""Separate ROOT read-only whole-family readback after actual closure."""
from pathlib import Path
import hashlib, json, stat, sys
base=Path(__file__).absolute().parent
assert len(sys.argv)==2, 'supply actual completed closure manifest SHA-256'
sha=lambda b:hashlib.sha256(b).hexdigest()
body=(base/'MANIFEST.json').read_bytes();assert sha(body)==sys.argv[1]
record=json.loads(body)
assert record['schema']=='pr50-final-submission-adversary-manifest/v1'
assert record['root_mathematical_or_publication_approval_conferred'] is False
expected={row['path']:row for row in record['payload']}
actual={p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()}
assert actual==set(expected)|{'MANIFEST.json'} and len(expected)==record['payload_count']
for name,row in expected.items():
    p=base/name;st=p.lstat();assert stat.S_ISREG(st.st_mode) and not p.is_symlink()
    b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(st.st_mode)==row['mode']==0o444
assert stat.S_IMODE((base/'MANIFEST.json').lstat().st_mode)==0o444
dirs={p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_dir()}
assert dirs==set(record['directories'])
for d in ['']+record['directories']:
    p=base/d;assert not p.is_symlink() and stat.S_IMODE(p.lstat().st_mode)==0o555
external=json.loads((base/'COMPLETE_READBACK.json').read_bytes())['external_inputs']
for row in external:
    p=Path(row['path']);assert p.is_file() and not p.is_symlink()
    b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
print(json.dumps({'status':'PASS_SEPARATE_ROOT_FULL_CLOSED_READBACK','payload_count':len(expected),
                  'directories':len(dirs),'external_inputs_full_body_matched':len(external),
                  'manifest_sha256':sha(body),'write_operations_performed':False},indent=2))
