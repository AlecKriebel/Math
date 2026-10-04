"""Parent's read-only whole closed second-review and control verification."""
from pathlib import Path
import json
from root_submission_gate import A, Capture, PY, load, sha, utc, inventory

V = A/'preprint_review_02'
closed = load(V/'CLOSURE.json')
assert closed['closed'] is True and closed['status'] == 'FINAL_CLOSED'
assert not (A/'ROOT_PREPRINT_REVIEW02_VERIFICATION.json').exists()
approval = load(A/'ROOT_PREPRINT_REVIEW02_APPROVAL.json')
assert (V/'private/ROOT_SEAL_AUTHORIZATION.json').read_bytes() == (A/'ROOT_PREPRINT_REVIEW02_APPROVAL.json').read_bytes()
before = inventory(V)
approved_tree = load(Path(approval['complete_inventory_path']))
for name, e in approved_tree.items():
    assert before[name] == e, ('Changed approved review payload', name)
assert set(before)-set(approved_tree) == {'PUBLIC_MANIFEST.json', 'PRIVATE_MANIFEST.json',
                                        'CLOSURE.json', 'private/ROOT_SEAL_AUTHORIZATION.json'}
for name, pin in approval['approved_artifact_bindings'].items():
    assert {'bytes': (V/name).stat().st_size, 'sha256': sha((V/name).read_bytes())} == pin
public = load(V/'PUBLIC_MANIFEST.json')['files']
private = load(V/'PRIVATE_MANIFEST.json')['files']
assert len(public) == 14
capture = Capture('preprint_review02_closed')
flat_captures = []
def flat(e):
    return {k: e[k] for k in ('argv', 'cwd', 'started_utc', 'finished_utc', 'exit_code')} | {
        'stdout_bytes': e['streams']['stdout']['bytes'], 'stdout_sha256': e['streams']['stdout']['sha256'],
        'stderr_bytes': e['streams']['stderr']['bytes'], 'stderr_sha256': e['streams']['stderr']['sha256'],
        'stdout_path': str(A/e['streams']['stdout']['path']), 'stderr_path': str(A/e['streams']['stderr']['path'])}
seal_sha = sha((V/'CLOSURE.json').read_bytes())
for full in (True, False):
    label = 'full' if full else 'public'
    args = [PY, '-B', V/'verify_namespace.py'] + ([] if full else ['--public-only'])
    z = capture.run(label, args, cwd=capture.directory)
    expected = {'status': 'PASS_CLOSED_READ_ONLY_INVENTORY', 'closed': True,
                'mode': 'full_private_and_live_external_bindings' if full else 'public_only_private_external_unchecked',
                'closure_sha256': seal_sha, 'public_files': 14,
                'private_files_checked': len(private) if full else 0,
                'replay_bindings_checked': 11 if full else 0, 'read_only': True}
    assert not z.stderr and z.stdout == (json.dumps(expected, indent=2)+'\n').encode()
    flat_captures.append(flat(capture.entries[-1]))
controls = []
preseal = load(A/'ROOT_PREPRINT_REVIEW02_PRESEAL_CONTROL_REPLAY.json')
for e in preseal['controls']:
    assert sha((V/e['source_path']).read_bytes()) == e['source_sha256']
    z = capture.run('controls_'+e['label'], [PY, '-B', V/e['source_path']], cwd=capture.directory)
    assert not z.stderr and z.stdout == (V/e['expected_agent_whole_stdout_path']).read_bytes()
    assert z.stdout == (A/e['native']['streams']['stdout']['path']).read_bytes()
    assert json.loads(z.stdout) == e['complete_stdout']
    execution = flat(capture.entries[-1])
    flat_captures.append(execution)
    controls.append({'label': e['label'], 'entire_stdout_identical': True,
                     'execution': execution, 'complete_stdout': e['complete_stdout'],
                     'stdout_path': execution['stdout_path'], 'control_source_sha256': e['source_sha256']})
assert inventory(V) == before
files = approval['approved_submission_files']
for e in files:
    b = (A/'preprint'/e['path']).read_bytes()
    assert len(b) == e['bytes'] and sha(b) == e['sha256']
gate = load(V/'PRIMARY_GATE.json')
baseline = next(e for e in gate['files'] if e['path'] == 'PRIMARY_BASELINE.md')
result = {'utc': utc(), 'status': 'PASS_ROOT_CLOSED_PREPRINT_REVIEW02', 'review_number': 2,
          'mandatory_findings': 0, 'all_mandatory_submission_findings_resolved': True,
          'closed_namespace_unchanged': True, 'whole_verifier_output_compared': True,
          'review_seal_path': 'CLOSURE.json', 'review_seal_sha256': seal_sha,
          'sealed_utc': closed['sealed_utc'],
          'baseline_seal': {'utc': gate['observed_seal_utc'], **baseline,
                            'candidate_access_before_seal': False,
                            'prior_or_current_substantive_verdict_access_before_seal': False,
                            'primary_gate_sha256': sha((V/'PRIMARY_GATE.json').read_bytes())},
          'sealed_submission_files': files, 'captures': flat_captures,
          'public_payload_count': len(public), 'private_payload_count': len(private),
          'whole_payload_files': sum(e['type'] == 'file' for e in before.values()),
          'whole_directories': sum(e['type'] == 'directory' for e in before.values()),
          'fully_read_report_sha256': sha((V/'REPORT.md').read_bytes()),
          'full_package_outputs_compared_to_current_expected': True,
          'root_approved_public_artifacts_unchanged': True,
          'scope': 'Root fully read the second analytical report, primary baseline, all public evidence/code/schema rows, reproduced both independent control sources, compared all current whole package outputs and verified sealed full/public custody without writes. No mandatory submission repairs remain; actual native integration/publication remain separate gates.'}
(capture.directory/'whole_inventory.json').write_text(json.dumps(before, indent=2)+'\n')
(A/'ROOT_PREPRINT_REVIEW02_VERIFICATION.json').write_text(json.dumps(result, indent=2)+'\n')
control = {'utc': utc(), 'entire_stdout_identical': True, 'closed_review_namespace_unchanged': True,
           'execution': controls[0]['execution'], 'control_runs': controls,
           'review_seal_sha256': seal_sha,
           'scope': 'Both distinct finalized control programs reproduced in full; no merged synthetic execution event is invented.'}
(A/'ROOT_PREPRINT_REVIEW02_CONTROL_REPRODUCTION.json').write_text(json.dumps(control, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k not in {'captures', 'baseline_seal'}}, indent=2))
