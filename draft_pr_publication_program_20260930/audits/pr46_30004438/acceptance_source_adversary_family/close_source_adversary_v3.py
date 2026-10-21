#!/usr/bin/env python3
"""ROOT-only own closure with the exact one-path dated native qualification."""
from datetime import datetime, timezone
import hashlib
import json
import os
import sys
from verify_closed_source_v3 import F, SELF, inventory, captures, external_bindings, original_bodies, check_verdict, v2_bodies, verify

assert __debug__ and sys.flags.optimize == 0
EXPECTED_PAYLOAD_COUNT = 94
EXPECTED_PATHS_SHA256 = 'fea082d82292eedc7b29e44ed32ebb8db3b22d96143316871a6ad8891981e63b'


if __name__ == '__main__':
    assert not (F / SELF).exists()
    files, dirs = inventory()
    names = [p.relative_to(F).as_posix() for p in files]
    assert len(files) == EXPECTED_PAYLOAD_COUNT
    assert hashlib.sha256(('\n'.join(names) + '\n').encode()).hexdigest() == EXPECTED_PATHS_SHA256
    verdict = check_verdict()
    preserved = original_bodies()
    preserved_v2 = v2_bodies()
    actual_captures = captures()
    foreign = external_bindings()
    payload = []
    for path in files:
        raw = path.read_bytes()
        path.chmod(0o444)
        payload.append({'path': path.relative_to(F).as_posix(), 'bytes': len(raw),
                        'sha256': hashlib.sha256(raw).hexdigest(), 'full_mode': path.stat().st_mode & 0o7777})
    for path in dirs:
        path.chmod(0o755 if path == F else 0o700)
    directory_rows = sorted([{'path': '.' if p == F else p.relative_to(F).as_posix(),
                              'full_mode': p.stat().st_mode & 0o7777} for p in dirs], key=lambda row: row['path'])
    mf = {'schema': 'pr46-acceptance-source-adversary-self-closure/v3',
          'actual_closing_child_pid': os.getpid(), 'created_utc': datetime.now(timezone.utc).isoformat(),
          'self_excluded': [SELF], 'files_count': len(payload), 'files': payload, 'directories': directory_rows,
          'all_4096_permission_bits_recorded': True, 'complete_prior_actual_captures': actual_captures,
          'original_payload_body_preservation': preserved, 'v2_payload_body_preservation': preserved_v2, 'qualified_external_readback': foreign,
          'verdict': verdict['verdict'], 'preparation_manifest_sha256': verdict['preparation_manifest_sha256'],
          'actual_prior_failed_ROOT_closure_child': 84831, 'actual_prior_failed_ROOT_closure_exit': 1,
          'actual_prior_failed_V2_ROOT_closure_child': 2427, 'actual_prior_failed_V2_ROOT_closure_exit': 1,
          'dated_native_scope': 'Only the exact original QUEUE body/mode observation; its body is recovered from actual historical Git. Other2610 original inputs remain exact live body/mode bindings.',
          'production_imported_compiled_executed': False, 'fresh_native_authority': False,
          'future_acceptance_approved': False, 'outer_capture_outside_family': True,
          'outer_capture_status_at_child_closure': 'PENDING_ACTUAL_CHILD_EXIT',
          'outer_capture_rule': 'ROOT finishes the genuine external capture after actual child exit; no future completion is inserted into this payload.',
          'original_substantive_attempts': 0, 'original_source_verification_responses': 1,
          'new_substantive_attempts': 0, 'audit_turns': 0, 'native_index_remote_or_paper_DOI_tracker_mutation': False}
    with (F / SELF).open('x') as handle:
        handle.write(json.dumps(mf, indent=2) + '\n')
    (F / SELF).chmod(0o444)
    result = verify()
    result.update(actual_pid=os.getpid(), finished_utc=datetime.now(timezone.utc).isoformat())
    print(json.dumps(result, indent=2))
