#!/usr/bin/env python3
"""ROOT's actual, bounded prerequisite authoring after personally reading V2.

This records completed reading; it does not certify a future runtime or merge.
Native bodies are read in place, never copied here. All outputs are exclusive.
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
A = Path(__file__).absolute().parent
R = A.parents[2]
F = A / 'current_preparation_family_v2'
S = A / 'current_source_adversary_family_v2'
T = dt.datetime.now(dt.timezone.utc).isoformat()

def sha(body):
    return hashlib.sha256(body).hexdigest()

def read(path):
    assert not path.is_symlink() and not any(p.is_symlink() for p in path.parents)
    assert stat.S_ISREG(path.stat().st_mode)
    return path.read_bytes()

def obj(path):
    return json.loads(read(path))

def row(path):
    body = read(A / path)
    return {'path': path, 'bytes': len(body), 'sha256': sha(body)}

def save(name, value):
    body = value.encode() if type(value) is str else (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
    with (A / name).open('xb') as handle:
        handle.write(body)
        handle.flush()
        os.fsync(handle.fileno())
    return sha(body)

assert R == Path('/Users/alec/Documents/Math') and A.name == 'pr46_30004438'
assert sha(read(F / 'PREPARATION_MANIFEST.json')) == '5ba87a43d1e5da841c8d6f47b6c398c5de55047a447468e1576d2b0cbbd7439e'
assert sha(read(F / 'prepare_current_packet.py')) == 'e6df8cf9b54132d0ec9aee6d4a010e4f8ae95797dbbdd4abd23eb03f86856215'
assert sha(read(F / 'capture_root_builder_operation.py')) == '02a5a169bfc87cb83595d796e375ece467f4073e63ac91f4171af6403606ae8a'
assert sha(read(S / 'MANIFEST.json')) == 'f41b95e4f2cb3bf32943434ec758718112eb922582865e7b4dca016d5a7beb86'
source_manifest = obj(S / 'MANIFEST.json')
assert source_manifest['closing_child_pid'] == 80723 and source_manifest['files_count'] == 189
assert dt.datetime.fromisoformat(source_manifest['closed_utc']) < dt.datetime.fromisoformat(T)
verdict = obj(S / 'verdict.json')
assert verdict['mandatory_corrections'] == [] and verdict['future_acceptance_approved'] is False
cap_path = A.parent / 'pr45_9900007/root_pr46_source_v2_closed_readback_actual_capture'
capture = obj(cap_path / 'CAPTURE.json')
assert capture['pid'] == 83132 and capture['exit_code'] == 0 and capture['completed'] is True
assert sha(read(cap_path / 'stdout.bin')) == capture['stdout']['sha256']
verification = json.loads(read(cap_path / 'stdout.bin'))
assert verification['manifest_sha256'] == sha(read(S / 'MANIFEST.json'))
assert verification['status'] == 'PASS_ROOT_POSTCLOSE_READ_ONLY_FAMILY_MEMBERSHIP_VERIFICATION'
assert dt.datetime.fromisoformat(capture['started_utc']) > dt.datetime.fromisoformat(source_manifest['closed_utc'])
new_record = {
    'schema': 'PR46_ROOT_NEW_SOURCE_ADVERSARY_RECORD_v1',
    'approved_by_root': True, 'created_utc': T,
    'complete_report_personally_read': True, 'new_different_source_adversary': True,
    'closed_clean': True, 'mandatory_corrections': [],
    'preparation_manifest_sha256': sha(read(F / 'PREPARATION_MANIFEST.json')),
    'builder_sha256': sha(read(F / 'prepare_current_packet.py')),
    'operator_sha256': sha(read(F / 'capture_root_builder_operation.py')),
    'manifest': row('current_source_adversary_family_v2/MANIFEST.json'),
    'report': row('current_source_adversary_family_v2/AUDIT.md'),
    'members': [dict(r, path='current_source_adversary_family_v2/' + r['path']) for r in source_manifest['files']],
    'ROOT_postclosing_verification_capture': str(cap_path.relative_to(R) / 'CAPTURE.json'),
    'ROOT_postclosing_verification_capture_sha256': sha(read(cap_path / 'CAPTURE.json')),
    'reconciled_limits': [
        'Isolated dot spelling is admitted; regular-file and exact-topology guards reject it as a member.',
        'Read-ledger/science guards constrain specified fields, not arbitrary extra keys. ROOT authors only contract fields.',
        '29,095 private assertions are independent controls, not production execution.',
        'Full byte reading of receipts does not authenticate unrelated historical primary-source narratives.',
        'Only outer CAPTURE is postchild; original inner GIT_COMMANDS is incremental and its frozen copy is a prefix.'
    ],
    'production_executed': False, 'current_whole_verdict': None,
    'future_acceptance_approved': False
}
save('ROOT_NEW_SOURCE_ADVERSARY_RECORD.json', new_record)

certificate = '''# ROOT PR46 exact known-result acceptance

ROOT_SCOPE_ACCEPTED_EXACT_KNOWN_RESULT_ONLY

PR46 / 30004438 / OWR-17475-003
Original head: a39d178b10f75fb127058b08e0d0002b3ae97f8a
Original GitHub base and merge base: c6975ca76f9f667f1250ba403d0e6da2aafe14d0
Status: already_solved
Original turns: 0/5; source-verification responses: 1; new: 0; audit: 0
Full exact target verified: true
Novelty: false
Existing result: Khazhgali Kozhasov and Mario Kummer, 2020 preprint.
NEW whole-current review: PENDING
Paper/new DOI/tracker: false

ROOT personally read the complete original scientific bodies, full scoped diff,
helpers and complete literal receipts; operative OWR668–669 and the stated v1/v2
theorem proofs; both independent mathematical derivations; the complete raw/prior
and typed SQL audit; unchanged 51/848 actual reproductions; closed V2 source,
605-line builder,129-line operator, execution contract and qualifications; and
the full new SOURCE report. ROOT's separate postclosing child83132 checked every
closed SOURCE member/body/full mode/topology after closing child80723 exited.
The exact theorem is every d>=2, every positive period in RP1 including infinity,
on one nonempty ordinary real-open full ambient dimension2d+1 neighborhood.
Neither finite checks nor credited prior work are presented as a new discovery.
Legacy PDF hashes/pixels are attributed, not freshly authenticated by ROOT.
The source review has no mandatory correction; its dot-path and unspecified-key
limits are expressly retained. Actual runtime, final original inner/outer full
evidence reading, different whole-current review and final integration remain
separate future gates. This certificate approves only the stated known science
and SOURCE prerequisite scope. It does not transfer historical PASS or approve
future native changes. AI tools were used extensively; no human peer review or
formal certification is claimed.
'''
scope_sha = save('ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md', certificate)
evidence = {
    'schema': 'PR46_ROOT_EVIDENCE_BINDINGS_v1', 'approved_by_root': True,
    'created_utc': T,
    'notes': 'ROOT completed and personally reconciled full mathematical, primary-text, original raw/SQL, unchanged helper reproduction, and freshly closed V2 SOURCE evidence; future whole-current/runtime/merge approval remains pending.',
    'manifest': row('root_original_actual_reproduction_v2/MANIFEST.json'),
    'proof_notes': row('ROOT_MATHEMATICAL_REVIEW.md'),
    'summary': row('root_original_actual_reproduction_v2/ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),
    'raw_audit': row('ROOT_COMPLETE_RAW_SQL_AUDIT.json'),
    'source_adversary': row('ROOT_NEW_SOURCE_ADVERSARY_RECORD.json'),
    'operative_preparation_directory': 'current_preparation_family_v2'
}
evidence_sha = save('ROOT_EVIDENCE_BINDINGS.json', evidence)

def git(*argv):
    return subprocess.check_output(['git', *argv], cwd=R, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))

assert git('branch', '--show-current').strip() == b'main'
head = git('rev-parse', 'HEAD').decode().strip()
native = ['unsolved_math_prioritization/' + n for n in [
    'QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json',
    'queue.py','policy.json','manifest.json','cache/problems.json',
    'cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']]
native.append('draft_pr_publication_program_20260930/inventory.json')
native_rows = []
for name in sorted(native):
    body = read(R / name)
    native_rows.append({'path':name,'bytes':len(body),'sha256':sha(body),'full_mode':stat.S_IMODE((R/name).stat().st_mode)})
for name in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json']:
    assert git('show', head + ':' + name) == read(R / name)
assert git('rev-parse', 'HEAD').decode().strip() == head
fresh = {
    'schema':'PR46_ROOT_FRESH13_INPUT_PREIMAGES_v1','approved_by_root':True,'created_utc':T,
    'reason':'Actual live complete13 bodies/full modes and committed native4 match this dated main HEAD. This authorizes only administrative V2 freezing; a new fresh authority is required before integration.',
    'current_head':head,'files':native_rows,'operative_preparation_directory':'current_preparation_family_v2'
}
fresh_sha = save('ROOT_CURRENT_INPUT_PREIMAGES.json', fresh)
reading = obj(F / 'DRAFT_ROOT_READ_LEDGER.json')
reading.update(created_utc=T, reading_completed=True,
    root_flags={k:True for k in reading['root_flags']},
    reading_notes='ROOT personally completed the scopes described in its full mathematical review and scope certificate, prior genuine raw/reproduction evidence and both independent proofs, then read closed V2 builder/operator/contract/qualifications and the full newly closed SOURCE report with honest dot/extra-key limits. Actual postclosing child83132 verified all189 members. No future runtime, whole-current or merge approval is asserted.',
    scope_certificate_sha256=scope_sha,
    preparation_manifest_sha256=sha(read(F/'PREPARATION_MANIFEST.json')),
    source_qualification_sha256=sha(read(F/'SOURCE_PRECISION_QUALIFICATIONS.md')),
    evidence_bindings_sha256=evidence_sha,
    family_manifest_sha256={k:sha(read(A/k/v['manifest']['path'])) for k,v in obj(F/'STATIC_INPUT_BINDINGS.json')['families'].items()})
ledger_sha = save('ROOT_PRIMARY_READ_LEDGER.json', reading)
science = obj(F/'DRAFT_ROOT_SCIENCE_CARD.json')
science.update({k:v for k,v in reading.items() if k != 'schema'})
science.update(exact_known_target_verified=True, full_problem_solved=True,
    full_target_prior_result_verified=True, read_ledger_sha256=ledger_sha,
    current_input_manifest_sha256=fresh_sha)
save('ROOT_SCIENCE_CARD.json', science)
assert git('rev-parse','HEAD').decode().strip() == head
for r in native_rows:
    assert sha(read(R/r['path'])) == r['sha256'] and stat.S_IMODE((R/r['path']).stat().st_mode) == r['full_mode']
print(json.dumps({'status':'PASS_ROOT_ACTUAL_V2_PREREQUISITES_AUTHORED','created_utc':T,'current_head':head,
    'five_prerequisites':[row(n) for n in ['ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_EVIDENCE_BINDINGS.json']],
    'source_record':row('ROOT_NEW_SOURCE_ADVERSARY_RECORD.json'),'future_acceptance_approved':False},indent=2))
