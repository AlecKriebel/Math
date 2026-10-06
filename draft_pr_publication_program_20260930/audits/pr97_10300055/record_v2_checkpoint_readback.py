"""Preserve actual checkpoint success and the earlier no-child command error."""
from pathlib import Path
import datetime, json, os

A = Path(__file__).resolve().parent
receipt = json.loads((A / 'actual_checkpoints/corrected_preparation_v2/RECEIPT.json').read_text())
execution = json.loads((A / 'actual_operations/checkpoint_v2_prepared_retry/execution.json').read_text())
failure = json.loads((A / 'actual_operations/checkpoint_v2_prepared/spawn_failure.json').read_text())
if (receipt['commit'] != 'ad789fadf6e398fe7e2c0d243db4625e78207a8e'
        or receipt['parent'] != 'bf5f7a735a853855ba4f86c58e579e4ca4a47f2a'
        or not receipt['remote_verified'] or execution['exit_code'] != 0
        or execution['child_PID'] != receipt['actual_operator_PID']
        or failure['child_PID'] is not None):
    raise RuntimeError('Actual checkpoint evidence differs')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
record = {
    'schema': 'pr97-root-v2-preparation-checkpoint-actual-readback/v1',
    'UTC': now, 'operator_PID': os.getpid(),
    'checkpoint': {key: receipt[key] for key in ['commit', 'parent', 'branch', 'remote_verified',
                                                'primary_checkout_mutated', 'primary_synchronization_pending']},
    'checkpoint_actual_child_PID': execution['child_PID'],
    'checkpoint_actual_exit_code': execution['exit_code'],
    'changed_paths': len(receipt['changed_paths']),
    'earlier_command_entry_failure': failure,
    'failure_scope': 'Nonexistent executable rejected before child creation; no Git action was started.',
    'frozen_v2_package_changed': False,
    'whole_package_round2_status': 'running',
    'priority_clearance': False, 'publication_authorized': False,
    'new_central_proof_search_turns': 0,
    'workflow_estimate_percent': 45, 'program_completion_percent': 13/99*100,
    'this_readback_future_metadata_checkpoint_pending': True,
}
with (A / 'ROOT_V2_PREPARATION_CHECKPOINT_ACTUAL_READBACK_20261006.json').open('x') as stream:
    stream.write(json.dumps(record, indent=2) + '\n')
with (A / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n### ' + now + ' — corrected preparation checkpoint released\n'
                 'Actual child43085 exited0 and pushed/remote-verified main ad789fadf6e398fe7e2c0d243db4625e78207a8e, a strict descendant of bf5f7a735a853855ba4f86c58e579e4ca4a47f2a, for the200 selected regular corrected-package/ROOT metadata bodies. Primary checkout/index were untouched; active roundtwo and private controlled/duplicate fixtures were excluded. An earlier ROOT command-entry mistake attempted a nonexistent executable; actual recorder42685 saved a no-child spawn failure at2026-10-06T01:44:00.598614UTC, before any Git action. Its evidence is preserved, not represented as an executed checkpoint. This late actual readback and compact operation receipts join the next metadata checkpoint; no recursive-self-commit claim. Fresh roundtwo is running. Mathematical scope/strict-priority hold remain unchanged, publication/native acceptance false. Original2/5, extra proof-search0; PR97workflow45%, program13/99=13.13%.\n')
print(json.dumps(record))
