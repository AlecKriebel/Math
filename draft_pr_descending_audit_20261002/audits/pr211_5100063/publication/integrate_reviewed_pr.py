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
OLD = '9d7b623203b525386da3d9d91548c79e7445a11c'
PREFIX = 'unsolved_math_prioritization/attempts/5100063/'
assert not (PUB / 'PR_PREPARED.json').exists(), 'Already integrated: reconcile read-only'
clear = json.loads((R / 'FINAL_CLEARANCE.json').read_text())
assert clear['release_cleared'] and clear['fresh_manuscript_reviews'] >= 2
assert clear['final_frozen_clean_reviews'] >= 1 and not clear['unresolved_mandatory_findings']
assert not clear['unresolved_optional_findings']
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


pr = api('GET', 'pulls/211')
assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == OLD
intake = json.loads((D / 'INTAKE.json').read_text())
oq = api('GET', 'contents/unsolved_math_prioritization/QUEUE.md?ref=' + OLD)
assert oq['sha'] == intake['Queue_blob']
original_queue = base64.b64decode(oq['content']).decode()
original_row = [x for x in original_queue.splitlines() if '5100063 / AMR-050-0063' in x]
assert len(original_row) == 1 and original_row[0].split('|')[8].strip() == 'claimed_solved'
main = api('GET', 'git/ref/heads/main')['object']['sha']
main_commit = api('GET', 'git/commits/' + main)
probe_tree = main_commit['tree']['sha']
for component in ['unsolved_math_prioritization', 'attempts', '5100063']:
    listing = api('GET', 'git/trees/' + probe_tree)
    assert not listing['truncated']
    matches = [x for x in listing['tree'] if x['path'] == component]
    if not matches:
        break
    assert len(matches) == 1 and matches[0]['type'] == 'tree'
    assert component != '5100063', 'Fresh main acquired this scientific subtree; independently reconcile before integration'
    probe_tree = matches[0]['sha']
mq = api('GET', 'contents/unsolved_math_prioritization/QUEUE.md?ref=' + main)
main_queue = base64.b64decode(mq['content']).decode()
rows = [x for x in main_queue.splitlines() if '5100063 / AMR-050-0063' in x]
assert len(rows) == 1
fields = rows[0].split('|')
assert len(fields) == 14
assert original_row[0].split('|')[9].strip() == '1/5'
fields[7] = ' 2020 '
fields[8] = ' claimed_solved '
fields[9] = ' 1/5 '
fields[11] = ' [Audited odd outer focal-inverse area product; credited preprint](attempts/5100063/FINAL_DISPOSITION.md) '
fields[12] = ' ' + z['doi_url'] + ' '
queue_row = '|'.join(fields)
assert main_queue.count(rows[0]) == 1
new_queue = main_queue.replace(rows[0], queue_row)
U = R / 'pr_update/5100063'
F = PUB / 'native_current_source'
assert not F.exists(), 'Prepared source already exists; reconcile before another attempt'
prefix = 'k904a_outer_focal_inverse_product/pr_update/5100063/'
with zipfile.ZipFile(R / 'k904a-source-verification.zip') as archive:
    names={p.relative_to(U).as_posix() for p in U.rglob('*') if p.is_file()}
    assert names=={x.removeprefix(prefix) for x in archive.namelist() if x.startswith(prefix)}
    for name in names:assert (U/name).read_bytes()==archive.read(prefix+name)
shutil.copytree(U,F)
assert (F/'PROOF.md').read_bytes()==(U/'PROOF.md').read_bytes()
meta=json.loads((F/'metadata.json').read_text())
meta.update(record_role='Current native accepted published outcome; exact historical inputs and dated prepublication snapshots retained',
    status='claimed_solved_audited_published',preprint_upload_cleared=True,
    whole_package_reviews_completed=clear['fresh_manuscript_reviews'],published_DOI=z['doi'],
    published_url=z['doi_url'],completed_author_turns=1,current_release_status='PUBLICATION_STATUS.md')
(F/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
record=json.loads((F/'source_record.json').read_text())
assert record['status']=='claimed_solved' and record['proposed_year']==2020
record['current_assessment'].update(published_DOI=z['doi'],publication_record=z['record_url'],
    version_bound_final_review_clearance='FINAL_ACCEPTANCE.json')
(F/'source_record.json').write_text(json.dumps(record,indent=2)+'\n')
readme=(F/'README.md').read_text()
readme+='\nVerified preprint and source/verification archive: '+z['doi_url']+'. The required sequential whole-manuscript/package reviews and global repairs are complete. Exact Google Workspace all-four-cell readback: '+t['updated_range']+'. FINAL_ACCEPTANCE.json and PUBLICATION_RECEIPT.json bind the actual release; native merge events are recorded separately in the case audit and GitHubPR#211.\n'
(F/'README.md').write_text(readme)
release=dict(utc=datetime.now(timezone.utc).isoformat(),status='claimed_solved',author_proof_turns='1/5',
    mathematical_verdict='PASS exact pinned original-focus outer signed-area product, strict confocal elliptical caustic, all odd least periods/stars/N3/repetitions',
    priority='No exact prior general proof verified in audited primary corpus; historical novelty undetermined; no first-proof, new general method or current-world-open claim',
    source_year=2020,original_native_head=OLD,original19files_archived_byte_identical=True,
    manuscript_reviews=clear,publication=z,tracker=t,unrefereed=True,extensive_AI_assistance=True,
    independent_human_peer_review=False,native_merge_at_receipt_creation='not yet asserted; see case PR_MERGED receipt and GitHub event')
(F/'FINAL_ACCEPTANCE.json').write_text(json.dumps(release,indent=2)+'\n')
(F/'PUBLICATION_RECEIPT.json').write_text(json.dumps(dict(publication=z,tracker=t),indent=2)+'\n')
status='# Accepted odd outer focal-inverse area product — claimed_solved\n\nThe exact original-focus OUTER straight-edge signed-area product is proved for every odd least-period billiard family with a strict nondegenerate confocal elliptical caustic, including all coprime stars and N3. Fixed repetitions multiply the product by r^2. Original vertices and outer-locus own foci are different targets. The mathematical sections and19 original archived inputs remain unchanged after the version-bound manuscript reviews.\n\nThree independent mathematical/source families, isolated reproductions, two independent bounded priority families, and the required fresh sequential whole-manuscript/package reviews and global repairs have completed. The pinned conjecture is2020 v10 k808,a /v11 k904,a. Classical Stachel/Jacobi, AST, KLS and Chavez-Caliz methods and related original-vertex results are credited. The general k806,a bridge is not assumed. Historical novelty remains undetermined; no first-proof/current-worldwide-open/new-general-method claim. Subscription-limited and selected-passage source limits remain explicit.\n\nExtensive AI tools were used; this is an unrefereed preprint, without independent human peer review or formal proof-assistant verification. FINAL_ACCEPTANCE.json binds the review clearances and exact submitted files. Dated preparation records remain immutable provenance, while this file states the actual published result. Native merge events are recorded separately by the GitHub PR and case PR_MERGED receipt; no merge event is invented here.\n\n'
status+='Preprint and source/verification archive: '+z['doi_url']+'. Exact metadata and both files verified; single GWS append and every cell read back at '+t['updated_range']+'.\n'
(F/'PUBLICATION_STATUS.md').write_text(status)
(F/'FINAL_DISPOSITION.md').write_text(status)
with (F/'RESEARCH_LOG.md').open('a') as log:
    log.write('\n'+datetime.now(timezone.utc).isoformat()+' — case95%: fresh sequential manuscript reviews/global repairs completed, exact preprint published at '+z['doi_url']+', GWS all4cells verified '+t['updated_range']+'. Native scientific readback/merge event remains to be recorded separately. Author1/5 and19 originals retained.\n')
# Rebind current administrative payload; preserve the reviewed mathematical bytes.
assert (F/'PROOF.md').read_bytes()==(U/'PROOF.md').read_bytes()
for p in (U/'history/original_submission_20261015').rglob('*'):
    if p.is_file():assert p.read_bytes()==(F/p.relative_to(U)).read_bytes()
subset=[]
for p in sorted(F.iterdir()):
    if p.is_file() and p.name not in {'MANIFEST.json','PUBLICATION_MANIFEST.json','CURRENT_PACKET_MANIFEST.json'}:
        raw=p.read_bytes();subset.append(dict(path=p.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
for name in ['MANIFEST.json','PUBLICATION_MANIFEST.json']:
    (F/name).write_text(json.dumps(dict(scope='Current accepted published administrative presentation; historical originals archived byte-exact',files=subset),indent=2)+'\n')
current=[]
for p in sorted(F.rglob('*')):
    if p.is_file() and p.name!='CURRENT_PACKET_MANIFEST.json':
        raw=p.read_bytes();current.append(dict(path=p.relative_to(F).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
(F/'CURRENT_PACKET_MANIFEST.json').write_text(json.dumps(dict(schema='pr211-reconciled-packet-v1',self_excluded=True,source_head=OLD,files=current,release_delta='Administrative actual review/DOI/tracker facts only; reviewed proof and19 historical originals unchanged'),indent=2)+'\n')
files={PREFIX+p.relative_to(F).as_posix():p.read_bytes() for p in F.rglob('*') if p.is_file()}
paths=[p for p in R.iterdir() if p.is_file() and p.suffix not in {'.log','.aux','.out'}]
for folder in ['verification','pr_update','history','manuscript_reviews']:
    paths += [p for p in (R/folder).rglob('*') if p.is_file()]
paths += [p for p in D.iterdir() if p.is_file()]
for folder in ['submitted','root_reproduction']:
    paths += [p for p in (D/folder).rglob('*') if p.is_file() and not any(x.startswith('private') or x=='__pycache__' for x in p.parts)]
for family in ['source_scope_adversary_01','geometry_algebra_adversary_01','meromorphic_divisor_adversary_01','priority_author_updates_01','priority_classical_general_01','whole_manuscript_adversary_01','whole_manuscript_adversary_02']:
    folder=D/family
    candidates=[p for p in [folder/'AUTHORED_MANIFEST.json',folder/'MANIFEST.json',folder/'SAFE_AUTHORED_MANIFEST.json'] if p.exists()]
    assert len(candidates)==1;seal=candidates[0];paths.append(seal);m=json.loads(seal.read_text())
    for row in m.get('files',m.get('entries')):
        if 'relative_path' in row:p=folder/row['relative_path']
        else:
            p=folder/row['path']
            if not p.exists():p=D/row['path']
        assert p.resolve().is_relative_to(folder.resolve()) and not p.is_symlink()
        raw=p.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];paths.append(p)
paths += [p for p in PUB.iterdir() if p.is_file()]
for p in sorted(set(paths)):
    assert not p.is_symlink() and p.resolve().is_relative_to(R.parent.resolve())
    assert not any(x.startswith('private') or x=='__pycache__' for x in p.relative_to(R.parent).parts)
    files[p.relative_to(ROOT).as_posix()]=p.read_bytes()
files['unsolved_math_prioritization/QUEUE.md']=new_queue.encode()
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
head = api('POST', 'git/commits', {'message': 'Integrate PR211 reviewed odd outer focal-inverse area-product preprint and verified DOI/tracker; preserve19 original artifacts',
                                'tree': tree, 'parents': [OLD, main]})['sha']
assert api('GET', 'pulls/211')['head']['sha'] == OLD
api('PATCH', 'git/refs/heads/' + pr['head']['ref'], {'sha': head, 'force': False})
# Save a durable ref receipt before a potentially stale PR API read.
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'prepared_head': head, 'original_head': OLD,
           'main_parent': main, 'parents': [OLD, main], 'tree': tree, 'target_queue_row': queue_row,
           'included_owned_pins': pins, 'doi_url': z['doi_url'], 'tracker_range': t['updated_range'],
           'native_merge': 'pending full exact readback', 'local_Git_index_ref_mutations': 0,
           'foreign_main_tree_preserved': True}
(PUB / 'PR_PREPARED.json').write_text(json.dumps(receipt, indent=2) + '\n')
body = ('Proves the pinned2020 k904,a (v10 k808,a) signed area-product assertion for original-focus unit inversion of OUTER tangent-intersection vertices, for every odd least-period confocal elliptical-caustic billiard family, all coprime stars/N3 and fixed repetitions. Author turn1/5 retained; all19 original artifacts preserved byte-for-byte.\n\n'
        'Explicit inverse-edge factorization and target-specific principal-part cancellation, followed by classical complementary torus zero/pole argument. Stachel coordinates, Jacobi/KLS methods, AST complex billiards and Chavez-Caliz prior area-divisor work credited, with related original-vertex results distinguished. Historical novelty undetermined, no first-proof/current-worldwide-open/new-general-method claim; explicit source-access limits retained.\n\n'
        'Mathematical/source reproduction, extensive bounded priority audit, required new sequential whole-package adversaries and global repairs completed. Exact controls and uncertified numerical diagnostics accompany the proof. Extensive AI use; unrefereed, no independent human peer review or proof-assistant formalization.\n\nPreprint and verification: '+z['doi_url']+'. Google Workspace tracker all4cells verified at '+t['updated_range']+'.')
api('PATCH','pulls/211',dict(title='5100063: audited odd outer focal-inverse area product and published preprint',body=body))
assert api('GET','git/ref/heads/'+pr['head']['ref'])['object']['sha']==head
print(json.dumps({k:v for k,v in receipt.items() if k!='included_owned_pins'},indent=2))
