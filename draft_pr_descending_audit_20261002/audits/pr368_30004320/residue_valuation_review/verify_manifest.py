#!/usr/bin/env python3
"""Read-only exact public-scope/seal verification."""
from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent
M=json.loads((D/'PUBLIC_MANIFEST.json').read_bytes())
actual={str(f.relative_to(D))for f in D.rglob('*')if f.is_file()and 'private'not in f.relative_to(D).parts and '__pycache__'not in f.relative_to(D).parts and f.name!='PUBLIC_MANIFEST.json'}
assert actual=={r['path']for r in M['files']}
for r in M['files']:
 b=(D/r['path']).read_bytes();assert len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
for name in ['SOURCE_FIRST_SEAL.json','MATHEMATICAL_SEAL.json']:
 a=json.loads((D/name).read_bytes());b=(D/a['file']).read_bytes();assert len(b)==a['bytes']and hashlib.sha256(b).hexdigest()==a['sha256']
print(json.dumps({'status':'PASS','public_files':len(M['files']),'immutable_original_seals':2},sort_keys=True))
