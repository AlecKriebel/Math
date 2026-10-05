#!/usr/bin/env python3
"""Read-only hash/inventory binding and finite diagnostic replay, not a topology proof."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
AUTHOR = '579a41fb8e474f60df00a4ecfe5d40e221e885385d5b8ee12557a9d7d32bdc37'
AUDIT = 'b4325adb6ec6d117e52c5b2f0f7a3aede535b0b717a1bc705536de6b9b71f32f'
ADDENDUM = 'd14b3c6f7489574c1ddd7d7a57fc99df625c8bdb4dbb9fe280642e6e5199b9e0'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def inventory(root):
    entries = list(root.rglob('*'))
    require(not any(p.is_symlink() for p in entries), 'Symlinks are not permitted')
    require(all(p.is_dir() or p.is_file() for p in entries), 'Nonregular file')
    return {p.relative_to(root).as_posix() for p in entries if p.is_file()}

def checked_path(root, name):
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and '.' not in path.parts,
            'Unsafe manifest path')
    return root / name

def checksums(root):
    entries = {}
    for line in (root / 'SHA256SUMS').read_text().splitlines():
        sha, name = line.split('  ', 1)
        require(name not in entries, 'Duplicate checksum entry')
        entries[name] = sha
        require(digest(checked_path(root, name).read_bytes()) == sha, 'Hash mismatch: ' + name)
    require(inventory(root) == set(entries) | {'SHA256SUMS'}, 'Unexpected or missing file')
    return entries

def json_manifest(root, filename, expected):
    require(digest((root / filename).read_bytes()) == expected, 'Immutable manifest changed: ' + filename)
    data = json.loads((root / filename).read_text())
    names = []
    for item in data['files']:
        name = item['path']
        names.append(name)
        raw = checked_path(root, name).read_bytes()
        require(len(raw) == item['bytes'] and digest(raw) == item['sha256'], 'Manifest mismatch: ' + name)
    require(len(set(names)) == len(names), 'Duplicate manifest entry')
    require(inventory(root) == set(names) | {filename, 'SHA256SUMS'}, 'Manifest inventory mismatch')
    checksums(root)

def validate():
    release = checksums(ROOT)
    json_manifest(ROOT / 'author', 'AUTHOR_MANIFEST.json', AUTHOR)
    json_manifest(ROOT / 'audit', 'AUDIT_MANIFEST.json', AUDIT)
    require(digest((ROOT / 'audit/CONTROLLING_ADDENDUM.md').read_bytes()) == ADDENDUM,
            'Controlling addendum changed')
    binding = json.loads((ROOT / 'audit/FREEZE_BINDING.json').read_text())
    require(binding['author_manifest_expected_sha256'] == AUTHOR, 'Wrong author binding')
    require({x['path'] for x in binding['files']} == inventory(ROOT / 'author'), 'Freeze inventory mismatch')
    for entry in binding['files']:
        raw = (ROOT / 'author' / entry['path']).read_bytes()
        require(len(raw) == entry['bytes'] and digest(raw) == entry['sha256'], 'Audit freeze mismatch')
    status = json.loads((ROOT / 'RELEASE_STATUS.json').read_text())
    require(status['disposition'] == 'unsolved' and status['turns'] == '5/5', 'Release disposition changed')
    require(status['controlling_addendum'] == 'audit/CONTROLLING_ADDENDUM.md', 'Addendum not controlling')
    return release

def replay(script, saved):
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    run = subprocess.run([sys.executable, '-B', str(ROOT / script)], cwd=ROOT,
                         env=env, capture_output=True, check=True)
    require(not run.stderr, 'Unexpected stderr: ' + script)
    require(run.stdout == (ROOT / saved).read_bytes(), 'Replay output mismatch: ' + script)
    return json.loads(run.stdout)

before = validate()
author = replay('author/check_controls.py', 'author/CONTROL_RESULTS.json')
independent = replay('audit/independent_controls.py', 'audit/INDEPENDENT_RESULTS.json')
verification = replay('audit/verify_audit.py', 'audit/VERIFICATION_RESULTS.json')
mutations = replay('audit/integrity_negative_controls.py', 'audit/INTEGRITY_NEGATIVE_RESULTS.json')
require(author['total_assertions'] == 226926 and independent['total_assertions'] == 22339,
        'Unexpected diagnostic totals')
require(len(independent['negative_controls']) == 13 and mutations['mutation_count'] == 6,
        'Unexpected negative-control totals')
require(all(x['rejected'] for x in mutations['mutations']), 'Mutation accepted')
require(validate() == before, 'Release changed during execution')
print(json.dumps({'result': 'PASS_RELEASE_BINDINGS_AND_FINITE_DIAGNOSTIC_REPLAY',
    'problem_id': 2890, 'disposition': 'unsolved', 'turns': '5/5',
    'controlling_addendum_sha256': ADDENDUM, 'frozen_author_files': 10,
    'frozen_audit_files': 14, 'release_files': len(before) + 1,
    'author_assertions': 226926, 'independent_assertions': 22339,
    'mathematical_negative_controls': 13, 'integrity_mutations_rejected': 6,
    'outputs_byte_identical': True, 'original_freezes_preserved': True,
    'source_downloads_replayed': False, 'geometric_realization_certified': False,
    'ci_pass_claim': False}, indent=2, sort_keys=True))
