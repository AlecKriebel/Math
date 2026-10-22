"""Authenticate frozen05 for independent review, without operational authority."""
from pathlib import Path
import datetime,hashlib,json,stat
A=Path(__file__).resolve().parent;F=A/'lifecycle_controls_preparation_05'
def require(x,m):
 if not x:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
require(pin(F/'FINAL_SEAL.json')['sha256']=='de78b12cf2cf954aa205f17177ffc38bc07464fdc71b9234c17dc7429b009a91','Terminal seal drift')
seal=json.loads((F/'FINAL_SEAL.json').read_text());allow=json.loads((F/'PROPOSED_FILE_ALLOWLIST.json').read_text())['files'];names={x['path'] for x in seal['manifest']}|{'FINAL_SEAL.json'}
require(set(allow)==names and len(allow)==len(names),'Exact public owned inventory mismatch')
for x in seal['manifest']:require(pin(F/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Owned bytes drift '+x['path'])
for n in names:require(stat.S_IMODE((F/n).stat().st_mode)==0o444 and not (F/n).is_symlink(),'Owned mode/symlink drift '+n)
for n,x in seal['runtime_pins'].items():require(pin(F/n)==x,'Runtime pin drift '+n)
handoff=A/'prepare_root_publication_clearance_v4.py';require(pin(handoff)=={'bytes':8358,'sha256':'c4f8f2c122e1954d3f3d5cf03d70cd0fe8a243e368efa166171c4aca97f4b548'},'Root handoff bytes drift')
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'PR':191,'status':'FROZEN_OPERATIONAL_PROPOSAL05_BYTES_AUTHENTICATED_NEW_INDEPENDENT_REVIEW_ACTIVE_NOT_AUTHORITY','proposal_seal':pin(F/'FINAL_SEAL.json'),'runtime_common':pin(F/'lifecycle_common.py'),'owned_files_authenticated':len(names),'runtime_files':len(seal['runtime_pins']),'Root_read_current_runtime_delta_all_new_functions_all_adapters_contract_and_entire_author_report':True,'Root_verified_exact_kit_published_receipt_schema_against_prior_actual190_output':True,'Root_handoff':{'path':handoff.name,**pin(handoff)},'NEW_independent_review':'lifecycle_adversary_05','author_test_count_is_not_independent_approval':True,'case_percent':80,'canonical_runtime_installed':False,'actual_operational_clearance_or_publication_gate_created':False,'actual_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'fully_completed_count':39,'published_count':23,'two_clean_NEW_science_reviews_unchanged':True,'goal_complete':False}
p=A/'ROOT_OPERATIONAL_PROPOSAL05_AUTHENTICATION.json';require(not p.exists(),'Never overwrite receipt');p.write_text(json.dumps(out,indent=2)+'\n');p.chmod(0o444)
case=json.loads((A/'CURRENT_CASE_STATUS.json').read_text());case.update(UTC=out['UTC'],status='SCIENTIFIC_PACKAGE_READY_FROZEN_OPERATIONAL_REPAIR05_UNDER_NEW_INDEPENDENT_REVIEW',case_percent=80,publication_ready=False,operational_lifecycle_audit_active=True,operational_proposal05_Root_authentication=p.name,remaining_required_steps='Complete NEW independent05 operations audit and global repairs; actual exact-kit Zenodo DOI/tracker, original-head MAIN merge and factual full-current-MAIN acceptance before192.')
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+out['UTC']+' — PR191 workflow80%: frozen05 authenticated (18 owned files, exact9 proposed controls, all0444); Root read the entire author report/contract, all runtime changes and unchanged adapters. Exact true-parent QUEUE postimage rederivation and both programme-date evidence bounds/order are added at consumption boundaries. NEW05 independently preplanned adversary is reviewing this freeze with inert Root handoff v4. Author440 controls are evidence, not clearance. Scientific proof, packet and two clean whole-package reviews unchanged. No canonical runtime/Root clearance/gate, actual publication/DOI/tracker/PR metadata/ready/merge or192 intake;39/23 unchanged.\n')
print(json.dumps(out))
