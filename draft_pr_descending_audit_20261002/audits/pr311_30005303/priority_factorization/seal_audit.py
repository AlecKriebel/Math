#!/usr/bin/env python3
"""Seal this audit only, with actual mode/hash observations and no Git operations.

The manifest cannot hash itself. A detached receipt hashes the sealed manifest;
the receipt's own hash is returned to the caller and rechecked externally.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

BASE = Path(__file__).resolve().parent
MANIFEST = BASE / 'FINAL_INPUT_OUTPUT_SHA_MANIFEST.json'
RECEIPT = BASE / 'FINAL_SEAL_RECEIPT.json'

def utc():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds')

def measure(path):
    data = path.read_bytes()
    info = path.stat()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
        'mode': oct(stat.S_IMODE(info.st_mode)), 'mtime_ns': info.st_mtime_ns}

if MANIFEST.exists() or RECEIPT.exists():
    raise SystemExit('Refusing to replace an existing final seal.')
started = utc()
assert measure(BASE/'private_sources/ems_owr_2022_55.pdf')['sha256'] == '56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65'
input_manifest = json.loads((BASE / 'released_candidate_input_manifest.json').read_text())
inputs = []
for item in input_manifest['read_scope_exact']:
    path = Path(item['absolute_path'])
    before = measure(path)
    assert before['sha256'] == item['sha256'] and before['bytes'] == item['bytes']
    assert before['mode'] == item['mode']
    inputs.append({'absolute_path': str(path), 'original_read_record': item,
        'actual_recheck_utc': utc(), 'final_measurement': before,
        'unchanged_since_read': True, 'mode_unchanged_since_read': True, 'written_by_audit': False})

frozen_checks = []
for name in ('source_only_freeze_manifest.json', 'first_priority_freeze_manifest.json', 'older_prior_freeze_manifest.json'):
    prior = json.loads((BASE/name).read_text())
    checked = []
    for item in prior['files']:
        now = measure(BASE/item['path'])
        assert now['sha256'] == item['sha256_after']
        if 'bytes' in item:
            assert now['bytes'] == item['bytes']
        assert now['mode'] == item['final_mode']
        checked.append({'path': item['path'], 'actual_recheck_utc': utc(),
            'measurement': now, 'unchanged_since_prior_seal': True})
    frozen_checks.append({'manifest': name, 'measurement': measure(BASE/name),
        'exact_prior_manifest_content': prior, 'prior_sealed_files_rechecked': checked})

files = sorted(p for p in BASE.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
outputs = []
for path in files:
    before = measure(path)
    at = utc()
    os.chmod(path, 0o444)
    after = measure(path)
    assert before['sha256'] == after['sha256'] and before['bytes'] == after['bytes']
    outputs.append({'relative_path': str(path.relative_to(BASE)), 'old_actual_measurement': before,
        'chmod_actual_utc': at, 'final_actual_measurement': after, 'bytes_unchanged_by_seal': True,
        'private_excluded_from_publication': path.relative_to(BASE).parts[0] in ('private_sources','command_captures')})

obj = {'audit_directory': str(BASE), 'seal_started_actual_utc': started,
    'measurement_completed_actual_utc': utc(), 'candidate_input_rechecks': inputs,
    'earlier_frozen_manifest_checks': frozen_checks, 'audit_files': outputs,
    'exclusions': ['__pycache__ generated Python caches',
        'This manifest does not hash itself; detached receipt does.',
        'Detached receipt does not hash itself; caller receives and rechecks its hash.'],
    'no_publication_or_git_write': True,
    'native_capture_limits': 'Wrapper captures argv/stdout/stderr, not inherited stdin; initial source fetch/render/freeze operations preceded wrapper. Exact session tool transcript remains the earlier native record. See query ledger.'}
MANIFEST.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
manifest_old = measure(MANIFEST)
manifest_at = utc()
os.chmod(MANIFEST,0o444)
manifest_final = measure(MANIFEST)
assert manifest_old['sha256'] == manifest_final['sha256']
receipt = {'actual_receipt_creation_utc': utc(), 'sealed_manifest': {
    'path': str(MANIFEST), 'old_actual_measurement': manifest_old,
    'chmod_actual_utc': manifest_at, 'final_actual_measurement': manifest_final,
    'bytes_unchanged_by_seal': True}, 'sealed_file_count': len(outputs),
    'receipt_self_hash_obtained_after_this_write': True,
    'completion_estimate_percent': 100,
    'completion_scope': 'Bounded independent factorization priority audit and artifact seal complete; no universal literature-exhaustion or C1 novelty claim.'}
RECEIPT.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
receipt_old = measure(RECEIPT)
receipt_at = utc()
os.chmod(RECEIPT,0o444)
receipt_final = measure(RECEIPT)
assert receipt_old['sha256'] == receipt_final['sha256']
print(json.dumps({'finished_actual_utc': utc(), 'manifest': manifest_final,
    'receipt': {'old_actual_measurement': receipt_old, 'chmod_actual_utc': receipt_at,
        'final_actual_measurement': receipt_final, 'bytes_unchanged_by_seal': True},
    'sealed_file_count': len(outputs)},indent=2))
