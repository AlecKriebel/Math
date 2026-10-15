"""Repair reviewed package labels and prepare a new immutable submission version."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, stat, subprocess, sys, zipfile

A = Path(__file__).resolve().parent
P = A / 'preprint_v01'
OLD = A / 'preprint_package_v01'
Q = A / 'preprint_package_v02'
O = A / 'submission_v02'
D = A / 'preprint_repair_private_v02'
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
load = lambda p: json.loads(p.read_bytes())

# This guard precedes any working-file mutation or output-directory creation.
adjudication = load(A / 'ROOT_PREPRINT01_ADJUDICATION.json')
assert adjudication['status'] == 'PASS_MATHEMATICS_PACKAGE_REPAIRS_REQUIRED'
assert adjudication['complete_report_read'] and adjudication['sealed_review_authenticated']
assert not Q.exists() and not O.exists() and not D.exists()
manifest = load(OLD / 'MANIFEST.json')
assert sha((OLD / 'MANIFEST.json').read_bytes()) == '9f4548310b58d667279ae8964cea55eeb79c4ddb9f44ee32fb2435bbf3468228'
for rel, pin in manifest.items():
    for root in [OLD, P]:
        p = root / rel
        assert p.is_file() and not p.is_symlink()
        assert p.stat().st_size == pin['bytes'] and sha(p.read_bytes()) == pin['sha256']
D.mkdir()
jobs = []

def run(label, args, cwd=P):
    j = dict(argv=args, cwd=str(cwd), started_utc=utc(), orchestration_script_sha256=sha(Path(__file__).read_bytes()))
    (D / (label + '_spec.json')).write_text(json.dumps(j, indent=2) + '\n')
    r = subprocess.run(args, cwd=cwd, capture_output=True)
    for k, b in [('stdout', r.stdout), ('stderr', r.stderr)]:
        (D / (label + '.' + k)).write_bytes(b)
        j[k + '_bytes'] = len(b)
        j[k + '_sha256'] = sha(b)
    j.update(ended_utc=utc(), exit_code=r.returncode)
    (D / (label + '_execution.json')).write_text(json.dumps(j, indent=2) + '\n')
    jobs.append(j)
    assert r.returncode == 0 and not r.stderr, label
    return r

code_path = P / 'verify_priority_examples.py'
code = code_path.read_text()
def replace_once(old, new):
    global code
    assert code.count(old) == 1, old
    code = code.replace(old, new)
replace_once('"""Independent, exact, candidate-code-free reproduction of all comparison laws.\n\nUsage: python3 verify_laws.py --output new_results.json',
    '"""Exact reproduction of comparison laws, with explicit count scope.\n\nThe original law checker was authored independently during the priority audit.\nPost-review edits clarify count/provenance labels; the law calculations remain.\nUsage: python3 verify_priority_examples.py --output new_results.json')
replace_once('    determinant_count = 0\n', '    determinant_count = 0\n    canonical_minor_labels = set()\n')
replace_once('                    determinant_count += 1\n',
    '                    determinant_count += 1\n                    direct = (A,B,C,c,a1,a2,b1,b2)\n                    transpose = (B,A,C,c,b1,b2,a1,a2)\n                    canonical_minor_labels.add(min(direct,transpose))\n')
replace_once("'unique_conditioning_2x2_minors_checked':determinant_count,'global_markov_failure_count'",
    "'ordered_conditioning_2x2_minor_evaluations':determinant_count,\n        'distinct_structural_minor_labels_up_to_A_B_transpose':len(canonical_minor_labels),'global_markov_failure_count'")
replace_once("'candidate_code_read':False,", "'original_checker_candidate_verification_code_read':False,\n        'post_review_label_corrections':'Root clarified count/provenance labels after reading candidate code; original law/invariant/recoding calculations retained.',")
replace_once("'minors':v['unique_conditioning_2x2_minors_checked'],",
    "'ordered_minor_evaluations':v['ordered_conditioning_2x2_minor_evaluations'],\n            'transpose_canonical_structural_labels':v['distinct_structural_minor_labels_up_to_A_B_transpose'],")
code_path.write_text(code)
result_path = D / 'priority_laws.json'
run('corrected_priority_laws', [sys.executable, str(code_path), '--output', str(result_path)])
old, new = load(OLD / 'expected/priority_laws.json'), load(result_path)
old.pop('candidate_code_read')
assert new.pop('original_checker_candidate_verification_code_read') is False
new.pop('post_review_label_corrections')
counts = {}
independent = load(A / 'ROOT_CI_MINOR_COUNT_SCOPE_03.json')['results']
for name, law in old['laws'].items():
    n = law['n']
    value = law.pop('unique_conditioning_2x2_minors_checked')
    fixed = new['laws'][name]
    assert fixed.pop('ordered_conditioning_2x2_minor_evaluations') == value == independent['C' + str(n)]['ordered_separation_conditioning_minor_evaluations']
    count = fixed.pop('distinct_structural_minor_labels_up_to_A_B_transpose')
    assert count == independent['C' + str(n)]['distinct_structural_minor_labels_up_to_A_B_transpose']
    counts[name] = dict(ordered_evaluations=value, transpose_canonical_structural_labels=count)
assert old == new, 'A non-label law/invariant/recoding result changed'
shutil.copyfile(result_path, P / 'expected/priority_laws.json')

supp_path = P / 'SUPPLEMENT.md'
supp = supp_path.read_text()
phrase = '`verify_priority_examples.py` was independently authored during the priority audit, without reading candidate verification code.'
assert supp.count(phrase) == 1
supp = supp.replace(phrase, 'The original law/invariant checker underlying `verify_priority_examples.py` was independently authored during the priority audit, without reading candidate verification code. Root subsequently corrected its count/provenance labels and usage filename; the original law calculations were retained.')
phrase = 'C6 has 4,096 MTP2 pairs, 252 ordered separations and 6,384 unique conditioning minors.'
assert supp.count(phrase) == 1
supp = supp.replace(phrase, 'Each C4 has 16 ordered conditioning-minor evaluations and 8 distinct structural labels after identifying A/B transposes. C6 has 4,096 MTP2 pairs, 252 ordered separations and 6,384 ordered conditioning-minor evaluations, corresponding to 3,192 structural labels after identifying A/B transposes. These are evaluation and structural-label counts, not a claim of distinct formal polynomials across different marginalizations.')
phrase = 'Replacing its zeros by 1/10 breaks MTP2. These falsify cancellation and naive smoothing at zeros; they do not refute the existence of a different attractive representation.'
assert supp.count(phrase) == 1
supp = supp.replace(phrase, 'Replacing the zero entries in the supplied unary pin factor and edge factor by 1/10 breaks MTP2. This test concerns entrywise smoothing of those supplied local factors, rather than replacement of zero cells in the joint law. These controls falsify cancellation and that local-factor smoothing shortcut; they do not refute the existence of a different attractive representation.')
supp_path.write_text(supp)

receipt_path = P / 'BUILD_RECEIPT.json'
receipt = load(receipt_path)
driver = A / 'root_build_preprint_v01.py'
driver_hash = sha(driver.read_bytes())
assert driver_hash == '85020339f2a629d3aafb62f63699c4e9c17be2997e910aaeb6630886663a5d03'
for label, job in zip(['compile', 'pdfinfo', 'extract', 'render'], receipt['native_jobs'], strict=True):
    authentic = load(A / 'preprint_build_private_v01' / (label + '_execution.json'))
    assert job == authentic and job['program_sha256'] == driver_hash
    for k in ['stdout', 'stderr']:
        b = (A / 'preprint_build_private_v01' / (label + '.' + k)).read_bytes()
        assert len(b) == job[k + '_bytes'] and sha(b) == job[k + '_sha256']
    job['orchestration_script_sha256'] = job.pop('program_sha256')
receipt['provenance_label_correction'] = dict(recorded_utc=utc(), original_receipt_sha256=manifest['BUILD_RECEIPT.json']['sha256'],
    original_orchestration_script_sha256=driver_hash,
    original_script_git_commit='c5c7b24caf85a2016da806d68894da85feefa8b1',
    original_script_repository_path='draft_pr_descending_audit_20261002/audits/pr311_30005303/root_build_preprint_v01.py',
    explanation='The original program_sha256 field measured the build orchestration script. Renamed to orchestration_script_sha256 from the authentic source and native records. Historical executable binary fingerprints were not captured and are not invented here. Original build timestamps and stream fingerprints are preserved. This dated correction and the original v01 record are separate.',
    original_native_streams_authenticated=True)
receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')

metadata = load(A / 'publication_preparation/DRAFT_ZENODO_METADATA.json')
deposit = dict(metadata=metadata, files=[dict(path='mtp2-edge-closure-note.pdf'), dict(path='mtp2-edge-closure-verification.zip')])
(P / 'zenodo-deposit.json').write_text(json.dumps(deposit, indent=2) + '\n')
readme = (P / 'README.md').read_text()
readme = readme.replace('- `LICENSE.txt`: CC BY 4.0 for the original material in this package.',
    '- `LICENSE.txt`: CC BY 4.0 for the original material in this package.\n- `zenodo-deposit.json`: exact submission metadata; its filenames identify the two separately uploaded files.\n\nThe build receipt is historical. Its dated provenance correction identifies the original orchestration script hash; no historical executable-binary fingerprints are claimed. Current review decisions are recorded separately. The original law checker was authored independently; later count/provenance-label corrections do not assert that their editor had never read candidate code.')
(P / 'README.md').write_text(readme)
assert sha((P / 'mtp2_edge_closure.tex').read_bytes()) == manifest['mtp2_edge_closure.tex']['sha256']
assert sha((P / 'output/pdf/mtp2_edge_closure.pdf').read_bytes()) == manifest['output/pdf/mtp2_edge_closure.pdf']['sha256']

run('active_reproduce', [sys.executable, str(P / 'REPRODUCE.py'), '--out-dir', str(D / 'active_results')])
Q.mkdir()
for rel in sorted(set(manifest) | {'zenodo-deposit.json'}):
    src, dst = P / rel, Q / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    dst.chmod(0o444)
pins = {str(p.relative_to(Q)): dict(bytes=p.stat().st_size, sha256=sha(p.read_bytes())) for p in Q.rglob('*') if p.is_file()}
(Q / 'MANIFEST.json').write_text(json.dumps(pins, indent=2) + '\n')
(Q / 'MANIFEST.json').chmod(0o444)
fresh = D / 'different_location_copy'
shutil.copytree(Q, fresh)
run('portable_reproduce', [sys.executable, str(fresh / 'REPRODUCE.py'), '--out-dir', str(D / 'portable_results')], cwd=fresh)
O.mkdir()
for source, name in [(Q / 'mtp2_edge_closure.tex', 'mtp2-edge-closure-note.tex'), (Q / 'output/pdf/mtp2_edge_closure.pdf', 'mtp2-edge-closure-note.pdf'), (Q / 'zenodo-deposit.json', 'zenodo-deposit.json')]:
    shutil.copyfile(source, O / name)
archive = O / 'mtp2-edge-closure-verification.zip'
members = {str(p.relative_to(Q)): p for p in Q.rglob('*') if p.is_file()}
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for rel, p in sorted(members.items()):
        info = zipfile.ZipInfo(rel, date_time=(2026, 10, 4, 0, 0, 0))
        info.create_system = 3
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
with zipfile.ZipFile(archive) as z:
    assert len(z.infolist()) == len(members) and set(z.namelist()) == set(members)
    assert all(z.read(rel) == p.read_bytes() for rel, p in members.items())
kit = A.parents[2] / 'zenodo_deposit_tool/zenodo.py'
assert sha(kit.read_bytes()) == '26f264df93b657137b343acc05ae87a3e8e60d46cbbb8b822bc327d77b89c277'
run('kit_local_check', [sys.executable, str(kit), 'check', str(O / 'zenodo-deposit.json')], cwd=O)
for p in O.iterdir():
    assert p.is_file()
    p.chmod(0o444)
formal = {p.name: dict(bytes=p.stat().st_size, sha256=sha(p.read_bytes()), mode='0444') for p in O.iterdir()}
submission = dict(recorded_utc=utc(), formal_files=formal, source_package=str(Q), source_package_manifest_sha256=sha((Q / 'MANIFEST.json').read_bytes()),
    archive_member_sha256={rel: sha(p.read_bytes()) for rel, p in sorted(members.items())}, archive_member_mode='0644',
    manuscript_and_pdf_unchanged=True, first_review_repairs_addressed=['R1', 'R2', 'R3'], fresh_second_review_pending=True, publication_ready=False)
(O / 'SUBMISSION_MANIFEST.json').write_text(json.dumps(submission, indent=2) + '\n')
(O / 'SUBMISSION_MANIFEST.json').chmod(0o444)
assert all(stat.S_IMODE(p.stat().st_mode) == 0o444 for p in Q.rglob('*') if p.is_file())
assert all(stat.S_IMODE(p.stat().st_mode) == 0o444 for p in O.iterdir())
result = dict(recorded_utc=utc(), status='PASS_V02_LABEL_REPAIRS_AND_PORTABLE_SUBMISSION_PREPARATION', repairs=['R1 orchestration hash label', 'R2 ordered/minor-label count scope', 'R3 actual checker usage filename'],
    additional_root_clarification='Supplement explicitly identifies the smoothed entries as zeros of supplied local factors, not joint-law zero cells; original control unchanged.',
    non_count_law_invariant_recoding_results_exactly_unchanged=True, corrected_counts=counts, manuscript_and_pdf_unchanged=True,
    package_manifest_sha256=sha((Q / 'MANIFEST.json').read_bytes()), package_payload_files=len(pins),
    formal_submission_files=formal, archive_all_members_exact=True, native_jobs=jobs, original_v01_preserved=True,
    second_fresh_review_pending=True, publication_ready=False, math_percent=100, bounded_priority_percent=100, workflow_percent=65)
assert not (A / 'ROOT_PREPRINT_REPAIR_V02.json').exists()
(A / 'ROOT_PREPRINT_REPAIR_V02.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'native_jobs'}, indent=2))
