#!/usr/bin/env python3
"""Verify the portable audit manifest and optionally the precise audited input."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
p=Path(__file__).resolve().parent
args=argparse.ArgumentParser()
args.add_argument('--input-zip')
a=args.parse_args()
manifest=json.loads((p/'MANIFEST.json').read_text())
records={r['path']:r for r in manifest['files']}
actual={str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and f.name!='MANIFEST.json' and '__pycache__' not in f.parts}
assert actual==set(records),('file set mismatch',sorted(actual^set(records)))
for name,r in records.items():
    b=(p/name).read_bytes()
    assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],name
out={'audit_manifest':'PASS','payload_files_verified':len(records)}
if a.input_zip:
    expected=json.loads((p/'AUDIT_BINDING.json').read_text())['input_zip']
    b=Path(a.input_zip).read_bytes()
    assert len(b)==expected['bytes'] and hashlib.sha256(b).hexdigest()==expected['sha256']
    with zipfile.ZipFile(a.input_zip) as z:
        assert sorted(z.namelist())==sorted(r['path'] for r in expected['members'])
        for r in expected['members']:
            b=z.read(r['path'])
            assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
    out['frozen_input_binding']='PASS'
    out['frozen_input_members_verified']=len(expected['members'])
print(json.dumps(out,sort_keys=True))
