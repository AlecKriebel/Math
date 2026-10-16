"""Read-only package/native-object and history checks; write review receipt only."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, stat, subprocess, zipfile

O = Path(__file__).resolve().parent
R = O.parent
D = R.parent/'initial_review_20261015'
repo = Path('/Users/alec/Documents/Math')
extracted = O/'private/extracted'
original = json.loads((extracted/'pr_update/30005244/ORIGINAL_SUBMISSION_MANIFEST.json').read_text())
head = original['original_PR_head']
rows = []
for row in original['files']:
    archived = (extracted/'pr_update/30005244'/row['archive_path']).read_bytes()
    native = subprocess.check_output(['git','--no-optional-locks','cat-file','blob',head+':'+row['native_path']],cwd=repo)
    assert native == archived
    blob = hashlib.sha1(b'blob '+str(len(native)).encode()+b'\0'+native).hexdigest()
    assert blob == row['native_blob']
    rows.append({'native_path':row['native_path'],'native_blob':blob,'bytes':len(native),'sha256':hashlib.sha256(native).hexdigest()})
assert len(rows) == 31
H = extracted/'history/review01_frozen'
history = json.loads((H/'HISTORY_MANIFEST.json').read_text())
for row in history['files']:
    raw = (H/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
old_frozen = json.loads((H/'FROZEN_INPUTS.json').read_text())
for row in old_frozen['submission_files']:
    raw = (H/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
with zipfile.ZipFile(H/'output/dipole_spectrum_verification.zip') as z:
    assert z.testzip() is None
    manifest = json.loads(z.read('PACKAGE_FILES.json'))
    assert len(z.namelist())==136 and len(manifest['files'])==135
    assert set(z.namelist())=={x['path'] for x in manifest['files']}|{'PACKAGE_FILES.json'}
    for row in manifest['files']:
        raw=z.read(row['path'])
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
old_review_manifest=json.loads((R/'fresh_review_01/SAFE_AUTHORED_MANIFEST.json').read_text())
for row in old_review_manifest['safe_authored_files']:
    raw=(R/'fresh_review_01'/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    assert raw==(extracted/'audits/fresh_review_01'/row['path']).read_bytes()
active=(R/'pr_update/30005244/CANDIDATE.md').read_text()
helper=(R/'prepare_supporting_materials.py').read_text()
assert '**Unreviewed.**' not in active
assert 'Independent review and a broader novelty check remain required.' not in active
assert 'Original analytical derivation. Current validation' in active
assert 'old_status' in helper and 'qualified_candidate = qualified_candidate.replace(old_review' in helper
assert 'Python3.14.6 with NumPy2.3.4 and SymPy1.14.0' in helper
assert 'Python3.13' not in helper
assert 'first run `mkdir -p output/pdf`' in (R/'README.md').read_text()
assert 'Equip full-lattice sequences with squared norm $h^3' in (R/'dipole_spectrum.tex').read_text()
assert '257--268' in (R/'dipole_spectrum.tex').read_text()
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'native_head':head,'all31_native_head_bytes_verified':True,'native_files':rows,
        'historical_snapshot_all_hashes_verified':True,'old_zip_members':136,'old_zip_payloads':135,
        'old_review_seal_valid_and_archived_identically':True,'D1_globally_fixed':True,
        'D2_globally_fixed':True,'full_lattice_norm_AT_pages_compilation_directory_clarifications_present':True,
        'historical_checkers_not_replayed_against_current_inputs':True,'mutation_scope':'Receipt only; native Git blobs were read without index/ref changes.'}
(O/'NATIVE_HISTORY_REPAIR_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='native_files'},indent=2))
