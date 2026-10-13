from pathlib import Path
import json,hashlib,datetime as dt
W=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr263_30000170/initial_review_20261011')
D=W/'publication_candidate/attempts/30000170';C=W/'scoped_candidate/attempts/30000170';N=W/'integration_preparation'
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify(root,entries):
 assert len({e['path'] for e in entries})==len(entries)
 for e in entries:
  f=root/e['path'];assert f.resolve()==f and f.is_file() and not f.is_symlink()
  a=pin(f);assert(a['bytes'],a['sha256'])==(e['bytes'],e['sha256']),(root,e['path'])
 return len(entries)
H=json.loads((W/'publication_candidate/HANDOFF_MANIFEST.json').read_text());assert verify(W/'publication_candidate',H['files'])==140
assert {e['path'] for e in H['files']}=={str(f.relative_to(W/'publication_candidate')) for f in (W/'publication_candidate').rglob('*') if f.is_file() and f.name!='HANDOFF_MANIFEST.json'}
X=json.loads((D/'CANDIDATE_MANIFEST.json').read_text());assert verify(D,X['payload'])==131
assert {e['path'] for e in X['payload']}|{'CANDIDATE_MANIFEST.json'}=={str(f.relative_to(D)) for f in D.rglob('*') if f.is_file()}
assert hashlib.sha256(json.dumps(X['payload'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==X['payload_sha256']
for f in C.rglob('*'):
 if f.is_file():assert f.read_bytes()==(D/'historical/source_candidate_v03'/f.relative_to(C)).read_bytes()
O=json.loads((W/'original_submission/MANIFEST_WITH_MODES.json').read_text());OS=[e for e in O if e['path'].startswith('attempts/30000170/')];assert len(OS)==17
for e in OS:
 f=Path(e['local']);a=pin(f);assert(a['bytes'],a['sha256'])==(e['bytes'],e['sha256']);assert f.read_bytes()==(D/'historical/original_submission/files'/e['path']).read_bytes()
checks={}
for sub,manifest,key,dest in [('preprint_package_v03','PACKAGE_MANIFEST.json','files','preprint'),('whole_preprint_review_01','REVIEW_MANIFEST.json','files','whole_preprint_reviews/review01'),('whole_preprint_review_02','REVIEW_MANIFEST.json','selected_authored_outputs','whole_preprint_reviews/review02')]:
 r=W/sub;m=json.loads((r/manifest).read_text());checks[sub]=verify(r,m[key]);assert(r/manifest).read_bytes()==(D/dest/manifest).read_bytes()
 for e in m[key]:assert(r/e['path']).read_bytes()==(D/dest/e['path']).read_bytes()
receipts={'ROOT_FINAL_WHOLE_PREPRINT_READINESS_ACCEPTANCE.json':W/'ROOT_FINAL_WHOLE_PREPRINT_READINESS_ACCEPTANCE.json','ROOT_ACTUAL_PUBLICATION_ACCEPTANCE.json':W/'publication_execution_20261011/ROOT_ACTUAL_PUBLICATION_ACCEPTANCE.json','ROOT_REVIEW01_REPAIR_AND_V03_PREPARATION.json':W/'package_preparation/ROOT_REVIEW01_REPAIR_AND_V03_PREPARATION.json','ROOT_ACTUAL_PUBLIC_METADATA_SEMANTIC_READBACK.json':W/'publication_execution_20261011/ROOT_ACTUAL_PUBLIC_METADATA_SEMANTIC_READBACK.json'}
for name,f in receipts.items():assert f.read_bytes()==(D/'publication_provenance'/name).read_bytes()
historical=['REVIEW_REQUEST.md','checks/verify.py','checks/CHECKS.json']+[e['path'][len('attempts/30000170/'):] for e in OS if '/independent_review/' in e['path']];assert len(historical)==9
for rel in historical:assert(D/rel).read_bytes()==(C/rel).read_bytes()
assert(D/'PROOF.md').read_text().split('## 2.',1)[1].split('## 8.',1)[0]==(C/'PROOF.md').read_text().split('## 2.',1)[1].split('## 8.',1)[0]
for f in (C/'checks').rglob('*'):
 if f.is_file():assert f.read_bytes()==(D/f.relative_to(C)).read_bytes()
paths=json.loads((D/'EXACT_PATH_CHANGES.json').read_text());changed=sorted(str(f.relative_to(C)) for f in C.rglob('*') if f.is_file() and f.read_bytes()!=(D/f.relative_to(C)).read_bytes());assert changed==paths['changed_existing_C_paths']==X['changed_existing_C_paths']
assert paths['new_paths_since_C']==sorted({str(f.relative_to(D)) for f in D.rglob('*') if f.is_file()}-{str(f.relative_to(C)) for f in C.rglob('*') if f.is_file()})
for category,root,key in [('original_target_comparisons',W/'original_submission/files/attempts/30000170','original'),('delivered_C_v03_comparisons',C,'delivered_C_v03')]:
 for e in paths[category]:
  p=pin(root/e['path']);q=pin(D/e['path']);assert(p['bytes'],p['sha256'])==(e[key]['bytes'],e[key]['sha256']);assert e['byte_identical']==((root/e['path']).read_bytes()==(D/e['path']).read_bytes())
  if 'current' in e and 'sha256' in e['current']:assert(q['bytes'],q['sha256'])==(e['current']['bytes'],e['current']['sha256'])
target=[{'path':str(f.relative_to(D)),'bytes':pin(f)['bytes'],'sha256':pin(f)['sha256']} for f in sorted(D.rglob('*')) if f.is_file()]
A={'schema':'pr263-root-final-publication-candidate-acceptance-v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'accepted_for_native_preparation':True,'candidate_root':str(D),'candidate_manifest':pin(D/'CANDIDATE_MANIFEST.json'),'target_bodies':target,'whole_read_current_semantics_and_source_manifest_delta':True,'independent_full_body_and_inventory_validation':{'handoff':140,'target_payload':131,'target_including_manifest':132,'original_exact_copies':17,'C_v03_exact_copies':24,'package_and_review_exact_copies':checks,'four_root_receipt_copies_exact':True,'historical9_unchanged':True,'core_PROOF_sections2_to7_unchanged':True,'all_checkers_unchanged':True,'changed_C_paths':changed,'unselected_private_reading_copies_or_credentials':False},'publication_verified_DOI':'10.5281/zenodo.23306332','priority_boundary':'Direct credited historical complex-quadratic theorem; no firstness/current-openness/application-priority clearance. Remaining unread-body gaps remain explicit.','tracker_pending':True,'native_merge_pending':True,'provider_mutations_by_this_acceptance':0,'completion_percent':85}
(N/'ROOT_FINAL_PUBLICATION_CANDIDATE_ACCEPTANCE.json').write_text(json.dumps(A,indent=2)+'\n')
print(json.dumps({'acceptance':pin(N/'ROOT_FINAL_PUBLICATION_CANDIDATE_ACCEPTANCE.json'),'target_count':len(target),'checks':A['independent_full_body_and_inventory_validation']},indent=2))
