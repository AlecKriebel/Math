#!/usr/bin/env python3
"""Read-only exact self-excluding closure check for this original audit family."""
from pathlib import Path
import argparse
import hashlib
import json

ap=argparse.ArgumentParser()
ap.add_argument('--family',required=True,type=Path)
args=ap.parse_args()
p=args.family
m=json.loads((p/'MANIFEST.json').read_text())
expected={row['path'] for row in m['files']}
actual={str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and f.relative_to(p).parts[0] not in ('sources','private') and f.name!='MANIFEST.json'}
assert expected==actual,{'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
for row in m['files']:
    b=(p/row['path']).read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
print(json.dumps({'closed_members':len(m['files']),'manifest_sha256':hashlib.sha256((p/'MANIFEST.json').read_bytes()).hexdigest(),'scope':m['scope']}))
