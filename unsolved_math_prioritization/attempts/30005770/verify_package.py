#!/usr/bin/env python3
"""Check the immutable reader inventory, proof identities, and derived audit hashes."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text())
errors=[]
expected={e['path']:e for e in manifest['files']}
actual={str(f.relative_to(ROOT)) for f in ROOT.rglob('*') if f.is_file() and f != ROOT/'PACKAGE_MANIFEST.json'}
for p in sorted(actual-set(expected)):errors.append('Unexpected file: '+p)
for p in sorted(set(expected)-actual):errors.append('Missing file: '+p)
for p,e in expected.items():
 f=ROOT/p
 if f.is_symlink():errors.append('Symlink is not permitted: '+p);continue
 if not f.is_file():continue
 b=f.read_bytes()
 if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:errors.append('Content mismatch: '+p)
transforms=json.loads((ROOT/'TRANSFORMATION_MAP.json').read_text())
for e in transforms['artifacts']:
 f=ROOT/e['path']
 if not f.is_file():errors.append('Mapped artifact missing: '+e['path']);continue
 b=f.read_bytes();h=hashlib.sha256(b).hexdigest()
 if len(b)!=e['public_bytes'] or h!=e['public_sha256']:errors.append('Public transformation pin mismatch: '+e['path'])
 if e['transformation']=='identity' and (h!=e['source_sha256'] or len(b)!=e['source_bytes']):errors.append('Identity transformation mismatch: '+e['path'])
for f in ROOT.rglob('*'):
 if f.is_symlink():errors.append('Symlink is not permitted: '+str(f.relative_to(ROOT)))
result={'status':'PASS' if not errors else 'FAIL','files_verified':len(expected),'copied_artifacts_verified':len(transforms['artifacts']),'scope':'Package integrity only; not a mathematical proof audit.','errors':errors}
print(json.dumps(result,indent=2))
sys.exit(bool(errors))
