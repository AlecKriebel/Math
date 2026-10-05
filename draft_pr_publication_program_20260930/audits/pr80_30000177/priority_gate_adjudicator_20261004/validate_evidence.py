#!/usr/bin/env python3
"""Validate completed custody records without substituting launcher status."""
import datetime
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent
evidence = root / 'process_evidence'
issues = []
current_capture_label = sys.argv[1] if len(sys.argv)>1 else 'validate_evidence'
preserved = root / 'initial_adjudication_preserved_20261004'

def actual(path):
    path = pathlib.Path(path)
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()

def agrees(pin, alternate=None):
    candidates = [pathlib.Path(pin['path'])]
    if alternate:
        candidates += list(alternate)
    for candidate in candidates:
        if candidate.exists() and actual(candidate) == (pin['bytes'], pin['sha256']):
            return True
    return False

manifest = json.loads((root / 'EVIDENCE_MANIFEST.json').read_text())
for source in manifest['source_inputs']:
    if not agrees(source):
        issues.append('source mismatch: ' + source['label'])

completed = []
child_failures = []
launcher_failures = []
for folder in sorted(evidence.iterdir()):
    if folder.name == current_capture_label:
        continue  # This child has no completion record until it returns.
    request_path = folder / 'request.json'
    if not request_path.exists():
        continue
    request = json.loads(request_path.read_text())
    for pin in request['prelaunch_pins']:
        # A revised launcher can be authenticated by its prelaunch source copy.
        alternatives = list(folder.glob('*_' + pathlib.Path(pin['path']).name))
        alternatives += [preserved / pathlib.Path(pin['path']).name]
        if request['argv'][0] == 'cat' and pin['path'] in request['argv'][1:]:
            alternatives += [folder / 'stdout.bin']
        if not agrees(pin, alternatives):
            issues.append('prelaunch pin mismatch: ' + folder.name + ': ' + pin['path'])
    result_path = folder / 'result.json'
    if not result_path.exists():
        if (folder.name.startswith('extract_')
                and not folder.name.endswith('_retry')
                and request['argv'][0] == '--pin'
                and not (folder / 'child_launch.json').exists()):
            launcher_failures.append(folder.name)
            continue
        issues.append('unexplained missing result: ' + folder.name)
        continue
    result = json.loads(result_path.read_text())
    launch = json.loads((folder / 'child_launch.json').read_text())
    if result['child_pid'] != launch['child_pid']:
        issues.append('PID mismatch: ' + folder.name)
    if not isinstance(result['child_exit_code'], int):
        issues.append('invalid actual child status: ' + folder.name)
    for stream in ['stdout', 'stderr']:
        if not agrees(result[stream]):
            issues.append('stream mismatch: ' + folder.name + ': ' + stream)
    if not (request['utc_before_launch'] <= launch['utc_launched'] <= result['utc_completed']):
        issues.append('capture chronology mismatch: ' + folder.name)
    completed.append(folder.name)
    if result['child_exit_code'] != 0:
        child_failures.append({'label': folder.name, 'actual_child_exit_code': result['child_exit_code']})

for file_pin in manifest['files_snapshot']:
    path = pathlib.Path(file_pin['path'])
    # The manifest child stdout/result are written after its in-child snapshot.
    if path.parent.name.startswith('finalize_evidence') and path.name in {'stdout.bin', 'stderr.bin', 'result.json'}:
        continue
    if not agrees(file_pin, [preserved / path.name]):
        issues.append('manifest snapshot mismatch: ' + str(path))

def request(label):
    return json.loads((evidence / label / 'request.json').read_text())

def result(label):
    return json.loads((evidence / label / 'result.json').read_text())

freeze_completed = result('freeze_receipt')['utc_completed']
candidate_started = request('read_candidate')['utc_before_launch']
candidate_completed = result('read_candidate')['utc_completed']
if not freeze_completed < candidate_started:
    issues.append('source-first freeze did not precede candidate read')
for family in ['read_target_priority_family_20261004', 'read_mechanism_priority_family_20261004']:
    if not candidate_completed < request(family)['utc_before_launch']:
        issues.append('family read did not follow candidate read: ' + family)
candidate_pin = result('read_candidate')['stdout']
expected_sha = 'fb8646bbe3cd8512ec7736fc180fa08a76740ac8b0dbb60b539a0320328c6404'
if candidate_pin['bytes'] != 11679 or candidate_pin['sha256'] != expected_sha:
    issues.append('candidate identity mismatch')
verdict = json.loads((root / 'VERDICT.json').read_text())
if verdict['candidate_sha256'] != expected_sha:
    issues.append('verdict candidate identity mismatch')
if len(launcher_failures) != 8:
    issues.append('unexpected launcher-failure accounting')
if not result('correction_source_freeze_receipt')['utc_completed'] < request('read_root_after_first_bound_comparison')['utc_before_launch']:
    issues.append('independent correction freeze did not precede ROOT comparison read')
for pin in request('preserve_initial_adjudication')['prelaunch_pins']:
    if pathlib.Path(pin['path']).name in {'REPORT.md','VERDICT.json','SOURCE_READ_SCOPE_LEDGER.md','EVIDENCE_MANIFEST.json','EVIDENCE_VALIDATION.json'}:
        if not agrees(pin, [preserved / pathlib.Path(pin['path']).name]):
            issues.append('initial adjudication preservation mismatch: ' + pin['path'])

output = {
    'validated_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_count': len(manifest['source_inputs']),
    'completed_child_records_checked': len(completed),
    'retained_nonzero_child_statuses': child_failures,
    'retained_launcher_failures_without_child': launcher_failures,
    'source_first_freeze_completed_utc': freeze_completed,
    'candidate_read_started_utc': candidate_started,
    'candidate_bytes': candidate_pin['bytes'],
    'candidate_sha256': candidate_pin['sha256'],
    'correction_source_freeze_completed_utc': result('correction_source_freeze_receipt')['utc_completed'],
    'root_comparison_read_started_utc': request('read_root_after_first_bound_comparison')['utc_before_launch'],
    'validation_issues': issues,
    'current_child_note': 'Actual validation PID/status/streams are captured by the parent launcher after this child returns.'
}
(root / 'EVIDENCE_VALIDATION.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps(output, indent=2))
if issues:
    raise SystemExit(1)
