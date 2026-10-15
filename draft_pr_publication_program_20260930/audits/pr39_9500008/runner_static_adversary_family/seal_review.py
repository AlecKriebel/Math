"""Seal own source-only runner review; never execute candidate source."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json

F = Path(__file__).resolve().parent
A = F.parent
R = A.parents[2]
def sha(b):
    return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(values):
        d = {}
        for k, v in values:
            assert k not in d
            d[k] = v
        return d
    return json.loads(b, object_pairs_hook=pairs, parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
def pin(p):
    b = p.read_bytes()
    return {'path': p.relative_to(R).as_posix(), 'bytes': len(b), 'sha256': sha(b)}
def write(n, obj):
    with (F / n).open('x') as stream:
        stream.write(json.dumps(obj, indent=2, sort_keys=True) + '\n')
E = F / 'own_actual_execution_01'
capture = parse((E / 'CAPTURE.json').read_bytes())
assert {p.name for p in E.iterdir()} == {'CAPTURE.json', 'prelaunch_source.py', 'stdout.bin', 'stderr.bin'}
assert capture['actual_execution'] is True and capture['completed'] is True and type(capture['pid']) is int and capture['pid'] == 37641
assert type(capture['exit_code']) is int and capture['exit_code'] == 0 and capture['status'] == 'PASS'
assert capture['runner_and_helpers_imported_or_executed'] is False and capture['stdin_supplied'] is False
assert capture['argv'] == ['/usr/bin/python3', '-B', str(F / 'own_static_controls.py')] and capture['cwd'] == str(F)
start, end = dt.datetime.fromisoformat(capture['started_utc']), dt.datetime.fromisoformat(capture['finished_utc'])
assert start.utcoffset() == end.utcoffset() == dt.timedelta(0) and start <= end
for channel in ['prelaunch_source', 'stdout', 'stderr']:
    z = capture[channel]
    raw = (E / z['path']).read_bytes()
    assert len(raw) == z['bytes'] and sha(raw) == z['sha256']
assert (E / 'prelaunch_source.py').read_bytes() == (F / 'own_static_controls.py').read_bytes()
assert sha((E / 'prelaunch_source.py').read_bytes()) == capture['source_sha256']
assert (E / 'stderr.bin').read_bytes() == b''
result = parse((E / 'stdout.bin').read_bytes())
assert result['status'] == 'PASS_STATIC_SOURCE_ONLY' and result['runner_sha256'] == '2de301f2f37837b8729d606962599c04bd380d1f6473cc4a76a9c46cef1c0b88'
runner = A / 'execute_root_acceptance_revised.py'
assert sha(runner.read_bytes()) == result['runner_sha256']
preparation = A / 'root_runner_revision_preparation_family'
assert sha((preparation / 'MANIFEST.json').read_bytes()) == 'a93237f6ecaf652942374fcb2829a534ee8edbb8d29f44c41b047a58bc15fef9'
source_bindings = parse((preparation / 'SOURCE_BINDINGS.json').read_bytes())
for row in [source_bindings['original_runner'], source_bindings['revised_runner'], source_bindings['revised_preparation_manifest'], source_bindings['revised_source_binding_record'], *source_bindings['revised_helpers']]:
    p = R / row['path']; raw = p.read_bytes()
    assert p.is_file() and not p.is_symlink() and len(raw) == row['bytes'] and sha(raw) == row['sha256'] and (p.stat().st_mode & 0o7777) == row['mode']
now = dt.datetime.now(dt.timezone.utc).isoformat()
coverage = {'schema': 'pr39-root-runner-static-full-read-coverage/v1', 'utc': now,
    'entire_342_line_runner_literally_read': True, 'runner': pin(runner),
    'complete_runner_preparation_members_literally_read': [pin(preparation / n) for n in ['CONTRACT.md', 'READ_NOTES.md', 'RESEARCH_LOG.md', 'ROOT_REVIEW_CHECKLIST.md', 'SOURCE_BINDINGS.json', 'STATIC_INSPECTION.json', 'MANIFEST.json']],
    'all_five_production_helpers_previously_fully_read_and_bytes_modes_rechecked': source_bindings['revised_helpers'],
    'prior_closed_integration_review': pin(A / 'acceptance_revised_static_adversary_family/MANIFEST.json'),
    'dated_original_native13_list_read_only_not_imposed_as_current': pin(A / 'ROOT_CURRENT_INPUT_PREIMAGES.json'),
    'own_actual_control_capture': pin(E / 'CAPTURE.json'), 'whole_own_result': result,
    'local_OS_primary_header': {'path': '/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/sys/stdio.h', 'operative_lines_read': [37, 51], 'RENAME_EXCL': '0x00000004'},
    'no_candidate_runner_or_helper_import_execution': True, 'no_native_canonical_Git_remote_write': True,
    'foreign_copied_members': [], 'foreign_exclusions': []}
write('READ_COVERAGE.json', coverage)
verdict = {'schema': 'pr39-root-runner-source-adversary/v1', 'utc': now, 'verdict': 'PASS_SOURCE_ONLY_ROOT_RUNNER_REVIEW', 'mandatory_corrections': [],
    'reviewed_runner': pin(runner), 'reviewed_preparation_manifest': pin(preparation / 'MANIFEST.json'),
    'exact_revised_preparation_SHA': source_bindings['revised_preparation_manifest']['sha256'],
    'interface_native13_source_modes_HEAD_capture_publication_failure_retention_checks_pass': True,
    'actual_runner_or_reviewed_helper_execution': False, 'actual_acceptance_status': 'PENDING',
    'root_full_report_read_and_actual_gates_still_required': True,
    'optional_limits': ['Before/after does not defeat hostile transient swaps.', 'Immediate child kill is not process-group termination; drain or early query can wait on an external process.', 'Failed storage retains available written bytes.', 'Root should inspect internal receipt interval against outer child clocks.'],
    'scientific_full_target_status': 'UNSOLVED', 'new_substantive_attempts': 0, 'audit_turns': 0,
    'scientific_discovery_percent': 0, 'review_workflow_completion_percent': 100,
    'own_control_capture': pin(E / 'CAPTURE.json'), 'report': pin(F / 'REPORT.md'), 'read_coverage': pin(F / 'READ_COVERAGE.json'),
    'first_party_only': True, 'foreign_exclusions': []}
write('FAMILY_VERDICT.json', verdict)
with (F / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n' + now + ' — Workflow review 100%, scientific discovery 0%. PASS_SOURCE_ONLY_ROOT_RUNNER_REVIEW; no mandatory corrections. Whole source/report/read coverage and genuine own child evidence retained. Exact first-party closure now sealed, literal self only, zero foreign exclusions. Every old root/source/failure remains untouched; root alone publishes checkpoints and performs actual acceptance.\n')
files, dirs = [], set()
for p in sorted(F.rglob('*')):
    assert not p.is_symlink() and (p.is_file() or p.is_dir())
    if p.is_dir():
        dirs.add(p.relative_to(F).as_posix())
    else:
        raw = p.read_bytes()
        if p.suffix == '.json':
            parse(raw)
        files.append({'path': p.relative_to(F).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)})
names = {z['path'] for z in files}
assert 'MANIFEST.json' not in names
assert dirs == {q.as_posix() for n in names for q in PurePosixPath(n).parents if q.as_posix() != '.'}
write('MANIFEST.json', {'schema': 'pr39-root-runner-static-adversary-exact-closure/v1', 'utc': now, 'files_count': len(files), 'files': files,
    'self_excluded': ['MANIFEST.json'], 'foreign_exclusions': [], 'source_only': True,
    'reviewed_runner_or_helpers_imported_or_executed': False, 'new_substantive_attempts': 0, 'audit_turns': 0})
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()} == names | {'MANIFEST.json'}
for z in files:
    raw = (F / z['path']).read_bytes()
    assert len(raw) == z['bytes'] and sha(raw) == z['sha256']
for p in F.rglob('*'):
    if p.is_file():
        p.chmod(0o444)
print(json.dumps({'status': 'CLOSED', 'verdict': verdict['verdict'], 'authored_members': len(files), 'manifest': pin(F / 'MANIFEST.json'), 'verdict_pin': pin(F / 'FAMILY_VERDICT.json'), 'report': pin(F / 'REPORT.md'), 'own_capture': pin(E / 'CAPTURE.json')}, indent=2, sort_keys=True))
