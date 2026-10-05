#!/usr/bin/env python3
"""Read complete authorized inputs; emit only hashes, sizes and match results.
No corpus records or source text are copied to the output. Paths are CLI inputs.
"""
import argparse,hashlib,json,zipfile
from pathlib import Path
P=argparse.ArgumentParser()
P.add_argument('--author-zip',required=True)
P.add_argument('--catalog',required=True)
P.add_argument('--problems',required=True)
P.add_argument('--research-results',required=True)
P.add_argument('--dataset-manifest',required=True)
P.add_argument('--source-directory',required=True)
a=P.parse_args()
def metadata(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
za=Path(a.author_zip).read_bytes();zh=metadata(za)
assert zh=={'bytes':18458,'sha256':'9ab3bab00933cd5dbdbc423eafd7f60c114a13bfb7fcdafb8f5569f29c8503aa'}
allow={'APPROACHES.md','MANIFEST.json','PROOF.md','README.md','RESULTS.json','SOURCE_VERIFICATION.json','check.py','verify_manifest.py'}
with zipfile.ZipFile(a.author_zip) as z:
 assert set(z.namelist())==allow and len(z.namelist())==len(allow)
 mb=z.read('MANIFEST.json')
 assert hashlib.sha256(mb).hexdigest()=='a69d19e3fdbf80a824b18b8c2527ce1de4029ebe5639ad020160a9cbb021cc88'
 mf=json.loads(mb)
 assert {i['path'] for i in mf['files']}==allow-{'MANIFEST.json'}
 for row in mf['files']:assert metadata(z.read(row['path']))=={'bytes':row['bytes'],'sha256':row['sha256']}
 authored=json.loads(z.read('SOURCE_VERIFICATION.json'))
 manifest_bytes=Path(a.dataset_manifest).read_bytes()
 manifest_blob=hashlib.sha1(b'blob '+str(len(manifest_bytes)).encode()+b'\0'+manifest_bytes).hexdigest()
 assert manifest_blob=='55589bae6bad2d3e2f696e08645330ff1219b709'
 manifest=json.loads(manifest_bytes)
 assert manifest['revision']=='37e53eabe540fb458758e198be61634bd02ee008'
 result={'author_freeze':zh,'author_manifest':metadata(mb),'exact_member_allowlist':True,'member_hashes_match':True,'dataset_revision':manifest['revision'],'dataset_files':{}}
 result['repository_dataset_manifest']={**metadata(manifest_bytes),'git_blob_sha':manifest_blob,'matches_pinned_repository_blob':True}
 all_data={}
 for filename,arg in [('problems.json',a.problems),('research_results.json',a.research_results)]:
  raw=Path(arg).read_bytes()
  mm=metadata(raw);assert mm==manifest['files'][filename]
  all_data[filename]=json.loads(raw)
  result['dataset_files'][filename]={**mm,'complete_bytes_read':True,'matches_freshly_read_repository_manifest':True}
 raw=Path(a.catalog).read_bytes();catmeta=metadata(raw)
 catmeta['git_blob_sha']=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 assert catmeta==authored['identity']['catalog']
 catalog=json.loads(raw)
 selected=[r for r in all_data['problems.json'] if str(r['id'])=='30005664']
 selectedcat=[r for r in catalog if str(r['id'])=='30005664']
 assert len(selected)==len(selectedcat)==1
 assert selectedcat[0]['rank']==779 and selectedcat[0]['holds']==[]
 statement_hash=hashlib.sha256(selected[0]['statement'].encode()).hexdigest()
 assert statement_hash==selectedcat[0]['statement_hash']==authored['identity']['statement_sha256']
 reports=all_data['research_results.json']
 review_hash=hashlib.sha256(json.dumps([selected[0],reports.get('OWR-14297742-004',{})],sort_keys=True).encode()).hexdigest()
 assert review_hash==selectedcat[0]['review_hash']=='4770883cfbb578cb13938241c495d2f9967f78602a9419ecf905c240f2fbd149'
 result['catalog']=catmeta
 result['identity']={'unique_numeric_id_match':True,'problem_id':30005664,'problem_code':'OWR-14297742-004','statement_sha256':statement_hash,'matches_catalog':True,'problem_records':len(all_data['problems.json']),'prior_report_entries':len(reports),'exact_prior_report_key_present':'OWR-14297742-004' in reports,'absence_scope':'Only the exact problem-code key in the complete pinned dictionary.'}
 result['identity']['review_hash']=review_hash
 result['identity']['review_hash_recomputed_using_repository_rule']=True
 assert result['identity']['exact_prior_report_key_present'] is False
 result['sources']=[]
 for filename,entry in zip(['owr.pdf','keller.pdf','keller_published.pdf','nice2026.pdf','ckn.pdf'],authored['sources']):
  mm=metadata((Path(a.source_directory)/filename).read_bytes());assert mm==entry['pdf']
  result['sources'].append({'title':entry['title'],'url':entry['url'],'pdf':mm,'complete_bytes_rehashed':True,'matches_author_source_fingerprint':True})
 result['status']='PASS'
 result['limitations']='Full cached authorized source/corpus bytes independently read and rehashed. This does not claim fresh redownloads or universal literature/repository absence.'
 print(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False))
