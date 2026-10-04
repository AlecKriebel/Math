#!/usr/bin/env python3
"""Read-only verification of frozen v1 and ROOT replay provenance."""
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent.parent
EXPECTED_HEAD = '5cc1602c05d79502defb07cec7027963149494d2'
EXPECTED_V1_MANIFEST = '1c272d87a1b06ed2b3c992a2b47a356ef204998d40da887ef61d4e126dc23f55'
EXPECTED_ROOT_RECEIPT = 'a364bf6677ea27664f962d28100670820e0e2fc2f5fc66f3aa985fe476b38d95'
manifest_data = (BASE / 'SELF_MANIFEST.json').read_bytes()
assert hashlib.sha256(manifest_data).hexdigest() == EXPECTED_V1_MANIFEST
manifest = json.loads(manifest_data)
assert manifest['immutable_head'] == EXPECTED_HEAD
for entry in manifest['artifacts']:
    data = (BASE / entry['path']).read_bytes()
    assert len(data) == entry['bytes']
    assert hashlib.sha256(data).hexdigest() == entry['sha256']
rows = [json.loads(line) for line in (BASE / 'ACTUAL_COMMANDS.jsonl').read_text().splitlines()]
assert len(rows) == 12
pid_names = {'pid', 'child_pid', 'actual_pid', 'PID', 'actual_child_pid'}
assert all(not (pid_names & set(row)) for row in rows)
auth = json.loads((BASE / 'AUTHENTICATED_INPUTS.json').read_text())
original = BASE.parent / 'original_source_authentication_20261004' / 'original'
for entry in auth['artifacts']:
    assert hashlib.sha256((original / entry['path']).read_bytes()).hexdigest() == entry['sha256']
root_path = BASE.parent / 'ROOT_reproduction_20261004' / 'NEW_FAMILIES_READBACK.json'
root_data = root_path.read_bytes()
assert hashlib.sha256(root_data).hexdigest() == EXPECTED_ROOT_RECEIPT
root = json.loads(root_data)
execution = next(e for e in root['executions'] if e['family'] == 'factorization')
assert execution['exit_code'] == 0 and execution['actual_pid'] == 69186
assert execution['exact_prior_receipt_reproduced'] is True
assert execution['finite_controls_are_proof'] is False
for key in ('stdout', 'stderr', 'original_code', 'executed_code'):
    entry = execution[key]
    data = Path(entry['path']).read_bytes()
    assert len(data) == entry['bytes']
    assert hashlib.sha256(data).hexdigest() == entry['sha256']
assert Path(execution['stdout']['path']).read_bytes() == (BASE / 'EXACT_CONTROL_RESULTS.json').read_bytes()
print(json.dumps({
    'result': 'PASS',
    'immutable_head': EXPECTED_HEAD,
    'frozen_v1_manifest_sha256': EXPECTED_V1_MANIFEST,
    'v1_manifest_members_unchanged': len(manifest['artifacts']),
    'original_candidate_bodies_unchanged': len(auth['artifacts']),
    'original_command_rows_without_recorded_pid': [r['label'] for r in rows],
    'retrospective_pid_assignment': False,
    'root_replay_receipt_sha256': EXPECTED_ROOT_RECEIPT,
    'root_recorded_factorization_child_pid': execution['actual_pid'],
    'root_replay_stream_and_source_hashes_pass': True,
    'root_replay_reproduces_4534_control_receipt_byte_for_byte': True,
    'new_proof_attempts': 0,
}, indent=2))
