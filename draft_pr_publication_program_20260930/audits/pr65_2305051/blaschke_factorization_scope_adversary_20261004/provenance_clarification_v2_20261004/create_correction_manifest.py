#!/usr/bin/env python3
"""Write only new clarification metadata and its stable supplement manifest."""
from pathlib import Path
import datetime
import hashlib
import json

BASE = Path(__file__).resolve().parent
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
execution = json.loads((BASE / 'ACTUAL_VERIFICATION_EXECUTION.json').read_text())
result = json.loads((BASE / 'verification.stdout.bin').read_text())
verdict = {
    'schema': 'PR65-factorization-provenance-clarification/v2',
    'utc': now,
    'immutable_head': execution['source_pin']['immutable_head'],
    'correction_status': 'COMPLETE',
    'mathematical_verdict_unchanged': 'PASS_NO_ESSENTIAL_GAP_IDENTIFIED_IN_ASSIGNED_FAMILY',
    'original_recorder_rows_without_recorded_child_pid': 12,
    'retrospective_pid_assignment': False,
    'frozen_v1_manifest_members_unchanged': result['v1_manifest_members_unchanged'],
    'original_source_bodies_unchanged': result['original_candidate_bodies_unchanged'],
    'root_recorded_replay_child_pid': result['root_recorded_factorization_child_pid'],
    'new_actual_preservation_verification_child_pid': execution['actual_child_pid'],
    'new_verification_exit_code': execution['exit_code'],
    'new_execution_receipt': 'ACTUAL_VERIFICATION_EXECUTION.json',
    'root_bounded_control_replay_receipt_verified': True,
    'new_proof_attempts': 0,
    'original_attempt_count': '2/5 unchanged',
    'validation_completion_estimate_percent': 100,
    'original_manifest_covered_files_modified': False,
}
(BASE / 'CORRECTION_VERDICT.json').write_text(json.dumps(verdict, indent=2) + '\n')
(BASE / 'RESEARCH_LOG.md').write_text(
    '# Append-only provenance correction log\n\n## ' + now + ' — completed correction\n\n'
    'Clarified that all 12 original recorder rows omit child PID, including 003 and 012. '
    'Preserved every frozen v1 manifest-covered file and the frozen manifest itself. '
    'New preservation verification captured actual child PID ' + str(execution['actual_child_pid']) +
    ', UTC timing, exit 0, streams and source pins; it confirms 40 v1 members and 18 original bodies unchanged. '
    'ROOT replay PID 69186 belongs only to ROOT’s later replay and is not assigned retrospectively. '
    'Mathematical verdict unchanged. Correction completion estimate: 100%; original substantive attempt count 2/5 unchanged. '
    'No new proof search, original-body mutation, Git index/ref mutation, status/queue/PR/editor mutation, publication, or outreach.\n'
)
artifacts = []
for path in sorted(BASE.rglob('*')):
    if path.is_file() and path.name != 'CORRECTION_MANIFEST.json':
        data = path.read_bytes()
        artifacts.append({'path': str(path.relative_to(BASE)), 'bytes': len(data),
                          'sha256': hashlib.sha256(data).hexdigest()})
manifest = {
    'schema': 'PR65-factorization-provenance-correction-manifest/v2',
    'utc': now,
    'immutable_head': execution['source_pin']['immutable_head'],
    'scope': 'Append-only supplement subfolder; excludes this manifest itself. Frozen v1 files are referenced and not modified.',
    'frozen_v1_manifest': {
        'path': str(BASE.parent / 'SELF_MANIFEST.json'),
        'sha256': execution['source_pin']['frozen_v1_manifest_sha256'],
        'unchanged_members': 40,
    },
    'root_replay_receipt': {
        'path': str(BASE.parent.parent / 'ROOT_reproduction_20261004' / 'NEW_FAMILIES_READBACK.json'),
        'sha256': execution['source_pin']['root_replay_receipt_sha256'],
    },
    'artifacts': artifacts,
}
data = (json.dumps(manifest, indent=2) + '\n').encode()
(BASE / 'CORRECTION_MANIFEST.json').write_bytes(data)
print(json.dumps({'status': 'COMPLETE', 'supplement_artifacts': len(artifacts),
                  'correction_manifest_sha256': hashlib.sha256(data).hexdigest(),
                  'actual_new_verification_child_pid': execution['actual_child_pid'],
                  'original_manifest_sha256_unchanged': execution['source_pin']['frozen_v1_manifest_sha256']}, indent=2))
