#!/usr/bin/env python3
"""Verify the self-excluding first-party family manifest without writing."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root/'MANIFEST.json').read_text())
excluded = {'tmp','cache','sources','__pycache__'}
actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
          if p.is_file() and p.name != 'MANIFEST.json'
          and not (set(p.relative_to(root).parts) & excluded)}
listed = {f['path'] for f in manifest['files']}
assert actual == listed, {'missing':sorted(listed-actual),'unlisted':sorted(actual-listed)}
assert len(listed) == len(manifest['files'])
for f in manifest['files']:
    b=(root/f['path']).read_bytes()
    assert len(b)==f['size'],f['path']
    assert hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
seal=json.loads((root/'EARLY_SEAL.json').read_text())
assert seal['sealed_utc']=='2026-10-02T01:12:16.919584+00:00'
assert hashlib.sha256((root/'EARLY_SEAL.json').read_bytes()).hexdigest()==(root/'EARLY_SEAL.sha256').read_text().split()[0]
assert json.loads((root/'controls_results.json').read_text())['pass']
print(json.dumps({'pass':True,'files':len(listed),'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()},indent=2))
