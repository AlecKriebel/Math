"""Authenticate the completed first review and record its actual repair obligations."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat

A = Path(__file__).resolve().parent
R = A / 'preprint_review_01'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_bytes())
out = A / 'ROOT_PREPRINT01_ADJUDICATION.json'
assert not out.exists()
pins = {'FINAL_REVIEW.md': 'd9eb02de0a037159b6a618b7da391876f4606ba83582281831d0f79cb7f9eb9c',
    'FINAL_SEAL_MANIFEST.json': '41f47c6204cf050e1275cf678a28c5a648285fe3d2a831097c54c226129655b8',
    'FINAL_SEAL_VERIFICATION.json': '0b875b09836eda51c9cdbeec9526dd75ee938b145156b527d1b40cc4773a98ab'}
for rel, value in pins.items():
    p = R / rel
    assert not p.is_symlink() and sha(p) == value and stat.S_IMODE(p.stat().st_mode) == 0o444
manifest = load(R / 'FINAL_SEAL_MANIFEST.json')
assert manifest['file_count'] == len(manifest['files']) == 376
listed = set()
def verify(row):
    p = Path(row['path'])
    assert p.is_file() and not p.is_symlink()
    assert p.stat().st_size == row['size_bytes'] and sha(p) == row['sha256']
    assert stat.S_IMODE(p.stat().st_mode) == 0o444
for row in manifest['files']:
    p = Path(row['path'])
    assert p.is_relative_to(R) and str(p.relative_to(R)) == row['relative_path']
    assert row['relative_path'] not in listed
    listed.add(row['relative_path'])
    verify(row)
excluded = set(manifest['terminal_receipt_exclusions'])
assert len(excluded) == 9 and not (excluded & listed)
assert {str(p.relative_to(R)) for p in R.rglob('*') if p.is_file()} == listed | excluded
for rel in excluded:
    p = R / rel
    assert not p.is_symlink() and stat.S_IMODE(p.stat().st_mode) == 0o444
verification = load(R / 'FINAL_SEAL_VERIFICATION.json')
assert verification['passed'] and verification['body_files_hash_size_mode_verified'] == 376
assert verification['source_only_26_pins_modes_unchanged'] and verification['package_12_pins_modes_unchanged']
for row in load(R / 'SOURCE_ONLY_FREEZE_MANIFEST.json')['files']:
    verify(row)
for row in verification['package_inputs']:
    assert Path(row['path']).is_relative_to(A / 'preprint_package_v01')
    verify(row)
driver = load(R / 'private/commands/final_driver.json')
assert driver['exit_code'] == 0
for key in ['manifest', 'verification', 'final_report', 'stdout', 'stderr']:
    verify(driver[key])
for job in driver['jobs']:
    assert job['exit_code'] == 0
    for key in ['stdout', 'stderr']:
        verify(job[key])
native = []
for rel in ['029_external_reproduction.json', '043_independent_finite_checks.json', '061_mutant_controls_retry_v02.json', '080_independent_artifact_comparison.json']:
    p = R / 'private/commands' / rel
    j = load(p)
    assert j['exit_code'] == 0
    for key in ['stdout', 'stderr']:
        row = j[key]
        q = Path(row['path'])
        assert q.is_relative_to(R) and q.stat().st_size == row['size_bytes'] and sha(q) == row['sha256']
    native.append(dict(receipt=rel, started_utc=j['started_utc'], finished_utc=j['finished_utc'], exit_code=0))
assert load(R / 'INDEPENDENT_CHECK_RESULTS.json')['priority_laws']['released_candidate_C6']['distinct_formal_minor_polynomials_up_to_sign'] == 1176
controls = load(R / 'MUTANT_AND_DENSITY_RESULTS.json')['mutants_and_runner_negatives']
assert len(controls) == 7 and all(x['exit'] == 1 and x['caught'] for x in controls)
result = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), status='PASS_MATHEMATICS_PACKAGE_REPAIRS_REQUIRED',
    complete_report_read=True, sealed_review_authenticated=True, final_pins=pins,
    body_files_authenticated=376, terminal_files_measured_0444=9, source_gate_and_twelve_inputs_unchanged=True,
    root_content_read_scope='Complete final report, independent_checks.py, mutant_controls.py, capture.py, verify_artifacts.py and all three result reports read. Full first-report display was reread separately after an initial combined display truncated. All sealed bodies authenticated mechanically; no claim of full reads of all private primary sources or raw streams.',
    successful_scientific_native_receipts=native,
    required_repairs={'R1': 'Actual old hash is the orchestration script, confirmed from authentic source and full native stdout/stderr; rename with dated correction and disclose absent historical executable pins.',
        'R2': 'Rename ordered evaluation counts; new explicitly defined transpose-canonical structural-label counts use actual deduplication and independent root count checks. Do not equate these with formal-polynomial uniqueness.',
        'R3': 'Correct direct-script usage filename.'},
    additional_root_clarification='Specify that the smoothing control replaces zero entries of supplied local factors, not joint-law zero cells.',
    optional_editorial_suggestions_adjudication='Existing packet terminology is explained by included tables; v1 is stated explicitly in the citation and version-pinned in new upload metadata. Catalogued PQ report label is supported. Optional suggestions do not constitute mathematical or submission defects.',
    previous_priority_checker_authorship='Root authenticated the source-first factorization family and its code-release boundary earlier; new output will name original authorship separately from subsequent root edits.',
    mathematical_defect_found=False, all_required_repairs_applied=False, second_new_whole_review_required=True,
    math_percent=100, bounded_priority_percent=100, workflow_percent=60, publication_ready=False, persistent_goal_complete=False)
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
