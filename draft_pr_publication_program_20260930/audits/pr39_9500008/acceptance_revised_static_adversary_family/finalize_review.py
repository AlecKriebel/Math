"""Finalize only this independently authored review directory.

No reviewed helper import/execution; no live administration or Git mutation.
"""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os

F = Path(__file__).resolve().parent
A = F.parent
R = A.parents[2]
S = A / 'acceptance_execution_preparation_family/integration_source_revision'
def sha(b):
    return hashlib.sha256(b).hexdigest()
def parse(raw):
    def pairs(rows):
        value = {}
        for k, v in rows:
            assert k not in value
            value[k] = v
        return value
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
def pin(p):
    raw = p.read_bytes()
    return {'path': p.relative_to(R).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}
def write(n, value):
    with (F / n).open('x') as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + '\n')
def closure(root, manifest_name, expected_sha, count):
    raw = (root / manifest_name).read_bytes()
    assert sha(raw) == expected_sha
    manifest = parse(raw)
    members = manifest['files']
    assert len(members) == count and manifest_name not in {z['path'] for z in members}
    files, dirs = set(), set()
    for p in root.rglob('*'):
        assert not p.is_symlink() and (p.is_file() or p.is_dir())
        (dirs if p.is_dir() else files).add(p.relative_to(root).as_posix())
    names = {z['path'] for z in members} | {manifest_name}
    assert files == names
    assert dirs == {q.as_posix() for n in names for q in PurePosixPath(n).parents if q.as_posix() != '.'}
    for z in members:
        raw = (root / z['path']).read_bytes()
        assert len(raw) == z['bytes'] and sha(raw) == z['sha256']
    return pin(root / manifest_name)
revision = closure(S, 'PREPARATION_MANIFEST.json', '522cf5062ffcb1aa9c60cb0054063b0f2801378446f2288d7f85e81ee9a70ae7', 17)
old = closure(A / 'acceptance_preparation_family', 'PREPARATION_MANIFEST.json', 'f66df61cb4b57ae63cc007fed3c4dabf9e67e027f1d428d4e0ffbc75a6332fca', 15)
old_audit = closure(A / 'acceptance_static_adversary_family', 'MANIFEST.json', 'c782c65b31ef0f38c14bcf49577d11b66b8e19b63b0cce83718f651b3d6f0c9a', 26)
execution = F / 'own_actual_execution_01'
assert {p.name for p in execution.iterdir()} == {'CAPTURE.json', 'prelaunch_source.py', 'stdout.bin', 'stderr.bin'}
capture = parse((execution / 'CAPTURE.json').read_bytes())
assert capture['actual_execution'] is True and capture['completed'] is True and type(capture['pid']) is int and capture['pid'] == 28624
assert type(capture['exit_code']) is int and capture['exit_code'] == 0 and capture['status'] == 'PASS' and capture['stdin_supplied'] is False
assert capture['reviewed_helpers_imported_or_executed'] is False and capture['unchanged_own_source_after'] is True
assert capture['argv'] == ['/usr/bin/python3', '-B', str(F / 'independent_static_controls.py')] and capture['cwd'] == str(F)
start, end = dt.datetime.fromisoformat(capture['started_utc']), dt.datetime.fromisoformat(capture['finished_utc'])
assert start.utcoffset() == end.utcoffset() == dt.timedelta(0) and start <= end
for k in ['prelaunch_source', 'stdout', 'stderr']:
    z = capture[k]
    raw = (execution / z['path']).read_bytes()
    assert len(raw) == z['bytes'] and sha(raw) == z['sha256']
assert (execution / 'prelaunch_source.py').read_bytes() == (F / 'independent_static_controls.py').read_bytes()
assert sha((execution / 'prelaunch_source.py').read_bytes()) == capture['source_sha256']
assert (execution / 'stderr.bin').read_bytes() == b''
result = parse((execution / 'stdout.bin').read_bytes())
assert result['status'] == 'PASS_SOURCE_ONLY_STATIC_REVIEW_CONTROLS' and result['reviewed_helpers_imported_or_executed'] is False
assert result['source_manifest_sha256'] == revision['sha256'] and result['exact_negative_inputs'] == 14
source_names = ['pr39_guards.py', 'integrate_reviewed_partial.py', 'seal_final_evidence.py', 'state_mirror_reconciliation.py', 'verify_post_acceptance.py', 'static_revision_checks.py']
read_names = ['CONTRACT.md', 'INPUT_BINDINGS.json', 'SOURCE_BINDINGS.json', 'REVISION_BASIS.json', 'REVISION.patch', 'DRAFT_FINAL_PLAN.json', 'SCIENTIFIC_SCOPE.json', 'PREPARATION_MANIFEST.json', 'STATIC_VALIDATION.json', 'ROOT_REVIEW_CHECKLIST.md', 'README.md', 'RESEARCH_LOG.md']
coverage = {'schema': 'pr39-revised-static-adversary-full-read-coverage/v1',
    'all_five_helper_bodies_and_static_checker_literally_fully_read': True,
    'sources': [{**pin(S / n), 'lines': len((S / n).read_text().splitlines()), 'fully_read': True} for n in source_names],
    'complete_contract_binding_scientific_and_draft_objects_read': [{**pin(S / n), 'fully_read': True} for n in read_names],
    'prior_three_defect_report_and_verdict_fully_read': [pin(A / 'acceptance_static_adversary_family' / n) for n in ['STATIC_ADVERSARIAL_REVIEW.md', 'FAMILY_VERDICT.json']],
    'own_controls_source_authored_and_fully_read_before_launch': pin(F / 'independent_static_controls.py'),
    'actual_own_capture': pin(execution / 'CAPTURE.json'),
    'bound_input_coverage': result,
    'review_scope': 'Administrative source revision and byte/type preservation; no independent rereading claim for entire historical primary mathematical corpus.',
    'candidate_helpers_imported_or_executed': False,
    'foreign_copied_inputs': [], 'foreign_exclusions': []}
write('READ_COVERAGE.json', coverage)
now = dt.datetime.now(dt.timezone.utc).isoformat()
verdict = {'schema': 'pr39-revised-acceptance-source-static-adversary/v1', 'utc': now,
    'verdict': 'PASS_SOURCE_ONLY_REVISED_ACCEPTANCE_REVIEW', 'mandatory_corrections': [],
    'reviewed_preparation_manifest': revision, 'original_preparation_manifest': old, 'old_three_defect_manifest': old_audit,
    'all_three_mandatory_repairs_verified': True,
    'atomic_exclusive_file_publication_and_collision_temporary_retention': True,
    'literal_capture_four_distinct_root_basenames': True,
    'parsed_aware_ordered_UTC_clocks': True,
    'new_nested_audit_and_repository_anchors_verified': True,
    'four_unchanged_helpers_three_unchanged_complete_objects': True,
    'entire_revision_patch_reconstructed': True,
    'draft_root_flags_false_and_preparation_digest_null': True,
    'original2of5_zero_new_audit0_no_paper_Doi_tracker': True,
    'current_runtime_reasoning_deadline_null': True,
    'scientific_scope_status': 'UNSOLVED', 'positive_novelty_claim': False,
    'scientific_discovery_percent': 0, 'review_workflow_completion_percent': 100,
    'new_substantive_attempts': 0, 'audit_turns': 0,
    'reviewed_helpers_imported_or_executed': False, 'native_shared_canonical_Git_remote_mutations': False,
    'root_actual_source_reading_new_pins_fresh_native13_and_acceptance_execution_remain_required': True,
    'optional_hardening': [
        'Root actual outer/internal interval containment can strengthen truthful clock evidence; no such containment is claimed by the source contract.',
        'Author static checker terminal-Z positive cases require a newer Python or normalization if rerun on Python3.9.6; production +00:00 stamp is supported.',
        'Cosmetic preflight error string names PR37 while exact literal predecessor is correctly PR38.'],
    'report': pin(F / 'REPORT.md'), 'read_coverage': pin(F / 'READ_COVERAGE.json'), 'own_execution_capture': pin(execution / 'CAPTURE.json'),
    'full_own_result_stdout': pin(execution / 'stdout.bin'), 'foreign_exclusions': [], 'first_party_only': True}
write('FAMILY_VERDICT.json', verdict)
with (F / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n' + now + ' — Workflow review 100%, scientific discovery 0%. PASS_SOURCE_ONLY_REVISED_ACCEPTANCE_REVIEW; no mandatory repairs. Full report/read coverage/verdict and exact own execution preserved. Revised17/original15/static26 closures checked again unchanged. Closing strict first-party manifest, literal self only, zero foreign exclusions. Root owns checkpoint publication and all subsequent actual execution.\n')
members = []
dirs = set()
for p in sorted(F.rglob('*')):
    assert not p.is_symlink() and (p.is_dir() or p.is_file())
    if p.is_dir():
        dirs.add(p.relative_to(F).as_posix())
    else:
        raw = p.read_bytes()
        members.append({'path': p.relative_to(F).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)})
        if p.suffix == '.json':
            parse(raw)
names = {z['path'] for z in members}
assert 'MANIFEST.json' not in names and dirs == {q.as_posix() for n in names for q in PurePosixPath(n).parents if q.as_posix() != '.'}
write('MANIFEST.json', {'schema': 'pr39-revised-acceptance-adversary-exact-first-party-closure/v1', 'utc': now, 'files_count': len(members), 'files': members,
    'self_excluded': ['MANIFEST.json'], 'foreign_exclusions': [], 'source_only_review': True, 'candidate_helpers_imported_or_executed': False, 'new_substantive_attempts': 0, 'audit_turns': 0})
manifest_pin = closure(F, 'MANIFEST.json', sha((F / 'MANIFEST.json').read_bytes()), len(members))
for p in F.rglob('*'):
    if p.is_file():
        p.chmod(0o444)
print(json.dumps({'status': 'CLOSED_REVIEW', 'verdict': verdict['verdict'], 'manifest': manifest_pin, 'authored_members': len(members), 'foreign_exclusions': [], 'reviewed_source_manifest_sha256': revision['sha256'], 'own_capture': pin(execution / 'CAPTURE.json'), 'family_verdict': pin(F / 'FAMILY_VERDICT.json'), 'report': pin(F / 'REPORT.md')}, indent=2, sort_keys=True))
