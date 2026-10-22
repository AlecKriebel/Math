"""Authenticate a frozen proposal without granting operational approval."""
from pathlib import Path
import datetime,hashlib,json,stat
A=Path(__file__).resolve().parent
def require(x,m):
 if not x:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
F=A/'lifecycle_controls_preparation_02';seal=json.loads((F/'FINAL_SEAL.json').read_text())
require(pin(F/'FINAL_SEAL.json')['sha256']=='f9aee609fec7ee494dd7bf0dd65ff344ec45d27f1a91b3040179618e7f5bc03a','Terminal seal mismatch')
names=set(json.loads((F/'PROPOSED_FILE_ALLOWLIST.json').read_text())['files'])
require(names=={x['path'] for x in seal['manifest']}|{'FINAL_SEAL.json'},'Owned inventory mismatch')
for x in seal['manifest']:
 p=F/x['path'];require(pin(p)=={k:x[k] for k in ['bytes','sha256']},'Owned hash mismatch '+x['path'])
for n in names:require(stat.S_IMODE((F/n).stat().st_mode)==0o444,'Owned mode mismatch '+n)
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'PR':191,'status':'FROZEN_PROPOSAL02_BYTES_AUTHENTICATED_NOT_OPERATIONAL_APPROVAL','seal':pin(F/'FINAL_SEAL.json'),'owned_files':len(names),'all_mode_0444':True,'Root_read_entire_runtime_and_author_report':True,'independent_adversary02_active':True,'independent_adversary02_confirmed_native_factual_path_exemption_requires_repair':True,'source_package_unchanged':True,'canonical_runtime_installed':False,'actual_publication_gate_created':False,'actual_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'case_percent':77,'fully_completed_count':39,'published_count':23,'goal_complete':False}
p=A/'ROOT_OPERATIONAL_PROPOSAL02_AUTHENTICATION.json';require(not p.exists(),'Receipt already exists');p.write_text(json.dumps(out,indent=2)+'\n');p.chmod(0o444)
case=json.loads((A/'CURRENT_CASE_STATUS.json').read_text());case.update(UTC=out['UTC'],status='SCIENTIFIC_PACKAGE_READY_REPAIRING_SECOND_OPERATIONAL_ADVERSARY_FINDINGS',case_percent=77,operational_lifecycle_audit_active=True,publication_ready=False,remaining_required_steps='Repair frozen02 factual-field validation and finish fresh operations review; actual publication, tracker, original-head merge and factual full-MAIN acceptance before intake192.')
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+out['UTC']+' — PR191 workflow77%: Root read and authenticated frozen02 code, contract and author report (18 owned immutable files). NEW independent adversary02 reproduced a scientific-field validation gap in the current native template: known factual files were exempted as whole paths. Generation03 factual-key/complete-byte repair in progress, while02 reviewer completes independent coverage. The two clean whole mathematical/package reviews and exact publication packet remain unchanged. No actual Zenodo publication, DOI, tracker append, PR metadata/ready/merge or192 intake;39completed/23published unchanged.\n')
print(json.dumps(out))
