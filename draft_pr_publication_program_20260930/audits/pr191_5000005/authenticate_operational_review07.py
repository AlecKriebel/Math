"""Authenticate independent07's bounded terminal findings; no clearance."""
from pathlib import Path
import datetime,hashlib,json,stat
A=Path(__file__).resolve().parent;D=A/'lifecycle_adversary_07'
def require(x,m):
 if not x:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def check(p,x):require(pin(p)=={k:x[k] for k in ['bytes','sha256']},'Binding drift '+str(p))
require(pin(D/'FINAL_SEAL_07.json')=={'bytes':2938,'sha256':'116c7f6e922ae7e240529b326d4bb3bcb5ddc6a2e6956d9b2a0701cc44afe3b6'},'Terminal seal drift')
seal=json.loads((D/'FINAL_SEAL_07.json').read_text())
require(seal['status']=='REPAIR_REQUIRED' and seal['cases']==435 and seal['expected_outcomes']==429 and seal['unexpected_acceptances']==6 and seal['unexpected_rejections']==0,'Terminal outcomes drift')
for x in seal['files']:check(D/x['path'],x)
allow=json.loads((D/'PUBLIC_SAFE_ALLOWLIST.json').read_text())['files']
require(len(allow)==12 and set(allow)=={x['path'] for x in seal['files']}|{'FINAL_SEAL_07.json'},'Exact safe inventory')
for n in allow:require(not (D/n).is_symlink() and stat.S_IMODE((D/n).stat().st_mode)==0o444,'Owned mode drift '+n)
source=json.loads((D/'SOURCE_VERIFICATION_07.json').read_text())
for x in source['runtime_files']:check(A/'lifecycle_controls_preparation_07'/x['path'],x)
for n,k in [('lifecycle_controls_preparation_07/FINAL_SEAL.json','source_seal_sha256'),('lifecycle_controls_preparation_07/GATE_CONTRACT.md','contract_sha256'),('prepare_root_publication_clearance_v6.py','paired_handoff_sha256'),('IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS06_01.json','dated_seed_sha256')]:require(pin(A/n)['sha256']==source[k],'Input drift '+n)
stamp=datetime.datetime.now(datetime.UTC).isoformat()
out={'UTC':stamp,'PR':191,'status':'ROOT_AUTHENTICATED_NEW_OPERATIONAL_REVIEW07_REPAIR_REQUIRED','report':{'path':'lifecycle_adversary_07/FINAL_REVIEW_07.md',**pin(D/'FINAL_REVIEW_07.md')},'seal':{'path':'lifecycle_adversary_07/FINAL_SEAL_07.json',**pin(D/'FINAL_SEAL_07.json')},'proposal_seal':{'path':'lifecycle_controls_preparation_07/FINAL_SEAL.json',**pin(A/'lifecycle_controls_preparation_07/FINAL_SEAL.json')},'public_safe_owned_files_authenticated':12,'Root_read_entire_report_and_execution_log':True,'independent_cases':435,'expected_outcomes':429,'unexpected_acceptances':6,'required_repairs':seal['required_repairs'],'actual_factual_prepare_and_factual_accept_reproductions':True,'separate_repair_generation':'lifecycle_controls_preparation_08','NEW_independent_plan_already_sealed':'lifecycle_adversary_08','two_clean_NEW_science_reviews_unchanged':True,'canonical_runtime_installed':False,'actual_operational_clearance_or_publication_gate_created':False,'actual_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'case_percent':79,'fully_completed_count':39,'published_count':23,'goal_complete':False}
p=A/'ROOT_OPERATIONAL_REVIEW07_REPAIR_REQUIRED.json'
with p.open('x') as f:f.write(json.dumps(out,indent=2)+'\n')
p.chmod(0o444)
case=json.loads((A/'CURRENT_CASE_STATUS.json').read_text())
case.update(UTC=stamp,status='SCIENTIFIC_PACKAGE_READY_REPAIRING_CURRENT_MERGE_RECEIPT_DOI_AND_COUNT',case_percent=79,publication_ready=False,operational_lifecycle_audit_active=True,operational_required_repairs=seal['required_repairs'],operational_review07_Root_authentication=p.name,operational_review07_report='lifecycle_adversary_07/FINAL_REVIEW_07.md',remaining_required_steps='Exact current merge receipt DOI/type/map-count checks, NEW08 ordinary workflow review; actual Zenodo DOI/tracker/original-head MAIN merge and full factual acceptance before192.')
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+stamp+' — PR191 workflow79%: Root read full terminal07 report/execution log; authenticated12 safe0444 artifacts and exact source/handoff/seed bindings.435 cases:429 expected,6 wrong acceptances from current merge receipt DOI scalar/type and selected-map count omissions. Each reproduced through actual factual preparation/acceptance; complete valid lifecycle and unchanged-native100 stale-parent retry pass. Narrow08 repair tested by author; distinct08 pre-inspection plan sealed, awaiting exact08 source. Unchanged scientific package and two whole-science PASS reviews. No actual authority/runtime/services/PR/merge/192 action;39/23 unchanged.\n')
print(json.dumps(out))

