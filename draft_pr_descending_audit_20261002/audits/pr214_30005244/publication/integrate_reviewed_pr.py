"""Guarded native PR integration after final review, DOI and tracker readbacks.

No local Git/index/ref writes. Never repeat an uncertain native ref mutation.
"""
from pathlib import Path
from datetime import datetime, timezone
import base64
import hashlib
import json
import shutil
import subprocess
import zipfile

ROOT = Path('/Users/alec/Documents/Math')
PUB = Path(__file__).resolve().parent
R = PUB.parent / 'preprint'
D = PUB.parent / 'initial_review_20261015'
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
B = 'repos/AlecKriebel/Math/'
OLD = '36d5ef15098163e74bf14c2e696f560ce592affd'
PREFIX = 'unsolved_math_prioritization/attempts/30005244/'
assert not (PUB / 'PR_PREPARED.json').exists(), 'Already integrated: reconcile read-only'
clear = json.loads((R / 'FINAL_CLEARANCE.json').read_text())
assert clear['release_cleared'] and clear['fresh_manuscript_reviews'] >= 2
assert clear['final_frozen_clean_reviews'] >= 1 and not clear['unresolved_mandatory_findings']
for row in clear['submission_files']:
    raw = (R / row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
z = json.loads((PUB / 'ZENODO_VERIFIED_PUBLICATION.json').read_text())
t = json.loads((PUB / 'TRACKER_VERIFIED_APPEND.json').read_text())
assert z['submitted'] and z['metadata_and_files_verified']
assert t['verified'] and t['doi_url'] == z['doi_url']
T = PUB / 'private_transport' / datetime.now(timezone.utc).strftime('native_prepare_%Y%m%dT%H%M%S%fZ')
T.mkdir(parents=True, exist_ok=False)
seq = 0


def api(method, path, payload=None):
    global seq
    seq += 1
    args = [GH, 'api', '--method', method, B + path]
    if payload is not None:
        p = T / f'{seq:03d}-request.json'
        p.write_text(json.dumps(payload))
        args += ['--input', str(p)]
    p = subprocess.run(args, capture_output=True, timeout=60)
    (T / f'{seq:03d}-stdout.json').write_bytes(p.stdout)
    (T / f'{seq:03d}-stderr.txt').write_bytes(p.stderr)
    if p.returncode:
        raise RuntimeError(f'Native call{seq} failed: inspect saved outcome before mutation retry')
    return json.loads(p.stdout)


pr = api('GET', 'pulls/214')
assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == OLD
intake = json.loads((D / 'INTAKE.json').read_text())
oq = api('GET', 'contents/unsolved_math_prioritization/QUEUE.md?ref=' + OLD)
assert oq['sha'] == intake['Queue_blob']
original_queue = base64.b64decode(oq['content']).decode()
original_row = [x for x in original_queue.splitlines() if '30005244 / OWR-11101924-008' in x]
assert len(original_row) == 1 and original_row[0].split('|')[8].strip() == 'claimed_solved'
main = api('GET', 'git/ref/heads/main')['object']['sha']
main_commit = api('GET', 'git/commits/' + main)
probe_tree = main_commit['tree']['sha']
for component in ['unsolved_math_prioritization', 'attempts', '30005244']:
    listing = api('GET', 'git/trees/' + probe_tree)
    assert not listing['truncated']
    matches = [x for x in listing['tree'] if x['path'] == component]
    if not matches:
        break
    assert len(matches) == 1 and matches[0]['type'] == 'tree'
    assert component != '30005244', 'Fresh main acquired this scientific subtree; independently reconcile before integration'
    probe_tree = matches[0]['sha']
mq = api('GET', 'contents/unsolved_math_prioritization/QUEUE.md?ref=' + main)
main_queue = base64.b64decode(mq['content']).decode()
rows = [x for x in main_queue.splitlines() if '30005244 / OWR-11101924-008' in x]
assert len(rows) == 1
fields = rows[0].split('|')
assert len(fields) == 14
fields[8] = ' claimed_solved '
fields[9] = ' 2/5 '
fields[11] = ' [Audited DDA theorem under (G), credited preprint](attempts/30005244/FINAL_DISPOSITION.md) '
fields[12] = ' ' + z['doi_url'] + ' '
queue_row = '|'.join(fields)
assert main_queue.count(rows[0]) == 1
new_queue = main_queue.replace(rows[0], queue_row)
U = R / 'pr_update/30005244'
F = PUB / 'native_current_source'
assert not F.exists(), 'Prepared native source exists: reconcile before another attempt'
with zipfile.ZipFile(R / 'output/dipole_spectrum_verification.zip') as archive:
    local_names = {p.relative_to(U).as_posix() for p in U.rglob('*') if p.is_file()}
    archived_names = {x.removeprefix('pr_update/30005244/') for x in archive.namelist() if x.startswith('pr_update/30005244/')}
    assert local_names == archived_names
    for name in local_names:
        assert (U / name).read_bytes() == archive.read('pr_update/30005244/' + name)
shutil.copytree(U, F)
candidate = (U / 'CANDIDATE.md').read_text()
pending = 'Publication and merge are pending final sequential manuscript reviews and later explicit receipts.'
assert candidate.count(pending) == 1
updated = candidate.replace(pending, 'The preprint has completed the required sequential manuscript reviews and is published at ' + z['doi_url'] + '. The verified publication/tracker receipts and FINAL_ACCEPTANCE.json record this administrative release update; native merge remains pending exact readback.')
assert updated.split('---\n\n', 1)[1] == candidate.split('---\n\n', 1)[1]
(F / 'CANDIDATE.md').write_text(updated)
readme = (U / 'README.md').read_text()
old_readme_status = 'The external manuscript package contains the portable verification runner and fresh sequential whole-manuscript reviews when completed. Mathematical review and qualified preparation have passed; publication remains pending those reviews and explicit final clearance.'
assert readme.count(old_readme_status) == 1
readme = readme.replace(old_readme_status, 'The manuscript package contains the portable verification runner and completed version-bound sequential whole-manuscript reviews. Mathematical review, the qualified bounded priority assessment and final manuscript clearance have completed; verified publication details follow.')
readme += '\nVerified publication: ' + z['doi_url'] + '. FINAL_ACCEPTANCE.json and PUBLICATION_RECEIPT.json establish the current release and exact tracker readback at ' + t['updated_range'] + '. The deposited archive retains its dated preparation snapshot; these native files add administrative release status only.\n'
(F / 'README.md').write_text(readme)
accept = json.loads((U / 'ACCEPTANCE.json').read_text())
accept.update(preprint_review_clearance=True, published_DOI=z['doi'], publication_receipt='PUBLICATION_RECEIPT.json', final_acceptance='FINAL_ACCEPTANCE.json')
(F / 'ACCEPTANCE.json').write_text(json.dumps(accept, indent=2) + '\n')
release = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'claimed_solved',
           'author_proof_turns': '2/5', 'mathematical_verdict': 'PASS explicit(G) off-interval source phenomenon',
           'priority': 'Credited independent exact-model proof; named unavailable dynamic manuscript and other source-access limits retained; no first-priority certification',
           'original_native_head': OLD, 'original31_files_archived_byte_identical': True,
           'manuscript_reviews': clear, 'publication': z, 'tracker': t,
           'unrefereed': True, 'extensive_AI_assistance': True, 'external_human_peer_review': False,
           'native_merge_at_receipt_creation': 'pending exact readback'}
(F / 'FINAL_ACCEPTANCE.json').write_text(json.dumps(release, indent=2) + '\n')
(F / 'PUBLICATION_RECEIPT.json').write_text(json.dumps({'publication': z, 'tracker': t}, indent=2) + '\n')
(F / 'FINAL_DISPOSITION.md').write_text('''# Current disposition: claimed_solved, audited and published

The off-interval convergence result is accepted under the explicit voxel-volume condition(G), including bounded Lipschitz particles and arbitrary translated cubic grids at each fixed complex frequency. It treats the actual zero-diagonal sampled matrix and proves stability, no pollution, multiplicity and norm Riesz-projection convergence. The compact empty-interior rational-grid example is a scope obstruction to an unrestricted extrapolation, not to the regular-particle theorem. Its finite mask index is existential.

Established static lattice, cubic consistency, abstract spectral, continuum pole and sphere perturbation ingredients are credited. The unavailable named2022/2023 dynamic manuscript, unread full Rahola article and metadata-only thesis limit remain explicit. This is a credited independent proof, without first-priority certification. All31 original artifacts are archived byte-for-byte with their original input bindings.

The full analytical manuscript and package completed the required sequential independent AI-assisted adversarial reviews and global fixes. FINAL_ACCEPTANCE.json binds the exact final files and findings. AI tools were used extensively; the preprint is unrefereed and has no asserted external human peer review or proof-assistant certification.

'''+ 'Preprint and verification package: ' + z['doi_url'] + '. Exact metadata and both files were verified. The Google Workspace tracker was appended once and all four cells read back at ' + t['updated_range'] + '. Native merge is pending exact scientific readback.\n')
(F / 'RESEARCH_LOG.md').write_text(datetime.now(timezone.utc).isoformat() + ' — case95%: required sequential manuscript reviews and global fixes completed. The final frozen credited preprint is published at ' + z['doi_url'] + ', exact tracker readback ' + t['updated_range'] + '. Native integration/readback/merge remains. Original31 artifacts and proofs are preserved.\n')
orig = json.loads((U / 'ORIGINAL_SUBMISSION_MANIFEST.json').read_text())
for row in orig['files']:
    raw = (F / row['archive_path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
assert (F / 'SOURCE_AUDIT.md').read_bytes() == (U / 'SOURCE_AUDIT.md').read_bytes()
manifest = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'claimed_solved_audited_published',
            'original_head': OLD, 'current_files': [], 'original_submission_manifest': 'ORIGINAL_SUBMISSION_MANIFEST.json',
            'frozen_preprint_submission_files': clear['submission_files'],
            'delta': 'Administrative release status only beyond the reviewed credited package. Analytical statements/arguments are unchanged, active status labels were corrected during manuscript review, and31 historical artifacts remain byte exact.'}
for p in sorted(F.iterdir()):
    if p.is_file():
        raw = p.read_bytes()
        manifest['current_files'].append({'path': p.name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
(F / 'CURRENT_SOURCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
files = {PREFIX + p.relative_to(F).as_posix(): p.read_bytes() for p in F.rglob('*') if p.is_file()}
paths = [p for p in R.iterdir() if p.is_file()]
for folder in ['verification', 'pr_update', 'history']:
    paths += [p for p in (R / folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
paths += [R / 'output/pdf/dipole_spectrum.pdf', R / 'output/dipole_spectrum_verification.zip']
for folder in sorted(R.glob('fresh_review_*')):
    seal = folder / 'SAFE_AUTHORED_MANIFEST.json'
    assert seal.exists()
    paths.append(seal)
    m = json.loads(seal.read_text())
    authored = m if isinstance(m, list) else m.get('safe_authored_files', m.get('files'))
    for row in authored:
        p = Path(row.get('path', row.get('file')))
        p = p if p.is_absolute() else folder / p
        assert p.resolve().is_relative_to(folder.resolve())
        raw = p.read_bytes()
        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
        paths.append(p)
paths += [p for p in PUB.iterdir() if p.is_file()]
for p in sorted(set(paths)):
    assert not p.is_symlink() and p.resolve().is_relative_to(R.parent.resolve())
    assert not any(part.startswith('private') or part == '__pycache__' for part in p.parts)
    files[p.relative_to(ROOT).as_posix()] = p.read_bytes()
files['unsolved_math_prioritization/QUEUE.md'] = new_queue.encode()
entries = []
pins = []
for path, raw in sorted(files.items()):
    try:
        entry = {'path': path, 'mode': '100644', 'type': 'blob', 'content': raw.decode('utf-8')}
    except UnicodeDecodeError:
        blob = api('POST', 'git/blobs', {'content': base64.b64encode(raw).decode(), 'encoding': 'base64'})['sha']
        entry = {'path': path, 'mode': '100644', 'type': 'blob', 'sha': blob}
    entries.append(entry)
    pins.append({'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                 'git_blob_sha1': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()})
tree = api('POST', 'git/trees', {'base_tree': main_commit['tree']['sha'], 'tree': entries})['sha']
head = api('POST', 'git/commits', {'message': 'Integrate PR214 credited DDA spectral preprint and verified DOI/tracker; preserve original31 artifacts',
                                'tree': tree, 'parents': [OLD, main]})['sha']
assert api('GET', 'pulls/214')['head']['sha'] == OLD
api('PATCH', 'git/refs/heads/' + pr['head']['ref'], {'sha': head, 'force': False})
# Save a durable ref receipt before a potentially stale PR API read.
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'prepared_head': head, 'original_head': OLD,
           'main_parent': main, 'parents': [OLD, main], 'tree': tree, 'target_queue_row': queue_row,
           'included_owned_pins': pins, 'doi_url': z['doi_url'], 'tracker_range': t['updated_range'],
           'native_merge': 'pending full exact readback', 'local_Git_index_ref_mutations': 0,
           'foreign_main_tree_preserved': True}
(PUB / 'PR_PREPARED.json').write_text(json.dumps(receipt, indent=2) + '\n')
body = ('Proves the OWR off-interval discrete-dipole spectral phenomenon under explicit voxel-volume condition(G), '
        'including bounded Lipschitz particles and arbitrary translated cubic grids at every fixed complex frequency. '
        'The actual zero-diagonal sampled matrices have no off-interval pollution and approximate isolated continuum '
        'eigenvalues with algebraic multiplicity and norm-convergent Riesz projections. A compact empty-interior '
        'support with an isolated null anchor supplies a separate rational-grid obstruction to an unrestricted extension.\n\n'
        'CDN static lattice bounds, old cubic consistency, classical compact spectral approximation, continuum poles '
        'and sphere perturbation are credited. The named unavailable2022/2023 dynamic manuscript and other exact '
        'source-access limits remain explicit; no first-priority or universal compact affirmative claim is made. '
        'All31 original artifacts are preserved with their original bindings.\n\n'
        'Independent math/source reproduction, extensive bounded priority audit and required fresh sequential whole-manuscript '
        'reviews and global fixes completed. Finite controls supplement the analytical proof. Extensive AI use; '
        'unrefereed, without external human peer review.\n\nPreprint and verification: ' + z['doi_url'] + '. '
        'Google Workspace tracker verified at ' + t['updated_range'] + '.')
api('PATCH', 'pulls/214', {'title': '30005244: audited DDA spectral convergence under (G) and published preprint', 'body': body})
assert api('GET', 'git/ref/heads/' + pr['head']['ref'])['object']['sha'] == head
print(json.dumps({k: v for k, v in receipt.items() if k != 'included_owned_pins'}, indent=2))
