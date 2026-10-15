"""Authenticate frozen04 for independent review, without operational authority."""
from pathlib import Path
import datetime,hashlib,json,stat
A=Path(__file__).resolve().parent;F=A/'lifecycle_controls_preparation_04'
def require(x,m):
 if not x:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
require(pin(F/'FINAL_SEAL.json')['sha256']=='3c9f2386caabaeb53fcacdce97625386c64b67866d9b958be29264a372b3605b','Terminal seal drift')
seal=json.loads((F/'FINAL_SEAL.json').read_text());allow=json.loads((F/'PROPOSED_FILE_ALLOWLIST.json').read_text())['files'];names={x['path'] for x in seal['manifest']}|{'FINAL_SEAL.json'}
require(set(allow)==names and len(allow)==len(names),'Exact public owned inventory mismatch')
for x in seal['manifest']:require(pin(F/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Owned bytes drift '+x['path'])
for n in names:require(stat.S_IMODE((F/n).stat().st_mode)==0o444 and not (F/n).is_symlink(),'Owned mode/symlink drift '+n)
for n,x in seal['runtime_pins'].items():require(pin(F/n)==x,'Runtime pin drift '+n)
handoff=A/'prepare_root_publication_clearance_v2.py';require(pin(handoff)=={'bytes':7821,'sha256':'6df49335d56f411836ca1206e2cfca04817bf84c6c5cf5e9d47750818c50aac5'},'Root handoff bytes drift')
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'PR':191,'status':'FROZEN_OPERATIONAL_PROPOSAL04_BYTES_AUTHENTICATED_NEW_INDEPENDENT_REVIEW_ACTIVE_NOT_AUTHORITY','proposal_seal':pin(F/'FINAL_SEAL.json'),'runtime_common':pin(F/'lifecycle_common.py'),'owned_files_authenticated':len(names),'runtime_files':len(seal['runtime_pins']),'Root_read_current_runtime_delta_all_new_functions_all_adapters_contract_and_entire_author_report':True,'Root_verified_exact_kit_published_receipt_schema_against_prior_actual190_output':True,'Root_handoff':{'path':handoff.name,**pin(handoff)},'NEW_independent_review':'lifecycle_adversary_04','author_test_count_is_not_independent_approval':True,'case_percent':80,'canonical_runtime_installed':False,'actual_operational_clearance_or_publication_gate_created':False,'actual_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'fully_completed_count':39,'published_count':23,'two_clean_NEW_science_reviews_unchanged':True,'goal_complete':False}
p=A/'ROOT_OPERATIONAL_PROPOSAL04_AUTHENTICATION.json';require(not p.exists(),'Never overwrite receipt');p.write_text(json.dumps(out,indent=2)+'\n');p.chmod(0o444)
case=json.loads((A/'CURRENT_CASE_STATUS.json').read_text());case.update(UTC=out['UTC'],status='SCIENTIFIC_PACKAGE_READY_FROZEN_OPERATIONAL_REPAIR04_UNDER_NEW_INDEPENDENT_REVIEW',case_percent=80,publication_ready=False,operational_lifecycle_audit_active=True,operational_proposal04_Root_authentication=p.name,remaining_required_steps='Complete NEW independent04 operations audit and global repairs; actual exact-kit Zenodo DOI/tracker, original-head MAIN merge and factual full-current-MAIN acceptance before192.')
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+out['UTC']+' — PR191 workflow80%: frozen04 authenticated (18 owned files, exact9 proposed controls, all0444), Root read full author report/contract, current code delta and all new functions/adapters. Exact full-file native derivation, live cursor191 in95/100, fresh actual service observations/evidence and live operations alias cleanup proposed; NEW04 independently preplanned adversary actively reviewing exact freeze and inert Root handoff. Author384 focused controls are evidence, not clearance. Exact science packet and two whole-package clean reviews unchanged. No actual runtime installation/Root clearance/gate, publication/DOI/tracker/PR metadata/ready/merge or192 intake;39/23 unchanged.\n')
print(json.dumps(out))
