"""Prepared read-only PR344 gates. No clearance is created by this module.

Historical reviews 01 and 02 remain adverse. A separately closed clean NEW
review of the repaired eight-input v04 packet is required before these gates
can authorize any integration or production-publication step.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess, zipfile

A = Path(__file__).resolve().parent
P = A.parents[1]
R = P.parent
Q = 'unsolved_math_prioritization/QUEUE.md'
TARGET = 'problems/30005649_qss_self_duality'
ORIGINAL_HEAD = '86a758b1cc9c94322ce6afc3d17150fa2c90327a'
BRANCH = 'math/30005649-qss-self-duality-wip'
SUBMISSION_NAMES = ('qss-self-duality-note.tex', 'qss-self-duality-note.pdf',
                    'qss-self-duality-verification.zip', 'zenodo-deposit.json')
AUTHOR_NAMES = SUBMISSION_NAMES + ('build_supplement.py', 'verify_supplement.py',
                                 'intrinsic_formula_regressions.txt',
                                 'CONTROL_FORMULA_CORRECTION.md')
CLEAR_STATUS = 'READY_AFTER_REPAIR_AND_NEW_THIRD_FULL_PREPRINT_REVIEW'

def utc():
    return datetime.now(timezone.utc).isoformat()

def sha(body):
    return hashlib.sha256(body).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

def pin(path):
    assert path.is_file() and not path.is_symlink(), str(path)
    body = path.read_bytes()
    return dict(bytes=len(body), sha256=sha(body), mode=stat.S_IMODE(path.stat().st_mode))

def inventory(root):
    assert root.is_dir() and not root.is_symlink()
    files, directories = {}, {'.': stat.S_IMODE(root.stat().st_mode)}
    for path in sorted(root.rglob('*')):
        assert not path.is_symlink(), str(path)
        if path.is_file():
            files[path.relative_to(root).as_posix()] = pin(path)
        else:
            assert path.is_dir(), str(path)
            directories[path.relative_to(root).as_posix()] = stat.S_IMODE(path.stat().st_mode)
    return dict(files=files, directories=directories)

def window():
    assert not load(P / 'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']

class Capture:
    def __init__(self, purpose):
        self.directory = A / 'root_integration_private' / (
            purpose + '_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
        self.directory.mkdir(parents=True, exist_ok=False)
        self.entries = []

    def run(self, label, args, cwd=R, ok=(0,), input=None):
        args = [str(value) for value in args]
        assert not (self.directory / (label + '.json')).exists()
        prep = dict(utc=utc(), argv=args, cwd=str(cwd),
                    program_pins={arg: pin(Path(arg)) for arg in args
                                  if arg.endswith('.py') and Path(arg).is_file()})
        (self.directory / (label + '.preexecution.json')).write_text(json.dumps(prep, indent=2) + '\n')
        result = subprocess.run(args, cwd=cwd, input=input, capture_output=True,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1',
                                         PYTHONHASHSEED='0', GIT_OPTIONAL_LOCKS='0',
                                         GIT_NO_LAZY_FETCH='1'))
        streams = {}
        for kind, body in [('stdout', result.stdout), ('stderr', result.stderr)]:
            path = self.directory / (label + '.' + kind)
            path.write_bytes(body)
            streams[kind] = dict(path=str(path), **pin(path))
        entry = dict(**prep, completed_utc=utc(), exit_code=result.returncode, streams=streams)
        self.entries.append(entry)
        (self.directory / (label + '.json')).write_text(json.dumps(entry, indent=2) + '\n')
        assert result.returncode in ok, (label, result.returncode, result.stderr.decode(errors='replace'))
        return result

    def git(self, *args, input=None, ok=(0,)):
        return self.run('git_' + str(len(self.entries)), ['git', *args], input=input, ok=ok).stdout

def current_clearance():
    # These documents must be created by a later, separately recorded root
    # closure. A pending-review status or a successful mechanical verifier
    # cannot substitute for the scientific clean-review decision.
    clear = load(A / 'PUBLISHING_CLEARANCE.json')
    assert clear['status'] == CLEAR_STATUS and clear['final_clean_review'] == 3
    assert clear['unresolved_mandatory_findings'] == 0
    assert clear['historical_adverse_reviews_retained'] is True
    assert clear['historical_findings_repaired'] == ['B1', 'F01/root B2']
    assert clear['original_head'] == ORIGINAL_HEAD and clear['original_status'] == 'claimed_solved'
    assert clear['first_priority_certified'] is False
    assert clear['first_application_certified'] is False
    author = clear['sealed_author_inputs']
    assert set(author) == set(AUTHOR_NAMES) and len(author) == 8
    assert {name: pin(A / 'preprint' / name) for name in AUTHOR_NAMES} == author
    assert load(A / 'preprint/REVIEW_PACKET_MANIFEST.json')['author_inputs'] == author
    formal = clear['sealed_submission_files']
    assert {entry['path']: {key: entry[key] for key in ('bytes', 'sha256', 'mode')}
            for entry in formal} == {name: author[name] for name in SUBMISSION_NAMES}
    required_artifacts = {
        'ROOT_MATHEMATICAL_ACCEPTANCE.json', 'ROOT_MATHEMATICAL_ACCEPTANCE_QUALIFICATION.json',
        'ROOT_PRIORITY_ACCEPTANCE.json', 'ROOT_PUBLIC_FORMULA_REPAIR.json',
        'ROOT_PREPRINT_REVIEW01_SEAL.json', 'ROOT_PREPRINT_REVIEW02_SEAL.json',
        'ROOT_PREPRINT_REVIEW03_SEAL.json', 'ROOT_PREPRINT_REVIEW03_VERIFICATION.json',
        'ROOT_PREPRINT03_SOURCE_GATE.json', 'ROOT_PREPRINT03_FIRST_ASSESSMENT_GATE.json',
        'ROOT_FINAL_CLOSED_EVIDENCE.json'}
    assert required_artifacts <= set(clear['immutable_root_artifact_pins'])
    for name, expected in clear['immutable_root_artifact_pins'].items():
        assert pin(A / name) == expected, name
    first = load(A / 'ROOT_PREPRINT_REVIEW01_VERIFICATION.json')
    second = load(A / 'ROOT_PREPRINT_REVIEW02_VERIFICATION.json')
    assert first['mandatory_findings'] == 1
    assert second['status'] == 'REVIEW_COMPLETE_SUBSTANTIVE_HELPER_BLOCKER_RETAINED'
    assert second['generic_helper_valid'] is False and second['main_theorem_valid'] is True
    final = load(A / 'ROOT_PREPRINT_REVIEW03_VERIFICATION.json')
    assert final['status'] == 'REVIEW_COMPLETE_NO_UNRESOLVED_MANDATORY_FINDINGS'
    assert final['mandatory_findings'] == 0 and final['closed_namespace_unchanged']
    assert final['whole_verifier_output_compared'] and final['source_first_and_premath_gates_preserved']
    assert final['sealed_author_inputs'] == author
    evidence = load(A / 'ROOT_FINAL_CLOSED_EVIDENCE.json')
    assert evidence['status'] == 'ALL_EIGHT_CLOSED_NAMESPACES_PINNED_AFTER_CLEAN_REVIEW03'
    assert set(evidence['namespaces']) == {
        'honda_lifting', 'intrinsic_invariants', 'semilinear_modules',
        'priority_supersingular_mechanism', 'priority_audit',
        'preprint_review_01', 'preprint_review_02', 'preprint_review_03'}
    for name, expected in evidence['namespaces'].items():
        assert inventory(A / name) == expected, name
    return clear

def queue_binding(capture, base, target):
    old = capture.git('show', f'{base}:{Q}').splitlines(keepends=True)
    new = capture.git('show', f'{target}:{Q}').splitlines(keepends=True)
    assert len(old) == len(new)
    changed = [i for i, (left, right) in enumerate(zip(old, new)) if left != right]
    assert len(changed) == 1, changed
    i = changed[0]
    before, after = old[i].split(b'|'), new[i].split(b'|')
    assert len(before) == len(after)
    assert before[2].strip().split(b' / ')[0] == b'30005649'
    assert [before[j].strip() for j in (8, 9)] == [b'queued', b'0/5']
    assert [after[j].strip() for j in (8, 9)] == [b'claimed_solved', b'1/5']
    assert [j for j, (left, right) in enumerate(zip(before, after)) if left != right] == [8, 9, 11]
    receipt = load(A / 'queue_repair_receipt.json')
    assert old[i].decode() == receipt['old_row'] and new[i].decode() == receipt['new_row']
    return dict(queue_physical_line=i + 1, queue_only_pipe_cells=[8, 9, 11],
                all_other_queue_bytes_equal=True, base_row=old[i].decode(), accepted_row=new[i].decode())

def tree_binding(capture, base, tree, require_disk=False):
    manifest = load(A / 'repaired_snapshot_manifest.json')
    expected = {entry['path'] for entry in manifest['files']}
    original = load(A / 'snapshot_manifest.json')
    assert original['head'] == ORIGINAL_HEAD and len(original['files']) == 16
    assert len(expected) == 21
    assert expected == {entry['path'] for entry in original['files']} | {
        TARGET + '/preprint/' + name for name in SUBMISSION_NAMES} | {TARGET + '/PREPRINT_RELEASE.md'}
    assert set(capture.git('diff', '--name-only', base, tree).decode().splitlines()) == expected
    for entry in manifest['files']:
        path = entry['path']
        body = capture.git('show', f'{tree}:{path}')
        assert (len(body), sha(body)) == (entry['bytes'], entry['sha256']), path
        assert capture.git('ls-tree', tree, '--', path).split(b'\t', 1)[0].split() == [
            b'100644', b'blob', entry['git_blob_sha'].encode()]
        if require_disk:
            assert (R / path).read_bytes() == body and pin(R / path)['mode'] == 0o644, path
    for entry in original['files']:
        if entry['path'] == Q:
            continue
        body = capture.git('show', f'{tree}:{entry["path"]}')
        assert (len(body), sha(body)) == (entry['bytes'], entry['sha256'])
    return dict(all_expected_paths_exact=21, all_target_file_hashes_exact=20,
                all_original_target_files_unchanged=15, **queue_binding(capture, base, tree))

def package_integrity(capture, interpreter='python3'):
    clear = current_clearance()
    scratch = capture.directory / 'zip_scratch'
    scratch.mkdir(exist_ok=False)
    with zipfile.ZipFile(A / 'preprint/qss-self-duality-verification.zip') as archive:
        members = archive.infolist()
        assert len(members) == 33 and len({entry.filename for entry in members}) == 33
        for entry in members:
            path = Path(entry.filename)
            assert not entry.is_dir() and not path.is_absolute() and '..' not in path.parts
            assert path.parts[0] == 'qss-self-duality-verification'
            assert entry.external_attr >> 16 == 0o100644
            destination = scratch / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(entry))
            destination.chmod(0o644)
    root = scratch / 'qss-self-duality-verification'
    before = inventory(root)
    for public, author in [('manuscript.tex', 'qss-self-duality-note.tex'),
                           ('zenodo-deposit.json', 'zenodo-deposit.json'),
                           ('verify_supplement.py', 'verify_supplement.py'),
                           ('CONTROL_FORMULA_CORRECTION.md', 'CONTROL_FORMULA_CORRECTION.md')]:
        assert (root / public).read_bytes() == (A / 'preprint' / author).read_bytes()
    identity = load(root / 'SOURCE_IDENTITY.json')
    origins = {
        'controls/check_realization.py': A / 'honda_lifting/check_realization.py',
        'controls/verify_semilinear.py': A / 'semilinear_modules/verify_semilinear.py',
        'controls/verify_intrinsic.py': A / 'intrinsic_invariants/public/verify_intrinsic.py',
        'controls/construction.json': A / 'intrinsic_invariants/public/construction.json',
        'controls/check_integral_flag.py': A / 'priority_supersingular_mechanism/check_integral_flag.py'}
    for name, origin in origins.items():
        body = origin.read_bytes()
        expected = identity['reviewed_original_control_pins'][name]
        assert {key: pin(origin)[key] for key in ('bytes', 'sha256')} == expected
        if name in identity['control_derivations']:
            text = body.decode()
            for edit in identity['control_derivations'][name]['edits']:
                assert text.count(edit['literal_old']) == edit['occurrences']
                text = text.replace(edit['literal_old'], edit['literal_new'])
            body = text.encode()
        assert body == (root / name).read_bytes(), name
    run = capture.run('fresh_package_integrity', [interpreter, '-B', root / 'verify_supplement.py'], cwd=root)
    assert not run.stderr and run.stdout == (A / 'root_preprint_private/dual_replay_v04/0_integrity.stdout').read_bytes()
    result = json.loads(run.stdout)
    assert result['status'] == 'PASS' and result['payload_files'] == 32
    assert result['package_bytes_inventory_unchanged'] and inventory(root) == before
    current_clearance()
    return dict(zip_members=33, payload_files=32, fresh_integrity_whole_output_equal=True,
                exact_original_to_public_derivations=True,
                full_mathematical_replay_bound_by_closed_review03_and_root_v04_pins=True,
                sealed_author_input_count=len(clear['sealed_author_inputs']))
