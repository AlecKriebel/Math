"""Guarded native integration after final clearance, publication and tracker readback.

No local Git/index/ref mutation. Preserve original PR lineage and fresh main.
Never rerun after an uncertain ref outcome without inspecting saved transport.
"""
from pathlib import Path
from datetime import datetime, timezone
import base64
import hashlib
import json
import shutil
import subprocess

ROOT = Path('/Users/alec/Documents/Math')
R = Path(__file__).resolve().parent
D = R.parent / 'initial_review_20261015'
PUB = R.parent / 'publication'
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
B = 'repos/AlecKriebel/Math/'
OLD = 'dc457c741c779fbf90fbfdcdc73f750b3716f561'
PREFIX = 'unsolved_math_prioritization/attempts/30006020/'
assert not (PUB / 'PR_PREPARED.json').exists(), 'Already integrated; only read-only reconciliation is allowed'
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
        raise RuntimeError(f'Native call {seq} failed; reconcile saved outcome before mutation retry')
    return json.loads(p.stdout)


pr = api('GET', 'pulls/218')
assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == OLD
oq = api('GET', 'contents/unsolved_math_prioritization/QUEUE.md?ref=' + OLD)
original_queue = base64.b64decode(oq['content']).decode()
original_row = [x for x in original_queue.splitlines() if '30006020 / OWR-14298589-005' in x]
assert len(original_row) == 1 and original_row[0].split('|')[8].strip() == 'claimed_solved'
main = api('GET', 'git/ref/heads/main')['object']['sha']
main_commit = api('GET', 'git/commits/' + main)
mq = api('GET', 'contents/unsolved_math_prioritization/QUEUE.md?ref=' + main)
main_queue = base64.b64decode(mq['content']).decode()
rows = [x for x in main_queue.splitlines() if '30006020 / OWR-14298589-005' in x]
assert len(rows) == 1
fields = rows[0].split('|')
assert len(fields) == 14
fields[8] = ' claimed_solved '
fields[9] = ' 1/5 '
fields[11] = ' [Credited intermediate-area theorem and verified publication](attempts/30006020/FINAL_DISPOSITION.md) '
fields[12] = ' ' + z['doi_url'] + ' '
queue_row = '|'.join(fields)
new_queue = main_queue.replace(rows[0], queue_row)
assert main_queue.count(rows[0]) == 1
release = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'claimed_solved',
           'author_proof_turns': '1/5', 'mathematical_verdict': 'PASS exact written source target',
           'priority': 'Credited geometric consequence; exact older DGZZ/DL/ABT/AT inputs and announced microscopic work acknowledged; no universal first-priority certificate',
           'original_native_head': OLD, 'original22_files_archived_byte_identical': True,
           'manuscript_reviews': clear, 'publication': z, 'tracker': t,
           'unrefereed': True, 'extensive_AI_assistance': True,
           'external_human_peer_review': False, 'native_merge_at_receipt_creation': 'pending exact readback'}
U = R / 'pr_update/30006020'
F = PUB / 'native_current_source'
assert not F.exists(), 'Native source already prepared; reconcile before another attempt'
shutil.copytree(U, F)
candidate = (U / 'CANDIDATE.md').read_text()
old = 'the credited preprint package is undergoing fresh sequential review.'
assert candidate.count(old) == 1
updated = candidate.replace(old, 'the credited preprint package completed the required sequential review after its precision fix and is published at ' + z['doi_url'] + '.')
assert updated.split('## 1.', 1)[1] == candidate.split('## 1.', 1)[1]
(F / 'CANDIDATE.md').write_text(updated)
disposition = (U / 'FINAL_DISPOSITION.md').read_text()
disposition = disposition.replace('# Current disposition: claimed_solved, publication preparation',
                                  '# Current disposition: claimed_solved, audited and published')
disposition += ('\n## Verified release\n\nSeven-page unrefereed preprint and verification package: ' + z['doi_url'] +
                '. Exact metadata and both files were verified. Tracker row was appended once and read back at ' +
                t['updated_range'] + '. Two sequential NEW full manuscript reviews completed; the first M1 finite-vector '
                'precision issue was fixed globally, and the new final reviewer found no mandatory remaining issue. '
                'The first report remains a one-finding review of its old hashes. FINAL_ACCEPTANCE.json binds the '
                'final frozen preprint and verified release. No mathematical statement was altered by this release-status update.\n')
(F / 'FINAL_DISPOSITION.md').write_text(disposition)
readme = (U / 'README.md').read_text()
readme += '\nVerified publication: ' + z['doi_url'] + '. FINAL_ACCEPTANCE.json and PUBLICATION_RECEIPT.json establish the current release and tracker state. The source/verification archive contains the honestly dated preparation snapshot; these native files add verified administrative status only.\n'
(F / 'README.md').write_text(readme)
with (F / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n' + datetime.now(timezone.utc).isoformat() + ' — case95%: required sequential manuscript reviews completed after global M1 repair; final frozen preprint published at ' + z['doi_url'] + ', exact tracker readback ' + t['updated_range'] + '. Native source integration/readback/merge remains. No proof change.\n')
(F / 'FINAL_ACCEPTANCE.json').write_text(json.dumps(release, indent=2, ensure_ascii=False) + '\n')
(F / 'PUBLICATION_RECEIPT.json').write_text(json.dumps({'publication': z, 'tracker': t}, indent=2) + '\n')
manifest = json.loads((U / 'CURRENT_SOURCE_MANIFEST.json').read_text())
manifest.update(utc=datetime.now(timezone.utc).isoformat(), status='claimed_solved_audited_published',
                frozen_preprint_submission_files=clear['submission_files'],
                publication_status_only_delta='Candidate text below ##1 is byte-identical to the reviewed current candidate; SOURCE_AUDIT and22 archived originals are unchanged.')
manifest['current_files'] = []
for p in sorted(F.iterdir()):
    if p.is_file() and p.name != 'CURRENT_SOURCE_MANIFEST.json':
        raw = p.read_bytes()
        manifest['current_files'].append({'path': p.name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
(F / 'CURRENT_SOURCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
for row in manifest['original_submission_files']:
    raw = (F / 'history/original_submission_20261001' / row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
assert (F / 'SOURCE_AUDIT.md').read_bytes() == (U / 'SOURCE_AUDIT.md').read_bytes()
files = {}
for p in sorted(F.rglob('*')):
    if p.is_file():
        files[PREFIX + p.relative_to(F).as_posix()] = p.read_bytes()
paths = [p for p in R.iterdir() if p.is_file()]
for folder in ['verification', 'pr_update', 'output', 'history']:
    paths += [p for p in (R / folder).rglob('*') if p.is_file()]
for family in ['fresh_review_01', 'fresh_review_02']:
    F = R / family
    seal = F / 'SAFE_AUTHORED_MANIFEST.json'
    paths.append(seal)
    m = json.loads(seal.read_text())
    for row in m['safe_authored_files']:
        p = F / row['path']
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
head = api('POST', 'git/commits', {
    'message': 'Integrate PR218 credited intermediate-area preprint and verified DOI/tracker; preserve original submission',
    'tree': tree, 'parents': [OLD, main]})['sha']
assert api('GET', 'pulls/218')['head']['sha'] == OLD
api('PATCH', 'git/refs/heads/' + pr['head']['ref'], {'sha': head, 'force': False})
assert api('GET', 'pulls/218')['head']['sha'] == head
body = ('Derives the intermediate-area cylinder Poisson law in the principal holomorphic quadratic stratum, '
        'with the square-count cutoff tending to infinity before genus. At every intermediate scale the '
        'process tends to PPP(dx/(2x)), including all fixed joint compact-window count moments. The original '
        '[1/sqrt(g),2/sqrt(g)] count tends to Poisson(log(2)/2), with the same limiting mean and variance.\n\n'
        'The exact weighted model, DL/DGZZ geometric foundation, Aggarwal estimates and ABT/AT probability '
        'inputs are credited. Announced Delecroix–Liu microscopic work and the unavailable manuscript '
        'priority uncertainty are explicit; no universal first-priority or new microscopic theorem is claimed. '
        'The unused OWR4g−4 versus exact6g−6 discrepancy is retained. All22 original files are archived.\n\n'
        'Independent mathematical/source reproduction, extensive bounded priority work and two sequential '
        'fresh manuscript reviews completed. The first precision finding was fixed globally; the new final '
        'review found no mandatory remaining issue. Portable verification reproduces7100 exact assertions, '
        '46233 labelled permutations and123 DVV cases; finite controls supplement the analytic proof. '
        'AI tools were used extensively; this is unrefereed without external human peer review.\n\n'
        'Seven-page preprint and source/verification package: ' + z['doi_url'] + '. '
        'Google Workspace tracker verified at ' + t['updated_range'] + '.')
api('PATCH', 'pulls/218', {'title': '30006020: audited intermediate-area cylinder theorem and published preprint', 'body': body})
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'prepared_head': head, 'original_head': OLD,
           'main_parent': main, 'parents': [OLD, main], 'tree': tree, 'target_queue_row': queue_row,
           'included_owned_pins': pins, 'doi_url': z['doi_url'], 'tracker_range': t['updated_range'],
           'native_merge': 'pending full exact readback', 'local_Git_index_ref_mutations': 0,
           'foreign_main_tree_preserved': True}
(PUB / 'PR_PREPARED.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k != 'included_owned_pins'}, indent=2))
