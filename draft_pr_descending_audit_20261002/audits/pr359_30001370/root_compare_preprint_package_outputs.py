"""Bind both fresh reviewers' entire actual current package output streams.

This comparison is independent of final closure and does not grant acceptance.
"""
from pathlib import Path
import json
from root_submission_gate import A, load, sha, utc

repair = load(A/'METADATA_REPAIR_RECEIPT.json')
files = repair['submission_files']
for e in files:
    b = (A/'preprint'/e['path']).read_bytes()
    assert len(b) == e['bytes'] and sha(b) == e['sha256']
assert load(A/'ROOT_PREPRINT_REVIEW01_VERIFICATION.json')['sealed_submission_files'] == files
v = A/'preprint_review_02'
second = load(v/'REPLAY_BINDINGS.json')
assert second['full_package_outputs_compared_to_current_expected']
assert {e['path']: {'bytes': e['bytes'], 'sha256': e['sha256']} for e in files} == {
    k: {'bytes': e['bytes'], 'sha256': e['sha256']} for k, e in load(v/'CURRENT_BINDINGS.json')['canonical_four'].items()}
labels = [('default', 'current_supplement_default', 'supplement_default'),
          ('full', 'current_supplement_full', 'supplement_full'),
          ('public_priority', 'current_priority_public', 'priority_public')]
reviews = [{'review': 1, 'replays': {}}, {'review': 2, 'replays': {}}]
for label, first_label, second_label in labels:
    expected = (A/'preprint/private/metadata_repair_001'/(label+'.stdout')).read_bytes()
    old = next(e for e in repair['complete_runs'] if e['label'] == label)['native']
    assert len(expected) == old['stdout_bytes'] and sha(expected) == old['stdout_sha256']
    first_dir = A/'preprint_review_01/native_runs'/first_label
    one = load(first_dir/'record.json')
    assert one['exit_code'] == 0
    for name in ('stdout', 'stderr'):
        b = (first_dir/(name+'.bin')).read_bytes()
        assert {'bytes': len(b), 'sha256': sha(b)} == one[name]
    assert (first_dir/'stdout.bin').read_bytes() == expected
    assert (first_dir/'stderr.bin').read_bytes() == b''
    reviews[0]['replays'][label] = {'exit_code': 0, 'stdout_path': str(first_dir/'stdout.bin'),
                                   'stderr_path': str(first_dir/'stderr.bin'),
                                   'stdout_bytes': len(expected), 'stdout_sha256': sha(expected)}
    two = second['runs'][second_label]
    native_pin = two['native_receipt']
    raw = Path(native_pin['path']).read_bytes()
    assert len(raw) == native_pin['bytes'] and sha(raw) == native_pin['sha256']
    native = json.loads(raw)
    assert native['argv'] == two['argv'] and native['exit_code'] == two['exit_code'] == 0
    assert native['started_utc'] == two['started_utc'] and native['finished_utc'] == two['finished_utc']
    for name in ('stdout', 'stderr'):
        e = two[name]
        b = Path(e['path']).read_bytes()
        assert len(b) == e['bytes'] and sha(b) == e['sha256'] == native[name+'_sha256']
    assert Path(two['stdout']['path']).read_bytes() == expected
    assert Path(two['stderr']['path']).read_bytes() == b''
    reviews[1]['replays'][label] = {'exit_code': 0, 'stdout_path': two['stdout']['path'],
                                   'stderr_path': two['stderr']['path'],
                                   'stdout_bytes': len(expected), 'stdout_sha256': sha(expected)}
result = {'utc': utc(), 'status': 'PASS_BOTH_REVIEWERS_CURRENT_FULL_PACKAGE_OUTPUTS',
          'submission_files': files, 'reviews': reviews,
          'first_review_closed': True, 'second_review_closure_claimed': False,
          'scope': 'Every default/full/public-priority stdout byte and every stderr byte matches the current expected output and native records. Second final closure and complete review verdict remain separate; this comparison grants no clearance.'}
(A/'ROOT_PREPRINT_PACKAGE_OUTPUT_COMPARISON.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k != 'reviews'}, indent=2))
