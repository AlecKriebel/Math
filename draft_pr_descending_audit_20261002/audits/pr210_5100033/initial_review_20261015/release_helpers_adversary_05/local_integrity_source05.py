"""Local immutable artifact verification only; no action-helper execution."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json,zipfile
O=Path(__file__).resolve().parent;D=O.parent;C=D.parent;P=C/'publication';R=C/'preprint';H=D/'history/release_helpers_review03_frozen'
load=lambda p:json.loads(p.read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):raw=p.read_bytes();return dict(path=p.name,bytes=len(raw),sha256=sha(raw))
freeze=load(O/'INDEPENDENT_FREEZE.json');sourcechecks=[]
for row in freeze['inputs']:
 p=Path(row['source']);f=O/row['path'];raw=p.read_bytes();assert raw==f.read_bytes() and len(raw)==row['bytes'] and sha(raw)==row['sha256'];compile(raw,str(f),'exec');sourcechecks.append(dict(path=p.name,bytes=len(raw),sha256=sha(raw),frozen_matches_current=True))
candidate=load(O/'frozen_inputs/RENEWED_CLEARANCE_CANDIDATE.json')
assert (O/'frozen_inputs/RENEWED_CLEARANCE_CANDIDATE.json').read_bytes()==(D/'RENEWED_CLEARANCE_CANDIDATE.json').read_bytes()
assert sha((D/'RENEWED_CLEARANCE_CANDIDATE.json').read_bytes())=='c1297bbb2a0e6e364076ff539f58a5337ebc304e4efe77c3fc2dcc0623dc9104'
assert candidate['release_cleared'] is False and candidate['candidate_only'] is True
assert candidate['release_helpers']==[pin(p) for p in sorted(P.glob('*.py'))]
assert candidate['supplemental_readonly_reconciliation']==pin(D/'reconcile_published_release_readonly.py')
archive=load(H/'ARCHIVE_MANIFEST.json');assert len(archive['files'])==14 and len({r['path'] for r in archive['files']})==14
for row in archive['files']:assert pin(H/row['path'])==row
assert pin(H/'ARCHIVE_MANIFEST.json')==candidate['initial_publication_tracker_state']['archive_manifest']
for key,n in [('publication_receipt','ZENODO_VERIFIED_PUBLICATION.json'),('tracker_receipt','TRACKER_VERIFIED_APPEND.json'),('stage_intent','STAGE_ATTEMPT.json'),('publish_intent','PUBLISH_ATTEMPT.json')]:assert pin(H/n)==candidate['initial_publication_tracker_state'][key]
evidence=['ZENODO_VERIFIED_PUBLICATION.json','TRACKER_VERIFIED_APPEND.json','STAGE_ATTEMPT.json','PUBLISH_ATTEMPT.json','ZENODO_STAGED_VERIFIED.json','ZENODO_TOOL_PUBLICATION_RECEIPT.json','ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json']
for n in evidence:assert (P/n).read_bytes()==(H/n).read_bytes()
old=load(H/'FINAL_CLEARANCE.json');assert (R/'FINAL_CLEARANCE.json').read_bytes()==(H/'FINAL_CLEARANCE.json').read_bytes()
assert sha((H/'FINAL_CLEARANCE.json').read_bytes())==candidate['prior_published_clearance_sha256']
sciencekeys=['package_manifest_sha256','deposit_manifest_sha256','publication_metadata_sha256','submission_files','source_manifest','manuscript_source','publication_metadata','original_native_head']
for k in sciencekeys:assert old[k]==candidate[k]
for n,k in [('PACKAGE_MANIFEST.json','package_manifest_sha256'),('deposit.json','deposit_manifest_sha256'),('metadata.json','publication_metadata_sha256')]:assert sha((R/n).read_bytes())==candidate[k]
package=load(R/'PACKAGE_MANIFEST.json');science=[]
for row in package['submission_files']+[package[k] for k in ['source_manifest','manuscript_source','metadata']]:assert pin(R/row['path'])==row;science.append(row)
stale=[r['path'] for r in old['release_helpers'] if pin(P/r['path'])!=r];assert stale==['integrate_reviewed_pr.py']
intake=load(D/'INTAKE.json');checks=[]
with zipfile.ZipFile(R/'k605a-source-verification.zip') as archivezip:
 names=archivezip.namelist();assert len(names)==len(set(names))==181
 assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names)
 U=R/'pr_update/5100033';prefix='k605a_outer_focal_pedal_product/pr_update/5100033/'
 native={p.relative_to(U).as_posix():p.read_bytes() for p in U.rglob('*') if p.is_file()}
 zipped={n.removeprefix(prefix):archivezip.read(n) for n in names if n.startswith(prefix)};assert native==zipped
 for row in intake['original_source_files']:
  rel=row['native_path'].removeprefix('unsolved_math_prioritization/attempts/5100033/')
  for base in [D/'submitted/unsolved_math_prioritization/attempts/5100033',U/'history/original_submission_20261015',R/'verification/original_submission']:
   p=base/rel;raw=p.read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256'];checks.append(str(p.relative_to(C)))
assert len(checks)==60
seals=[]
for family in ['release_helpers_adversary_03','release_helpers_adversary_04']:
 F=D/family;m=load(F/'AUTHORED_MANIFEST.json');rows=m.get('files',m.get('authored_files',m.get('entries')))
 for row in rows:
  p=F/row.get('path',row.get('relative_path'));assert p.resolve().is_relative_to(F.resolve()) and not p.is_symlink();raw=p.read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
 seals.append(dict(family=family,manifest_sha256=sha((F/'AUTHORED_MANIFEST.json').read_bytes()),checked_payloads=len(rows)))
cap=P/'private_transport/native_prepare_20261015T142749854176Z';capturechecks=[];qrows=[]
for name in ['002-stdout.json','008-stdout.json']:
 p=cap/name;value=load(p);raw=base64.b64decode(value['content']);target=[r for r in raw.decode().splitlines() if '5100033 / AMR-050-0033' in r];assert len(target)==1;qrows.append(target[0]);capturechecks.append(dict(path=name,source_sha256=sha(p.read_bytes()),decoded_queue_sha256=sha(raw),decoded_queue_git_blob_sha1=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),provider_reported_blob=value['sha']))
assert capturechecks[0]['decoded_queue_git_blob_sha1']==intake['Queue_blob'] and capturechecks[0]['decoded_queue_sha256']==intake['Queue_sha256']
assert all(r['decoded_queue_git_blob_sha1']==r['provider_reported_blob'] for r in capturechecks)
placeholder=qrows[0].split('|');placeholder[8]=' queued ';placeholder[9]=' 0/5 '
for i in [10,11,12]:placeholder[i]='  '
assert '|'.join(placeholder)==qrows[1] and qrows[0]==intake['queue_row']
assert qrows[0].split('|')[8].strip()=='claimed_solved' and qrows[0].split('|')[9].strip()=='1/5'
assert qrows[1].split('|')[8].strip()=='queued' and qrows[1].split('|')[9].strip()=='0/5'
for n in ['NATIVE_PREPARE_ATTEMPT.json','PR_PREPARED.json','NATIVE_READY_ATTEMPT.json','NATIVE_MERGE_REQUEST.json','PR_MERGED.json','native_current_source','RELEASE_BINDING_RECONCILIATION_ATTEMPT.json','RELEASE_BINDING_RECONCILIATION.json']:assert not (P/n).exists(),n
z=load(H/'ZENODO_VERIFIED_PUBLICATION.json');t=load(H/'TRACKER_VERIFIED_APPEND.json');assert z['id']==23398175 and z['doi']=='10.5281/zenodo.23398175' and t['append_count']==1 and t['updated_range']=="'Math Puzzles'!A113:D113"
value=dict(utc=datetime.now(timezone.utc).isoformat(),source_checks=sourcechecks,candidate_sha256=sha((D/'RENEWED_CLEARANCE_CANDIDATE.json').read_bytes()),candidate_release_cleared=False,initial_archive_payloads_verified=14,current_original_evidence_files_unchanged=7,historical_clearance_unchanged=True,genuine_old_clearance_stale_helper=stale,science_pins= science,unique_safe_zip_entries=len(names),native_source_zip_equalities=len(native),original_twenty_three_copy_checks=60,prior_review_seals=seals,actual_queue_capture_checks=capturechecks,actual_queued_placeholder_equals_two_space_reconstruction=True,native_and_reconciliation_intents_absent=True,actual_record=23398175,actual_tracker_range=t['updated_range'],real_provider_CLI_network_Git_calls=0)
(O/'LOCAL_INTEGRITY_SOURCE05_RESULTS.json').write_text(json.dumps(value,indent=2)+'\n');print(json.dumps(value,indent=2))
