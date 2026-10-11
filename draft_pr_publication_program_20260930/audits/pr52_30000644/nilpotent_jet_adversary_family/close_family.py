"""ROOT-only SOURCE. Preparer must exit before ROOT executes this."""
import argparse
import datetime
import json
import os
import sys
from closure_common import F, MF, digest, identity, inspect

p = argparse.ArgumentParser()
p.add_argument('--expected-index-sha256', required=True)
p.add_argument('--expected-ready-sha256', required=True)
p.add_argument('--after-preparer-exit', action='store_true', required=True)
a = p.parse_args()
assert a.after_preparer_exit and not MF.exists()
r = inspect(a.expected_index_sha256, a.expected_ready_sha256, False)
m = {'schema': 'pr52-nilpotent-jet-self-closure/v1',
     'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'closure_operator_pid': os.getpid(), 'closure_operator_argv': sys.argv,
     'closure_operator_source': identity(F / 'close_family.py'),
     'caller_supplied_after_preparer_exit': True,
     'payload_verified': True, 'index_sha256': a.expected_index_sha256,
     'ready_sha256': a.expected_ready_sha256, **r,
     'process_completion_and_exit_must_be_captured_externally_after_return': True,
     'claimed_process_exit_code': None, 'root_personal_read_attestation': False,
     'native_acceptance_authority': False, 'remote_action_authority': False,
     'merged': False, 'preprint_created': False, 'doi_created': False}
with MF.open('xb') as f:
    f.write((json.dumps(m, sort_keys=True, indent=2) + '\n').encode())
    f.flush()
    os.fsync(f.fileno())
MF.chmod(0o444)
for d in r['directories']: (F / d).chmod(0o555)
F.chmod(0o555)
inspect(a.expected_index_sha256, a.expected_ready_sha256, True)
print(json.dumps({'status': 'CLOSED_INDEPENDENT_REVIEW_ONLY', 'manifest_sha256': digest(MF.read_bytes()),
                  'payload_plus_manifest': len(r['file_bindings']) + 1,
                  'production_or_remote_authority': False}, sort_keys=True))
