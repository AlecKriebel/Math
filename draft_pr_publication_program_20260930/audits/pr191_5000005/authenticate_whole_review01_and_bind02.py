"""Authenticate completed independent review01 and bind unchanged input for NEW review02."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent;F=A/'whole_package_review_01'
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,obj):
 require(not p.exists(),'Receipt already exists '+p.name);p.write_text(json.dumps(obj,indent=2)+'\n');p.chmod(0o444)
seal=json.loads((F/'FINAL_SEAL.json').read_text());manifest=json.loads((F/'FINAL_FILE_MANIFEST.json').read_text());allow=json.loads((F/'PUBLIC_SAFE_ALLOWLIST.json').read_text());verdict=json.loads((F/'FINAL_VERDICT.json').read_text())
for name,key in [('FINAL_REPORT.md','final_report_sha256'),('FINAL_VERDICT.json','final_verdict_sha256'),('FINAL_FILE_MANIFEST.json','final_manifest_sha256'),('PUBLIC_SAFE_ALLOWLIST.json','final_allowlist_sha256')]:require(pin(F/name)['sha256']==seal[key],'Terminal seal drift '+name)
require(seal['status']=='FINAL_AUTHORITATIVE_PASS_SEALED' and verdict['authoritative_final_verdict'] and verdict['status']=='PASS_FOR_EXACT_CREDITED_REDERIVATION_PACKAGE_V1' and verdict['blocking_issues']==verdict['mandatory_repairs']==[],'Review not authoritative clean final')
expected={x['path'] for x in manifest['files']}
require(len(expected)==len(manifest['files'])==seal['manifest_file_count'],'Review manifest duplicates/count drift')
for x in manifest['files']:
 p=F/x['path'];require(not p.is_symlink() and pin(p)=={'bytes':x['bytes'],'sha256':x['sha256']} and p.stat().st_mode&0o777==0o444,'Final owned review file identity/protection drift '+x['path'])
actual={str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}
require(actual==expected|{'FINAL_FILE_MANIFEST.json','FINAL_SEAL.json'},'Unexpected terminal review files')
for n in allow['allowlist']:require(n in actual and not any(t in Path(n).parts for t in ['private_source_derivatives','extracted','compile','tmp']),'Unsafe review publication member')
inp=json.loads((A/'ROOT_WHOLE_REVIEW_INPUT_01.json').read_text())
for n,x in inp['package_files'].items():require(pin(A/'publication_package_v1'/n)==x,'Frozen publication payload drift')
require(pin(A/'CURRENT_PROOF_V4.md')=={k:inp['current_proof'][k] for k in ['bytes','sha256']},'Proof drift')
auth={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'ROOT_AUTHENTICATED_AUTHORITATIVE_WHOLE_REVIEW01_PASS_EXACT_V1','reviewer':'whole_package_review_01','report':pin(F/'FINAL_REPORT.md'),'final_verdict':pin(F/'FINAL_VERDICT.json'),'final_seal':pin(F/'FINAL_SEAL.json'),'final_manifest':pin(F/'FINAL_FILE_MANIFEST.json'),'public_allowlist':pin(F/'PUBLIC_SAFE_ALLOWLIST.json'),'all_manifest_files_actual_identity_and0444_accepted':len(expected),'all_owned_files_actual0444':all((F/n).stat().st_mode&0o777==0o444 for n in actual),'Root_read_complete_final_report':True,'substantive_blockers':[],'mandatory_repairs':[],'review01_disposition':'PASS','successive_NEW_review02_required':True,'publication_ready':False,'actual_publication_performed':False}
save(A/'ROOT_WHOLE_REVIEW01_FINAL_AUTHENTICATION.json',auth)
inp.update(UTC=datetime.datetime.now(datetime.UTC).isoformat(),status='SECOND_NEW_INDEPENDENT_WHOLE_REVIEW_INPUT_UNCHANGED_CREDITED_V1',review_round=2,previous_exact_input={'path':'ROOT_WHOLE_REVIEW_INPUT_01.json',**pin(A/'ROOT_WHOLE_REVIEW_INPUT_01.json')},previous_authoritative_review={'reviewer':'whole_package_review_01','disposition':'PASS','required_repairs':[],'Root_authentication':'ROOT_WHOLE_REVIEW01_FINAL_AUTHENTICATION.json','report':pin(F/'FINAL_REPORT.md'),'seal':pin(F/'FINAL_SEAL.json')},no_package_or_scientific_native_change_since_review01=True,new_fresh_whole_package_reviews_required=True,publication_ready=False)
save(A/'ROOT_WHOLE_REVIEW_INPUT_02.json',inp)
print(json.dumps({'status':auth['status'],'owned_files_checked':len(actual),'public_safe_files':len(allow['allowlist']),'second_input':pin(A/'ROOT_WHOLE_REVIEW_INPUT_02.json')}))
