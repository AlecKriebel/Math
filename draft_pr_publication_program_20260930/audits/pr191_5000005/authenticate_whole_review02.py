"""Authenticate the second NEW complete-package review and scientific readiness."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent;F=A/'whole_package_review_02'
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,obj):
 require(not p.exists(),'Receipt exists '+p.name);p.write_text(json.dumps(obj,indent=2)+'\n');p.chmod(0o444)
seal=json.loads((F/'FINAL_SEAL_02.json').read_text());manifest=json.loads((F/'FINAL_MANIFEST_02.json').read_text());allow=json.loads((F/'PUBLIC_ALLOWLIST_02.json').read_text())
for n,k in [('REVIEW_02.md','report_sha256'),('FINAL_MANIFEST_02.json','manifest_sha256'),('PUBLIC_ALLOWLIST_02.json','public_allowlist_sha256'),('FINAL_INPUT_READBACK_02.json','input_readback_sha256'),('SOURCE_FIRST_SEAL_02.json','source_first_seal_sha256')]:require(pin(F/n)['sha256']==seal[k],'Terminal second-review seal drift '+n)
require(seal['verdict']=='PASS_EXACT_FROZEN_CREDITED_VERIFICATION_REDERIVATION_PACKAGE' and seal['required_repairs']==[],'Second reviewer not final clean')
expected=set()
for x in manifest['files']:
 n=x['path'];require(n not in expected,'Duplicate second-review file');expected.add(n);p=F/n;require(not p.is_symlink() and pin(p)=={'bytes':x['bytes'],'sha256':x['sha256']} and p.stat().st_mode&0o777==0o444,'Second review file drift '+n)
actual={str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}
require(actual==expected|{'FINAL_MANIFEST_02.json','FINAL_SEAL_02.json'},'Second review terminal inventory mismatch')
for n in allow['allowlist']:require(n in actual and 'private' not in Path(n).parts and (F/n).stat().st_mode&0o777==0o444,'Unsafe second-review publication member')
readback=json.loads((F/'FINAL_INPUT_READBACK_02.json').read_text());require(readback['status']=='PASS' and readback['all_initial_protected_sizes_and_hashes_unchanged'] and readback['initial_protected_files_checked']==109,'Second input readback failure')
inp=json.loads((A/'ROOT_WHOLE_REVIEW_INPUT_02.json').read_text())
for n,x in inp['package_files'].items():require(pin(A/'publication_package_v1'/n)==x==readback['package_files'][n],'Final packet drift '+n)
require(pin(A/'CURRENT_PROOF_V4.md')=={k:inp['current_proof'][k] for k in ['bytes','sha256']},'Current proof drift')
auth={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'ROOT_AUTHENTICATED_AUTHORITATIVE_NEW_WHOLE_REVIEW02_PASS_EXACT_V1','reviewer':'whole_package_review_02','report':pin(F/'REVIEW_02.md'),'final_seal':pin(F/'FINAL_SEAL_02.json'),'final_manifest':pin(F/'FINAL_MANIFEST_02.json'),'public_allowlist':pin(F/'PUBLIC_ALLOWLIST_02.json'),'all_owned_files_hash_and_actual0444_accepted':len(actual),'Root_read_complete_final_report':True,'required_repairs':[],'disposition':'PASS','actual_publication_performed':False}
save(A/'ROOT_WHOLE_REVIEW02_FINAL_AUTHENTICATION.json',auth)
first=json.loads((A/'ROOT_WHOLE_REVIEW01_FINAL_AUTHENTICATION.json').read_text());require(first['review01_disposition']=='PASS' and first['mandatory_repairs']==[],'First successive review not accepted')
science={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'EXACT_CREDITED_PUBLICATION_PACKAGE_SCIENTIFICALLY_READY_AFTER_TWO_NEW_CLEAN_WHOLE_REVIEWS','PR':191,'original_head':inp['original_head'],'original_QUEUE_status':'claimed_solved','original_effort':'2/5','packet_name':'publication_package_v1','payloads':inp['package_files'],'current_proof':inp['current_proof'],'native_pending_manifest':inp['native_pending_manifest'],'review_input':{'path':'ROOT_WHOLE_REVIEW_INPUT_02.json',**pin(A/'ROOT_WHOLE_REVIEW_INPUT_02.json')},'reviews':[{'reviewer':'whole_package_review_01','disposition':'PASS','Root_authentication':pin(A/'ROOT_WHOLE_REVIEW01_FINAL_AUTHENTICATION.json')},{'reviewer':'whole_package_review_02','disposition':'PASS','Root_authentication':pin(A/'ROOT_WHOLE_REVIEW02_FINAL_AUTHENTICATION.json')}],'all_required_mathematical_and_package_repairs_resolved':True,'required_repairs':[],'exact_scope':'Imported unrestricted bare-A0/global signed conjunction refuted alln>=5; explicit parity-selected K_PS signed law and first-vertex existence proved alln>=3 for actual admissible angles/evenell for evenn. Source open generic-sector distinction retained.','qualified_credited_note_route_authorized':True,'novelty_clearance':False,'historical_priority_clearance':False,'current_open_status_certified':False,'author_authenticated_erratum':False,'firstness_or_independent_discovery_certified':False,'claim_level':'Credited rederivation/verification; exact Ferudun theorem and convention/method overlap and classical inputs credited.','extensive_AI':True,'unrefereed':True,'conventional_human_peer_review':False,'operational_lifecycle_gate_still_required':True,'actual_Zenodo_published':False,'actual_DOI':None,'actual_tracker_updated':False,'actual_PR_merged':False,'case_percent':80,'completed':39,'published':23,'goal_complete':False}
save(A/'ROOT_SCIENTIFIC_PUBLICATION_CLEARANCE.json',science)
print(json.dumps({'status':science['status'],'owned_second_review_files':len(actual),'two_fresh_whole_package_passes':True,'actual_published':False,'clearance':pin(A/'ROOT_SCIENTIFIC_PUBLICATION_CLEARANCE.json')}))
