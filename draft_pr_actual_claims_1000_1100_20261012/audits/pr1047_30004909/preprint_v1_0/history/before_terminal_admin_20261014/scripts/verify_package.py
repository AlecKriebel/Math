#!/usr/bin/env python3
"""Verify extracted authored package; no outside files or services needed."""
import hashlib
import json
import pathlib
import stat

ROOT = pathlib.Path(__file__).resolve().parent.parent
def require(ok, message):
    if not ok:
        raise RuntimeError(message)
def get(name):
    path = pathlib.PurePosixPath(name)
    require(not path.is_absolute() and not any(p in ('', '.', '..') for p in path.parts) and '\\' not in name, 'unsafe path')
    p = ROOT.joinpath(*path.parts)
    require(p.is_file() and not p.is_symlink() and stat.S_ISREG(p.stat().st_mode), 'not regular: ' + name)
    require(p.resolve().is_relative_to(ROOT), 'outside root')
    return p.read_bytes()
def check(name, size, digest):
    data = get(name)
    require(len(data) == size and hashlib.sha256(data).hexdigest() == digest, 'hash mismatch: ' + name)

manifest = json.loads(get('MANIFEST.json'))
allow = json.loads(get('ALLOWLIST.json'))['members']
require(allow == sorted(set(allow)), 'allowlist duplicates/order')
require(manifest['members'] == allow + ['MANIFEST.json'], 'manifest membership')
require([e['path'] for e in manifest['entries']] == allow, 'manifest exact entry coverage')
for row in manifest['entries']:
    check(row['path'], row['bytes'], row['sha256'])
copies = json.loads(get('EVIDENCE_COPY_MAP.json'))['copies']
require(len({c['package_path'] for c in copies}) == len(copies), 'duplicate evidence paths')
for row in copies:
    check(row['package_path'], row['bytes'], row['sha256'])
accepted = json.loads(get('evidence/ROOT_MATH_ACCEPTANCE.json'))
require(len(accepted['original_files']) == 9, 'original edition count')
for row in accepted['original_files']:
    check('evidence/' + row['snapshot_path'], row['bytes'], row['sha256'])
metadata = json.loads(get('zenodo_metadata.json'))
require(set(metadata) == {'metadata'}, 'request wrapper')
require(metadata['metadata'] == json.loads(get('.zenodo.json')), 'metadata mismatch')
require(metadata['metadata']['title'] == 'An elementary obstruction to same-ground-set matroid-rank approximation', 'title mismatch')
state = json.loads(get('CURRENT_REVIEW_STATE.json'))
require(state['publication_ready'] is False and state['all_issues_resolved'] is False, 'preparation-stage operational hold')
adapt = json.loads(get('CHECKER_ADAPTATION.json'))
original = get(adapt['source'])
portable = get(adapt['portable_copy'])
require(hashlib.sha256(original).hexdigest() == adapt['source_sha256'], 'checker source identity')
require(hashlib.sha256(portable).hexdigest() == adapt['portable_sha256'], 'portable checker identity')
require(original.decode().count(adapt['before']) == 1 and original.decode().replace(adapt['before'], adapt['after']) == portable.decode(), 'checker adaptation scope')
require('zenodo-deposit.json' not in manifest['members'] and not any('sources/raw/' in p for p in allow), 'redistribution boundary')
print(json.dumps({'status': 'PASS', 'manifest_entries': len(allow), 'evidence_copies': len(copies), 'exact_originals': 9,
                  'metadata_equivalence': True, 'portable_adaptation': True, 'historical_labels_are_stage_scoped': True}))
