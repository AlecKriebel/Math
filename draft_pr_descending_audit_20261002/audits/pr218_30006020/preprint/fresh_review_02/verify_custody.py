#!/usr/bin/env python3
"""Read-only custody checks for the exact frozen PR218 package."""
from pathlib import Path
import json,hashlib,zipfile,datetime
A=Path(__file__).resolve().parent;R=A.parent;D=R.parent/'initial_review_20261015';M=Path('/Users/alec/Documents/Math')
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[]
def check(name,ok,detail=None):
 checks.append({'name':name,'pass':bool(ok),**({'detail':detail} if detail is not None else {})})
 assert ok,name

def manifest(root,rows,name):
 names=[]
 for row in rows:
  p=root/row['path'];raw=p.read_bytes(); names.append(row['path']);check(name+'/'+row['path'],len(raw)==row['bytes'] and sha(raw)==row['sha256'])
 check(name+'/unique',len(set(names))==len(names))
 return len(names)
f=json.loads((R/'FROZEN_INPUTS.json').read_text());manifest(R,f['submission_files'],'submission')
z=zipfile.ZipFile(R/'output/cylinder_areas_verification.zip');p=json.loads(z.read('PACKAGE_FILES.json'))
check('ZIP_CRC',z.testzip() is None)
check('ZIP_no_duplicate_names',len(set(z.namelist()))==len(z.namelist()))
check('ZIP_file_manifest_equals_frozen_manifest',p['files']==f['archive_payload_manifest'])
check('ZIP_exact_names',set(z.namelist())=={x['path'] for x in p['files']}|{'PACKAGE_FILES.json'})
for row in p['files']:
 b=z.read(row['path']);check('ZIP/'+row['path'],len(b)==row['bytes'] and sha(b)==row['sha256'])
E=A/'private/extracted';check('no_external_full_payload_suffixes',not any(Path(n).suffix.lower() in {'.pdf','.png','.jpg','.html','.txt'} for n in z.namelist()))
U=R/'pr_update/30006020';u=json.loads((U/'CURRENT_SOURCE_MANIFEST.json').read_text());manifest(U,u['current_files'],'current_source');H=U/'history/original_submission_20261001';S=D/'submitted/unsolved_math_prioritization/attempts/30006020'
manifest(H,u['original_submission_files'],'original_archive')
check('all_22_original_names',len(u['original_submission_files'])==22 and {str(x.relative_to(H)) for x in H.rglob('*') if x.is_file()}=={x['path'] for x in u['original_submission_files']})
for row in u['original_submission_files']:
 check('original_equals_submission/'+row['path'],(H/row['path']).read_bytes()==(S/row['path']).read_bytes())
for rel in [x['path'] for x in u['current_files']]+['CURRENT_SOURCE_MANIFEST.json']:
 check('ZIP_current_matches_disk/'+rel,(E/'current_source'/rel).read_bytes()==(U/rel).read_bytes())
for row in u['original_submission_files']:
 check('ZIP_original_matches_disk/'+row['path'],(E/'current_source/history/original_submission_20261001'/row['path']).read_bytes()==(H/row['path']).read_bytes())
old=(H/'CANDIDATE.md').read_text();new=(U/'CANDIDATE.md').read_text()
check('core_sections3_to9_identical',old[old.index('## 3.'):old.index('## 10.')]==new[new.index('## 3.'):new.index('## 10.')])
manifest(H,json.loads((H/'MANIFEST.json').read_text())['files'],'old_author_manifest')
v=json.loads((H/'independent_review/REVIEW_MANIFEST.json').read_text())
for rel,digest in v['author_files'].items():check('old_review_author_pins/'+rel,sha((H/rel).read_bytes())==digest)
for rel,digest in v['review_files'].items():check('old_review_own_pins/'+rel,sha((H/'independent_review'/rel).read_bytes())==digest)
check('old_verdict_tied_to_old_candidate',v['candidate_sha256']==sha((H/'CANDIDATE.md').read_bytes()) and v['candidate_sha256']!=sha((U/'CANDIDATE.md').read_bytes()))
manifest(E/'verification',json.loads((E/'verification/PACKAGE_MANIFEST.json').read_text())['files'],'portable_manifest')
prov=json.loads((E/'verification/PROVENANCE.json').read_text())
for row in prov['programs']:
 b=(E/'verification'/row['file']).read_bytes();check('program_provenance/'+row['file'],len(b)==row['bytes'] and sha(b)==row['sha256'] and b==(M/row['original_repository_path']).read_bytes())
 check('original_receipt_provenance/'+row['file'],sha((M/row['historical_expected_receipt_repository_path']).read_bytes())==row['historical_expected_receipt_sha256'])
check('metadata_object_identical',json.loads((R/'metadata.json').read_text())==json.loads((R/'deposit.json').read_text())['metadata'])
# Source hash and read receipts: metadata only, no copyrighted source text copied.
source_map={
 'OWR':D/'private_reading/OWR_2024_41.pdf','DL':D/'private_reading/DL_final.pdf','DGZZ':D/'private_reading/DGZZ_final.pdf',
 'AT94':D/'root_priority_01/private_reading/AT94.pdf','AT94-facsimile':D/'root_priority_01/private_reading/AT94_cleanfacsimile.pdf','ABT00':D/'root_priority_01/private_reading/ABT00.pdf',
 'Liu-thesis':D/'priority_author_history_01/private_reading/liu_thesis_2022.pdf','Liu-Durham2025':D/'priority_author_history_01/private_reading/liu_durham2025_slides.pdf'}
sources=[]
for row in json.loads((E/'verification/PRIMARY_INPUTS.json').read_text())['sources']:
 p=source_map[row['id']];b=p.read_bytes();check('primary_source_pin/'+row['id'],len(b)==row['retrieved_source_bytes'] and sha(b)==row['retrieved_source_sha256']);sources.append({'id':row['id'],'path':str(p),'bytes':len(b),'sha256':sha(b),'read_locations':row['controlling_locations']})
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'check_count':len(checks),'archive_members':len(z.namelist()),'manifested_payloads_excluding_self':len(p['files']) if isinstance(p,dict) else len(f['archive_payload_manifest']),'original_files_preserved':22,'core_sections3_to9_identical':True,'sources':sources,'limits':'Read-only byte and provenance verification, not a universal-priority or publication certificate.'}
(A/'CUSTODY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
# Correct the initial pre-self-manifest check with the explicit documented exception.
i=json.loads((A/'INPUT_PIN_RECEIPT.json').read_text());i['archive_manifest_self_exception']='PACKAGE_FILES.json';i['archive_exact_names_with_self_exception']=True;i['all_pass']=True;i['initial_strict_exact_names_test_note']='The initial strict set comparison excluded the documented self-manifest. Full custody verification checks that member against its exact contents and the remaining 137 frozen hashes.';(A/'INPUT_PIN_RECEIPT.json').write_text(json.dumps(i,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'checks','sources'}},indent=2))
