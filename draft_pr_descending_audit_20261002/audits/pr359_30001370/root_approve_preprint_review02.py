"""Record root's full draft assessment before a single local review seal."""
from pathlib import Path
import json, zipfile
from root_submission_gate import A, Capture, PY, load, sha, utc, inventory

V = A/'preprint_review_02'
assert not (V/'CLOSURE.json').exists()
assert not (A/'ROOT_PREPRINT_REVIEW02_APPROVAL.json').exists()
plan = load(V/'CLOSURE_PLAN.json')
names = plan['public_whitelist_before_generated_closure']
assert len(names) == 14 and len(set(names)) == 14
assert sha((V/'REPORT.md').read_bytes()) == '21384c5f869fc23b30c8e3018d078a0a3b49942b1a075f4982011a043e592d27'
assert sha((V/'verify_namespace.py').read_bytes()) == '893e304d96e6953839d8c13c246fa3f6631a08e540a6e8b58f1694af7ea40fe0'
assert sha((V/'seal_namespace.py').read_bytes()) == 'f116755a16e1b2f686a79c188e1b247f504f8a569f1c803b0fc9518fc24a5978'
bindings = {name: {'bytes': (V/name).stat().st_size, 'sha256': sha((V/name).read_bytes())} for name in names}
schema = load(V/'FILE_SCHEMA_INVENTORY.json')
with zipfile.ZipFile(A/'preprint/basin-boundaries-verification.zip') as z:
    members = {m.filename.removeprefix('basin-boundaries-verification/'): m for m in z.infolist()}
    assert set(members) == {e['path'] for e in schema['members']} and len(members) == 74
    for e in schema['members']:
        m = members[e['path']]
        b = z.read(m)
        assert len(b) == e['bytes'] and sha(b) == e['sha256']
        assert list(m.date_time) == e['zip_date_time'] and m.compress_type == e['zip_compression']
        b.decode('utf-8')
        assert e['regular_file'] and e['utf8_valid']
captures = Capture('preprint_review02_draft_approval')
before = inventory(V)
draft = captures.run('draft', [PY, '-B', V/'verify_namespace.py', '--draft'], cwd=captures.directory)
assert not draft.stderr
answer = json.loads(draft.stdout)
assert answer['status'] == 'PASS_DRAFT_READ_ONLY_INVENTORY' and answer['closed'] is False
assert answer['public_files'] == 14 and answer['replay_bindings_checked'] == 11
assert inventory(V) == before
all_receipts = []
for f in sorted((V/'private/receipts').glob('*.json')):
    e = load(f)
    if 'exit_code' in e:
        assert e['exit_code'] == 0, ('Hidden failed native receipt', str(f), e['exit_code'])
        all_receipts.append({'path': str(f.relative_to(V)), 'sha256': sha(f.read_bytes()), 'exit_code': 0})
for name, e in bindings.items():
    assert {'bytes': (V/name).stat().st_size, 'sha256': sha((V/name).read_bytes())} == e
replays = load(A/'ROOT_PREPRINT_PACKAGE_OUTPUT_COMPARISON.json')
assert replays['status'] == 'PASS_BOTH_REVIEWERS_CURRENT_FULL_PACKAGE_OUTPUTS'
controls = load(A/'ROOT_PREPRINT_REVIEW02_PRESEAL_CONTROL_REPLAY.json')
assert controls['status'] == 'PASS_BOTH_SECOND_REVIEW_FINALIZED_CONTROLS_PRESEAL'
assert all(e['entire_stdout_identical'] and e['native']['exit_code'] == 0 for e in controls['controls'])
message = ('Root has fully read the complete second review report, primary baseline/gate, all14 public artifacts, '
           'every74-member schema row, replay/source inventories, both final control programs, and the entire local verifier/sealer/plan. '
           'Root independently reproduced both final controls and compared both reviewers\' complete current package output streams. '
           'The read-only draft custody verifier passes. No mandatory submission repair remains. '
           'I authorize one local seal only: copy A/ROOT_PREPRINT_REVIEW02_APPROVAL.json exactly to '
           'N/private/ROOT_SEAL_AUTHORIZATION.json, then invoke seal_namespace.py once with that approval. '
           'You may record the actual native sealer argv/cwd/UTC/exit/fullstdout/fullstderr outside N in '
           'A/root_replay_private/preprint_review02_external_seal_001. '
           'After CLOSURE.json is created, perform NO namespace writes; root will capture full/public closed verification externally. '
           'This authorizes no canonical edit, publication, Git operation or outside communication. '
           'Approved public14 hashes and exact4 submission pins are bound in the root approval receipt; any difference stops final clearance.')
receipt = {'observed_utc': utc(), 'authorized_by': '/root', 'one_shot_local_seal_authorized': True,
           'root_message_exact': message, 'approved_artifact_bindings': bindings,
           'approved_submission_files': replays['submission_files'], 'mandatory_findings': 0,
           'full_draft_read': True, 'both_new_controls_independently_reproduced': True,
           'all74_schema_rows_read_and_actual_bytes_compared': True,
           'whole_native_replay_records': all_receipts, 'draft_verifier': answer,
           'native': captures.entries, 'namespace_unchanged_during_root_checks': True,
           'complete_inventory_path': str(captures.directory/'approved_namespace_inventory.json'),
           'scope': 'Local one-shot review custody closure only; actual source integration and publication remain separate.'}
(captures.directory/'approved_namespace_inventory.json').write_text(json.dumps(before, indent=2)+'\n')
(A/'ROOT_PREPRINT_REVIEW02_APPROVAL.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({'status': 'ROOT_DRAFT_READ_APPROVED_FOR_ONE_LOCAL_SEAL', 'utc': receipt['observed_utc'],
                  'approval_sha256': sha((A/'ROOT_PREPRINT_REVIEW02_APPROVAL.json').read_bytes()),
                  'public_files': len(bindings), 'draft': answer,
                  'root_message_exact': message}, indent=2))
