"""Finalize bounded editorial corrections and bind already completed native evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
A = Path(__file__).resolve().parent
D = A / 'priority_correction_packet'
F = A / 'priority_correction_review'
R = A / 'correction_review_replay_private'
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
pin = lambda p: {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
def require(test, label):
    if not test:
        raise RuntimeError(label)
def save(p, value):
    require(not p.exists(), 'Receipt already exists: ' + str(p))
    p.write_text(json.dumps(value, indent=2) + '\n')
def check(p, expected):
    require(pin(p) == {k: expected[k] for k in ['bytes', 'sha256']}, 'Pin mismatch: ' + str(p))
review = json.loads((F / 'REVIEW_MANIFEST.json').read_bytes())
require(sha((F / 'CORRECTION_REVIEW.md').read_bytes()) == '5c71497386666bb678c9964d002510ac37c98ae299bf75d62c78735275f85f46', 'Reviewed report changed')
require(sha((F / 'REVIEW_MANIFEST.json').read_bytes()) == 'f4d58c939952a1d1a61998e7b0c7f18451d74f0c8ffd7630c4b931a249041842', 'Review manifest changed')
for name, expected in review['files'].items():
    check(F / name, expected)
    require(stat.S_IMODE((F / name).stat().st_mode) == 0o444, 'Closed review mode changed')
execution = json.loads((R / 'execution.json').read_bytes())
require(execution['exit_code'] == 0, 'Completed native replay failed')
for name, expected in execution['inputs'].items():
    check(R / name, expected)
for k in ['stdout', 'stderr']:
    require(pin(R / (k + '.bin')) == {'bytes': execution[k + '_bytes'], 'sha256': execution[k + '_sha256']}, 'Native stream changed')
source = (F / 'validate_artifacts.py').read_bytes()
needle = ("root=Path('" + str(A) + "')").encode()
require(source.count(needle) == 1, 'Unexpected checker path')
require((R / 'validate_artifacts_disposable.py').read_bytes() == source.replace(needle, ("root=Path('" + str(R) + "')").encode()), 'Scientific code adaptation changed')
outputs = ['artifact_validation.json', 'author_checker.stdout', 'author_checker.stderr', 'independent_endpoint_controls.json']
for name in outputs:
    require((R / 'priority_correction_review/executions' / name).read_bytes() == (F / 'executions' / name).read_bytes(), 'Whole output differs: ' + name)
artifact = json.loads((R / 'priority_correction_review/executions/artifact_validation.json').read_bytes())
control = json.loads((R / 'priority_correction_review/executions/independent_endpoint_controls.json').read_bytes())
require((artifact['artifact_assertions'], artifact['author_output']['exact_assertions'], control['exact_assertions'], control['straddling_identity_cases']) == (80, 7852, 1959, 1875), 'Unexpected actual counts')
failed = A / 'root_runs_private/pr316_correction_review_root_replay_actual001'
failed_meta = json.loads((failed / 'execution.json').read_bytes())
require(failed_meta['exit_code'] == 1 and b"KeyError: 'assertions'" in (failed / 'stderr.bin').read_bytes(), 'Original metadata failure missing')
save(A / 'ROOT_CORRECTION_REPLAY.json', {
    'utc': utc(), 'status': 'PASS_DISPOSABLE_ROOT_CORRECTION_REVIEW_REPLAY',
    'completed_native_execution': execution, 'execution_receipt_pin': pin(R / 'execution.json'),
    'artifact_assertions': 80, 'author_assertions': 7852, 'endpoint_controls': 1959,
    'identity_cases': 1875, 'all_four_complete_output_artifacts_byte_identical': True,
    'closed_reviewer_evidence_unchanged': True, 'scientific_code_byte_preserved': True,
    'metadata_finalization_only': True, 'scientific_tests_rerun': False,
    'preserved_outer_metadata_failure': {'directory': str(failed), 'execution': pin(failed / 'execution.json'), 'stderr': pin(failed / 'stderr.bin'), 'reason': "Completed scientific run passed; outer receipt used assertions instead of exact_assertions"}})
native = {}
for name, field, count in [
    ('pr316_original_author_actual001', 'exact_assertions', 7852),
    ('pr316_original_reviewer_actual001', 'assertions', 646),
    ('pr316_root_geometric_crossing_actual001', 'exact_checks', 6124),
    ('pr316_fresh_probability_root001', 'assertions', 263),
    ('pr316_fresh_normalization_root001', 'assertions', 1773)]:
    folder = A / 'root_runs_private' / name
    e = json.loads((folder / 'execution.json').read_bytes())
    require(e['exit_code'] == 0, 'Actual native check failed: ' + name)
    for k in ['stdout', 'stderr']:
        require(pin(folder / (k + '.bin')) == {'bytes': e[k + '_bytes'], 'sha256': e[k + '_sha256']}, 'Native evidence changed')
    for program in e['programs']:
        check(Path(program['path']), program)
    require(json.loads((folder / 'stdout.bin').read_bytes())[field] == count, 'Count mismatch')
    native[name] = {'execution_receipt': pin(folder / 'execution.json'), 'actual_execution': e, 'count_field': field, 'count': count}
before = {p.name: pin(p) for p in D.iterdir() if p.is_file()}
require(len(before) == 6, 'Unexpected packet files')
for name, expected in before.items():
    require(expected == pin(R / 'priority_correction_packet' / name), 'Pre-review packet changed')
accepted = utc()
status = json.loads((D / 'CURRENT_STATUS.json').read_bytes())
old_review = 'Submitted mathematics PASS; operational classical-corollary priority correction awaiting final bound acceptance before branch publication'
require(status['independent_review'] == old_review, 'Unexpected pending status')
status['independent_review'] = 'Submitted mathematics PASS; classical-corollary priority correction and independent prepared-packet mathematical review accepted; bounded editorial finalization separately bound'
status['accepted_correction_review_sha256'] = pin(F / 'CORRECTION_REVIEW.md')['sha256']
status['accepted_correction_review_manifest_sha256'] = pin(F / 'REVIEW_MANIFEST.json')['sha256']
status['utc'] = accepted
status['review_acceptance_utc'] = accepted
(D / 'CURRENT_STATUS.json').write_text(json.dumps(status, indent=2) + '\n')
replacements = {
    'CURRENT_PRIORITY_NOTE.md': [
        ('M(t) <= sqrt(t) + t/(1+(log t)/2)^2,', 'M(t) <= sqrt(t) + t/(1+(log t)/2)^2,  t>=1,'),
        ('their final bound reports must be accepted before this prepared packet is published to the PR.', 'their final mathematical and priority reports have been accepted. The bounded editorial finalization and its exact bytes are recorded separately before branch publication.')],
    'PR_BODY.md': [('This excludes every positive deterministic scale', 'This excludes a proper nondegenerate weak limit for every positive deterministic scale')]
}
readability = [('author1/5', 'author 1/5'), ('Problem1.2', 'Problem 1.2'), ('Erickson1970', 'Erickson 1970'), ("Erickson's1970", "Erickson's 1970"), ('in1970', 'in 1970'), ('All15', 'All 15'), ('all15', 'all 15'), ('the1/5', 'the 1/5'), ('Author7852', 'Author 7852'), ('author7852', 'author 7852'), ('inherited646', 'inherited 646'), ('root6124', 'root 6124'), ('separate6124', 'separate 6124'), ('fresh263/1773', 'fresh 263/1773'), ('fresh263', 'fresh 263'), ('Theorem5', 'Theorem 5'), ('printedp265', 'printed p265'), ('equation2.2', 'equation 2.2'), ('Section1', 'Section 1'), ('Angus–Ding2020', 'Angus–Ding 2020'), ('is108745', 'is 108745'), ('rather than108747', 'rather than 108747'), ('The2015', 'The 2015'), ('separate1987', 'separate 1987')]
for name in ['CURRENT_PRIORITY_NOTE.md', 'PR_BODY.md', 'README.md']:
    s = (D / name).read_text()
    for old, new in replacements.get(name, []):
        require(s.count(old) == 1, 'Unexpected editorial replacement: ' + old)
        s = s.replace(old, new)
    for old, new in readability:
        s = s.replace(old, new)
    (D / name).write_text(s)
title = (D / 'PR_TITLE.txt').read_text()
require(title.count('already_solved1/5') == 1, 'Unexpected title')
(D / 'PR_TITLE.txt').write_text(title.replace('already_solved1/5', 'already_solved, 1/5'))
manifest = json.loads((D / 'PUBLICATION_MANIFEST.json').read_bytes())
T = A / 'snapshot/unsolved_math_prioritization/attempts/9900002'
for name, old in manifest['files'].items():
    p = D / name if (D / name).exists() else T / name
    if p.parent != D:
        check(p, old)
    b = p.read_bytes()
    manifest['files'][name] = {'bytes': len(b), 'sha256': sha(b), 'git_blob_sha1': hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()}
manifest['utc'] = accepted
(D / 'PUBLICATION_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
after = {p.name: pin(p) for p in sorted(D.iterdir()) if p.is_file()}
save(A / 'PRIORITY_CORRECTION_FINALIZATION.json', {
    'utc': utc(), 'status': 'PASS_BOUNDED_EDITORIAL_FINALIZATION_PENDING_INDEPENDENT_BYTE_RECHECK',
    'pre_review_packet': before, 'final_packet': after, 'accepted_report': pin(F / 'CORRECTION_REVIEW.md'),
    'accepted_review_manifest': pin(F / 'REVIEW_MANIFEST.json'),
    'root_completed_replay': pin(A / 'ROOT_CORRECTION_REPLAY.json'), 'native_count_evidence': native,
    'historic_preparation_receipt_unchanged': pin(A / 'PRIORITY_CORRECTION_PREPARATION.json'),
    'bounded_changes': replacements, 'readability_replacements': readability,
    'status_acceptance_fields_and_manifest_regenerated': True,
    'mathematics_changed': False, 'historical_author_review_files_changed': False,
    'author_turns': '1/5', 'operational_status': 'already_solved', 'mathematical_percent': 100,
    'bounded_priority_percent': 100, 'workflow_percent': 75, 'remote_mutations': False,
    'paper': False, 'zenodo': False, 'merge': False, 'tracker': False})
print(json.dumps({'status': 'PASS_BOUNDED_EDITORIAL_FINALIZATION', 'final_packet': after, 'actual_controls': [7852, 646, 6124, 263, 1773, 80, 1959], 'scientific_tests_rerun': False}, indent=2))
