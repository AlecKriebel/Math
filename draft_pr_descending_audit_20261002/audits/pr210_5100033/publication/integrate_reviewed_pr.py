"""Guarded native PR integration after final review, DOI and tracker readbacks.

No local Git/index/ref writes. Never repeat an uncertain native ref mutation.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Release helpers refuse optimized Python before any action')
from release_binding import context,binding,unchanged,publication,tracker,acquire,exclusive_json,pr_identity,require,digest,durable_mkdir
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
OLD = '2180d64b648b81ac660a792f7823d0b715f9cf12'
PREFIX = 'unsolved_math_prioritization/attempts/5100033/'
assert not (PUB / 'PR_PREPARED.json').exists(), 'Already integrated: reconcile read-only'
assert not (PUB / 'NATIVE_PREPARE_ATTEMPT.json').exists(), 'Prior ref attempt: reconcile read-only'
_RELEASE_LOCK=acquire(PUB)
CTX=context(R)
clear=CTX['clear']
assert clear['release_cleared'] and clear['fresh_manuscript_reviews'] >= 2
assert clear['final_frozen_clean_reviews'] >= 1 and not clear['unresolved_mandatory_findings']
assert not clear['unresolved_optional_findings']
for row in clear['submission_files']:
    raw = (R / row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
z=publication(R,PUB,CTX)
t=tracker(R,PUB,CTX,z)
assert z['submitted'] and z['metadata_and_files_verified']
assert t['verified'] and t['doi_url'] == z['doi_url']
T = PUB / 'private_transport' / datetime.now(timezone.utc).strftime('native_prepare_%Y%m%dT%H%M%S%fZ')
durable_mkdir(T,exist_ok=False)
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


pr = api('GET', 'pulls/210')
pr_identity(pr,OLD,True)
intake = json.loads((D / 'INTAKE.json').read_text())
oq = api('GET', 'contents/unsolved_math_prioritization/QUEUE.md?ref=' + OLD)
assert oq['sha'] == intake['Queue_blob']
original_queue = base64.b64decode(oq['content']).decode()
original_row = [x for x in original_queue.splitlines() if '5100033 / AMR-050-0033' in x]
assert len(original_row) == 1 and original_row[0].split('|')[8].strip() == 'claimed_solved'
main = api('GET', 'git/ref/heads/main')['object']['sha']
main_commit = api('GET', 'git/commits/' + main)
probe_tree = main_commit['tree']['sha']
for component in ['unsolved_math_prioritization', 'attempts', '5100033']:
    listing = api('GET', 'git/trees/' + probe_tree)
    assert not listing['truncated']
    matches = [x for x in listing['tree'] if x['path'] == component]
    if not matches:
        break
    assert len(matches) == 1 and matches[0]['type'] == 'tree'
    assert component != '5100033', 'Fresh main acquired this scientific subtree; independently reconcile before integration'
    probe_tree = matches[0]['sha']
mq = api('GET', 'contents/unsolved_math_prioritization/QUEUE.md?ref=' + main)
main_queue = base64.b64decode(mq['content']).decode()
rows = [x for x in main_queue.splitlines() if '5100033 / AMR-050-0033' in x]
assert len(rows) == 1
fields = rows[0].split('|')
assert len(fields) == 14
# Eligibility is determined at the exact frozen PR head above. MAIN can still
# contain this problem's untouched queued placeholder until this PR is merged.
# Permit only that exact placeholder or the previously supported claimed state.
placeholder=original_row[0].split('|')
placeholder[8]=' queued ';placeholder[9]=' 0/5 '
for index in [10,11,12]:placeholder[index]='  '
require(fields[8].strip()=='claimed_solved' or rows[0]=='|'.join(placeholder),
        'Fresh MAIN row is neither claimed_solved nor the exact untouched queued placeholder; reconcile before integration')
assert original_row[0].split('|')[9].strip() == '1/5'
fields[7] = ' 2020 '
fields[8] = ' claimed_solved '
fields[9] = ' 1/5 '
fields[11] = ' [Audited odd outer focal-pedal area product; credited preprint](attempts/5100033/FINAL_DISPOSITION.md) '
fields[12] = ' ' + z['doi_url'] + ' '
queue_row = '|'.join(fields)
assert main_queue.count(rows[0]) == 1
new_queue = main_queue.replace(rows[0], queue_row)
U = R / 'pr_update/5100033'
F = PUB / 'native_current_source'
assert not F.exists(), 'Prepared source already exists; reconcile before another attempt'
prefix = 'k605a_outer_focal_pedal_product/pr_update/5100033/'
with zipfile.ZipFile(R / 'k605a-source-verification.zip') as archive:
    names={p.relative_to(U).as_posix() for p in U.rglob('*') if p.is_file()}
    assert names=={x.removeprefix(prefix) for x in archive.namelist() if x.startswith(prefix)}
    for name in names:assert (U/name).read_bytes()==archive.read(prefix+name)
shutil.copytree(U,F)
assert (F/'PROOF.md').read_bytes()==(U/'PROOF.md').read_bytes()
readiness=json.loads((F/'readiness.json').read_text())
readiness.update(gate_status='claimed_solved_audited_published',preprint_upload_cleared=True,
    whole_package_reviews_completed=clear['fresh_manuscript_reviews'],published_DOI=z['doi'],
    publication_record=z['record_url'],version_bound_final_review_clearance='FINAL_ACCEPTANCE.json',
    current_release_receipt='RELEASE_RECEIPT.json')
(F/'readiness.json').write_text(json.dumps(readiness,indent=2)+'\n')
ledger=json.loads((F/'turn_ledger.json').read_text())
assert ledger['author_turns_completed']==1 and ledger['max_author_turns_if_unresolved']==5
ledger.update(status='claimed_solved_audited_published',current_release_record='RELEASE_RECEIPT.json')
(F/'turn_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
(F/'PUBLICATION_METADATA.json').write_text(json.dumps(z['metadata'],indent=2)+'\n')
readme=(F/'README.md').read_text()
readme+='\nVerified preprint and source/verification archive: '+z['doi_url']+'. The required sequential whole-manuscript/package reviews and global repairs are complete. Exact Google Workspace all-four-cell readback: '+t['updated_range']+'. FINAL_ACCEPTANCE.json and PUBLICATION_RECEIPT.json bind the actual release; native merge events are recorded separately in the case audit and GitHubPR#210.\n'
(F/'README.md').write_text(readme)
release=dict(utc=datetime.now(timezone.utc).isoformat(),status='claimed_solved',author_proof_turns='1/5',
    mathematical_verdict='PASS exact pinned original-focus outer focal-pedal signed-area product, strict confocal elliptical caustic, all odd least periods/stars/N3/repetitions',
    priority='No exact prior general proof verified in audited primary corpus; historical novelty undetermined; no first-proof, new general method or current-world-open claim',
    source_year=2020,original_native_head=OLD,original20files_archived_byte_identical=True,
    manuscript_reviews=clear,publication=z,tracker=t,unrefereed=True,extensive_AI_assistance=True,
    independent_human_peer_review=False,native_merge_at_receipt_creation='not yet asserted; see case PR_MERGED receipt and GitHub event')
(F/'FINAL_ACCEPTANCE.json').write_text(json.dumps(release,indent=2)+'\n')
(F/'PUBLICATION_RECEIPT.json').write_text(json.dumps(dict(publication=z,tracker=t),indent=2)+'\n')
(F/'RELEASE_RECEIPT.json').write_text(json.dumps(release,indent=2)+'\n')
status='# Accepted odd outer focal-pedal area product — claimed_solved\n\nThe original-focus signed outer-tangent pedal-area product is proved for every odd least-period billiard family with a strictly nested nondegenerate confocal elliptical caustic, including coprime stars and N3. Fixed repeated traversals multiply the product by s^2; the circular case is a direct extension. The two genuine N4 phases give products16 and25, excluding the primitive-even extension. The reviewed proof and all20 original archived inputs are unchanged.\n\nThe historical source labels are2020 arXiv v1 k604, v11 k605,a and published k606. Three independent mathematical/source families, exact and high-precision controls, two bounded priority families and the required fresh sequential whole-package adversaries/global repairs are complete. Stachel/Jacobi/auxiliary-circle, classical cyclic elliptic/area methods, Khare–Sukhatme2004 and current Ferudun inverse-area/outer-pedal antecedents receive substantive credit. Both exact comparison bridges are documented. Historical novelty and public proof priority remain undetermined; no first-proof/new-general-method/current-worldwide-open claim. Source-access limits and the local0062p6 fixture correction remain explicit.\n\nExtensive AI assistance was used. This is an unrefereed preprint without independent human peer review or formal proof-assistant verification. FINAL_ACCEPTANCE.json and RELEASE_RECEIPT.json bind the actual reviewed submission and DOI/tracker facts; PUBLICATION_METADATA.json preserves the exact deposit metadata. Dated prepublication statuses are immutable provenance. Native merge events are recorded separately by GitHub and the case PR_MERGED receipt, without forecasting a merge here.\n\n'
status+='Verified preprint and source/verification archive: '+z['doi_url']+'. Exact metadata/both public files verified; single GWS append/all4cells read back at '+t['updated_range']+'.\n'
(F/'PUBLICATION_STATUS.md').write_text(status)
(F/'FINAL_DISPOSITION.md').write_text(status)
with (F/'RESEARCH_LOG.md').open('a') as log:
    log.write('\n'+datetime.now(timezone.utc).isoformat()+' — case95%: fresh sequential manuscript reviews/global repairs completed, exact preprint published at '+z['doi_url']+', GWS all4cells verified '+t['updated_range']+'. Native scientific readback/merge event remains to be recorded separately. Author1/5 and20 originals retained.\n')
# Rebind current administrative payload; preserve the reviewed mathematical bytes.
allowed_admin={'readiness.json','turn_ledger.json','README.md','RESEARCH_LOG.md','PUBLICATION_STATUS.md','FINAL_DISPOSITION.md','FINAL_ACCEPTANCE.json','PUBLICATION_RECEIPT.json','RELEASE_RECEIPT.json','PUBLICATION_METADATA.json','MANIFEST.json','PUBLICATION_MANIFEST.json','CURRENT_PACKET_MANIFEST.json'}
for path in U.rglob('*'):
    if path.is_file() and path.relative_to(U).as_posix() not in allowed_admin:
        assert path.read_bytes()==(F/path.relative_to(U)).read_bytes()

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
(F/'CURRENT_PACKET_MANIFEST.json').write_text(json.dumps(dict(schema='pr210-reconciled-packet-v1',self_excluded=True,source_head=OLD,files=current,release_delta='Administrative actual review/DOI/tracker facts only; reviewed proof and20 historical originals unchanged'),indent=2)+'\n')
files={PREFIX+p.relative_to(F).as_posix():p.read_bytes() for p in F.rglob('*') if p.is_file()}
paths=[p for p in R.iterdir() if p.is_file() and p.suffix not in {'.log','.aux','.out'}]
for folder in ['verification','pr_update','history','manuscript_reviews']:
    paths += [p for p in (R/folder).rglob('*') if p.is_file()]
paths += [p for p in D.iterdir() if p.is_file()]
for folder in ['submitted','root_reproduction']:
    paths += [p for p in (D/folder).rglob('*') if p.is_file() and not any(x.startswith('private') or x=='__pycache__' for x in p.parts)]
for family in ['source_domain_adversary_01','physical_geometry_adversary_01','meromorphic_divisor_adversary_01','priority_author_updates_01','priority_classical_general_01','whole_manuscript_adversary_01','whole_manuscript_adversary_02','whole_manuscript_adversary_03','release_helpers_adversary_01','release_helpers_adversary_02','release_helpers_adversary_03','release_helpers_adversary_04','release_helpers_adversary_05']:
    folder=D/family
    candidates=[p for p in [folder/'AUTHORED_MANIFEST.json',folder/'MANIFEST.json',folder/'SAFE_AUTHORED_MANIFEST.json'] if p.exists()]
    assert len(candidates)==1;seal=candidates[0];paths.append(seal);m=json.loads(seal.read_text())
    for row in m.get('authored_files',m.get('files',m.get('entries'))):
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
head = api('POST', 'git/commits', {'message': 'Integrate PR210 reviewed odd outer focal-pedal area-product preprint and verified DOI/tracker; preserve20 original artifacts',
                                'tree': tree, 'parents': [OLD, main]})['sha']
fresh_pr=api('GET', 'pulls/210')
pr_identity(fresh_pr,OLD,True)
unchanged(R,CTX);publication(R,PUB,CTX);tracker(R,PUB,CTX,z)
actual_commit=api('GET','git/commits/'+head)
assert [x['sha'] for x in actual_commit['parents']]==[OLD,main] and actual_commit['tree']['sha']==tree
exclusive_json(PUB/'NATIVE_PREPARE_ATTEMPT.json',dict(utc=datetime.now(timezone.utc).isoformat(),old=OLD,head=head,main=main,branch='dot/math-5100033',nonforce=True,release_binding=binding(CTX)))
api('PATCH', 'git/refs/heads/' + pr['head']['ref'], {'sha': head, 'force': False})
# Save a durable ref receipt before a potentially stale PR API read.
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'prepared_head': head, 'original_head': OLD,
           'main_parent': main, 'parents': [OLD, main], 'tree': tree, 'target_queue_row': queue_row,
           'included_owned_pins': pins, 'doi_url': z['doi_url'], 'tracker_range': t['updated_range'],
           'native_merge': 'pending full exact readback', 'local_Git_index_ref_mutations': 0,
           'foreign_main_tree_preserved': True,'release_binding':binding(CTX),'publication_receipt_sha256':digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json'),'tracker_receipt_sha256':digest(PUB/'TRACKER_VERIFIED_APPEND.json')}
(PUB / 'PR_PREPARED.json').write_text(json.dumps(receipt, indent=2) + '\n')
body = ('Proves the historical k605,a (published k606; v1 k604) signed product of the two original-focus pedal areas of the OUTER tangent polygon, for every odd least-period strict confocal elliptical-caustic family, all coprime stars/N3 and fixed repetitions. Author turn1/5 and all20 original artifacts retained. Exact N4 counterexamples delimit the primitive-even boundary.\n\n'
        'Explicit focal-foot geometry, adjacent collinear residue cancellation, reflection and classical complementary torus divisor proof. Stachel/Jacobi/auxiliary-circle and cyclic elliptic/area methods, the exact Khare–Sukhatme2004 analytic identity and related Ferudun results receive substantive credit, with complete geometric comparison bridges. Historical novelty/public priority remain undetermined; no first-proof/new-general-method/current-worldwide-open claim. Source-access limits and related-source fixture correction remain explicit.\n\n'
        'Independent mathematical/source reconstruction, full reproduction, extensive bounded priority audit and required NEW sequential whole-package adversaries/global repairs completed. Exact controls and labelled uncertified numerical diagnostics accompany the note. Extensive AI use; unrefereed, no independent human peer review or formal proof-assistant verification.\n\nPreprint and verification: '+z['doi_url']+'. Single GWS append/all4cells verified at '+t['updated_range']+'.')
api('PATCH','pulls/210',dict(title='5100033: audited odd outer focal-pedal area product and published preprint',body=body))
assert api('GET','git/ref/heads/'+pr['head']['ref'])['object']['sha']==head
print(json.dumps({k:v for k,v in receipt.items() if k!='included_owned_pins'},indent=2))
