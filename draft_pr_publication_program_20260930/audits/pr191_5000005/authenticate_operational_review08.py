"""Authenticate the terminal independent08 PASS and global concrete repair closure."""
from pathlib import Path
import datetime,hashlib,json,stat
A=Path(__file__).resolve().parent;D=A/'lifecycle_adversary_08'
def require(v,m):
 if not v:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def check(p,x):require(pin(p)=={k:x[k] for k in ['bytes','sha256']},'Binding drift '+str(p))
require(pin(D/'FINAL_SEAL_08.json')=={'bytes':1474,'sha256':'d527cf3a9848c8a1e09cbe3eca37ce1ed67ea00650f0d6577a2d444ed5c0f2c6'},'Independent seal drift')
seal=json.loads((D/'FINAL_SEAL_08.json').read_text())
require(seal['disposition']=='PASS' and seal['checks_passed']==74 and seal['checks_failed']==0 and seal['required_concrete_defects']==0 and seal['sealed_reproduction_matched'] is True,'Final independent disposition drift')
check(D/seal['manifest']['path'],seal['manifest']);check(D/seal['report']['path'],seal['report'])
manifest=json.loads((D/'MANIFEST.json').read_text())
for n,x in manifest['files'].items():check(D/n,x)
allow=json.loads((D/'PUBLIC_SAFE_ALLOWLIST.json').read_text())['files']
require(set(allow)==set(manifest['files'])|{'MANIFEST.json','FINAL_SEAL_08.json'} and len(allow)==11,'Exact independent safe scope mismatch')
for n in allow:require(not (D/n).is_symlink() and stat.S_IMODE((D/n).stat().st_mode)==0o444,'Mode/symlink drift '+n)
for x in json.loads((D/'INPUT_PINS.json').read_text())['inputs']:check(Path(x['path']),x);require(stat.S_IMODE(Path(x['path']).stat().st_mode)==0o444,'Input mode drift')
proposal=A/'lifecycle_controls_preparation_08/FINAL_SEAL.json'
require(pin(proposal)['sha256']==seal['proposal_seal_sha256']=='ec4f6196e8a299418eccea088395e61d64419f42d9569689579da6a41efdd4df','Proposal drift')
for x in json.loads(proposal.read_text())['manifest']:check(proposal.parent/x['path'],x)
kit=Path('/Users/alec/Documents/Math/zenodo_deposit_tool')
require(pin(kit/'zenodo.py')=={'bytes':25740,'sha256':'a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'},'Exact kit source drift')
require(pin(kit/'README.md')=={'bytes':14761,'sha256':'b022bb5470ab951b56fbded771df087f3cdb85e7188783a84fae085d26a8873f'},'Exact kit README drift')
stamp=datetime.datetime.now(datetime.UTC).isoformat()
out={'UTC':stamp,'PR':191,'original_head':'a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe','status':'ROOT_AUTHENTICATED_NEW_OPERATIONAL_REVIEW08_PASS','all_required_findings_globally_resolved':True,'outstanding_required_repairs':[],'report':{'path':'lifecycle_adversary_08/FINAL_REVIEW_08.md',**pin(D/'FINAL_REVIEW_08.md')},'seal':{'path':'lifecycle_adversary_08/FINAL_SEAL_08.json',**pin(D/'FINAL_SEAL_08.json')},'proposal_seal':{'path':'lifecycle_controls_preparation_08/FINAL_SEAL.json',**pin(proposal)},'Root_read_entire_independent_report':True,'Root_reviewed_entire_runtime_delta_contract_and_author_report':True,'independent_checks_passed':74,'independent_checks_failed':0,'safe_owned_files_authenticated':11,'global_concrete_repair_closure':['Original true-parent, full-delta and complete selected-current-map binding','Exact native scientific bytes; factual case/programme/log derivations and timestamps','Exact original QUEUE row transformation and foreign byte preservation','Pending95/100 factual receipt/cursor aliases and immutable native100 retry','Canonical own-only public dynamic service/control record schemas','Current original merge receipt exact actual DOI string/type and validated original map count'],'review06_remains_incomplete_historical_evidence_not_a_PASS':True,'exact_kit':{'source':pin(kit/'zenodo.py'),'README':pin(kit/'README.md'),'Root_static_saved_state_stage_inspect_publish_logic_read':True,'recovery_boundary':'Restage reuses the existing ID only while the exact-manifest/environment saved state remains intact; unknown/missing state or unresolved observation stops. No concurrent state writer assumed. No blind create/publish retry. Published DOI assignment is separate from resolver availability.'},'two_clean_NEW_whole_science_package_reviews_unchanged':True,'qualified_fully_credited_note_only':True,'novelty_priority_independence_firstness_certified':False,'actual_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'case_percent':85,'fully_completed_count':39,'published_count':23,'goal_complete':False}
p=A/'ROOT_OPERATIONAL_REVIEW08_AUTHENTICATION.json'
with p.open('x') as f:f.write(json.dumps(out,indent=2)+'\n')
p.chmod(0o444)
case=json.loads((A/'CURRENT_CASE_STATUS.json').read_text())
case.update(UTC=stamp,status='SCIENTIFIC_PACKAGE_AND_OPERATIONAL_CONTROLS_CLEARED_PENDING_ROOT_GATE_AND_ACTUAL_PUBLICATION',case_percent=85,operational_lifecycle_audit_active=False,operational_required_repairs=[],operational_review08_Root_authentication=p.name,operational_review08_report='lifecycle_adversary_08/FINAL_REVIEW_08.md',publication_ready=False,remaining_required_steps='Root exclusive ready gate; actual exact-kit Zenodo DOI, tracker, original-head MAIN merge and factual current-MAIN acceptance before192.')
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+stamp+' — PR191 workflow85%: Root read entire NEW independent08 terminal PASS and authenticated11 safe0444 artifacts plus all13 input bindings;74/74 expected behaviors, zero required defects, sealed replay matched. Prior concrete repairs globally closed by current exact controls and unchanged whole-science PASS01/PASS02. Exact repository kit source/README hashes and saved-state recovery logic rechecked; external response/concurrency boundaries explicit. Qualified fully credited note only; no novelty/priority/firstness/independence certification. Root v7 may now issue ready authority. No actual publication/tracker/PR merge/factual acceptance/192 action yet;39/23 unchanged.\n')
print(json.dumps(out))

