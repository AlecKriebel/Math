#!/usr/bin/env python3
"""Check this acceptance artifact against its exact safe-file manifest."""
import hashlib, json
from pathlib import Path
NAMES=set(('ACCEPTANCE.md REPORT.md README.md RESULT.json INPUT_BINDING.json SOURCE_CHECK.json '
           'code/verify_delta.py code/targeted_checks.py code/replay_inputs.py code/verify_package.py '
           'results/delta_checks.json results/targeted_checks.json results/input_replays.json MANIFEST.json').split())
root=Path(__file__).resolve().parents[1]
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
if actual!=NAMES: raise ValueError('safe-file allowlist mismatch')
m=json.loads((root/'MANIFEST.json').read_text())
if len(m['files'])!=len(NAMES)-1: raise ValueError('manifest count')
if {e['path'] for e in m['files']}!=NAMES-{'MANIFEST.json'}: raise ValueError('manifest coverage')
for e in m['files']:
    p=root/e['path']
    if p.is_symlink(): raise ValueError('symlink')
    b=p.read_bytes()
    if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise ValueError('hash or size: '+e['path'])
print(json.dumps({'status':'PASS','members_including_manifest':len(NAMES),
                  'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest(),
                  'scope':'Artifact integrity and exact allowlist, not formal mathematical verification'},indent=2))
