"""Actual local preflight of prepared gates, while review03 remains pending."""
from pathlib import Path
import json, sys
from root_submission_gate import A, Capture, load, pin, utc

assert not (A / 'PUBLISHING_CLEARANCE.json').exists()
assert not (A / 'queue_repair_receipt.json').exists()
assert not (A / 'ACTUAL_MERGE_ATTEMPT.json').exists()
paths = ['root_submission_gate.py', 'root_refresh_claimed_queue.py',
         'root_integrate_claimed.py', 'root_verify_exact_live.py',
         'root_verify_post_merge.py', 'publication/run_zenodo_step.py',
         'publication/verify_public_record.py', 'publication/append_tracker.py']
prepared = {name: pin(A / name) for name in paths}
inputs = load(A / 'preprint/REVIEW_PACKET_MANIFEST.json')['author_inputs']
assert {name: pin(A / 'preprint' / name) for name in inputs} == inputs
capture = Capture('prepared_gates_pending_review03')
syntax = """import ast,json
from pathlib import Path
names=json.loads(__import__('sys').argv[1])
for name in names: ast.parse(Path(name).read_text())
print(json.dumps({'status':'SYNTAX_PASS','prepared_programs':len(names)}))
"""
result = capture.run('syntax', [sys.executable, '-B', '-c', syntax,
                      json.dumps([str(A / name) for name in paths])])
assert not result.stderr and json.loads(result.stdout)['prepared_programs'] == 8
blocked = """from root_submission_gate import current_clearance
try:
    current_clearance()
except FileNotFoundError as error:
    assert str(error.filename).endswith('/PUBLISHING_CLEARANCE.json')
    print('PASS: pending review has no clearance; integration/publication gate refuses it.')
else:
    raise AssertionError('Premature clearance was accepted')
"""
result = capture.run('pending_clearance', [sys.executable, '-B', '-c', blocked], cwd=A)
assert not result.stderr and result.stdout == b'PASS: pending review has no clearance; integration/publication gate refuses it.\n'
assert {name: pin(A / name) for name in paths} == prepared
assert {name: pin(A / 'preprint' / name) for name in inputs} == inputs
assert not (A / 'PUBLISHING_CLEARANCE.json').exists()
assert not (A / 'queue_repair_receipt.json').exists()
assert not (A / 'ACTUAL_MERGE_ATTEMPT.json').exists()
record = dict(utc=utc(), status='PREPARED_LOCAL_GATES_ONLY_FULL_REVIEW03_PENDING',
              prepared_programs=prepared, unchanged_author_inputs=inputs,
              actual_syntax_check=True, pending_clearance_refusal_verified=True,
              native_capture_directory=str(capture.directory),
              accepted_pr_body_is_conditional_prepared_text=True,
              no_git_branch_index_or_pr_mutation=True, no_deposit_or_tracker_write=True,
              math_percent=100, bounded_priority_percent=100, workflow_percent=60)
(A / 'PREPARATION_STATUS.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
