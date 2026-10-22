#!/usr/bin/env python3
"""Verify the flat public packet; use the external receipt to pin the manifest."""
import argparse
import hashlib
import json
from pathlib import Path

NAMES = {
    'README.md','PROOF.md','SOURCE_AND_SCOPE.md','RESULT.json',
    'DATASET_VERIFICATION.json','PRIOR_WORK_CHECK.json','SOURCE_METADATA.json',
    'verify_algebra.py','CHECK_RESULTS.json','verify_manifest.py','MANIFEST.json'
}

def verify(root, expected_manifest=None):
    root=Path(root)
    observed={p.name for p in root.iterdir()}
    if observed!=NAMES:
        raise ValueError('Unexpected or missing entries: '+str(sorted(observed^NAMES)))
    for p in root.iterdir():
        if p.is_symlink() or not p.is_file():
            raise ValueError('Only regular files are allowed: '+p.name)
    raw=(root/'MANIFEST.json').read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if expected_manifest and digest!=expected_manifest:
        raise ValueError('Manifest differs from externally pinned digest')
    manifest=json.loads(raw)
    rows=manifest['files']
    if len(rows)!=len(NAMES)-1 or {r['path'] for r in rows}!=NAMES-{'MANIFEST.json'}:
        raise ValueError('Manifest does not list exactly the allowed payload')
    for row in rows:
        b=(root/row['path']).read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:
            raise ValueError('Integrity mismatch: '+row['path'])
    return {'status':'pass','files':len(NAMES),'manifest_sha256':digest,
            'externally_pinned':bool(expected_manifest)}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',default=str(Path(__file__).resolve().parent))
    p.add_argument('--expected-manifest')
    args=p.parse_args()
    print(json.dumps(verify(args.root,args.expected_manifest),indent=2,sort_keys=True))
