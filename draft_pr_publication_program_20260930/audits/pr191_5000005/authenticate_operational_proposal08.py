"""Authenticate frozen08 bytes for independent review; no service authority."""
from pathlib import Path
import datetime,hashlib,json,stat
A=Path(__file__).resolve().parent;F=A/'lifecycle_controls_preparation_08'
def require(x,m):
 if not x:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
require(pin(F/'FINAL_SEAL.json')['sha256']=='ec4f6196e8a299418eccea088395e61d64419f42d9569689579da6a41efdd4df','Terminal seal drift')
seal=json.loads((F/'FINAL_SEAL.json').read_text());allow=json.loads((F/'PROPOSED_FILE_ALLOWLIST.json').read_text())['files']
names={x['path'] for x in seal['manifest']}|{'FINAL_SEAL.json'}
require(set(allow)==names and len(allow)==len(names)==19,'Exact public inventory mismatch')
for x in seal['manifest']:require(pin(F/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Owned bytes drift '+x['path'])
for n in names:require(stat.S_IMODE((F/n).stat().st_mode)==0o444 and not (F/n).is_symlink(),'Mode/symlink drift '+n)
require(len(seal['runtime_pins'])==9,'Runtime inventory')
for n,x in seal['runtime_pins'].items():require(pin(F/n)==x,'Runtime drift '+n)
handoff=A/'prepare_root_publication_clearance_v7.py'
require(pin(handoff)=={'bytes':8943,'sha256':'2536efb0005ef1036c15634dd37f5596cf45fcc5e1968bbea84913397a37c372'},'Handoff drift')
require(pin(A/'IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS06_01.json')==seal['operations06_seed644'],'Seed drift')
require(pin(A/'lifecycle_adversary_07/FINAL_REVIEW_07.md')==seal['terminal_review07_read_before_freeze'],'Terminal07 report drift')
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'PR':191,'status':'FROZEN_OPERATIONAL_PROPOSAL08_BYTES_AUTHENTICATED_NEW_INDEPENDENT_REVIEW_ACTIVE_NOT_AUTHORITY','proposal_seal':pin(F/'FINAL_SEAL.json'),'runtime_common':pin(F/'lifecycle_common.py'),'owned_files_authenticated':19,'runtime_files':9,'Root_read_entire_author_report_entire07_to08_runtime_delta_and_entire_current_contract':True,'Root_static_source_and_seal_binding_checks_complete':True,'Root_handoff':{'path':handoff.name,**pin(handoff)},'NEW_independent_review':'lifecycle_adversary_08','author_test_count_is_not_independent_approval':True,'case_percent':80,'canonical_runtime_installed':False,'actual_operational_clearance_or_publication_gate_created':False,'actual_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'fully_completed_count':39,'published_count':23,'two_clean_NEW_science_reviews_unchanged':True,'review06_terminal_incomplete_not_clearance':True,'goal_complete':False}
p=A/'ROOT_OPERATIONAL_PROPOSAL08_AUTHENTICATION.json';require(not p.exists(),'Never overwrite receipt')
p.write_text(json.dumps(out,indent=2)+'\n');p.chmod(0o444)
case=json.loads((A/'CURRENT_CASE_STATUS.json').read_text())
case.update(UTC=out['UTC'],status='SCIENTIFIC_PACKAGE_READY_FROZEN_OPERATIONAL_REPAIR08_UNDER_NEW_INDEPENDENT_REVIEW',case_percent=80,publication_ready=False,operational_lifecycle_audit_active=True,operational_proposal08_Root_authentication=p.name,remaining_required_steps='Complete NEW independent08 ordinary data-format/workflow review; actual exact-kit Zenodo DOI/tracker, original-head MAIN merge and factual full-current-MAIN acceptance before192.')
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+out['UTC']+' — PR191 workflow80%: frozen08 authenticated (19 owned files, exact9 proposed controls, all0444). Root read the entire current contract, full author report and entire07-to08 source delta; sealed static checks and unchanged constructor/adapters verified. Current merge receipt DOI/type and selected-map count match approved publication/map context; other runtime controls and seven pure constructors unchanged. NEW08 independent reviewer active. Earlier06 review remains incomplete, not clearance. Author721 controls are evidence only. Two clean whole-science reviews and all frozen scientific bytes unchanged. No canonical runtime/Root baseline/clearance/gate, actual services/PR/merge or192 action;39/23 unchanged.\n')
print(json.dumps(out))

