#!/usr/bin/env python3
"""Read-only release verification for this audit and its exact author dependency."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

assert __debug__, 'Do not run the verifier with assertions disabled'
parser = argparse.ArgumentParser()
parser.add_argument('--author', default=str(Path(__file__).resolve().parent.parent/'author'))
args = parser.parse_args()
root = Path(__file__).resolve().parent
manifest_path = root/'AUDIT_MANIFEST.json'
assert not manifest_path.is_symlink()
raw = manifest_path.read_bytes()
manifest = json.loads(raw)
expected = {}
for rec in manifest['files']:
    p = Path(rec['path'])
    assert not p.is_absolute() and '..' not in p.parts
    assert rec['path'] not in expected
    expected[rec['path']] = rec
actual = set()
for p in root.rglob('*'):
    assert not p.is_symlink(), 'Audit symlink: '+str(p)
    if p.is_file() and p != manifest_path:
        actual.add(p.relative_to(root).as_posix())
assert actual == set(expected), 'Audit file set mismatch'
for name, rec in expected.items():
    p = root/name
    assert p.suffix in {'.md','.json','.py'}
    b = p.read_bytes()
    assert len(b) == rec['bytes'], name
    assert hashlib.sha256(b).hexdigest() == rec['sha256'], name
run = subprocess.run([sys.executable, '-B', str(root/'binding_checks.py'), '--author', args.author], check=True, capture_output=True, text=True)
author = json.loads(run.stdout)
assert author['manifest_sha256'] == manifest['author_manifest_sha256']
assert author['author_tree_sha256'] == manifest['author_tree_sha256']
saved_binding = json.loads((root/'AUDIT_BINDING.json').read_text())
assert saved_binding['files'] == author['files']
assert saved_binding['negative_control_count'] == 7
assert all(x['status']=='REJECTED' for x in saved_binding['negative_controls'])
controls = json.loads((root/'INDEPENDENT_CONTROL_RESULTS.json').read_text())
assert controls['status']=='PASS' and controls['negative_control_count']==10
assert all(x['status']=='REJECTED' for x in controls['negative_controls'].values())
sources = json.loads((root/'SOURCE_RETRIEVAL_CHECKS.json').read_text())['results']
assert len(sources)==6 and all(x['matches_author_private_pdf'] for x in sources)
print(json.dumps({'status':'PASS','author_total_files':author['total_bound_files'],
                  'audit_payload_files':len(expected),
                  'author_manifest_sha256':author['manifest_sha256'],
                  'author_tree_sha256':author['author_tree_sha256'],
                  'audit_manifest_sha256':hashlib.sha256(raw).hexdigest(),
                  'source_pdf_hash_matches':len(sources),
                  'arithmetic_negative_controls':controls['negative_control_count'],
                  'integrity_negative_controls':saved_binding['negative_control_count'],
                  'verdict':manifest['verdict'],
                  'full_solution_claimed':False},indent=2,sort_keys=True))
