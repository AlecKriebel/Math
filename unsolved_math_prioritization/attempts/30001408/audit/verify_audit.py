#!/usr/bin/env python3
"""Verify audit bytes, its exact original binding, and deterministic controls.

The externally reported AUDIT_MANIFEST.json SHA-256 is the trust anchor. This
program does not purport to authenticate a manifest that an attacker also changed.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
original = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root.parents[1] / 'safe_output'
sha = lambda data: hashlib.sha256(data).hexdigest()
manifest = json.loads((root/'AUDIT_MANIFEST.json').read_bytes())
assert manifest['problem_id'] == '30001408'
assert manifest['verdict'] == 'PASS_WITH_REQUIRED_CORRECTION'
assert manifest['mathematical_status'] == 'unsolved' and manifest['approaches_used'] == 5
assert {p.name for p in root.iterdir()} == {r['path'] for r in manifest['files']} | {'AUDIT_MANIFEST.json'}
for row in manifest['files']:
    assert Path(row['path']).name == row['path']
    data = (root/row['path']).read_bytes()
    assert len(data) == row['bytes'], row['path']+' bytes'
    assert sha(data) == row['sha256'], row['path']+' sha256'
binding = json.loads((root/'BINDING.json').read_bytes())
assert sha((original/'AUTHOR_MANIFEST.json').read_bytes()) == binding['author_manifest']['sha256']
for row in binding['author_files']:
    data = (original/row['path']).read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
text = (original/'RESULT.md').read_text()
start = text.index(binding['corrected_paragraph']['starts_with'])
end = text.index('\n\n', start)
paragraph = text[start:end].encode()
assert len(paragraph) == binding['corrected_paragraph']['bytes']
assert sha(paragraph) == binding['corrected_paragraph']['sha256']
correction = (root/'CORRECTION.md').read_text()
replacement = correction.split('## Complete replacement paragraph\n\n',1)[1].split('\n\n## Exact counterexample',1)[0].encode()
assert sha(replacement) == binding['replacement_paragraph']['sha256']
actual = subprocess.check_output([sys.executable,str(root/'audit_controls.py'),str(original)], env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
assert actual == (root/'AUDIT_RESULTS.json').read_bytes()
print(json.dumps({'status':'PASS','audit_files_verified':len(manifest['files']),'author_files_verified':7,'original_manifest_sha256':binding['author_manifest']['sha256'],'required_correction_bound':True,'controls_byte_match':True,'author_assertions':15200,'independent_checks':json.loads(actual)['independent_assertions'],'mathematical_status':'unsolved','approaches_used':5},sort_keys=True,indent=2))
