#!/usr/bin/env python3
"""Check this prospective plan and genuine capture, without repository mutations."""
import datetime
import hashlib
import json
import os
from pathlib import Path

OUT = Path(__file__).resolve().parent
if OUT != Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr50_10600042/native_acceptance_plan_20261004'):
    raise RuntimeError('Unexpected location')
CAP = OUT / 'actual_plan_readback'
CAP.mkdir()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
source = Path(__file__).read_bytes()
(CAP / 'PRELAUNCH_SOURCE.py').write_bytes(source)
sha = lambda data: hashlib.sha256(data).hexdigest()
(CAP / 'PRELAUNCH.json').write_text(json.dumps({'utc': started, 'actual_pid': os.getpid(),
    'script': str(Path(__file__)), 'script_sha256': sha(source),
    'source_snapshot_sha256': sha((CAP / 'PRELAUNCH_SOURCE.py').read_bytes()),
    'only_output_directory': str(OUT)}, indent=2) + '\n')
obs = json.loads((OUT / 'OBSERVATIONS.json').read_text())
plan = json.loads((OUT / 'PLAN.json').read_text())
ready = json.loads((OUT / 'READY.json').read_text())
commands = json.loads((OUT / 'actual_readonly_observation/COMPLETE_COMMANDS.json').read_text())
checks = 0
def check(condition, message):
    global checks
    if not condition:
        raise RuntimeError(message)
    checks += 1

def bound(binding):
    data = Path(binding['path']).read_bytes()
    check(len(data) == binding['bytes'], 'Byte count mismatch')
    check(sha(data) == binding['sha256'], 'SHA256 mismatch')

for output in ready['outputs']:
    bound(output)
bound(plan['observations'])
for snapshot in obs['source_snapshots']:
    bound(snapshot['snapshot'])
for command in commands:
    check(command['exit_code'] == 0, 'Failed actual command')
    check(command['child_pid'] > 0 and command['parent_pid'] == obs['actual_pid'], 'Missing actual PID')
    check(command['started_utc'] <= command['ended_utc'], 'Invalid actual timestamps')
    bound(command['stdout'])
    bound(command['stderr'])
check(len(commands) == 28, 'Unexpected capture count')
check(len(obs['original_files']) == 15, 'Unexpected original count')
check(len(obs['original_turn_ledger']) == 1 and obs['original_turn_ledger'][0]['turn'] == 1, 'Unexpected turn ledger')
check(plan['original_budget'] == '1/5', 'Wrong budget')
check(plan['actual_DOI'] is None and plan['actual_tracker_range'] is None, 'Fabricated publication')
check(plan['actual_original_integration_merge_commit'] is None and plan['actual_native_acceptance_commit'] is None, 'Fabricated merge')
check(plan['actual_native_acceptance_percent'] == 0 and not plan['new_mathematical_or_priority_approval'], 'Approval incorrectly claimed')
check(len(plan['minimal_prospective_administrative_paths']) == 5, 'Scope exceeded')
check(plan['original_scientific_files_to_preserve_exactly'] == obs['original_files'], 'Original mapping changed')
check(obs['native_selected_state'] is None and obs['native_selected_history'] == [], 'Target already imported at capture')
check(plan['no_dependency_on_excluded_PR48_or_PR49'], 'Excluded dependency')
check(plan['state_and_history_schema_recommendation']['actual_execution_delta'] ==
      {'new_target_entries': 1, 'imported_original_turns': 1, 'new_history_events': 1}, 'Wrong proposed import delta')
result = {'status': 'PASS_PROSPECTIVE_PLAN_READBACK_ONLY', 'actual_pid': os.getpid(),
    'started_utc': started, 'ended_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'checks': checks, 'command_streams_fully_rechecked': len(commands),
    'source_snapshots_rechecked': len(obs['source_snapshots']),
    'plan_sha256': sha((OUT / 'PLAN.json').read_bytes()),
    'report_sha256': sha((OUT / 'REPORT.md').read_bytes()),
    'math_or_priority_approval': False, 'publication_merge_or_native_mutations': [],
    'only_written_directory': str(OUT)}
body = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode()
(CAP / 'stdout.bin').write_bytes(body)
(CAP / 'stderr.bin').write_bytes(b'')
(OUT / 'FINAL_READBACK.json').write_bytes(body)
(CAP / 'RECEIPT.json').write_text(json.dumps({'actual_pid': os.getpid(), 'started_utc': started,
    'ended_utc': result['ended_utc'], 'source_sha256': sha(source),
    'stdout_sha256': sha(body), 'stdout_bytes': len(body),
    'stderr_sha256': sha(b''), 'stderr_bytes': 0,
    'checks': checks, 'actual_result': result['status']}, indent=2) + '\n')
print(body.decode(), end='')
