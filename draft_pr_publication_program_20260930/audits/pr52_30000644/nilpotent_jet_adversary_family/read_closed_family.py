"""ROOT-only SOURCE: read whole closed family with no file writes."""
import argparse
import json
from closure_common import F, MF, digest, identity, inspect, read_json

p = argparse.ArgumentParser()
p.add_argument('--expected-index-sha256', required=True)
p.add_argument('--expected-ready-sha256', required=True)
p.add_argument('--expected-manifest-sha256', required=True)
a = p.parse_args()
assert MF.exists() and digest(MF.read_bytes()) == a.expected_manifest_sha256
r = inspect(a.expected_index_sha256, a.expected_ready_sha256, True)
m = read_json(MF)
assert m['schema'] == 'pr52-nilpotent-jet-self-closure/v1'
assert m['index_sha256'] == a.expected_index_sha256 and m['ready_sha256'] == a.expected_ready_sha256
assert m['payload_verified'] is True and m['caller_supplied_after_preparer_exit'] is True
assert m['closure_operator_source'] == identity(F / 'close_family.py')
assert type(m['closure_operator_pid']) is int and m['closure_operator_pid'] > 0
assert m['claimed_process_exit_code'] is None
assert m['process_completion_and_exit_must_be_captured_externally_after_return'] is True
for key in ('file_bindings', 'directories', 'fixed_external_rows', 'capture_count',
            'retained_interrupted_capture_count'):
    assert m[key] == r[key]
for key in ('root_personal_read_attestation', 'native_acceptance_authority',
            'remote_action_authority', 'merged', 'preprint_created', 'doi_created'):
    assert m[key] is False
print(json.dumps({'status': 'READ_ONLY_CLOSED_INDEPENDENT_REVIEW_PASS',
                  'payload_plus_manifest': len(r['file_bindings']) + 1,
                  'manifest_sha256': a.expected_manifest_sha256,
                  'production_or_remote_authority': False}, sort_keys=True))
