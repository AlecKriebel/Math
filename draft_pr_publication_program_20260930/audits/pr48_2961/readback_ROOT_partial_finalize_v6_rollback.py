"""Separate ROOT readback of actual rollback; no production or Git mutation."""
from pathlib import Path
import base64, datetime, hashlib, json, os, stat, sys
A = Path(__file__).resolve().parent
R = A.parents[2]
K = R / 'unsolved_math_prioritization/attempts/2961'
def need(value, message):
    if not value:
        raise ValueError(message)
def sha(body):
    return hashlib.sha256(body).hexdigest()
def ref(path):
    need(path.is_file() and not path.is_symlink(), 'Regular evidence')
    body = path.read_bytes()
    return {'path': path.relative_to(R).as_posix(), 'bytes': len(body), 'sha256': sha(body),
            'full_mode': stat.S_IMODE(path.stat().st_mode)}
def checked(row):
    need(ref(R / row['path']) == row, 'Exact complete body/mode: ' + row['path'])
    return (R / row['path']).read_bytes()
need(sys.argv[1:] == ['--source-receipt-sha256', 'e86885a769f4d0a5b9730340bae90d6c85d8d757cc51b2e9bc836db196f43453'] and __debug__, 'Exact ROOT receipt pin')
receipt = A / 'ROOT_PARTIAL_FINALIZE_V6_ROLLBACK_RECEIPT.json'
need(sha(receipt.read_bytes()) == sys.argv[2], 'Actual receipt unchanged')
obj = json.loads(receipt.read_bytes())
need(obj['status'] == 'PASS_EXACT_SELECTED_ROLLBACK_ONLY' and obj['actual_pid'] == 40863
     and obj['overall_rollback_success_claimed'] is True and obj['V7_execution_or_acceptance_approved'] is False, 'Actual success boundary')
plan = json.loads(checked(obj['plan']))
for key in ['source', 'source_prelaunch', 'lock_ownership', 'lock_release', 'runtime_outside_baseline', 'quarantine_receipt', 'native_critical_result', 'readonly_commands']:
    checked(obj[key])
release = json.loads(checked(obj['lock_release']))
need(release['released'] is True and release['complete_body_written'] is True, 'Exact owned lock released')
need(not (R / '.git/index.lock').exists(), 'No coordination lock remains at readback')
critical = json.loads(checked(obj['native_critical_result']))
need(critical['status'] == 'PASS_NATIVE_CRITICAL_CHECKS_PENDING_LOCK_RELEASE'
     and critical['overall_rollback_success_claimed'] is False, 'Pending result is not prematurely promoted')
quarantine = json.loads(checked(obj['quarantine_receipt']))
need(quarantine['actual_mutation_started'] is False and quarantine['retained_count'] == 11, 'Pre-mutation quarantine')
need([r['original'] for r in quarantine['retained']] == plan['partial11'], 'Exact all eleven preimages retained')
for row in quarantine['retained']:
    checked(row['retained'])
    need(all(row['original'][key] == row['retained'][key] for key in ['bytes', 'sha256', 'full_mode']), 'Quarantine retains full body/mode')
overlay = json.loads(checked(plan['original_overlay']))['canonical_overlay_files']
names = {row['path'] for row in overlay}
need(len(names) == len(overlay) == 1955, 'Original complete domain')
actual = {p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file()}
need(actual == names, 'Canonical original1955 restored')
admin = {'status.json', 'readiness.json', 'review/review_summary.json', 'review/verdict.json'}
for row in overlay:
    p = K / row['path']
    descriptor = ref(p)
    need(descriptor['bytes'] == row['bytes'] and descriptor['sha256'] == row['sha256'], 'Every canonical body original-exact')
    need(descriptor['full_mode'] == (0o644 if row['path'] in admin else 0o444), 'Explicit four ADMIN /1951 science modes')
for p in [K] + list(K.rglob('*')):
    need(not p.is_symlink(), 'No canonical symlink')
    if p.is_dir():
        need(stat.S_IMODE(p.stat().st_mode) == 0o755, 'Directory full mode')
checked(plan['inventory_original'])
need((R / 'draft_pr_publication_program_20260930/inventory.json').read_bytes() == checked(plan['inventory_original']), 'Program inventory restored')
for operation in obj['complete_operations']:
    if 'after' in operation:
        checked(operation['after'])
    else:
        need(not (R / operation['path']).exists(), 'Only quarantined receipt removed')
need(len(obj['complete_operations']) == 11, 'Exact eleven operations')
for row in plan['fixed_failed_evidence'] + obj['unrelated_native12'] + obj['owned_logs']:
    checked(row)
outside = []
for row in obj['complete_current_outside_rows']:
    current = ref(R / row['path'])
    outside.append({'recorded': row, 'current': current, 'unchanged_at_later_readback': current == row})
ledger = json.loads(checked(obj['readonly_commands']))
commands = ledger['complete_commands']
for command in commands:
    need(command['actual_execution'] is True and command['completed'] is True and command['exit_code'] == 0 and type(command['pid']) is int, 'Genuine completed read-only child')
    for name in ['stdout', 'stderr']:
        raw = base64.b64decode(command[name + '_base64'], validate=True)
        need(len(raw) == command[name + '_bytes'] and sha(raw) == command[name + '_sha256'], 'Complete raw stream authentication')
failed = json.loads((A / 'root_finalize_actual_capture/CAPTURE.json').read_bytes())
need(failed['status'] == 'FAIL' and failed['exit_code'] == 1 and failed['pid'] == 80480, 'Original failure remains genuine failure')
result = {'schema': 'pr48-ROOT-separate-actual-rollback-readback/v1', 'actual_pid': os.getpid(),
          'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'argv': sys.argv,
          'status': 'PASS_EXACT_SELECTED_NATIVE_RESTORATION_AND_EVIDENCE_READBACK', 'actual_receipt': ref(receipt),
          'canonical_original_bodies': 1955, 'science_full0444': 1951, 'ADMIN_full0644': 4,
          'quarantine_preimages_verified': 11, 'readonly_children_complete_streams_authenticated': len(commands),
          'outside_dated_readback': outside, 'original_failure_rewritten': False,
          'index_identity_claim': 'Original receipt certifies owned-lock interval only; no new HEAD/index invariance interval asserted here.',
          'native_or_Git_mutation_by_readback': False, 'acceptance_completed': False, 'V7_approved': False}
body = (json.dumps(result, sort_keys=True, indent=2) + '\n').encode()
output = A / 'ROOT_PARTIAL_FINALIZE_V6_ROLLBACK_READBACK_20261003.json'
with output.open('xb') as stream:
    stream.write(body); os.fchmod(stream.fileno(), 0o444); stream.flush(); os.fsync(stream.fileno())
print(json.dumps({'status': result['status'], 'receipt': ref(output), 'readonly_children': len(commands),
                  'all_outside_rows_still_unchanged': all(r['unchanged_at_later_readback'] for r in outside)}))
