#!/usr/bin/env python3
"""Verify the exact safe audit package, optionally also the untouched author ZIP."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

p = argparse.ArgumentParser()
p.add_argument('--author-freeze', type=Path)
a = p.parse_args()
root = Path(__file__).resolve().parent
manifest = json.loads((root / 'AUDIT_MANIFEST.json').read_text())
expected = {x['path'] for x in manifest['files']}
actual = {str(f.relative_to(root)) for f in root.rglob('*')
          if f.is_file() and '__pycache__' not in f.parts and f.name != 'AUDIT_MANIFEST.json'}
assert actual == expected, ('Unexpected or missing files', actual ^ expected)
for item in manifest['files']:
    path = root / item['path']
    assert not path.is_symlink()
    data = path.read_bytes()
    assert len(data) == item['bytes'], item['path']
    assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']
assert manifest['problem_id'] == 2623
assert manifest['problem_result'] == 'unresolved_after_five_approaches'
assert manifest['release_gate'] == 'pending_separate_v2_and_delta_acceptance'
if a.author_freeze:
    data = a.author_freeze.read_bytes()
    frozen = manifest['author_freeze']
    assert len(data) == frozen['bytes']
    assert hashlib.sha256(data).hexdigest() == frozen['sha256']
    with zipfile.ZipFile(a.author_freeze) as z:
        assert len(z.namelist()) == frozen['files']
        assert hashlib.sha256(z.read('AUTHOR_MANIFEST.json')).hexdigest() == frozen['manifest_sha256']
        author = json.loads(z.read('AUTHOR_MANIFEST.json'))
        assert set(z.namelist()) == {x['path'] for x in author['files']} | {'AUTHOR_MANIFEST.json'}
        for item in author['files']:
            payload = z.read(item['path'])
            assert len(payload) == item['bytes']
            assert hashlib.sha256(payload).hexdigest() == item['sha256']
print(json.dumps({'ok': True, 'audit_files': len(expected)+1,
                  'original_author_zip_checked': bool(a.author_freeze),
                  'release_gate': manifest['release_gate']}, sort_keys=True))
