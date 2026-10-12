"""Independently replay the second fresh review's finalized controls before seal."""
from pathlib import Path
import json
from root_submission_gate import A, Capture, PY, sha, utc

v = A/'preprint_review_02'
capture = Capture('preprint_review02_preseal_controls')
specs = [
    ('primary', 'independent_controls.py',
     '425a2a5a8ce5192172c339d64dddd8d9486fc84e79bb463c7aa1cd68f6eb7e73',
     'private/receipts/independent_primary_controls.stdout',
     '0b0e337323aebd7ea806fcf035db1d1baf0ccb6484e1e3cbe6edef79470abdec'),
    ('transport', 'independent_transport_controls.py',
     '89ec030cdf761082fa284589ac5fc8b8658da675afc23d1684a8a7f067b8716d',
     'private/receipts/independent_transport_controls_strengthened.stdout',
     'b20859fc6b77c263b0e74b9310c38f9955270fdb47f68459c9ffcb2869a6afe4'),
]
results = []
for label, code, code_sha, expected_path, expected_sha in specs:
    b = (v/code).read_bytes()
    assert sha(b) == code_sha
    (capture.directory/(label+'_source.py')).write_bytes(b)
    expected = (v/expected_path).read_bytes()
    assert sha(expected) == expected_sha
    z = capture.run(label, [PY, '-B', v/code], cwd=capture.directory)
    assert not z.stderr and z.stdout == expected
    assert (v/code).read_bytes() == b
    results.append({'label': label, 'source_path': code, 'source_bytes': len(b), 'source_sha256': code_sha,
                    'entire_stdout_identical': True, 'stdout_bytes': len(z.stdout), 'stdout_sha256': sha(z.stdout),
                    'expected_agent_whole_stdout_path': expected_path, 'complete_stdout': json.loads(z.stdout),
                    'native': capture.entries[-1]})
receipt = {'utc': utc(), 'status': 'PASS_BOTH_SECOND_REVIEW_FINALIZED_CONTROLS_PRESEAL',
           'controls': results, 'native_capture_directory': str(capture.directory),
           'closed_namespace_claimed': False,
           'scope': 'Root read both complete final program versions and independently reproduced their complete native outputs. The active second review is not yet closed; no mathematical verdict or publication clearance is inferred from finite controls.'}
(A/'ROOT_PREPRINT_REVIEW02_PRESEAL_CONTROL_REPLAY.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt, indent=2))
